# ブラウザの保存領域 (OPFS、IndexedDB、StorageManager)

対象: OPFS (同期アクセスハンドルを含む)、IndexedDB、Cache Storage の容量の扱い、StorageManager (estimate、persist)、Storage Buckets、File System Access API、退避 (eviction) の規則 (Safari の 7 日規則を含む)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 仕様と標準化の段階 (W3C / WHATWG / WICG、草案か勧告か) | StorageManager (`estimate`、`persist`、`persisted`) と quota・退避の枠組みは WHATWG Storage Living Standard。OPFS (`navigator.storage.getDirectory()`、`FileSystemSyncAccessHandle`、`createWritable`) は WHATWG File System Living Standard (2026-10-19 更新)。ファイル選択 (`showOpenFilePicker` など) と `requestPermission` は WICG の File System Access 草案。IndexedDB は W3C で、TR の IndexedDB と IndexedDB 3.0 はどちらも Working Draft (2026-10-30 更新)。Storage Buckets は WICG の草案。Cache Storage は W3C Service Workers (Candidate Recommendation Draft) |
| Baseline の状態 (Widely available / Newly available / 未達) | IndexedDB は Widely available (2024-03-20)。Storage manager (`estimate` を含む) は Widely available (2026-03-18、Safari 17 で揃った)。OPFS は Widely available (2025-09-27、Safari 16.4 で揃った)。File System Access (ファイル選択、`FileSystemWritableFileStream` を含む機能のまとまり) は未達。Storage Buckets は未達。IndexedDB の `getAllRecords()` は未達 |

## ブラウザの対応

API ごとに、対応した版を書く。iOS では全ブラウザが WebKit を使うので、iOS Safari の欄が iOS 全体の対応になる (EU では iOS 17.4 以降、別エンジンのブラウザが許されている)。版は MDN browser-compat-data 8.1.8 (2026-11-02 生成) による。Edge は Chromium 版で、Chrome と同じ版から使える。

| API | Chrome / Edge | Firefox | Safari (macOS) | Safari (iOS / iPadOS) | Android の WebView | 出典 |
|---|---|---|---|---|---|---|
| IndexedDB (`indexedDB`) | 24 (Baseline の基準は 58) | 16 (基準は 51) | 8 (基準は 15) | 8 (基準は 15) | 4.4 | MDN BCD `api.IDBFactory`、web-features `indexeddb` |
| IndexedDB の `durability` (トランザクションの耐久性指定) | 83 | 126 | 15 | 15 | 83 | MDN BCD `api.IDBTransaction.durability` |
| IndexedDB の `getAllRecords()` | 141 | 153 | Technology Preview のみ | 未対応 | 141 | MDN BCD `api.IDBObjectStore.getAllRecords` |
| `navigator.storage.persist()` / `persisted()` | 55 | 57 | 15.2 | 15.2 | 55 | MDN BCD `api.StorageManager.persist` |
| `navigator.storage.estimate()` | 61 | 57 | 17 | 17 | 61 | MDN BCD `api.StorageManager.estimate` |
| OPFS (`navigator.storage.getDirectory()`) | 86 (機能としての基準は 108、Android 109) | 111 | 15.2 (機能としての基準は 16.4) | 15.2 (基準は 16.4) | 109 | MDN BCD `api.StorageManager.getDirectory`、web-features `origin-private-file-system` |
| OPFS の同期アクセスハンドル (`createSyncAccessHandle`、`FileSystemSyncAccessHandle`) | 102 | 111 | 15.2 | 15.2 | 109 | MDN BCD `api.FileSystemSyncAccessHandle` |
| `createSyncAccessHandle` の `mode` 指定 (複数ハンドルの同時オープン) | 121 | 未対応 | 未対応 | 未対応 | (BCD に記載なし) | MDN BCD `api.FileSystemFileHandle.createSyncAccessHandle.mode` |
| `createWritable()` / `FileSystemWritableFileStream` | 86 | 111 | 26 | 26 | 109 | MDN BCD `api.FileSystemFileHandle.createWritable` |
| `FileSystemHandle.move()` | 102 (ファイルだけ、ディレクトリは不可) | 111 | 15.2 | 15.2 | 109 | MDN BCD `api.FileSystemHandle.move` |
| ファイル選択 (`showOpenFilePicker`、`showSaveFilePicker`、`showDirectoryPicker`) と `requestPermission` | 86 (Android の Chrome は 132) | 未対応 | 未対応 | 未対応 | 132 (`requestPermission` は 109) | MDN BCD `api.Window.showOpenFilePicker`、web-features `file-system-access` |
| `FileSystemObserver` (ファイルの変更通知) | 133 | 未対応 | 未対応 | 未対応 | 未対応 | MDN BCD `api.FileSystemObserver` |
| Storage Buckets (`navigator.storageBuckets`) | 122 | 未対応 (bug 1594740) | 未対応 | 未対応 | 122 | MDN BCD `api.StorageBucketManager` |
| Cache Storage (容量は他と共通) | 43 | 41 | 11.1 | 11.3 | 43 | MDN BCD `api.CacheStorage` |

