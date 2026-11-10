# Leaflet とラスタタイルからの移行

対象: Leaflet とラスタタイルの地図から、ベクトルタイルとスタイル仕様の地図への移行

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 根拠の版 | Leaflet 1.9.4 と 2.0.0-beta.2、@maplibre/maplibre-gl-leaflet 0.1.4 (npm、2026-08-16)、MapLibre GL JS 6.17.0。Leaflet と MapLibre の事実は map-compare-library の reference (2026-11-10 確認) による |

## 移行元の特徴

Leaflet はタイルとマーカーを DOM で、図形を SVG か Canvas 2D で描く 2D のライブラリで、コアにベクトルタイルとスタイル仕様の読み込みは無い ([leaflet](../../map-compare-library/references/libraries/leaflet.md))。地図の見た目はタイル提供者が描いたラスタ画像で決まり、配色を変えるには別のタイルに替えるしかない。ライブラリに縛りは少なく、縛るのはタイル提供者の規約である。

2026-11 時点で Leaflet 自体も節目にある。安定版 1.9.4 は 2023-05 以降更新が無く、2.0 は beta で ESM 化、グローバル `L` の分離、ファクトリからコンストラクタへの変更など API が大きく変わる ([leaflet](../../map-compare-library/references/libraries/leaflet.md))。Leaflet に残る場合も、いずれ 2.0 への移行の手間がかかる。

## 移行先の候補と API の対応

3 つの道がある。どれを選ぶかの目安は下の「判断の目安」に書く。

- A. Leaflet に残し、ベクトルタイルをプラグインで描く (maplibre-gl-leaflet、protomaps-leaflet)。
- B. MapLibre GL JS に乗り換える。
- C. OpenLayers に乗り換える (ol-mapbox-style でスタイルを読む)。

| 移行元の機能・API | 移行先 (ライブラリ・サービス) | 違いと注意 | 出典 |
|---|---|---|---|
| `L.tileLayer` (ラスタの XYZ) | A: maplibre-gl-leaflet で MapLibre のスタイルを 1 枚のレイヤーとして重ねる。B: MapLibre の `vector` ソースとスタイル。C: OpenLayers の `VectorTile` レイヤーと ol-mapbox-style | ラスタのままでよい層 (航空写真、地理院タイルの陰影など) は、MapLibre の `raster` ソースとしてそのまま残せる | https://github.com/maplibre/maplibre-gl-leaflet, [maplibre-gl-js](../../map-compare-library/references/libraries/maplibre-gl-js.md), [openlayers](../../map-compare-library/references/libraries/openlayers.md) |
| ベクトルタイルを Leaflet で描く | A: protomaps-leaflet (MVT と PMTiles、BSD-3-Clause) | README が保守モードと明記し、新機能を足さず、既存の Leaflet の仕組み以外では MapLibre GL JS を勧めている。スタイルは JavaScript で書き、MapLibre Style は読まない。Leaflet.VectorGrid もある (最終 push 2025-01-09) | [leaflet](../../map-compare-library/references/libraries/leaflet.md) |
| `L.marker`、`bindPopup` | B: MapLibre の `Marker` と `Popup`。A ではそのまま | A なら既存のマーカーとポップアップのコードを変えずに済むのが利点。大量の点は B で GeoJSON ソースと `circle` / `symbol` レイヤーに移すと軽くなる (推測) | https://maplibre.org/maplibre-gl-js/docs/API/classes/Marker/, https://maplibre.org/maplibre-gl-js/docs/API/classes/Popup/ |
| `L.geoJSON` (`style`、`onEachFeature`) | B: `geojson` ソースとレイヤー、属性はデータ駆動の式で塗り分ける | 関数で書いていた塗り分けを式 (`match`、`interpolate`) に書き換える。クリックの処理は `click` イベントと `features` で | [maplibre-gl-js](../../map-compare-library/references/libraries/maplibre-gl-js.md) |
| Leaflet.markercluster (MIT) | B: GeoJSON ソースの `cluster: true` | クラスタの見た目はレイヤーで描く | https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/ |
| Leaflet.heat (BSD-2-Clause) | B: `heatmap` レイヤー | | https://maplibre.org/maplibre-gl-js/docs/examples/create-a-heatmap-layer/ |
| Leaflet-Geoman、Leaflet.draw | B: Terra Draw (MapLibre のプラグイン一覧に載る) | 編集の操作感が変わる。利用者の作業手順を見て比べる | https://maplibre.org/maplibre-gl-js/docs/plugins/ |
| `L.tileLayer.wms` | B: `raster` ソースの URL に `{bbox-epsg-3857}` を入れる。C: OpenLayers の WMS ソース | WMTS 専用のソース型は MapLibre に無い | [maplibre-gl-js](../../map-compare-library/references/libraries/maplibre-gl-js.md) |
| Proj4Leaflet (EPSG:3857 以外の投影) | C: OpenLayers (proj4 で登録、再投影の例がある)。B は 6.15 から実験的に `addProjection` | 平面直角座標系などのタイルを使っているなら、OpenLayers が最も無理が少ない (推測) | [openlayers](../../map-compare-library/references/libraries/openlayers.md), [maplibre-gl-js](../../map-compare-library/references/libraries/maplibre-gl-js.md) |
| react-leaflet (Hippocratic License 2.1) | B: react-map-gl の `react-map-gl/maplibre` (MIT) | react-leaflet は OSI 非承認のライセンスで、移行のついでに外せる | [leaflet](../../map-compare-library/references/libraries/leaflet.md), https://visgl.github.io/react-map-gl/docs/get-started |

