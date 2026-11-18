---
financial: commercial
organization: corp-ent
---

# セブン銀行 ATM検索

- URL: https://location.sevenbank.co.jp/sevenbank/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ATM検索、コンビニATM、セブン銀行、セブンイレブン、現金引出、スマホATM、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のセブン-イレブンや商業施設・駅・空港等に設置されたセブン銀行 ATM を現在地・エリア・駅・路線から検索し、地図上に表示する公式 ATM 検索サイト |
| 提供する価値 | 24 時間稼働やスマホ ATM 対応、音声ガイダンス対応、海外発行カード対応など利用条件に合う最寄り ATM を地図と詳細ページですぐ確認できる |
| 想定する利用者 | 現金の入出金・スマホ ATM・電子マネーチャージ等を利用したい一般消費者や訪日外国人旅行者 |
| 商用か非商用か | 商用 (全国の ATM 稼働率向上および提携金融機関利用者の送客基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 検索サイト単体の売上は 0 円。国内約 28,000〜28,600 台以上の ATM 利用に伴う受入手数料収益に貢献 |
| 運営 | 企業 (株式会社セブン銀行) |
| 推定の運用費 | 推測: 月数十万〜百万円規模。NAVITIME Location Cloud の法人向け店舗・ATM 検索 ASP 利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME Location Cloud (`//pkg.navitime.co.jp/sevenbank/api/map/tilemap`) |
| フレームワーク | jQuery 3.7.1 (`jquery-3.7.1.min.js`)、JsRender、Slick、iframeResizer |
| 背景の地図とタイル | NAVITIME 地図タイル (`https://alttile.pkg.navitime.co.jp/` および `pkg.navitime.co.jp`) |
| 投稿やデータの保存先 | 株式会社ナビタイムジャパンの NAVITIME Location Cloud 基盤 (`location.sevenbank.co.jp` / `pkg.navitime.co.jp`) |
| 配信 | Apache (`server: Apache`) |

メモ:

- 拠点詳細ページ (`/sevenbank/spot/detail?code=...`) において `//pkg.navitime.co.jp/sevenbank/api/map/tilemap` と `https://alttile.pkg.navitime.co.jp/` を使った地図描画を確認した
- アイコン画像等は `image.pkg.navitime.co.jp/citrus/...` から配信されており、NAVITIME Location Cloud の標準パッケージ構成である

データの出どころ (2026-11-17):

- ATM データ: 株式会社セブン銀行管理の ATM 設置情報
- 背景地図・検索基盤: 株式会社ナビタイムジャパン (NAVITIME Location Cloud)
