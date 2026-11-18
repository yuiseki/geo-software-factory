---
financial: commercial
organization: corp-ent
---

# イトーヨーカドー 店舗検索

- URL: https://stores.itoyokado.co.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、スーパー、総合スーパー、イトーヨーカドー、Ito-Yokado、ヨーク、Canly、営業時間、チラシ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のイトーヨーカドー店舗をエリア・キーワード・条件から検索し、個別店舗ページの地図や営業時間・サービス設備を確認できる公式店舗検索サイト |
| 提供する価値 | 多言語対応（日本語・英語・中国語・韓国語）で店舗を探し、個別店舗ページで位置情報・営業時間・チラシや設備情報を確認できる |
| 想定する利用者 | イトーヨーカドーでの買い物を予定している一般客、訪日外国人客、近隣の店舗を探している生活者 |
| 商用か非商用か | 商用 (実店舗への来店送客およびネットスーパー等への導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗および EC 売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社イトーヨーカ堂) |
| 推定の運用費 | 推測: 月数万〜数十万円。店舗情報管理 SaaS (Canly) の利用料および CloudFront + Next.js の運用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (個別店舗ページ `/detail/555/` の `__NEXT_DATA__` 内に `"mapMapSetting":"leaflet"` を確認) |
| フレームワーク | Next.js (`x-powered-by: Next.js`、`/_next/static/chunks/...`)、Canly 店舗ページ基盤 (GTM `GTM-TXVHHDM`) |
| 背景の地図とタイル | OpenStreetMap 等 (事前調査では OpenStreetMap / Leaflet、タイル URL の直接観測は未確認) |
| 投稿やデータの保存先 | Canly 管理の店舗データベース (`__NEXT_DATA__` にエリア・設定・店舗データを埋め込み) |
| 配信 | Amazon CloudFront (`via: ...cloudfront.net (CloudFront)`、`x-cache: Hit from cloudfront`) |

メモ:

- 2026-11-17 の HTTP 観測では、CloudFront 配信の Next.js アプリ（Canly 基盤）であり、多言語サブドメイン (`en.`、`zh-cn.`、`zh-tw.`、`ko.`) が用意されていることを確認した
- 個別店舗ページ (`/detail/555/`) の `__NEXT_DATA__` 内に `"mapMapSetting":"leaflet"` の設定が含まれており、詳細ページ側で Leaflet 地図を描画する構成になっている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社イトーヨーカ堂 (Canly 連携)
- 背景地図: OpenStreetMap (事前調査結果。今回の HTTP 静的取得では Leaflet 設定まで確認)
