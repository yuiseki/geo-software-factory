---
financial: commercial
organization: corp-ent
first_seen: 2020-08-04
first_seen_by: wayback
---

# ユニクロ 店舗検索 (UNIQLO Store Locator)

- URL: https://map.uniqlo.com/jp/ja/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ストアロケーター、店舗検索、ユニクロ、UNIQLO、アパレル、店舗在庫、営業時間、免税、大型店、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のユニクロ店舗をエリア・キーワード・取扱商品やサービス条件で検索し、地図上で場所と営業時間を確認できる公式店舗検索サイト |
| 提供する価値 | 来店前に最寄り店舗の位置、営業時間、大型店・小型店や各種サービスの有無、Google マップでの経路リンクを確認できる |
| 想定する利用者 | ユニクロで買い物を予定している一般客、特定の取扱商品やサービス対応店舗を探している利用者 |
| 商用か非商用か | 商用 (実店舗への来店送客と EC サイトとの連携を目的として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗およびオンラインストアの売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社ユニクロ / ファーストリテイリンググループ) |
| 推定の運用費 | 推測: 月数十万〜数百万円。Google Maps JavaScript API のマップロード課金と、Akamai 経由の配信・API 運用費がかかる |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`https://maps.googleapis.com/maps/api/js?`、`google.maps.Map`) |
| フレームワーク | React (`@react-google-maps/api` を使用、JS バンドル `./static/js/main.162be17d.js`) |
| 背景の地図とタイル | Google マップ (Google Maps Platform) |
| 投稿やデータの保存先 | 自社の店舗検索 API (`/api/storelocator/v1/`) |
| 配信 | nginx + Akamai (`server: nginx`、Akamai Bot Manager / mPulse のヘッダ・スクリプトを確認) |

メモ:

- グローバル共通の店舗検索基盤 (`map.uniqlo.com/<country>/<lang>/`) として構築されており、各国版のルート URL を JS バンドル内に保持している
- ルート案内リンクとして `https://www.google.com/maps/dir/?api=1&destination=` を生成している

データの出どころ (2026-11-16):

- 店舗データ: ユニクロ自社 API (`/api/storelocator/v1/`)
- 背景地図・タイル: Google (Google Maps Platform)
