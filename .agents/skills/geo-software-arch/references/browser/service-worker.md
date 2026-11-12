# Service Worker と Cache Storage

対象: Service Worker、Cache Storage、Background Fetch、Background Sync、Periodic Background Sync、Navigation Preload、Static Routing API、PWA のインストール

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 仕様と標準化の段階 (W3C / WHATWG / WICG、草案か勧告か) | Service Worker、Cache Storage、Navigation Preload、Static Routing (`InstallEvent.addRoutes`) は W3C Web Applications WG の Service Workers 仕様に入っている。TR 版は Candidate Recommendation Draft (2026-10-29 更新)、Editor's Draft も 2026-10-29 更新。Background Fetch、Background Sync、Periodic Background Sync は WICG の草案 (勧告への道筋はない)。Web App Manifest は W3C Working Draft (2026-11-06 更新)。`beforeinstallprompt` は WICG の Manifest Incubations、`navigator.install()` は WICG の Web Install / install element の提案 |
| Baseline の状態 (Widely available / Newly available / 未達) | Service workers (Cache Storage と Navigation Preload を含む) は Widely available (Newly available 2018-04-30、Widely 2020-10-30)。Service worker の JavaScript モジュール (`type: "module"`) は Newly available (2026-01-13、Firefox 147 で揃った)。Static Routing、Background Fetch、Background Sync、Periodic Background Sync、`beforeinstallprompt`、Web App Manifest、`navigator.install()` は未達 |

## ブラウザの対応

API ごとに、対応した版を書く。iOS では全ブラウザが WebKit を使うので、iOS Safari の欄が iOS 全体の対応になる (EU では iOS 17.4 以降、別エンジンのブラウザが許されている)。版は MDN browser-compat-data 8.1.8 (2026-11-02 生成) と web-features による。Edge は Chromium 版 (79 以降) を前提に、Chrome と同じ版から使えるものは「Chrome と同じ」と書く。

| API | Chrome / Edge | Firefox | Safari (macOS) | Safari (iOS / iPadOS) | Android の WebView | 出典 |
|---|---|---|---|---|---|---|
| Service Worker (`navigator.serviceWorker`、`FetchEvent`) | Chrome 40 / Edge 17 (EdgeHTML) | 44 | 11.1 | 11.3 | 40 | MDN BCD `api.ServiceWorker`、web-features `service-workers` |
| Cache Storage (`caches`、`Cache`) | `Cache` 40 / `CacheStorage` 43、Edge 16 | 41 | 11.1 | 11.3 | 43 | MDN BCD `api.CacheStorage`、`api.Cache` |
| Service worker の ES モジュール | 91 | 147 | 15 | 15 | (BCD 上は Chrome に準ずる、推測) | web-features `js-modules-service-workers` |
| Navigation Preload | 59 | 99 | 15.4 | 15.4 | 59 | MDN BCD `api.NavigationPreloadManager` |
| Static Routing API (`InstallEvent.addRoutes`) | 123 | 未対応 (bug 1855580) | 27 | 27 | 123 | MDN BCD `api.InstallEvent.addRoutes`、WebKit の Safari 27 beta 記事、Chrome の発表記事 |
| Background Fetch | 74 / Edge 79 | 未対応 | 未対応 | 未対応 | 未対応 | MDN BCD `api.BackgroundFetchManager` |
| Background Sync (`SyncManager`) | 49 / Edge 79 | 未対応 | 未対応 | 未対応 | 未対応 | MDN BCD `api.SyncManager` |
| Periodic Background Sync | 80 / Edge 80 | 未対応 | 未対応 | 未対応 | 未対応 | MDN BCD `api.PeriodicSyncManager` |
| `beforeinstallprompt` イベント | 61 (`BeforeInstallPromptEvent` は 44) / Edge 79 | 未対応 | 未対応 | 未対応 | 61 | MDN BCD `api.Window.beforeinstallprompt_event` |
| Web App Manifest (インストールに使う) | 53 / Edge 79 | デスクトップは manifest としては未対応、Android 版 79。Windows では 143 から「ウェブアプリ」としてタスクバーに固定できる | 17 (Dock に追加) | 15.4 | (未確認) | web-features `manifest`、Firefox 143 リリースノート |
| `navigator.install()` (Web Install API) | 154 でフラグ (`#web-app-installation-api`)。Origin Trial は 143 から | 未対応 | 未対応 | 未対応 | 未対応 | MDN BCD `api.Navigator.install`、blink-dev の Intent to Ship |

## 概要

