# deck.gl

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | v9.4.1 (2026-10-28、JST)。9.3 系の保守版 v9.3.12 が 2026-10-30 に出ている ([GitHub Releases](https://github.com/visgl/deck.gl/releases)、[npm](https://www.npmjs.com/package/deck.gl))。9.4 は v9 系の最後のリリースになる見込みと公式が書いている ([What's New](https://deck.gl/docs/whats-new)) |
| リポジトリ | https://github.com/visgl/deck.gl |
| ドキュメント | https://deck.gl/docs |
| ライセンス (LICENSE ファイルで確かめる) | MIT (Copyright Vis.gl contributors) ([LICENSE](https://github.com/visgl/deck.gl/blob/master/LICENSE)) |
| 運営主体・ガバナンス | vis.gl の一部で、vis.gl は OpenJS Foundation のプロジェクト ([README](https://github.com/visgl/deck.gl/blob/master/README.md)) |

## 概要

GPU を使って大量の地理データを描く可視化フレームワークである。点、線、ポリゴン、ヒートマップ、六角形集計、タイル、3D Tiles などをレイヤーとして重ね、MapLibre GL JS、Mapbox GL JS、Google Maps、ArcGIS などのベース地図と同期させるか、ベース地図なしで単独で使う ([modules 一覧](https://github.com/visgl/deck.gl/tree/master/modules)、[Using with MapLibre](https://deck.gl/docs/developer-guide/base-maps/using-with-maplibre))。ベース地図そのもの (道路や注記のスタイル描画) を担うライブラリではなく、データを可視化する層を担う。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): WebGL2 (luma.gl 経由)。WebGPU は試験的。9.2 (2025-10-07) で一部レイヤーの早期プレビューが始まり、9.4 (2026-09-05) のリリースノートは公式レイヤーカタログの全レイヤーが WebGPU に対応したとするが、WebGPU ガイドの対応表では CARTO のレイヤー (`@deck.gl/carto`) と拡張の多くが未実装 (❌) のままで、両者は食い違う。本番利用はまだ勧めないと公式が明記している。一部の機能は WebGPU で使えないか部分対応 ([What's New](https://deck.gl/docs/whats-new)、[WebGPU ガイド](https://deck.gl/docs/developer-guide/webgpu))
- 2D / 2.5D (傾き・回転) / 3D: 2D、傾き・回転、3D すべて。MapView (地図)、OrbitView、FirstPersonView、OrthographicView を持つ ([API リファレンス core](https://github.com/visgl/deck.gl/tree/master/docs/api-reference/core))。9.3 で地形に沿って視点を動かす TerrainController が入った ([What's New](https://deck.gl/docs/whats-new))
- 地球儀表示: GlobeView があるが試験的。ズーム 12 を超えると精度が落ちる、座標系は経緯度のみ、HeatmapLayer と ContourLayer は動かない、TileLayer / MVTLayer / TerrainLayer の対応は試験的、などの制限がある ([GlobeView](https://deck.gl/docs/api-reference/core/globe-view))。9.4 で TerrainLayer、Tile3DLayer、IconLayer、TextLayer などが地球儀上で動くようになった ([What's New](https://deck.gl/docs/whats-new))
- 対応する投影法: Web メルカトル (MapView)、地球儀 (GlobeView、試験的)、地理座標を使わない直交・透視ビュー。任意の CRS で平面地図を描く `_CustomProjectionView` は master の What's New では「Unreleased」節にあり、9.4.1 時点の安定版には含まれない ([What's New (master)](https://github.com/visgl/deck.gl/blob/master/docs/whats-new.md)、[CustomProjectionView](https://github.com/visgl/deck.gl/blob/master/docs/api-reference/core/custom-projection-view.md))

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | TileLayer の `renderSubLayers` で BitmapLayer を使って描く ([TileLayer](https://deck.gl/docs/api-reference/geo-layers/tile-layer)) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT は対応、PMTiles と MLT は未確認 | MVTLayer が URL テンプレートか TileJSON を受け取る。既定でバイナリ形式を使い、大きなデータで 2〜3 倍速いとしている ([MVTLayer](https://deck.gl/docs/api-reference/geo-layers/mvt-layer))。deck.gl のドキュメントとソース (geo-layers、mapbox、maplibre) に PMTiles と MLT の記述はなかった |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 非対応 | MVTLayer の見た目は GeoJsonLayer と同じアクセサ (`getFillColor` など) で指定する ([MVTLayer](https://deck.gl/docs/api-reference/geo-layers/mvt-layer))。スタイル仕様で描く地図はベース地図側 (MapLibre など) に任せる |
| GeoJSON | 対応 | GeoJsonLayer |
| 3D Tiles / glTF | 対応 | Tile3DLayer が OGC 3D Tiles (点群、glTF、I3S) を読み、Google の Photorealistic 3D Tiles や Cesium ion の例が公式にある。glTF モデルは ScenegraphLayer ([Using with 3D Tiles](https://github.com/visgl/deck.gl/blob/master/docs/developer-guide/base-maps/using-with-3d-tiles.md)、[Tile3DLayer](https://deck.gl/docs/api-reference/geo-layers/tile-3d-layer)) |
| 地形 (標高タイル) | 対応 | TerrainLayer が標高画像からメッシュを作る。`elevationDecoder` で Mapbox Terrain-RGB や Terrarium などのエンコードを指定する ([TerrainLayer](https://deck.gl/docs/api-reference/geo-layers/terrain-layer)) |
| WMS / WMTS | WMS は試験的に対応、WMTS は未確認 | WMSLayer (v8.9 から、試験的) が表示範囲ごとに 1 枚の画像を要求する ([WMSLayer](https://deck.gl/docs/api-reference/geo-layers/wms-layer))。WMTS は XYZ 形式の URL で引ければ TileLayer で扱える (推測) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: deck.gl 自体に制約はない。重ねる先のベース地図とタイルの規約に従う。Google Maps と組み合わせる場合は `GoogleMapsOverlay` を使い、Google の地図の上に描く ([Using with Google Maps](https://github.com/visgl/deck.gl/blob/master/docs/developer-guide/base-maps/using-with-google-maps.md))。Google Maps Platform 利用規約 3.2.3(e) は Google の地図と Google 以外の地図の併用を禁じている ([利用規約](https://cloud.google.com/maps-platform/terms))。Google の 3D Tiles を読むには Google Maps の API キーが要る ([Tile3DLayer](https://deck.gl/docs/api-reference/geo-layers/tile-3d-layer))
- API キー・アカウントの要否: deck.gl 自体は不要。ベース地図やタイル (Mapbox、Google、CARTO など) 側で要る場合がある

## ライセンスと費用

- ライセンス: MIT ([LICENSE](https://github.com/visgl/deck.gl/blob/master/LICENSE))
- 利用料 (無料 / 従量 / 有料の機能): 無料。費用はベース地図とデータ配信の側で発生する
- 版によるライセンスの変化: なし

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): `deck.gl` 一括パッケージ 9.4.1 で 545,189 バイト、`@deck.gl/core` 9.4.1 で 217,973 バイト、`@deck.gl/layers` 9.4.1 で 57,656 バイト ([bundlephobia deck.gl@9.4.1](https://bundlephobia.com/package/deck.gl@9.4.1)、[bundlephobia @deck.gl/core@9.4.1](https://bundlephobia.com/package/@deck.gl/core@9.4.1))。公式の計測 (v9.4.0-alpha.2、esbuild で minify、gzip -9) では Deck + Layer の最小構成が 146.8 kB、WebGL のみに絞るエクスポート条件 `visgl:webgl-only` で 144.5 kB ([Building Apps](https://deck.gl/docs/developer-guide/building-apps))
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 2015 年の MacBook Pro (デュアル GPU) で、ScatterplotLayer などの基本レイヤーなら約 100 万件までパン・ズーム中 60 FPS。1,000 万件に近づくと 10〜20 FPS。1,000 万〜1 億件の間で GPU バッファ生成時にブラウザのメモリ上限に当たることが多く、レイヤーを分けて回避する ([Performance](https://deck.gl/docs/developer-guide/performance))
- 低性能端末・モバイルブラウザでの注意: スマートフォンはノート PC よりメモリ圧迫に弱く、ブラウザの再起動やページ再読み込みが起きやすい。データの読み込みも遅く、調整が要る。`useDevicePixels` を切ると描画するピクセル数が減って速くなる ([Performance](https://deck.gl/docs/developer-guide/performance))。WebGPU は試験的なので、モバイルで WebGPU 前提の構成は取りにくい

## エコシステム

- 主なプラグイン・拡張: 公式モジュールに aggregation-layers、geo-layers、mesh-layers、extensions、widgets、json、jupyter-widget、carto、arcgis、google-maps、mapbox、maplibre がある ([modules 一覧](https://github.com/visgl/deck.gl/tree/master/modules))。MapLibre には `@deck.gl/maplibre` の `MapLibreOverlay` (9.4 で `@deck.gl/mapbox` から分岐、MapLibre GL JS v4.5.1 / v5 / v6 に対応)。interleaved (MapLibre の WebGL2 コンテキストに描き、地図レイヤーと前後関係を混ぜる)、overlaid (別キャンバス)、reverse-controlled の 3 方式がある ([Using with MapLibre](https://deck.gl/docs/developer-guide/base-maps/using-with-maplibre)、[What's New](https://deck.gl/docs/whats-new))。Mapbox には `MapboxOverlay`、interleaved は mapbox-gl v2.13 以降 ([Using with Mapbox](https://deck.gl/docs/developer-guide/base-maps/using-with-mapbox))。Google Maps には `GoogleMapsOverlay`、ベクターマップなら WebGL2 コンテキストを共有して interleaved、ラスターマップか WebGL2 なしなら overlaid に切り替わり、overlaid では傾き・回転・フラクショナルズームが使えない ([Using with Google Maps](https://github.com/visgl/deck.gl/blob/master/docs/developer-guide/base-maps/using-with-google-maps.md)、[GoogleMapsOverlay](https://deck.gl/docs/api-reference/google-maps/google-maps-overlay))
- React / Vue などのラッパー: React は公式の `@deck.gl/react` ([npm](https://www.npmjs.com/package/@deck.gl/react))。Vue の公式ラッパーは未確認
- TypeScript の型: 同梱。8.9 で任意、9.0 から既定で有効 ([What's New](https://deck.gl/docs/whats-new))
- ネイティブ版・兄弟プロジェクト: Python から使う pydeck (PyPI 0.9.3) と Jupyter 用ウィジェット (`bindings/pydeck`、`modules/jupyter-widget`) ([リポジトリ](https://github.com/visgl/deck.gl)、[PyPI pydeck](https://pypi.org/project/pydeck/))。vis.gl の兄弟として luma.gl (GPU 抽象化)、loaders.gl (データ読み込み)、react-map-gl、`@vis.gl/react-google-maps` がある
- 日本語の情報 (公式翻訳、国内コミュニティ): 公式ドキュメントは英語のみ (日本語訳の案内は見当たらない)。国内コミュニティは未確認

## 開発の活発さ

- 直近 1 年のリリース数: 24 (2025-11-10〜2026-11-10 に GitHub Releases で公開された、プレリリースを除く版の数。9.2 系、9.3 系、9.4 系の保守版を含む)
- 最終コミット日: 2026-11-09 (master ブランチ、JST)
- 近年の大きな破壊的変更: 9.0 (2024-03-21) で luma.gl v9 の API に移り、`DeckProps.gl` が `device` に変わるなど避けられない破壊的変更があった ([What's New](https://deck.gl/docs/whats-new)、[Upgrade Guide](https://deck.gl/docs/upgrade-guide))。9.1 (2025-01-21) でシェーダーを uniform buffer に移し、独自レイヤーの移行が必要になった ([What's New](https://deck.gl/docs/whats-new))。次の v10 は luma.gl v10 と loaders.gl v5 を伴う大きな変更になる見込み ([What's New](https://deck.gl/docs/whats-new))

## 向いている場面

- 数十万〜百万件規模の点・線・ポリゴンを、GPU で滑らかに描きたい場合
- 集計 (六角形、グリッド、ヒートマップ) や時系列アニメーション (TripsLayer) など、可視化の表現が中心の場合
- MapLibre、Mapbox、Google Maps のどれかを既に使っていて、その上に大量データの層を足したい場合
- 3D Tiles や点群を Web で扱いたい場合
- Python / Jupyter での分析結果を地図で見せたい場合 (pydeck)

## 向いていない場面

- ベース地図そのもの (道路、注記、スタイル仕様に基づく地図) を描く用途。ベース地図ライブラリと組み合わせる前提になる
- 地球儀表示が主役の用途 (GlobeView は試験的で制限が多い)
- WebGPU を本番で使いたい場合 (公式が本番利用をまだ勧めていない)
- 数件のマーカーを置くだけの単純な地図 (バンドルサイズと学習コストに見合わない)

## 出典

- https://github.com/visgl/deck.gl
- https://github.com/visgl/deck.gl/releases
- https://github.com/visgl/deck.gl/blob/master/LICENSE
- https://github.com/visgl/deck.gl/blob/master/README.md
- https://github.com/visgl/deck.gl/tree/master/modules
- https://github.com/visgl/deck.gl/tree/master/docs/api-reference/core
- https://github.com/visgl/deck.gl/blob/master/docs/whats-new.md
- https://github.com/visgl/deck.gl/blob/master/docs/api-reference/core/custom-projection-view.md
- https://github.com/visgl/deck.gl/blob/master/docs/developer-guide/base-maps/using-with-3d-tiles.md
- https://github.com/visgl/deck.gl/blob/master/docs/developer-guide/base-maps/using-with-google-maps.md
- https://deck.gl/docs
- https://deck.gl/docs/whats-new
- https://deck.gl/docs/upgrade-guide
- https://deck.gl/docs/developer-guide/webgpu
- https://deck.gl/docs/developer-guide/performance
- https://deck.gl/docs/developer-guide/building-apps
- https://deck.gl/docs/developer-guide/base-maps/using-with-maplibre
- https://deck.gl/docs/developer-guide/base-maps/using-with-mapbox
- https://deck.gl/docs/api-reference/core/globe-view
- https://deck.gl/docs/api-reference/geo-layers/tile-layer
- https://deck.gl/docs/api-reference/geo-layers/mvt-layer
- https://deck.gl/docs/api-reference/geo-layers/terrain-layer
- https://deck.gl/docs/api-reference/geo-layers/tile-3d-layer
- https://deck.gl/docs/api-reference/geo-layers/wms-layer
- https://deck.gl/docs/api-reference/google-maps/google-maps-overlay
- https://cloud.google.com/maps-platform/terms
- https://www.npmjs.com/package/deck.gl
- https://www.npmjs.com/package/@deck.gl/react
- https://bundlephobia.com/package/deck.gl@9.4.1
- https://bundlephobia.com/package/@deck.gl/core@9.4.1
- https://pypi.org/project/pydeck/

## 未確認のこと

- PMTiles と MLT: deck.gl のドキュメントと geo-layers / mapbox / maplibre のソースを検索したが記述がなかった。loaders.gl 側の対応は調べていない
- WMTS: 公式ドキュメントに記述がない
- 9.0 で WebGL1 対応が完全になくなったか: What's New と Upgrade Guide に明記された箇所を見つけられなかった
- Vue 向けの公式ラッパー、国内コミュニティ: 公式の案内が見つからなかった
- 9.4 の公式バンドルサイズ表は v9.4.0-alpha.2 での計測であり、9.4.1 での公式計測値は見当たらない
