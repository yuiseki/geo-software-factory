---
financial: commercial
organization: corp-ent
---

# ノジマ 店舗案内

- URL: https://www.nojima.co.jp/shop/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、家電量販店、ノジマ、nojima、店舗案内、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 関東を中心に展開する家電専門店ノジマの店舗を都道府県や条件から探し、詳細ページの地図やアクセスを確認できる公式店舗案内サイト |
| 提供する価値 | 各店舗の営業時間、電話番号、駐車場・最寄駅からの案内、埋め込み地図を一つの店舗詳細ページで確認できる |
| 想定する利用者 | 家電製品や携帯端末の購入・相談でノジマ店舗へ来店する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗売上への送客に貢献する集客基盤 |
| 運営 | 企業 (株式会社ノジマ) |
| 推定の運用費 | 推測: 月数万〜数十万円。Web サーバー運用費および Google Maps JavaScript API の従量課金がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (店舗詳細ページ `/shop/tokyo/seiyunarimasu/` 等にて `//maps.googleapis.com/maps/api/js?key=...&lang=ja` および `/nojimamap.js` を読み込み) |
| フレームワーク | jQuery 3.7.1 (`ajax.googleapis.com`)、jquery.matchHeight.js、jquery.jscrollpane.min.js、jquery-cookie 1.4.1 (WordPress 系の `/shop/feed/` 構造を確認) |
| 背景の地図とタイル | Google Maps (Maps JavaScript API 経由) |
| 投稿やデータの保存先 | 自社管理の店舗情報基盤 (`www.nojima.co.jp/shop/store_prefecture/<都道府県>/` および `/shop/<都道府県>/<店舗>/`) |
| 配信 | nginx (`server: nginx`) |

メモ:

- 2026-11-17 の一次 HTTP 取得 (`https://www.nojima.co.jp/shop/` および店舗詳細ページ) で HTTP/2 200 を確認した
- 店舗詳細ページ内で Google Maps JavaScript API と独自スクリプト `/nojimamap.js` を読み込んで地図を描画している

データの出どころ (2026-11-17):

- 店舗データ: 株式会社ノジマ自社管理の店舗情報
- 背景地図: Google Maps Platform (Maps JavaScript API)
