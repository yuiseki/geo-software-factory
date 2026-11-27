---
financial: commercial
organization: corp-ent
first_seen: 2022-02-19
first_seen_by: wayback
---

# カワチ薬品 店舗検索

- URL: https://www.cawachi.co.jp/customer/store/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ドラッグストア、カワチ薬品、CAWACHI、調剤薬局、Google Maps、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 関東・東北・甲信越を中心に展開するカワチ薬品の店舗を地図・現在地・条件から検索し、店舗詳細を確認できる公式店舗検索サイト |
| 提供する価値 | 地図上のマーカーや現在地周辺検索から最寄りのカワチ薬品店舗を探し、吹き出しや詳細ページで営業時間・駐車場・調剤対応等を確認できる |
| 想定する利用者 | カワチ薬品を利用する一般客、郊外型大型ドラッグストアを探している生活者 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社カワチ薬品) |
| 推定の運用費 | 推測: 月数万円。Cloudflare + Varnish + WordPress の運用費と Google Maps JavaScript API の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`/_assets/corp/store.js` 内で `new google.maps.Map(document.getElementById('js-search-map'), ...)`、`google.maps.Marker`、`google.maps.InfoWindow` を使用) |
| フレームワーク | WordPress + 独自 JS バンドル (`/_assets/corp/store.js`、`/customer/_assets/main.module.bundle.js`) + jQuery 3.3.1 (GA4 / GTM) |
| 背景の地図とタイル | Google マップ (Google Maps JavaScript API) |
| 投稿やデータの保存先 | WordPress 側で店舗ページ (`/customer/store/<slug>/`) を生成し、`store.js` 側で店舗座標を描画 |
| 配信 | Cloudflare + Varnish (`server: cloudflare`、`via: 1.1 varnish (Varnish/6.0)`、`cf-ray: ...-NRT`) |

メモ:

- 2026-11-17 の HTTP 観測では、店舗検索ページで読み込まれる `/_assets/corp/store.js` のコード内に `google.maps.Map`、`google.maps.LatLng`、`google.maps.Marker`、`google.maps.InfoWindow` の実装があることを確認した
- 一部の個別店舗ページ (`/customer/store/kuramochi/`) の静的 HTML には地図 iframe は含まれていなかった

データの出どころ (2026-11-17):

- 店舗データ: 株式会社カワチ薬品
- 背景地図: Google (Google Maps JavaScript API)
