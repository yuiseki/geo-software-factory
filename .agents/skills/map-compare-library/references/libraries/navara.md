# Navara (MapLibre)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | v0.3.0 (2026-11-09)。0.x 系で、1.0 には達していない (https://github.com/maplibre/navara/releases) |
| リポジトリ | https://github.com/maplibre/navara |
| ドキュメント | https://navara.world/docs/ (日本語版あり)、例: https://navara.world/examples/ |
| ライセンス (LICENSE ファイルで確かめる) | MIT と Apache-2.0 のデュアルライセンス (利用者がどちらかを選ぶ)。LICENSE に「dual-licensed under either of Apache License, Version 2.0 / MIT license at your option」とあり、本文は LICENSE-APACHE と LICENSE-MIT に分かれている。GitHub の判定が NOASSERTION なのはこの構成のためと考えられる (推測)。npm の `license` は `MIT OR Apache-2.0` |
| 運営主体・ガバナンス | MapLibre 組織のリポジトリ。もとは reearth/navara で、2026-07-17 に MapLibre への受け入れ申請 (maplibre/maplibre#509) が出され、理事 2 名の承認を得て移管された (https://github.com/maplibre/maplibre/issues/509)。reearth 組織の名義は Eukarya, Inc. (https://github.com/reearth)。コミットの大半は keiya01 による (https://github.com/maplibre/navara/graphs/contributors) |

## 概要

Navara は拡張性を重視した汎用の 3D 地図エンジンで、衛星画像・地形・3D 都市モデル・ベクトルデータを地球儀上にストリーミング表示する (https://navara.world/docs/guides/introduction/what-is-navara/)。地理空間計算は Web Worker 上の Rust/WASM エンジンが担い、描画は Three.js に任せる (README)。宣言的 API、プラグイン、低レベル API、独自シェーダの 4 段の API を持つ。MapLibre GL JS とはコードを共有しない別エンジンであり、MapLibre Style をプラグインで読み込むことで MapLibre の生態系とつながる。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): WebGL (Three.js の `WebGLRenderer` を使う。`web/navara_three/src/scene.ts`)。README は描画層を差し替え可能にして将来ほかの描画エンジンへ広げるとしている
- 2D / 2.5D (傾き・回転) / 3D: 3D
- 地球儀表示: 対応 (地球儀が前提)
- 対応する投影法: 地球儀 (ECEF) 上に表示する。入力タイルは Web Mercator と EPSG:4326 (quantized-mesh の `geographic` オプション)。平面の地図投影モードは未確認

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | `raster-tile` Source。XYZ と TMS (https://navara.world/docs/ja/three/source/raster-tile-source/) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT と PMTiles は対応、MLT は未対応 | `vector-tile` Source が `{z}/{x}/{y}` のテンプレートと `.pmtiles` の URL を受け付ける (https://navara.world/docs/ja/three/source/vector-tile-source/)。MLT は受け入れ申請でロードマップにあると述べている (maplibre/maplibre#509) |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 部分対応 (実験的) | `@navaramap/maplibre-style` の `MapLibreStylePlugin` が MapLibre Style の「実用的な部分集合」を読む。fill、line、circle、symbol と vector、raster、GeoJSON の Source を扱う。API は変わりうると明記されている。SDF グリフ (`glyphs`) は非対応で、Web フォントを `font-faces` で読む (https://navara.world/docs/maplibre_style/about/) |
| GeoJSON | 対応 | `geojson` Source を `vector` レイヤーで描く |
| 3D Tiles / glTF | 対応 | 3D Tiles 1.0 (b3dm、pnts) と 1.1 (GLB コンテンツ、`EXT_mesh_features`、`EXT_structural_metadata`、Draco、meshopt) と Google Photorealistic 3D Tiles。pnts の一部属性は非対応 (https://navara.world/docs/ja/three/source/3d-tiles-source/) |
| 地形 (標高タイル) | 対応 | `raster-dem` (国土地理院、Mapbox Terrain-RGB、Terrarium の各デコーダを用意) と Cesium の `quantized-mesh` (https://navara.world/docs/ja/three/source/raster-dem-source/) |
| WMS / WMTS | WMTS は URL テンプレートで可、WMS は未確認 | 公式例は NASA GIBS の WMTS を `{z}/{y}/{x}` テンプレートとして `raster-tile` で読んでいる。WMS 専用の Source は無い |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリとして禁じる記述は見当たらない。Google Photorealistic 3D Tiles を使う場合は Google Maps Platform の規約に従う必要がある
- API キー・アカウントの要否: ライブラリ自体は不要。`quantized-mesh` Source には Bearer トークンを渡す `token` 項目がある

## ライセンスと費用

- ライセンス: MIT OR Apache-2.0
- 利用料 (無料 / 従量 / 有料の機能): 無料。有料版は見当たらない
- 版によるライセンスの変化: 未確認。現行の LICENSE 3 ファイルは 2026-07-17 (受け入れ申請と同日) に入った。それ以前の reearth/navara 時代のライセンスは確かめていない

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 約 405 KB (@navaramap/three 0.3.0、min 約 1.67 MB。bundlephobia API の値、2026-11-10 取得。https://bundlephobia.com/package/@navaramap/three@0.3.0)。peer dependency の three (0.183.0 で約 180 KB) と postprocessing、WASM と Worker のファイルは含まないとみられる (推測)。npm パッケージの展開サイズは約 65 MB
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 公式の数値は未確認。ドキュメントは計算を Worker の Rust/WASM に分けるため大規模データでも応答性を保つと述べている
- 低性能端末・モバイルブラウザでの注意: v0.3.0 で「Mobile crashes by shader trouble」と iOS のカメラ移動の不具合を修正しており、モバイル対応は途上とみられる (https://github.com/maplibre/navara/blob/main/CHANGELOG.md)

## エコシステム

- 主なプラグイン・拡張: `@navaramap/three-default-plugin` (フォトリアルな空・太陽・大気)、`@navaramap/three-plugins` (一人称視点、DOM オーバーレイ、帰属表示など)、`@navaramap/maplibre-style`。大気と雲は @takram/three-atmosphere、@takram/three-clouds に依存する
- React / Vue などのラッパー: `@navaramap/three-react` (React 19 以上)
- TypeScript の型: 同梱 (各パッケージの `types` は `dist/index.d.ts`)
- ネイティブ版・兄弟プロジェクト: Rust の GIS コア (`crates/`) は描画エンジンから独立しており、地理計算は `@navaramap/three-api` として単体で使える。ネイティブ版は無い
- 日本語の情報 (公式翻訳、国内コミュニティ): 公式ドキュメントに日本語版がある (https://navara.world/docs/ja/)。FOSS4G 2025 で発表があった (https://talks.osgeo.org/foss4g-2025/talk/RM9RHS/)

## 開発の活発さ

- 直近 1 年のリリース数: 13 (GitHub Releases の v0.0.1 から v0.3.0。最初のリリースは 2026-07-22)
- 最終コミット日: 2026-11-09 (main)
- 近年の大きな破壊的変更: v0.3.0 で MapLibre Style の color-relief 対応と、テキスト・スプライトのアンカー指定の変更が BREAKING とされている (https://github.com/maplibre/navara/blob/main/CHANGELOG.md)。0.x のため今後も変わりうる

## 向いている場面

- MapLibre の生態系 (MVT、PMTiles、MapLibre Style) のデータを 3D 地球儀上で使いたい場合
- 3D Tiles の都市モデルと地形を、フォトリアルな大気・影つきで見せたい場合
- 独自のシェーダや描画効果を加えたい場合

## 向いていない場面

- 本番で長期に安定した API が必要な場合 (0.x で破壊的変更が続く)
- MapLibre Style の全機能を 2D 地図として忠実に再現したい場合 (部分対応、SDF グリフ非対応。この用途は MapLibre GL JS)
- バンドルと初期読み込みを小さく保ちたい場合 (Three.js と WASM が必要)

## 出典

- https://github.com/maplibre/navara
- https://github.com/maplibre/navara/releases
- https://github.com/maplibre/navara/blob/main/LICENSE
- https://github.com/maplibre/navara/blob/main/CHANGELOG.md
- https://github.com/maplibre/navara/graphs/contributors
- https://github.com/maplibre/navara/blob/main/web/navara_three/src/scene.ts
- https://github.com/maplibre/maplibre/issues/509
- https://github.com/reearth
- https://navara.world/docs/
- https://navara.world/docs/ja/
- https://navara.world/examples/
- https://navara.world/docs/guides/introduction/what-is-navara/
- https://navara.world/docs/maplibre_style/about/
- https://navara.world/docs/ja/three/source/raster-tile-source/
- https://navara.world/docs/ja/three/source/vector-tile-source/
- https://navara.world/docs/ja/three/source/3d-tiles-source/
- https://navara.world/docs/ja/three/source/raster-dem-source/
- https://www.npmjs.com/package/@navaramap/three
- https://bundlephobia.com/package/@navaramap/three@0.3.0
- https://talks.osgeo.org/foss4g-2025/talk/RM9RHS/

## 未確認のこと

- MapLibre への移管が完了した日: 受け入れ申請の Issue は 2026-11-10 時点で open のままで、移管日を示す記録を見つけられなかった
- reearth/navara 時代のライセンス: 移管前のリポジトリを確かめていない
- 平面の地図投影モードの有無: ドキュメントに記述が見当たらなかった
- WMS の扱い: 専用の Source が無いことだけを確かめた
- バンドルサイズに WASM と Worker が含まれるか: bundlephobia の計測範囲を確かめていない
- 扱える地物数の公式の目安: 数値の記述が見つからなかった
- MapLibre 公式のニュースでの発表: 2026 年のニュース一覧と 7 月から 10 月のニュースレターに Navara の記述は見当たらなかった
