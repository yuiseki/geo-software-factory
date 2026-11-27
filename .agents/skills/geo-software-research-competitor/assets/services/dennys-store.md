---
financial: commercial
organization: corp-ent
first_seen: 2014-11-10
first_seen_by: wayback
---

# デニーズ 店舗検索

- URL: https://shop.dennys.jp/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ストアロケーター、店舗検索、ファミレス、デニーズ、営業時間、駐車場、宅配、テイクアウト、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のデニーズ店舗を、現在地・エリア・条件から検索して地図上に表示する公式店舗検索サイト |
| 提供する価値 | 近くのデニーズ店舗の位置や営業時間、駐車場・充電設備などの店舗情報を確認でき、来店やテイクアウト利用につなげられる |
| 想定する利用者 | デニーズを利用したい一般客、外出先やドライブ中に近くの店舗を探している利用者 |
| 商用か非商用か | 商用 (実店舗への来店送客およびテイクアウト・デリバリー導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社セブン＆アイ・フードシステムズ) |
| 推定の運用費 | 推測: 月数万〜数十万円。GOGA 店舗検索サービスの利用料と Google Maps Platform の利用料、Google Cloud 側の配信費がかかる |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API + GOGA 店舗検索サービス。一次 HTTP 取得 HTML で Maps JavaScript API の読み込み (`has_gmaps: true`) を確認し、ブラウザ観測で「地図データ ©2026 Google」「Powered by GOGA」を確認 |
| フレームワーク | 未確認 (トップページの一次 HTTP 取得のみ実施) |
| 背景の地図とタイル | Google マップ (Google Maps Platform / 地図データ ©2026 Google) |
| 投稿やデータの保存先 | GOGA 店舗検索基盤・自社店舗データ (API 詳細は未確認) |
| 配信 | Google Frontend (`server: Google Frontend`、`via: 1.1 google`) |

メモ:

- 2026-11-16 のブラウザ観測で「地図データ ©2026 Google」および「Powered by GOGA」の表示を確認した
- 一次 HTTP 取得 (`https://shop.dennys.jp/`) では HTML からも Google Maps JavaScript API の読み込み (`has_gmaps: true`) と `Google Frontend` 配信を確認した
- 公式スマートフォンアプリとして「デニーズアプリ」が提供されている

データの出どころ (2026-11-16):

- 店舗データ: 株式会社セブン＆アイ・フードシステムズ / GOGA 店舗検索基盤
- 背景地図: Google (Google Maps Platform / 地図データ ©2026 Google)
