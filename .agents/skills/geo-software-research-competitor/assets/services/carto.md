---
financial: commercial
organization: corp-smb
first_seen: 1996-10-31
first_seen_by: wayback
---

# CARTO

- URL: https://carto.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: CARTO、CartoDB、Location Intelligence、空間解析、BigQuery、Snowflake、deck.gl、MapLibre、WebGIS

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | BigQuery や Snowflake などのクラウドデータウェアハウスに直接接続して、大規模空間解析と地図可視化を行うエンタープライズ向け Location Intelligence プラットフォーム |
| 提供する価値 | データを外部 GIS サーバーへコピーせずに、SQL ベースの空間関数 (Analytics Toolbox)、ノーコードのワークフロー (Workflows)、AI エージェント、高速描画を組み合わせて分析とアプリ構築ができる |
| 想定する利用者 | 小売・物流・通信・金融・不動産などの大企業および中堅企業のデータチーム、空間データサイエンティスト |
| 商用か非商用か | 商用 (常設の無料プランはなく、14〜30 日間の試用期間後、従量課金 Pay As You Go または年間契約の Enterprise / Self-Hosted プランを提供) |
| 推定の売上 | 推測: 年間 2,800 万ドルから 5,700 万ドル規模 (SaaS 調査機関 GetLatka / Growjo による推定値。非上場のため公式非公開、累計調達額は約 9,200 万〜9,700 万ドル) |
| 運営 | 企業 (CARTO / CartoDB Inc.、米国およびスペイン拠点、従業員約 250〜310 名規模) |
| 推定の運用費 | 未確認 (マルチクラウド SaaS 基盤、空間タイル生成、AI 機能、グローバルサポート体制の維持費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | deck.gl (`@deck.gl/carto` による WebGL/WebGPU 描画) + MapLibre GL JS |
| フレームワーク | React / Next.js 等 (トップページ HTML 内に `next`、`deck.gl`、`d3` の文字列を確認) |
| 背景の地図とタイル | CARTO ベースマップ (Voyager、Positron、Dark Matter 等、OSM ベース) およびクラウドデータウェアハウスから直接生成される動的ベクトルタイル |
| 投稿やデータの保存先 | 顧客のクラウドデータウェアハウス (Google BigQuery、Snowflake、Amazon Redshift、Databricks) または CARTO クラウド |
| 配信 | Google Cloud (`server: UploadServer` を確認) |

メモ:

- 2011 年に CartoDB として始まり、2016 年に CARTO へ改称したのち、自社 DB 中心の旧構成からクラウドデータウェアハウス直結のクラウドネイティブ構成へ転換した。
- オープンソースの `deck.gl` エコシステムや MapLibre と深く連携し、クライアント SDK も公開している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 料金体系・機能・クラウド連携 | CARTO 公式サイトおよび技術ドキュメント | carto.com 公開ページ |
| 売上推定・従業員数・調達額 | GetLatka、Growjo、PitchBook、CARTO 公式発表 | 公開調査データおよびプレスリリース |
