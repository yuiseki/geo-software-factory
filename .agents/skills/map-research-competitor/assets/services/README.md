# 観測した地図サービスのカード

公開されている地図サービスとアプリを、1 サービス 1 枚のカードにしたもの。ウェブはヘッドレスのブラウザで開き、アプリは App Store と Google Play の表示と、運営者の発表を読んだ。似たサービスを探すとき (SKILL.md の手順 3、4) は、まずここを見て、同じサービスを調べ直さない。

各カードは 2 つの節からなる。

- どんなサービスか: 一行で、提供する価値、想定する利用者、商用か非商用か、推定の売上、運営、推定の運用費。似たサービスと比べて、作るかどうか、何で違いを出すかを決める材料
- 技術: 種類 (ウェブ、アプリ)、描画のライブラリ、フレームワーク、背景の地図とタイル、投稿やデータの保存先、配信。後の段階 (arch、infra、library) の参考。アプリはストアの表示 (販売元、価格とアプリ内課金、評価の数、ダウンロード数、初出と最新の更新) も書く

## 読むときの注意

- 技術は 2026-11-11 (2026-11-12 に足した 13 枚は 2026-11-12)、どんなサービスかは 2026-11-12 の観測で、その後に作りが変わっていることがある。結論に使う前に、そのサービスを開き直す
- 外から見えた範囲だけを書いている。どんなサービスかは、トップページと、運営者、料金、寄付、特定商取引法の表記のページ (見つかったものだけ) を読んで書いた。「見つからなかった」は「使っていない」ではない (1 つにまとめた JavaScript の中や、別のページにある地図は見えない)
- 描画のライブラリは、ページの DOM (`maplibregl-map` などのクラス) と、読み込んだ JavaScript の中の文字列で判定した。版は JavaScript の中に版の文字列が見えたときだけ書いた
- 配信は応答ヘッダー (`server`、`cf-ray`、`x-vercel-id`、`x-github-request-id`、`x-amz-cf-id` など) で判定した。Cloudflare はプロキシとして前に置かれるので、その後ろの配信元は分からないことがある
- 背景の地図は、読み込んだタイルとスタイルの通信先で判定した
- 寄付も商用に含める。広告、有料プラン、アプリの課金、寄付、本業への集客 (企業の宣伝) のどれかが見えたら商用とした。見えなかったものは「非商用と見られる」とし、断定していない
- 売上と運用費は、運営者が公表していればその数字と出どころを書いた (例: [国会議員マップ](kokkaimap.md))。公表していなければ「推測」と書き、根拠 (広告の有無、はてなブックマークの件数、配信の構成) を添えた。推測の金額は桁の目安で、確かめた値ではない
- 運用費の推測は、技術の節で見えた構成から積み上げた。静的配信 (GitHub Pages、Cloudflare Pages) と無料のタイル (地理院タイル、OpenFreeMap) は 0 円、Google Maps JavaScript API は月 1 万ロードを超えると 1,000 回あたり 7 USD、Mapbox GL JS は月 5 万ロードまで無料 (単価は [map-compare-infra の providers](../../../map-compare-infra/references/providers/) の 2026-11-10 の値)。人の時間と開発の費用は含めていない
- はてなブックマークの件数は、カードの URL そのものへのブックマークの数 (2026-11-12、はてなブックマークの件数取得 API)。別の URL へのブックマークは数えていないので、話題の大きさの目安にとどまる
- アプリは端末で開いていない。描画のライブラリ、地図のデータ、通信先は「未確認」とし、ストアの説明と運営者の発表に書かれたことだけを書いた。確かめるには、端末でアプリのオープンソースのライセンスの一覧と通信を見る
- ストアの数字の読み方: App Store の評価の数は日本のストアの数、Google Play のダウンロード数は世界の数で「500万+」のように区切りの下限しか出ない。Google Play の「広告を含む」の表示は、ページの HTML からは取れなかったので書いていない
- 開けなかったもの (2026-11-11): historydraft.com (403)、ワールドトレインマップ (403)、platinumaps (403)、思い出地図 (名前を引けなかった)

## 一覧

「運営」と「商用か」は、カードの欄の括弧の前だけを抜いたもの。根拠と金額はカードを読む。

