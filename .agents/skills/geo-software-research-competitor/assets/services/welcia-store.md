---
financial: commercial
organization: corp-ent
first_seen: 2023-11-04
first_seen_by: wayback
---

# ウエルシア 店舗検索

- URL: https://store.welcia.co.jp/welcia/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ストアロケーター、店舗検索、ドラッグストア、ウエルシア、調剤薬局、24時間営業、処方箋、チラシ、営業時間、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のウエルシアグループ店舗を現在地・住所・駅・サービス条件から検索して地図上に表示する公式店舗検索サイト |
| 提供する価値 | 最寄り店舗の位置、営業時間（24 時間営業など）、調剤受付や取扱商品・サービス条件を素早く確認し、来店や処方箋利用に繋げられる |
| 想定する利用者 | ウエルシアグループの利用客、外出先で営業中のドラッグストアや調剤薬局を探している利用者 |
| 商用か非商用か | 商用 (実店舗への来店送客およびチラシ・調剤案内への導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (ウエルシア薬局株式会社) |
| 推定の運用費 | 推測: 月数十万円。NAVITIME Location Cloud (法人向け店舗検索 ASP) の利用料がかかる |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME Location Cloud (ブラウザ観測で NAVITIME Location Cloud およびゼンリン地図を確認。一次 HTTP 取得でも `has_navitime: true`) |
| フレームワーク | jQuery (`jquery-3.7.1.min.js`)、各種ポリフィル・レガシー対応スクリプト (`html5shiv.min.js`、`es5-shim.min.js`、`iframeResizer.contentWindow.min.js` 等) |
| 背景の地図とタイル | ゼンリン地図 (NAVITIME Location Cloud 経由で提供) |
| 投稿やデータの保存先 | NAVITIME Location Cloud 側の店舗検索データベース |
| 配信 | Apache (`server: Apache`) |

メモ:

- 2026-11-16 のブラウザ観測で NAVITIME Location Cloud を利用しており、背景地図がゼンリンであることを確認した
- 一次 HTTP 取得 (`https://store.welcia.co.jp/welcia/`) でも `has_navitime: true` が検出され、`//store.welcia.co.jp/welcia/resources/js/` 配下のスクリプト群が確認された
- 公式スマートフォンアプリとして「ウエルシアグループアプリ」（会員証・クーポン・WAON POINT / Vポイント連携・店舗検索等）が提供されている

データの出どころ (2026-11-16):

- 店舗データ: ウエルシア薬局株式会社 / NAVITIME Location Cloud
- 背景地図: 株式会社ゼンリン (NAVITIME Location Cloud 経由)
