# オーケー 店舗一覧と検索

- URL: https://ok-corporation.jp/shop/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、スーパー、ディスカウントスーパー、オーケー、OKストア、オーケーストア、Google マイマップ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ディスカウントスーパーマーケット「オーケー」の全店舗を、地域・条件検索および Google マイマップの埋め込みから探せる公式店舗検索サイト |
| 提供する価値 | 首都圏・関西圏のオーケー店舗をエリアや駐車場・駐輪場などの条件、地図上の全店ピンから探し、営業時間やアクセスマップを確認できる |
| 想定する利用者 | オーケー各店舗への来店を予定している一般客、新店舗や駐車場付き店舗を探している利用者 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。営業収益 約 7,557 億円 (2026 年 3 月期) の実店舗送客に貢献 |
| 運営 | 企業 (オーケー株式会社) |
| 推定の運用費 | 推測: 月数万円。CMS (a-blog cms) と nginx サーバーの運用費程度で、地図は無料の Google マイマップと Google Maps 埋め込み `iframe` を利用 |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 店舗一覧トップ (`/shop/`) に Google マイマップの埋め込み `iframe` (`https://www.google.com/maps/d/embed?mid=1ku7qxZnOHPQIjCCdI_Ypv4euyw-5M75a`)、個別店舗ページ (`/shop/aobadai.html` 等) に Google マップの `iframe` (`https://www.google.com/maps/embed?pb=...`) を埋め込み |
| フレームワーク | a-blog cms (`/acms.js`)、jQuery 3.6.1、jQuery Migrate 3.0.1、Modernizr |
| 背景の地図とタイル | Google マップ (Google マイマップ埋め込みおよび Google Maps `embed?pb=`) |
| 投稿やデータの保存先 | a-blog cms 上で店舗データを管理 (`/shop/keyword/...` 等)。多言語化に shutto翻訳 (`d.shutto-translation.com`) を利用 |
| 配信 | nginx (`server: nginx`) |

メモ:

- 店舗数は 174 店舗 (2026 年 3 月期末時点) で、首都圏に加え関西圏へも展開中
- Google Maps JavaScript API の従量課金を避けつつ、トップページは Google マイマップ、個別店舗ページは Google Maps 埋め込み `iframe` で地図表示を実現している

データの出どころ (2026-11-17):

- 店舗データ: オーケー株式会社
- 埋め込み地図: Google マイマップ / Google マップ
