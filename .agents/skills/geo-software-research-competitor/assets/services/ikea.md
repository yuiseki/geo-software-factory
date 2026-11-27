---
financial: commercial
organization: corp-ent
first_seen: 2019-03-27
first_seen_by: wayback
---

# IKEA（店舗検索）

- URL: https://www.ikea.com/de/de/stores/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: IKEA、イケア、店舗検索、Store Locator、Google Maps Platform、ドイツ、在庫確認、ルート案内、オムニチャネル

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 家具・インテリア大手 IKEA の各店舗の場所、営業時間、店舗ごとの商品在庫やイベント情報、現在地からの移動時間を案内する店舗検索サービス |
| 提供する価値 | 最寄りの大型店舗や受取拠点を地図や距離順ですばやく見つけ、各店舗の営業時間やローカル情報、商品の店頭在庫状況を来店前に確認できる |
| 想定する利用者 | IKEA の実店舗への来店や店舗受取を検討している一般消費者 |
| 商用か非商用か | 商用 (店舗検索機能は無料。EC および実店舗での家具・雑貨販売によるオムニチャネル導線として運用) |
| 推定の売上 | 最大手フランチャイジーである Ingka Group の 2024 年会計年度 (FY24) 総売上は 418 億ユーロ (IKEA 小売売上は 396 億ユーロ) |
| 運営 | 企業 (IKEA / Ingka Group 等、スウェーデン発祥・オランダ拠点) |
| 推定の運用費 | 推測: 店舗検索機能単体は Google Maps Platform 等の API 利用料を含め月数十万〜数百万円規模 (IKEA 全体の EC・Cloudflare 基盤の一部として運用) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (`https://www.ikea.com/de/de/stores/` は HTTP 200 を返却したが、静的 HTML 上では `has_gmaps: false` であり、動的スクリプト内の描画手段までは未確認。Google Maps Platform 公式導入事例では IKEA ドイツが Maps JavaScript API 等を採用と公開されている) |
| フレームワーク | 未確認 (HTML 上からはフレームワーク特定に至らず) |
| 背景の地図とタイル | Google Maps Platform (IKEA ドイツの Google 公式導入事例にて、パートナー maplicate と共に Maps JavaScript API、Places API、Geocoding API、Routes / Directions / Distance Matrix API を統合と公開) |
| 投稿やデータの保存先 | IKEA 自社基盤 (各国の店舗マスタ、営業時間、リアルタイム在庫、ローカルイベント情報) |
| 配信 | Cloudflare (`Server: cloudflare`、`cf-ray` ヘッダーを確認) |

メモ:

- Google Maps Platform の公式事例として、IKEA ドイツ（53店舗）がグローバル標準テンプレート刷新にあたり、Google Cloud プレミアパートナーの maplicate と組んで Google Maps Platform を統合し、店舗検索・在庫可視化・移動時間計算を実現したことが紹介されている。
- ウェブ版のほか、iOS / Android 向けの公式「IKEA」アプリも提供されており、アプリ内でも店舗選択や店頭在庫の確認が可能。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 店舗情報・在庫・営業時間 | IKEA 各国法人・店舗システム | IKEA 公式サイトおよび Google Maps Platform 公式事例 |
| 地図・ルート・距離計算 | Google Maps Platform | Google Maps Platform 公式導入事例 (IKEA Germany) |
