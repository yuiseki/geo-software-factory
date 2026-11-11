# 観測した地図アプリのカード

ストアのアプリが本体の地図アプリを、1 アプリ 1 枚のカードにしたもの。App Store と Google Play の表示、運営者のサイトと発表、ソースが公開されていればその設定のファイルを読んで書いた。似たものを探すとき (SKILL.md の手順 3、4) は、[../services/](../services/README.md) と合わせてまず見て、同じものを調べ直さない。

カードの形は [../services/](../services/README.md) と同じで、どんなサービスかの 7 項目と技術の節からなる。技術の節には、種類 (iOS、Android、Apple Watch など) と、ストアの表示 (販売元、価格とアプリ内課金、評価の数、ダウンロード数、初出と最新の更新) を書く。

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
| [Appleマップ](apple-maps.md) | 企業 | 非商用と見られる | 未確認 | App Store |
| [バスNAVITIME 時刻表&乗り換え案内&路線図ナビ](bus-navitime.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [CoMaps](comaps.md) | 団体 | 商用 | 自前の C++ の地図エンジン (Organic Maps から分かれた) | App Store、Google Play |
| [Dokoka - 矢印だけの散歩ナビ](dokoka.md) | 個人 | 非商用 | 未確認 | App Store、Google Play |
| [Every Door](everydoor.md) | 個人 | 非商用と見られる | flutter_map と vector_map_tiles | App Store、Google Play |
| [ジオクエ-写真を撮ってポイントに！ポイ活アプリ](geoquest.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Google マップ](google-maps.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [本コレ](honcolle.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [KAKUNIN MAP](kakunin-map.md) | 企業 | 非商用と見られる | 未確認 | App Store、Google Play |
| [Maply](maply.md) | 企業 | 商用と見られる | 未確認 | App Store |
| [オフライン地図、GPSナビ:MAPS.ME](mapsme.md) | 企業 | 商用 | 自前の C++ の地図エンジン (Organic Maps と CoMaps の元になった omim、Apache-2.0。今の版の中は未確認) | App Store、Google Play |
| [ドライブサポーター by NAVITIME (カーナビ)](navitime-drive.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [Organic マップ: オフライン地図](organicmaps.md) | 企業 | 商用 | 自前の C++ の地図エンジン (MAPS.ME の omim から分かれた) | App Store、Google Play、Obtainium (GitHub のリリース) |
| [StreetComplete](streetcomplete.md) | 個人 | 商用 | MapLibre (maplibre-compose 0.20.0) | Google Play、App Store |
| [スーパー地形](superdem.md) | 個人 | 商用 | 未確認 | App Store、Google Play |
| [トリマ-歩数・移動でポイント！散歩やウォーキングでお金を稼ぐ](trima.md) | 企業 | 商用 | 未確認 | App Store、Google Play |
| [V2X2MAP - live receiver and map for ITS-G5 / V2X](v2x2map.md) | 個人 | 商用 | 地図ライブラリの名前は見つからなかった | Cloudflare |
| [Yahoo!防災速報](yahoo-bousai.md) | 企業 | 非商用と見られる | 未確認 | App Store、Google Play |

## アプリもあるウェブのサービス

ウェブの地図とアプリの両方があるものは [../services/](../services/README.md) に置いている。

- [ダジック・アース - ダジック・アース](../services/dagik.md)
- [【推し活カフェ】日本最大級の推し活・コラボカフェ検索 ｜ imako推し活カフェ](../services/imako.md)
- [熊出没マップ2026年 - 全国165,975件 - クママップ](../services/kumamap.md)
- [LivMap (リブマップ) - チームで使う共有地図](../services/livmap.md)
- [Mapillary](../services/mapillary.md)
- [地図マピオン（Mapion）｜地図検索/ルート検索/天気予報](../services/mapion.md)
- [OsmAnd Map](../services/osmand.md)
- [裁判官マップ - 日本地図から裁判官を探す ｜ 裁判官マップ](../services/saibankan.md)
- [Yahoo!マップ](../services/yahoo-map.md)
- [YAMAP / ヤマップ ｜ 登山をもっと楽しく、登山情報プラットフォーム](../services/yamap.md)
- [気象衛星とレーダーマップ ｜ Zoom Earth](../services/zoomearth.md)

## カードを足すとき

1 アプリ 1 ファイルで、ファイル名はアプリを表す短い英字にする。ストアのアプリが本体のものをここに置き、ウェブの地図もあるものは ../services/ に置いて上の「アプリもあるウェブのサービス」に 1 行足す。どんなサービスかの 7 項目は欠かせず、欠けているか空だと `scripts/check.py` が誤りにする。App Store は `https://itunes.apple.com/lookup?id=<ID>&country=jp`、Google Play はパッケージ名の詳細のページで読む。観測した日を書き、端末で見ていないところは「未確認」と書く。足したらこの一覧に 1 行足す。
