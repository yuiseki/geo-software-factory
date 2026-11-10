# 特定の要件でだけ候補になるタイル・データ

確かめた日: 2026-11-10

比較表に毎回並べるほどではないが、特定の要件ではそれでしか実現できない、または選ばざるを得ないもの。要件に当てはまるときだけ候補に加える。

| 名前 | 種別 | それでしか実現できないこと / 選ぶ事情 | 提供状況 | ライセンス・利用条件 (コピーレフトや商用禁止の注意を含む) | 料金の概略 | 出典 |
|---|---|---|---|---|---|---|
| 地理院 最適化ベクトルタイル | 国のベクトルタイル (MVT、PMTiles 版と z/x/y 版) | 数値地図 (国土基本情報) を元にした国内全域のベクトルタイルを、地理院地図と同じ内容でスタイルを変えて使える。ズームは 4〜16 で、17 は 16 をオーバーズームする | 2022-09-06 からの「試験公開」で、基本測量成果ではない。URL、データ構成、属性は変わりうると明記されている。PMTiles 版のデータは 2026-07-01 時点 | 国土地理院コンテンツ利用規約に従う。「国土地理院最適化ベクトルタイル」などの出典明示が要る | 料金の記載は無い | [optimal_bvmap](https://github.com/gsi-cyberjapan/optimal_bvmap) |
| 重ねるハザードマップのタイル | 国のラスタタイル (PNG、地理院タイル準拠、WMTS メタデータあり) | 洪水、内水、高潮、津波の浸水想定と土砂災害警戒区域、雪崩危険箇所を、全国で共通の URL と凡例で重ねられる | 配信中。ただし多くのデータは都道府県や市町村ごとに一部だけ配信で、ズームもデータごとに異なる | 商用・非商用を問わず利用できる。出典の書き方は指定どおりにする。土砂災害のデータは国土数値情報の利用規約と各都道府県の利用条件への同意が要る | 料金の記載は無い | [オープンデータ](https://disaportal.gsi.go.jp/hazardmapportal/hazardmap/copyright/opendata.html) |
| Thunderforest | OSM 由来のラスタタイル API | OpenCycleMap、Transport、Outdoors など、自転車道や公共交通、登山道を強調した既製のスタイル | 商用サービスとして提供中 | 地図画像は CC BY-SA 4.0、データは ODbL。Thunderforest と OpenStreetMap の帰属表示はどのプランでも外せない。キャッシュプロキシでの再配布は禁止、一括ダウンロードは Small Business 以上 | 月額 Hobby 無料 (15 万タイル)、Solo $125、Small Business $255、Large Business $525 (USD、税別、2026-11-10) | [pricing](https://www.thunderforest.com/pricing/)、[terms](https://www.thunderforest.com/terms/) |
| Geoapify | OSM 由来の地図タイル、ジオコーディング、ルート、到達圏などの API | 到達圏 (isochrone)、ルート、場所検索を 1 つのクレジット制でまとめて使える | 商用サービスとして提供中 | 無料プランも本番の商用利用ができるが、Geoapify と出典データの帰属表示が要る。OSM の帰属表示はどのプランでも要る | 月額 Free (1 日 3,000 クレジット)、$59〜$609、Custom は $860 から (USD、2026-11-10) | [pricing](https://www.geoapify.com/pricing/)、[terms](https://www.geoapify.com/terms-and-conditions/) |
| NAVITIME API | 地図表示、ルート検索、乗換検索の API | 国内の公共交通の乗換と徒歩を組み合わせたドアツードアのルート、大型車規制を考慮した車ルート、配車・巡回ルート | 直接契約、RapidAPI、SBI の API Hub で提供中。API マーケット経由は基本機能のみで、技術サポートは無い | 契約による。条件は公開ページで確かめていない (未確認) | 直接契約は初期費用と月間アクセス数による個別見積もりで、90 日の無料試用がある。RapidAPI の無料枠は 500 アクセス、有料プランの金額は未確認 | [NAVITIME API](https://api-sdk.navitime.co.jp/api/) |
| YOLP (Yahoo! Open Local Platform) | 検索・ジオコーディング系の Web API | 国内のローカルサーチ、住所ディレクトリ、施設内検索、気象 (降水強度) | 提供中。2026-11-10 時点の API 一覧に地図表示の API は無い。2022-06-30 にルート沿い検索 API とカセットサーチ API が終了 | 1 アプリ 1 日 5 万リクエストまで。社内ネットワーク内のサービス、利益を得ていると認められるサービス、キャッシュを含む保存などは禁止で、有償版 YOLP Premier が要る | 無料版の料金は無い。YOLP Premier は金額の公開が無い (未確認) | [YOLP](https://developer.yahoo.co.jp/webapi/map/)、[2022-05-13 お知らせ](https://developer.yahoo.co.jp/changelog/2022-05-13-map.html) |
| OpenTopoMap | OSM と SRTM 由来の地形図風ラスタタイル | 等高線と陰影入りの地形図を無料で重ねられる | 有志が運営。2026-01-05 に描画サーバーを小さい vServer へ移した。可用性の保証は無い | CC BY-SA で、派生物は同じ条件で共有する必要がある。商用利用も可でライセンス料は無いが、一括ダウンロードなどでサーバーに負荷をかけない | 無料 (寄付は受けていない) | [about](https://opentopomap.org/about) |
| OpenRailwayMap | OSM 由来の鉄道のラスタタイル (重ね合わせ用) | 線路、駅、信号、最高速度、電化方式、軌間を示す鉄道専用レイヤー | 有志が運営。サポートと可用性の保証は無い | タイルは CC BY-SA 2.0、データは ODbL。営利目的で使うなら自前サーバーを立てるよう求めており、商用や非公開のプロジェクトは予告なく遮断されうる。利用側アプリは無料かつ登録不要で公開されている必要がある。一括取得は禁止 | 無料 (小規模な利用に限る) | [OpenRailwayMap/API](https://wiki.openstreetmap.org/wiki/OpenRailwayMap/API) |
| 今昔マップ | 旧版地形図のラスタタイル (TMS) | 明治以降の旧版地形図を時期別に現在の地図と重ねられる | 配信中。2000〜2022 年は谷謙二氏が運営し、その後の更新は遺族の了承を得た「今昔マップ運営委員会」が行っている。ズームは 8〜16 (地域により 15 まで)。y 軸は南西起点 | 画面に「今昔マップ on the web」の文字を入れる必要がある。一般公開時は連絡を求めている。地図は国土地理院長の承認を得て作られており、複製には国土地理院長の承認が要ると記載がある。商用利用の可否は記載が無い (未確認) | 料金の記載は無い | [タイルマップサービス](https://ktgis.net/kjmapw/tilemapservice.html)、[今昔マップ](https://ktgis.net/kjmapw/) |
| Planet | 衛星画像 (PlanetScope、SkySat) とベースマップ | 高頻度で撮り直す衛星画像による変化の把握 | 商用で提供中。熱帯林の画像を無償公開していた NICFI 衛星データプログラムは 2025-01-23 で契約期間が終わった。GEE などで公開されていた NICFI のベースマップは非商用利用に限られていた | 契約 (EULA) による。条件は公開ページで確かめていない (未確認) | 問い合わせ制。Planet Insights Platform に 30 日の無料試用、教育・研究プログラムがある | [contact sales](https://www.planet.com/contact-sales/)、[NICFI](https://www.nicfi.no/2025/01/28/nicfi-satellite-data-program-enters-new-phase/)、[GEE カタログ](https://developers.google.com/earth-engine/datasets/catalog/projects_planet-nicfi_assets_basemaps_africa) |
| Vantor (旧 Maxar) | 高解像度の衛星画像、ベースマップ、3D 地形 | 15cm / 30cm の全球モザイク (Vivid)、3D 地形・地表モデル、ベクトルのベースマップ | 2025-10-01 に Maxar Intelligence が Vantor に改称した。WorldView と Vivid の製品群を引き継ぐ | 契約による。条件は公開ページで確かめていない (未確認) | 問い合わせ制 | [Vantor](https://vantor.com/)、[Washington Technology](https://www.washingtontechnology.com/companies/2025/10/maxars-name-no-more-after-rebrand/408532) |
| Copernicus Data Space Ecosystem | Sentinel 衛星データの配布・処理基盤 (S3、OData、STAC、Sentinel Hub API) | Sentinel-1/2 などを無償で入手し、商用を含めて加工・再配布できる | EU が提供中。登録が要る。無料ユーザーは月 12TB の転送、Sentinel Hub は月 10,000 リクエストなどの上限がある | Sentinel データは EU 法で複製、配布、公衆送信、改変が無償で認められる。配布時は「Copernicus Sentinel data [Year]」(改変時は「Contains modified Copernicus Sentinel data [Year]」) の表示が要る | 無料。上限を超える場合は商用クラウドのクレジットや支援への申請を案内している | [terms](https://dataspace.copernicus.eu/terms-and-conditions)、[Quotas](https://documentation.dataspace.copernicus.eu/Quotas.html)、[Legal Notice](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice) |
| Yandex Maps | 地図 API (JavaScript API など) | ロシアと周辺国の地図・検索の詳しさ | 提供中。利用前に、取引先と自社に適用される制裁 (米 OFAC、EU、日本の外為法など) の確認が要る。ロシアの技術企業として制裁や規制の対象が変わりうる。2022 年に共同創業者が EU の制裁対象になり、2024 年に解除された | 無料の埋め込みは、無料で誰でも使えるサイトやアプリに限られ、有料のプロジェクトには使えない。商用目的の複製や公開は事前の書面許可が要る | Free ライセンスは年 250 万リクエストまで。Basic は年 $13,000 から (USD、2026-11-10) | [JS API](https://yandex.com/maps-api/products/js-api)、[利用規約](https://yandex.ru/legal/maps_termsofuse/)、[ain.ua](https://en.ain.ua/2024/03/13/eu-lifts-sanctions-on-yandex-co-founder-arkady-volozh) |
| 2GIS | 地図 API と SDK (MapGL JS、モバイル、検索、ナビ) | ロシアと CIS の都市の建物入口や施設情報まで含む詳しい地図 | 提供中。ロシア企業なので、利用前に制裁 (米 OFAC、EU、日本の外為法など) の確認が要る。制裁対象かどうかは今回確かめていない (未確認) | デモキーは 1 か月、リクエスト数に上限あり。商用は問い合わせ | 問い合わせ制。金額は未確認 | [dev.2gis.com](https://dev.2gis.com/)、[MapGL JS API](https://docs.2gis.com/en/mapgl/overview) |
| Mappls (MapmyIndia) | インドの地図 SDK、検索、ジオコーディング、ルート API | インドの番地レベルの地図と、インド特有の交通手段を含むルート検索 | 提供中 | インド政府が主張する国境で地図を描く必要があるかを確かめる。インドの刑法改正法 1961 年 2 条 2 項は、Survey of India の地図と一致しないインドの地図を公表した者を 6 か月以下の懲役または罰金 (併科あり) とする。訴追は政府の告発に限る | 「Start for free」の登録はあるが、金額と無料枠は公開ページで確かめられなかった (未確認) | [Mappls API](https://about.mappls.com/api/)、[Criminal Law Amendment Act 1961](https://www.uppolice.gov.in/Site-Content/uploaded-content/pdf/cl_amendment_act_1961.pdf) |
| Longdo Map | タイの地図 API と SDK、オンプレミスの地図サーバー (Longdo Box) | タイ語の地名と施設、タイ国内の検索とルート。閉域網で使うオンプレミス版がある | Metamedia Technology (バンコク) が提供中。SLA で稼働率 99.9% | 一般向けのサービスなら無料枠内で無償。地図ロゴや権利表示を消してはならない。無料利用には将来広告を入れる権利を留保している | 月額 Free (地図 80 万、サービス 10 万トランザクション、1 日 5,000 リクエスト)、Starter 8,250 バーツ〜Premium 27,500 バーツ、Super Power は問い合わせ (THB、2026-11-10) | [pricing](https://map.longdo.com/products/pricing)、[terms](https://map.longdo.com/api/terms/?locale=en)、[products](https://map.longdo.com/products) |

## 出典

- https://github.com/gsi-cyberjapan/optimal_bvmap
- https://disaportal.gsi.go.jp/hazardmapportal/hazardmap/copyright/opendata.html
- https://www.thunderforest.com/pricing/
- https://www.thunderforest.com/terms/
- https://www.geoapify.com/pricing/
- https://www.geoapify.com/terms-and-conditions/
- https://api-sdk.navitime.co.jp/api/
- https://developer.yahoo.co.jp/webapi/map/
- https://developer.yahoo.co.jp/changelog/2022-05-13-map.html
- https://opentopomap.org/about
- https://wiki.openstreetmap.org/wiki/OpenRailwayMap/API
- https://ktgis.net/kjmapw/tilemapservice.html
- https://ktgis.net/kjmapw/
- https://www.planet.com/contact-sales/
- https://www.nicfi.no/2025/01/28/nicfi-satellite-data-program-enters-new-phase/
- https://developers.google.com/earth-engine/datasets/catalog/projects_planet-nicfi_assets_basemaps_africa
- https://vantor.com/
- https://www.washingtontechnology.com/companies/2025/10/maxars-name-no-more-after-rebrand/408532
- https://dataspace.copernicus.eu/terms-and-conditions
- https://documentation.dataspace.copernicus.eu/Quotas.html
- https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice
- https://yandex.com/maps-api/products/js-api
- https://yandex.ru/legal/maps_termsofuse/
- https://en.ain.ua/2024/03/13/eu-lifts-sanctions-on-yandex-co-founder-arkady-volozh
- https://dev.2gis.com/
- https://docs.2gis.com/en/mapgl/overview
- https://about.mappls.com/api/
- https://www.uppolice.gov.in/Site-Content/uploaded-content/pdf/cl_amendment_act_1961.pdf
- https://map.longdo.com/products
- https://map.longdo.com/products/pricing
- https://map.longdo.com/api/terms/?locale=en

## 未確認のこと

- NAVITIME API の直接契約の利用条件と、RapidAPI の有料プランの金額: 公開ページに金額と条件の記載が無い。
- YOLP Premier の料金: 公開ページに金額が無く、問い合わせ制と見られる (推測)。
- 今昔マップのタイルの商用利用の可否: タイルマップサービスのページに記載が無い。「使用上の注意」のページは今回読んでいない。
- Planet と Vantor の利用条件 (EULA) と価格: どちらも問い合わせ制で、契約条件は公開ページから読み取れなかった。NICFI の次の段階が始まったかどうかも、公式の発表を見つけられなかった。
- 2GIS と Yandex の制裁上の現在の扱い: OFAC の SDN リスト、EU の統合リスト、日本の資産凍結等の対象者リストを今回は照合していない。2GIS の料金は公開ページに無い。
- Mappls の料金と無料枠、インドの国境表示に関する Mappls 自身の方針: 公開ページに記載が無く、料金ページは API の紹介ページへ転送された。刑法改正法の条文は州警察が掲載する PDF で読み、India Code の公式版は 403 で取得できなかった。
- 地理院最適化ベクトルタイルと重ねるハザードマップのタイルの利用規約の本文 (測量法に基づく承認が要る場面など): 今回は規約の本文を読んでいない。
