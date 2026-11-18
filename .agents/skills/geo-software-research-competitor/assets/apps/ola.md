---
financial: commercial
organization: corp-ent
---

# Ola

- URL: https://apps.apple.com/in/app/ola-book-cab-auto-bike-taxi/id539179365
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: 配車、タクシー、オートリキシャ、インド、Ola Maps、自社地図移行、Ola

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | インド最大手の配車アプリで、タクシー、オートリキシャ、バイクタクシーの配車と決済を提供する |
| 提供する価値 | 地図上で乗降地を指定して配車でき、インドの複雑な道路事情や住所体系に合わせた乗車地点の案内と料金見積もりを受けられる |
| 想定する利用者 | インド全土および一部海外都市の通勤者・旅行者 |
| 商用か非商用か | 商用 (配車ごとの仲介手数料、法人向けサービス、自社 Ola Maps の API 外販) |
| 推定の売上 | 公開報道あり (ANI Technologies の年間売上は数百億円規模。ただし非上場) |
| 運営 | 企業 (ANI Technologies Pvt. Ltd.) |
| 推定の運用費 | 推測: 年間数十億円規模 (2024年7月に Google Maps の年間約 100 クローレ・ルピーの費用を自社 Ola Maps 移行でゼロにしたと発表) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | iOS と Android のアプリ |
| 描画 | 未確認 (アプリの中は開いていない) |
| 背景の地図とタイル | 自社開発の「Ola Maps」(OpenStreetMap ベースに自社の配車 GPS テレメトリ・AI を組み合わせた地図基盤)。2024年7月に Google Maps から全面移行した |
| 投稿やデータの保存先 | サーバー (配車リクエスト、走行軌跡、テレメトリによる地図更新データ) |
| 配信 | App Store、Google Play |

ストアの表示 (2026-11-16):

- App Store: 販売元 ANI Technologies Pvt. Ltd.、Free (無料)、インドストア評価 1,772,075 件 (平均 4.59)、初出 2012-07-11、最新版 5.0.23 (2026-11-02)、分類 Travel
- Google Play: `com.olacabs.customer`、1億+ ダウンロード (100M+)、開発元 Ola (ANI TECHNOLOGIES PRIVATE LIMITED)、アプリ内購入 なし

メモ:

- 2024年7月、CEO の Bhavish Aggarwal 氏が Google Maps への年間約 100 クローレ・ルピー (100 crore INR、約 1,200 万ドル) の支出を削減するため、自社開発の Ola Maps へ全面移行したと発表し、同時に Krutrim Cloud 上で Ola Maps API の外販も開始した
- Ola Maps はベースデータとして OpenStreetMap (OSM) を活用していることが技術コミュニティの検証や報道で確認されている
- アプリの中の描画のライブラリや通信先は端末で開いていないため未確認。確かめるには端末でオープンソースのライセンス一覧と通信を見る
