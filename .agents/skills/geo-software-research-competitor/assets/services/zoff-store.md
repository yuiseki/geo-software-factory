---
financial: commercial
organization: corp-ent
first_seen: 2018-09-08
first_seen_by: wayback
---

# Zoff 店舗検索

- URL: https://www.zoff.co.jp/shop/store/search.aspx
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、眼鏡、メガネ、サングラス、Zoff、ゾフ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の Zoff 店舗をエリアやキーワードから検索し、店舗詳細ページで地図や営業時間を確認できる公式店舗検索ページ |
| 提供する価値 | Zoff オンラインストアと同一ドメイン上で最寄り店舗を探し、店舗の地図・営業時間・取扱情報を確認できる |
| 想定する利用者 | メガネやサングラスの購入・調整・店舗受取のために Zoff の実店舗へ来店する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客および公式オンラインストアとの連携として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗販売および EC 送客に貢献する集客基盤 |
| 運営 | 企業 (株式会社ゾフ / 株式会社インターメスティック) |
| 推定の運用費 | 推測: 月数万〜数十万円。EC 統合基盤と Amazon CloudFront の配信費、Google Maps API の利用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (店舗詳細 `/shop/store/11034` にて `maps.googleapis.com/maps/api/js` および `google.com/maps/embed/v1/place` を確認) |
| フレームワーク | ASP.NET Web Forms (`search.aspx`、`list.aspx`)、jQuery 3.5.1 (`jquery.min.js`)、Magnific Popup、独自 JS (`shopsearch.js`) |
| 背景の地図とタイル | Google Maps (Maps JavaScript API および Maps Embed API) |
| 投稿やデータの保存先 | 自社 EC 統合基盤 (`www.zoff.co.jp/shop/store/`) |
| 配信 | Amazon CloudFront (`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 観測では、検索トップ (`/shop/store/search.aspx`) ではなく個別の店舗詳細ページ (`/shop/store/11034` 等) 側で Google Maps JavaScript API と Maps Embed API の呼び出しを確認した
- 店舗検索は独立ドメインではなく EC サイト (`www.zoff.co.jp`) 内の機能として統合されている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社ゾフ自社管理の店舗情報
- 背景地図: Google Maps