## 概要

ブラウザは IndexedDB、Cache Storage、OPFS などのデータをオリジンごとにまとめて管理し、オリジン単位の割り当て (quota) と退避 (eviction) をかける。OPFS はオリジン専用の隠れたファイルシステムで、権限の確認なしに大きなバイナリファイルを置け、Web Worker の中では同期アクセスハンドルで任意の位置を読み書きできるので、SQLite や DuckDB の Wasm 版がデータベースファイルを直接置ける。StorageManager の `estimate()` で使用量と上限の見積もりを、`persist()` で「保存領域の圧迫で消されない」永続モードを求められる。File System Access のファイル選択はユーザーの実ファイルを開いて書き戻す API で、Chromium 系だけにある。

## 地図プロダクトでの使いどころ

保存、計算、表現のどれを、ブラウザ・アプリの層に置けるようにするか。

- 保存: 地域単位の PMTiles や MBTiles、数百 MB から GB 級の GeoParquet、DuckDB や SQLite のデータベースファイルを OPFS に置ける。上限は Chrome でオリジンあたり総ディスクの 60%、Safari 17 以降で 60% なので、端末の空きがあれば GB 級も入る。ただし best-effort のままだと容量の圧迫で消えうるので、`persist()` を求め、`estimate()` で残りを確かめてからダウンロードする。少量の構造化データ (お気に入り地点、現地調査の入力、タイルの索引) は IndexedDB が向く。
- 計算: Web Worker の中で SQLite Wasm (opfs-sahpool VFS) や DuckDB-Wasm (`opfs://` パス) を OPFS 上のファイルで動かし、属性検索、空間の絞り込み、集計を端末で済ませられる。PMTiles JS の `FileSource` は `File` を受け取るので、OPFS の `getFile()` で得た `File` を渡せば、ネットワークなしでタイルを読める (`FileSource` が `File` を受け取ることはソースで確認、OPFS の `File` で動くことは推測)。
- 表現: Chromium 系ではファイル選択でユーザーの手元の GeoJSON や PMTiles を開き、編集結果を同じファイルに書き戻すデスクトップアプリ風の地図エディタを作れる。Safari と Firefox ではファイル選択 API がないので、`<input type="file">` で読み、ダウンロードで書き出す形になる。

## 制約

- 容量と寿命:
  - 割り当ての対象は IndexedDB、Cache Storage、OPFS で、オリジン全体で合算される。`localStorage` / `sessionStorage` はそれぞれ 5 MiB の別枠 (MDN)。
  - Chrome と Edge: オリジンあたり総ディスクの最大 60% (best-effort でも persistent でも)。ブラウザ全体で総ディスクの 80% を超えると、best-effort のオリジンを最も長く使われていない順 (LRU) に消す。
  - Firefox: best-effort は総ディスクの 10% か 10 GiB の小さい方 (同じサイトのオリジンで共有する group limit)。persistent は総ディスクの 50%、上限 8 TiB で、group limit を受けない。
  - Safari (macOS 14 / iOS 17 以降、Safari 17.0 から): ブラウザアプリはオリジンあたり総ディスクの約 60%、全体で 80%。WKWebView など Web を表示するほかのアプリはオリジンあたり約 15%、全体で 20%。ホーム画面と Dock の Web アプリはブラウザアプリと同じ枠。クロスオリジンの iframe は親の 10%。上限を超えると `QuotaExceededError`。Safari 17.0 から容量追加の確認ダイアログは出なくなった (それ以前は 1 GiB を超えると確認していた)。
  - 上限は空き容量でなく総ディスクに対する割合で決まるので、実際には上限まで入らないことがある。フィンガープリント対策で値が少しずれる。
  - 退避はオリジン単位で全部まとめて消える (IndexedDB だけ残る、ということはない)。容量の圧迫による退避は LRU で、persistent のオリジンは対象外。WebKit は開いているページがあるオリジンも対象外にする。
  - Safari の 7 日規則: 追跡防止が有効なとき、Safari を使った 7 日間にそのサイトでの操作 (クリックやタップ) がなければ、スクリプトで書いた保存領域 (IndexedDB、localStorage、sessionStorage、Media keys、Service Worker の登録とキャッシュ) を消す。サーバーが付けた Cookie は対象外。Safari 13.1 / iOS 13.4 から。ホーム画面に追加した Web アプリは Safari の一部ではなく、アプリの使用日数を別に数える。WebKit は「そうしたアプリのファーストパーティのデータが消えることは想定していない」と書いている。
