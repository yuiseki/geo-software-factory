# 観測した地図サービスのカード

公開されている地図サービスを、ヘッドレスのブラウザで 1 回ずつ開き、外から見えた技術 (描画のライブラリ、フレームワーク、背景の地図とタイル、投稿やデータの保存先、配信) を 1 サービス 1 枚のカードにしたもの。似たサービスを探すとき (SKILL.md の手順 3、4) は、まずここを見て、同じサービスを調べ直さない。

## 読むときの注意

- どのカードも 2026-11-11 の観測で、その後に作りが変わっていることがある。結論に使う前に、そのサービスを開き直す
- 外から見えた範囲だけを書いている。運営者の資料は読んでいない。「見つからなかった」は「使っていない」ではない (1 つにまとめた JavaScript の中や、別のページにある地図は見えない)
- 描画のライブラリは、ページの DOM (`maplibregl-map` などのクラス) と、読み込んだ JavaScript の中の文字列で判定した。版は JavaScript の中に版の文字列が見えたときだけ書いた
- 配信は応答ヘッダー (`server`、`cf-ray`、`x-vercel-id`、`x-github-request-id`、`x-amz-cf-id` など) で判定した。Cloudflare はプロキシとして前に置かれるので、その後ろの配信元は分からないことがある
- 背景の地図は、読み込んだタイルとスタイルの通信先で判定した
- 開けなかったもの (2026-11-11): historydraft.com (403)、ワールドトレインマップ (403)、platinumaps (403)、思い出地図 (名前を引けなかった)

## 一覧

