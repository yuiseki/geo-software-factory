# maptalks.js

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | maptalks 1.13.0 と maptalks-gl 0.126.0 (どちらも npm 公開は 2026-10-20)。WebGPU 版の maptalks-gpu も 0.126.0 (https://www.npmjs.com/package/maptalks 、https://www.npmjs.com/package/maptalks-gl 、https://github.com/maptalks/maptalks.js/releases) |
| リポジトリ | https://github.com/maptalks/maptalks.js (モノレポ。旧来のコア `maptalks` は `packages/maptalks` にある) |
| ドキュメント | https://maptalks.org (API: https://maptalks.org/maptalks.js/api/1.x/Map.html 、Wiki: https://github.com/maptalks/maptalks.js/wiki 、例: https://maptalks.org/examples/en/map/load/) |
| ライセンス (LICENSE ファイルで確かめる) | パッケージごとに異なり、一部は OSS ライセンスが付いていない。リポジトリ直下に LICENSE ファイルは無い (GitHub の判定 none はこのため)。`packages/maptalks/LICENSE` は BSD-3-Clause (npm の `license` も BSD-3-Clause)。`packages/vt`、`analysis`、`layer-gltf`、`gltf-loader` の LICENSE は MIT。統合パッケージ maptalks-gl と maptalks-gpu の package.json は MIT。一方、maptalks-gl が依存する `@maptalks/gl`、`@maptalks/3dtiles`、`@maptalks/gltf-layer`、`@maptalks/video-layer`、`@maptalks/transform-control` などは package.json の `license` が `UNLICENSED` で、配布物の先頭にも「LICENSE : UNLICENSED」と書かれている (例: https://unpkg.com/@maptalks/gl@0.126.0/dist/maptalksgl.js)。npm の慣例で `UNLICENSED` は利用許諾を与えないことを示す (https://docs.npmjs.com/cli/v10/configuring-npm/package-json#license) |
| 運営主体・ガバナンス | 開発者の fuzhenn が 2012 年に開発を始め、2017 年に GitHub で公開した (https://github.com/maptalks/maptalks.js/issues/2471)。配布物の著作権表示は maptalks.org または maptalks.com。運営会社と意思決定の仕組みは未確認 |

## 概要

maptalks.js は 2D 地図を傾け・回転させて 2D と 3D を統合して扱う JavaScript 地図ライブラリである (https://maptalks.org)。現在は WebGL/WebGPU で描く maptalks-gl への移行中で、ベクトルタイル、3D Tiles、glTF、3D 解析、交通シミュレーションの機能を持つ (https://github.com/maptalks/maptalks.js)。2024-11 の Issue #2471 で、Canvas 2D の図層を廃止して純粋な WebGL/WebGPU エンジンへ移る方針が示されている。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): Canvas 2D (旧来の VectorLayer など) と WebGL (maptalks-gl)。WebGPU 版として maptalks-gpu がある (README)。Canvas 2D の図層は廃止の方針 (Issue #2471)
- 2D / 2.5D (傾き・回転) / 3D: 2.5D の平面地図に 3D の図層 (glTF、3D Tiles、地形) を重ねる
- 地球儀表示: 非対応。2020 年の Issue #1228 で作者が「コアライブラリでは地球儀モードを支持しない」と回答している (https://github.com/maptalks/maptalks.js/issues/1228)
- 対応する投影法: EPSG:3857、EPSG:4326、EPSG:9807、UTM、Baidu、IDENTITY (平面座標)、独自定義 (`packages/maptalks/src/geo/projection/`)。WMTS の空間参照も扱う

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | `TileLayer` の `urlTemplate` |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT は対応、PMTiles と MLT は未確認 | `@maptalks/vt` の `VectorTileLayer` (README)。PMTiles と MLT の実装はリポジトリと Issue で見つからなかった |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 非対応 (独自のスタイル) | 独自の symbol と renderPlugin のスタイルを使う (https://github.com/maptalks/maptalks.js/wiki/Symbol-Reference)。Mapbox Style を読む機能は未確認。mapbox-gl-js を図層として重ねるプラグインはある (https://maptalks.org) |
| GeoJSON | 対応 | `VectorLayer`、WebGL 版の `PointLayer`/`LineStringLayer`/`PolygonLayer`、`GeoJSONVectorTileLayer` (README) |
| 3D Tiles / glTF | 対応 | `Geo3DTilesLayer` (`@maptalks/3dtiles`) と `GLTFLayer`/`GLTFMarker`。Draco、KTX2、CRN のデコーダは別パッケージ。いずれも `UNLICENSED` のパッケージに含まれる |
| 地形 (標高タイル) | 対応 | `@maptalks/gl` の `TerrainLayer` が `mapbox` (Terrain-RGB)、`cesium`/`cesium-ion` (quantized-mesh)、`tianditu` の形式を扱う (`packages/gl/src/layer/terrain/TerrainLayer.js`)。`UNLICENSED` のパッケージに含まれる |
| WMS / WMTS | 対応 | `WMSTileLayer` と WMTS の空間参照 (`SpatialReference.WMTS.ts`) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリとして禁じる記述は見当たらない。地形で `cesium-ion` を使う場合は Cesium ion の規約に従う
- API キー・アカウントの要否: ライブラリ自体は不要

## ライセンスと費用

- ライセンス: 混在。コア `maptalks` は BSD-3-Clause、`@maptalks/vt` などは MIT、統合パッケージ maptalks-gl は MIT 表記。しかし maptalks-gl が依存する WebGL の基盤 `@maptalks/gl` と 3D Tiles・glTF の図層は `UNLICENSED` で、OSS としての利用許諾が書かれていない。maptalks-gl の 3D 機能を使うと、この許諾の無いパッケージを取り込むことになる
- 利用料 (無料 / 従量 / 有料の機能): 料金表は見当たらない。`UNLICENSED` のパッケージを商用で使ってよいかは公開情報で確かめられなかった
- 版によるライセンスの変化: 未確認。旧リポジトリ fuzhenn/gl-layers (maptalks-gl の前身) の時期のライセンスは確かめていない

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 約 188 KB (maptalks 1.13.0、min 約 635 KB)、約 790 KB (maptalks-gl 0.126.0、min 約 2.70 MB)。いずれも bundlephobia API の値、2026-11-10 取得 (https://bundlephobia.com/package/maptalks@1.13.0 、https://bundlephobia.com/package/maptalks-gl@0.126.0)
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 公式サイトは「Canvas 2D で 10ks、WebGL で 1000ks のジオメトリ」を滑らかに描けるとする (単位の意味が曖昧で、測定条件は書かれていない。https://maptalks.org)
- 低性能端末・モバイルブラウザでの注意: 公式サイトはモバイルブラウザに対応するとしている。Issue #2471 は、図層ごとに canvas を持ち合成する構造のため図層が増えるとフレームレートが落ちると説明している

## エコシステム

- 主なプラグイン・拡張: 公式サイトのプラグイン一覧に mapbox-gl-js、THREE、D3、ECharts との連携がある (https://maptalks.org)。モノレポ内に 3D 解析 (`@maptalks/analysis`)、交通シミュレーション (`@maptalks/traffic`)、変形操作 (`@maptalks/transform-control`)
- React / Vue などのラッパー: 公式のものは見当たらない
- TypeScript の型: 同梱 (maptalks は `dist/index.d.ts`、maptalks-gl は `index.d.ts`)
- ネイティブ版・兄弟プロジェクト: なし (見当たらない)
- 日本語の情報 (公式翻訳、国内コミュニティ): 見当たらない。Issue の議論は中国語が多い

## 開発の活発さ

- 直近 1 年のリリース数: npm で maptalks-gl 16 版、コアの maptalks 11 版 (2025-11-10 から 2026-11-10)。GitHub Releases は全パッケージ合わせて 18 件
- 最終コミット日: 2026-10-22 (master)
- 近年の大きな破壊的変更: Canvas 2D 図層 (VectorLayer など) の廃止と WebGL/WebGPU への一本化の方針 (Issue #2471、2024-11)。README は旧来の maptalks を「legacy maptalks」(maptalks/maptalks-canvas) と呼び、maptalks-gl へ移行できるとしている (移行手順は TBD)。実際にどの版で何が削除されたかは未確認

## 向いている場面

- 平面地図 (独自投影を含む) に 3D モデル・3D Tiles・地形を重ねる 2.5D の表現
- 中国の地図サービス (Baidu の投影、天地図の地形) と組み合わせる場合

## 向いていない場面

- 地球儀表示が必要な場合
- ライセンスを明確にしておく必要がある製品 (3D 機能の主要パッケージが `UNLICENSED`)
- MapLibre/Mapbox Style をそのまま使いたい場合

## 出典

- https://github.com/maptalks/maptalks.js
- https://github.com/maptalks/maptalks.js/releases
- https://github.com/maptalks/maptalks.js/blob/master/packages/maptalks/LICENSE
- https://github.com/maptalks/maptalks.js/blob/master/packages/vt/LICENSE
- https://github.com/maptalks/maptalks.js/blob/master/packages/gl/package.json
- https://github.com/maptalks/maptalks.js/blob/master/packages/gl/src/layer/terrain/TerrainLayer.js
- https://github.com/maptalks/maptalks.js/tree/master/packages/maptalks/src/geo/projection
- https://github.com/maptalks/maptalks.js/issues/2471
- https://github.com/maptalks/maptalks.js/issues/1228
- https://github.com/maptalks/maptalks.js/wiki
- https://github.com/maptalks/maptalks.js/wiki/Symbol-Reference
- https://maptalks.org
- https://maptalks.org/maptalks.js/api/1.x/Map.html
- https://maptalks.org/examples/en/map/load/
- https://www.npmjs.com/package/maptalks
- https://www.npmjs.com/package/maptalks-gl
- https://unpkg.com/@maptalks/gl@0.126.0/dist/maptalksgl.js
- https://unpkg.com/maptalks-gl@0.126.0/dist/maptalks-gl.js
- https://docs.npmjs.com/cli/v10/configuring-npm/package-json#license
- https://bundlephobia.com/package/maptalks@1.13.0
- https://bundlephobia.com/package/maptalks-gl@0.126.0

## 未確認のこと

- `UNLICENSED` パッケージ (`@maptalks/gl`、`@maptalks/3dtiles` など) の利用条件: リポジトリ、npm、公式サイトのいずれにも許諾の説明が無く、商用利用の可否や有償ライセンスの有無を確かめられなかった
- 運営主体 (maptalks.com の会社) とガバナンス: 公式サイトに会社名の記載が無かった
- PMTiles と MLT への対応: 実装も Issue も見つからなかった
- Mapbox Style を読む機能の有無: ドキュメントで確かめられなかった
- Canvas 2D 図層の廃止がどの版で実施されたか: CHANGELOG を版ごとに照合していない
- maptalks-gl の前身 (fuzhenn/gl-layers) の時期のライセンス: 確かめていない
