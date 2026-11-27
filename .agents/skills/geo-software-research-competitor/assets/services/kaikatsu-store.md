---
financial: commercial
organization: corp-ent
first_seen: 2012-08-06
first_seen_by: wayback
---

# 快活CLUB 店舗検索・料金案内

- URL: https://www.kaikatsu.jp/shop/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、快活CLUB、ネットカフェ、漫画喫茶、鍵付完全個室、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の快活CLUB店舗をエリア・設備・現在地 (GPS) から検索し、席種や料金表、空席状況を確認できる公式店舗検索サイト |
| 提供する価値 | 鍵付完全個室やシャワー、無料モーニング、駐車場の有無などで店舗を絞り込み、現在地から近い店舗を Google マップ上で探せる |
| 想定する利用者 | テレワーク、休憩、宿泊代わり、漫画・動画鑑賞などでネットカフェを探しているビジネス客や一般客 |
| 商用か非商用か | 商用 (快活CLUB各店舗への来店送客および公式アプリ会員獲得のために提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の利用料金・飲食売上に貢献 |
| 運営 | 企業 (株式会社快活フロンティア) |
| 推定の運用費 | 推測: 月数十万円。Amazon S3 + Amazon CloudFront による静的ホスティング費と、GPS 検索ページ (`/shop/gps/`) の Google Maps JavaScript API 利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`https://maps.googleapis.com/maps/api/js?key=...&libraries=geometry` を `/shop/gps/` で使用) |
| フレームワーク | jQuery 3.2.1 + 独自 JS (`/common/js/shop.js`, `/common/js/gps.js`) |
| 背景の地図とタイル | Google マップの地図タイル |
| 投稿やデータの保存先 | 自社静的 JS データ (`/shop/data/shop.js`) |
| 配信 | Amazon S3 + Amazon CloudFront (`server: AmazonS3`、`via: ...cloudfront.net`) |

メモ:

- `/shop/` トップでは静的 JS データ (`/shop/data/shop.js`) を用いた店舗検索を提供し、現在地検索ページ (`/shop/gps/`) にて Google Maps JavaScript API (Geometry ライブラリ含む) を読み込んでいる
- サイト全体が Amazon S3 上の静的ファイルと CloudFront CDN で配信されており、軽量なサーバーレス構成となっている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社快活フロンティア自社管理の店舗情報 (`/shop/data/shop.js`)
- 背景地図: Google Maps Platform
