---
financial: commercial
organization: corp-ent
---

# Bing Maps (Bing 地図)

- URL: https://www.bing.com/maps
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Bing Maps、Bing 地図、Microsoft、TomTom、Overture Maps、ルート検索、航空写真、ストリートサイド

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | Microsoft が検索エンジン Bing の一部として提供する、地図検索・ルート案内・航空写真・3D 都市表示を備えたウェブ地図サービス |
| 提供する価値 | 複数地点のマッピング、車・徒歩・乗換のルート検索、リアルタイム交通情報、高精細な航空写真・斜め写真 (Bird's Eye) をブラウザから無料で利用できる |
| 想定する利用者 | Bing や Windows・Copilot を使う一般の利用者、旅行や移動の計画を立てる人 |
| 商用か非商用か | 商用 (一般向けウェブ地図は無料。Bing 検索・Microsoft 広告や Copilot 等のエコシステムと連携) |
| 推定の売上 | 未公表 (Microsoft の Search and news advertising 部門等に含まれ、Bing Maps 単体の売上は公表されていない) |
| 運営 | 企業 (Microsoft Corporation) |
| 推定の運用費 | 未確認 (TomTom 等の地図データライセンス、航空写真・Streetside 撮影、Microsoft Azure 上の配信・検索基盤の運用費がかかる) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (HTML 内では `#appShellRoot` と Bing 独自のクライアントスクリプト構成を確認。法人向け API は Azure Maps への移行が進んでいる) |
| フレームワーク | 未確認 (HTML 内は Microsoft / Bing 独自のフロントエンド構成) |
| 背景の地図とタイル | TomTom (TomTom Orbis Maps / Orbis Addresses を含む)、OpenStreetMap / Overture Maps 関連データ、および Microsoft 自社の航空写真・衛星写真 |
| 投稿やデータの保存先 | Microsoft アカウント連携 (お気に入りやルート履歴等、詳細は未確認) |
| 配信 | Microsoft Azure / CDN (`x-cdn-traceid` ヘッダーを確認、`r.bing.com` 等の静的配信ドメイン) |

メモ:

- 2026-11-16 に `https://www.bing.com/maps` のヘッダーを確認したところ、`x-cdn-traceid` を返していた。
- ベースマップは主に TomTom が供給しており、Microsoft と TomTom は Overture Maps Foundation の中核メンバーとしてオープン地図標準の整備にも関わっている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 道路・住所・ベースマップ | TomTom (TomTom Orbis Maps 等)、一部地域は現地パートナーおよび OpenStreetMap 関連データ | Microsoft・TomTom 公式発表および地図画面の著作権表記 |
| 航空写真・衛星写真 | Microsoft および提携衛星・航空測量パートナー | Bing Maps 公式ドキュメント |
