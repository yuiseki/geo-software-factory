---
financial: commercial
organization: corp-ent
first_seen: none
first_seen_by: none
---

# Garmin Explore

- URL: https://explore.garmin.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Garmin Explore、ガーミン、inReach、衛星通信、オフライン地形図、登山 GPS、TopoActive、Outdoor Maps+

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | Garmin のアウトドア GPS 端末や inReach 衛星通信機と連携し、オフライン地形図でのルート計画・軌跡管理・位置共有を行う地図サービス |
| 提供する価値 | 携帯電波の届かない山岳・海洋環境でも、事前ダウンロードした地形図や衛星写真上でルート作成やウェイポイント同期ができ、inReach 契約時は衛星経由の位置追跡・SOS が使える |
| 想定する利用者 | 登山家、バックカントリースキーヤー、遠征探検家、船舶・航空利用者、Garmin / inReach 端末の所有者 |
| 商用か非商用か | 商用 (Web ポータルおよびアプリの基本機能・TopoActive/USGS 等の標準地図ダウンロードは無料。高精細地図「Outdoor Maps+」は有料年額プラン、衛星通信機能は inReach 月額/年額プランが必要。本体ハードウェア販売と連動) |
| 推定の売上 | 推測: 単独売上は非公開 (親会社 Garmin Ltd. 全体の年間売上は約 60 億米ドル超規模の上場企業。Garmin Explore はアウトドア端末と inReach 課金を支えるエコシステム基盤) |
| 運営 | 企業 (Garmin Ltd.、米国カンザス州オレイサ拠点・スイス登記の上場企業) |
| 推定の運用費 | 推測: 月数千万円規模 (世界中のユーザー同期クラウド、オフライン地形タイル配信、Iridium 衛星網と連動する inReach 追跡・SOS 基盤を維持) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (2026-11-16 の観測で `tech_hits` に `leaflet` を検出。ネイティブアプリは独自のオフラインベクター/ラスタ地図エンジンを使用) |
| フレームワーク | ASP.NET + React + jQuery + RequireJS (応答ヘッダー `x-powered-by: ASP.NET`、`/bundles/react.js`、`/bundles/jquery.js`、`/bundles/requirejs.js` を確認) |
| 背景の地図とタイル | TopoActive (OpenStreetMap 由来)、USGS 地形図、衛星画像、Outdoor Maps+ 等 |
| 投稿やデータの保存先 | Garmin Explore クラウド (ウェイポイント・トラック・ルート・inReach メッセージを端末と同期) |
| 配信 | Cloudflare (`server: cloudflare`、`cf-ray` ヘッダーを確認) |

メモ:

- 2026-11-16 のアクセス時はログインページ (`/Account/LogOn`) へ遷移した。
- ウェブ版のほか iOS / Android アプリ「Garmin Explore」を無料提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| TopoActive 地形図 | OpenStreetMap 等をベースに Garmin が編集・最適化 | Garmin 公式サポート・製品ページ |
| 公的地形図・衛星画像 | USGS 等、各種衛星画像プロバイダー (Outdoor Maps+ 等) | Garmin 公式サポート・製品ページ |