## 判断の目安

- A (Leaflet に残す) が向く: マーカー、ポップアップ、図形の既存のコードやプラグインが多く、背景の地図だけをベクトルにしたい。地図の傾きや回転が要らない。maplibre-gl-leaflet 0.1.4 の peer 依存は `leaflet ^1.9.3` で、Leaflet 2.0 への対応は書かれていない (npm の registry、2026-11-11)。A を選ぶと Leaflet 2.0 への移行が後で別に要る。また Leaflet の上に MapLibre の地図を重ねるので、両方のライブラリを読み込む。
- B (MapLibre GL JS) が向く: 配色の作り込み、大量の地物、傾き・回転、3D 建物、地形、地球儀が要る。Web とアプリで同じスタイルを使いたい (MapLibre Native)。
- C (OpenLayers) が向く: EPSG:3857 以外の投影、WMS / WMTS、GIS の機能が多い。ol-mapbox-style で MapLibre Style をどこまで同じ見た目で描けるかは確かめられていない ([openlayers](../../map-compare-library/references/libraries/openlayers.md))。
- どれを選ぶかは map-compare-library の手順で、対象端末と配布形態から決める。

## 規約上の注意

- 移行元のデータ (キャッシュ、ジオコーディングの結果、プレイス ID) を移行後も使えるか: ラスタタイルを端末やサーバーにためていたなら、その提供者の規約に従う。OpenStreetMap 財団の標準タイルは、表示していないタイルの一括取得 (オフライン保存を含む) を禁じている ([tile-openstreetmap-org](../../map-compare-infra/references/providers/tile-openstreetmap-org.md))。商用の提供者のラスタタイルは、各 provider の reference の「キャッシュ・オフライン保存」を見る。
- 移行中に移行元と移行先を併用してよいか: ラスタタイルの提供者が Google なら、Google 以外の地図との併用は禁止 ([google-maps](../../map-compare-infra/references/providers/google-maps.md))。それ以外の提供者は、各 provider の reference の「他社の地図との併用」を見る。OSM のデータどうしなら、帰属表示を両方出せば併用に規約上の問題は見当たらない (推測)。

## 費用の変化

- ラスタタイルはタイル 1 枚あたりの課金が多く、ベクトルタイルも提供者によってはタイルのリクエスト数で課金される。ベクトルタイルは 1 枚の範囲を大きいズームまで引き伸ばせる (オーバーズーム) ので枚数が減ることがあるが、減り方は確かめていない (未確認)。map-compare-infra の [criteria](../../map-compare-infra/references/criteria.md) の「費用の見積もり方」で、月の地図表示回数から並べる。
- 自前配信 (PMTiles を静的ホスティングに置く) にすると、タイルの課金が転送量とストレージに変わる ([self-hosting](../../map-compare-arch/references/self-hosting.md))。

