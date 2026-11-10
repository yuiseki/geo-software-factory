# OGC API

対象: OGC API - Features、Tiles、Maps、Processes、EDR (と、関係する Common、CQL2、Tile Matrix Set)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 仕様と標準化団体、版 | Open Geospatial Consortium (OGC)。部品ごとの版と承認日は下の「部品ごとの状態」の表 |

## 概要

OGC API は、WMS や WFS の後を継ぐ、OpenAPI で記述する REST 風の地理空間 API の標準群である。ランディングページ、適合宣言 (`/conformance`)、コレクション (`/collections/{id}`) という共通の骨格の上に、地物 (Features)、タイル (Tiles)、地図画像 (Maps)、処理 (Processes)、環境データの取り出し (EDR) を部品として載せる。JSON と GeoJSON を基本にし、HTML でも返せるので、ブラウザから直接読みやすい。部品ごとに承認の段階が違い、書き込み (Features Part 4) や Processes の Part 2 以降はまだ承認されていない。

## 部品ごとの状態

| 部品 | 版と状態 | 承認日 | 出典 (2026-11-11) |
|---|---|---|---|
| Features Part 1: Core | 1.0.1 (17-069r4、正誤訂正)、承認済み | 2022-04-05 (1.0.1) | https://docs.ogc.org/is/17-069r4/17-069r4.html |
| Features Part 2: CRS by Reference | 1.0.1 (18-058r1)、承認済み | 2022-04-05 | https://docs.ogc.org/is/18-058r1/18-058r1.html |
| Features Part 3: Filtering | 1.0 (19-079r2)、承認済み | 2024-05-23 | https://docs.ogc.org/is/19-079r2/19-079r2.html |
| CQL2 (絞り込みの言語) | 1.0.0 (21-065r2)、承認済み | 2024-05-23 | https://docs.ogc.org/is/21-065r2/21-065r2.html |
| Features Part 4: Create, Replace, Update and Delete | 草案 (20-002r2)。意見募集を終え、承認の手続きの準備中 | 未承認 | https://github.com/opengeospatial/ogcapi-features (README) |
| Features Part 5 / Common Part 3: Schemas | 1.0.0 (23-058r2)、承認済み | 2026-04-30 | https://docs.ogc.org/is/23-058r2/23-058r2.html |
| Features Part 6: Property Selection | 初期の草案 (24-019) | 未承認 | https://github.com/opengeospatial/ogcapi-features (README) |
| Tiles Part 1: Core | 1.0 (20-057)、承認済み。Tile Matrix Set 2.0 (17-083r4、2022-02-20 承認) に拠る | 2022-08-26 | https://docs.ogc.org/is/20-057/20-057.html 、 https://docs.ogc.org/is/17-083r4/17-083r4.html |
| Maps Part 1: Core | 1.0 (20-058)、承認済み。WMS の GetFeatureInfo に当たるものは持たない | 2024-06-12 | https://docs.ogc.org/is/20-058/20-058.html 、 https://github.com/opengeospatial/ogcapi-maps (README) |
| Processes Part 1: Core | 1.0.0 (18-062r2)、承認済み。2.0 は編集者の草案 (18-062r3) | 2021-08-23 | https://docs.ogc.org/is/18-062r2/18-062r2.html 、 https://github.com/opengeospatial/ogcapi-processes (README) |
| Processes Part 2〜5 (配備、ワークフロー、ジョブ管理、来歴) | 草案 (20-044、21-009、24-051、26-038) | 未承認 | https://github.com/opengeospatial/ogcapi-processes (README) |
| EDR Part 1 | 1.2 (19-086r9)、承認済み。1.0、1.0.1、1.1 もある | 2026-04-30 (1.2) | https://docs.ogc.org/is/19-086r9/19-086r9.html 、 https://www.ogc.org/standards/ogcapi-edr/ |
| EDR Part 2: Publish-Subscribe Workflow | 1.0 (23-057r1)、承認済み | 2024-05-07 | https://docs.ogc.org/is/23-057r1/23-057r1.html |

