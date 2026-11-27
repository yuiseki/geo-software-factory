---
financial: non-commercial
organization: individual
first_seen: 2011-10-10
first_seen_by: wayback
---

# HOT Tasking Manager

- URL: https://tasks.hotosm.org
- ソース: https://github.com/hotosm/tasking-manager (BSD-2-Clause)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: HOT Tasking Manager、HOT、Humanitarian OpenStreetMap Team、災害マッピング、人道支援、クラウドソーシング、MapLibre、React

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 災害発生時や人道支援のために、対象地域を細かいグリッドに分割して世界中のボランティアが重複なく OpenStreetMap を編集できるようにする協調マッピング基盤 |
| 提供する価値 | 地震・洪水・感染症流行などの緊急時や途上国の地図整備において、数千人のリモートマッパーが同じ場所を重複編集せず効率的に建物や道路を地図化できる |
| 想定する利用者 | 人道支援団体 (赤十字、国境なき医師団等)、Missing Maps ボランティア、OpenStreetMap マッパー、防災・開発機関 |
| 商用か非商用か | 非商用 (非営利団体 Humanitarian OpenStreetMap Team が運営する無料プラットフォーム。助成金、寄付、クラウドクレジット支援等で運営) |
| 推定の売上 | 推測: 年数億〜十数億円規模の組織予算 (HOT 全体の非営利活動資金として助成金・寄付を受領。Tasking Manager 単体の予算は非公開) |
| 運営 | 非営利団体 (Humanitarian OpenStreetMap Team / HOT、米国登録の 501(c)(3) 非営利法人) |
| 推定の運用費 | 推測: 月数十万〜数百万円規模。Amazon CloudFront + S3 によるフロントエンド配信と FastAPI バックエンド・タスク管理 DB を運用している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS (v5.5 以降で MapLibre へ完全移行。応答 HTML では `/static/js/main.2fc3a7b8.js` のバンドルを確認) |
| フレームワーク | React フロントエンド + Python / FastAPI バックエンド (`hotosm/tasking-manager` リポジトリおよび静的 JS バンドルで確認) |
| 背景の地図とタイル | OpenStreetMap タイルおよび衛星画像 (Bing、Esri、Maxar 等の人道支援向け航空写真) |
| 投稿やデータの保存先 | タスク進捗・プロジェクト情報は自前 PostgreSQL/PostGIS DB、実際の地図地物は OpenStreetMap 本体 DB へ保存 |
| 配信 | Amazon S3 + Amazon CloudFront (`server: AmazonS3`、`via: ...cloudfront.net` を応答ヘッダーで確認) |

メモ:

- 公式の単体 iOS / Android アプリはなく、ウェブブラウザから利用する協調マッピング管理ツールとして提供されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 地図データ | OpenStreetMap contributors (ODbL) | 公式サイト・GitHub |
| 判読用衛星画像 | 提携衛星画像プロバイダ (Bing、Esri 等) の人道支援向け提供画像 | HOT 公式サイト |