- 権限とユーザーの操作が要るか: OPFS、IndexedDB、Cache Storage に権限の確認はない。`persist()` は Firefox では確認のポップアップを出す。Chrome、Edge、Safari は確認を出さず、サイトとのやりとりの履歴などで自動的に許可か拒否を決める。WebKit はホーム画面の Web アプリとして開かれているかを判断材料の例に挙げている。ファイル選択はユーザーの操作が要り、書き込みには権限の確認が出る。
- セキュアコンテキスト、クロスオリジン分離 (COOP/COEP) などの前提: OPFS は HTTPS (セキュアコンテキスト) が要る。同期アクセスハンドルは専用 Web Worker の中だけで使える。OPFS 自体に COOP/COEP は要らないが、SQLite Wasm の `opfs` VFS は `SharedArrayBuffer` を使うので COOP/COEP が要る。同じ SQLite の `opfs-sahpool` VFS は要らない。
- iOS / Safari での制限: `estimate()` は Safari 17 から。`createWritable()` は Safari 26 から。ファイル選択 API、Storage Buckets、`FileSystemObserver` はない。7 日規則があるので、Safari のタブで使うオフライン地図は、1 週間開かないと丸ごと消えうる。SQLite Wasm の `opfs` VFS は Safari 17 未満で動かない (WebKit のサブワーカーの不具合)。
- WebView (アプリに埋め込んだブラウザ) での制限: iOS の WKWebView はオリジンあたり約 15%、全体で 20% と、Safari より小さい。Android の WebView は OPFS が 109、ファイル選択が 132 から。Android の WebView の quota と退避の規則は、MDN と Chrome の文書では確かめられなかった (未確認のこと)。

## 地図の実装例

この API を使っている OSS やライブラリ (地図ライブラリ、PMTiles、DuckDB-Wasm など)。

- DuckDB-Wasm (MIT、最新リリース v1.33.0、2025-12-16): `opfs://` で始まるファイル名を `DuckDBDataProtocol.BROWSER_FSACCESS` として扱い、`navigator.storage.getDirectory()` からハンドルを取り、`createSyncAccessHandle()` で開く。設定に `opfs.fileHandling` (`auto` / `manual`) と `homeDirectory` (`opfs://home`) がある。リモートのファイルは `registerFileURL()` と `DuckDBDataProtocol.HTTP` で必要な部分だけ読み、ブラウザの CORS に従う。
- SQLite Wasm (SQLite はパブリックドメイン): `opfs` VFS (Worker の中、COOP/COEP が要る、複数タブ可、`SQLITE_BUSY` の処理が要る)、`opfs-sahpool` VFS (COOP/COEP 不要、OPFS の中で最も速い、同じデータベースへの同時接続は不可、3.50 で協調的な共有のための pause / unpause を追加)、`opfs-wl` (3.53.0 で追加、Web Locks を使う) がある。対応は Chromium 系 2022 年半ば以降、Firefox 111、Safari 16.4 以降 (`opfs` VFS は Safari 17 以降)。
- PMTiles JS (`pmtiles` 4.5.0、BSD-3-Clause): `FileSource` がブラウザの `File` から読む。OPFS に保存した PMTiles を `getFile()` で `File` にして渡す使い方ができる (推測)。
- MapLibre GL JS (BSD-3-Clause): v2.x までは Cache Storage にタイルを入れていた (`mapbox-tiles`)。v3.0.0 以降は持たない。詳細は service-worker.md。

## 落とし穴

- `estimate()` の値は見積もりで、クロスオリジンのデータは水増しされることがある。上限は保証ではないので、大きなダウンロードでも `QuotaExceededError` の処理が要る。
- 退避はオリジン単位の全消しなので、「タイルは消えてもいいがユーザーの入力は残したい」を同じオリジンの best-effort では実現できない。Chromium 系なら Storage Buckets で分けられる (ただし Chrome の実装は IndexedDB だけ)。他のブラウザでは、ユーザーの入力をサーバーへ送るか、`persist()` を求める。
- Firefox の best-effort は 10 GiB で頭打ちになる。全国規模のタイルをそのまま置く設計は Firefox で収まらない。
- 同期アクセスハンドルはファイルに排他ロックをかける (File System 仕様のロックの状態に `taken-exclusive` がある)。複数タブで同じ DuckDB / SQLite のファイルを開くと失敗する。Chrome 121 以降は `mode` で複数のハンドルを開けるが、他のブラウザにはない。
- OPFS のファイルはユーザーから見えず、OS のファイルとも一対一に対応しない。サイトデータの削除で OPFS も消える。ユーザーが「ダウンロードした地図」を自分で管理できると思っていると齟齬が出る。
- Safari では `persist()` を明示的な確認なしに判定するので、Safari のタブでは許可されない可能性がある。ホーム画面の Web アプリにすると許可されやすい (WebKit の記事は判断材料の例として挙げているだけで、必ず許可されるとは書いていない)。
- 書き込み中に容量が尽きた場合の部分書き込みを想定する。IndexedDB は `durability: "strict"` で電源断に強くできるが、遅くなる (推測。Chrome の Storage Buckets の記事は strict の利点と性能・電池の代償を述べている)。

