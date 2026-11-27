---
financial: commercial
organization: individual
first_seen: 2020-08-16
first_seen_by: wayback
---

# City Guesser

- URL: https://virtualvacation.us/guess
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: City Guesser、Virtual Vacation、Paul McBurney、動画ベース、街当てゲーム、Leaflet、OpenStreetMap、Ko-fi

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界各地の街歩き動画（音声付き）を見て、どこの都市・場所かを地図上で当てる動画ベースの地理ゲーム |
| 提供する価値 | 静止画のストリートビューではなく実際の街の雑踏や動き・音を含む動画から手がかりを探し、バーチャル旅行感覚で都市を当てられる |
| 想定する利用者 | GeoGuessr 系のゲーム好き、世界の街歩き動画を楽しみたいユーザー、オンラインでのマルチプレイ参加者 |
| 商用か非商用か | 商用（基本無料・Web 広告および Ko-fi 等を通じた寄付で運営） |
| 推定の売上 | 推測: 年数百万〜数千万円規模（Virtual Vacation 全体の広告ネットワーク AdinPlay / AdSense と寄付収入によるが非公開） |
| 運営 | 個人発プロジェクト（Paul McBurney Jr. / Virtual Vacation） |
| 推定の運用費 | 推測: 月数万円程度（サイト自体は GitHub Pages 上の静的配信、動画は YouTube 埋め込み、地図は OSM ベースで API 課金を抑えている） |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet（応答 HTML 内で `leaflet@1.6.0/dist/leaflet.js` の読み込みを確認） |
| フレームワーク | Vue.js + jQuery + Bootstrap（応答 HTML 内で Vue 構文および jQuery 3.5.1 / Bootstrap 4.5.0 の読み込みを確認） |
| 背景の地図とタイル | OpenStreetMap 系タイルおよび YouTube 動画埋め込み（HTML 内の OSM 参照と YouTube 連携を確認） |
| 投稿やデータの保存先 | 静的サイト構成（動画・都市リストのキュレーションデータ） |
| 配信 | GitHub Pages + Varnish（応答ヘッダーで `server: GitHub.com`、`via: 1.1 varnish` を確認。AdinPlay と AdSense を掲載） |

メモ:

- Google Street View API を使わずに YouTube の街歩き動画と Leaflet + OSM を組み合わせることで、高額な Street View API 課金を回避した設計が特徴。
- 同じ Virtual Vacation プラットフォーム上で、地球上のドットから動画を探す「VidEarth」なども展開している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 街歩き動画 | YouTube 上の各地のウォーキング動画（埋め込み再生） | https://virtualvacation.us/guess |
| 推測用ベースマップ | OpenStreetMap | サイト内 Leaflet 表示 |
