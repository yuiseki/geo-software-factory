---
financial: commercial
organization: corp-ent
---

# ルートインホテルズ 地図から探す・ホテル一覧

- URL: https://www.route-inn.co.jp/hotel_list/area/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ホテル検索、ルートイン、ホテルルートイン、ビジネスホテル、GOGA、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のホテルルートイン (360 施設以上) をエリア・地図や各ホテルのアクセスページから検索し予約できる公式ホテル検索サイト |
| 提供する価値 | 都道府県別のホテル一覧と個別ホテルページの周辺地図・駐車場・マップコード案内により、車や鉄道での出張先近くの宿泊拠点を見つけられる |
| 想定する利用者 | 車・電車での国内出張者や観光旅行者など、ルートインホテルズ各施設の予約を検討している利用者 |
| 商用か非商用か | 商用 (自社予約システムへの宿泊予約送客として提供。検索ページの利用料は無料) |
| 推定の売上 | 推測: ホテル検索単体の売上は 0 円。ルートインジャパングループ (2026年3月期連結売上高 約1,954億円、ホテル 368施設) の宿泊売上に貢献 |
| 運営 | 企業 (ルートインジャパン株式会社 / ルートイングループ。店舗検索・地図部分は株式会社ゴーガの StoreLocator を採用) |
| 推定の運用費 | 推測: 月数十万円。Apache による自社サイト運用費に加え、StoreLocator (`route-inn.storelocator.jp`) の SaaS 利用料および Google Maps JavaScript API の従量課金がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 各ホテルのアクセス・駐車場ページ (`/hotel_list/.../parking/#gmap`) で `<iframe src="https://route-inn.storelocator.jp/detail/<id>/?iframe">` を埋め込み、iframe 内で Google Maps JavaScript API (`maps.googleapis.com/maps/api/js?v=quarterly&libraries=geometry,places,visualization`) と GOGA StoreLocator (`/static/bundle-4b49ea093bf637ae6d41.js`) を使用 |
| フレームワーク | jQuery 3.5.1 (本体サイト)、予約導線に tripla SDK (`tripla.min.js`)、地図 iframe 側は webpack バンドルされた StoreLocator |
| 背景の地図とタイル | Google マップ (Google Maps JavaScript API 経由) |
| 投稿やデータの保存先 | 本体はサーバー側生成 HTML (`/hotel_list/...`)、地図・周辺情報は `route-inn.storelocator.jp` 側で保持 |
| 配信 | Apache (`Server: Apache`) |

メモ:

- 本体ページ側では地図コンテナのクラス名に `class="p-navitime"` が残っているが、実際に埋め込まれている iframe 先は `route-inn.storelocator.jp` (GOGA StoreLocator + Google Maps API) になっている

データの出どころ (2026-11-17):

- ホテルデータ: ルートインジャパン株式会社管理のホテル情報
- 背景地図: Google (Google Maps Platform)
- 地図検索システム: 株式会社ゴーガ (GOGA StoreLocator)