## まだ使えないもの、これから使えるもの

提案中、Origin Trial 中、一部のブラウザだけのもの。

- Storage Buckets: Chrome 122 以降だけ。オプションは `persisted` と `durability` (`relaxed` が既定、`strict`)。Chrome の実装は IndexedDB だけで、Cache Storage や OPFS をバケットに入れることはまだできない。Firefox は実装の bug 1594740 がある。
- File System Access のファイル選択と `requestPermission`: Chromium 系だけ (Android の Chrome は 132 から)。Firefox と Safari は未実装。
- `FileSystemObserver`: Chrome 133 だけ。標準化の段階にない (BCD で standard_track が false)。
- `FileSystemHandle.remove()`: Chrome 110 だけ (標準化の段階にない)。
- `createSyncAccessHandle` の `mode` 指定: Chrome 121 だけ。
- IndexedDB の `getAllRecords()`: Chrome 141、Firefox 153。Safari は Technology Preview のみ。

## 出典

- https://unpkg.com/@mdn/browser-compat-data/data.json (MDN browser-compat-data 8.1.8、2026-11-02 生成。表の各版)
- https://unpkg.com/web-features/data.json (web-features。Baseline の状態と日付)
- https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria (各ブラウザの quota、best-effort と persistent、`persist()` の許可のしかた、LRU、Chrome 全体 80%、Safari の proactive eviction、オリジン単位の全消し、Web Storage の 5 MiB)
- https://webkit.org/blog/14403/updates-to-storage-policy/ (Safari 17.0 の quota 60% / 15% / 80% / 20%、ホーム画面の Web アプリ、iframe 10%、確認ダイアログの廃止、`persist()` の判断材料、開いているページの除外)
- https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/ (7 日規則の対象と、ホーム画面の Web アプリの別カウント)
- https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system (OPFS は権限の確認不要、quota に数えられる、サイトデータの削除で消える、同期 API は Worker の中だけ、HTTPS)
- https://fs.spec.whatwg.org/ (File System Living Standard、2026-10-19 更新、ロックの状態)
- https://storage.spec.whatwg.org/ (Storage Living Standard)
- https://www.w3.org/TR/IndexedDB/ と https://www.w3.org/TR/IndexedDB-3/ (Working Draft、2026-10-30)
- https://developer.chrome.com/docs/web-platform/storage-buckets (Chromium 122、`persisted`、`durability`、実装は IndexedDB だけ)
- https://sqlite.org/wasm/doc/trunk/persistence.md (`opfs` / `opfs-sahpool` / `opfs-wl` VFS の要件と制限、対応ブラウザ、Safari 17 未満の不具合)
- https://raw.githubusercontent.com/duckdb/duckdb-wasm/main/packages/duckdb-wasm/src/bindings/bindings_base.ts (`opfs://` と `createSyncAccessHandle()`)
- https://raw.githubusercontent.com/duckdb/duckdb-wasm/main/packages/duckdb-wasm/src/bindings/config.ts (`opfs.fileHandling`、`homeDirectory`)
- https://duckdb.org/docs/2.0/clients/wasm/data_ingestion.html (`registerFileURL()` と HTTP、CORS)
- https://raw.githubusercontent.com/protomaps/PMTiles/main/js/src/index.ts (`FileSource`)

## 未確認のこと

- Android の WebView の quota と退避の規則 (Chrome と同じ 60% か、アプリのデータ領域で別の制限がかかるか)。
- Safari のタブで `persist()` が実際にどの条件で許可されるか (WebKit は判断材料の例しか示していない)。
- Safari 18 以降で 7 日規則の扱いが変わったか (2020 年の記事以降の公式な更新は見つけていない)。
- Chrome の `persist()` の自動許可の現在の条件 (ブックマーク、インストール、通知の許可など)。
- Firefox と Safari の Storage Buckets への公式の立場 (standards-positions)。
- OPFS の `File` を PMTiles JS の `FileSource` に渡して大きなアーカイブを読む実装例と、その性能。
- DuckDB-Wasm の OPFS 対応が Safari と Firefox でどこまで動くか (公式文書で対応ブラウザを確かめられなかった)。
- iOS の EU で別エンジンのブラウザを使ったときの OPFS と quota の実際の値。
