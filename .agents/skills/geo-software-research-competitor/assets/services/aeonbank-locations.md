---
financial: commercial
organization: corp-ent
first_seen: 2016-02-02
first_seen_by: wayback
---

# イオン銀行 店舗・ATM検索

- URL: https://map.aeonbank.co.jp/aeonbank/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ATM検索、銀行、イオン銀行、イオンモール、WAON、住宅ローン相談、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のイオンモールやイオン・マックスバリュ・ミニストップ等に設置されたイオン銀行の店舗・ATM を検索し、地図上に表示する公式検索サイト |
| 提供する価値 | 近くのイオン銀行店舗 (相談窓口) や ATM の営業時間、WAON チャージ対応、外貨両替・住宅ローン相談などの取扱条件を確認し、来店につなげられる |
| 想定する利用者 | イオン銀行口座・イオンカード・WAON 利用者、ショッピングの合間に相談や入出金を行いたい一般顧客 |
| 商用か非商用か | 商用 (店舗相談窓口・ATM への送客およびグループ商業施設への集客基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 検索サイト単体の売上は 0 円。ATM 利用手数料収益および住宅ローン・資産運用等の相談成約に貢献 |
| 運営 | 企業 (株式会社イオン銀行) |
| 推定の運用費 | 推測: 月数十万円。NAVITIME Location Cloud の法人向け店舗・ATM 検索 ASP 利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME Location Cloud (HTML 内の `location-cloud.navitime.co.jp` リンクおよび `image.pkg.navitime.co.jp/citrus/...` 等の共通テンプレート構成を確認) |
| フレームワーク | jQuery 3.7.1 (`jquery-3.7.1.min.js`)、Bootstrap 3.2.0、JsRender、iframeResizer |
| 背景の地図とタイル | NAVITIME 地図タイル (NAVITIME Location Cloud 基盤) |
| 投稿やデータの保存先 | 株式会社ナビタイムジャパンの NAVITIME Location Cloud 基盤 (`map.aeonbank.co.jp`) |
| 配信 | Apache (`server: Apache`) |

メモ:

- セブン銀行と同じく NAVITIME Location Cloud の共通パッケージ (`/resources/js/...`、`pkg.navitime.co.jp/citrus/...`、`navitime_logo.gif`) を利用しており、英語切り替え (`?lang=en`) にも対応している
- ヘッダーおよびフッターは `www.aeonbank.co.jp/navitime/globalnavi.html` および `footer.html` を読み込む構成になっている

データの出どころ (2026-11-17):

- 店舗・ATM データ: 株式会社イオン銀行管理の拠点情報
- 背景地図・検索基盤: 株式会社ナビタイムジャパン (NAVITIME Location Cloud)
