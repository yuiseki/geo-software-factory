# 3DTilesRendererJS

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | v0.5.4 (2026-11-03 JST) ([GitHub Releases](https://github.com/NASA-AMMOS/3DTilesRendererJS/releases/tag/v0.5.4)、npm パッケージ名は `3d-tiles-renderer`) |
| リポジトリ | https://github.com/NASA-AMMOS/3DTilesRendererJS |
| ドキュメント | README と各 API.md (https://github.com/NASA-AMMOS/3DTilesRendererJS#readme 、three.js 向けは [USAGE.md](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/USAGE.md))。サンプル: https://nasa-ammos.github.io/3DTilesRendererJS/ |
| ライセンス (LICENSE ファイルで確かめる) | Apache-2.0 ([LICENSE](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/LICENSE))。著作権は California Institute of Technology で、Caltech と JPL の名前を派生物の宣伝に使うことを禁じる注記がある ([README](https://github.com/NASA-AMMOS/3DTilesRendererJS#license)) |
| 運営主体・ガバナンス | NASA-AMMOS の GitHub organization (NASA/JPL 由来)。コミットの大半は gkjohnson (Garrett Johnson) で、確かめた時点の貢献数は 2 位以下を大きく上回る (2,649 件。2 位は dependabot の 87 件) ([contributors](https://github.com/NASA-AMMOS/3DTilesRendererJS/graphs/contributors))。財団などのガバナンス文書は無い |

## 概要

OGC 3D Tiles を読み込み、three.js、Babylon.js、PlayCanvas のシーンに表示する JavaScript ライブラリである ([README](https://github.com/NASA-AMMOS/3DTilesRendererJS))。描画エンジンではなく、タイルの選択、読み込み、キャッシュを受け持ち、描画はホストのエンジンに任せる。プラグインで Cesium ion と Google Photorealistic 3D Tiles の認証、quantized-mesh や Terrain-RGB の地形、XYZ / WMS / WMTS / GeoJSON / MVT / PMTiles の重ね合わせ、地球儀用のカメラ操作 (GlobeControls) を足せる ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md)、[core plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/core/plugins/API.md))。PLATEAU の建物を Cesium ion 経由で読むサンプルが公式にある ([plateau.js](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/example/three/plateau.js))。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU、独自エンジンか他ライブラリの上か): 他ライブラリの上。three.js (r167 以上)、Babylon.js (8 以上)、PlayCanvas (2.23 以上) を peerDependency に持つ ([npm 3d-tiles-renderer](https://www.npmjs.com/package/3d-tiles-renderer))。three.js では通常 WebGLRenderer を使う。three.js の WebGPURenderer と組み合わせた利用者の報告があり、精度の問題は `WebGPURenderer.highPrecision = true` で解決したとされる ([issue #1245](https://github.com/NASA-AMMOS/3DTilesRendererJS/issues/1245))。WebGPU を公式に対応と書いた記述は見つからなかった。
- 2D / 2.5D (傾き・回転) / 3D: 3D。2D の地図表示は主用途ではないが、GeneratedSurfacePlugin でタイル画像を平面に貼った面を作れる ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md))。
- 地球儀表示: 対応。GlobeControls で楕円体の地球を操作する ([README](https://github.com/NASA-AMMOS/3DTilesRendererJS)、[CHANGELOG](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/CHANGELOG.md))。ReorientationPlugin でタイルセットを原点付近に置き直してローカルなシーンとしても扱える ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md))。
- 対応する投影法: 3D Tiles は楕円体 (WGS84) 上に置く。重ね合わせる画像タイルの投影は EPSG:4326、EPSG:3857、EPSG:8857 (Equal Earth、0.5.3 から) ([ProjectionScheme.js](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/images/utils/ProjectionScheme.js)、[CHANGELOG](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/CHANGELOG.md))。0.5.3 から生成した面を投影した平面で表示する `projection` オプションがある。

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 (重ね合わせ) | ImageOverlayPlugin の XYZTilesOverlay、TMSTilesOverlay で 3D タイルや地形の上に貼る ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md)) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT と PMTiles は対応 (重ね合わせ)。MLT は未確認 | MVTOverlay は XYZ テンプレートの MVT を Canvas でラスタ化して貼る。PMTilesOverlay はベクタとラスタの PMTiles を読み、Range リクエストはブラウザに自動キャッシュされないので Service Worker でのキャッシュを勧めている。MVTAnnotationsPlugin でラベルも描ける ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md)) |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 非対応 | MVT の見た目は VectorTileStyle (fill、stroke、strokeWidth など) で指定し、MapLibre / Mapbox Style JSON を読む機能の記載は無い ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md)) |
| GeoJSON | 対応 (重ね合わせ) | GeoJSONOverlay が Canvas 2D でタイルごとにラスタ化して貼る。地物ごとの色や線幅は properties で上書きできる ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md)) |
| 3D Tiles / glTF | 対応 (主用途) | 3D Tiles の仕様の大部分に対応し、未実装の機能はマイルストーンで管理している ([README](https://github.com/NASA-AMMOS/3DTilesRendererJS))。B3DM、I3DM、PNTS、glTF の拡張 (Draco、KTX2、Meshopt、CESIUM_RTC、EXT_mesh_features、EXT_structural_metadata)、暗黙タイリング、Potree 点群 (0.5.3 から) を扱える ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md)、[core plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/core/plugins/API.md)、[CHANGELOG](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/CHANGELOG.md)) |
| 地形 (標高タイル) | 対応 | QuantizedMeshPlugin (Cesium の quantized-mesh)、TerrainRGBMeshPlugin (Terrain-RGB)、TerrariumMeshPlugin ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md)) |
| WMS / WMTS | 対応 (重ね合わせ) | WMSTilesOverlay、WMTSTilesOverlay と、それぞれの GetCapabilities を読むローダーがある ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md)) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリ側の制限は無い。Google Photorealistic 3D Tiles を使う場合は Google の Map Tiles API のポリシーに従う。Google Maps のロゴ (難しければ「Google Maps」の文字) と、データの帰属表示をそのまま表示し、他のロゴで隠さないこと、規約の例外を除き先読み・保存・キャッシュをしないこと、オフライン利用をしないこと、Photorealistic 3D Tiles から手作業や機械でなぞった 3D オブジェクトを作らないことが求められる ([Map Tiles API Policies](https://developers.google.com/maps/documentation/tile/policies))。GoogleCloudAuthPlugin はセッショントークンの管理、タイルごとの帰属表示の収集、ロゴ表示を行う ([core plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/core/plugins/API.md))。PMTiles 用に勧められている Service Worker のキャッシュを Google のタイルにも効かせると、キャッシュ禁止の規定に触れうる (推測)。
- API キー・アカウントの要否: ライブラリ自体には不要。Google のタイルは Google Maps Platform の API キー、Cesium ion のアセット (PLATEAU の例を含む) は Cesium ion のアクセストークンが要る ([README](https://github.com/NASA-AMMOS/3DTilesRendererJS))。

## ライセンスと費用

- ライセンス: Apache-2.0 ([LICENSE](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/LICENSE))。
- 利用料 (無料 / 従量 / 有料の機能): ライブラリは無料。データ側の費用 (USD、2026-11-10 確認): Google の Photorealistic 3D Tiles は月 1,000 イベントまで無料、以降 1,000 イベントあたり $6.00 (10 万まで)、量に応じて $5.10、$4.20、$3.30、$2.40 と下がる ([Google Maps Platform pricing](https://developers.google.com/maps/billing-and-pricing/pricing))。Cesium ion は Community が無料 (個人・非商用向け)、Commercial が月 $149 から、Custom と Self-Hosted は問い合わせ制 ([Cesium pricing](https://cesium.com/pricing/))。
- 版によるライセンスの変化: なし。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): ライブラリ自体はなし (Apache-2.0 の通常の条件: 配布時の LICENSE 同梱と変更箇所の明示)。Caltech と JPL の名前を派生物の宣伝に使えない ([README](https://github.com/NASA-AMMOS/3DTilesRendererJS#license))。データ側では、Cesium ion の PLATEAU (Japan 3D Buildings) を使うアプリは国土交通省 3D 都市モデルの帰属表示を入れる必要がある ([Japan 3D Buildings](https://cesium.com/platform/cesium-ion/content/japan-3d-buildings/))。Google のタイルは上の帰属・キャッシュの条件がかかる。

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 30,098 バイト (v0.5.4、main エントリ、min は 107,304 バイト。three.js などの peerDependency は含まない) ([bundlephobia](https://bundlephobia.com/package/3d-tiles-renderer@0.5.4))。プラグインを読み込むとこれに加わる。依存として pbf、pmtiles、@mapbox/vector-tile を持つ ([npm 3d-tiles-renderer](https://www.npmjs.com/package/3d-tiles-renderer))。
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 対象外 (地物単位でなくタイル単位で読み込むため)。読み込み量は LRUCache の `maxSize` と `maxBytesSize` で上限を決め、上限に達すると新しいタイルを読まず粗いタイルのまま表示する ([README Gotchas](https://github.com/NASA-AMMOS/3DTilesRendererJS#gotchas))。
- 低性能端末・モバイルブラウザでの注意: 公式のモバイル向けの記述は見つからなかった。メモリの少ない端末ではキャッシュ上限 (`maxBytesSize`) と `errorTarget` を調整して読み込み量を抑えることになる ([README Gotchas](https://github.com/NASA-AMMOS/3DTilesRendererJS#gotchas))。

## エコシステム

- 主なプラグイン・拡張: 公式プラグイン (認証、地形、画像の重ね合わせ、フェード、バッチ描画、デバッグなど) と、コミュニティのプラグイン (3D Gaussian Splatting、スタイリング、アウトライン、MapLibre GL JS 連携の maplibre-gl-3d-tiles など) ([plugins README](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/README.md))。three-geospatial (大気・雲)、Giro3D、iTowns などが組み込んでいる。MapLibre GL JS の公式サンプルにも three.js のカスタムレイヤーで使う例がある ([README](https://github.com/NASA-AMMOS/3DTilesRendererJS#community-resources))。
- React / Vue などのラッパー: React Three Fiber 向けの `3d-tiles-renderer/r3f` を同梱 ([README](https://github.com/NASA-AMMOS/3DTilesRendererJS))。Vue の公式ラッパーは無い。
- TypeScript の型: 同梱 (`src/index.d.ts`) ([npm 3d-tiles-renderer](https://www.npmjs.com/package/3d-tiles-renderer))。
- 日本語の情報: PLATEAU 公式の学習コンテンツ「TOPIC 12 Three.js で活用する」がこのライブラリを使う (2023-03-03 公開、v0.3.13 時点) ([PLATEAU TOPIC 12](https://www.mlit.go.jp/plateau/learning/tpc12-2/))。この記事は CESIUM_RTC を自前で処理しているが、現行版には GLTFCesiumRTCExtension がある ([three plugins API](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md))。

## 開発の活発さ

- 直近 1 年のリリース数: 16 件 (2025-11-10 から 2026-11-10 まで、v0.4.18 から v0.5.4) ([GitHub Releases](https://github.com/NASA-AMMOS/3DTilesRendererJS/releases))。
- 最終コミット日: 2026-11-07 JST (master ブランチ) ([commits](https://github.com/NASA-AMMOS/3DTilesRendererJS/commits/master))。
- 近年の大きな破壊的変更: 1.0 前。v0.5.0 (2026-07-15) で非推奨 API を削除し、TilesRenderer の各種キューとキャッシュを既定で全インスタンス共有に変えた。v0.4.0 (2024-12-25) で three.js の最低版を r166 に上げ、非推奨関数を削除 ([CHANGELOG](https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/CHANGELOG.md))。

## 環境の違いと保守

- ブラウザ間の互換: 対応ブラウザを示した公式文書は未確認。CI は型の検査と Vitest を Node の環境で回すだけで、ブラウザでの自動テストはない (https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/.github/workflows/node.js.yml, https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/vitest.config.js)。描画は three.js などのエンジンに任せるので、ブラウザ間の違いはそのエンジンが吸収する (推測)。
- OS 間の互換: 対応 OS と端末、GPU の違いを述べた文書は未確認。メモリについては、タイルのキャッシュ (LRUCache) が `maxBytesSize` と `cachedBytes` でバイト数を数えて上限を設ける (https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/core/renderer/API.md)。WebXR のように `requestAnimationFrame` が使えない場面向けに、読み込みの予定を差し替える `schedulingCallback` を持つ (https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/CHANGELOG.md)。
- 操作の網羅: three.js 向けの EnvironmentControls がドラッグでのパン、スクロールでのズーム、右クリックでの回転、任意の減衰による慣性を持ち、`enableFlight` で W/A/S/D と矢印キーのキーボード飛行ができる。GlobeControls は楕円体に沿った回転と地球儀の慣性を持つ (https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/renderer/API.md)。ポインタの追跡は `PointerTracker` が受け持つ (https://github.com/NASA-AMMOS/3DTilesRendererJS/tree/master/src/three/renderer/controls)。ページのスクロールと両立させる設定は未確認。
- エッジケースへの対応: タイルの読み込み失敗は `load-error` イベント (タイル、エラー、URL を渡す) で受ける (https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/core/renderer/API.md)。自動の再試行は未確認。精度については、ReorientationPlugin でタイルセットを原点付近に置き直してローカルなシーンとして扱える (https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md)。WebGL のコンテキスト喪失の扱いはコード検索で見つからなかった (`repo:NASA-AMMOS/3DTilesRendererJS contextlost`、2026-11-12、未確認)。
- 継続的な保守: CSP についての公式文書は未確認。ブラウザ別のラベルはなく、タイトルに Safari を含む issue は 1 件、Firefox は 3 件、iOS は 0 件である (GitHub の issue 検索、`repo:NASA-AMMOS/3DTilesRendererJS` に各条件を付けて、2026-11-12)。

## 向いている場面

- three.js (または Babylon.js、PlayCanvas、React Three Fiber) で作る 3D 表現に、PLATEAU、Google Photorealistic 3D Tiles、点群などの 3D Tiles を組み込む場合。
- CesiumJS ほど大きな仕組みを持ち込まず、シーンの描画やマテリアルを自分で制御したい場合。
- MapLibre GL JS の地図の上に 3D Tiles を重ねる場合 (three.js のカスタムレイヤー経由)。

## 向いていない場面

- 道路地図などの 2D 地図を MapLibre Style で描く用途 (スタイル仕様に対応しない)。
- three.js などの 3D エンジンを扱う開発体制が無い場合 (カメラ、ライト、描画ループを自分で書く)。
- API の安定性を重視する場合 (1.0 前で、0.x のマイナー版で破壊的変更が入る)。
- 主要な開発者がほぼ 1 人であることを調達上のリスクと見る場合。

## 出典

- https://github.com/NASA-AMMOS/3DTilesRendererJS
- https://github.com/NASA-AMMOS/3DTilesRendererJS#license
- https://github.com/NASA-AMMOS/3DTilesRendererJS#gotchas
- https://github.com/NASA-AMMOS/3DTilesRendererJS#community-resources
- https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/LICENSE
- https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/USAGE.md
- https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/CHANGELOG.md
- https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/API.md
- https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/README.md
- https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/core/plugins/API.md
- https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/src/three/plugins/images/utils/ProjectionScheme.js
- https://github.com/NASA-AMMOS/3DTilesRendererJS/blob/master/example/three/plateau.js
- https://github.com/NASA-AMMOS/3DTilesRendererJS/releases
- https://github.com/NASA-AMMOS/3DTilesRendererJS/releases/tag/v0.5.4
- https://github.com/NASA-AMMOS/3DTilesRendererJS/commits/master
- https://github.com/NASA-AMMOS/3DTilesRendererJS/graphs/contributors
- https://github.com/NASA-AMMOS/3DTilesRendererJS/issues/1245
- https://nasa-ammos.github.io/3DTilesRendererJS/
- https://www.npmjs.com/package/3d-tiles-renderer
- https://bundlephobia.com/package/3d-tiles-renderer@0.5.4
- https://developers.google.com/maps/documentation/tile/policies
- https://developers.google.com/maps/billing-and-pricing/pricing
- https://cesium.com/pricing/
- https://cesium.com/platform/cesium-ion/content/japan-3d-buildings/
- https://www.mlit.go.jp/plateau/learning/tpc12-2/

## 未確認のこと

- WebGPU への公式な対応状況。利用者の報告 (issue) はあるが、README や CHANGELOG に対応を明記した記述が見つからなかった。
- MLT (MapLibre Tiles) への対応。プラグインの API 一覧に記載が無かった。
- モバイルブラウザでの公式な推奨設定や動作要件。ドキュメントに記載が見つからなかった。
- Google Maps Platform の利用規約本文にある、Google 以外の地図との併用の制限の条文。規約ページの本文を取得できず、Map Tiles API のポリシーだけを確かめた。
- Cesium ion 経由で Google Photorealistic 3D Tiles を読む場合の課金の扱い (ion 側の配信量か Google 側の課金か)。