| カード | 種類 | 運営 | 商用か | 描画 | 配信 |
|---|---|---|---|---|---|
| [adsb.lol, unfiltered flight tracking](adsblol.md) | ウェブ | 個人 | 商用 | OpenLayers | Istio (Kubernetes) の後ろ |
| [Appleマップ](apple-maps.md) | アプリ | 企業 | 非商用と見られる | - | App Store |
| [クマ遭遇AI予測マップ｜上智大学 深澤研究室](bear-ai.md) | ウェブ | 大学の研究室 | 非商用 | - | GitHub Pages |
| [バスNAVITIME 時刻表&乗り換え案内&路線図ナビ](bus-navitime.md) | アプリ | 企業 | 商用 | - | App Store、Google Play |
| [浸水センサ表示システム（国土交通省）](c-sensor.md) | ウェブ | 公的機関 | 非商用 | OpenLayers | CloudFront 経由 (nginx/1.14.1) |
| [Custom Sydney Maps - Floor Plans On A Map](castlemap.md) | ウェブ | 個人 | 商用と見られる | - | Apache/2.4.58 (Ubuntu) (配信先の事業者は不明) |
| [全国地番マップ｜公図（法務局地図）・地番図を全国で検索・ダウンロード](chiban.md) | ウェブ | 団体 | 商用 | MapLibre GL JS | Cloudflare |
| [ChizuZu - 地図比較アプリ](chizuzu.md) | ウェブ | 個人と見られる | 非商用 | Leaflet | Cloudflare |
| [JR東海道本線（東京〜熱海）｜吉田初三郎風・鳥瞰路線図](chokanzu.md) | ウェブ | 個人 | 非商用と見られる | - | Cloudflare |
| [CoMaps](comaps.md) | アプリ | 団体 | 商用 | 自前の C++ の地図エンジン (Organic Maps から分かれた) | App Store、Google Play |
| [CSTB Japan and NW Pacific 2026](cstb.md) | ウェブ | 個人と見られる | 非商用 | Leaflet 1.9.4 | Cloudflare |
| [方位図法世界地図作成ツール](cubbit.md) | ウェブ | 個人 | 非商用 | Google Maps JavaScript API | Cloudflare |
| [ダジック・アース - ダジック・アース](dagik.md) | アプリとウェブ | 団体と大学 | 非商用 | - | Cloudflare |
| [DeFlock Maps ｜ ALPR Camera Map & Privacy Routes](deflock.md) | ウェブ | 団体 | 非商用と見られる | MapLibre GL JS | Cloudflare |
| [Dokoka - 矢印だけの散歩ナビ](dokoka.md) | アプリ | 個人 | 非商用 | - | App Store、Google Play |
| [Every Door](everydoor.md) | アプリ | 個人 | 非商用と見られる | flutter_map と vector_map_tiles | App Store、Google Play |
| [Flight Atlas](flightatlas.md) | ウェブ | 個人 | 非商用 | MapLibre GL JS 5.24.0 | GitHub Pages |
| [Flock camera map: Find the Flock cameras watching you ｜ Proton](flock.md) | ウェブ | 企業 | 商用 | MapLibre GL JS | 不明 (応答ヘッダーに手がかりが無い) |
| [🍽️ Japan Food Facilities - 地図](food-facilities.md) | ウェブ | 団体か個人 | 非商用と見られる | MapLibre GL JS | GitHub Pages |
| [Hail Mary - Star Map](gaia-mary.md) | ウェブ | 個人 | 非商用 | - | GitHub Pages |
| [GeoConfirmed - Open-Source Conflict Geolocation & Verification](geoconfirmed.md) | ウェブ | 団体 | 非商用と見られる | MapLibre GL JS | Cloudflare |
| [GeoLens: Open-Source Geospatial Data Catalog & Map Builder](geolens.md) | ウェブ | 団体 | 非商用 | - | Cloudflare |
| [ジオクエ-写真を撮ってポイントに！ポイ活アプリ](geoquest.md) | アプリ | 企業 | 商用 | - | App Store、Google Play |
| [Global Threat Map ｜ Intelligence Platform](globalthreatmap.md) | ウェブ | 未確認 | 商用と見られる | Mapbox GL JS | Railway |
| [God's Eye View ｜ Official Site: Real-Time 3D Globe](godseyeview.md) | ウェブ | 企業 | 商用と見られる | - | Cloudflare |
| [ゴミ箱マップ ｜ 街中のゴミ箱情報をシェアしよう！](gomibako.md) | ウェブ | 個人と見られる | 商用 | Leaflet | nginx (配信先の事業者は不明) |
| [Google マップ](google-maps.md) | アプリ | 企業 | 商用 | - | App Store、Google Play |
| [印刷地図作成ツール - 移転のお知らせ](gpxmapprint.md) | ウェブ | 個人と見られる | 非商用と見られる | - | nginx (配信先の事業者は不明) |
| [電力系統マップ - Electrical Grid Map](grid.md) | ウェブ | 個人と見られる | 非商用と見られる | - | Cloudflare |
| [3次元地図可視化サイト](gsi-3d.md) | ウェブ | 公的機関 | 非商用 | MapLibre GL JS | GitHub Pages |
| [地理院ルートビルダー｜峠名がわかる自転車ルート作成（GPX無料）](gsi-routebuilder.md) | ウェブ | 個人と見られる | 商用 | Leaflet | nginx (配信先の事業者は不明) |
| [点群PNGタイルの実例](gsj-pcpng.md) | ウェブ | 公的機関 | 非商用 | - | Amazon S3 + CloudFront |
| [どこでも北海道マップ](hokkaido-map.md) | ウェブ | 個人と見られる | 非商用 | Leaflet | GitHub Pages |
| [本コレ](honcolle.md) | アプリ | 企業 | 商用 | - | App Store、Google Play |
| [探す｜今からほんや](imahon.md) | ウェブ | 個人 | 非商用と見られる | MapLibre GL JS 5.6.0 | Cloudflare |
| [【推し活カフェ】日本最大級の推し活・コラボカフェ検索 ｜ imako推し活カフェ](imako.md) | アプリとウェブ | 企業 | 商用 | - | Cloudflare |
| [自分のサーバーで日本地図を表示する｜Japan PMTiles](japan-pmtiles.md) | ウェブ | 個人 | 非商用 | MapLibre GL JS | nginx (配信先の事業者は不明) |
| [防災インタフェース](jaxa-bousai.md) | ウェブ | 公的機関 | 非商用 | - | volt-adc (配信先の事業者は不明) |
| [日本地図の陣とりバトル](jintori.md) | ウェブ | 個人と見られる | 非商用と見られる | - | nginx/1.24.0 (Ubuntu) (配信先の事業者は不明) |
| [JP Market Vis - 日本の上場企業マップ](jp-market-vis.md) | ウェブ | 個人 | 非商用 | - | GitHub Pages |
| [ライブハウス検索マップ - JVMAP｜全国の音楽会場を地図で探す](jvmap.md) | ウェブ | 企業 | 商用 | MapLibre GL JS | Vercel |
| [KAKUNIN MAP](kakunin-map.md) | アプリ | 企業 | 非商用と見られる | - | App Store、Google Play |
| [令和8年熊本地震関連情報 - 紙マップ](kamimap.md) | ウェブ | 団体 | 非商用 | MapLibre GL JS、Mapbox GL JS | GitHub Pages |
| [県境王｜KSKだぜGAMES](kenkyo.md) | ウェブ | 個人と見られる | 非商用と見られる | - | Cloudflare |
| [全球大気の流れ、寒気・暖気の状況：2026年10月25日12UTC ｜ 気温のページ ｜ 気温データから地球大気を見る](kion.md) | ウェブ | 個人 | 商用 | Google Maps JavaScript API | nginx (配信先の事業者は不明) |
| [国会議員マップ - あなたに近い議員がわかる](kokkaimap.md) | ウェブ | 個人 | 商用 | - | Vercel |
| [国道マップ](kokudo-map.md) | ウェブ | 個人 | 非商用 | MapLibre GL JS | Cloudflare 経由の GitHub Pages |
| [避難施設のご案内](kokuminhogo.md) | ウェブ | 公的機関 | 非商用 | ゼンリンデータコムの地図 API | Amazon S3 + CloudFront |
| [こにゃーきんぐ](konyaking.md) | ウェブ | 個人か有志 | 非商用 | MapLibre GL JS 4.7.1、Leaflet | GitHub Pages |
| [熊出没マップ2026年 - 全国165,975件 - クママップ](kumamap.md) | アプリとウェブ | 個人か小さなチーム | 商用 | - | Cloudflare |
| [熊本地震（2026-07-28）支援拠点マップ](kumamoto-ai.md) | ウェブ | 個人 | 非商用 | Leaflet | GitHub Pages |
| [令和8年熊本地震 生活支援・被害状況マップ｜給水所・避難所・断水](kumamoto-sagri.md) | ウェブ | 企業 | 非商用 | Leaflet | Cloudflare |
| [くまっぷ - クマ目撃・痕跡情報を共有するマップアプリ](kumap-xenon.md) | ウェブ | 企業 | 商用と見られる | Leaflet | 不明 (応答ヘッダーに手がかりが無い) |
| [東京終電マップ｜TOKYO LAST TRAIN MAP](last-train.md) | ウェブ | 個人と見られる | 非商用と見られる | - | Cloudflare |
| [ラズリマップ｜図面から、測る手間を消す](lazuri.md) | ウェブ | 企業 | 商用と見られる | MapLibre GL JS | Fly.io |
| [LivMap (リブマップ) - チームで使う共有地図](livmap.md) | アプリとウェブ | 企業 | 商用 | - | Cloudflare |
| [Map Studio](map-enoki.md) | ウェブ | 個人と見られる | 非商用 | - | Vercel |
| [MapComplete](mapcomplete.md) | ウェブ | 個人 | 非商用と見られる | MapLibre GL JS | Caddy (配信先の事業者は不明) |
| [Mapillary](mapillary.md) | アプリとウェブ | 企業 | 非商用と見られる | ウェブ: Mapillary JS (自社の OSS。トップページでは地図を開いていない) | App Store、Google Play。ウェブの画像は fbcdn.net |
| [地図マピオン（Mapion）｜地図検索/ルート検索/天気予報](mapion.md) | アプリとウェブ | 企業 | 商用 | - | CloudFront 経由 (nginx) |
| [Maply](maply.md) | アプリ | 企業 | 商用と見られる | - | App Store |
| [オフライン地図、GPSナビ:MAPS.ME](mapsme.md) | アプリとウェブ | 企業 | 商用 | 自前の C++ の地図エンジン (Organic Maps と CoMaps の元になった omim、Apache-2.0。今の版の中は未確認) | App Store、Google Play |
| [近くの安いマックがわかる｜マクドナルド価格帯マップ](mcd-pricemap.md) | ウェブ | 個人 | 商用 | Leaflet | Cloudflare |
| [MeshMap - Meshtastic Node Map](meshmap.md) | ウェブ | 個人 | 非商用 | Leaflet | Cloudflare |
| [Interactive Middle-earth Map - LOTR, Hobbit & Silmarillion](middle-earth.md) | ウェブ | 個人と見られる | 非商用 | Leaflet | 不明 (応答ヘッダーに手がかりが無い) |
| [みんなの行政地図](minchizu.md) | ウェブ | 個人と見られる | 商用 | - | LiteSpeed (配信先の事業者は不明) |
| [みんなでつくる全国冠水道路マップ｜みんつく全国冠水マップ](mintsuku.md) | ウェブ | 有志 | 商用 | MapLibre GL JS 6.6.0 | Cloudflare |
| [Mobility Maps: Making Public Transport Infrastructure Transparent](mobility.md) | ウェブ | 大学 | 非商用 | MapLibre GL JS 5.0.1、deck.gl | nginx/1.29.8 (配信先の事業者は不明) |
| [THE MODAL EARTH - 旋法の地球儀｜世界35の旋法を、本当の音程で聴き比べる ｜ Música Terra PLAYGROUND](modalearth.md) | ウェブ | 企業か個人 | 商用 | three.js | nginx (配信先の事業者は不明) |
| [Monitor the Situation ｜ Live World News Map & OSINT Dashboard](monitor-situation.md) | ウェブ | 個人 | 商用 | MapLibre GL JS | Cloudflare |
| [名字マップ](myojimap.md) | ウェブ | 大学 | 非商用 | Leaflet 1.6.0 | Amazon S3 + CloudFront |
| [Navara, an open-source 3D map engine](navara.md) | ウェブ | 団体 | 非商用 | - | Cloudflare |
| [ドライブサポーター by NAVITIME (カーナビ)](navitime-drive.md) | アプリ | 企業 | 商用 | - | App Store、Google Play |
| [withfs ニュースマップ｜ニュースの舞台を地図で俯瞰する ｜ withfs](newsmap.md) | ウェブ | 個人と見られる | 商用 | - | Google (Blogger) |
| [電界強度マップ - 電磁環境研究室モニタリングプロジェクト](nict-emc.md) | ウェブ | 公的機関 | 非商用 | - | Apache (配信先の事業者は不明) |
| [earth :: a global map of wind, weather, and ocean conditions](nullschool.md) | ウェブ | 企業 | 商用 | - | Cloudflare |
| [OpenGeocode: free, open-source, self-hosted geocoding](opengeocode.md) | ウェブ | 団体 | 非商用 | - | Cloudflare |
| [Open Infrastructure Map](openinframap.md) | ウェブ | 個人 | 非商用 | MapLibre GL JS | Cloudflare |
| [Organic マップ: オフライン地図](organicmaps.md) | アプリ | 企業 | 商用 | 自前の C++ の地図エンジン (MAPS.ME の omim から分かれた) | App Store、Google Play、Obtainium (GitHub のリリース) |
| [OsmAnd Map](osmand.md) | アプリとウェブ | 企業 | 商用 | ウェブ: Leaflet。アプリ: 自前のエンジン (Android は Java の `osmandapp/OsmAnd`、描画の中核は C++ の `osmandapp/OsmAnd-core`) | nginx/1.18.0 (Ubuntu) (配信先の事業者は不明) |
| [建物名 地名マップ v2.9.26](place-name-map.md) | ウェブ | 個人 | 非商用 | Leaflet | GitHub Pages |
| [国勢調査 メッシュ年齢構成クラスターマップ](popbalance.md) | ウェブ | 個人 | 非商用 | MapLibre GL JS | GitHub Pages |
| [全国農業用ため池マップについて ｜ 全国Q地図](qchizu-pond.md) | ウェブ | 個人か団体 | 商用 | - | Cloudflare |
| [Relief Fiddler Demo](relief-fiddler.md) | ウェブ | 企業 | 非商用と見られる | MapLibre GL JS | nginx (配信先の事業者は不明) |
| [Rennes Transit Map - Visualisation temps réel du réseau STAR](rennes-transit.md) | ウェブ | 個人 | 非商用 | MapLibre GL JS | GitHub Pages |
| [令和８年千葉連続風水害 復旧・復興アーカイブ ｜ Ri2MAPS](ri2maps.md) | ウェブ | 未確認 | 非商用と見られる | Leaflet 1.9.4 | Apache (配信先の事業者は不明) |
| [全国のトレランコースと大会コース｜Runnable](runnable.md) | ウェブ | 個人と見られる | 商用 | MapLibre GL JS | Vercel |
| [裁判官マップ - 日本地図から裁判官を探す ｜ 裁判官マップ](saibankan.md) | アプリとウェブ | 個人 | 非商用と見られる | - | Cloudflare |
| [おでかけ航路マップ ｜ 日本全国の旅客船・フェリー航路情報と時刻表リンク](searoute.md) | ウェブ | 個人 | 商用 | MapLibre GL JS | Cloudflare |
| [生活利便性マップ](seikatsu-map.md) | ウェブ | 個人 | 非商用 | Leaflet 1.9.4 | Cloudflare |
| [せんべろ東京マップ（東京都内の立ち飲み・大衆酒場・居酒屋を地図から検索） ｜ せんべろnet](senbero.md) | ウェブ | 個人 | 商用 | Google Maps JavaScript API | nginx (配信先の事業者は不明) |
| [showhand - 全晒しAI不動産周辺マップ](showhand.md) | ウェブ | 企業 | 商用 | - | Vercel |
| [SNS災害情報集約マップAI](solafune-alert.md) | ウェブ | 企業 | 商用と見られる | MapLibre GL JS | Amazon S3 + CloudFront |
| [THE SOUNDING EARTH](sounding-earth.md) | ウェブ | 企業か個人 | 商用 | three.js | nginx (静的な配信) |
| [StreetComplete](streetcomplete.md) | アプリ | 個人 | 商用 | MapLibre (maplibre-compose 0.20.0) | Google Play、App Store |
| [Sunlit Earth: Earth from space as your wallpaper](sunlit-earth.md) | ウェブ | 個人か有志 | 非商用 | - | Cloudflare |
| [スーパー地形](superdem.md) | アプリ | 個人 | 商用 | - | App Store、Google Play |
| [世界のライブカメラ地図｜いま見れるライブ映像 - たま旅ライブ](tamatabi.md) | ウェブ | 個人と見られる | 商用 | MapLibre GL JS 4.7.1、D3 | Vercel |
| [Dig a Hole to China? See Where You'd Come Out ｜ Through Earth](throughearth.md) | ウェブ | 個人 | 非商用 | three.js | Cloudflare |
| [TokyoMap（東京都地図情報サイト）](tokyomap.md) | ウェブ | 公的機関 | 非商用 | Google Maps JavaScript API | Amazon S3 + CloudFront |
| [日本のライブカメラ地図 ｜ とまり木](tomarigi.md) | ウェブ | 企業 | 商用 | Leaflet | Cloudflare |
| [trainsworld](trainsworld.md) | ウェブ | 個人 | 非商用 | MapLibre GL JS | Cloudflare 経由の GitHub Pages |
| [トリマ-歩数・移動でポイント！散歩やウォーキングでお金を稼ぐ](trima.md) | アプリ | 企業 | 商用 | - | App Store、Google Play |
| [Trip Planner 山行計画サポートマップ｜日本雪崩ネットワーク](tripplanner.md) | ウェブ | 団体 | 商用 | - | Cloudflare |
| [uMap - Online map creator](umap.md) | ウェブ | 団体 | 非商用 | Leaflet | nginx/1.31.6 (配信先の事業者は不明) |
| [Urbanist Map](urbanistmap.md) | ウェブ | 個人 | 非商用 | MapLibre GL JS | Cloudflare |
| [USOMAP - 架空世界地図ジェネレーター｜無料の地図メーカー](usomap.md) | ウェブ | 企業 | 商用と見られる | three.js | Cloudflare |
| [Trump Deadline Countdown ｜ CENTCOM Theater Operations Map ｜ US vs Iran Force Tracker](usvsiran.md) | ウェブ | 個人 | 非商用と見られる | Leaflet | Cloudflare |
| [V2X2MAP - live receiver and map for ITS-G5 / V2X](v2x2map.md) | アプリとウェブ | 個人 | 商用 | - | Cloudflare |
| [WAR 3.0 - Live World War 3 Heat Map & Real-Time Conflict Tracker](warheatmap.md) | ウェブ | 個人と見られる | 非商用と見られる | MapLibre GL JS 4.7.1 | Cloudflare |
| [Watched · Something watched you this week](watched-earth.md) | ウェブ | 個人 | 非商用 | - | Vercel |
| [Interactive Map (WebMCP)](webmcp-gmap.md) | ウェブ | 個人と見られる | 非商用 | Google Maps JavaScript API | Cloudflare |
| [Yahoo!防災速報](yahoo-bousai.md) | アプリ | 企業 | 非商用と見られる | - | App Store、Google Play |
| [Yahoo!マップ](yahoo-map.md) | アプリとウェブ | 企業 | 商用 | ウェブ: Mapbox GL JS (アプリの中は開いていない) | App Store、Google Play。ウェブの配信元は未確認 |
| [非公式 山岡家 Map](yamaokaya.md) | ウェブ | 個人 | 非商用 | MapLibre GL JS | Amazon S3 + CloudFront |
| [YAMAP / ヤマップ ｜ 登山をもっと楽しく、登山情報プラットフォーム](yamap.md) | アプリとウェブ | 企業 | 商用 | - | CloudFront 経由 (配信元は不明)。アプリは App Store、Google Play |
| [気象衛星とレーダーマップ ｜ Zoom Earth](zoomearth.md) | アプリとウェブ | 企業 | 商用 | - | Cloudflare |

## カードを足すとき

1 サービス 1 ファイルで、ファイル名はサービスを表す短い英字にする。ウェブとアプリの両方があるサービスは 1 枚にまとめ、技術の表の「種類」に両方を書く。節と項目は既存のカードと揃える。どんなサービスかの 7 項目 (一行で、提供する価値、想定する利用者、商用か非商用か、推定の売上、運営、推定の運用費) は欠かせない。欠けているか空だと `scripts/check.py` が誤りにする。分からないものは空にせず「未確認」と書く。観測した日を必ず書き、見えなかったものは「見つからなかった」「見えなかった」と書いて推測で埋めない。推測を書くときは (推測) と付ける。足したらこの一覧に 1 行足す。
