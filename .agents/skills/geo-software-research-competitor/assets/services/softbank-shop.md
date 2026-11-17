# ソフトバンクショップ 店舗検索

- URL: https://www.softbank.jp/shop/search/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ソフトバンクショップ、SoftBank、携帯電話、来店予約、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のソフトバンクショップ・取扱店を現在地、キーワード、都道府県・市区町村から検索し、店舗詳細や来店予約へ進める公式店舗検索サービス |
| 提供する価値 | 周辺店舗の空き状況や営業時間、取り扱いサービスを確認し、マップ上で位置を把握して来店予約へつなげられる |
| 想定する利用者 | 携帯電話の新規契約、機種変更、プラン見直し、故障受付などのためソフトバンク店舗への来店を希望する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客と事前予約促進のために提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗での契約獲得・アップセルおよびサポート対応に貢献 |
| 運営 | 企業 (ソフトバンク株式会社) |
| 推定の運用費 | 推測: 月数十万〜数百万円。店舗検索 API サーバー運用費に加え、Mapbox GL JS・カスタムスタイル利用料および Yahoo! 逆ジオコーディング API 利用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Mapbox GL JS v1.10.1 (`https://api.tiles.mapbox.com/mapbox-gl-js/v1.10.1/mapbox-gl.js` を `/shop/search/locationlist/` 等で利用) |
| フレームワーク | jQuery 3.6.1 |
| 背景の地図とタイル | Mapbox カスタムスタイル (`mapbox://styles/softbank-cpp/ckfx3x18r08ac19qwzr8w1did`) |
| 投稿やデータの保存先 | 自社店舗検索 API (`/shop/d/system/v1/api/shop-info-list/`、`shop-detail/`、`shop-search/`、`suggest/`) および Yahoo! 逆ジオコーディング API (`https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder`) |
| 配信 | 未確認 (`HTTP/2 200` を確認したがレスポンスヘッダに Web サーバーや CDN の製品名は出力されない) |

メモ:

- `/shop/search/locationlist/` の JS (`/shop/set/data/search/locationlist/js/shared/index.v2.min.js`) 内で `mapboxgl.Map` とソフトバンク専用の Mapbox Studio スタイルを指定していることを確認した
- 一覧や詳細画面では `https://www.softbank.jp/shop/d/system/v1/api/` 配下の JSON API から店舗情報を取得している

データの出どころ (2026-11-17):

- 店舗データ: ソフトバンク株式会社自社管理の店舗情報
- 背景地図: Mapbox (OpenStreetMap 等の地図データをベースにしたカスタムスタイル)
- 逆ジオコーディング: LINEヤフー株式会社 (Yahoo!ジオコーダAPI)
