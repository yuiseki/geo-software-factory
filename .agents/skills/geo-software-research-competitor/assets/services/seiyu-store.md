---
financial: commercial
organization: corp-ent
---

# 西友 店舗検索

- URL: https://www.seiyu.co.jp/searchshop/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、スーパー、スーパーマーケット、西友、SEIYU、リヴィン、サニー、トライアル西友、営業時間、チラシ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の西友店舗を地域・都道府県別のメニューや店舗名から検索し、各店舗の営業時間・駐車場・アクセスマップを確認できる公式店舗検索サイト |
| 提供する価値 | 地域から最寄りの西友店舗を素早く見つけ、個別店舗ページで営業時間・フロアガイド・Google マップによる位置情報を確認できる |
| 想定する利用者 | 西友での買い物を予定している一般客、近隣のスーパーや 24 時間営業店舗を探している生活者 |
| 商用か非商用か | 商用 (実店舗およびネットスーパーへの送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗および楽天西友ネットスーパー等の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社西友) |
| 推定の運用費 | 推測: 月数万円。Cloudflare + WordPress の運用費と Google Maps Embed API の利用（Maps Embed API は原則無料枠） |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps Embed API (`/wp-content/themes/seiyu-corporate/js/shop/index.js` が個別店舗ページの `.js-shop_map_inner` iframe に `https://www.google.com/maps/embed/v1/place?key=...` を設定) |
| フレームワーク | WordPress (`/wp-content/themes/seiyu-corporate/...`) + 独自 JS (`searchshop.js`、`shop/index.js`、Google Analytics 4 / GTM) |
| 背景の地図とタイル | Google マップ (Google Maps Embed API による iframe 埋め込み) |
| 投稿やデータの保存先 | WordPress 側で店舗ページ (`/shop/<店舗名>/`) を生成し、`data-ll` 属性で緯度・経度を保持 |
| 配信 | Cloudflare (`server: cloudflare`、`cf-ray: ...-NRT`) |

メモ:

- トップの店舗検索ページ (`/searchshop/`) には地図ライブラリは読み込まれておらず、地方・都道府県別の地方ブロックから個別店舗ページ (`/shop/<店舗名>/`) へ遷移する構成になっている
- 個別店舗ページでは `data-ll` に緯度・経度が埋め込まれ、JavaScript で Google Maps Embed API の iframe を動的に差し込んでいる

データの出どころ (2026-11-17):

- 店舗データ: 株式会社西友
- 背景地図: Google (Google Maps Embed API)
