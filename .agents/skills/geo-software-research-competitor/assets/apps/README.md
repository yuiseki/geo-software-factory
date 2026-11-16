# 観測した地図アプリのカード

ストアのアプリが本体の地図アプリを、1 アプリ 1 枚のカードにしたもの。App Store と Google Play の表示、運営者のサイトと発表、ソースが公開されていればその設定のファイルを読んで書いた。似たものを探すとき (SKILL.md の手順 3、4) は、[../services/](../services/README.md) と合わせてまず見て、同じものを調べ直さない。

カードの形は [../services/](../services/README.md) と同じで、どんなサービスかの 7 項目と技術の節からなる。技術の節には、種類 (iOS、Android、Apple Watch など) と、ストアの表示 (販売元、価格とアプリ内課金、評価の数、ダウンロード数、初出と最新の更新) を書く。

## カードを探すとき

各カードの冒頭の「探すときの語」に言い換えを並べてある。探し方は [../services/README.md](../services/README.md) の「カードを探すとき」と同じで、両方のディレクトリを引く。

## 読むときの注意

- どのカードも 2026-11-12 の観測で、その後に変わっていることがある。結論に使う前に、ストアと運営者のサイトを開き直す
- アプリは端末で開いていない。描画のライブラリ、地図のデータ、通信先は「未確認」とし、ストアの説明、運営者の発表、公開されたソースに書かれたことだけを書いた。確かめるには、端末でアプリのオープンソースのライセンスの一覧と通信を見る
- ソースが公開されているアプリは、ビルドの設定のファイル (例: `gradle/libs.versions.toml`、`pubspec.yaml`) から描画のライブラリと版を読んだ
- ストアの数字の読み方: App Store の評価の数は日本のストアの数、Google Play のダウンロード数は世界の数で「500万+」のように区切りの下限しか出ない。Google Play の「広告を含む」の表示は、ページの HTML からは取れなかったので書いていない
- 寄付も商用に含める。寄付の額は、Open Collective と Liberapay のように公開されていれば書いた (Liberapay の額は週あたり)
- 売上と運用費の推測の仕方は [../services/README.md](../services/README.md) の注意と同じ。推測の金額は桁の目安で、確かめた値ではない

## 一覧

