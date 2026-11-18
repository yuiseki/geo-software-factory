---
financial: commercial
organization: corp-ent
---

# 洋服の青山 店舗検索

- URL: https://stores.y-aoyama.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、スーツ、紳士服、洋服の青山、青山商事、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の洋服の青山店舗を都道府県・市区町村・現在地・地図から検索できる公式店舗検索サイト |
| 提供する価値 | 最寄り店舗の所在地、営業時間、駐車場の有無や取扱サービスを地図やエリア階層から確認できる |
| 想定する利用者 | ビジネススーツ、礼服、リクルートスーツ等の購入・採寸で洋服の青山へ来店する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客および公式オンラインストアの店舗受取・試着予約導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗売上への送客に貢献する集客基盤 |
| 運営 | 企業 (青山商事株式会社) |
| 推定の運用費 | 推測: 月数十万円。店舗管理 SaaS「Canly (カンリー)」の利用料、Amazon CloudFront 配信費、Google Maps JavaScript API の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`/map/` ページのチャンク `7d0bf13e-*.js` 等にて Google Maps を使用。HTML 内に `leaflet` / `gsi` の文字列参照も含む) |
| フレームワーク | Next.js (`x-powered-by: Next.js`、`__NEXT_DATA__`) + 店舗検索 SaaS「Canly HP」(`api.site.can-ly.com`、`meocloud-image.can-ly.com`) |
| 背景の地図とタイル | Google Maps (Maps JavaScript API 経由) |
| 投稿やデータの保存先 | Canly API (`api.site.can-ly.com`) および Canly 画像基盤 (`meocloud-image.can-ly.com`) |
| 配信 | Amazon CloudFront (`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 取得 (`https://stores.y-aoyama.jp/` および `/map/`) で HTTP/2 200 を確認した
- `store.joshin.co.jp` (ジョーシン) と同じ Next.js + Canly HP の店舗検索基盤を利用している

データの出どころ (2026-11-17):

- 店舗データ: 青山商事株式会社管理の店舗情報 (Canly 基盤経由で配信)
- 背景地図: Google Maps Platform (Maps JavaScript API)
