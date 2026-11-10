# OpenLayers

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 10.11.0 (2026-10-05 JST)。npm パッケージ名は `ol` で、`latest` タグも 10.11.0 (https://github.com/openlayers/openlayers/releases/tag/v10.11.0, https://www.npmjs.com/package/ol) |
| リポジトリ | https://github.com/openlayers/openlayers |
| ドキュメント | https://openlayers.org/ (API は https://openlayers.org/en/latest/apidoc/、例は https://openlayers.org/en/latest/examples/) |
| ライセンス (LICENSE ファイルで確かめる) | BSD 2-Clause。著作権表記は「2005-present, OpenLayers Contributors」(https://github.com/openlayers/openlayers/blob/main/LICENSE.md) |
| 運営主体・ガバナンス | 著作権者は OpenLayers Contributors (LICENSE)。保守の資金は GitHub Sponsors と Open Collective の継続スポンサーから受けている (https://github.com/openlayers/openlayers/blob/main/README.md)。OSGeo のサイトにプロジェクトページがあり、主要コントリビュータの所属先として terrestris、Camptocamp、ahocevar geospatial が載る (https://www.osgeo.org/projects/openlayers/)。運営委員会などの規程は確かめられなかった |

## 概要

OpenLayers は Web ページに対話的な地図を載せる JavaScript ライブラリで、XYZ タイル、OGC の地図サービス、タイルでない画像レイヤーと、GeoJSON、TopoJSON、KML、GML、Mapbox Vector Tiles などのベクターを扱う (https://openlayers.org/)。描画には Canvas 2D と WebGL を使う (同ページ)。投影法の扱いが広く、proj4 で登録した任意の投影を使える (https://openlayers.org/doc/faq.html)。GIS 業務で使う OGC サービスや GeoTIFF を標準で読める点が特徴である。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): 既定は Canvas 2D。WebGL のレイヤー (`WebGLTile`、`WebGLVector`、WebGL のベクトルタイル) を選べる (https://openlayers.org/, https://openlayers.org/en/latest/examples/webgl-vector-layer.html, https://openlayers.org/en/latest/examples/webgl-vector-tiles.html)。WebGL Vector Layer の例は `experimental` 扱いである (https://github.com/openlayers/openlayers/blob/main/examples/webgl-vector-layer.html)。WebGPU は公式サイトに記述がない。
- 2D / 2.5D (傾き・回転) / 3D: 2D で、地図の回転に対応する (View の rotation、https://openlayers.org/en/latest/apidoc/module-ol_View-View.html)。傾き (pitch) は持たない。3D は CesiumJS と組み合わせる ol-cesium (npm 名 `olcs`、BSD-2-Clause) で行う (https://github.com/openlayers/ol-cesium)。
- 地球儀表示: 本体は非対応。ol-cesium で CesiumJS の地球儀に OpenLayers のレイヤーを載せる (https://github.com/openlayers/ol-cesium)。
- 対応する投影法: 既定は EPSG:3857 で、EPSG:4326 も組み込み。他の投影は proj4 で定義して登録すれば使える (https://openlayers.org/doc/faq.html)。ラスタの再投影、GeoTIFF の再投影、ベクトルタイルの再投影の例がある (https://openlayers.org/en/latest/examples/reprojection.html, https://openlayers.org/en/latest/examples/geotiff-reprojection.html, https://openlayers.org/en/latest/examples/vector-tiles-reprojected.html)。

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | XYZ、OSM などのタイルソース (https://openlayers.org/)。10.0 で画像タイル用の新しい基底ソースが入った (https://github.com/openlayers/openlayers/releases/tag/v10.0.0)。COG / GeoTIFF も WebGL タイルレイヤーで読める (https://openlayers.org/en/latest/examples/cog.html) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT は標準、PMTiles は外部パッケージ | MVT は標準で読める (https://openlayers.org/, https://openlayers.org/en/latest/examples/mapbox-vector-tiles.html)。PMTiles は `ol-pmtiles` (BSD-3-Clause、2.0.2) か `pmtiles` ライブラリと DataTile ソースの組み合わせで読む (https://www.npmjs.com/package/ol-pmtiles, https://openlayers.org/en/latest/examples/pmtiles-elevation.html)。MLT 対応は未確認 |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 外部パッケージで対応 | ol-mapbox-style (BSD-2-Clause) が Mapbox Style / MapLibre Style から OpenLayers のレイヤーや地図を作る (https://github.com/openlayers/ol-mapbox-style)。OpenLayers 10.3.1 より新しい版には ol-mapbox-style 12.4 以上が要る (同 README、https://github.com/openlayers/openlayers/blob/main/changelog/upgrade-notes.md)。本体には独自の「flat style」と式がある (https://github.com/openlayers/openlayers/releases/tag/v10.0.0) |
| GeoJSON | 対応 | GeoJSON、TopoJSON、KML、GML などのフォーマットを標準で持つ (https://openlayers.org/)。10.11.0 で空座標配列の扱いを直した (https://github.com/openlayers/openlayers/blob/main/changelog/upgrade-notes.md) |
| 3D Tiles / glTF | 本体は非対応 | ol-cesium で CesiumJS と組み合わせる場合は CesiumJS 側の機能になる (https://github.com/openlayers/ol-cesium)。CesiumJS 側の対応範囲はこのファイルの範囲外 |
| 地形 (標高タイル) | 2D の陰影表現のみ | 標高タイルを WebGL タイルレイヤーで読み、陰影図や海面上昇の表現を計算する例がある (https://openlayers.org/en/latest/examples/webgl-shaded-relief.html, https://openlayers.org/en/latest/examples/pmtiles-elevation.html)。3D 地形は ol-cesium 経由 |
| WMS / WMTS | 対応 | WMS (タイル、単一画像) と WMTS を標準で持ち、Capabilities 文書からレイヤーを作れる (https://openlayers.org/en/latest/examples/wms-tiled.html, https://openlayers.org/en/latest/examples/wmts-layer-from-capabilities.html)。10.11.0 で WMTS のタイル格子の範囲計算と `wrapX` の扱いが変わった (https://github.com/openlayers/openlayers/blob/main/changelog/upgrade-notes.md) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリ側の制限はなく、タイル提供者の規約に従う。OpenStreetMap 財団の標準タイルは、帰属表示、識別できる User-Agent と Referer、表示外タイルの一括取得の禁止、過度な利用の禁止を定め、SLA はない (https://operations.osmfoundation.org/policies/tiles/)。Bing Maps for Enterprise が 2028-06-30 に終了するため、10.10.0 で `ol/source/BingMaps` が非推奨になり、Azure Maps のタイル API への置き換えが案内されている (https://github.com/openlayers/openlayers/blob/main/changelog/upgrade-notes.md)。
- API キー・アカウントの要否: ライブラリ自体には不要。タイル提供者によっては必要になる。

## ライセンスと費用

- ライセンス: BSD 2-Clause (https://github.com/openlayers/openlayers/blob/main/LICENSE.md)
- 利用料 (無料 / 従量 / 有料の機能): ライブラリは無料。費用はタイルや地図サービスの提供者で決まる。
- 版によるライセンスの変化: なし (npm の license 欄も BSD-2-Clause、https://www.npmjs.com/package/ol)

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 10.11.0 で 85.9 kB (bundlephobia、https://bundlephobia.com/package/ol@10.11.0)。これはパッケージの既定エントリを計った値で、`ol` はモジュール単位で import するため、実際の大きさは使うモジュールで変わる。
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 公式に件数の目安は見当たらない。大量の点は WebGL のベクターレイヤーで描く例がある (https://openlayers.org/en/latest/examples/webgl-points-layer.html)。10.4.0 で `WebGLPointsLayer` は非推奨になり、線と面も描ける `WebGLVectorLayer` に置き換える (https://github.com/openlayers/openlayers/blob/main/changelog/upgrade-notes.md)。
- 低性能端末・モバイルブラウザでの注意: 公式サイトはモバイル対応を掲げる (https://openlayers.org/)。10.10.0 から TextPath が `Intl.Segmenter` を使い、Firefox 125 より前などの古いブラウザでは polyfill が要る (https://github.com/openlayers/openlayers/blob/main/changelog/upgrade-notes.md)。Internet Explorer は 7.0.0 で対応を外した (同ファイル)。

## エコシステム

- 主なプラグイン・拡張: ol-mapbox-style (Mapbox/MapLibre Style、13.9.0、https://github.com/openlayers/ol-mapbox-style)、ol-cesium (3D と地球儀、2.23.1、https://github.com/openlayers/ol-cesium)、ol-pmtiles (PMTiles、https://www.npmjs.com/package/ol-pmtiles)。いずれも openlayers 組織か protomaps が公開している。
- React / Vue などのラッパー: React は rlayers (ISC、https://github.com/mmomtchev/rlayers)、Vue 3 は vue3-openlayers (MIT、https://github.com/MelihAltintas/vue3-openlayers)。どちらも第三者のプロジェクトである。
- TypeScript の型: `ol` パッケージに自動生成の `.d.ts` が同梱される (https://github.com/openlayers/openlayers/blob/main/README.md)。
- ネイティブ版・兄弟プロジェクト: ネイティブ SDK はない (確認した範囲)。兄弟プロジェクトとして ol-mapbox-style と ol-cesium が同じ GitHub 組織にある。
- 日本語の情報 (公式翻訳、国内コミュニティ): 公式サイトのトップページに日本語版への導線は見当たらなかった (https://openlayers.org/)。国内コミュニティは未確認。

## 開発の活発さ

- 直近 1 年のリリース数: 安定版 4 件 (10.8.0、10.9.0、10.10.0、10.11.0)。対象期間は 2025-11-10 から 2026-11-10 (https://github.com/openlayers/openlayers/releases)。npm には `dev` タグの開発版が別に公開されている (https://www.npmjs.com/package/ol)
- 最終コミット日: 2026-11-02 (JST、main ブランチ、https://github.com/openlayers/openlayers/commits/main)
- 近年の大きな破壊的変更: メジャー版はおおむね年 1 回で、v8.0.0 (2023-08)、v9.0.0 (2024-02)、v10.0.0 (2024-07) と出ている (https://github.com/openlayers/openlayers/releases)。v10.0.0 は、`getFeaturesInExtent()` の VectorTile ソースからレイヤーへの移動、flat style の `get` 式の型ヒント廃止などで、リリースノートは「破壊的変更はごく小さい」と書く (https://github.com/openlayers/openlayers/releases/tag/v10.0.0)。v10 系の中でも非推奨化 (10.4.0 の `WebGLPointsLayer`、10.10.0 の `BingMaps`) が続いている (https://github.com/openlayers/openlayers/blob/main/changelog/upgrade-notes.md)。

## 向いている場面

- Web メルカトル以外の投影法 (国や自治体の平面直角座標系など) で地図を表示する GIS 業務。
- WMS / WMTS の Capabilities、GeoTIFF / COG、KML、GML など OGC 系のデータを直接扱う案件。
- 作図、編集、計測などの対話機能を、ラスタとベクターの両方の上で作り込む管理画面。

## 向いていない場面

- 傾き、3D 建物、3D 地形を Web 地図の中で軽く使いたい場合 (本体に pitch がなく、3D は CesiumJS との組み合わせになる)。
- MapLibre Style で作ったベース地図を、そのままの見た目で描きたい場合 (ol-mapbox-style での変換になり、表現の一致は保証されていない。一致の程度は未確認)。
- MLT のベクトルタイルを使う場合 (対応を確かめられなかった)。

## 出典

- https://openlayers.org/
- https://openlayers.org/doc/faq.html
- https://openlayers.org/en/latest/apidoc/
- https://openlayers.org/en/latest/apidoc/module-ol_View-View.html
- https://openlayers.org/en/latest/examples/
- https://openlayers.org/en/latest/examples/webgl-vector-layer.html
- https://openlayers.org/en/latest/examples/webgl-vector-tiles.html
- https://openlayers.org/en/latest/examples/webgl-points-layer.html
- https://openlayers.org/en/latest/examples/webgl-shaded-relief.html
- https://openlayers.org/en/latest/examples/pmtiles-elevation.html
- https://openlayers.org/en/latest/examples/mapbox-vector-tiles.html
- https://openlayers.org/en/latest/examples/cog.html
- https://openlayers.org/en/latest/examples/reprojection.html
- https://openlayers.org/en/latest/examples/geotiff-reprojection.html
- https://openlayers.org/en/latest/examples/vector-tiles-reprojected.html
- https://openlayers.org/en/latest/examples/wms-tiled.html
- https://openlayers.org/en/latest/examples/wmts-layer-from-capabilities.html
- https://github.com/openlayers/openlayers
- https://github.com/openlayers/openlayers/blob/main/LICENSE.md
- https://github.com/openlayers/openlayers/blob/main/README.md
- https://github.com/openlayers/openlayers/blob/main/changelog/upgrade-notes.md
- https://github.com/openlayers/openlayers/blob/main/examples/webgl-vector-layer.html
- https://github.com/openlayers/openlayers/releases
- https://github.com/openlayers/openlayers/releases/tag/v10.0.0
- https://github.com/openlayers/openlayers/releases/tag/v10.11.0
- https://github.com/openlayers/openlayers/commits/main
- https://www.npmjs.com/package/ol
- https://bundlephobia.com/package/ol@10.11.0
- https://www.osgeo.org/projects/openlayers/
- https://github.com/openlayers/ol-mapbox-style
- https://github.com/openlayers/ol-cesium
- https://www.npmjs.com/package/ol-pmtiles
- https://github.com/mmomtchev/rlayers
- https://github.com/MelihAltintas/vue3-openlayers
- https://operations.osmfoundation.org/policies/tiles/

## 未確認のこと

- 運営委員会 (PSC など) の有無と OSGeo での位置づけ (卒業済みか): OSGeo のプロジェクトページと README に記述がなかった。
- MLT への対応: 例と upgrade notes に記述が見当たらなかった。
- WebGPU への取り組み: 公式サイトに記述がなかった。
- 扱える地物の数の目安: 公式の例に件数の記述がなかった。
- ol-mapbox-style で MapLibre Style をどこまで同じ見た目で描けるか: 対応範囲の一覧を確かめていない。
- 国内コミュニティと日本語の公式情報: 一次情報を確かめられなかった。
