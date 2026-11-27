---
financial: commercial
organization: corp-ent
first_seen: 2025-06-03
first_seen_by: wayback
---

# 眼鏡市場 店舗検索

- URL: https://shop.meganeichiba.jp/meganeichiba/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、眼鏡、メガネ、補聴器、コンタクト、眼鏡市場、メガネトップ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の眼鏡市場店舗をエリア・現在地・取扱商品から検索し、営業時間やアクセスを確認できる公式店舗検索サイト |
| 提供する価値 | 最寄り店舗の所在地や駐車場・補聴器取扱などの条件を一覧と地図で探し、来店予約や店舗訪問につなげられる |
| 想定する利用者 | メガネやコンタクトレンズ、補聴器の購入・調整のために眼鏡市場の店舗を探す一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客および来店予約の導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗での眼鏡・補聴器販売への送客に貢献する集客基盤 |
| 運営 | 企業 (株式会社メガネトップ) |
| 推定の運用費 | 推測: 月数万〜数十万円。NAVITIME Location Cloud の SaaS 利用料および店舗データ連携の運用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME Location Cloud (参考の事前調査およびページ内の `location-cloud.navitime.co.jp` 導線、`navitime_logo.gif` 等から確認) |
| フレームワーク | jQuery 3.7.1 (`jquery-3.7.1.min.js`)、Bootstrap、jsrender、iframeResizer |
| 背景の地図とタイル | NAVITIME Location Cloud (一次 HTTP 取得ではロゴおよびアセット `image.pkg.navitime.co.jp/citrus/583/` を確認、タイル URL 詳細は未確認) |
| 投稿やデータの保存先 | NAVITIME Location Cloud 基盤 (`shop.meganeichiba.jp` / `images.pkg.navitime.co.jp`) |
| 配信 | Apache (`server: Apache`) |

メモ:

- 2026-11-17 の一次 HTTP 観測 (`https://shop.meganeichiba.jp/meganeichiba/`) では `HTTP/2 200` を確認した
- ページ内に `https://location-cloud.navitime.co.jp/` へのリンクや `image.pkg.navitime.co.jp/citrus/583/` のアセット、`navitime_logo.gif` が含まれており、NAVITIME Location Cloud 製の店舗検索パッケージであることが確認できた

データの出どころ (2026-11-17):

- 店舗データ: 株式会社メガネトップ管理の店舗情報 (NAVITIME Location Cloud 上で配信)
- 背景地図: NAVITIME Location Cloud