Service Worker はページとネットワークの間に入るスクリプトで、ページが閉じていても登録したオリジンの `fetch` を横取りし、Cache Storage や IndexedDB から応答を返せる。Cache Storage は Request と Response の組をオリジンごとに保存する領域で、HTTP キャッシュと違い、何を入れて何を消すかをスクリプトが決める。Static Routing API はインストール時に「この URL はネットワークへ」「この URL は指定したキャッシュから」といった規則を宣言し、Service Worker を起動せずにブラウザが振り分けられるようにする。Background Fetch、Background Sync、Periodic Background Sync はページを閉じた後の取得や送信を扱うが、Chromium 系だけにある。

## 地図プロダクトでの使いどころ

保存、計算、表現のどれを、ブラウザ・アプリの層に置けるようにするか。

- 保存: スタイル JSON、グリフ (PBF)、スプライト、XYZ タイルを Cache Storage に入れて、再訪問時やオフライン時にネットワークなしで地図を出せる。事前に範囲とズームを決めて「地図パック」としてまとめて取得することもでき、Chromium 系なら Background Fetch でページを閉じても続く進捗表示つきのダウンロードにできる。PMTiles のように 1 ファイルを Range で読む形式は、Cache API が 206 応答を保存できない (後述) ので、全体を 200 で取って保存するか、Range 単位の結果を別の URL キーで保存するか、OPFS に置くかを選ぶ必要がある (設計の選択肢は推測、206 を保存できないことは仕様で確認)。
- 計算: Service Worker の中で、保存済みの PMTiles 全体から Range 要求に合う部分を切り出して 206 応答を合成すれば、地図ライブラリからは通常の Range 取得に見せられる (推測、実装例は確認していない)。オフライン中の現地調査の入力を IndexedDB に溜め、Background Sync で接続回復時に送る用途もある (Chromium 系のみ)。
- 表現: PWA としてインストールすれば、ブラウザの枠なしで地図アプリとして起動できる。iOS / iPadOS 26 以降は、ホーム画面に追加したサイトが既定で Web アプリとして開く。ホーム画面の Web アプリは Safari と別に「7 日規則」の日数を数えるので、オフライン地図を保持させたい場合の受け皿になる (詳しくは storage.md)。

## 制約

- 容量と寿命: Cache Storage は IndexedDB、OPFS と同じオリジンの割り当て (quota) に数えられ、退避 (eviction) もオリジン単位でまとめて起きる (MDN)。Chrome はオリジンあたり総ディスクの最大 60%、Firefox は best-effort で 10% か 10 GiB の小さい方、Safari 17 以降のブラウザアプリは 60%、WKWebView などは 15%。Safari は追跡防止が有効なとき、7 日間 Safari を使ってもそのサイトでの操作がなければ Service Worker の登録とキャッシュを含むスクリプトで書いた保存領域を消す。詳細は storage.md。Background Fetch は保存領域が足りないと `quota-exceeded` で失敗する。Background Fetch で取った応答は `backgroundfetchsuccess` などのイベントの間しか読めないので、その中で Cache Storage へ移す必要がある。
- 権限とユーザーの操作が要るか: Service Worker と Cache Storage に権限の確認はない。Periodic Background Sync はインストールされた PWA で、サイトのエンゲージメントスコアが 0 より大きく、権限 `periodic-background-sync` が `granted` のときだけ動き、発火の間隔はブラウザが決める。以前つないだことのあるネットワークでしか動かない。Background Fetch はユーザーがダウンロードを拒否していると失敗し、進捗が UI に出る。Chrome のインストールの条件は HTTPS、manifest (`name` か `short_name`、192px と 512px のアイコン、`start_url`、`display`)、ページを 1 回以上クリックし 30 秒以上見ていること。メニューからのインストールに `fetch` ハンドラは要らなくなった (Android 108、デスクトップ 112) が、インストールを促す表示には当時 `fetch` ハンドラが要った (現在も同じかは未確認)。
- セキュアコンテキスト、クロスオリジン分離 (COOP/COEP) などの前提: Service Worker は HTTPS (localhost を除く) が要る。COOP/COEP は要らない。Background Fetch のクロスオリジン要求は CORS が要り、プリフライトは使えない。Chrome の実装は本文のない要求だけを受け付ける。
- iOS / Safari での制限: Background Fetch、Background Sync、Periodic Background Sync、`beforeinstallprompt` はない。インストールは共有メニューの「ホーム画面に追加」で、サイトからインストールを促す API はない。Static Routing は Safari 27 で入ったばかりで、Safari 27 beta の記事は仕様上の制限の検査や、`fetch` ハンドラがないときに規則が当たらない不具合を直したと書いている。
- WebView (アプリに埋め込んだブラウザ) での制限: iOS の WKWebView では Service Worker は iOS 14 から使えるが、App-Bound Domains (Info.plist の `WKAppBoundDomains`、最大 10 ドメイン) を設定したアプリか、Web ブラウザの entitlement を持つアプリだけに公開される (MDN BCD の注記)。WebKit の不具合報告では App-Bound Domains の WKWebView は Service Worker 3 個までと書かれている (現行の iOS でも同じかは未確認)。Android の WebView は 40 から Service Worker を持ち、アプリ側は `ServiceWorkerController` (API レベル 24) で Service Worker の要求を横取りできる。すべての WebView で 1 つの既定インスタンスを共有する。Android の WebView には Background Fetch、Background Sync、Periodic Background Sync がない。

