# Global Forest Watch

- URL: https://www.globalforestwatch.org/map/ (2026-11-16 時点では https://globalnaturewatch.org/map/ へ 301 リダイレクト)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Global Forest Watch、GFW、Global Nature Watch、WRI、森林減少、森林監視、衛星データ、Mapbox、CARTO

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 衛星データを用いて世界中の森林被覆の変化や森林火災・開発の兆候をほぼリアルタイムに監視・分析できるオープンデータプラットフォーム |
| 提供する価値 | 最新の衛星画像解析による森林減少アラートや国・地域別の統計をブラウザ上で即座に集計・可視化し、森林保全の意思決定や監視に役立てられる |
| 想定する利用者 | 政府機関、環境 NGO、研究者、企業のサプライチェーン調達担当者、ジャーナリスト |
| 商用か非商用か | 非商用 (公益プラットフォームとして基本無料で公開。政府・慈善財団・パートナー企業の資金援助で運営) |
| 推定の売上 | なし (非営利プロジェクト。ノルウェー政府 NICFI、Bezos Earth Fund、英米政府等の助成金により運営) |
| 運営 | 国際 NGO (World Resources Institute: 世界資源研究所、米国) |
| 推定の運用費 | 推測: 年数億円規模と見られる (全球衛星データの解析パイプライン、クラウド計算基盤、研究・開発体制の維持費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Mapbox GL JS (`/_next/static/chunks/` 内に `mapbox-gl` および `carto` の記述を確認) |
| フレームワーク | Next.js (`x-powered-by: Next.js` ヘッダーおよび `/_next/static/chunks/` を確認) |
| 背景の地図とタイル | Mapbox ベースマップおよび衛星解析データ・CARTO 等を利用したテーマ別タイル |
| 投稿やデータの保存先 | 未確認 (保存エリアやアラート購読機能を持つが保存先インフラの詳細は非公開) |
| 配信 | Cloudflare + Heroku (`www.globalforestwatch.org` が Cloudflare 経由でリダイレクトし、リダイレクト先が `server: Heroku` / `via: 2.0 heroku-router` であることを確認) |

メモ:

- 2026-11-16 時点で `https://www.globalforestwatch.org/map/` へのアクセスは `https://globalnaturewatch.org/map/` へ 301 リダイレクトされ、タイトルも Global Nature Watch (`GNW`) に拡張されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 樹木被覆変化データ | メリーランド大学 (Hansen ら)、Google Earth Engine | 公式サイトおよびパートナー紹介 |
| 衛星画像・火災アラート等 | NASA / USGS (Landsat、MODIS、VIIRS)、Planet、WRI | 公式サイトおよびデータセット説明 |