## 移行の手順

1. 使っているタイル (URL と提供者)、プラグイン、Leaflet の版、`L.` を使う箇所を洗い出す (`grep -rn "L\.\|leaflet" src`)。
2. 上の「判断の目安」で A、B、C を決める。
3. ベクトルタイルの供給元とスタイルを map-compare-infra で決める。今のラスタタイルと似た見た目のスタイルがあるかを先に探す。
4. A なら背景のレイヤーだけを差し替え、既存のマーカーとプラグインが動くかを確かめる。B か C なら、上の表の行ごとに書き換える。
5. ズームの段階ごとに今の地図と並べて比べ、[migration-plan](migration-plan.md) の手順で切り替える。

## 既にある移行の道具

- maplibre-gl-leaflet (ISC、0.1.4): MapLibre GL JS の地図を Leaflet のレイヤーとして重ねる。もとは Mapbox 向けの mapbox-gl-leaflet で、Mapbox のライセンス変更の後に MapLibre へ移った。`getMaplibreMap()` で MapLibre の地図を取り出し、ソースやレイヤーを足せる。README は Leaflet と同期のずれを避けるため `maxBounds` と `minZoom: 1` の設定を例に入れている (https://github.com/maplibre/maplibre-gl-leaflet)。
- protomaps-leaflet (保守モード) と Leaflet.VectorGrid ([leaflet](../../map-compare-library/references/libraries/leaflet.md))。
- Leaflet 1.x から 2.0 への公式の移行の説明は、2.0 の告知とリリースノートにある ([leaflet](../../map-compare-library/references/libraries/leaflet.md))。

## 落とし穴

- ベクトルタイルの地図は、ラスタと文字の出方 (ラベルの間引き、フォント) が違う。日本語のフォント (グリフ) の配信元を決めておかないと、文字が出ない。
- MapLibre GL JS v6 は WebGL2 必須で、Leaflet が動いていた古い端末で地図が出なくなることがある。`error` イベントで検知し、代わりの表示を用意する ([maplibre-gl-js](../../map-compare-library/references/libraries/maplibre-gl-js.md))。
- A の構成では Leaflet と MapLibre の 2 つの描画が重なり、パンやズームの同期がずれる場面がある (maplibre-gl-leaflet の README が設定で避けることを勧めている)。
- タイルの提供者を替えると帰属表示も替わる ([attribution](../../map-legal-check/references/attribution.md))。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- Leaflet (BSD-2-Clause)、MapLibre GL JS (BSD-3-Clause)、maplibre-gl-leaflet (ISC)、protomaps-leaflet (BSD-3-Clause) はいずれも寛容なライセンスで、再配布の際に著作権表示が要る。
- react-leaflet は OSI 非承認の Hippocratic License 2.1 で、使い方の制限がある ([leaflet](../../map-compare-library/references/libraries/leaflet.md))。
- OpenStreetMap 由来のタイルは ODbL の帰属表示が要る ([odbl](../../map-legal-check/references/odbl.md))。

## 出典

- https://github.com/maplibre/maplibre-gl-leaflet (2026-11-11 確認。README の由来、使い方、設定の例)
- https://registry.npmjs.org/@maplibre%2fmaplibre-gl-leaflet (2026-11-11 確認。0.1.4、2026-08-16 公開、peer 依存 `leaflet ^1.9.3`、`maplibre-gl ^2.4.0 || ^3.3.1 || ^4.3.2 || ^5.0.0 || ^6.0.0`、ライセンス ISC)
- https://maplibre.org/maplibre-gl-js/docs/plugins/ (Terra Draw などのプラグイン一覧)
- https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/、https://maplibre.org/maplibre-gl-js/docs/examples/create-a-heatmap-layer/
- https://visgl.github.io/react-map-gl/docs/get-started (2026-11-11 確認)

## 未確認のこと

- maplibre-gl-leaflet の Leaflet 2.0 対応の予定。
- ラスタからベクトルに替えたときのタイルのリクエスト数の変化 (同じ操作での実測)。
- ol-mapbox-style で MapLibre Style をどこまで同じ見た目で描けるか。
