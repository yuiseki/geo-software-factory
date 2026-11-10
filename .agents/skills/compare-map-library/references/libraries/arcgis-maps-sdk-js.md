# ArcGIS Maps SDK for JavaScript

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 5.2.1 (npm の `@arcgis/core`、2026-11-07 JST)。5.2.0 は 2026-11-06 JST ([npm @arcgis/core](https://www.npmjs.com/package/@arcgis/core))。確かめた時点で公式のリリースノートは 5.1 (2026 年 6 月) までの記載だった ([Release notes](https://developers.arcgis.com/javascript/latest/release-notes/)) |
| リポジトリ | ソースコードのリポジトリは非公開。配布は npm の `@arcgis/core`、`@arcgis/map-components` と CDN (https://js.arcgis.com)。テンプレートとサンプルは [Esri/jsapi-resources](https://github.com/Esri/jsapi-resources) (このリポジトリ自体は Apache-2.0) |
| ドキュメント | https://developers.arcgis.com/javascript/latest/ |
| ライセンス (LICENSE ファイルで確かめる) | プロプライエタリ。npm パッケージの LICENSE.md は「Esri Master License Agreement (MLA) の条件で使用を許諾し、改変しない限り再配布と使用を認める」と書く ([LICENSE.txt](https://js.arcgis.com/5.2/LICENSE.txt)、npm の `license` 欄は `SEE LICENSE IN LICENSE.md`) |
| 運営主体・ガバナンス | Esri (Environmental Systems Research Institute, Inc.、米国カリフォルニア州レッドランズ) の単独開発。外部からのコード貢献の経路は無い。日本では ESRI ジャパンが販売と支援を行う ([LICENSE.txt](https://js.arcgis.com/5.2/LICENSE.txt)、[ESRI ジャパン](https://www.esrij.com/case-studies/list/?tx=local-governments)) |

## 概要

Esri が提供する Web 向けの地図・空間解析用 SDK で、2D の MapView と 3D の SceneView を持つ ([Key features](https://developers.arcgis.com/javascript/latest/key-features/)、[SceneView](https://developers.arcgis.com/javascript/latest/references/core/views/SceneView/))。クライアント側のクエリ、フィルター、統計、ジオメトリ演算、2D/3D の編集、凡例やポップアップなどの UI コンポーネントを含む ([Key features](https://developers.arcgis.com/javascript/latest/key-features/))。ArcGIS Online、ArcGIS Enterprise、ArcGIS Location Platform と組み合わせて使う前提の製品で、Web アプリとして配備する場合は他の Esri 製品と併用することがライセンス条件になっている ([E300 脚注 63](https://www.esri.com/content/dam/esrisites/en-us/media/legal/product-specific-terms-of-use/e300.pdf))。5.0 から UI は Web コンポーネント (`@arcgis/map-components`) が推奨で、従来のウィジェットは非推奨になった ([Release notes](https://developers.arcgis.com/javascript/latest/release-notes/))。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU、独自エンジンか他ライブラリの上か): WebGL2 による独自エンジン。動作要件は「WebGL2 が使える 64 ビットのブラウザのみ」で、WebGPU についての記載は無い ([System requirements](https://developers.arcgis.com/javascript/latest/system-requirements/))。npm の依存に他の地図描画ライブラリは含まれない ([npm @arcgis/core](https://www.npmjs.com/package/@arcgis/core))。
- 2D / 2.5D (傾き・回転) / 3D: 2D の MapView は回転に対応し、傾きは扱わない。3D は SceneView で、3D シンボルは SceneView でしか描けない ([MapView](https://developers.arcgis.com/javascript/latest/references/core/views/MapView/)、[ObjectSymbol3DLayer](https://developers.arcgis.com/javascript/latest/references/core/symbols/ObjectSymbol3DLayer/))。
- 地球儀表示: 対応。SceneView の `viewingMode` が global なら地球儀、local なら平面に描く ([SceneView](https://developers.arcgis.com/javascript/latest/references/core/views/SceneView/))。
- 対応する投影法: SceneView の global は WGS84、Web メルカトル、CGCS2000 (火星・月などは実験的)。local は任意の投影座標系と WGS84、CGCS2000 ([SceneView](https://developers.arcgis.com/javascript/latest/references/core/views/SceneView/))。MapView は `spatialReference` を実行時に切り替えられるが、ベースマップのタイル層はタイル体系の空間参照と一致させる必要があり、一致しないレイヤーは表示されない ([MapView](https://developers.arcgis.com/javascript/latest/references/core/views/MapView/))。

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | WebTileLayer に `{level}/{col}/{row}` や `{z}/{x}/{y}` の URL テンプレートを渡す。既定の空間参照は Web メルカトル。別ドメインは CORS が要る ([WebTileLayer](https://developers.arcgis.com/javascript/latest/references/core/layers/WebTileLayer/)) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT は対応。PMTiles と MLT は未確認 | VectorTileLayer。スタイル JSON の `vector` ソースに任意の URL を指定できる。4.34 から TileJSON も読めるが、Web メルカトル、512 px タイルなどの条件がある ([VectorTileLayer](https://developers.arcgis.com/javascript/latest/references/core/layers/VectorTileLayer/)) |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 一部対応 | VectorTileLayer の描画は「MapLibre style specification で定義される」と書かれている。スタイルを書き換えるヘルパーは 2D の MapView のみ。対応範囲がどこまで仕様と一致するかは未確認 ([VectorTileLayer](https://developers.arcgis.com/javascript/latest/references/core/layers/VectorTileLayer/)) |
| GeoJSON | 対応 | GeoJSONLayer。RFC 7946 準拠が前提で、1 レイヤーに 1 種類のジオメトリ、GeometryCollection 非対応、日付変更線をまたぐジオメトリ非対応 ([GeoJSONLayer](https://developers.arcgis.com/javascript/latest/references/core/layers/GeoJSONLayer/)) |
| 3D Tiles / glTF | 対応 (SceneView) | IntegratedMesh3DTilesLayer (4.29 から) が tileset.json を読む。テクスチャは JPEG、PNG、KTX2/Basis ([IntegratedMesh3DTilesLayer](https://developers.arcgis.com/javascript/latest/references/core/layers/IntegratedMesh3DTilesLayer/))。glTF は ObjectSymbol3DLayer の外部モデルとして使える ([ObjectSymbol3DLayer](https://developers.arcgis.com/javascript/latest/references/core/symbols/ObjectSymbol3DLayer/)) |
| 地形 (標高タイル) | 対応 (ArcGIS の標高サービス) | ElevationLayer は ArcGIS Image Server の標高サービスを指す。`ground: "world-elevation"` で Esri の全球標高を使える。Terrain-RGB や quantized-mesh の記載は無い ([ElevationLayer](https://developers.arcgis.com/javascript/latest/references/core/layers/ElevationLayer/)) |
| WMS / WMTS | 対応 | WMSLayer、WMTSLayer がある ([WMS サンプル](https://developers.arcgis.com/javascript/latest/sample-code/layers-wms/)、[WMTS サンプル](https://developers.arcgis.com/javascript/latest/sample-code/layers-wmts/))。SceneView では WMTS の空間参照を view と合わせる必要がある ([Esri Community](https://community.esri.com/t5/arcgis-javascript-maps-sdk-questions/add-wmts-service-to-scene/m-p/1195347/highlight/true)) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: 技術的には XYZ、MVT、WMS、WMTS など他社のタイルも読める。ただし製品別利用規約 E300 (2025-11-13 版) は「Web 配備の付加価値アプリケーションは他の Esri 製品と併用しなければならない」(脚注 63)、「第三者の技術は、付加価値アプリケーションが常に他の Esri 製品と併用される限り併用できる」(脚注 64) と定める ([E300](https://www.esri.com/content/dam/esrisites/en-us/media/legal/product-specific-terms-of-use/e300.pdf))。このため OSM などのタイルだけで Esri のサービスを一切使わないアプリにこの SDK を使うのは規約上認められないと読める (推測。最終的な解釈は Esri への確認が要る)。また Esri の Basemap Styles は ArcGIS Location Platform の Basemap Services 専用 (脚注 109)。
- API キー・アカウントの要否: Esri のサービス (ベースマップ、ジオコーディング、ルーティング、標高など) を使うには ArcGIS Location Platform か ArcGIS Online のアカウントが要る。Location Platform では API キーを発行して使う ([Licensing](https://developers.arcgis.com/javascript/latest/licensing/))。収益を生むアプリが Location Platform にアクセスする場合は認証 (API キーなど) が必須 (E300 脚注 89)。

## ライセンスと費用

- ライセンス: プロプライエタリ (Esri MLA)。SDK 自体の追加購入は不要で、ArcGIS Online / Enterprise の組織、または ArcGIS Location Platform のアカウントで使う ([Licensing](https://developers.arcgis.com/javascript/latest/licensing/))。SDK で作ったアプリを第三者に配布・使用許諾してよい (E300 脚注 16)。
- 利用料 (無料 / 従量 / 有料の機能): SDK の利用料は無い。ArcGIS Location Platform のサービスは従量課金で、例として (USD、2026-11-10 確認) ベースマップタイルは月 200 万タイルまで無料、以降 1,000 タイルあたり $0.15。ベースマップセッションは 1,000 まで無料、以降 1,000 セッションあたり $4。ジオコーディング (保存しない) は 2 万件まで無料、以降 1,000 件あたり $0.5。標高は 5 万点まで無料、以降 1,000 点あたり $1。ベクタータイルの配信は 25 GB まで無料、以降 1 GB あたり $0.43。技術サポートは年 $2,500 ([Location Platform pricing](https://location.arcgis.com/pricing/))。ArcGIS Online のユーザータイプは年間ライセンスで、価格は公式ページに表示が無く問い合わせ制 ([ArcGIS Online ユーザー タイプの価格](https://www.esri.com/ja-jp/arcgis/products/arcgis-online/buy))。日本の自治体向けには ESRI ジャパンの「ArcGIS 自治体ソリューションライセンス」(2014 年発表、人口に応じ年 40 万円 (税抜) から) などの包括契約がある ([2014-08-18 プレスリリース](https://www.value-press.com/pressrelease/129860))。現行価格は未確認。
- 版によるライセンスの変化: なし (確かめた範囲で、4.x から 5.x まで同じ MLA 系の条件)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): OSI 非承認のプロプライエタリ製品。組み込み: Esri のアカウント (Location Platform、ArcGIS Online、Enterprise のいずれか) と、Web 配備では他の Esri 製品との併用が条件 (E300 脚注 63、64)。改変: LICENSE は「改変しない限り」再配布を認めるので、SDK 本体のコードを改変して配布することはできない ([LICENSE.txt](https://js.arcgis.com/5.2/LICENSE.txt))。配布: アプリに同梱して配布できるが、著作権表示を残す必要がある ([LICENSE.txt](https://js.arcgis.com/5.2/LICENSE.txt))。収益を生むアプリを第三者に配布する場合は Location Platform への認証付きアクセスが必須で、配備用に使える Location Platform のサブスクリプションは組織内で 1 つまで (E300 脚注 89、90)。SaaS 提供: 上記に加え、地図のないアプリも含め「Powered by Esri」の表示と、ベースマップ・データ提供元の帰属表示が必須 ([Licensing](https://developers.arcgis.com/javascript/latest/licensing/))。ジオコーディング結果の保存は有料の保存付きジオコードでのみ可 (E300 脚注 66)。

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 未確認。bundlephobia は `@arcgis/core` 5.2.1 のエントリポイントを判定できず計測結果を返さない ([bundlephobia](https://bundlephobia.com/package/@arcgis/core@5.2.1))。参考として npm パッケージの展開後サイズは 88,864,727 バイト (ES モジュールの集合で、実際のバンドルは使うモジュールで変わる) ([npm @arcgis/core](https://www.npmjs.com/package/@arcgis/core))。
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 公式は「2D と 3D で数十万の地物を可視化できる」と書き、約 100 万の建物地物を動かす例を挙げる ([Key features](https://developers.arcgis.com/javascript/latest/key-features/))。測定条件は書かれていない。
- 低性能端末・モバイルブラウザでの注意: 必要メモリはデスクトップ 8 GB 以上、モバイル 4 GB 以上。対応ブラウザは Chrome / Edge 146 以上、Firefox 151 以上と 140 ESR、Safari と iOS Safari 18 以上 (5.1 時点)。ハードウェアアクセラレーションが無いと 2D は劣化した描画モードになる。SceneView は 4K を超える解像度に非対応。iOS Safari では Fullscreen コンポーネントが動かない ([System requirements](https://developers.arcgis.com/javascript/latest/system-requirements/))。

## エコシステム

- 主なプラグイン・拡張: Esri 製の Web コンポーネント群 (`@arcgis/map-components`、チャートの `@arcgis/charts-components`、コード編集の coding components) と UI の Calcite Design System (`@esri/calcite-components`) ([@arcgis/core README](https://www.npmjs.com/package/@arcgis/core)、[Esri/jsapi-resources templates](https://github.com/Esri/jsapi-resources/tree/main/templates)、[Release notes](https://developers.arcgis.com/javascript/latest/release-notes/))。サードパーティのプラグイン市場は無い。
- React / Vue などのラッパー: 公式の `@arcgis/map-components-react` は 5.0 で非推奨、6.0 で削除予定。React 19 以降と Vue では Web コンポーネントの `@arcgis/map-components` を直接使う ([npm @arcgis/map-components-react](https://www.npmjs.com/package/@arcgis/map-components-react))。React、Vue、Angular、Vite、webpack 向けの公式テンプレートがある ([templates](https://github.com/Esri/jsapi-resources/tree/main/templates))。
- TypeScript の型: パッケージに同梱 (5.2.1 の tarball に `.d.ts` が 1,740 ファイル) ([npm @arcgis/core](https://www.npmjs.com/package/@arcgis/core))。
- 日本語の情報: 公式ドキュメントは英語のみ。ESRI ジャパンが GitHub で日本語のガイド集を公開している ([esrijapan/arcgis-dev-resources](https://esrijapan.github.io/arcgis-dev-resources/tips/javascript))。Esri Community に日本語の連載がある ([Esri Community](https://community.esri.com/t5/s/a/ta-p/1664557))。

## 開発の活発さ

- 直近 1 年のリリース数: 2025-11-10 から 2026-11-10 までに npm の安定版は 53 件 (パッチを含む)。マイナー版は 5.0.0 (2026-02-21 JST)、5.1.0 (2026-06-19 JST)、5.2.0 (2026-11-06 JST) の 3 つ。プレリリース (`next`) は別に 434 件 ([npm @arcgis/core](https://www.npmjs.com/package/@arcgis/core))。
- 最終コミット日: 対象外 (ソースリポジトリが非公開)。npm パッケージの最終更新は 2026-11-09 JST ([npm @arcgis/core](https://www.npmjs.com/package/@arcgis/core))。
- 近年の大きな破壊的変更: 5.0 (2026-02) で全ウィジェットが非推奨になり、6.0 (2027 年第 1 四半期予定) から削除が始まる。5.1 で `arcgis-popup` の `triggerAction()` 削除、複数のコンポーネント名の置き換えなど ([Release notes](https://developers.arcgis.com/javascript/latest/release-notes/))。

## 向いている場面

- ArcGIS Online / Enterprise を既に導入している組織 (日本では自治体の導入事例が ESRI ジャパンのサイトに 256 件あり、防災や道路・上下水道の管理が多い) が、その上で Web アプリを作る場合 ([ESRI ジャパン 導入事例](https://www.esrij.com/case-studies/list/?tx=local-governments))。ただしこれらは ArcGIS 製品全体の事例で、この SDK を直接使った事例かは区別されていない。
- 2D と 3D、クライアント側の空間解析、編集、凡例・ポップアップなどの業務 UI を 1 つの SDK でまとめたい場合。
- 任意の投影座標系 (平面直角座標系など) のデータを 2D / 3D で扱う場合。

## 向いていない場面

- Esri の製品やサービスを使わず、OSM などのタイルだけで地図を出したい場合 (規約上 Esri 製品との併用が条件)。
- SDK を改変して配布したい場合、OSS であることが調達条件になっている場合。
- バンドルを小さく保ちたい軽量な地図表示。
- 費用を事前に固定したい小規模サービス (Location Platform は従量課金、ArcGIS Online は問い合わせ制)。

## 出典

- https://developers.arcgis.com/javascript/latest/
- https://developers.arcgis.com/javascript/latest/licensing/
- https://developers.arcgis.com/javascript/latest/release-notes/
- https://developers.arcgis.com/javascript/latest/key-features/
- https://developers.arcgis.com/javascript/latest/system-requirements/
- https://developers.arcgis.com/javascript/latest/references/core/views/SceneView/
- https://developers.arcgis.com/javascript/latest/references/core/views/MapView/
- https://developers.arcgis.com/javascript/latest/references/core/layers/WebTileLayer/
- https://developers.arcgis.com/javascript/latest/references/core/layers/VectorTileLayer/
- https://developers.arcgis.com/javascript/latest/references/core/layers/GeoJSONLayer/
- https://developers.arcgis.com/javascript/latest/references/core/layers/IntegratedMesh3DTilesLayer/
- https://developers.arcgis.com/javascript/latest/references/core/layers/ElevationLayer/
- https://developers.arcgis.com/javascript/latest/references/core/symbols/ObjectSymbol3DLayer/
- https://developers.arcgis.com/javascript/latest/sample-code/layers-wms/
- https://developers.arcgis.com/javascript/latest/sample-code/layers-wmts/
- https://community.esri.com/t5/arcgis-javascript-maps-sdk-questions/add-wmts-service-to-scene/m-p/1195347/highlight/true
- https://js.arcgis.com/5.2/LICENSE.txt
- https://www.esri.com/en-us/legal/terms/product-specific-scope-of-use
- https://www.esri.com/content/dam/esrisites/en-us/media/legal/product-specific-terms-of-use/e300.pdf
- https://location.arcgis.com/pricing/
- https://www.esri.com/ja-jp/arcgis/products/arcgis-online/buy
- https://www.npmjs.com/package/@arcgis/core
- https://www.npmjs.com/package/@arcgis/map-components-react
- https://bundlephobia.com/package/@arcgis/core@5.2.1
- https://github.com/Esri/jsapi-resources
- https://github.com/Esri/jsapi-resources/tree/main/templates
- https://esrijapan.github.io/arcgis-dev-resources/tips/javascript
- https://community.esri.com/t5/s/a/ta-p/1664557
- https://www.esrij.com/case-studies/list/?tx=local-governments
- https://www.value-press.com/pressrelease/129860

## 未確認のこと

- バンドルサイズ (min+gzip)。bundlephobia が計測できず、Esri の公式な数値も見つからなかった。
- PMTiles と MLT への対応。VectorTileLayer のリファレンスに記載が無かった。
- VectorTileLayer が MapLibre Style Spec のどの範囲に対応するか。リファレンスは仕様名を挙げるだけで対応表を確かめられなかった。
- Google Photorealistic 3D Tiles や Cesium ion のタイルセットを IntegratedMesh3DTilesLayer で読めるか。リファレンスに記載が無かった。
- 5.2 の変更内容。確かめた時点で公式リリースノートが 5.1 までで、5.2 の告知ブログは取得できなかった (HTTP 403)。
- Esri 製品を併用しないアプリでの利用可否の最終的な解釈 (E300 脚注 63、64 の読み方)。条文からの推測にとどまる。
- ESRI ジャパンの自治体向けライセンスの現行価格。手元で確かめられたのは 2014 年の発表のみ。
