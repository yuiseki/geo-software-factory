# 成城石井 店舗情報

- URL: https://shop.seijoishii.com/seijoishii/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、スーパー、スーパーマーケット、成城石井、SEIJO ISHII、NAVITIME、Location Cloud、営業時間、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の成城石井店舗を都道府県・現在地・店舗一覧から検索し、店舗ごとの地図・ルート案内・営業時間・取扱サービスを確認できる公式店舗検索サイト |
| 提供する価値 | 駅ナカや商業施設内を含む成城石井の店舗を素早く探し、店舗詳細ページの地図やルート検索で迷わず来店できる |
| 想定する利用者 | 成城石井での買い物を予定している一般客、外出先や出張先で近くの成城石井を探している利用者 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗および公式オンラインショップへの送客に貢献 |
| 運営 | 企業 (株式会社成城石井) |
| 推定の運用費 | 推測: 月数万〜数十万円。NAVITIME Location Cloud の SaaS 利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME Location Cloud (`https://location-cloud.navitime.co.jp/...` のリンクおよび `/seijoishii/api/proxy1/route` 等の API を HTML 内に確認) |
| フレームワーク | jQuery 3.7.1 + NAVITIME Location Cloud テンプレート (`/seijoishii/resources/js/...`、moment.js、slick、GTM `GTM-M59VSW`) |
| 背景の地図とタイル | NAVITIME の地図タイル (NAVITIME Location Cloud 基盤) |
| 投稿やデータの保存先 | NAVITIME Location Cloud 側の店舗データベースおよび API (`/seijoishii/api/proxy1/...`、`images.pkg.navitime.co.jp`) |
| 配信 | Apache (`server: Apache`) |

メモ:

- 2026-11-17 の HTTP 観測で、URL パス (`/seijoishii/spot/lists`、`/seijoishii/address/list?address=13&search=address`)、アセット配信元 (`images.pkg.navitime.co.jp`)、およびフッターの `location-cloud.navitime.co.jp` リンクから NAVITIME Location Cloud による構築を確認した

データの出どころ (2026-11-17):

- 店舗データ: 株式会社成城石井
- 背景地図・ルート検索基盤: 株式会社ナビタイムジャパン (NAVITIME Location Cloud)
