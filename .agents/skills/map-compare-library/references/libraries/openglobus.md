# OpenGlobus

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 0.28.7 (2026-03-05、npm の `latest`)。1.0.0 の候補版 1.0.0-rc41 (2026-11-06) が npm の `next` タグで出ている (https://www.npmjs.com/package/@openglobus/og 、https://github.com/openglobus/openglobus/releases) |
| リポジトリ | https://github.com/openglobus/openglobus |
| ドキュメント | https://openglobus.github.io/docs/ (API)、https://github.com/openglobus/openglobus/wiki 、https://sandbox.openglobus.org (例) |
| ライセンス (LICENSE ファイルで確かめる) | 版で異なる。master と 1.0.0-rc 系は Apache-2.0 (LICENSE.md、npm の `license` も Apache-2.0)。安定版 v0.28.7 のタグの LICENSE.md は MIT で、npm の `license` も MIT |
| 運営主体・ガバナンス | 個人主導。LICENSE.md の著作権者は Michael Gevlich で、コミット数の大半 (4,493 件) が同氏のアカウント Zemledelec による (https://github.com/openglobus/openglobus/graphs/contributors)。寄付は Open Collective で受けている (https://opencollective.com/openglobusjs) |

## 概要

OpenGlobus は TypeScript/JavaScript で書かれた、3D 地図と地理空間データを表示するライブラリである (https://github.com/openglobus/openglobus)。README は、高解像度の地形、画像レイヤー、数千の 3D オブジェクトの描画、計測ツールなどを備えるとしている。CesiumJS と同じく地球儀型のエンジンだが、3D Tiles とベクトルタイルには対応していない (下記)。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): WebGL 2 (`src/webgl/Handler.ts` が `webgl2` コンテキストを取る)。WebGPU の実装は見当たらない
- 2D / 2.5D (傾き・回転) / 3D: 3D。正射影カメラへの切り替え (`OrthoSwitcher`) と、地表付近での自由移動の操作部品がある (`src/control/`)
- 地球儀表示: 対応
- 対応する投影法: EPSG:3857 と EPSG:4326 のタイル、proj4 による任意の投影定義を持つ (`src/proj/`)。平面の 2D 地図モードは未確認

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | `XYZ`、`OpenStreetMap`、`Bing` レイヤー (`src/layer/`)。GeoTIFF/COG の `GeoTIFFLayer` もある |
| ベクトルタイル (MVT / PMTiles / MLT) | 非対応 (開発中) | MVT 対応の Issue #850 が open、PR #1147 「Feature/mvt layer」は draft (2026-10-28 作成、https://github.com/openglobus/openglobus/pull/1147)。PMTiles、MLT の実装は見当たらない |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 非対応 | ベクトルタイル自体が未対応。Style 仕様を読む実装は見当たらない |
| GeoJSON | 部分対応 | `Geometry.setGeometry` が GeoJSON 形式のジオメトリを受け取る (`src/entity/geometry/Geometry.ts`)。FeatureCollection を読み込む専用のローダーは src に見当たらない。KML は `KML` レイヤーで読む |
| 3D Tiles / glTF | glTF は対応、3D Tiles は非対応 | glTF/GLB のパーサ (`src/utils/gltf/`) がある。3D Tiles の実装は src に見当たらない |
| 地形 (標高タイル) | 対応 | RGB 標高タイル (`RgbTerrain`、`MapterhornTerrain`)、独自形式の `GlobusTerrain`、BIL、GeoTIFF (`src/terrain/`)。既定は地形なし (`EmptyTerrain`) |
| WMS / WMTS | WMS は対応、WMTS は専用クラスなし | `WMS` レイヤーがある。WMTS は XYZ 形式の URL で取れる場合に限り `XYZ` で読めると考えられる (推測) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: `OpenStreetMap` レイヤーの既定 URL は `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png` であり、OSMF のタイル利用ポリシーに従う必要がある (https://operations.osmfoundation.org/policies/tiles/)。`Bing` レイヤーは API キーなしで `ecn.{s}.tiles.virtualearth.net` のタイルを直接読む実装であり、Bing Maps の利用規約上この使い方が許されるかは未確認 (`src/layer/Bing.ts`)。既定の地形サービスは openglobus.org のサーバー (`terrain.openglobus.org`、`srtm3.openglobus.org`) を指す
- API キー・アカウントの要否: ライブラリ自体は不要。Cesium ion のような専用の有料サービスへの依存は無い

## ライセンスと費用

- ライセンス: 1.0.0-rc 系と master は Apache-2.0、0.28.x までの安定版は MIT
- 利用料 (無料 / 従量 / 有料の機能): 無料。README は「completely free」としている。有料プランは見当たらない
- 版によるライセンスの変化: あり。v0.28.7 のタグは MIT、master は 2025-02-24 の LICENSE.md 更新以降 Apache-2.0 (https://github.com/openglobus/openglobus/commits/master/LICENSE.md)。1.0.0 正式版は Apache-2.0 になると見込まれる (推測)

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 約 226 KB (@openglobus/og 0.28.7、min 約 973 KB)、約 673 KB (1.0.0-rc41、min 約 2.41 MB)。いずれも bundlephobia API の値、2026-11-10 取得 (https://bundlephobia.com/package/@openglobus/og@0.28.7)
- 扱える地物の数の目安 (公式の記述か、測った条件つき): README は「renders thousands of 3D objects」とするのみで、具体的な条件つきの数値は未確認
- 低性能端末・モバイルブラウザでの注意: WebGL 2 が必須。タッチ操作の部品 (`TouchNavigation`) はある。モバイルでの性能の公式の記述は未確認

## エコシステム

- 主なプラグイン・拡張: 組み込みのコントロール群 (計測、レイヤー切り替え、エンティティの移動・回転ギズモ、Projector など)。外部プラグインの一覧は未確認
- React / Vue などのラッパー: openglobus-react (`@openglobus/openglobus-react` 1.0.1、MIT、peer は `@openglobus/og` 1.0.0-rc15。https://github.com/openglobus/openglobus-react)。テンプレート生成の `create-openglobus` もある
- TypeScript の型: 同梱 (TypeScript で書かれ、npm の `types` は `lib/index.d.ts`)
- ネイティブ版・兄弟プロジェクト: なし (見当たらない)
- 日本語の情報 (公式翻訳、国内コミュニティ): 見当たらない

## 開発の活発さ

- 直近 1 年のリリース数: npm に 49 版 (2025-11-10 から 2026-11-10。安定版 12 版 (0.27.21 から 0.28.7) と 1.0.0-rc 37 版)。GitHub Releases も 49 件
- 最終コミット日: 2026-11-06 (master)
- 近年の大きな破壊的変更: 1.0.0-rc 系で多数の変更が続いている。CHANGELOG の Unreleased には `Projector` の `sourceType` 引数の削除などがある (https://github.com/openglobus/openglobus/blob/master/CHANGELOG.md)。0.28 から 1.0 への移行ガイドは未確認

## 環境の違いと保守

- ブラウザ間の互換: 対応ブラウザを示した公式文書は未確認。CI のテストは Vitest を jsdom の環境で回し、シェーダーは模擬に差し替える (https://github.com/openglobus/openglobus/blob/master/.github/workflows/push.yml, https://github.com/openglobus/openglobus/blob/master/vitest.config.ts)。実際のブラウザでの自動テストは CI 設定に見当たらない。
- OS 間の互換: 対応 OS と端末、GPU の違い、メモリ上限への対応を述べた文書は未確認。公開の CI は Ubuntu だけである (同 push.yml)。
- 操作の網羅: 操作の部品として、マウスの `Navigation`、`KeyboardNavigation`、`TouchNavigation`、簡易版の `SimpleNavigation` と `SimpleTouchNavigation`、地表付近を自由に動く `FreeNavigation` を持つ (https://github.com/openglobus/openglobus/tree/master/src/control)。ペン入力、慣性、ページのスクロールと両立させる設定は未確認。
- エッジケースへの対応: README は「Precision at all scales」をうたうが (https://github.com/openglobus/openglobus/blob/master/README.md)、精度を保つ仕組みを説明した文書は未確認。コード検索で `webglcontextlost` は 0 件で (`repo:openglobus/openglobus webglcontextlost`、2026-11-12)、コンテキスト喪失の扱いは未確認。日付変更線と極、読み込み失敗の扱いも未確認。
- 継続的な保守: CSP についての公式文書は未確認。CHANGELOG は短く、ブラウザ固有の修正は見当たらない (https://github.com/openglobus/openglobus/blob/master/CHANGELOG.md)。ブラウザ別のラベルはなく、タイトルに Safari、Firefox、iOS を含む issue はそれぞれ 1 件である (GitHub の issue 検索、`repo:openglobus/openglobus` に各条件を付けて、2026-11-12)。

## 向いている場面

- Cesium ion などの外部サービスに頼らず、地球儀上にラスタ画像・地形・glTF モデル・エンティティを表示したい場合
- CesiumJS より小さいバンドルで地球儀を使いたい場合

## 向いていない場面

- 3D Tiles (PLATEAU の 3D 都市モデルなど) を表示したい場合
- MVT や MapLibre Style のベクトルタイル地図を表示したい場合
- 組織的な保守体制を重視する場合 (開発が 1 人に集中している)

## 出典

- https://github.com/openglobus/openglobus
- https://github.com/openglobus/openglobus/releases
- https://github.com/openglobus/openglobus/blob/master/LICENSE.md
- https://github.com/openglobus/openglobus/blob/v0.28.7/LICENSE.md
- https://github.com/openglobus/openglobus/commits/master/LICENSE.md
- https://github.com/openglobus/openglobus/blob/master/CHANGELOG.md
- https://github.com/openglobus/openglobus/graphs/contributors
- https://github.com/openglobus/openglobus/issues/850
- https://github.com/openglobus/openglobus/pull/1147
- https://github.com/openglobus/openglobus/blob/master/src/layer/Bing.ts
- https://github.com/openglobus/openglobus/blob/master/src/layer/OpenStreetMap.ts
- https://github.com/openglobus/openglobus/blob/master/src/webgl/Handler.ts
- https://github.com/openglobus/openglobus/tree/master/src/terrain
- https://github.com/openglobus/openglobus/tree/master/src/proj
- https://github.com/openglobus/openglobus/wiki
- https://openglobus.github.io/docs/
- https://sandbox.openglobus.org
- https://www.openglobus.org/
- https://www.npmjs.com/package/@openglobus/og
- https://opencollective.com/openglobusjs
- https://github.com/openglobus/openglobus-react
- https://bundlephobia.com/package/@openglobus/og@0.28.7
- https://operations.osmfoundation.org/policies/tiles/

## 未確認のこと

- 平面の 2D 地図モードの有無: ソースの構成からは判断できず、ドキュメントでも確かめられなかった
- WMTS の扱い: 専用クラスが無いことだけを確かめた。XYZ で読めるかは推測
- Bing レイヤーの規約上の可否: Bing Maps の規約を照合していない
- 扱える地物数とモバイル性能の公式の目安: 公式サイト (openglobus.org) の本文を取得できず、README にも数値が無かった
- 0.28 から 1.0 への移行ガイドの有無: 見つからなかった
