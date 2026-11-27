---
financial: commercial
organization: corp-ent
first_seen: 2025-11-01
first_seen_by: wayback
---

# Francfranc 店舗一覧

- URL: https://francfranc.com/pages/stores
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、Francfranc、フランフラン、インテリア、生活雑貨、店舗一覧、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の Francfranc 店舗を絞り込み検索し、選択した店舗の詳細情報や地図を確認できる公式ショップリストページ |
| 提供する価値 | エリアや条件で店舗を絞り込み、営業時間、所在地、埋め込み地図を同一画面上で確認して来店につなげられる |
| 想定する利用者 | 家具やインテリア雑貨、ギフトの購入で実店舗での確認や来店を希望する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客および公式オンラインショップとの連携のために株式会社 Francfranc が提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗および EC のオムニチャネル送客に貢献する集客基盤 |
| 運営 | 企業 (株式会社 Francfranc) |
| 推定の運用費 | 推測: 月数万円。Shopify 基盤上のカスタムページと Cloudflare 配信、および Google Maps 埋め込みで構成されている |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | iframe 埋め込み (`selectedStore.googleMapEmbedUrl` を iframe の `src` にバインド) |
| フレームワーク | Shopify Storefront + Vue.js (`v-for`、`v-if`、`v-text` による絞り込み表示) |
| 背景の地図とタイル | Google Maps (Embed URL による埋め込み) |
| 投稿やデータの保存先 | Shopify 店舗ページデータ / 自社管理の店舗 JSON データ (詳細は未確認) |
| 配信 | Cloudflare (`server: cloudflare`、`cf-ray` ヘッダ) |

メモ:

- 2026-11-17 の一次 HTTP 取得 (`https://francfranc.com/pages/stores`) ではステータス 200 を返し、Shopify 基盤上で Vue.js による店舗絞り込みと `selectedStore.googleMapEmbedUrl` の iframe 埋め込みを行っていることを確認した

データの出どころ (2026-11-17):

- 店舗データ: 株式会社 Francfranc 自社管理の店舗情報
- 背景地図: Google Maps (埋め込み iframe)
