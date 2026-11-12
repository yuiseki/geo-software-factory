# 大量の地物の見せ方

対象: マーカーが多すぎるときの手段 (クラスタリング、ヒートマップ、ベクトルタイル化、サーバー側の集計、六角形グリッド) と、件数ごとの目安

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 確かめた版 | MapLibre GL JS 6.17.0、MapLibre Style Spec (main、2026-11-11)、Leaflet 1.9.4 (2.0.0-beta.3 も参照)、Leaflet.markercluster (master)、@googlemaps/markerclusterer (main)、supercluster 9.1.0、tippecanoe (felt/tippecanoe main) |

## 概要

地物が増えると、点が重なって読めなくなる問題と、描画や読み込みが重くなる問題が同時に起きる。前者は見せ方 (まとめる、密度で見せる、ズームで出し分ける) で、後者は描き方 (DOM の要素をやめて地図の描画のレイヤに載せる、見えている範囲だけ読む) で解く。どちらの問題かを分けてから手段を選ぶ。件数の目安は、どのライブラリも公式には数値で示していないので、測った条件と一緒に扱う。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| 描画のレイヤに載せる (DOM のマーカーをやめる) | 要素の数による重さ | 見た目の自由度が下がる (アイコンはスプライトか画像) | MapLibre の circle、symbol レイヤ (6.17.0)。MapLibre の `Marker` は DOM 要素。Leaflet は Canvas レンダラー (1.9.4 の `preferCanvas`、既定 false。2.0.0-beta.1 で `preferCanvas` は廃止) | https://maplibre.org/maplibre-style-spec/layers/ 、https://leafletjs.com/reference-1.9.4.html 、[leaflet](../../geo-software-library/references/libraries/leaflet.md) |
| クラスタリング | 点の重なりと、点の数による重さ | 個々の点はズームするまで選べない。集計値 (合計など) は自分で定義する | MapLibre の GeoJSON ソースの `cluster` (既定 false)、`clusterRadius` (既定 50、512 でタイルの幅)、`clusterMaxZoom` (既定は maxzoom の 1 つ手前)、`clusterMinPoints` (既定 2)、`clusterProperties`。Leaflet.markercluster (MIT、「数十万のマーカー向け」と README にある、`chunkedLoading` で読み込みを分割)。@googlemaps/markerclusterer (Apache-2.0、既定のアルゴリズムは supercluster、`maxZoom` 16、`radius` 60 px) | https://github.com/maplibre/maplibre-style-spec/blob/main/src/reference/v8.json 、https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/ 、https://github.com/Leaflet/Leaflet.markercluster 、https://developers.google.com/maps/documentation/javascript/marker-clustering |
| ヒートマップ | 多数の点の分布 (密度) を見せる | 個々の点は選べない。色の濃さから値を読ませるのに向かない (推測)。ズームで見え方が変わる | MapLibre の heatmap レイヤ (`heatmap-radius`、`heatmap-weight`、`heatmap-intensity`、`heatmap-color`、`heatmap-opacity`)。Google Maps JavaScript API の HeatmapLayer は 2025-05-27 に非推奨、2026 年 5 月に使えなくなり、deck.gl の HeatmapLayer が代わりに案内されている | https://maplibre.org/maplibre-gl-js/docs/examples/create-a-heatmap-layer/ 、https://developers.google.com/maps/documentation/javascript/heatmaplayer |
| グリッドで集計 (六角形、メッシュ) | 分布を、面積がそろった区画の値として見せる | 区画の大きさで見え方が変わる (どの大きさを選んだかを書く)。区画をまたぐ境界の点の扱い | H3 (h3-js、Apache-2.0)、日本の地域メッシュ (統計と結合しやすい)、Turf の `hexGrid` (MIT) | https://github.com/uber/h3-js 、https://github.com/Turfjs/turf |
| ベクトルタイル化 | データの大きさによる読み込みの重さ。見えている範囲だけ読む | 前処理と配信の仕組みが要る。低いズームで点を間引く | tippecanoe (BSD-2-Clause) で MBTiles か PMTiles に書き出す。`-zg` で最大ズームを自動で選び、`--drop-densest-as-needed` でタイルを 500K 未満に収めるよう点の間隔を広げる | https://github.com/felt/tippecanoe 、[maplibre-gl-js](../../geo-software-library/references/libraries/maplibre-gl-js.md) |
| サーバー側で集計して返す | 端末に全件を送れない、件数が変わり続ける | 表示範囲が変わるたびに問い合わせる。キャッシュの設計 | PostGIS の集計、Martin などのタイルサーバー (置き場所は geo-software-arch) | https://maplibre.org/maplibre-gl-js/docs/guides/large-data/ |
| ズームで出し分ける | 広域で細部を出さない | どのズームで何を出すかを決める手間 | MapLibre のレイヤの `minzoom` / `maxzoom`、ソースの `maxzoom` (GeoJSON の既定 18) | https://maplibre.org/maplibre-style-spec/ |

