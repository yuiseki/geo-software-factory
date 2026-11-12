# アプリの中の保存と計算

対象: Android と iOS のネイティブアプリ、React Native と Flutter のアプリで、地図データを端末に置き、端末で計算するための手段 (端末内の保存領域、SQLite と SpatiaLite、オフライン用のタイルパック、端末でのルート検索と検索、バックグラウンドでの取得)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |

## ブラウザとの違い

| 観点 | ブラウザ | ネイティブアプリ | 出典 |
|---|---|---|---|
| 保存できる量と消される条件 | 上限は総ディスク容量に対する割合で決まる。Chromium は 1 オリジンあたり総容量の 60%。Firefox は best-effort で総容量の 10% か 10 GiB の小さいほう、persistent で 50% (8 TiB まで)。WebKit (macOS 14、iOS 17 以降) はブラウザアプリで約 60%、Web を埋め込んだ他のアプリで約 15%。容量が逼迫すると最近使われていないオリジンから丸ごと消す (LRU)。Safari はトラッキング防止が有効だと、7 日間操作のないオリジンのスクリプト由来のデータを消す。`navigator.storage.persist()` が通れば利用者が消すまで残る | 容量の割合による上限はなく、端末の空き容量が上限になる (推測)。Android は内部ストレージの `filesDir` (残る) と `cacheDir` (空きが少ないと OS が消すことがある) を分け、`getAllocatableBytes()` と `allocateBytes()` で必要量を確保できる。アンインストールでアプリ固有の領域は消える。外部ストレージのアプリ固有領域は SD カードを抜くと読めない。iOS は `tmp` と `Library/Caches` を「OS が定期的に消す」領域とし、iCloud バックアップから外す。再取得できる大きなデータは消されない場所に置き、`isExcludedFromBackup` を付けてバックアップから外すよう Apple が勧めている | [MDN Storage quotas](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)、[Android app-specific storage](https://developer.android.com/training/data-storage/app-specific)、[Apple iCloud backup](https://developer.apple.com/documentation/foundation/optimizing-your-app-s-data-for-icloud-backup) |
| バックグラウンドでの取得 | Background Fetch API は Service Worker を使い、タブを閉じても取得を続けられるが、MDN では Experimental かつ Limited availability (広く使われているブラウザの一部で動かない) | Android は WorkManager (再起動をまたいで再スケジュール、非従量回線や充電中などの条件指定、10 分を超える処理はフォアグラウンドサービスとして実行) か、利用者が始めた転送なら User-Initiated Data Transfer Job を勧めている。iOS は `URLSession` のバックグラウンドセッションで、アプリが停止中でも別プロセスでダウンロードが続き、終わるとアプリが起こされる。`isDiscretionary` を有効にすると Wi-Fi や充電中など条件のよい時まで待つ。数分かかる処理は `BGProcessingTaskRequest` で予約できる | [MDN Background Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Background_Fetch_API)、[WorkManager](https://developer.android.com/develop/background-work/background-tasks/persistent)、[Android data transfer options](https://developer.android.com/develop/background-work/background-tasks/data-transfer-options)、[Downloading files in the background](https://developer.apple.com/documentation/foundation/downloading-files-in-the-background)、[BGProcessingTaskRequest](https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest) |
| 計算 (スレッド、GPU) | Web Worker で別スレッドを使える。WebGPU は MDN で Limited availability (Baseline でない)、HTTPS のみ、Worker 内でも使える | ネイティブのスレッドと GPU API を制限なく使える (推測)。MapLibre Native、Valhalla、SQLite などの C/C++ ライブラリをそのまま組み込める | [MDN WebGPU](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API) |
| 配布と更新 (ストア審査、データの差し替え) | 審査なしで即時に差し替えられる | アプリ本体の更新はストア審査を通る。iOS アプリは非圧縮 4 GB、実行ファイルの `__TEXT` 合計 500 MB (iOS 9 以降が対象) が上限で、大きな素材は Background Assets を使うよう Apple が勧めている。Android の Play Asset Delivery は 200 MB を超えるアプリ向けで、`install-time` のパックはストアの表示サイズに含まれ端末に 2 倍の空きを要し、`fast-follow` と `on-demand` は含まれない。地図データは本体と分けてアプリ内でダウンロードすれば審査なしで差し替えられる (推測) | [Apple maximum build file sizes](https://developer.apple.com/help/app-store-connect/reference/app-uploads/maximum-build-file-sizes)、[Play Asset Delivery](https://developer.android.com/guide/playcore/asset-delivery) |

## 地図データを端末に置く手段

| 手段 | 何を置けるか | 対応する SDK | 出典 |
|---|---|---|---|
| MapLibre Native のオフラインパック (`OfflineManager`) | スタイルが参照するタイル、グリフ、スプライトを範囲 (タイルピラミッドか図形) とズームで指定してダウンロードし、端末内の DB に保存する。既定では 1 端末 6,000 タイルまでで、`setOfflineMapboxTileCountLimit` で変えられる | MapLibre Android 13.x (最新リリースは 2026-11-09 の android-v13.5.4 と 2026-10-15 の 13.7.1)、MapLibre iOS 7.0.0 (2026-10-28)、BSD-2-Clause | [setOfflineMapboxTileCountLimit](https://maplibre.org/maplibre-native/android/api/-map-libre%20-native%20-android/org.maplibre.android.offline/-offline-manager/set-offline-mapbox-tile-count-limit.html)、[maplibre-native releases](https://github.com/maplibre/maplibre-native/releases) |
| PMTiles を直接読む (`pmtiles://`) | 1 ファイルの PMTiles を、リモート (`pmtiles://https://...`)、端末内 (`pmtiles://file://` と絶対パス)、APK の assets (`pmtiles://asset://...`) から読む。相対パスは解決されない。オフラインパックのダウンロードとキャッシュには対応しないと公式に書かれている。一方で Android 13.3.0 と iOS 6.27.0 で PMTiles ソースの ambient cache が入った | Android の CHANGELOG では 11.8.0 で追加 (例のページは 11.7.0 からと書いており食い違う)、iOS 6.10.0 で追加。assets から Range で読む対応は Android 13.7.1 | [PMTiles example](https://maplibre.org/maplibre-native/android/examples/data/PMTiles/)、[Android CHANGELOG](https://github.com/maplibre/maplibre-native/blob/main/platform/android/CHANGELOG.md)、[iOS CHANGELOG](https://github.com/maplibre/maplibre-native/blob/main/platform/ios/CHANGELOG.md) |
| MBTiles (`mbtiles://`) | 端末内の MBTiles (SQLite) からベクタータイルを描く | Android 9.3.0、iOS 5.10.0 で追加 (2021-01-06)。Android 9.6.0 で MaptilerFileSource から MBTilesFileSource に改名 | [Android CHANGELOG](https://github.com/maplibre/maplibre-native/blob/main/platform/android/CHANGELOG.md)、[iOS CHANGELOG](https://github.com/maplibre/maplibre-native/blob/main/platform/ios/CHANGELOG.md) |
| SQLite (R*Tree、FTS) | 属性と位置の表。R*Tree は矩形の範囲検索用の索引で、`SQLITE_ENABLE_RTREE` を付けてビルドすると有効になる | SQLite はパブリックドメインで、商用・非商用を問わず複製、改変、配布できる | [SQLite copyright](https://www.sqlite.org/copyright.html)、[R*Tree](https://www.sqlite.org/rtree.html) |
| SpatiaLite | SQLite に空間型と空間関数を足す拡張。libspatialite 5.1.0 (2023-08-04) | MPL 1.1、GPL v2 以降、LGPL v2.1 以降から選ぶ三重ライセンス。Android 移植版は 4.3.0 | [libspatialite](https://www.gaia-gis.it/fossil/libspatialite/index) |
| React Native | MapLibre Native を包んだもの。Expo でも使える | `@maplibre/maplibre-react-native` v11.5.1 (2026-10-29)、MIT。オフライン用の `OfflineManager` モジュールがある | [maplibre-react-native](https://github.com/maplibre/maplibre-react-native)、[offline manager](https://maplibre.org/maplibre-react-native/docs/modules/offline-manager) |
| Flutter | MapLibre Native (Android、iOS) と MapLibre GL JS (Web) を包んだもの。オフライン領域のダウンロードは Android と iOS のみ。PMTiles のソースに対応。デスクトップは非対応 | `maplibre_gl` v0.28.0 (2026-11-03)、BSD-3-Clause | [flutter-maplibre-gl](https://github.com/maplibre/flutter-maplibre-gl) |

### ライセンスの注意 (一般的な解釈であり、法的助言ではない)

- SpatiaLite: 3 つから 1 つを選ぶ。MPL 1.1 を選ぶと、改変した SpatiaLite のファイルはソースを公開する必要があるが、アプリの他の部分は閉じたままにできる。LGPL v2.1 を選ぶと、改変した SpatiaLite のソースを提供し、利用者が SpatiaLite を差し替えて再リンクできるようにする必要がある。静的リンクが前提になる iOS では再リンクの条件を満たす手間が大きい (推測)。GPL v2 を選ぶとアプリ全体を GPL 互換で配る必要がある。サーバーで動かすだけ (SaaS) なら、いずれも配布にあたらずソース提供義務は生じない。
- OsmAnd: コードは GPLv3、アートワークと UI/UX (レイアウト、アイコン) は CC-BY-NC-ND 4.0 で、一部のアートワークと音声ファイルは独自ライセンス。OsmAnd の UI/UX のコードを使ったアプリを Google Play、Amazon、App Store に出すには書面の許可が要る。GPLv3 のコードを組み込んだアプリを配るなら、アプリ全体を GPLv3 で配り、ソースを提供する必要がある。改変して社内だけで使う、あるいはサーバーで動かすだけなら配布にあたらない。CC-BY-NC-ND の部分は商用利用も改変もできない。
- Organic Maps: コードは Apache-2.0 で、組み込み、改変、商用配布ができる (NOTICE の保持が要る)。`.mwm` などのデータファイルは ODbL の Produced Works とされ、「Map data © OpenStreetMap and Organic Maps」の表示と、organicmaps.app と openstreetmap.org/copyright へのリンクが要る。表示なしで配布や組み込みはできず、ホワイトラベル化には書面の許可が要る。
- OSM のデータ (ODbL): 帰属表示と ODbL であることの明示が要る。データを改変・加工したデータベースを配るなら同じライセンスで配る必要がある。

## 端末で動く検索とルート検索

- Valhalla (MIT): タイル状の階層グラフにより、メモリの少ない機器でのオフラインのルート検索を狙っていると公式に書かれており、iOS と Android でも使われている。
- Organic Maps (Apache-2.0): ダウンロード済みの地図で、検索、ルートの計画、ナビゲーションをインターネットなしで行えると公式サイトに書かれている。
- OsmAnd (GPLv3): ルートの種類として online と offline があり、BRouter も選べる。インターネットに頼らずに使えることを公式ドキュメントがうたっている。
- SQLite の R*Tree と全文検索は端末内で動く。R*Tree は地理空間の矩形検索が主な用途と SQLite の公式に書かれている。

## 地図の実装例

- OsmAnd: オフライン用のデータを `.obf` ファイルに持つ。1 つのファイルに地図、ルート検索、POI と交通、住所 (検索) の部分を複数持てる。住所検索の都市には OSM の `place` タグ (city、town、suburb、village、hamlet) を使う。ファイルは 2 GB 未満に保つよう勧められており、部分の結合や分割は OsmAndMapCreator の `binary_inspector` で行う。
- Organic Maps: 地図は独自の `.mwm` 形式で、地域ごとにダウンロードする。ダウンロードと更新の配信は Mythic Beasts のサーバーが支えていると README に書かれている。MAPS.ME 時代の文書では、ズームごとに分類・簡略化した地物を持つ形式で、車のルート検索には別の索引が要るとされている。現在の Organic Maps の `.mwm` の内部構成は確かめられていない。

## 出典

- https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria (ブラウザの容量上限と消される条件、`persist()`)
- https://developer.mozilla.org/en-US/docs/Web/API/Background_Fetch_API (Background Fetch の状態)
- https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API (WebGPU の状態)
- https://developer.android.com/training/data-storage/app-specific (Android のアプリ固有領域、キャッシュの削除、空き容量の確保)
- https://developer.android.com/develop/background-work/background-tasks/persistent (WorkManager)
- https://developer.android.com/develop/background-work/background-tasks/data-transfer-options (Android のバックグラウンド転送の選び方)
- https://developer.android.com/guide/playcore/asset-delivery (Play Asset Delivery のパック種別と容量の扱い)
- https://developer.apple.com/documentation/foundation/optimizing-your-app-s-data-for-icloud-backup (iOS の purgeable な領域と `isExcludedFromBackup`)
- https://developer.apple.com/documentation/foundation/downloading-files-in-the-background (URLSession のバックグラウンドダウンロード)
- https://developer.apple.com/documentation/backgroundtasks/bgprocessingtaskrequest と https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler (BGTaskScheduler)
- https://developer.apple.com/help/app-store-connect/reference/app-uploads/maximum-build-file-sizes (iOS アプリの大きさの上限と Background Assets)
- https://maplibre.org/maplibre-native/android/examples/data/PMTiles/ (MapLibre Android の PMTiles の URL 形式とオフラインの制約)
- https://github.com/maplibre/maplibre-native (Android と iOS の CHANGELOG で PMTiles と MBTiles の追加版を確認、リリース一覧を GitHub API で確認、BSD-2-Clause)
- https://maplibre.org/maplibre-native/android/api/-map-libre%20-native%20-android/org.maplibre.android.offline/-offline-manager/set-offline-mapbox-tile-count-limit.html (オフラインの既定 6,000 タイル)
- https://github.com/maplibre/maplibre-react-native (Expo 対応、MIT。v11.5.1 を GitHub API で確認)
- https://github.com/maplibre/flutter-maplibre-gl (対応プラットフォームとオフライン。LICENSE ファイルで BSD-3-Clause を確認、v0.28.0 を GitHub API で確認)
- https://www.sqlite.org/copyright.html と https://www.sqlite.org/rtree.html (SQLite のパブリックドメインと R*Tree)
- https://www.gaia-gis.it/fossil/libspatialite/index (SpatiaLite の三重ライセンスと版)
- https://github.com/osmandapp/OsmAnd/blob/master/LICENSE (OsmAnd のライセンス構成とストア公開の条件)
- https://osmand.net/docs/technical/osmand-file-formats/osmand-obf/ (OBF の構成)
- https://osmand.net/docs/user/navigation/ (OsmAnd のオンラインとオフラインのルート検索、BRouter)
- https://github.com/organicmaps/organicmaps と https://raw.githubusercontent.com/organicmaps/organicmaps/master/DATA_LICENSE.txt (Organic Maps のコードとデータのライセンス)
- https://organicmaps.app/ (オフラインの検索とナビゲーション)
- https://github.com/mapsme/omim/blob/map-downloader/docs/MAPS.md (MAPS.ME 時代の MWM とルート検索索引の説明。検索結果の要約で確認)
- https://valhalla.github.io/valhalla/ (Valhalla の端末でのオフライン利用と MIT)
- https://www.openstreetmap.org/copyright (ODbL の要件)

## 未確認のこと

- Android と iOS が 1 アプリに許す保存容量の明示的な上限 (公式に数値を見つけられなかった)。
- MapLibre Native のオフラインパックの保存先の DB の場所と大きさの上限、6,000 タイルの既定が iOS でも同じか。
- PMTiles ソースの ambient cache (Android 13.3.0、iOS 6.27.0) とオフラインパック非対応の記述の関係。例のページが最新の挙動を反映しているか。
- PMTiles 対応の初出が Android 11.7.0 か 11.8.0 か (例のページと CHANGELOG が食い違う)。
- iOS の BGContinuedProcessingTask など新しいバックグラウンド API の有無と条件。
- Google Play の base モジュールとアセットパックの具体的な大きさの上限 (公式の別ページにある)。
- Organic Maps の現在の `.mwm` の内部構成 (検索索引とルート検索グラフの持ち方)。
- OsmAnd の OBF が Protocol Buffers ベースであること (公式ページでは確認できなかった)。
- GPL のアプリを App Store で配布する時の規約上の扱い。
- Valhalla を Android と iOS に組み込むための公式のビルド手順とバイナリの大きさ。