| カード | 描画 | 背景の地図とタイル | 配信 |
|---|---|---|---|
| [adsb.lol, unfiltered flight tracking](adsblol.md) | OpenLayers | - | Istio (Kubernetes) の後ろ |
| [クマ遭遇AI予測マップ｜上智大学 深澤研究室](bear-ai.md) | - | - | GitHub Pages |
| [浸水センサ表示システム（国土交通省）](c-sensor.md) | OpenLayers | 地理院タイル、自前のタイル (サイトと同じドメイン) | CloudFront 経由 (nginx/1.14.1) |
| [Custom Sydney Maps - Floor Plans On A Map](castlemap.md) | - | 自前のタイル (サイトと同じドメイン) | Apache/2.4.58 (Ubuntu) (配信先の事業者は不明) |
| [全国地番マップ｜公図（法務局地図）・地番図を全国で検索・ダウンロード](chiban.md) | MapLibre GL JS | 地理院タイル、Geolonia (フォントのグリフ)、自前のタイル (サイトと同じドメイン) | Cloudflare |
| [ChizuZu - 地図比較アプリ](chizuzu.md) | Leaflet | OSM 財団の公開タイル | Cloudflare |
| [CSTB Japan and NW Pacific 2026](cstb.md) | Leaflet 1.9.4 | 自前のタイル (サイトと同じドメイン) | Cloudflare |
| [方位図法世界地図作成ツール](cubbit.md) | Google Maps JavaScript API | - | Cloudflare |
| [ダジック・アース - ダジック・アース](dagik.md) | - | - | Cloudflare |
| [DeFlock Maps ｜ ALPR Camera Map & Privacy Routes](deflock.md) | MapLibre GL JS | 下の URL のタイル (配信元は分類していない) | Cloudflare |
| [Flight Atlas](flightatlas.md) | MapLibre GL JS 5.24.0 | OpenFreeMap | GitHub Pages |
| [Flock camera map: Find the Flock cameras watching you ｜ Proton](flock.md) | MapLibre GL JS | OpenFreeMap | 不明 (応答ヘッダーに手がかりが無い) |
| [🍽️ Japan Food Facilities - 地図](food-facilities.md) | MapLibre GL JS | 地理院タイル | GitHub Pages |
| [Hail Mary - Star Map](gaia-mary.md) | - | - | GitHub Pages |
| [GeoConfirmed - Open-Source Conflict Geolocation & Verification](geoconfirmed.md) | MapLibre GL JS | OpenFreeMap、自前のタイル (サイトと同じドメイン) | Cloudflare |
| [GeoLens: Open-Source Geospatial Data Catalog & Map Builder](geolens.md) | - | - | Cloudflare |
| [Global Threat Map ｜ Intelligence Platform](globalthreatmap.md) | Mapbox GL JS | Mapbox | Railway |
| [ゴミ箱マップ ｜ 街中のゴミ箱情報をシェアしよう！](gomibako.md) | Leaflet | OSM 財団の公開タイル、Mapbox の API への通信 (用途は未確認) | nginx (配信先の事業者は不明) |
| [印刷地図作成ツール - 移転のお知らせ](gpxmapprint.md) | - | - | nginx (配信先の事業者は不明) |
| [電力系統マップ - Electrical Grid Map](grid.md) | - | - | Cloudflare |
| [3次元地図可視化サイト](gsi-3d.md) | MapLibre GL JS | 地理院タイル | GitHub Pages |
| [点群PNGタイルの実例](gsj-pcpng.md) | - | - | Amazon S3 + CloudFront |
| [どこでも北海道マップ](hokkaido-map.md) | Leaflet | OSM 財団の公開タイル | GitHub Pages |
| [探す｜今からほんや](imahon.md) | MapLibre GL JS 5.6.0 | OpenFreeMap | Cloudflare |
| [【推し活カフェ】日本最大級の推し活・コラボカフェ検索 ｜ imako推し活カフェ](imako.md) | - | - | Cloudflare |
| [自分のサーバーで日本地図を表示する｜Japan PMTiles](japan-pmtiles.md) | MapLibre GL JS | OpenStreetMap Japan のタイル、自前のタイル (サイトと同じドメイン) | nginx (配信先の事業者は不明) |
| [防災インタフェース](jaxa-bousai.md) | - | - | volt-adc (配信先の事業者は不明) |
| [JP Market Vis - 日本の上場企業マップ](jp-market-vis.md) | - | - | GitHub Pages |
| [ライブハウス検索マップ - JVMAP｜全国の音楽会場を地図で探す](jvmap.md) | MapLibre GL JS | CARTO basemaps | Vercel |
| [令和8年熊本地震関連情報 - 紙マップ](kamimap.md) | MapLibre GL JS、Mapbox GL JS | OpenStreetMap Japan のタイル | GitHub Pages |
| [全球大気の流れ、寒気・暖気の状況：2026年10月25日12UTC ｜ 気温のページ ｜ 気温データから地球大気を見る](kion.md) | Google Maps JavaScript API | Google Maps Platform | nginx (配信先の事業者は不明) |
| [国会議員マップ - あなたに近い議員がわかる](kokkaimap.md) | - | - | Vercel |
| [国道マップ](kokudo-map.md) | MapLibre GL JS | 地理院タイル、自前のタイル (サイトと同じドメイン) | Cloudflare 経由の GitHub Pages |
| [避難施設のご案内](kokuminhogo.md) | ゼンリンデータコムの地図 API | - | Amazon S3 + CloudFront |
| [こにゃーきんぐ](konyaking.md) | MapLibre GL JS 4.7.1、Leaflet | OpenFreeMap | GitHub Pages |
| [熊出没マップ2026年 - 全国165,975件 - クママップ](kumamap.md) | - | - | Cloudflare |
| [熊本地震（2026-07-28）支援拠点マップ](kumamoto-ai.md) | Leaflet | OSM 財団の公開タイル | GitHub Pages |
| [令和8年熊本地震 生活支援・被害状況マップ｜給水所・避難所・断水](kumamoto-sagri.md) | Leaflet | 地理院タイル、自前のタイル (サイトと同じドメイン) | Cloudflare |
| [くまっぷ - クマ目撃・痕跡情報を共有するマップアプリ](kumap-xenon.md) | Leaflet | OSM 財団の公開タイル | 不明 (応答ヘッダーに手がかりが無い) |
| [東京終電マップ｜TOKYO LAST TRAIN MAP](last-train.md) | - | - | Cloudflare |
| [ラズリマップ｜図面から、測る手間を消す](lazuri.md) | MapLibre GL JS | 地理院タイル、自前のタイル (サイトと同じドメイン) | Fly.io |
| [LivMap (リブマップ) - チームで使う共有地図](livmap.md) | - | - | Cloudflare |
| [Map Studio](map-enoki.md) | - | - | Vercel |
| [地図マピオン（Mapion）｜地図検索/ルート検索/天気予報](mapion.md) | - | - | CloudFront 経由 (nginx) |
| [近くの安いマックがわかる｜マクドナルド価格帯マップ](mcd-pricemap.md) | Leaflet | CARTO basemaps | Cloudflare |
| [MeshMap - Meshtastic Node Map](meshmap.md) | Leaflet | OSM 財団の公開タイル | Cloudflare |
| [Interactive Middle-earth Map - LOTR, Hobbit & Silmarillion](middle-earth.md) | Leaflet | 自前のタイル (サイトと同じドメイン) | 不明 (応答ヘッダーに手がかりが無い) |
| [みんなの行政地図](minchizu.md) | - | - | LiteSpeed (配信先の事業者は不明) |
| [みんなでつくる全国冠水道路マップ｜みんつく全国冠水マップ](mintsuku.md) | MapLibre GL JS 6.6.0 | Protomaps (フォントとスプライト)、自前のタイル (サイトと同じドメイン) | Cloudflare |
| [Mobility Maps: Making Public Transport Infrastructure Transparent](mobility.md) | MapLibre GL JS 5.0.1、deck.gl | - | nginx/1.29.8 (配信先の事業者は不明) |
| [THE MODAL EARTH - 旋法の地球儀｜世界35の旋法を、本当の音程で聴き比べる ｜ Música Terra PLAYGROUND](modalearth.md) | three.js | - | nginx (配信先の事業者は不明) |
| [Monitor the Situation ｜ Live World News Map & OSINT Dashboard](monitor-situation.md) | MapLibre GL JS | 自前のタイル (サイトと同じドメイン) | Cloudflare |
| [名字マップ](myojimap.md) | Leaflet 1.6.0 | MIERUNE | Amazon S3 + CloudFront |
| [Navara, an open-source 3D map engine](navara.md) | - | - | Cloudflare |
| [withfs ニュースマップ｜ニュースの舞台を地図で俯瞰する ｜ withfs](newsmap.md) | - | Google Maps Platform | Google (Blogger) |
| [電界強度マップ - 電磁環境研究室モニタリングプロジェクト](nict-emc.md) | - | Esri (ArcGIS) のベースマップ | Apache (配信先の事業者は不明) |
| [earth :: a global map of wind, weather, and ocean conditions](nullschool.md) | - | - | Cloudflare |
| [Open Infrastructure Map](openinframap.md) | MapLibre GL JS | 自前のタイル (サイトと同じドメイン) | Cloudflare |
| [OsmAnd Map](osmand.md) | Leaflet | OsmAnd のタイル、自前のタイル (サイトと同じドメイン) | nginx/1.18.0 (Ubuntu) (配信先の事業者は不明) |
| [国勢調査 メッシュ年齢構成クラスターマップ](popbalance.md) | MapLibre GL JS | 地理院タイル、自前のタイル (サイトと同じドメイン) | GitHub Pages |
| [全国農業用ため池マップについて ｜ 全国Q地図](qchizu-pond.md) | - | - | Cloudflare |
| [Rennes Transit Map - Visualisation temps réel du réseau STAR](rennes-transit.md) | MapLibre GL JS | data.gouv.fr の OpenMapTiles | GitHub Pages |
| [令和８年千葉連続風水害 復旧・復興アーカイブ ｜ Ri2MAPS](ri2maps.md) | Leaflet 1.9.4 | 地理院タイル | Apache (配信先の事業者は不明) |
| [全国のトレランコースと大会コース｜Runnable](runnable.md) | MapLibre GL JS | 地理院タイル | Vercel |
| [裁判官マップ - 日本地図から裁判官を探す ｜ 裁判官マップ](saibankan.md) | - | - | Cloudflare |
| [おでかけ航路マップ ｜ 日本全国の旅客船・フェリー航路情報と時刻表リンク](searoute.md) | MapLibre GL JS | OpenStreetMap Japan のタイル、Protomaps (フォントとスプライト)、自前のタイル (サイトと同じドメイン) | Cloudflare |
| [せんべろ東京マップ（東京都内の立ち飲み・大衆酒場・居酒屋を地図から検索） ｜ せんべろnet](senbero.md) | Google Maps JavaScript API | Google Maps Platform | nginx (配信先の事業者は不明) |
| [showhand - 全晒しAI不動産周辺マップ](showhand.md) | - | - | Vercel |
| [SNS災害情報集約マップAI](solafune-alert.md) | MapLibre GL JS | 地理院タイル | Amazon S3 + CloudFront |
| [THE SOUNDING EARTH](sounding-earth.md) | three.js | 使っていない (4K の地球の画像を three.js の球に貼り、文化圏を塗った画像を重ねる) | nginx (静的な配信) |
| [世界のライブカメラ地図｜いま見れるライブ映像 - たま旅ライブ](tamatabi.md) | MapLibre GL JS 4.7.1、D3 | OpenFreeMap | Vercel |
| [TokyoMap（東京都地図情報サイト）](tokyomap.md) | Google Maps JavaScript API | Google Maps Platform | Amazon S3 + CloudFront |
| [日本のライブカメラ地図 ｜ とまり木](tomarigi.md) | Leaflet | 地理院タイル | Cloudflare |
| [Trip Planner 山行計画サポートマップ｜日本雪崩ネットワーク](tripplanner.md) | - | - | Cloudflare |
| [uMap - Online map creator](umap.md) | Leaflet | OSM 財団の公開タイル、OpenStreetMap France のタイル、Esri (ArcGIS) のベースマップ、OpenTopoMap、自前のタイル (サイトと同じドメイン) | nginx/1.31.6 (配信先の事業者は不明) |
| [Urbanist Map](urbanistmap.md) | MapLibre GL JS | OpenFreeMap | Cloudflare |
| [USOMAP - 架空世界地図ジェネレーター｜無料の地図メーカー](usomap.md) | three.js | - | Cloudflare |
| [Trump Deadline Countdown ｜ CENTCOM Theater Operations Map ｜ US vs Iran Force Tracker](usvsiran.md) | Leaflet | CARTO basemaps | Cloudflare |
| [V2X2MAP - live receiver and map for ITS-G5 / V2X](v2x2map.md) | - | - | Cloudflare |
| [WAR 3.0 - Live World War 3 Heat Map & Real-Time Conflict Tracker](warheatmap.md) | MapLibre GL JS 4.7.1 | Esri (ArcGIS) のベースマップ | Cloudflare |
| [Interactive Map (WebMCP)](webmcp-gmap.md) | Google Maps JavaScript API | Google Maps Platform | Cloudflare |
| [非公式 山岡家 Map](yamaokaya.md) | MapLibre GL JS | Amazon Location Service | Amazon S3 + CloudFront |
| [気象衛星とレーダーマップ ｜ Zoom Earth](zoomearth.md) | - | 自前のタイル (サイトと同じドメイン) | Cloudflare |

## カードを足すとき

1 サービス 1 ファイルで、ファイル名はサービスを表す短い英字にする。項目は既存のカードと揃える (描画、フレームワーク、背景の地図とタイル、投稿やデータの保存先、配信)。観測した日を必ず書き、見えなかったものは「見つからなかった」「見えなかった」と書いて推測で埋めない。推測を書くときは (推測) と付ける。足したらこの一覧に 1 行足す。
