# Starbucks（Global Store Locator）

- URL: https://www.starbucks.com/store-locator
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Starbucks、スターバックス、スタバ、Store Locator、店舗検索、Google Maps、モバイルオーダー、ドライブスルー、Esri

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中のスターバックス店舗を地図上で検索し、営業時間、ドライブスルーやモバイルオーダー対応状況、現在地からの経路を確認できる公式店舗検索サービス |
| 提供する価値 | 近くの店舗をすぐに見つけ、設備条件（24時間営業、ドライブスルー、Wi-Fi、モバイルオーダー対応など）で絞り込み、そのまま事前注文や来店につなげられる |
| 想定する利用者 | 最寄りのスターバックス店舗を探したい、またはモバイルオーダーで事前注文して受け取りたい一般消費者 |
| 商用か非商用か | 商用 (店舗検索機能は無料。実店舗およびモバイルオーダーでの飲食・物販売上への送客導線として運用) |
| 推定の売上 | Starbucks Corporation 全体の 2024 年会計年度 (FY24) 連結純売上は 約 361.4 億〜361.8 億ドル |
| 運営 | 企業 (Starbucks Corporation、米国) |
| 推定の運用費 | 推測: 店舗検索機能単体は Google Maps Platform 等の API 利用料を含め月数百万円規模 (グローバルな店舗データおよびモバイルオーダー基盤の一部として運用) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (`https://www.starbucks.com/store-locator` の HTTP 200 応答にて `has_gmaps: true` を確認) |
| フレームワーク | 未確認 (`x-powered-by: core01` ヘッダーを確認。公開の技術情報等では React を用いた Web フロントエンド構成が知られる) |
| 背景の地図とタイル | Google Maps (応答 HTML での Google Maps 読み込みを確認。なお社内の新規出店・立地分析 GIS 基盤としては Esri / Atlas 等も併用している) |
| 投稿やデータの保存先 | Starbucks 自社基盤 (世界中の店舗座標、営業時間、設備フラグ、モバイルオーダー対応状況) |
| 配信 | `x-powered-by: core01` (`https://www.starbucks.com/store-locator` の応答ヘッダーを確認) |

メモ:

- 2026-11-16 の一次観測でも `https://www.starbucks.com/store-locator` にて Google Maps の利用 (`has_gmaps: true`) を確認した。
- ウェブ版のほか、iOS / Android 向けの公式「Starbucks」アプリを提供しており、アプリ内の店舗検索と Mobile Order & Pay が米国取引の約 31%（2024年時点）を支える重要な導線となっている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 店舗位置・営業時間・設備情報 | Starbucks 各国法人・店舗管理システム | Starbucks 公式サイトおよび公式アプリ |
| 地図・ジオコーディング・経路 | Google Maps | 応答 HTML の Google Maps 読み込みおよび公開技術情報 |
