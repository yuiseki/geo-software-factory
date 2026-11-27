---
financial: commercial
organization: corp-ent
first_seen: 2024-10-03
first_seen_by: wayback
---

# ジョーシン 店舗検索

- URL: https://store.joshin.co.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、家電量販店、ジョーシン、Joshin、上新電機、店舗一覧、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のジョーシン (Joshin) 店舗をエリア・地図・現在地から検索し、店舗情報やサービス内容を確認できる公式店舗検索サイト |
| 提供する価値 | 都道府県や市区町村、地図上の検索 (`/map/`) から最寄りのジョーシン店舗を探し、営業時間や取扱サービスを確認できる |
| 想定する利用者 | 家電・パソコン・おもちゃ・リフォーム等の購入や相談でジョーシン店舗へ来店する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客および公式通販「Joshin webショップ」との連携基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗売上および EC 送客に貢献する集客基盤 |
| 運営 | 企業 (上新電機株式会社) |
| 推定の運用費 | 推測: 月数十万円。店舗管理 SaaS「Canly (カンリー)」の利用料、Amazon CloudFront 配信費、Google Maps JavaScript API の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`/map/` ページのチャンク `7d0bf13e-*.js` にて `https://maps.googleapis.com/maps/api/js` および React Google Maps ラッパーを確認。HTML 内に `leaflet` / `gsi` の文字列参照も含む) |
| フレームワーク | Next.js (`x-powered-by: Next.js`、`__NEXT_DATA__`) + 店舗検索 SaaS「Canly HP」(`g9ey9rioe.api.hp.can-ly.com`、`meocloud-image.can-ly.com`) |
| 背景の地図とタイル | Google Maps (Maps JavaScript API 経由) |
| 投稿やデータの保存先 | Canly API (`g9ey9rioe.api.hp.can-ly.com`) および Canly 画像基盤 (`meocloud-image.can-ly.com`) |
| 配信 | Amazon CloudFront (`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 取得 (`https://store.joshin.co.jp/` および `/map/`) で HTTP/2 200 を確認した
- `stores.y-aoyama.jp` (洋服の青山) と共通の Next.js + Canly HP テンプレート構成を採用している

データの出どころ (2026-11-17):

- 店舗データ: 上新電機株式会社管理の店舗情報 (Canly 基盤経由で配信)
- 背景地図: Google Maps Platform (Maps JavaScript API)
