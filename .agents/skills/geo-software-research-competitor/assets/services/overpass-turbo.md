---
financial: non-commercial
organization: individual
first_seen: 2012-07-16
first_seen_by: github
---

# Overpass Turbo

- URL: https://overpass-turbo.eu
- ソース: https://github.com/tyrasd/overpass-turbo (MIT)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Overpass Turbo、Overpass API、OpenStreetMap、データ抽出、クエリ、GeoJSON、Leaflet、Martin Raifer

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ブラウザ上で Overpass API のクエリを実行し、OpenStreetMap の生データを地図上に可視化・抽出できるウェブデータマイニングツール |
| 提供する価値 | 専門的な GIS ソフトを使わずに、ウィザードやクエリで世界中の OSM 地物を絞り込み、GeoJSON や GPX、KML 等として即座にエクスポートできる |
| 想定する利用者 | OpenStreetMap マッパー、GIS アナリスト、研究者、データジャーナリスト、オープンデータを使う開発者 |
| 商用か非商用か | 非商用 (個人開発者 Martin Raifer 氏が MIT ライセンスで公開・運営する無料ウェブツール。バックエンドの公開 Overpass API もコミュニティによる無償提供) |
| 推定の売上 | なし (非商用オープンソースツール) |
| 運営 | 個人有志・コミュニティ (Martin Raifer / `tyrasd`) |
| 推定の運用費 | 推測: 月数万円以下 (静的フロントエンド中心の軽量構成。重いクエリ処理は外部の公開 Overpass API サーバー群に依存) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (応答 HTML 内に `leaflet` / `Leaflet` の記述および `./assets/index-D4ZnH7OT.js` バンドルを確認) |
| フレームワーク | Vite バンドルによる TypeScript/JavaScript SPA (`./assets/index-*.js` を確認) |
| 背景の地図とタイル | OpenStreetMap 標準タイル等の公開ラスタタイル |
| 投稿やデータの保存先 | クエリ結果は Overpass API へ都度問い合わせ、共有リンクやローカル保存にはブラウザストレージ等を利用 |
| 配信 | Apache/2.4.58 (Ubuntu) (`server: Apache/2.4.58 (Ubuntu)` を応答ヘッダーで確認) |

メモ:

- 公式の iOS / Android ネイティブアプリはなく、モバイルブラウザからも利用可能なレスポンシブウェブアプリとして提供されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 抽出対象の地物データ | OpenStreetMap contributors (ODbL) via Overpass API | 公式サイト・GitHub リポジトリ |
