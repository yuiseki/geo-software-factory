---
financial: commercial
organization: corp-ent
---

# ケーヨーデイツー (現 DCM) 店舗検索

- URL: https://www.dcm-hc.co.jp/shop/search/list_point.html
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ケーヨーデイツー、DCM、ホームセンター、DIY、園芸、店舗一覧、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 旧ケーヨーデイツーを含む全国の DCM ホームセンター店舗を一覧・地図から検索できる公式店舗検索ページ |
| 提供する価値 | 都道府県や条件、地図上のマーカーから最寄りの DCM 店舗を探し、営業時間や取扱サービス、チラシ情報を確認して来店できる |
| 想定する利用者 | DIY 用品、園芸用品、日用品、リフォーム資材などの購入でホームセンターへ来店したい一般客・事業者 |
| 商用か非商用か | 商用 (実店舗への来店および店舗取り置き・チラシ販促のために DCM 株式会社が提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。全国のホームセンター実店舗での販売売上に貢献する集客基盤 |
| 運営 | 企業 (DCM 株式会社 / 旧・株式会社ケーヨーを 2024年9月に吸収合併) |
| 推定の運用費 | 推測: 月数万円〜十数万円。自社店舗検索システムの運用費および Google Maps JavaScript API の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`/common/js/shopSearch.js` 内で `google.maps.LatLng`、`google.maps.LatLngBounds`、`google.maps.Marker` を使用) |
| フレームワーク | 独自フロントエンド JS (`/common/js/import.js`、`/common/js/shop.js`、`/common/js/shopSearch.js`) |
| 背景の地図とタイル | Google Maps (Google Maps JavaScript API) |
| 投稿やデータの保存先 | 自社管理の店舗データ (JSON 形式で `rt_bn_shops_json_list` 等を返却) |
| 配信 | nginx (`server: nginx`、`x-cacheable: YES`、`x-frame-options: SAMEORIGIN`) |

メモ:

- 旧・株式会社ケーヨーは 2024年9月1日に DCM 株式会社へ吸収合併され、「ケーヨーデイツー」の屋号も順次「DCM」へ統合された
- 2026-11-17 の一次 HTTP 取得 (`https://www.dcm-hc.co.jp/shop/search/list_point.html` および `/common/js/shopSearch.js`) で、Google Maps JavaScript API によるマーカー表示と店舗 JSON リスト (`rt_bn_shops_json_list`) の読み込みを確認した

データの出どころ (2026-11-17):

- 店舗データ: DCM 株式会社自社管理の店舗情報
- 背景地図: Google Maps (Google Maps JavaScript API)
