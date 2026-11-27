---
financial: non-commercial
organization: individual
first_seen: 2004-08-28
first_seen_by: wayback
---

# OpenStreetMap

- URL: https://www.openstreetmap.org/
- ソース: https://github.com/openstreetmap/openstreetmap-website (GPL-3.0-or-later)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: OpenStreetMap、OSM、オープンデータ、クラウドソーシング地図、地図データベース、ODbL、ベースマップ、コミュニティ地図

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中の参加者が道路や建物や施設などの地理情報を自由に編集して共有する共同作成型の地図データベースおよびウェブ地図サービス |
| 提供する価値 | 誰でも無料で閲覧・編集・再利用 (ODbL ライセンス下で商用利用も可) できる世界の地図データと、多数の地図アプリやナビゲーションサービスの土台となるデータ基盤を提供する |
| 想定する利用者 | 地図を編集するマッパー、OSM データを自社の地図サービスやアプリに組み込む開発者・企業、災害支援や学術研究の利用者 |
| 商用か非商用か | 非商用 (OpenStreetMap Foundation が運営する非営利プロジェクト。データは ODbL で公開され無料で利用できる) |
| 推定の売上 | 約 47 万英ポンド (OSMF の 2024 年度の法定財務報告による総収益は £470,211。内訳は法人会員会費 £232,249、寄付 £74,279、助成金 £66,892 等。商用売上ではなく会費・寄付・助成金) |
| 運営 | 非営利団体 (OpenStreetMap Foundation。英国登記の保証有限会社) |
| 推定の運用費 | 年間数十万英ポンド規模の運営費に加えて、企業や大学からサーバー機材・コロケーション・CDN (Fastly 等) の現物寄付を受けて世界の編集 API とタイル配信を維持している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet および MapLibre GL JS (HTML 内で標準のラスタ地図とベクトルタイル表示の双方への参照を確認) |
| フレームワーク | Ruby on Rails + Hotwire Turbo (応答ヘッダーの `x-powered-by: Phusion Passenger(R) 6.2.2` および HTML 内の `turbo-*.js` を確認) |
| 背景の地図とタイル | OpenStreetMap 自身のラスタタイル (`tile.openstreetmap.org`)、ベクトルタイル (`vector.openstreetmap.org`)、Thunderforest、Tracestrack、OpenStreetMap France 等 (CSP ヘッダーで確認) |
| 投稿やデータの保存先 | 自前の PostgreSQL + PostGIS データベース (編集 API の中核。ユーザーアバターや GPS 画像の保存には AWS S3 `s3.dualstack.eu-west-1.amazonaws.com` を使用していることを CSP ヘッダーで確認) |
| 配信 | Apache + Phusion Passenger + Varnish (`server: Apache`、`via: 1.1 varnish` を応答ヘッダーで確認。CDN やホストの事業者は一部寄付に依存) |

メモ:

- 世界中の地図サービスのベースマップおよび主題データの基盤として広く利用されている。
- ウェブエディタ (iD) や外部エディタ (JOSM 等) との連携機能を備える。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 地図データ | OpenStreetMap contributors (ODbL) | https://www.openstreetmap.org/copyright |
| ドキュメント・ウェブサイト基盤 | OpenStreetMap Foundation (CC BY-SA 2.0 等) | https://www.openstreetmap.org/copyright |