| カード | 運営 | 商用か | 描画 | 配信 |
|---|---|---|---|---|
| [7NOW](7now.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [AlpineQuest](alpinequest.md) | 個人 / 小規模開発元 | 商用 | 未確認 | Google Play、公式サイト (直接購入版) |
| [Alto](alto.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Appleマップ](apple-maps.md) | 企業 | 非商用と見られる | 未確認 | App Store |
| [バスNAVITIME 時刻表&乗り換え案内&路線図ナビ](bus-navitime.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [c:geo](cgeo.md) | 団体 | 商用 | Mapsforge | Google Play (GitHub Releases からも APK 配布) |
| [地図ロイド](chizroid.md) | 個人 | 商用 | 未確認 | Google Play |
| [CoMaps](comaps.md) | 団体 | 商用 | 自前の C++ の地図エンジン (Organic Maps から分かれた) | App Store、Google Play |
| [DiDi（モビリティ）](didi.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Dokoka - 矢印だけの散歩ナビ](dokoka.md) | 個人 | 非商用 | 未確認 | App Store、Google Play |
| [DoorDash](doordash.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [ドラゴンクエストウォーク](dq-walk.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Every Door](everydoor.md) | 個人 | 非商用と見られる | flutter_map と vector_map_tiles | App Store、Google Play |
| [ジオグラフィカ](geographica.md) | 個人 | 商用 | 未確認 | App Store、Google Play |
| [ジオクエ-写真を撮ってポイントに！ポイ活アプリ](geoquest.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Ghostbusters World](ghostbusters-world.md) | 企業 | 商用 | 未確認 | かつて App Store、Google Play で配信 (2020-08-13 終了によりプレイ不可) |
| [GO（タクシーアプリ）](go-taxi.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Google マップ](google-maps.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Grab](grab.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [本コレ](honcolle.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Instacart](instacart.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Jurassic World Alive](jurassic-world-alive.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [KAKUNIN MAP](kakunin-map.md) | 企業 | 非商用と見られる | 未確認 | App Store、Google Play |
| [LINE GO](line-go.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Lyft](lyft.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Maply](maply.md) | 企業 | 商用と見られる | 未確認 | App Store |
| [オフライン地図、GPSナビ:MAPS.ME](mapsme.md) | 企業 | 商用 | 自前の C++ の地図エンジン (Organic Maps と CoMaps の元になった omim、Apache-2.0。今の版の中は未確認) | App Store、Google Play |
| [MoodGo](moodgo.md) | 個人 | 商用 | 未確認 | App Store |
| [ドライブサポーター by NAVITIME (カーナビ)](navitime-drive.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Ola](ola.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Organic マップ: オフライン地図](organicmaps.md) | 企業 | 商用 | 自前の C++ の地図エンジン (MAPS.ME の omim から分かれた) | App Store、Google Play、Obtainium (GitHub のリリース) |
| [Pokémon GO](pokemon-go.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [S.RIDE](s-ride.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [StreetComplete](streetcomplete.md) | 個人 | 商用 | MapLibre (maplibre-compose 0.20.0) | Google Play、App Store |
| [スーパー地形](superdem.md) | 個人 | 商用 | 未確認 | App Store、Google Play |
| [登山記録 - 百名山・GPS・オフライン地図](tozan-kiroku.md) | 個人 | 商用 | 未確認 | App Store |
| [トリマ-歩数・移動でポイント！散歩やウォーキングでお金を稼ぐ](trima.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Trip Supporter](trip-supporter.md) | 個人 | 商用 | Mapbox | App Store |
| [Uber](uber.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [V2X2MAP - live receiver and map for ITS-G5 / V2X](v2x2map.md) | 個人 | 商用 | 地図ライブラリの名前は見つからなかった | Cloudflare |
| [The Walking Dead: Our World](walking-dead-our-world.md) | 企業 | 商用 | 未確認 | かつて App Store、Google Play で配信 (2023-01-31 終了によりストアから削除・プレイ不可) |
| [WhatsApp](whatsapp.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Yahoo!防災速報](yahoo-bousai.md) | 企業 | 非商用と見られる | 未確認 | App Store、Google Play |
| [妖怪ウォッチ ワールド](youkai-watch-world.md) | 企業 | 商用 | 未確認 | かつて App Store、Google Play で配信 (2022-12-23 終了) |
| [ずぼ旅（DriftLog）](zubotabi.md) | 個人 | 商用 | 未確認 | App Store、Google Play |

## アプリもあるウェブのサービス

ウェブの地図とアプリの両方があるものは [../services/](../services/README.md) に置いている。

- [2GIS](../services/2gis.md)
- [ABCマート 店舗検索](../services/abc-mart-store.md)
- [Amazon ロッカー／カウンター検索](../services/amazon-locker.md)
- [ArcGIS Online](../services/arcgis-online.md)
- [Atlas Obscura](../services/atlas-obscura.md)
- [Bikemap](../services/bikemap.md)
- [CellMapper](../services/cellmapper.md)
- [CHINTAI](../services/chintai.md)
- [DeepStateMap](../services/deepstatemap.md)
- [DHL ジャパン 拠点検索](../services/dhl-locator.md)
- [Domino's（Pinpoint Delivery / 店舗検索）](../services/dominos.md)
- [EarthCam](../services/earthcam.md)
- [EMSC](../services/emsc.md)
- [ENEOS サービスステーション検索](../services/eneos-ss.md)
- [Expedia](../services/expedia.md)
- [FedEx ジャパン 拠点検索](../services/fedex-locator.md)
- [FlightAware](../services/flightaware.md)
- [Garmin Explore](../services/garmin-explore.md)
- [Geocaching](../services/geocaching.md)
- [GU 店舗検索](../services/gu-store.md)
- [Hotels.com](../services/hotels-com.md)
- [Idealista](../services/idealista.md)
- [IKEA（店舗検索）](../services/ikea.md)
- [ImmoScout24](../services/immoscout24.md)
- [iOverlander](../services/ioverlander.md)
- [IQAir Earth](../services/iqair-earth.md)
- [J-SHIS 地震ハザードステーション](../services/j-shis.md)
- [Light Pollution Map](../services/light-pollution-map.md)
- [LiveUAmap](../services/liveuamap.md)
- [LivMap (リブマップ) - チームで使う共有地図](../services/livmap.md)
- [MapChart](../services/mapchart.md)
- [MapFan](../services/mapfan.md)
- [Mapillary](../services/mapillary.md)
- [MapQuest](../services/mapquest.md)
- [Mapy.com（旧 Mapy.cz）](../services/mapy-com.md)
- [Meteoblue](../services/meteoblue.md)
- [NAVITIME（ウェブ総合版）](../services/navitime.md)
- [NewDays 店舗検索](../services/newdays-store.md)
- [onX](../services/onx.md)
- [OsmAnd Map](../services/osmand.md)
- [Outdooractive](../services/outdooractive.md)
- [Park4Night](../services/park4night.md)
- [Polarsteps](../services/polarsteps.md)
- [RadarBox（AirNav Radar）](../services/radarbox.md)
- [Radio Garden](../services/radio-garden.md)
- [RainViewer](../services/rainviewer.md)
- [Realtor.com](../services/realtor.md)
- [Redfin](../services/redfin.md)
- [Relive](../services/relive.md)
- [Rightmove](../services/rightmove.md)
- [Roadtrippers](../services/roadtrippers.md)
- [Rome2Rio](../services/rome2rio.md)
- [Seterra](../services/seterra.md)
- [Starbucks（Global Store Locator）](../services/starbucks.md)
- [Stellarium Web](../services/stellarium-web.md)
- [SunCalc](../services/suncalc.md)
- [tenki.jp](../services/tenki-jp.md)
- [TimeGuessr](../services/timeguessr.md)
- [TomTom](../services/tomtom.md)
- [Trailforks](../services/trailforks.md)
- [TripAdvisor](../services/tripadvisor.md)
- [Trulia](../services/trulia.md)
- [UPS ジャパン 取扱店検索](../services/ups-locations.md)
- [Ushahidi](../services/ushahidi.md)
- [Wanderlog](../services/wanderlog.md)
- [Watch Duty](../services/watch-duty.md)
- [Wayfair](../services/wayfair.md)
- [Wheelmap](../services/wheelmap.md)
- [Wikiloc](../services/wikiloc.md)
- [WorldGuessr](../services/worldguessr.md)
- [Worldle](../services/worldle.md)
- [Yahoo!マップ](../services/yahoo-map.md)
- [YAMAP / ヤマップ ｜ 登山をもっと楽しく、登山情報プラットフォーム](../services/yamap.md)
- [Yandex Maps](../services/yandex-maps.md)
- [【推し活カフェ】日本最大級の推し活・コラボカフェ検索 ｜ imako推し活カフェ](../services/imako.md)
- [くら寿司 店舗検索](../services/kurasushi-store.md)
- [しまむら 店舗検索](../services/shimamura-store.md)
- [すかいらーくグループ 店舗検索](../services/skylark-store.md)
- [すき家 店舗検索](../services/sukiya-store.md)
- [はま寿司 店舗検索](../services/hamasushi-store.md)
- [びっくりドンキー 店舗検索](../services/bikkuri-donkey-store.md)
- [ウェザーニュース](../services/weathernews.md)
- [ウエルシア 店舗検索](../services/welcia-store.md)
- [オートバックス 店舗検索](../services/autobacs-store.md)
- [カインズ 店舗検索](../services/cainz-store.md)
- [ケンタッキーフライドチキン 店舗検索](../services/kfc-store.md)
- [ココス 店舗検索](../services/cocos-store.md)
- [コメダ珈琲店 店舗検索](../services/komeda-store.md)
- [コーナン 店舗検索](../services/kohnan-store.md)
- [ジョイフル 店舗検索](../services/joyfull-store.md)
- [ジョルダン乗換案内](../services/jorudan.md)
- [スギ薬局 店舗検索](../services/sugi-store.md)
- [スシロー 店舗検索](../services/sushiro-store.md)
- [セイコーマート 店舗検索](../services/seicomart-store.md)
- [ゼッテリア（旧ロッテリア） 店舗検索](../services/zetteria-store.md)
- [タリーズコーヒー 店舗検索](../services/tullys-store.md)
- [ダイソー 店舗検索](../services/daiso-store.md)
- [ダジック・アース - ダジック・アース](../services/dagik.md)
- [ツルハドラッグ 店舗検索](../services/tsuruha-store.md)
- [デニーズ 店舗検索](../services/dennys-store.md)
- [ドコモショップ 店舗検索](../services/docomo-shop.md)
- [ドトールコーヒー 店舗検索](../services/doutor-store.md)
- [ドン・キホーテ 店舗検索](../services/donki-store.md)
- [ビックカメラ 店舗検索](../services/biccamera-store.md)
- [ファミリーマート 店舗検索](../services/familymart-store.md)
- [ポストマップ](../services/postmap.md)
- [マツモトキヨシ 店舗検索](../services/matsukiyo-store.md)
- [ミスタードーナツ 店舗検索](../services/misterdonut-store.md)
- [ミニストップ 店舗検索](../services/ministop-store.md)
- [モスバーガー 店舗検索](../services/mos-burger-store.md)
- [ヤマダデンキ 店舗検索](../services/yamada-denki-store.md)
- [ヤマト運輸 営業所・取扱店検索](../services/yamato-locations.md)
- [ヨドバシカメラ 店舗検索](../services/yodobashi-store.md)
- [ライフ 店舗検索](../services/lifecorp-store.md)
- [ロイヤルホスト 店舗検索](../services/royalhost-store.md)
- [ロフト 店舗検索](../services/loft-store.md)
- [ローソン 店舗検索](../services/lawson-store.md)
- [ワークマン 店舗検索](../services/workman-store.md)
- [丸亀製麺 店舗検索](../services/marugame-store.md)
- [佐川急便 営業所検索](../services/sagawa-locations.md)
- [吉野家 店舗検索](../services/yoshinoya-store.md)
- [地図マピオン（Mapion）｜地図検索/ルート検索/天気予報](../services/mapion.md)
- [東横イン ホテル一覧・検索](../services/toyoko-inn-store.md)
- [松屋 店舗検索](../services/matsuya-store.md)
- [気象衛星とレーダーマップ ｜ Zoom Earth](../services/zoomearth.md)
- [無印良品 店舗検索](../services/muji-store.md)
- [熊出没マップ2026年 - 全国165,975件 - クママップ](../services/kumamap.md)
- [福山通運 営業所検索](../services/fukutsu-locations.md)
- [裁判官マップ - 日本地図から裁判官を探す ｜ 裁判官マップ](../services/saibankan.md)
- [西濃運輸 営業所検索](../services/seino-locations.md)

## カードを足すとき

1 アプリ 1 ファイルで、ファイル名はアプリを表す短い英字にする。ストアのアプリが本体のものをここに置き、ウェブの地図もあるものは ../services/ に置いて上の「アプリもあるウェブのサービス」に 1 行足す。どんなサービスかの 7 項目は欠かせず、欠けているか空だと `scripts/check.py` が誤りにする。App Store は `https://itunes.apple.com/lookup?id=<ID>&country=jp`、Google Play はパッケージ名の詳細のページで読む。冒頭に「- 探すときの語:」の行を置く。観測した日を書き、端末で見ていないところは「未確認」と書く。足したらこの一覧に 1 行足す。
