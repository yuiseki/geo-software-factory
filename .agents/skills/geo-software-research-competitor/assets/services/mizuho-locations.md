---
financial: commercial
organization: corp-ent
first_seen: 2022-06-26
first_seen_by: wayback
---

# みずほ銀行 ATM・店舗検索

- URL: https://shop.www.mizuhobank.co.jp/b/mhbk/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ATM検索、銀行、みずほ銀行、みずほ信託銀行、みずほ証券、店舗外ATM、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のみずほ銀行 (およびみずほ信託銀行・みずほ証券の関連拠点) の店舗・ATM を検索し、地図上に表示する公式店舗・ATM 検索サイト |
| 提供する価値 | 駅名・住所・現在地や利用サービス条件から最寄りの店舗や ATM を探し、営業時間や窓口予約ページへそのまま遷移できる |
| 想定する利用者 | みずほ銀行・みずほ信託銀行・みずほ証券の顧客、近くで現金引出や窓口相談を行いたい利用者 |
| 商用か非商用か | 商用 (銀行・証券・信託グループの店舗案内および来店予約への送客基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 検索サイト単体の売上は 0 円。みずほフィナンシャルグループ各社の個人・法人業務の顧客接点維持に貢献 |
| 運営 | 企業 (株式会社みずほ銀行) |
| 推定の運用費 | 推測: 月数十万〜百万円規模。ONE COMPATH (旧 Mapion) の法人向け店舗検索 SPA 基盤と地図タイル配信費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (`chunk-vendors.3eedd891.js` 内に Leaflet を確認) + ONE COMPATH (旧 Mapion) |
| フレームワーク | Vue.js (`mapspa` SPA 構成、`chunk-vendors.3eedd891.js`、`app.12eb7cdb.js`、Swiper 同梱) |
| 背景の地図とタイル | ONE COMPATH (Mapion) 地図タイル (`https://bm0{s}.mapion.co.jp/m2/tile/{z}/{x}/{y}.png?usr=atlas_org`) |
| 投稿やデータの保存先 | ONE COMPATH (旧 Mapion) の店舗検索 API (`https://sasp.mapion.co.jp/b/mizuho_c/` 等) |
| 配信 | nginx (`server: nginx`) |

メモ:

- 同じ ONE COMPATH 採用でも、従来の jQuery ベースの `ss5_5` 構成ではなく、Vue.js + Leaflet による SPA (`mapspa`) 構成を採用している
- `app.12eb7cdb.js` 内でみずほ銀行・みずほ信託銀行・みずほ証券の各拠点 URL が連携されている

データの出どころ (2026-11-17):

- 店舗・ATM データ: 株式会社みずほ銀行・みずほ信託銀行・みずほ証券管理の拠点情報
- 背景地図・店舗検索基盤: 株式会社 ONE COMPATH (Mapion 地図)
