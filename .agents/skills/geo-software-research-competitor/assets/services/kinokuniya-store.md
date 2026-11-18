---
financial: commercial
organization: corp-ent
---

# 紀伊國屋書店 Store Locator

- URL: https://store.kinokuniya.co.jp/store-locator/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、紀伊國屋書店、KINOKUNIYA、書店、本屋、店舗一覧、MapLibre、OpenStreetMap、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の紀伊國屋書店 (国内および海外店舗) を地図とリストから探せる公式ストアロケーター |
| 提供する価値 | 地図上のピンや検索欄から最寄りの紀伊國屋書店を探し、住所、電話番号、営業時間や店舗ページへの導線を確認できる |
| 想定する利用者 | 書籍・雑誌の購入や店頭受け取りのために最寄りの紀伊國屋書店を探す一般客および海外店舗の利用者 |
| 商用か非商用か | 商用 (実店舗への来店送客のために株式会社紀伊國屋書店が提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗での書籍・雑貨販売およびウェブストアとの連携に貢献する集客基盤 |
| 運営 | 企業 (株式会社紀伊國屋書店) |
| 推定の運用費 | 推測: 月数千円〜数万円。ノーコードの Elfsight Store Locator ウィジェットを利用しており、Google Maps ではなく MapLibre GL JS + OpenStreetMap (Stadia Maps) ベースの地図表示で運用コストを抑えている |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Elfsight Store Locator の iframe (`https://edb98f70651a498596555fa2e5d11089.elf.site`) 経由で MapLibre GL JS (`.maplibregl-map`、DOM/Canvas 描画) |
| フレームワーク | WordPress (`wp-content/themes/kino-production`) + jQuery + Elfsight Store Locator ウィジェット (`storeLocator.js` v1.25.1) |
| 背景の地図とタイル | OpenStreetMap (参考の事前調査では Stadia Maps タイルを利用。ウィジェットの `storeLocator.js` 内に MapLibre GL JS の vector/raster タイル定義を確認) |
| 投稿やデータの保存先 | Elfsight クラウド基盤 + 自社管理の店舗情報 |
| 配信 | nginx (`Server: nginx`)、ウィジェット本体は Elfsight CDN (`static.elfsight.com`、`universe-static.elfsightcdn.com`) |

メモ:

- 2026-11-17 の一次 HTTP 取得で、`https://store.kinokuniya.co.jp/store-locator/` は WordPress 上のページであり、Elfsight の iframe (`https://edb98f70651a498596555fa2e5d11089.elf.site`) を読み込んでいることを確認した
- ウィジェットの JS (`storeLocator.js`) には `.maplibregl-map` (MapLibre GL JS) が組み込まれており、参考の事前調査では OpenStreetMap (Stadia Maps) タイルが使われている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社紀伊國屋書店自社管理の店舗情報 (Elfsight Store Locator 経由で配信)
- 背景地図: OpenStreetMap (Stadia Maps タイル、MapLibre GL JS で描画)
