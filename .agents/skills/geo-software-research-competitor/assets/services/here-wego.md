---
financial: commercial
organization: corp-ent
first_seen: 2016-08-04
first_seen_by: wayback
---

# HERE WeGo

- URL: https://wego.here.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: HERE WeGo、HERE Maps、HERE Technologies、ナビ、オフライン地図、自動車、経路検索、欧州

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 欧州の自動車メーカー連合が主要株主の HERE Technologies が提供する、広告なし・無料で使える地図・マルチモーダル経路案内サービス |
| 提供する価値 | 車・公共交通・徒歩・自転車の経路案内、リアルタイム交通情報、モバイル版でのオフライン地図ダウンロードを広告なし・プライバシー重視で利用できる |
| 想定する利用者 | 日常の移動や海外旅行でオフライン地図や経路案内を使いたい一般の人、プライバシーを重視する利用者 |
| 商用か非商用か | 商用 (一般向けアプリ・ウェブ版は無料で広告なし。親会社 HERE Technologies は自動車業界向け地図や法人向け位置情報 API で収益を得ている) |
| 推定の売上 | 未公表 (非公開企業のため HERE Technologies 単体の最新売上は非公表。一般向け HERE WeGo 自体は直接課金を行っていない) |
| 運営 | 企業 (HERE Technologies、Audi・BMW・Mercedes-Benz 等のコンソーシアムが There Holding B.V. 等を通じて出資) |
| 推定の運用費 | 未確認 (世界中の LiDAR・カメラ搭載測量車両の運用、接続車両からのテレメトリ処理、CloudFront / S3 等での配信基盤の維持費がかかる) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | HERE Maps API for JavaScript ベースのベクター描画 (HTML では `type="module"` のバンドル `/static/js/index-Q0lzcw2c.js` を確認) |
| フレームワーク | モダン JavaScript / TypeScript 構成 (公式開発者向けリファレンス等では React 等の利用例が紹介されているが、本番バンドル内部の特定は未確認) |
| 背景の地図とタイル | HERE 自社測量の世界地図データ、コネクテッドカー由来の交通情報、各都市の GTFS 公共交通データ、一部 OpenStreetMap データ |
| 投稿やデータの保存先 | HERE アカウント (お気に入りやコレクションの同期。ログインなしでの基本利用も可能) |
| 配信 | Amazon S3 + Amazon CloudFront (`server: AmazonS3`、`via: ...cloudfront.net` ヘッダーを確認) |

メモ:

- 2026-11-16 に `https://wego.here.com/` の応答ヘッダーを確認したところ、`server: AmazonS3` と `via: ...cloudfront.net (CloudFront)` を確認した。
- 法人・開発者向けには HERE Location Services として無料枠付きの従量課金 API / SDK を提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 道路網・建物・制限速度・POI | HERE Technologies 自社測量車両 (LiDAR・カメラ) および提携自動車メーカーのコネクテッド車両データ | HERE Technologies 公式技術解説 |
| 公共交通・歩行者補完データ | 各地の公共交通機関 (GTFS) および OpenStreetMap 等の外部データ | HERE 公式ドキュメント・アプリ説明 |
