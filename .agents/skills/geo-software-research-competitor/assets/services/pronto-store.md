---
financial: commercial
organization: corp-smb
---

# プロント 店舗検索

- URL: https://shop.pronto.co.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、カフェ、バー、プロント、PRONTO、キッサカバ、営業時間、Canly、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | カフェ・バー「PRONTO」や「キッサカバ」などプロントグループ各店舗を地域・ブランド・地図から検索できる公式店舗検索サイト |
| 提供する価値 | 都道府県・駅名・キーワード・地図 (`/map`) から最寄りのプロント店舗を探し、カフェ/バーそれぞれの営業時間やメニュー・設備を確認できる |
| 想定する利用者 | PRONTO や姉妹ブランドへの来店を予定している一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客・情報基盤 |
| 運営 | 企業 (株式会社プロントコーポレーション。店舗情報・ストアロケーター基盤は株式会社カンリー / Canly を利用) |
| 推定の運用費 | 推測: 月十万〜数十万円。Canly のストアロケーター SaaS 利用料および Google Maps API 利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`https://maps.googleapis.com/maps/api/js`、`google.maps.Map`、`Marker`、`InfoWindow`、`OverlayView` 等を `/map` ページのチャンクで利用) |
| フレームワーク | Next.js (`x-powered-by: Next.js`、Canly ストアロケーター基盤) |
| 背景の地図とタイル | Google Maps (`maps.googleapis.com/maps/api/js`。共通 `_app` バンドル内には Leaflet 用設定フラグも含まれるが `/map` では Google Maps を読み込み) |
| 投稿やデータの保存先 | Canly API (`https://api.site.can-ly.com`)、画像は `https://meocloud-image.can-ly.com` |
| 配信 | Amazon CloudFront (`via: CloudFront`, `x-cache: Hit from cloudfront`) |

メモ:

- プロントコーポレーション全体の総店舗数は約 288〜291 店舗 (PRONTO 単体で約 183〜186 店舗)
- Canly の共通 Next.js ストアロケーター基盤を採用しており、ヴィ・ド・フランス (`shop.viedefrance.co.jp`) と同一のアーキテクチャ・チャンク構成を持つ

データの出どころ (2026-11-17):

- 店舗データ: 株式会社プロントコーポレーション (Canly 経由で配信)
- 背景地図: Google Maps Platform
