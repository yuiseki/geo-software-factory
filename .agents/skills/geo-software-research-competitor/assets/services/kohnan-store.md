---
financial: commercial
organization: corp-ent
first_seen: 2021-07-06
first_seen_by: wayback
---

# コーナン 店舗検索

- URL: https://map.hc-kohnan.com/shop
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ストアロケーター、店舗検索、ホームセンター、コーナン、コーナンPRO、チラシ、木材カット、軽トラ貸出、営業時間、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ホームセンターコーナン・コーナンPRO などの店舗を現在地・エリア・サービス条件から検索し、地図上に表示する公式店舗検索サイト |
| 提供する価値 | 近くの店舗の位置や営業時間、木材カットや軽トラック貸出・資材館などのサービス対応を確認でき、目的に合った店舗へ来店できる |
| 想定する利用者 | コーナン・コーナンPRO の利用客、業者や一般の DIY 利用者で近くのホームセンターを探している人 |
| 商用か非商用か | 商用 (実店舗への来店送客およびチラシ・サービス案内の導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (コーナン商事株式会社) |
| 推定の運用費 | 推測: 月数万円〜十数万円。OpenStreetMap と Leaflet を採用することで地図描画のライセンス料を抑えつつ、CloudFront と店舗検索基盤の運用費がかかる |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (ブラウザ観測で OpenStreetMap + Leaflet を確認。一次 HTTP 取得でも `has_leaflet: true`) |
| フレームワーク | 未確認 (一次 HTTP 取得で `has_leaflet: true` を確認、後続の直接取得では接続切断) |
| 背景の地図とタイル | OpenStreetMap |
| 投稿やデータの保存先 | コーナン商事店舗検索データベース (API 詳細は未確認) |
| 配信 | Amazon CloudFront + Apache (`server: Apache`、`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-16 のブラウザ観測で OpenStreetMap と Leaflet の組み合わせによる地図表示を確認した
- 一次 HTTP 取得 (`https://map.hc-kohnan.com/shop`) でも `has_leaflet: true` が検出された (`has_gmaps` は `false`)
- 公式スマートフォンアプリとして「コーナンアプリ」（コーナン プラス会員証・コーナン Pay・クーポン・マイストアチラシ等）が提供されている

データの出どころ (2026-11-16):

- 店舗データ: コーナン商事株式会社
- 背景地図: OpenStreetMap contributors (Leaflet で描画)
