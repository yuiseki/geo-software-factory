# flutter_map

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 8.3.2 (2026-08-28 JST)。別に 8.4.0-dev.1 (2026-09-03 JST) がプレリリースとして出ている (https://pub.dev/packages/flutter_map 、 https://github.com/fleaflet/flutter_map/releases/tag/v8.3.2) |
| リポジトリ | https://github.com/fleaflet/flutter_map |
| ドキュメント | https://docs.fleaflet.dev |
| ライセンス (LICENSE ファイルで確かめる) | BSD-3-Clause (Copyright (c) 2018-2026, the 'flutter_map' authors and maintainers) (https://github.com/fleaflet/flutter_map/blob/master/LICENSE) |
| 運営主体・ガバナンス | GitHub の `fleaflet` Organization。GitHub Sponsors で寄付を受けている。特定の地図ベンダーには属さない (https://github.com/fleaflet 、 https://github.com/sponsors/fleaflet) |

## 概要

Flutter 用の地図ウィジェット。Leaflet に似たレイヤー構成で、タイルレイヤー、マーカー、ポリライン、ポリゴンなどを Flutter のウィジェットとして重ねる。pub.dev の説明は「vendor-free、fully cross-platform、100% pure-Flutter」で、ネイティブの地図 SDK やプラットフォームビューを使わない (https://pub.dev/packages/flutter_map 、 https://docs.fleaflet.dev)。標準ではラスタタイルを扱い、ベクトルタイルはコミュニティのプラグインに任せている (https://docs.fleaflet.dev/layers/vector-tile-layer)。

## 対応プラットフォーム

| プラットフォーム | 対応 | 最低 OS 版・備考 |
|---|---|---|
| Android | 対応 | flutter_map 独自の要件は無く、Flutter 本体の最低版に従う (pubspec の `platforms`) |
| iOS | 対応 | 同上 |
| Web | 対応 | 同上。Web ではブラウザが User-Agent を決めるため `userAgentPackageName` が効かない (https://docs.fleaflet.dev/tile-servers/using-openstreetmap-direct) |
| デスクトップ (macOS / Windows / Linux) | 対応 | pubspec の `platforms` に linux、macos、windows がある |

- フレームワークの版の要件: 8.3.2 の pubspec で Dart SDK `>=3.6.0 <4.0.0`、Flutter `>=3.27.0` (https://pub.dev/packages/flutter_map/versions/8.3.2/pubspec 、 https://github.com/fleaflet/flutter_map/blob/master/pubspec.yaml)

## 描画方式

- 自前で描画するか、OS や他の SDK のラッパーか: 自前で描画する。ネイティブ SDK を包まず、すべて Flutter の描画で地図を組み立てる (https://docs.fleaflet.dev)
- ラスタ / ベクトルタイル、2D / 3D: 本体はラスタタイルとベクタ図形 (マーカー、ポリライン、ポリゴン、円) の 2D 描画。ベクトルタイルはプラグインで対応する。ドキュメントは、ベクトルタイルでは要素を一つずつ解釈して描くので性能に響き、文字や図形の回転は毎フレーム計算が要る、と書く (https://docs.fleaflet.dev/why-and-how/how-does-it-work/raster-vs-vector-tiles)。3D 表示 (傾き、地形) は未確認

## 対応するタイル・データ

- 表示できるタイル・地図データ: 本体はラスタの XYZ タイル (ネットワーク、アプリ同梱アセット `AssetTileProvider`、端末のファイル `FileTileProvider`)、WMS (未確認)、ベクタ図形。プラグインで MBTiles (`flutter_map_mbtiles`)、PMTiles (`flutter_map_pmtiles`)、ベクトルタイル (`vector_map_tiles`、`flutter_map_vector_tiles`、MapLibre Native のレイヤーをプラットフォームビューなしで埋め込む `mapigrade`) を扱える (https://docs.fleaflet.dev/tile-servers/offline-mapping 、 https://docs.fleaflet.dev/layers/vector-tile-layer)
- 組み合わせの制約 (下にある SDK の規約・課金を引き継ぐか): 下に SDK は無いので、規約と課金はタイルの提供元だけで決まる。ドキュメントは OpenStreetMap の公開タイルサーバーについて「誰でも無料で使えるわけではない」と書き、利用方針の遵守、User-Agent の設定 (`TileLayer.userAgentPackageName`、未設定や `com.example.app` のままだとブロックされる)、帰属表示 (`RichAttributionWidget` など) を求めている。Google Maps や Mapbox のタイルも使えるが割高になりうる、とも書く (https://docs.fleaflet.dev/tile-servers/using-openstreetmap-direct 、 https://docs.fleaflet.dev)
- オフライン地図: 8.2.0 から閲覧したタイルの長期キャッシュを標準で持つ。地域の一括ダウンロードはプラグイン `flutter_map_tile_caching` (FMTC、GPL-3.0) を推奨している。アプリ同梱やファイルとして置いたタイル、MBTiles、PMTiles でもオフライン表示できる (https://docs.fleaflet.dev/tile-servers/offline-mapping)

## ライセンスと費用

- ライセンス: BSD-3-Clause。pub.dev の説明にある「non-commercially aimed」は商用ベンダーが運営していないことを指すと読め、ライセンスは商用利用を制限していない (この読み方は推測)
- 下にある SDK の費用: 対象外 (下にある SDK が無い)。費用はタイル配信の提供元か自前配信のインフラで決まる
- ライセンス上の注意: 本体と直接の依存 (dart_earcut は MIT、dart_polylabel2 は BSD-3-Clause、proj4dart は MIT、latlong2 は Apache-2.0、uuid は MIT、http、path_provider、async、collection、meta、path は BSD-3-Clause) にコピーレフトは無い。配布時は BSD-3-Clause などの著作権表示を含める。注意が要るのはオフライン用プラグインの `flutter_map_tile_caching` で、GPL-3.0 である。GPL-3.0 のライブラリをアプリに組み込んで配布すると、アプリ全体を GPL-3.0 で提供し、受け取った人にソースコードを提供する (少なくとも求めに応じて) 必要がある。改変した場合も同じ条件で公開する。App Store の利用条件 (端末数の制限など) が GPL-3.0 と両立しないとする見方があり、ストア配布ではこの点も問題になりうる (推測)。作者はプロプライエタリなアプリ向けに有償ライセンス (年単位の交渉制、非営利団体には無償の場合あり) を別に売っている (https://github.com/JaffaKetchup/flutter_map_tile_caching#proprietary-licensing)。ほかのプラグイン (`vector_map_tiles`、`mapigrade`、`flutter_map_vector_tiles`、`flutter_map_location_marker` は BSD-3-Clause、`flutter_map_pmtiles` は MIT) にコピーレフトは無い。OSM データを表示する場合は ODbL の帰属表示が要る

## エコシステム

- 主なプラグイン・拡張: 現在地表示の `flutter_map_location_marker`、オフラインの `flutter_map_tile_caching`、`flutter_map_mbtiles`、`flutter_map_pmtiles`、ベクトルタイルの `vector_map_tiles`、`flutter_map_vector_tiles`、`mapigrade` (https://docs.fleaflet.dev 、 https://docs.fleaflet.dev/layers/vector-tile-layer 、 https://github.com/josxha/flutter_map_plugins)。ドキュメントはベクトルタイル用プラグインについて、元の `vector_map_tiles` は本番に耐える性能を出せなかったこと、FlutterGPU を使うベータ版は性能が改善したが FlutterGPU 自体がベータで制約が大きいこと、`mapigrade` と `flutter_map_vector_tiles` は独自に検証していないことを書いている
- 似た位置づけの他のライブラリとの違い: Google Maps や MapLibre Native を包む Flutter 用プラグイン (google_maps_flutter、maplibre_gl など) はネイティブ SDK とプラットフォームビューに頼るため、ベクトルタイルの描画性能や 3D 表現は得やすいが、対応プラットフォームと見た目の一貫性はラップ先に縛られる。flutter_map は全ターゲットで同じ Dart コードで描くが、ベクトルタイルは弱い (違いの整理は推測を含む。docs.fleaflet.dev は「バグが多く制約のあるプラットフォームビュー」を避けると書く)

## 開発の活発さ

- 直近 1 年のリリース数: 安定版 3 (8.3.0、8.3.1、8.3.2)、プレリリース 1 (8.4.0-dev.1) (2025-11-10 から 2026-11-10 の GitHub Releases)
- 最終コミット日: 2026-11-04 JST (master、Dependabot による GitHub Actions の更新)
- 主なメンテナー (個人か組織か): `fleaflet` Organization。直近 1 年の人間のコミットは JaffaKetchup が最多で、ben-milanko、monsieurtanuki が続く。累計では johnpryan (初期の作者)、JaffaKetchup、kengu、josxha が多い (https://github.com/fleaflet/flutter_map/graphs/contributors)

## 環境の違いと保守

- ブラウザ間の互換: Web でも Flutter の描画で地図を組み立てるので、ブラウザの違いは Flutter の Web エンジンが引き受ける (上の「描画方式」)。文書でうたう対応ブラウザの一覧は未確認。CI では PR ごとに `flutter build web --wasm` で Web (WebAssembly) 版のデモをビルドするが、ブラウザの上で動かすテストは無い ([branch.yml](https://github.com/fleaflet/flutter_map/blob/master/.github/workflows/branch.yml))。8.3.0 (2026-04-14) で `dart:io` への参照を取り除き、pana が WASM 対応と認めるようにした ([CHANGELOG](https://github.com/fleaflet/flutter_map/blob/master/CHANGELOG.md))。Web では User-Agent ヘッダーを付けないようにした修正もある (同)。
- OS 間の互換: CI のテストは ubuntu-latest の上の `flutter test` (ウィジェットテスト) で、最低版の Flutter 3.27.0 と最新の stable の 2 つで回す ([branch.yml](https://github.com/fleaflet/flutter_map/blob/master/.github/workflows/branch.yml))。デモのビルドは Android の APK (Flutter 3.27.0 と最新)、Windows (windows-2022 の 3.27.0 と windows-latest の最新)、Web である (同)。iOS、macOS、Linux のビルドは CI に無く、実機やエミュレーターでの実行も無い (同)。GPU とメモリの上限への対応の文書は未確認。
- 操作の網羅: `InteractiveFlag` で、ドラッグ、フリングの慣性、ピンチでの移動、ピンチでのズーム、ダブルタップでのズーム、ダブルタップ後のドラッグでのズーム、ホイールでのズーム、回転を個別に有効、無効にできる ([interactive_flag.dart](https://github.com/fleaflet/flutter_map/blob/master/lib/src/gestures/interactive_flag.dart))。回転、ピンチのズーム、ピンチの移動のどれが勝つかのしきい値と「多指の身ぶりの競争」の設定がある ([interaction.dart](https://github.com/fleaflet/flutter_map/blob/master/lib/src/map/options/interaction.dart))。キーボードでの移動、ズーム、回転をアニメーションつきで受け、カーソルとキーで回転する設定もある (8.0.0 で追加、[keyboard.dart](https://github.com/fleaflet/flutter_map/blob/master/lib/src/map/options/keyboard.dart)、[CHANGELOG](https://github.com/fleaflet/flutter_map/blob/master/CHANGELOG.md))。傾きは無い (2D)。スクロールする親ビューとの両立の設定は未確認。
- エッジケースへの対応: 日付変更線は 8.0.0 (2025-02-02) で、既定の投影法で横方向に無限に移動でき、レイヤーが日付変更線をまたげるようになり、8.1.0 でポリゴンとポリラインが複数の世界に対応した ([CHANGELOG](https://github.com/fleaflet/flutter_map/blob/master/CHANGELOG.md))。`LatLngBounds.center` が世界の境界をまたいで正しく働く修正もある (同)。タイルは 8.2.0 (2025-07-10) で `NetworkTileProvider` に組み込みのキャッシュが入り、8.2.1 で HTTP の仕様に沿わない応答でキャッシュに失敗してもタイルを読み込むよう直した (同)。再試行は 5.0.0 で `NetworkNoRetryTileProvider` を外し、`NetworkTileProvider.httpClient` を差し替えて決める形にした (同)。端末へのオフライン保存は本体ではなく `flutter_map_tile_caching` などのプラグインが担う (上の「エコシステム」)。描画コンテキストの喪失とアプリのバックグラウンド移行の扱いは未確認。
- 継続的な保守: CI で、対応する最低版の Flutter (3.27.0) と最新の stable の両方を試しており、Flutter の新版への追随を毎回確かめている ([branch.yml](https://github.com/fleaflet/flutter_map/blob/master/.github/workflows/branch.yml))。Issue のラベルは優先度と分類 (`P: 2` など、`plugins`) で、プラットフォーム別のラベルは無い ([labels](https://github.com/fleaflet/flutter_map/labels))。

## 向いている場面

- Flutter で Android、iOS、Web、デスクトップのすべてに同じ地図を出したいとき。
- ラスタタイル (自前配信や提供元の XYZ) にマーカーや図形を重ねる用途。
- 地図ベンダーへの依存や API キーを避けたいとき。
- アプリ同梱タイル、MBTiles、PMTiles でオフライン表示したいとき (BSD / MIT のプラグインで済む範囲)。

## 向いていない場面

- ベクトルタイルを本番品質で滑らかに描きたいとき (プラグイン頼みで、性能と成熟度に注意書きがある)。
- 3D 地図、地形、建物の立体表示が要るとき。
- プロプライエタリなアプリで地域の一括ダウンロードが要るとき (推奨の FMTC は GPL-3.0 なので有償ライセンスか別の手段が要る)。
- OSM の公開タイルサーバーをそのまま本番で使うつもりのとき (利用方針の制約がある)。

## 出典

- https://github.com/fleaflet/flutter_map
- https://github.com/fleaflet/flutter_map/blob/master/LICENSE
- https://github.com/fleaflet/flutter_map/blob/master/pubspec.yaml
- https://github.com/fleaflet/flutter_map/releases/tag/v8.3.2
- https://github.com/fleaflet/flutter_map/graphs/contributors
- https://github.com/fleaflet
- https://github.com/sponsors/fleaflet
- https://pub.dev/packages/flutter_map
- https://pub.dev/packages/flutter_map/versions/8.3.2/pubspec
- https://docs.fleaflet.dev
- https://docs.fleaflet.dev/why-and-how/how-does-it-work/raster-vs-vector-tiles
- https://docs.fleaflet.dev/layers/vector-tile-layer
- https://docs.fleaflet.dev/tile-servers/offline-mapping
- https://docs.fleaflet.dev/tile-servers/using-openstreetmap-direct
- https://github.com/JaffaKetchup/flutter_map_tile_caching
- https://github.com/JaffaKetchup/flutter_map_tile_caching#proprietary-licensing
- https://github.com/josxha/flutter_map_plugins
- https://github.com/greensopinion/flutter-vector-map-tiles
- https://github.com/greensopinion/mapigrade
- https://github.com/JonasGrunau/flutter-map-vector-tiles
- https://github.com/tlserver/flutter_map_location_marker
- https://github.com/JaffaKetchup/dart_earcut
- https://github.com/JaffaKetchup/dart_polylabel2
- https://github.com/maRci002/proj4dart
- https://github.com/ThexXTURBOXx/dart-latlong
- https://github.com/Daegalus/dart-uuid

## 未確認のこと

- 各プラットフォームの最低 OS 版の具体的な数字: flutter_map は Flutter 本体に委ねており、Flutter 3.27 以降の各版の最低 OS 版を確かめていない。
- 本体の WMS 対応と 3D 表示 (傾き) の有無: API リファレンスを確かめていない。
- GPL-3.0 と App Store の利用条件が両立しないかどうか: 法的な判断であり、公式の見解を確かめていない。
- 他の Flutter 用地図プラグインとの比較: 各プラグインのリポジトリを調べておらず、違いの整理には推測を含む。
