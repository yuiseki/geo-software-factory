# Strava Global Heatmap

- URL: https://www.strava.com/maps/global-heatmap
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Strava、Global Heatmap、ヒートマップ、ランニング、サイクリング、GPS、OpenStreetMap、ルート探索

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中の Strava ユーザーが公開した過去 1 年分のアクティビティ GPS 軌跡を集計し、人気のルートやトレイルを可視化するグローバルヒートマップ |
| 提供する価値 | ランナーやサイクリスト、ハイカーが実際に多く通っている道やトレイルを直感的に把握でき、OpenStreetMap の未整備な登山道や小道のマッピング資料としても活用できる |
| 想定する利用者 | ランナー、サイクリスト、トレイルランナー、ハイカー、OpenStreetMap マッパー |
| 商用か非商用か | 商用 (グローバルヒートマップの基本閲覧は無料、詳細な個人ヒートマップやルート作成機能は Strava 有料サブスクリプション、米国で年額 79.99 米ドル前後) |
| 推定の売上 | 推測: Strava 全体の年間経常収益 (ARR) は約 4.15 億から 4.9 億米ドル規模 (評価額 22 億米ドル、登録ユーザー 2 億人超と報じられる。Global Heatmap 単体の売上は非区分のため未確認) |
| 運営 | 企業 (Strava, Inc.、米国サンフランシスコ拠点) |
| 推定の運用費 | 未確認 (数十億点規模の GPS テレメトリ集計基盤、月次ヒートマップタイル生成、Mapbox 利用料、CloudFront 配信費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | ウェブ (Strava プラットフォーム内)、iOS と Android のアプリ |
| 描画 | Mapbox GL (`_next/static/chunks/pages/maps/` 内の JavaScript バンドルで `mapbox` の参照を確認) |
| フレームワーク | Next.js (`__NEXT_DATA__`、`_next/`)、React、Sentry |
| 背景の地図とタイル | Mapbox ベースの地図 (OpenStreetMap データ由来) に、Strava 独自の集計ヒートマップラスター・ベクトルレイヤーを重畳 |
| 投稿やデータの保存先 | 未確認 (Strava のクラウド基盤に蓄積された公開アクティビティデータから匿名化集計) |
| 配信 | istio-envoy + Amazon CloudFront (`server: istio-envoy`、`via: CloudFront` を応答ヘッダーで確認) |

メモ:

- 過去 1 年間の公開アクティビティから生成され、毎月更新される。
- OpenStreetMap コミュニティ向けに JOSM や iD エディタ上でのトレイル確認用背景レイヤーとしても公式に利用許諾されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| ヒートマップデータ | Strava ユーザーの匿名化・集計済み公開 GPS アクティビティ | Strava Global Heatmap ページ |
| ベースマップ | Mapbox / OpenStreetMap contributors | Strava マップ画面および OSM Wiki |
