---
financial: commercial
organization: corp-ent
first_seen: 2023-05-31
first_seen_by: wayback
---

# auショップ 店舗検索

- URL: https://www.au.com/storelocator/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、auショップ、au Style、UQスポット、携帯電話、来店予約、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の au Style・auショップ・UQスポット・トヨタ au取扱店などをエリアや地図から検索し、来店予約ができる公式店舗検索サービス |
| 提供する価値 | 最寄り店舗の営業時間、対応サービス、バリアフリーや外国語対応の有無を確認し、そのままオンラインで来店予約まで完結できる |
| 想定する利用者 | 新規契約、機種変更、料金相談、修理・サポートなどのために実店舗への来店を予定している携帯電話・通信サービスの利用者 |
| 商用か非商用か | 商用 (実店舗への来店送客と窓口予約の効率化のために提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。携帯電話契約や各種サービス契約の店舗売上・解約抑止に貢献する集客基盤 |
| 運営 | 企業 (KDDI株式会社 / 沖縄セルラー電話株式会社) |
| 推定の運用費 | 推測: 月数十万〜数百万円。Adobe Experience Manager (AEM) 基盤と Fastly CDN 配信費、店舗データ基盤、地図タイル (MapTiler / OpenMapTiles) の利用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS (`/etc.clientlibs/au-com/clientlibs/clientlib-site/resources/maplibre/json/style.json` および `clientlib-site` JS バンドル内で実装) |
| フレームワーク | jQuery + Adobe Experience Manager (AEM、`/etc.clientlibs/au-com/...`、`/@adobe/helix-rum-js`) |
| 背景の地図とタイル | MapTiler Planet / OpenMapTiles ベクトルタイル (`/etc.clientlibs/au-com/clientlibs/clientlib-site/resources/maplibre/json/tile.json`、帰属表示: MapTiler / OpenStreetMap contributors) |
| 投稿やデータの保存先 | 自社店舗検索 API (`window.auDataLayer.storeLocator` 経由で都道府県・GPS・パラメータ検索を実行) |
| 配信 | Fastly CDN (`x-served-by: cache-nrt-...`, `x-cache: HIT`) |

メモ:

- `/storelocator/` および `/storelocator/map/` の `clientlib-site` バンドル内に MapLibre GL JS のスタイル設定 (`style.json`) とタイル定義 (`tile.json`) が組み込まれている
- 地図タイルは `tile.json` にて `MapTiler Planet` (TileJSON 2.1.0, OpenMapTiles 形式) が指定されている

データの出どころ (2026-11-17):

- 店舗データ: KDDI株式会社自社管理の店舗・取扱店情報
- 背景地図: MapTiler / OpenStreetMap contributors