## 判断を左右すること

- 1 件ずつ選ばせるか: 選ばせるならクラスタリングかズームでの出し分け、分布だけならヒートマップかグリッド。
- 件数の今と将来: 伸びる見込みがあれば、最初から伸びたときの件数で手段を選ぶ。
- データの大きさ: 件数より、端末に送るバイト数が効く。同じ点の数でも属性が多いと大きくなる。
- 更新の頻度: 毎分変わるデータを前処理のタイルにすると、作り直しが追いつかない。
- 点か、線と面か: クラスタリングは点だけ。線と面が重いならベクトルタイル化か簡略化。

## 件数と大きさの実測

公式の閾値は無いので、次の値は条件つきの目安として使う。

- supercluster 9.1.0 の索引を作る時間 (Node.js 23.9.0、AMD Ryzen 9 5950X、東京 23 区の範囲に一様に置いた点、`radius: 50`、`maxZoom: 16`、各 1 回): 1 万点で 29 ms、10 万点で 137 ms、100 万点で 630 ms。ズーム 11 で 23 区全体のクラスタを取り出すのはどれも 1 ms 未満 (約 240 クラスタ)。プロセスの RSS は 100 万点で 394 MB (2026-11-11 実測)。スマートフォンのブラウザでは数倍遅いと考えられる (推測。端末では測っていない)。
- 点の GeoJSON の大きさ (座標を小数 6 桁、属性は数値の `id` と短い日本語の `name`): 1 万点で 1.29 MB、gzip で 0.14 MB。10 万点で 13.06 MB、gzip で 1.44 MB (2026-11-11 実測)。
- MapLibre の大きなデータの手引きは、件数の閾値を示さず、不要な属性の削除、座標の精度を下げる、簡略化、分割、点ソースの `maxzoom` を下げる、クラスタリング、ベクトルタイル化を勧める (https://maplibre.org/maplibre-gl-js/docs/guides/large-data/ 、確かめた日 2026-11-11)。
- Leaflet の FAQ は、数千のマーカーには Leaflet.markercluster、数千点のベクターには Canvas レンダラーを勧める ([leaflet](../../geo-software-library/references/libraries/leaflet.md))。
- Google の marker clustering の文書は、件数の目安を示していない (https://developers.google.com/maps/documentation/javascript/marker-clustering 、確かめた日 2026-11-11)。
- 東京 23 区のセブン-イレブン (OSM で 1,944 件) は、店舗の点ではなく区ごとの集計 (コロプレス) で見せた ([seven-eleven-tokyo23](../../../../examples/seven-eleven-tokyo23/README.md))。

## 手順

1. 1 件ずつ選ばせるか、分布を見せるかを決める。
2. 今の件数と伸びたときの件数、GeoJSON にしたときのバイト数を見積もる (上の実測を目安にする)。
3. 点で、1 件ずつ選ばせ、数 MB 以内ならクラスタリング。クラスタを押したら、そのクラスタが開くズームまで寄る (MapLibre の `getClusterExpansionZoom`)。
4. 分布を見せるならヒートマップかグリッド。値を比べさせるならグリッドで集計し、凡例をつける。
5. 数 MB を超える、線や面が細かい、全球のデータなら、ベクトルタイルにする。置き場所と配信は geo-software-arch で決める。
6. 端末で測る。結論が件数に左右されるなら、geo-software-poc-measure で想定の端末と件数で測る値 (描画のフレーム時間、初回の読み込みのバイト数) を決める。

## 落とし穴

- クラスタの数字だけでは中身が分からない。分類の違う地物を 1 つのクラスタにまとめると、何が多いのか読めない。分類ごとにソースを分けるか、`clusterProperties` で分類ごとの件数を持たせる。
- 同じ座標の点 (同じ建物のテナントなど) は、どこまでズームしても開かない。`clusterMaxZoom` より上では重なったまま残るので、一覧で出す。
- ヒートマップの色は、点の数と `heatmap-weight` と半径の掛け合わせで、ズームで変わる。「赤いところが危険」のような読みを誘う用途では、グリッドで集計して数を出す (推測)。
- 件数をコロプレスで見せると、面積の大きい区画が目立つ。率か密度に直す ([cartography](cartography.md))。
- Google Maps JavaScript API の HeatmapLayer は 2026 年 5 月に使えなくなった。古い記事の手順をそのまま使わない。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- ここに挙げた道具はどれも寛容なライセンスで、組み込み、改変、配布、SaaS 提供で著作権表示とライセンス文の同梱 (Apache-2.0 は加えて NOTICE と変更の表示) を求めるだけである: supercluster (ISC)、Leaflet.markercluster (MIT)、@googlemaps/markerclusterer (Apache-2.0)、h3-js (Apache-2.0)、Turf (MIT)、tippecanoe (BSD-2-Clause) (各リポジトリの LICENSE、GitHub API で 2026-11-11 に確かめた)。
- データの方の条件は別に効く。OSM (ODbL) の点を集計して出した値やタイルは、派生データベースか生成された著作物かで義務が変わる (geo-software-data の [license-mixing](../../geo-software-data/references/license-mixing.md)、geo-software-legal-check の [odbl](../../geo-software-legal-check/references/odbl.md))。

## 出典

- https://github.com/maplibre/maplibre-style-spec/blob/main/src/reference/v8.json (GeoJSON ソースの `cluster` 系の既定値と説明、heatmap レイヤの属性。2026-11-11)
- https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/ 、https://maplibre.org/maplibre-gl-js/docs/examples/create-a-heatmap-layer/ (例の所在。2026-11-11)
- https://maplibre.org/maplibre-gl-js/docs/guides/large-data/ (大きなデータの手引き。geo-software-library の reference から)
- https://github.com/Leaflet/Leaflet.markercluster (README の対象件数の記述、`chunkedLoading`、`removeOutsideVisibleBounds`、MIT。2026-11-11)
- https://github.com/googlemaps/js-markerclusterer と https://developers.google.com/maps/documentation/javascript/marker-clustering (既定のアルゴリズムと既定値。2026-11-11)
- https://developers.google.com/maps/documentation/javascript/heatmaplayer (HeatmapLayer の非推奨と提供終了。2026-11-11)
- https://github.com/mapbox/supercluster (ISC、README。実測は npm の 9.1.0)
- https://github.com/felt/tippecanoe (README の `-zg`、`--drop-densest-as-needed` と 500K の上限。2026-11-11)
- https://leafletjs.com/reference-1.9.4.html (`preferCanvas` の既定値。2026-11-11)

## 未確認のこと

- MapLibre GL JS 6.17.0 のクラスタリングが内部でどの実装 (supercluster か、@maplibre/geojson-vt に入ったものか) を使っているか。ワーカーのソースは `@maplibre/geojson-vt` を読み込んでいたが、クラスタの処理の場所までは追っていない。
- スマートフォンの実機で、クラスタリングや描画のレイヤが何件まで滑らかに動くか。測っていない。
- Leaflet 2.0 で Canvas レンダラーをどう選ぶか (`preferCanvas` の代わり)。MIGRATION.md を読んでいない。
