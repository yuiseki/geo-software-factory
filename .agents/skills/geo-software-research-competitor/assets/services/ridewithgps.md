---
financial: commercial
organization: corp-smb
---

# Ride with GPS

- URL: https://ridewithgps.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Ride with GPS、RWGPS、サイクリング、ルート作成、ブルベ、キューシート、Garmin、Wahoo、Google Maps

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | サイクリストや自転車クラブ、イベント主催者向けに詳細なルート作成、キューシート出力、GPS サイコン連携を提供するサイクリング地図プラットフォーム |
| 提供する価値 | 舗装・未舗装や勾配を確認しながら正確なサイクリングルートを作成し、Garmin や Wahoo への同期、PDF キューシート印刷、音声ナビまで一貫して行える |
| 想定する利用者 | ロードサイクリスト、ブルベ参加者、自転車ツーリング愛好家、サイクリングクラブ、自転車イベント主催者 |
| 商用か非商用か | 商用 (Starter は無料。有料プランは年払いで月額 6.67 米ドル相当・年約 80 米ドル、クラブ・団体向けの Organizations プランあり) |
| 推定の売上 | 未確認 (非公開企業で従業員数は 30 から 35 名規模。2023 年 9 月に 300 万米ドルのシード資金調達。アプリストア課金だけで月数万から 10 万米ドル超と推定される) |
| 運営 | 企業 (Ride with GPS、2007 年創業、米国オレゴン州ポートランド拠点) |
| 推定の運用費 | 未確認 (OSM ルーティングおよびタイル生成基盤、Google Maps Platform API 利用料、S3 互換ストレージと配信費、開発運用人件費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | ウェブ、iOS と Android のアプリ |
| 描画 | Mapbox および Google Maps (`/routes/new` の HTML 内で `mapbox`、トップページ HTML 内で `google.maps` の参照を確認) |
| フレームワーク | Next.js (`_next/`、`/routes/new` で `next` を確認)、React |
| 背景の地図とタイル | OpenStreetMap ベースの自社「RWGPS Cycle」地図、および切り替え可能な Google Maps (標準・地形・衛星・ストリートビュー) |
| 投稿やデータの保存先 | Amazon S3 または S3 互換ストレージ (`x-amz-storage-class: STANDARD`、`x-amz-request-id` を応答ヘッダーで確認) |
| 配信 | openresty/1.15.8.2 (`server: openresty/1.15.8.2` を応答ヘッダーで確認) |

メモ:

- 自転車のロングライドやブルベ (ランドヌール) で定番のキューシート生成機能とサイコン連携に強みを持つ。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| RWGPS Cycle 地図・サイクリング道データ | OpenStreetMap contributors | Ride with GPS 公式サイト |
| 衛星・地形・ストリートビュー切替 | Google Maps Platform | Ride with GPS 公式サイト |
