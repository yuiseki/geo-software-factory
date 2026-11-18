---
financial: commercial
organization: corp-ent
---

# やよい軒 店舗検索

- URL: https://store.yayoiken.com/b/yayoiken/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、定食、和食、やよい軒、プレナス、営業時間、テイクアウト、ONE COMPATH、Mapion、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のやよい軒店舗を、エリア・条件・地図から検索できる公式店舗検索サイト |
| 提供する価値 | 最寄り店舗の営業時間、駐車場、テイクアウト対応やアクセスを地図上で確認し、来店へ進める |
| 想定する利用者 | やよい軒を利用したい一般客、ランチや夕食、テイクアウト先を探す人 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社プレナス) |
| 推定の運用費 | 推測: 月数万円〜十数万円。株式会社ONE COMPATH (Mapion 店舗検索 ASP) の利用料および CloudFront 配信費 |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet + Mapion (`lbs.mapion.co.jp/jslibs/JSPack.2.1.0.js`, `common-ss2.0/js/client_js/SpotSearch.js`) |
| フレームワーク | jQuery 3.6.0 + ONE COMPATH 店舗検索 ASP (`common-ss2.0`, `proj4.js`) |
| 背景の地図とタイル | ONE COMPATH / Mapion 地図基盤 (事前調査: Leaflet + ONE COMPATH) |
| 投稿やデータの保存先 | ONE COMPATH 店舗検索 ASP 基盤 |
| 配信 | nginx + Amazon CloudFront (`server: nginx`、`via: 1.1 ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 取得で、`https://store.yayoiken.com/b/yayoiken/` は `https://lbs.mapion.co.jp/jslibs/JSPack.2.1.0.js` および `/f/common-ss/common-ss2.0/js/client_js/SpotSearch.js` を読み込んでおり、株式会社ONE COMPATH の店舗検索 ASP (Mapion 地図基盤) と Leaflet を採用していることを確認した

データの出どころ (2026-11-17):

- 店舗データ: 株式会社プレナス (ONE COMPATH 店舗検索 ASP 経由)
- 背景地図: 株式会社ONE COMPATH / Mapion