## 地図の実装例

この API を使っている OSS やライブラリ (地図ライブラリ、PMTiles、DuckDB-Wasm など)。

- MapLibre GL JS (BSD-3-Clause): v2.x までは `src/util/tile_request_cache.ts` で Cache Storage に `mapbox-tiles` という名前のキャッシュを作り、タイルを入れていた。v3.0.0 ではこのファイルがなく、現行 (6.17.0) もタイルを Cache Storage に入れる仕組みは持たない。オフライン化は、アプリ側の Service Worker か `addProtocol` で自前に作る前提になる。Mapbox GL JS 由来の CHANGELOG には Safari の CacheStorage のメモリリークへの回避策 (mapbox-gl-js #8956) が残っている。
- PMTiles JS (`pmtiles` 4.5.0、BSD-3-Clause): `FetchSource` が HTTP Range でアーカイブを読み、ETag の不一致を検知するとブラウザキャッシュを使わない (`cache: "no-store"` など) で取り直す。ライブラリ内のキャッシュはヘッダーとディレクトリだけで、タイル本体はキャッシュしない。`FileSource` はブラウザの `File` から読むので、OPFS やファイル選択で得たファイルをそのまま渡せる。Service Worker や Cache Storage を使う公式の仕組みは、ソースを見た範囲ではない。

## 落とし穴

- `Cache.put()` は status 206 の応答を `TypeError` で拒む。`Cache.add()` / `addAll()` は ok でない応答か 206 なら拒む (Service Workers 仕様)。PMTiles や COG のように Range で読む形式は、そのまま Cache Storage に入らない。
- Cache Storage は URL と `Vary` で引くので、Range の値ごとには分けられない。同じ URL に違う Range の結果を入れると上書きになる (仕様から推測)。
- PMTiles のアーカイブを差し替えたとき、古いディレクトリと新しいタイルの組み合わせを避けるため、PMTiles JS は ETag で判定している。Service Worker で自前にキャッシュする場合も、ETag かバージョンつき URL でキャッシュの鍵を変える必要がある (推測)。
- Static Routing の規則は `install` イベントの中でしか足せない。条件は入れ子を含めて合計 1024 個まで、深さ 10 までで、超えると `TypeError` で拒まれる。`fetch-event` と `race-network-and-fetch-handler` を source にするには `fetch` ハンドラが要る。Chrome の Origin Trial 版の `registerRouter()` は廃止された。
- Background Fetch は `downloadTotal` を超えると中止される。指定しないとサイズ不明として表示され、ユーザーが取り消しやすくなる (Chrome の記事)。
- Safari の 7 日規則は Service Worker の登録そのものも消すので、オフライン地図の Service Worker ごと失われうる。ホーム画面の Web アプリは別に数えるので、オフライン用途はインストールを前提にする方が安全。
- Periodic Background Sync で「毎晩タイルを更新する」設計は、インストール済みで、エンゲージメントがあり、Chromium 系の場合だけ動く。間隔は保証されない。

## まだ使えないもの、これから使えるもの

提案中、Origin Trial 中、一部のブラウザだけのもの。

- Static Routing API: Chrome 123、Safari 27 (2026-09-14 公開) に入った。Firefox は未実装 (bug 1855580)。Chrome は Origin Trial (116 から) の後に 123 で公開した。
- Web Install API (`navigator.install()`) と `<install>` 要素: Chrome と Edge の Origin Trial。blink-dev の Intent to Ship はデスクトップ 156 での公開を挙げているが、公開済みかは未確認。他サイトのアプリのインストールを促す用途も含む提案。
- Background Fetch、Background Sync、Periodic Background Sync: Chromium 系だけ。WICG の草案のまま、Firefox と Safari の実装はない。
- `beforeinstallprompt`: Chromium 系だけ。web-features でも未達。
- Firefox のデスクトップの PWA: 143 (2025-09-16) で Windows のタスクバーに固定する「ウェブアプリ」が入った。Microsoft Store 版では使えない。

## 出典

- https://unpkg.com/@mdn/browser-compat-data/data.json (MDN browser-compat-data 8.1.8、2026-11-02 生成。各 API の対応版、iOS WKWebView の App-Bound Domains の注記)
- https://unpkg.com/web-features/data.json (web-features。Baseline の状態と日付、Safari 27 の公開日 2026-09-14)
- https://w3c.github.io/ServiceWorker/ (Editor's Draft 2026-10-29。`Cache.put()` が 206 を拒むこと、`addAll` が ok でない応答と 206 を拒むこと、RouterSourceEnum の 4 種、条件 1024 個と深さ 10 の上限、`fetch` ハンドラの要件)
- https://www.w3.org/TR/service-workers/ (Candidate Recommendation Draft、2026-10-29)
- https://www.w3.org/TR/appmanifest/ (Web App Manifest、Working Draft、2026-11-06)
- https://developer.mozilla.org/en-US/docs/Web/API/Cache/put (`put()` は 200 以外も保存できる、`add` / `addAll` は 200 番台以外を保存しない)
- https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria (Cache Storage が quota に数えられること、オリジン単位の退避)
- https://developer.chrome.com/blog/service-worker-static-routing (Chrome 123、`install` で `addRoutes`、条件と source の種類、Origin Trial の `registerRouter()` の廃止)
- https://webkit.org/blog/17967/news-from-wwdc26-webkit-in-safari-27-beta/ (Safari 27 beta で Static Routing に対応、関連の修正)
- https://webkit.org/blog/17333/webkit-features-in-safari-26-0/ (Safari 26 でホーム画面に追加したサイトが既定で Web アプリとして開く)
- https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/ (7 日規則が Service Worker の登録とキャッシュを含むこと、ホーム画面の Web アプリは別に数えること)
- https://webkit.org/blog/10882/app-bound-domains/ (App-Bound Domains、iOS 14、最大 10 ドメイン、`WKAppBoundDomains`)
- https://bugs.webkit.org/show_bug.cgi?id=227531 (App-Bound Domains の WKWebView で Service Worker が 3 個までという報告)
- https://developer.chrome.com/blog/background-fetch (Chrome 74、進捗 UI、ページを閉じても続くこと、`quota-exceeded`、本文なしの要求のみ、CORS プリフライト不可、レコードはイベント中だけ読める)
- https://developer.chrome.com/docs/capabilities/periodic-background-sync (インストール済み、エンゲージメント、権限、既知のネットワーク)
- https://web.dev/articles/install-criteria (Chrome のインストール条件)
- https://developer.chrome.com/blog/update-install-criteria (`fetch` ハンドラ要件の撤廃、Android 108 / デスクトップ 112)
- https://groups.google.com/a/chromium.org/d/msgid/blink-dev/dc40448e-61c3-468f-929c-b17bfa21771fn%40chromium.org (Web Install API の Intent to Ship、Origin Trial 143 から、公開予定 156)
- https://developer.chrome.com/blog/install-element-ot (`<install>` 要素の Origin Trial)
- https://www.firefox.com/en-US/firefox/143.0/releasenotes/ (Firefox 143、Windows のウェブアプリ)
- https://developer.android.com/reference/android/webkit/ServiceWorkerController (Android WebView の Service Worker の制御、API 24)
- https://raw.githubusercontent.com/maplibre/maplibre-gl-js/v2.4.0/src/util/tile_request_cache.ts (MapLibre v2 の Cache Storage `mapbox-tiles`。v3.0.0 では同パスが 404)
- https://raw.githubusercontent.com/maplibre/maplibre-gl-js/main/CHANGELOG.md (Safari の CacheStorage メモリリーク回避)
- https://raw.githubusercontent.com/protomaps/PMTiles/main/js/src/index.ts (PMTiles JS の `FetchSource`、`FileSource`、ETag 処理、ヘッダーとディレクトリだけのキャッシュ)

## 未確認のこと

- Chrome がインストールを促す表示 (`beforeinstallprompt` を含む) に今も `fetch` ハンドラを要るか。オフラインで 200 を返すかを試す案 (blink-dev) が公開されたか。
- Web Install API がデスクトップ 156 で公開されたか、Android と Edge での扱い。
- Android の WebView での Web App Manifest の扱い (BCD に該当データがない)。
- Service worker の ES モジュールの Android WebView での対応版。
- App-Bound Domains の WKWebView で Service Worker が 3 個までという制限が現行の iOS でも残っているか。
- Service Worker で PMTiles の Range 応答を合成して配る OSS の実装例 (探したが見つけていない)。
- Static Routing の `cache` source が Range 要求をどう扱うか (206 を返すのか、全体を返すのか)。
- Safari 27 の Static Routing が Chrome と同じ条件 (`or`、`not`、`runningStatus` など) をすべて持つか。
