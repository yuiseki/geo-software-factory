---
financial: commercial
organization: corp-ent
---

# 平和堂 店舗検索

- URL: https://shoplist.heiwado.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、スーパー、スーパーマーケット、平和堂、アル・プラザ、フレンドマート、Canly、営業時間、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 滋賀県や関西・北陸・東海エリアを中心に展開する平和堂・アル・プラザ・フレンドマート等の店舗を検索し、各店舗の地図や営業情報を確認できる公式店舗検索サイト |
| 提供する価値 | 地域や業態・キーワードから最寄りの平和堂グループ店舗を探し、個別店舗ページで地図や営業時間・サービス情報を確認できる |
| 想定する利用者 | 平和堂各店舗への来店を予定している一般客、近隣のスーパーやショッピングセンターを探している生活者 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社平和堂) |
| 推定の運用費 | 推測: 月数万〜数十万円。店舗情報管理 SaaS (Canly) の利用料および CloudFront + Next.js の運用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (個別店舗ページ `/detail/422/` の `__NEXT_DATA__` 内に `"mapMapSetting":"leaflet"` を確認) |
| フレームワーク | Next.js (`x-powered-by: Next.js`、`/_next/static/chunks/...`)、Canly 店舗ページ基盤 (GTM `GTM-MMF6TMPG`) |
| 背景の地図とタイル | OpenStreetMap 等 (事前調査では OpenStreetMap / Leaflet、タイル URL の直接観測は未確認) |
| 投稿やデータの保存先 | Canly 管理の店舗データベース (`__NEXT_DATA__` にエリア・設定・店舗データを埋め込み) |
| 配信 | Amazon CloudFront (`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の HTTP 観測では、CloudFront 配信の Next.js アプリ（Canly 基盤）であることを確認した
- 個別店舗ページ (`/detail/422/`) の `__NEXT_DATA__` 内に `"mapMapSetting":"leaflet"` の設定が含まれており、詳細ページ側で Leaflet 地図を描画する構成になっている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社平和堂 (Canly 連携)
- 背景地図: OpenStreetMap (事前調査結果。今回の HTTP 静的取得では Leaflet 設定まで確認)
