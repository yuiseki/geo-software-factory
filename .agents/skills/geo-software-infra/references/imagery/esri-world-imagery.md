# Esri World Imagery

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | Environmental Systems Research Institute, Inc. (Esri)。ArcGIS Living Atlas of the World の 1 レイヤとして提供 |
| 公式サイト | アイテムページ https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9 、タイルサービス https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer |
| 料金ページ | https://location.arcgis.com/pricing/ (ArcGIS Location Platform のベースマップタイルとして課金) |
| 利用規約・ライセンス | Esri Master Agreement (E204、2026-08-14 版) https://www.esri.com/en-us/legal/terms/full-master-agreement 、利用の概要 https://goto.arcgis.com/termsofuse/viewsummary 、利用規約 https://goto.arcgis.com/termsofuse/viewtermsofuse 、データ収集・編集での許可範囲 https://www.arcgis.com/home/item.html?id=8e90a00a0a6845a49262e0b756f57a10 |

## 概要

Esri World Imagery は、全球の低解像度衛星画像と、世界の大半の陸域をおおう 1 m 以上の高解像度の衛星・航空写真をつないだ画像ベースマップである (https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9)。小縮尺は Earthstar Geographics の TerraColor、大縮尺は Vantor (旧 Maxar Intelligence) の Vivid 系の製品と、自治体などが Community Maps Program で提供した航空写真からなる。ArcGIS Location Platform では `arcgis/imagery` などのベースマップスタイルとして使え (https://developers.arcgis.com/rest/basemap-styles/)、過去の版は World Imagery Wayback で 2014 年から見られる (https://github.com/Esri/wayback)。

## 画像の性質

- 元になる衛星・航空機とセンサー: 小縮尺 (約 1:5 億 9,100 万〜約 1:28 万 8,000) は Earthstar Geographics の 15 m 解像度 TerraColor。大縮尺は Vantor の画像ベースマップ製品で、Vivid Premium (15 cm HD、一部の大都市)、Vivid Advanced (30 cm と 30 cm HD、1,000 以上の都市圏)、Vivid Standard (1.2 m〜30 cm HD、世界の大半)。これに GIS User Community が提供した 30 cm〜3 cm の航空写真が加わる (https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9 、https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer?f=json)。Esri は 2026-08-20 に、Airbus が 2026 年後半から約 2,000 都市の 30 cm 画像の提供を始めること、Nearmap の 20 cm 航空写真を米国・カナダ・豪州・ニュージーランドの 200 都市圏で取り込むこと、Vantor の 40 の大都市を 15 cm HD に上げることを発表した (https://www.esri.com/about/newsroom/announcements/esri-expands-world-imagery-with-airbus-high-resolution-basemap-coverage-for-2000-cities-worldwide 、転載 https://newshub.medianet.com.au/2026/08/esri-expands-world-imagery-with-airbus-high-resolution-basemap-coverage-for-2000-cities-worldwide/167393/)。発表に日本の都市名はなく、対象都市の一覧も公表されていない。2026-11-10 時点の帰属データ (https://static.arcgis.com/attribution/World_Imagery?f=json、646 件) には Nearmap はあるが Airbus はまだない。
- 地上解像度 (地域ごとに違えば国内と全球を分けて): 全球は 15 m (小縮尺) と 1.2 m〜30 cm (大縮尺)。米国と西欧の一部は 30 cm HD (https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9)。国内は、帰属データで東京付近を引くと Vantor がズーム 14〜17、練馬区の航空写真 (CC BY 4.0) がズーム 20〜23 に出る (https://static.arcgis.com/attribution/World_Imagery?f=json)。国内のどこが何 cm かの一覧は公表されていない。
- 撮影時期と更新頻度: アイテムの説明では高解像度部分はおおむね 3〜5 年以内のもの (https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9)。Vivid Premium と Vivid Advanced は「更新を約束した」製品とされる。更新は月 1 回程度で版が出ており、Wayback の設定ファイルでは 2026 年は R01〜R10 まで公開されている (https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json)。撮影日は地点ごとに Identify や「World Imagery with Metadata」で確認できる。
- 過去画像 (時系列) の有無と期間: あり。World Imagery Wayback が 2014-02-20 から 2026-10-29 までの 198 版を公開している (2026-11-10 に https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json を集計)。各版は WMTS の URL (`https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/{版番号}/{level}/{row}/{col}`) で取得でき、アプリは https://livingatlas.arcgis.com/wayback/ 。アプリのコードは Apache-2.0 だが、画像は Esri Master Agreement に従う (https://github.com/Esri/wayback)。各版は前の版から変わった地域だけが入れ替わる累積のモザイクなので、版の日付はその地点の撮影日ではない。
- 雲・季節の処理 (モザイクの作り方): Vivid Standard は数千の画像ストリップを色調補正と継ぎ目のブレンドでつないだ連続モザイク (https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9)。雲量の基準や季節の選び方は公表されていない。
- 国内のカバー範囲: 全国を 1 m 以上でおおうかは未確認。上記のとおり東京付近では Vantor の画像と練馬区の航空写真が確認できる。

## 提供形式

- 形式 (XYZ / WMTS / COG / STAC など): ArcGIS の MapServer タイル (`https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`、Web メルカトル (EPSG:3857)、256×256 px の JPEG。https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer?f=json の tileInfo で確認) と WMTS。Location Platform では Basemap Styles service の `arcgis/imagery`、`arcgis/imagery/standard`、`arcgis/imagery/labels` (Mapbox Style Spec v8 のスタイル JSON から参照) (https://developers.arcgis.com/rest/basemap-styles/)。Static Basemap Tiles service は `arcgis/imagery` を含まない (https://developers.arcgis.com/rest/static-basemap-tiles/)。COG と STAC での提供はない (公開文書に記載なし)。
- 最大ズーム: サービスの定義はレベル 0〜23 (https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer?f=json)。実際に画像がある最大ズームは地点で違い、Vantor の画像は場所によってズーム 17 程度まで、コミュニティ提供の航空写真は 20〜23 まである (帰属データより)。
- 対応ライブラリと API キーの要否: 技術的には MapServer のタイル URL はキーなしで取得でき、Leaflet、OpenLayers、MapLibre GL JS のラスタソースで表示できる。ただし規約上、アプリに組み込むには ArcGIS Location Platform または ArcGIS Online のアカウントとトークンを通すのが前提で (下記)、Location Platform はベースマップスタイル経由での利用を想定している (https://location.arcgis.com/help/licensing-and-attribution/)。MapLibre 向けには Esri/maplibre-arcgis (Apache-2.0) がある (https://github.com/Esri/maplibre-arcgis)。

## 料金

- 無料枠と課金単位: ArcGIS Location Platform ではベースマップのタイル (月 200 万タイル無料) かセッション (月 1,000 セッション無料、1 セッション最長 12 時間) で課金される。`arcgis/imagery` も Basemap Styles service のスタイルなのでこの枠に入る (2026-11-10 確認、https://location.arcgis.com/pricing/ 、https://developers.arcgis.com/rest/basemap-styles/)。ArcGIS Online の契約ではタイルはサブスクリプションに含まれる (同)。
- 従量単価・契約形態 (問い合わせ制ならそう書き、金額を推測しない): Location Platform では 1,000 タイルあたり 0.15 USD、または 1,000 セッションあたり 4.0 USD (2026-11-10 確認、https://developers.arcgis.com/rest/basemap-styles/)。月次の従量課金でセルフサーブ (https://location.arcgis.com/help/billing/)。Living Atlas のレイヤを自前のアプリで使うには個別のライセンス契約が要るとされており、その場合の金額は営業への問い合わせ制 (https://location.arcgis.com/help/licensing-and-attribution/)。

## 利用規約上の制約

- 商用利用: Location Platform のベースマップスタイルとしてなら、トークンで認証したうえで収益を得るアプリに使える (Product-Specific Terms E300 脚注 89、https://www.esri.com/content/dam/esrisites/en-us/media/legal/product-specific-terms-of-use/e300.pdf)。Living Atlas のレイヤとして独自のアプリに使う場合は個別のライセンス契約が要る (https://location.arcgis.com/help/licensing-and-attribution/)。データは Esri が提供した製品とだけ使える (Master Agreement 3.2 a)。
- キャッシュ・ダウンロード・二次加工 (解析、学習データ) の可否: スクレイピング、ダウンロード、保存は原則禁止 (Master Agreement 3.2 c)。オフライン用の書き出しは別レイヤ「World Imagery (for Export)」で 1 回 15 万タイルまで、ArcGIS のアプリと ArcGIS Runtime SDK で作ったアプリでのオフライン利用に限る (https://www.arcgis.com/home/item.html?id=226d23f076da478bba4589e7eae95952)。帰属表示つきの静的な画像 (PDF、JPEG など) は可視化目的に限り作成・報告書に載せられる (Master Agreement 3.2 b)。判読してデータを作る (データ収集・編集) ことは ArcGIS のアプリ内で一定の範囲で許されている (https://www.arcgis.com/home/item.html?id=8e90a00a0a6845a49262e0b756f57a10)。第三者向けのデータ集の作成・検証に使うこと (3.3 b) と、Esri の Software と Online Services の外で AI/ML の学習に使うこと (3.3 h) は禁止。ArcGIS Image services の機械的な大量利用 (深層学習、10 MB を超える書き出しなど) も禁止 (E300 脚注 96)。
- 帰属表示の要件: 「Powered by Esri」と、画像の提供元 (サービスの著作権表示は「Esri, Vantor, Earthstar Geographics, and the GIS User Community」) を表示する。表示範囲とズームに応じた提供元は帰属データ API で得られる (https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer?f=json 、https://static.arcgis.com/attribution/World_Imagery?f=json 、https://developers.arcgis.com/documentation/esri-and-data-attribution)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): 画像は Esri の独自ライセンス (Esri Master Agreement) で、オープンライセンスではない。Master Agreement B.1 k は Esri の製品を GPL やオープンデータベースのライセンス条件に服させる形で組み込み・改変・配布・結合することを禁じているので、画像やそこから作ったものを ODbL や CC BY-SA のデータと混ぜて再配布する形は避ける。一部にコミュニティ提供の画像 (例: 練馬区 CC BY 4.0) が含まれるが、帰属データで示される提供元を表示すれば、表示のみ (SaaS で画面に出す) の用途で追加の継承条件はない。Wayback アプリと maplibre-arcgis は Apache-2.0 でコピーレフトはない。

## 向いている場面

- 全球を同じ見た目でつないだ背景用の衛星・航空写真を、ArcGIS Location Platform の月 200 万タイルの無料枠の範囲で表示したい場合。
- 2014 年以降の画像の変化を Wayback で目視で追いたい場合 (災害前後、開発の進み具合の確認など)。
- ArcGIS のネイティブ SDK や ArcGIS Pro でオフライン用の画像を持ち出したい場合。

## 向いていない場面

- 画像を解析する、AI/ML の学習データにする、判読結果を第三者に提供するデータ集にする場合。規約で禁じられている。
- ブラウザアプリ用にタイルを自前でキャッシュ・配信したい場合。
- 撮影日がそろった最新画像が必要な場合や、特定の日付の画像を指定して取得したい場合。モザイクは地点ごとに撮影日が違う。
- 国内の特定地域で解像度や撮影時期の保証が必要な場合。国内の範囲と解像度の一覧が公表されていない。

## プライバシーとテレメトリ (2026-11-14 確認)

- **Esri プラットフォームの扱い**: `esri-arcgis-location-platform` と同様、Esri Products & Services Privacy Statement Supplement の対象であり、API キーによる利用計測が行われる。衛星画像タイルのみを標準 HTTP で取得する場合のエンドユーザー位置テレメトリの有無やネイティブ SDK 利用時の開示項目は、利用形態に応じて [esri-arcgis-location-platform](../providers/esri-arcgis-location-platform.md) とあわせて確認する (画像単体でのログ保持詳細は未確認)。

## 出典

- https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9
- https://www.arcgis.com/sharing/rest/content/items/10df2279f9684e4a9f6a7f08febac2a9?f=json
- https://www.arcgis.com/home/item.html?id=226d23f076da478bba4589e7eae95952
- https://www.arcgis.com/home/item.html?id=8e90a00a0a6845a49262e0b756f57a10
- https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer
- https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer?f=json
- https://static.arcgis.com/attribution/World_Imagery?f=json
- https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json
- https://livingatlas.arcgis.com/wayback/
- https://github.com/Esri/wayback
- https://github.com/Esri/maplibre-arcgis
- https://developers.arcgis.com/rest/basemap-styles/
- https://developers.arcgis.com/rest/static-basemap-tiles/
- https://developers.arcgis.com/documentation/esri-and-data-attribution
- https://location.arcgis.com/pricing/
- https://location.arcgis.com/help/billing/
- https://location.arcgis.com/help/licensing-and-attribution/
- https://www.esri.com/en-us/legal/terms/full-master-agreement
- https://www.esri.com/content/dam/esrisites/en-us/media/legal/ma-full/ma-full.pdf
- https://www.esri.com/content/dam/esrisites/en-us/media/legal/product-specific-terms-of-use/e300.pdf
- https://goto.arcgis.com/termsofuse/viewsummary
- https://goto.arcgis.com/termsofuse/viewtermsofuse
- https://www.esri.com/about/newsroom/announcements/esri-expands-world-imagery-with-airbus-high-resolution-basemap-coverage-for-2000-cities-worldwide
- https://newshub.medianet.com.au/2026/08/esri-expands-world-imagery-with-airbus-high-resolution-basemap-coverage-for-2000-cities-worldwide/167393/
- https://www.esri.com/arcgis-blog/products/arcgis-living-atlas/imagery/whats-new-in-world-imagery-july-2026

## 未確認のこと

- Airbus 30 cm 画像の対象都市、日本が入るか、World Imagery への反映時期: Esri の発表に都市一覧がなく、2026-11-10 時点の帰属データに Airbus がまだない。esri.com の発表本文とブログ (2026 年 7 月の World Imagery 更新記事) は機械取得が 403 で拒否され、転載記事と検索結果の抜粋で確かめた。
- 国内の解像度と撮影時期の分布: 公表資料がない。帰属データで東京付近を引いた範囲しか確かめていない。
- 雲量の基準と季節の選び方: 公表されていない。
- キーなしの MapServer タイル URL を Esri 製品以外のアプリで直接使うことの可否: Master Agreement 3.2 a と Location Platform の説明 (Living Atlas のレイヤは個別契約) から認められないと読むのが自然だが、明文で直接触れた条項は見つけていない (推測)。
