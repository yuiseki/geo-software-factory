---
financial: commercial
organization: corp-ent
---

# カフェ・ベローチェ (C-United) 店舗検索

- URL: https://c-united.co.jp/search/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、カフェ、カフェ・ベローチェ、珈琲館、カフェ・ド・クリエ、C-United、Wi-Fi、電源、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | カフェ・ベローチェや珈琲館、カフェ・ド・クリエなど C-United 各ブランドの店舗を地図や条件から横断検索できる公式店舗検索サイト |
| 提供する価値 | ブランドやエリア、設備条件から店舗を探し、Google マップ上の位置や店舗詳細・営業時間を確認できる |
| 想定する利用者 | カフェ・ベローチェなど C-United グループのカフェを利用したい一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。グループ各店舗の飲食売上に貢献する送客基盤 |
| 運営 | 企業 (C-United株式会社) |
| 推定の運用費 | 推測: 月数万〜十数万円。Web サーバー (Apache / PHP) の運用費に加え、Google Maps JavaScript API (マップ描画および Geocoding) の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`https://maps.googleapis.com/maps/api/js`、`google.maps.Map`、`Marker`、`InfoWindow`、`Geocoder` を `store.js` で利用) |
| フレームワーク | jQuery 3.5.1、および `store.js` 内にバンドルされたフロントエンドライブラリ (React / Vue 関連モジュールを含む)、バックエンドは PHP 7.4 (`x-powered-by: PHP/7.4.33`) |
| 背景の地図とタイル | Google Maps (`maps.googleapis.com/maps/api/js`) |
| 投稿やデータの保存先 | C-United 管理の店舗情報データ (PHP サーバー側管理) |
| 配信 | Apache (`server: Apache`, `PleskLin`) |

メモ:

- カフェ・ベローチェ単体で約 170 店舗、C-United 全体では約 560〜570 店舗を展開している

データの出どころ (2026-11-17):

- 店舗データ: C-United株式会社
- 背景地図・ジオコーディング: Google Maps Platform
