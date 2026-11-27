---
financial: commercial
organization: corp-ent
first_seen: 2020-06-29
first_seen_by: wayback
---

# サイゼリヤ 店舗検索

- URL: https://shop.saizeriya.co.jp/sz_restaurant/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ストアロケーター、店舗検索、ファミレス、サイゼリヤ、営業時間、駐車場、テイクアウト、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のサイゼリヤ店舗を、エリア・最寄駅・現在地や条件から検索して地図上に表示する公式店舗検索サイト |
| 提供する価値 | 近くのサイゼリヤ店舗の位置、営業時間、最寄駅や設備情報などを素早く確認し、来店前の店舗選びができる |
| 想定する利用者 | サイゼリヤの店舗を探している一般客、外出先で最寄り店舗を探している利用者 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社サイゼリヤ) |
| 推定の運用費 | 推測: 月数万〜数十万円。NAVITIME Location Cloud の法人向け店舗検索サービス利用料およびサーバー運用費がかかる |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME Location Cloud。ブラウザ観測で地図上に「© NAVITIME JAPAN」「地図 ©ゼンリン」、フッターに「Powered by NAVITIME Location Cloud」を確認 |
| フレームワーク | 未確認 (トップページの一次 HTTP 取得のみ実施) |
| 背景の地図とタイル | ゼンリン地図データ (NAVITIME Location Cloud 経由で配信、「地図 ©ゼンリン」) |
| 投稿やデータの保存先 | NAVITIME Location Cloud / サイゼリヤ店舗データ (API 詳細は未確認) |
| 配信 | Apache (`server: Apache`) |

メモ:

- 2026-11-16 のブラウザ観測で「© NAVITIME JAPAN」「地図 ©ゼンリン」「Powered by NAVITIME Location Cloud」を確認した
- 一次 HTTP 取得 (`https://shop.saizeriya.co.jp/sz_restaurant/`) でも `has_navitime: true` が観測された
- 会員ポイントやクーポンを扱う一般的な「公式店舗アプリ」は提供されていない

データの出どころ (2026-11-16):

- 店舗データ: 株式会社サイゼリヤ / NAVITIME Location Cloud
- 背景地図: 株式会社ゼンリン / 株式会社ナビタイムジャパン (NAVITIME Location Cloud)
