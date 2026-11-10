# WMS、WMTS、WFS

対象: OGC Web Map Service (WMS)、Web Map Tile Service (WMTS)、Web Feature Service (WFS)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 仕様と標準化団体、版 | OGC。WMS 1.3.0 (06-042、ISO 19128 と同じ文書)。WMTS 1.0.0 (07-057r7)。WFS 2.0.2 (09-025r2、正誤訂正付き。2.0 は ISO 19142)。古い版として WMS 1.1.1、WFS 1.1.0 と 1.0.0 も一覧にある (https://www.ogc.org/standards/wms/ 、 https://www.ogc.org/standards/wmts/ 、 https://www.ogc.org/standards/wfs/ 、2026-11-11) |

## 概要

2000 年代に作られた、`SERVICE=WMS&REQUEST=GetMap` のようなクエリ文字列で呼ぶ地理空間サービスの標準である。WMS は範囲と大きさを指定して地図画像を 1 枚作らせ、WMTS は決まったタイルの格子で切った画像を返し、WFS は地物を GML などで返す。どれも能力を XML の Capabilities 文書で宣言する。公共の GIS では今も広く使われており、OGC は WFS について、今も信頼できる手段としつつ、新しい実装には OGC API - Features を勧めている ([ogc-api](ogc-api.md))。

## 通信の形

- 向き: 利用者が取りに行く。
- 何を運ぶか: WMS と WMTS は地図画像 (PNG、JPEG)。WMS の GetFeatureInfo はクリックした場所の属性。WFS は地物 (GML が基本。実装によって GeoJSON も返す)。WFS-T は書き込み (Transaction)。
- 下にある通信: HTTP (GET の KVP、POST の XML。WMTS は REST 形式の URL テンプレートも定める)。

## 対応状況

| 環境 | 対応 | 備考 | 出典 |
|---|---|---|---|
| ブラウザ | 対応 (画像と XML) | 画像はそのまま表示できる。Capabilities と GML の解析はライブラリに任せる。他のオリジンの画像を WebGL のテクスチャにするには CORS が要る (推測) | 推測 |
| ネイティブアプリ | 対応 | QGIS、ArcGIS などのデスクトップ GIS は昔から読む。.NET の Mapsui は WMS、WFS、WMTS を読む ([mapsui](../../../map-compare-library/references/native/mapsui.md)) | map-compare-library |
| エッジ関数・サーバーレス (接続の維持) | 前段のキャッシュに向く | WMTS のタイルは URL が決まるので CDN でキャッシュしやすい。WMS の GetMap は範囲が自由なので、タイル状の範囲に揃えないとキャッシュが効かない (推測) | 推測 |
| 地図ライブラリ | 広く対応 | OpenLayers は WMS (タイル、単一画像) と WMTS を標準で持ち、Capabilities からレイヤーを作れる。WFS は `ol/format/WFS` で読み書きの要求を組める。Leaflet は WMS をコアに持つが WMTS 専用クラスは無い。MapLibre GL JS は raster ソースの URL に `{bbox-epsg-3857}` を入れて WMS を読み、WMTS 専用のソースは無い。CesiumJS は WMS と WMTS のプロバイダを持つ | [openlayers](../../../map-compare-library/references/libraries/openlayers.md)、[leaflet](../../../map-compare-library/references/libraries/leaflet.md)、[maplibre-gl-js](../../../map-compare-library/references/libraries/maplibre-gl-js.md)、[cesiumjs](../../../map-compare-library/references/libraries/cesiumjs.md)、`gh api repos/openlayers/openlayers/contents/src/ol/format/WFS.js?ref=v10.11.0` (2026-11-11) |

## 実装

| 実装 (OSS / 管理型サービス) | 版 | ライセンス・料金の単位 | 出典 |
|---|---|---|---|
| GeoServer | 3.0.2 (2026-10-17) | GPL-2.0-or-later (結合の例外付き)。WMS、WMTS (GeoWebCache)、WFS、WCS | `gh api repos/geoserver/geoserver/license` (2026-11-11) |
| MapServer | 8.6.6 (2026-09-06) | MIT 型 | `gh api repos/MapServer/MapServer/license` (2026-11-11) |
| QGIS Server | 3.44.15 (QGIS、2026-09-25) | GPL-2.0 (GitHub の判定。QGIS 全体のライセンス) | `gh api repos/qgis/QGIS/license` (2026-11-11) |
| MapProxy | 8.1.0 (2026-11-05) | Apache-2.0。WMS や XYZ をキャッシュして WMS、WMTS、TMS で出し直す | `gh api repos/mapproxy/mapproxy/license` (2026-11-11) |
| deegree | 3.6.14 (2026-11-03) | LGPL-2.1 | `gh api repos/deegree/deegree3/license` (2026-11-11) |
| OWSLib (Python の利用者側) | 0.36.0 (2026-06-04) | BSD-3-Clause | `gh api repos/geopython/OWSLib/license` (2026-11-11) |

## 地図プロダクトでの使いどころ

- 公共案件や既存の GIS と「WMS で配信してほしい」「WMS を重ねたい」と求められたとき。発注者の GIS が WMS や WFS しか読めないことがある。
- 公的機関が WMS で出している主題図を重ねるとき。例: 防災科学技術研究所の J-SHIS は地すべり地形分布図を WMS 1.3.0 で出しており (GetCapabilities を 2026-11-11 に取得、MapServer の名前空間を含む)、版 1.1.1 と 1.3.0、操作 GetCapabilities、GetMap、GetLegendGraphic、GetFeatureInfo に対応すると案内している (https://www.j-shis.bosai.go.jp/en/wms-landslide 、2026-11-11)。
- 新しく作る Web 地図の配信には、ベクタータイル (PMTiles、OGC API - Tiles) や XYZ を選び、WMS は求められたときに並べて出すほうが扱いやすい (推測)。

## 規模と費用

- WMS の GetMap は要求ごとにサーバーで画像を描くので、利用者が増えると CPU を使う。WMTS や MapProxy のようにタイルに切ってキャッシュすると、負荷が CDN に移る (推測)。
- WFS で地物を全件返すと重い。`count` (2.0) で件数を絞り、範囲で切る。

## 落とし穴

- WMS 1.3.0 は EPSG:4326 の軸の順を緯度、経度とする。1.1.1 は経度、緯度。版を変えると BBOX がずれる (WMS 1.3.0 の仕様の一般に知られた性質。この reference では条文を引いていない)。
- MapLibre GL JS は Web メルカトル (EPSG:3857) でしか WMS を描けない。日本の平面直角座標系だけを出す WMS は重ねられない (推測)。
- WMTS の格子が Web メルカトルでないと、XYZ のライブラリでは読めない。
- 多くの公共 WMS は HTTP のままか、CORS を許していない。ブラウザから読めるかを先に確かめる (推測)。
- 国土地理院の地理院タイルは XYZ 形式で配られる。WMTS の Capabilities を作る道具は公開されているが (https://gsi-cyberjapan.github.io/experimental_wmts/ 、ページの題は「WMTSメタデータ作成ツール」)、国土地理院が WMTS を公式に配信しているかは未確認。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- GeoServer、QGIS Server (GPL): 自社のサーバーで動かしてネットワーク越しに使わせるだけなら、改変していてもソースの提供義務は生じない (GPL にはネットワーク越しの利用の条項が無い、条文からの読み)。受託で納品する、パッケージや機器に入れて配布するなら、配布物のソースを GPL で出す。自社のプラグインを組み込んで配布すると、プラグインも GPL の対象になりうる (推測)。
- deegree (LGPL-2.1): ライブラリとして自社のアプリに組み込んで配布するなら、利用者が deegree の部分を差し替えられるようにする (動的リンクなど)。deegree を改変して配布するなら、改変部分のソースを LGPL で出す。SaaS 提供だけなら配布に当たらない (条文からの読み)。
- MapServer (MIT 型)、MapProxy (Apache-2.0)、OWSLib (BSD-3-Clause) は表示の保持で足りる。
- 重ねる WMS の画像の利用条件は配信元ごとに違う。J-SHIS など公的機関の WMS も、利用規約を map-legal-check で確かめる。

## 出典

- https://www.ogc.org/standards/wms/ : WMS の版と文書番号、ISO 19128。
- https://www.ogc.org/standards/wmts/ : WMTS 1.0.0 (07-057r7)、Simple Profile。
- https://www.ogc.org/standards/wfs/ : WFS 2.0.2 (09-025r2)、ISO 19142、OGC API - Features の推奨。
- `gh api repos/<owner>/<repo>/license` と releases (geoserver/geoserver、MapServer/MapServer、qgis/QGIS、mapproxy/mapproxy、deegree/deegree3、geopython/OWSLib) : ライセンスと版。
- https://www.j-shis.bosai.go.jp/en/wms-landslide と `https://www.j-shis.bosai.go.jp/map/wms/landslide?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0` : J-SHIS の WMS。
- map-compare-library の各ライブラリの reference : ライブラリの対応。

## 未確認のこと

- 国土地理院、国土交通省、海しるなどの WMS、WMTS の公式の配信の有無と規約。
- QGIS の LICENSE の「or later」の扱い (GitHub は GPL-2.0 と判定した)。
- WMS 1.3.0 の軸の順の条文の箇所。
- 主要な国内の自治体 GIS が出している WMS の数。