ほかに Records Part 1、Connected Systems Part 1 と 2、Moving Features、DGGS Part 1 も OGC の一覧で承認済みとされる。Coverages、Styles、Routes は一覧に状態の表示が無い (https://ogcapi.ogc.org/ 、2026-11-11)。

## 通信の形

- 向き: 利用者が取りに行く。EDR Part 2 は発行と購読の流れ (MQTT などの通知) を定める。
- 何を運ぶか: Features は地物 (GeoJSON が基本)。Tiles はベクタータイル、地図画像のタイル、カバレッジのタイル。Maps は地図画像。Processes は処理の実行とジョブ。EDR は位置、範囲、軌跡を指定した観測値や予報値。
- 下にある通信: HTTP。

## 対応状況

| 環境 | 対応 | 備考 | 出典 |
|---|---|---|---|
| ブラウザ | 対応 (普通の `fetch`) | JSON と GeoJSON で返るので、専用の解析器は要らない。他のオリジンから読むならサーバー側で CORS を許す | 仕様の形からの判断 |
| ネイティブアプリ | 対応 (HTTP) | QGIS などのデスクトップ GIS が読む (QGIS の対応版は未確認) | 未確認 |
| エッジ関数・サーバーレス (接続の維持) | 対応 | 接続を保たないので、関数や CDN の前段に置ける。Features の結果を CDN でキャッシュできる (推測) | 推測 |
| 地図ライブラリ | 一部 | OpenLayers 10.11.0 は `ol/source/OGCVectorTile` と `ol/source/OGCMapTile` (Tiles) と `ol/source/OGCMap` (Maps の単一画像) を持つ。MapLibre GL JS と Leaflet に専用のソースは無い。Tiles の URL テンプレート (`/collections/{id}/tiles/WebMercatorQuad/{z}/{y}/{x}`、行と列の順に注意) を MapLibre の `vector` や `raster` ソースに書けば読める (推測)。Features の `/items?f=json` を GeoJSON ソースの URL にすれば 1 ページ目は描けるが、`next` のリンクをたどる処理は自分で書く (推測)。CesiumJS の OGC API への対応は未確認 | `gh api repos/openlayers/openlayers/contents/src/ol/source/OGCMapTile.js?ref=v10.11.0` ほか (2026-11-11)、map-compare-library の [maplibre-gl-js](../../../map-compare-library/references/libraries/maplibre-gl-js.md)、[openlayers](../../../map-compare-library/references/libraries/openlayers.md) |

## 実装

| 実装 (OSS / 管理型サービス) | 版 | ライセンス・料金の単位 | 出典 |
|---|---|---|---|
| pygeoapi | 0.24.0 (2026-07-28) | MIT。OSGeo のプロジェクト。Features 1.0、EDR 1.0.1、Tiles 1.0、Processes 1.0 の OGC 参照実装 | `gh api repos/geopython/pygeoapi/license` 、 https://pygeoapi.io/ (2026-11-11) |
| ldproxy | v4.8.2 (2026-10-07) | MPL-2.0。Features Part 1 と Part 2 の OGC 参照実装。Tiles、Styles、Routes、3D Tiles の部品も持つ (各部品の適合の状態は未確認) | `gh api repos/interactive-instruments/ldproxy/license` 、 https://docs.ldproxy.net/ (2026-11-11) |
| GeoServer | 3.0.2 (2026-10-17) | GPL-2.0-or-later (EMF、XSD、OSHI との結合の例外付き)。Features はサービスの本体に入っている。Tiles、Maps、Coverages、Processes、Styles はコミュニティモジュール (公式の保守の対象外) | `gh api repos/geoserver/geoserver/license` 、 https://docs.geoserver.org/latest/en/user/services/features/index.html (2026-11-11) |
| MapServer | 8.6.6 (2026-09-06) | MIT 型 (MapServer のライセンス)。8.0 で初めて OGC API に対応 (RFC 134)、のちに Features Part 2 を実装 | `gh api repos/MapServer/MapServer/license` 、 https://github.com/MapServer/MapServer/blob/main/HISTORY.md (2026-11-11) |
| 製品の一覧 | (OGC) | OGC が実装製品と適合製品のデータベースを公開している | https://github.com/opengeospatial/ogcapi-features (README の products へのリンク) |

## 地図プロダクトでの使いどころ

- 公共案件で「標準の API で地物を出してほしい」と求められたとき、WFS の代わりに Features を出す。OGC も WFS より Features を勧めている ([ogc-classic](ogc-classic.md))。
- 既存の PostGIS の表を、書かずに API として公開したいとき (pygeoapi、ldproxy、GeoServer の設定だけで出せる)。
- 観測値や予報を位置や範囲で切り出す API が要るとき (EDR)。

## 規模と費用

- 実装はどれも常駐のサーバーで、費用はサーバーの台数と DB の負荷で決まる (推測)。
- Features のページ送りは `limit` と `next` のリンクで行う。全件を一度に取る使い方は向かないので、件数の多い地物を地図に全部出すならベクタータイル (Tiles) か PMTiles を併用する (推測)。

## 落とし穴

- 「OGC API 対応」とだけ書かれた製品は、どの部品のどの適合クラスに対応しているかが分からない。`/conformance` の一覧で確かめる。
- Tiles の URL は `{tileMatrix}/{tileRow}/{tileCol}` の順で、XYZ の `{z}/{x}/{y}` と行と列が入れ替わる。
- 書き込み (Part 4) は承認前で、実装ごとに対応が違う。編集の API を OGC API で標準化したいなら、草案に従うことを答えに書く。
- GeoServer の Tiles や Maps はコミュニティモジュールで、版を上げたときに使えなくなりうる (推測)。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- GeoServer (GPL-2.0-or-later): 改変せずに、または改変して自社のサーバーで動かし、ネットワーク越しに使わせるだけなら、GPL にはネットワーク越しの利用でソースを出す条項が無いので、ソースの提供義務は生じない (条文からの読み、AGPL との違い)。GeoServer を受託で納品する、機器やパッケージに入れて配布するなら、配布物について GPL の条件 (ソースの提供、同じライセンス) がかかる。GeoServer に自社の拡張を組み込んで配布すると、拡張も GPL の対象になりうる (推測)。
- ldproxy (MPL-2.0): ファイル単位のコピーレフト。ldproxy のファイルを改変して配布するなら、そのファイルのソースを MPL-2.0 で出す。別のファイルに書いた自社のコードには及ばない。SaaS 提供だけなら配布に当たらない (条文からの読み)。
- pygeoapi (MIT)、MapServer (MIT 型) は、著作権表示の保持で足りる。
- 配る地物のデータの継承条件 (OSM 由来なら ODbL) は別に効く。

## 出典

- https://ogcapi.ogc.org/ : OGC API の一覧と承認の表示。
- https://www.ogc.org/standards/ogcapi-features/ 、 https://www.ogc.org/standards/ogcapi-tiles/ 、 https://www.ogc.org/standards/ogcapi-maps/ 、 https://www.ogc.org/standards/ogcapi-processes/ 、 https://www.ogc.org/standards/ogcapi-edr/ : 版と文書番号。
- 上の表の docs.ogc.org の各文書 : 承認日と版。
- https://github.com/opengeospatial/ogcapi-features 、 https://github.com/opengeospatial/ogcapi-processes 、 https://github.com/opengeospatial/ogcapi-maps 、 https://github.com/opengeospatial/ogcapi-tiles : 草案の状態、Maps の GetFeatureInfo、Tiles と TMS 2.0。
- `gh api repos/<owner>/<repo>/license` と releases (geopython/pygeoapi、interactive-instruments/ldproxy、geoserver/geoserver、MapServer/MapServer) : ライセンスと版。
- https://pygeoapi.io/ 、 https://docs.ldproxy.net/ 、 https://docs.geoserver.org/latest/en/user/services/features/index.html : 対応する部品。
- OpenLayers のソース (`src/ol/source/OGCMapTile.js`、`OGCVectorTile.js`、`OGCMap.js`、タグ v10.11.0) : ライブラリの対応。

## 未確認のこと

- 国内の公的機関が OGC API を公開している例 (見つけられなかった)。
- CesiumJS、QGIS、ArcGIS の OGC API への対応の範囲と版。
- ldproxy の Tiles、Styles などの部品の OGC 適合の状態。
- MapServer が Features Part 2 を実装した版 (HISTORY.md では 8.0.1 より後)。
- GeoServer で Features が拡張から本体に移った版。
