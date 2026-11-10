# CesiumJS

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 1.147 (2026-11-02)。毎月 1 日前後に 1 版ずつ出る (https://github.com/CesiumGS/cesium/releases) |
| リポジトリ | https://github.com/CesiumGS/cesium |
| ドキュメント | https://cesium.com/learn/cesiumjs/ref-doc/ |
| ライセンス (LICENSE ファイルで確かめる) | Apache-2.0 (リポジトリ直下の LICENSE.md、GitHub の判定も Apache-2.0、npm の `license` も Apache-2.0) |
| 運営主体・ガバナンス | Cesium 社が開発する。Cesium 社は 2024-09-06 に Bentley Systems に買収された (https://cesium.com/blog/2024/09/06/cesium-joins-bentley/ 、https://www.bentley.com/news/bentley-systems-acquires-3d-geospatial-company-cesium/) |

## 概要

CesiumJS は Web ブラウザで 3D 地球儀と地図を描く JavaScript ライブラリである (https://github.com/CesiumGS/cesium)。地形、衛星画像、3D Tiles、glTF モデル、GeoJSON・KML・CZML などを楕円体の地球上に重ねて表示する。3D Tiles 仕様の策定元でもあり、大規模な 3D 都市モデルや点群のストリーミング表示に使われる。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): WebGL。1.140 以降、ビルボードとラベルは WebGL 2、または `ANGLE_instanced_arrays` などを備えた WebGL 1 を要求する (https://github.com/CesiumGS/cesium/blob/main/CHANGES.md)。リポジトリに WebGPU の実装は見当たらない
- 2D / 2.5D (傾き・回転) / 3D: 3D、2D、2.5D (Columbus View) の 3 モードを切り替えられる (https://cesium.com/learn/cesiumjs/ref-doc/SceneMode.html)
- 地球儀表示: 対応 (既定は 3D の地球儀)
- 対応する投影法: 2D と Columbus View では Geographic (正距円筒) と Web Mercator を選べる (https://cesium.com/learn/cesiumjs/ref-doc/GeographicProjection.html 、https://cesium.com/learn/cesiumjs/ref-doc/WebMercatorProjection.html)

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | `UrlTemplateImageryProvider`、`OpenStreetMapImageryProvider` (https://cesium.com/learn/cesiumjs/ref-doc/UrlTemplateImageryProvider.html) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT は対応 (1.142 以降)。PMTiles と MLT は未確認 | 1.142 (2026-06-01) で `MVTDataProvider` が加わり、MVT を 3D Tiles として読み込む。1.145 で地形・3D Tiles へのドレープが加わった (https://github.com/CesiumGS/cesium/blob/main/CHANGES.md)。それ以前は外部ライブラリが必要だった (PLATEAU 配信サービスのチュートリアルは cesium-mvt-imagery-provider を使う。https://github.com/Project-PLATEAU/plateau-streaming-tutorial/blob/main/3d-tiles/plateau-3dtiles-streaming.md) |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 非対応 | 独自の `Cesium3DTileStyle` を使う。MapLibre Style を読む機能は CHANGES.md に見当たらない |
| GeoJSON | 対応 | `GeoJsonDataSource` (Entity ベース)。1.142 で大量データ向けの `GeoJsonPrimitive` が加わった (https://cesium.com/learn/cesiumjs/ref-doc/GeoJsonDataSource.html 、CHANGES.md) |
| 3D Tiles / glTF | 対応 | 3D Tiles 仕様の策定元。`Cesium3DTileset`、glTF の `Model`、Google Photorealistic 3D Tiles 用の `createGooglePhotorealistic3DTileset`、Gaussian splat も扱う (https://cesium.com/learn/cesiumjs/ref-doc/Cesium3DTileset.html) |
| 地形 (標高タイル) | 対応 | quantized-mesh の `CesiumTerrainProvider`、ArcGIS の標高タイルなど。既定の地形は平らな楕円体 (`EllipsoidTerrainProvider`) で、全球地形 `Terrain.fromWorldTerrain()` は Cesium ion から読む (https://cesium.com/learn/cesiumjs/ref-doc/Viewer.html 、https://cesium.com/learn/cesiumjs-learn/cesiumjs-quickstart/)。Terrain-RGB を直接読む機能は未確認 |
| WMS / WMTS | 対応 | `WebMapServiceImageryProvider`、`WebMapTileServiceImageryProvider` (https://cesium.com/learn/cesiumjs/ref-doc/WebMapServiceImageryProvider.html) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: 既定の背景 `ImageryLayer.fromWorldImagery()` は「ion の既定の全球画像、現在は Bing Maps」であり、Cesium ion の利用条件に従う (https://cesium.com/learn/cesiumjs/ref-doc/ImageryLayer.html)。ion を使わない構成では、背景画像・地形・建物を自前か他のサービスで用意する必要がある。ライブラリとして特定のサービスを禁じる記述は見当たらない
- API キー・アカウントの要否: ライブラリ自体は不要。ただし既定の Viewer は Cesium ion の資産 (Bing 画像、ジオコーダ) を使い、公式クイックスタートは ion のアクセストークンを設定する前提で書かれている (https://cesium.com/learn/cesiumjs-learn/cesiumjs-quickstart/)。ion を使わない場合は `baseLayer` などを自前のプロバイダに差し替える

## ライセンスと費用

- ライセンス: Apache-2.0
- 利用料 (無料 / 従量 / 有料の機能): CesiumJS は無料。Cesium ion は月額制で、Community は無料 (個人・非商用、ストレージ 10 GB、配信 15 GB/月)、Commercial は 149 USD/月 (個人) または 524 USD/月 (チーム)、Premium は 499 USD/月 (個人) または 874 USD/月 (チーム)、Custom は要問い合わせ (2026-11-10 に確認。https://cesium.com/platform/cesium-ion/pricing/)。同ページの FAQ は、年間売上か調達額が 5 万 USD を超える企業、政府案件、資金のある教育研究では有料アカウントが必要としている。組織外で使うソリューションに ion を組み込む場合は問い合わせるよう注記がある。ion にはセルフホスト版もあるが価格は非公開
- 版によるライセンスの変化: なし (Apache-2.0 のまま)

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 約 1.35 MB (cesium 1.147.0、min 約 4.95 MB。bundlephobia API の値、2026-11-10 取得。https://bundlephobia.com/package/cesium@1.147.0)。npm パッケージの展開サイズは約 80 MB (https://www.npmjs.com/package/cesium)
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 公式の上限値は未確認。CHANGES.md には 1.140 で性能重視の `BufferPointCollection` などを実験的に加えたこと、Gaussian splat で約 1,600 万点を超える場合のクラッシュを直したことが書かれている
- 低性能端末・モバイルブラウザでの注意: WebGL 2 (または拡張つき WebGL 1) を要求する機能がある (1.140)。バンドルが大きく、初回の読み込みに時間がかかる

## エコシステム

- 主なプラグイン・拡張: Cesium ion (変換・配信の SaaS)、3D Tiles 仕様、Google Photorealistic 3D Tiles 連携、iTwin 連携 (`ITwinData`)
- React / Vue などのラッパー: Resium (React、MIT、Re:Earth 組織が保守。https://github.com/reearth/resium)
- TypeScript の型: 同梱 (npm の `types` は `./Source/Cesium.d.ts`)
- ネイティブ版・兄弟プロジェクト: Cesium Native (C++、Apache-2.0。https://github.com/CesiumGS/cesium-native) と、それを使う Unreal / Unity 向けプラグイン。ゲームエンジンで使う場合は native/cesium-native.md を参照
- 日本語の情報 (公式翻訳、国内コミュニティ): 公式の日本語訳は未確認。国土交通省の Project PLATEAU は「3D都市モデルの可視化環境としてCesium及びRe:Earthを利用した」PLATEAU VIEW を運用しており、配信サービスのチュートリアルに CesiumJS のサンプルが日本語で載っている (https://github.com/Project-PLATEAU/plateau-streaming-tutorial)。PLATEAU VIEW 5.0 のエディタは Re:Earth 系のコード (`@reearth/core`) で、cesium 1.118 と resium に依存している (https://github.com/Project-PLATEAU/PLATEAU-VIEW-5.0)。同チュートリアルによれば、PLATEAU の地形データ (PLATEAU-Terrain) の作成と配信には Cesium ion を使っている

## 開発の活発さ

- 直近 1 年のリリース数: 13 (2025-11-10 から 2026-11-10 までの GitHub Releases。1.136 から 1.147、1.139.1 を含む)
- 最終コミット日: 2026-11-09 (main)
- 近年の大きな破壊的変更: 1.135 で Gaussian splat の旧拡張 `KHR_spz_gaussian_splats_compression` を削除。1.139 で Cartesian 系を ES6 クラス化し、静的ファクトリに `new` を付けると例外になった。1.141 で Node 22 以上が必須になった。1.145 で `ClippingPolygons` の座標が不変になった。1.146 で数学・ジオメトリ系を新パッケージ `@cesium/core` に分け、`@cesium/engine` からの再輸出は 1.150 で削除予定 (いずれも https://github.com/CesiumGS/cesium/blob/main/CHANGES.md)

## 向いている場面

- 3D Tiles の 3D 都市モデル (PLATEAU など)、点群、フォトグラメトリを地球儀上に表示する
- 地形と 3D モデルを組み合わせた本格的な 3D GIS や、時系列 (CZML) の可視化
- Cesium ion を契約して、データ変換と配信をまとめて任せる

## 向いていない場面

- MapLibre Style で書いた 2D のベクトルタイル地図をそのまま使いたい場合 (Style 仕様を読まない)
- バンドルサイズを小さく保ちたい軽量な地図
- ion を使わずに既定の見た目 (全球画像・地形) をそのまま商用で使いたい場合 (自前で差し替えが必要)

## 出典

- https://github.com/CesiumGS/cesium
- https://github.com/CesiumGS/cesium/releases
- https://github.com/CesiumGS/cesium/blob/main/CHANGES.md
- https://cesium.com/learn/cesiumjs/ref-doc/
- https://cesium.com/learn/cesiumjs/ref-doc/SceneMode.html
- https://cesium.com/learn/cesiumjs/ref-doc/GeographicProjection.html
- https://cesium.com/learn/cesiumjs/ref-doc/WebMercatorProjection.html
- https://cesium.com/learn/cesiumjs/ref-doc/UrlTemplateImageryProvider.html
- https://cesium.com/learn/cesiumjs/ref-doc/GeoJsonDataSource.html
- https://cesium.com/learn/cesiumjs/ref-doc/Cesium3DTileset.html
- https://cesium.com/learn/cesiumjs/ref-doc/WebMapServiceImageryProvider.html
- https://cesium.com/learn/cesiumjs/ref-doc/Viewer.html
- https://cesium.com/learn/cesiumjs/ref-doc/ImageryLayer.html
- https://cesium.com/learn/cesiumjs-learn/cesiumjs-quickstart/
- https://cesium.com/platform/cesium-ion/pricing/
- https://cesium.com/blog/2024/09/06/cesium-joins-bentley/
- https://www.bentley.com/news/bentley-systems-acquires-3d-geospatial-company-cesium/
- https://bundlephobia.com/package/cesium@1.147.0
- https://www.npmjs.com/package/cesium
- https://github.com/reearth/resium
- https://github.com/CesiumGS/cesium-native
- https://github.com/Project-PLATEAU/plateau-streaming-tutorial
- https://github.com/Project-PLATEAU/plateau-streaming-tutorial/blob/main/3d-tiles/plateau-3dtiles-streaming.md
- https://github.com/Project-PLATEAU/PLATEAU-VIEW-5.0

## 未確認のこと

- PMTiles と MLT の読み込み: CHANGES.md とソースツリーに記述が無く、公式ドキュメントでも確かめられなかった
- Terrain-RGB 形式の標高タイルを直接読む公式機能: ref-doc で該当するプロバイダを確かめられなかった
- 扱える地物数の公式の目安: 公式の記述が見つからなかった
- 公式の日本語ドキュメント: cesium.com に日本語版があるかを確かめられなかった
- PLATEAU VIEW 5.0 の公開ビューア (editor 以外の部分) がどの版の CesiumJS を使うか: editor/web と editor/core の package.json だけを確かめた
