---
financial: commercial
organization: corp-ent
first_seen: 2026-07-06
first_seen_by: wayback
---

# サブウェイ 店舗検索

- URL: https://subway.co.jp/shop/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、サンドイッチ、ファストフード、サブウェイ、SUBWAY、営業時間、店舗マップ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のサブウェイ店舗を、エリア・キーワード・現在地から検索し、店舗情報やマップを確認できる公式店舗検索サイト |
| 提供する価値 | 最寄りのサブウェイ店舗の場所、営業時間、メニューやサービス対応状況を確認し、来店や注文へ進める |
| 想定する利用者 | サブウェイを利用したい一般客、ランチやテイクアウト先を探す人 |
| 商用か非商用か | 商用 (実店舗への来店送客および注文導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (WATAMI FAST CASUAL MANAGEMENT株式会社) |
| 推定の運用費 | 推測: 月数万円〜。Amazon Linux 上の Apache サーバー運用費および Google Maps API 利用料 |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (Maps Static API を `shop.js` 内で参照。マップページ `/shop/map/` では `window.GOOGLE_MAPS_API_KEY` を設定。事前調査: Google Maps) |
| フレームワーク | Vanilla JS (ES Modules: `/assets/js/shop.js`) |
| 背景の地図とタイル | Google マップ (Maps Static API 等) |
| 投稿やデータの保存先 | 自社店舗データ (`/shop/map/` では HTML 内の `window.SHOP_MAP_DATA` に店舗配列 JSON を埋め込み) |
| 配信 | Apache (`server: Apache/2.4.67 (Amazon Linux) OpenSSL/3.5.5`) |

メモ:

- 2026-11-17 の一次 HTTP 取得で、`https://subway.co.jp/shop/` は Amazon Linux 上の Apache から配信されており、ES Modules 構成の `/assets/js/shop.js` を読み込んでいることを確認した
- `/shop/map/` の HTML 内に `window.SHOP_MAP_DATA` (全店舗 JSON 配列) と `window.GOOGLE_MAPS_API_KEY` が埋め込まれており、`shop.js` で `https://maps.googleapis.com/maps/api/staticmap` を参照していることを確認した

データの出どころ (2026-11-17):

- 店舗データ: WATAMI FAST CASUAL MANAGEMENT株式会社
- 背景地図: Google (事前調査および Google Maps API キー・Static API 参照の観測による)
