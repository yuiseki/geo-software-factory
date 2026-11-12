# d3-geo

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 3.1.2 (2026-11-03 JST)。npm の `latest` タグも 3.1.2 (https://github.com/d3/d3-geo/releases/tag/v3.1.2, https://www.npmjs.com/package/d3-geo) |
| リポジトリ | https://github.com/d3/d3-geo |
| ドキュメント | https://d3js.org/d3-geo |
| ライセンス (LICENSE ファイルで確かめる) | ISC (Copyright 2010-2026 Mike Bostock)。同じ LICENSE に、移植元の GeographicLib (1.12 以降、Charles Karney) の MIT ライセンスが併記されている (https://github.com/d3/d3-geo/blob/main/LICENSE)。npm の license 欄は ISC |
| 運営主体・ガバナンス | GitHub の d3 組織で管理され、package.json の author は Mike Bostock である (https://github.com/d3/d3-geo/blob/main/package.json)。D3 全体の一部モジュールとして配布される (https://github.com/d3/d3)。運営の規程は確かめられなかった |

## 概要

d3-geo は、球面の GeoJSON を投影法で平面に写し、SVG のパス文字列にするか Canvas に描く JavaScript モジュールである (https://d3js.org/d3-geo, https://d3js.org/d3-geo/path)。多角形の辺を大圏の弧として扱い、適応的なサンプリングで補間するので、投影後も形が崩れにくい (https://d3js.org/d3-geo)。面積、重心、距離、包含判定、経緯線などの球面計算も持つ (https://github.com/d3/d3-geo/blob/main/src/index.js)。タイルを使わずに主題図 (コロプレス図など) を描く用途が中心で、パンやズームの操作はアプリ側で作る。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): `geoPath` は context を渡さなければ SVG のパス文字列を返し、Canvas の 2D コンテキスト (`beginPath`、`moveTo`、`lineTo`、`arc`、`closePath` を持つもの) を渡せばそこに描く (https://d3js.org/d3-geo/path)。WebGL / WebGPU には描かない。
- 2D / 2.5D (傾き・回転) / 3D: 2D。投影の `rotate` で球を 3 軸 (yaw、pitch、roll) に回せるが、地図の傾き表示 (2.5D) や 3D はない (https://d3js.org/d3-geo/projection)。
- 地球儀表示: 正射図法 (`geoOrthographic`) と `rotate`、`clipAngle` の組み合わせで、地球儀に見える図を 2D で描ける (https://d3js.org/d3-geo/projection, https://github.com/d3/d3-geo/blob/main/src/index.js)。回転操作のアニメーションはアプリ側で作る。
- 対応する投影法: 本体は方位図法 (`geoAzimuthalEqualArea`、`geoAzimuthalEquidistant`、`geoGnomonic`、`geoOrthographic`、`geoStereographic`)、円錐図法 (`geoAlbers`、`geoAlbersUsa`、`geoConicConformal`、`geoConicEqualArea`、`geoConicEquidistant`)、円筒図法ほか (`geoEquirectangular`、`geoMercator`、`geoTransverseMercator`、`geoEqualEarth`、`geoNaturalEarth1`)、平面用の `geoIdentity` を持つ (https://github.com/d3/d3-geo/blob/main/src/index.js, https://d3js.org/d3-geo/projection)。さらに d3-geo-projection と d3-geo-polygon で多くの投影法を足せ、`geoProjection` で独自の投影を作れる (https://d3js.org/d3-geo/projection)。

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対象外 | d3-geo はタイルを扱わない。タイル座標を計算する別モジュール d3-tile はあるが、最新リリースは 1.0.0 (2019-07-25) で、最終 push は 2022-07-20 である (https://github.com/d3/d3-tile) |
| ベクトルタイル (MVT / PMTiles / MLT) | 対象外 | タイルを扱わない。描くのは GeoJSON に変換したデータである |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 対象外 | 見た目は SVG の属性や CSS、Canvas の描画コードで決める |
| GeoJSON | 対応 | 球面の GeoJSON が入力形式である。巻き方向 (winding order) の約束が RFC 7946 と逆である点に注意が要る (https://d3js.org/d3-geo)。TopoJSON は topojson-client で GeoJSON に変換して使う (https://d3js.org/d3-geo, https://github.com/topojson/topojson-client) |
| 3D Tiles / glTF | 対象外 | 3D 描画の仕組みがない |
| 地形 (標高タイル) | 対象外 | タイルとラスタを扱わない |
| WMS / WMTS | 対象外 | 地図サービスから画像を取得する機能がない |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: 対象外。タイルサービスを使わないため、組み合わせによる規約上の制約は生じない。背景データ (行政界など) を使う場合は、そのデータのライセンスに従う。
- API キー・アカウントの要否: 不要。

## ライセンスと費用

- ライセンス: ISC。GeographicLib 由来の部分は MIT (https://github.com/d3/d3-geo/blob/main/LICENSE)
- 利用料 (無料 / 従量 / 有料の機能): 無料
- 版によるライセンスの変化: なし (確かめた範囲では ISC のまま、https://www.npmjs.com/package/d3-geo)

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 3.1.2 で 13.7 kB。依存は d3-array の 1 つ (bundlephobia、https://bundlephobia.com/package/d3-geo@3.1.2)
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 公式に件数の目安はない。公式ドキュメントは、path 要素を分けると 1 つにまとめるより遅いが、分けたほうがスタイルと操作に使いやすいこと、Canvas は一般に SVG より速いが、スタイルと操作の実装に手間がかかることを書く (https://d3js.org/d3-geo/path)。
- 低性能端末・モバイルブラウザでの注意: 公式の記述は見当たらない。SVG で地物を多く描く場合は DOM 要素の数が負担になりうる (推測)。3.1.0 で SVG パスの座標の桁数を `path.digits` で決められるようになり、既定は 3 桁である (https://github.com/d3/d3-geo/releases/tag/v3.1.0)。

## エコシステム

- 主なプラグイン・拡張: d3-geo-projection (追加の投影法、最新リリース 4.0.0 は 2021-06-11、https://github.com/d3/d3-geo-projection)、d3-geo-polygon (https://d3js.org/d3-geo/projection)、topojson-client (https://github.com/topojson/topojson-client)。より高水準な作図ライブラリ Observable Plot (ISC) は geo マークを持ち、d3 と d3-geo-projection に依存する (https://github.com/observablehq/plot)。
- React / Vue などのラッパー: 専用の公式ラッパーはない。`geoPath` が返すパス文字列を React や Vue のテンプレートで `<path d>` に渡せば使える (推測)。
- TypeScript の型: パッケージに型は同梱されない。DefinitelyTyped の `@types/d3-geo` (最新 3.1.1) を使う (https://www.npmjs.com/package/@types/d3-geo)。
- ネイティブ版・兄弟プロジェクト: ネイティブ版はない。兄弟は D3 の他モジュール (d3-selection、d3-zoom など) で、D3 本体 (https://github.com/d3/d3) にまとめて含まれる。
- 日本語の情報 (公式翻訳、国内コミュニティ): 公式ドキュメントの日本語訳は確かめられなかった。国内コミュニティは未確認。

## 開発の活発さ

- 直近 1 年のリリース数: 1 件 (3.1.2、2026-11-03)。対象期間は 2025-11-10 から 2026-11-10。その前のリリースは 3.1.1 (2024-03-13 JST) である (https://github.com/d3/d3-geo/releases)
- 最終コミット日: 2026-11-03 (JST、main ブランチ、https://github.com/d3/d3-geo/commits/main)
- 近年の大きな破壊的変更: 3.0.0 (2021-06-06 JST) で `type: module` になり Node.js 12 以上が必要になった (https://github.com/d3/d3-geo/releases/tag/v3.0.0)。3.1.2 は個別のソースファイルでなく ES モジュールのバンドルを公開する形に変わり、package.json の `files` は `dist` のみ、`exports` は `umd` と `default` のみになった (https://github.com/d3/d3-geo/releases/tag/v3.1.2, https://github.com/d3/d3-geo/blob/main/package.json)。このため `d3-geo/src/...` のような深い import は 3.1.2 で使えなくなったと考えられる (推測)。

## 環境の違いと保守

- ブラウザ間の互換: 文書は「D3 works in any JavaScript environment」とだけ書き、ブラウザの一覧はない (https://d3js.org/getting-started)。CI は Node の上で Vitest を回すだけで、ブラウザでの自動テストはない (https://github.com/d3/d3-geo/blob/main/.github/workflows/test.yml, https://github.com/d3/d3-geo/blob/main/package.json)。d3-geo は座標の計算と SVG のパスや Canvas への描画命令の生成を受け持ち、描画はブラウザの SVG か Canvas 2D に任せるので、ブラウザ間の違いを吸収する層は持たない (推測)。
- OS 間の互換: 対応 OS と端末を述べた文書はない (未確認)。GPU を使わないので、ドライバの違いへの対応は対象外である。
- 操作の網羅: d3-geo は操作を持たない。ドラッグやズームは別のモジュール d3-zoom と d3-drag が受け持ち、文書の目次の「Interaction」に並ぶ (https://d3js.org/d3-geo)。ピンチ、慣性、キーボード、ページのスクロールとの両立は、利用者がそれらのモジュールで組む。
- エッジケースへの対応: 球面幾何の扱いについて文書が厚い。投影の既定は日付変更線での切断で (`clipAngle` が null)、`geoClipAntimeridian` が日付変更線を跨ぐ線と面を両側に切り分ける。投影は大円に沿って適応的に再標本化し、その閾値 `precision` の既定は √0.5 ピクセルである。投影できない点では `projection(point)` が null を返す (https://d3js.org/d3-geo/projection)。球面の多角形は巻き方向で内側を決め、半球より小さい外周は時計回りという約束で、GeoJSON の RFC 7946 とは逆である (https://d3js.org/d3-geo)。逆向きのデータを渡すと面が地球の残りを覆う描画になる (推測)。全文に antimeridian を含む issue は 16 件である (`repo:d3/d3-geo antimeridian`、2026-11-12)。
- 継続的な保守: CSP についての文書は未確認。worker や WebGL を使わない純粋な計算のライブラリなので、ブラウザや OS の変化に追随する必要は小さい (推測)。ブラウザ別のラベルはなく、タイトルに Safari を含む issue は 0 件である (GitHub の issue 検索、2026-11-12)。

## 向いている場面

- タイルを使わず、投影法を選んで描く静的な主題図 (コロプレス図、分布図) や、報道の図解。
- 正距方位図法や正積図法など、Web メルカトル以外の投影法が意味を持つ図。
- SVG で出力し、印刷物や記事に埋め込む図。D3 の他モジュールと組み合わせたグラフと地図の混在。

## 向いていない場面

- 背景地図 (道路、建物、地名) の上で利用者がパンやズームして場所を探す地図。
- タイル、WMS / WMTS、ベクトルタイル、地形、3D を使う地図。
- マーカー、ポップアップ、作図といった地図 UI を手早く作りたい場合 (すべて自作になる)。

## 出典

- https://d3js.org/d3-geo
- https://d3js.org/d3-geo/path
- https://d3js.org/d3-geo/projection
- https://github.com/d3/d3-geo
- https://github.com/d3/d3-geo/blob/main/LICENSE
- https://github.com/d3/d3-geo/blob/main/package.json
- https://github.com/d3/d3-geo/blob/main/src/index.js
- https://github.com/d3/d3-geo/releases
- https://github.com/d3/d3-geo/releases/tag/v3.0.0
- https://github.com/d3/d3-geo/releases/tag/v3.1.0
- https://github.com/d3/d3-geo/releases/tag/v3.1.2
- https://github.com/d3/d3-geo/commits/main
- https://www.npmjs.com/package/d3-geo
- https://www.npmjs.com/package/@types/d3-geo
- https://bundlephobia.com/package/d3-geo@3.1.2
- https://github.com/d3/d3
- https://github.com/d3/d3-tile
- https://github.com/d3/d3-geo-projection
- https://github.com/topojson/topojson-client
- https://github.com/observablehq/plot

## 未確認のこと

- D3 の運営体制 (意思決定や保守の担い手): 規程を記した文書を見つけられなかった。
- 扱える地物の数の目安と低性能端末での注意: 公式に数値や記述がなく、自分では計測しない方針のため未確認とした。
- 3.1.2 で深い import が使えなくなったかは package.json からの推測で、実際に試していない。
- React / Vue での使い方は公式の記述を確かめておらず、推測である。
- 日本語の公式訳と国内コミュニティ: 一次情報を確かめられなかった。
