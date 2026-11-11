# Official MapQuest - Maps, Driving Directions, Live Traffic

- URL: https://www.mapquest.com/
- 観測した日: 2026-11-12
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 地図検索、道案内、ルート検索、経路検索、ルートプランナー、カーナビ、ナビ、交通情報、渋滞、店の検索、アメリカの地図、カナダの地図、老舗の地図サイト、maps、directions、driving directions、route planner、navigation、GPS、live traffic

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 米国とカナダを中心に、地図の検索、道案内、交通情報、店や施設の検索、ルートプランナーを無料で提供する老舗の地図サイトとアプリ |
| 提供する価値 | 住所や店を探し、車や徒歩の道順を、登録なしに無料で調べられる。複数の経由地のルートや、ホテルの予約までつながる |
| 想定する利用者 | 米国とカナダで道順や店を調べる一般の人 |
| 商用か非商用か | 商用 (Google、Amazon をはじめ広告の事業者の通信が 20 以上あるディスプレイ広告、ウェブ検索 (Search the web、広告の説明は System1 のページ)、ホテルの予約 (MapQuest Travel)、Merch のストア、事業者の掲載 (Claim your business)、開発者向けの API。Plans のページはログインが要り中身は未確認) |
| 推定の売上 | 推測: 年数千万 USD 規模。広告の多さ、Google Play 1,000万+ ダウンロード、App Store (米国) の評価 30,443 件 (2026-11-12) から。親会社 System1 は上場しているが、MapQuest 単体の売上は未確認 |
| 運営 | 企業 (MapQuest Holdings LLC、System1 の子会社。利用規約のページの表記) |
| 推定の運用費 | 推測: 月数十万 USD 以上。HERE の地図データと API の使用料、検索とルートと交通情報のサーバー、CloudFront の配信、開発と運用の人件費 |

## 技術 (2026-11-12 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | ウェブと iOS、Android のアプリ (技術の欄はウェブの観測。アプリの中は開いていない) |
| 描画 | MapLibre GL JS (DOM の `maplibregl-map` クラス。グローバル変数には無く、版は未確認) |
| フレームワーク | Next.js、React (`/_next/static/` のパス) |
| 背景の地図とタイル | HERE の Vector Tile API (`vector.hereapi.com`、道路、道路の注記、陰影) を、自社のスタイル (`styles.mapq.st/styles/quest/light`) で描く。店や施設は自社のベクトルタイル (`layers.mapq.st`、popular と essential の 2 つ) を重ねる |
| 投稿やデータの保存先 | 自社の GraphQL の API (`graphql.aws.mapquest.com`)。保存した場所 (My saved places) はログインが要る |
| 配信 | CloudFront (AWS WAF のトークンの通信あり)。紹介と規約のページ `hello.mapquest.com` は Vercel |

読み込んだタイルとスタイルの URL (一部、API キーは省いた):

- `https://styles.mapq.st/styles/quest/light?layers=popular,essential,places`
- `https://vector.hereapi.com/v2/vectortiles/base/mc/{z}/{x}/{y}/omv?content=default,road_labels,hillshade`
- `https://layers.mapq.st/v2/popular/{z}/{x}/{y}.pbf`
- `https://layers.mapq.st/v2/essential/{z}/{x}/{y}.pbf`
- `https://static.mqcdn.com/shared/map_styles/production/fonts/{fontstack}/{range}.pbf`

ストアの表示 (2026-11-12):

- App Store: 日本のストアには無かった (検索でも lookup でも出ない)。米国のストアでは MapQuest GPS Navigation & Maps、販売元 MapQuest Holdings LLC、無料、評価 30,443 件 (平均 4.4)、初出 2009-06-11、最新の更新 2026-11-06、分類 Navigation (https://apps.apple.com/us/app/id316126557)
- Google Play: `com.mapquest.android.ace`、1,000万+ ダウンロード、アプリ内購入 あり
- アプリは米国とカナダの音声ナビ、Apple CarPlay、交通情報、衛星写真、ガソリンの価格の比較、ホテルの予約、OpenTable と GrubHub での予約や注文に対応する (App Store の説明)

メモ:

- 利用規約が、リバースエンジニアリングと、ロボットやデータの抽出の道具の使用を禁じている。そのため JavaScript の中は読まず、トップページを 1 回開いた通信と画面の文字だけを記録した
- 描画は MapLibre GL JS、データは HERE のベクトルタイルという組み合わせ。スタイル、フォント、店のレイヤーは自社のドメイン (`mapq.st`、`mqcdn.com`) から配る
- 地図の右下の帰属表示は「© 2026 MapQuest」と「Legal」のリンクだけで、HERE の名前は画面に出ていなかった。「Legal」と「Data and licenses」のリンクはどちらも利用規約のページへ飛び、その中の「3rd Party Notices and Licenses」の「Click here」にはリンクが無かった (2026-11-12)
- 広告の通信先は、Google (doubleclick、googlesyndication)、Amazon、Prebid 系 (rubicon、pubmatic、openx、criteo、3lift など)、Confiant、System1 など 20 以上。計測は New Relic、comScore、Google Analytics、Bing
- メニューに Live Radio、Search the web (`search.mapquest.com`)、Jobs がある
- はてなブックマーク 76 件 (2026-11-12)

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 背景の地図 (道路、注記、陰影) | HERE (Vector Tile API) | 画面には書かれていない。通信先 (`vector.hereapi.com`) で判定 |
| 店や施設のレイヤー | MapQuest の自社のタイル (`layers.mapq.st`)。元のデータは未確認 | 画面には書かれていない。通信先で判定 |
| 事業者の情報 | 事業者自身の登録 (Claim your business、Business Listings) を含む | 利用規約 (Supplemental Terms for MapQuest Business Listings)、メニュー |
| レストランの予約と注文 (アプリ) | OpenTable、GrubHub | App Store の説明 |
| 衛星写真、交通情報 (アプリ) | 未確認 | App Store の説明に機能だけ書かれている |
| 第三者のライセンスの一覧 | 未確認 (利用規約から一覧へのリンクが切れていた) | 利用規約 |

背景の地図の出どころが画面のどこにも書かれていないので、HERE であることは通信先からの判定にとどまる (2026-11-12)
