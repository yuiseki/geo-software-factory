---
financial: commercial
organization: corp-ent
first_seen: 2024-11-27
first_seen_by: wayback
---

# フレッシュネスバーガー 店舗検索

- URL: https://search.freshnessburger.co.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ハンバーガー、カフェ、フレッシュネスバーガー、FRESHNESS BURGER、営業時間、モバイルオーダー、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のフレッシュネスバーガー店舗を、エリア・条件・地図から検索し、店舗詳細やメニューを確認できる公式店舗検索サイト |
| 提供する価値 | 店舗の営業時間、メニュー、モバイルオーダー導線や店舗位置を確認し、来店や事前注文へ進める |
| 想定する利用者 | フレッシュネスバーガーを利用したい一般客、ランチやカフェ利用先を探す人 |
| 商用か非商用か | 商用 (実店舗への来店送客およびモバイルオーダー導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社フレッシュネス / コロワイドグループ) |
| 推定の運用費 | 推測: 月数万円〜十数万円。株式会社カンリー (Canly) 店舗検索 SaaS の利用料および CloudFront 配信費 |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (`__NEXT_DATA__` 内に `"mapMapSetting":"leaflet"` を確認。事前調査では Google Maps との記載もあったが現行設定は Leaflet) |
| フレームワーク | Next.js (`x-powered-by: Next.js`、Canly 店舗検索基盤) |
| 背景の地図とタイル | 未確認 (初期チャンクからはタイル配信元 URL を直接特定できず) |
| 投稿やデータの保存先 | Canly (株式会社カンリーの店舗情報管理 SaaS 基盤) |
| 配信 | Amazon CloudFront (`via: 1.1 ...cloudfront.net (CloudFront)`、`x-cache: Hit from cloudfront`) |

メモ:

- 2026-11-17 の一次 HTTP 取得で、`https://search.freshnessburger.co.jp/` は Next.js + CloudFront で配信される Canly (`canly` クラス・アセット) ベースの店舗検索サイトであることを確認した
- `__NEXT_DATA__` 内の設定値として `"mapMapSetting":"leaflet"` が記録されており、地図描画設定は Leaflet になっていることを確認した

データの出どころ (2026-11-17):

- 店舗データ: 株式会社フレッシュネス (Canly 基盤経由)
- 背景地図: 未確認 (Leaflet 設定を確認)
