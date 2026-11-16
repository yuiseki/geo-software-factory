# DCM 店舗検索

- URL: https://www.dcm-hc.co.jp/shop/search/list_point.html
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ホームセンター、DCM、DCMカーマ、DCMダイキ、DCMホーマック、DIY、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の DCM 店舗を現在地や条件・地域から検索し、店舗詳細やチラシ情報を確認できる公式店舗検索サイト |
| 提供する価値 | 近隣のホームセンターを探し、営業時間・取扱サービス・チラシ情報・店舗所在地へのアクセス手段をまとめて確認できる |
| 想定する利用者 | 日用品や DIY 資材、園芸用品の購入で最寄りの DCM 店舗へ来店する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客およびチラシ・ネット取り置き等のオムニチャネル導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗売上への送客に貢献する集客基盤 |
| 運営 | 企業 (DCM株式会社) |
| 推定の運用費 | 推測: 月数万〜数十万円。Web サーバーの運用費および Google Maps 関連の利用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (参考の事前調査による。一次 HTTP 取得の `/common/js/shopSearch.js` 内で緯度経度 `lat`/`lng` および `https://www.google.com/maps?q=...` への導線を確認) |
| フレームワーク | 独自 JavaScript (`/common/js/import.js`、`/common/js/shop.js`、`/common/js/shopSearch.js`、`/common/js/shopDetail.js`) |
| 背景の地図とタイル | Google Maps (詳細ページの HTML 上では `https://www.google.com/maps?q=...` へのリンクを確認。埋め込み描画の詳細は未確認) |
| 投稿やデータの保存先 | 自社管理の店舗情報基盤 (`https://www.dcm-hc.co.jp/shop/detail/...` の静的またはサーバー生成 HTML および検索用 JS データ) |
| 配信 | nginx (`server: nginx`) |

メモ:

- 2026-11-17 の一次 HTTP 取得 (`https://www.dcm-hc.co.jp/shop/search/list_point.html` および `/shop/detail/01_0258.html`) では HTTP/2 200 を確認した
- 店舗詳細ページの HTML 内には Google マップへの外部リンク (`https://www.google.com/maps?q=...`) が含まれており、検索一覧側では `/common/js/shopSearch.js` が動作している

データの出どころ (2026-11-17):

- 店舗データ: DCM株式会社自社管理の店舗情報
- 背景地図: Google Maps (参考調査および検索 JS 内の参照より)
