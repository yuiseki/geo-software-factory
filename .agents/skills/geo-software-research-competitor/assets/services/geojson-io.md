---
financial: non-commercial
organization: individual
first_seen: 2013-05-10
first_seen_by: github
---

# geojson.io

- URL: https://geojson.io
- ソース: https://github.com/mapbox/geojson.io (ISC License)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: geojson.io、GeoJSON、TopoJSON、Mapbox、地図データ編集、WKT、KML、GIS ツール、ブラウザエディタ

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ブラウザ上で GeoJSON などの地理空間データを即座に作成・編集・変換・プレビューできるオープンソースのウェブエディタ |
| 提供する価値 | 地図上の描画と JSON テキストエディタが双方向に即時同期し、GeoJSON / TopoJSON / KML / CSV / Shapefile 等の変換や GitHub Gist での共有をログイン不要ですぐに行える |
| 想定する利用者 | GIS 開発者、Web 地図エンジニア、データアナリスト、ちょっと境界データやテスト用 GeoJSON を作って確認したい人 |
| 商用か非商用か | 非商用・無料 OSS (Web 版は無料で利用可能。ソースコードは ISC License で公開されているが、描画エンジンに Mapbox GL JS v2+ を使用しているため自前ホスト時は Mapbox の規約とトークンが適用される) |
| 推定の売上 | 直接の売上なし (Mapbox が公開・維持する開発者向け無償ツール) |
| 運営 | 企業・OSS コミュニティ (Mapbox 発のオープンソースプロジェクト) |
| 推定の運用費 | 推測: 月数万円〜十数万円程度 (静的サイトは GitHub Pages で配信し、実費は Mapbox のベースマップタイル利用分のみ) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Mapbox GL JS + Mapbox GL Draw (応答内の `mapbox` 記述およびリポジトリ構成で確認) |
| フレームワーク | React + Vite によるバンドル (`/assets/index-CxePgzEO.js` を確認) |
| 背景の地図とタイル | Mapbox ベースマップ (Streets, Satellite 等) および OpenStreetMap 等の切り替えに対応 |
| 投稿やデータの保存先 | サーバー側データベースなし (ブラウザのメモリ/ローカル保存、URL ハッシュ、またはユーザーの GitHub / Gist アカウントへ直接保存) |
| 配信 | GitHub Pages + Varnish (`server: GitHub.com`、`via: 1.1 varnish` を応答ヘッダーで確認) |

メモ:

- iOS / Android の専用アプリは提供されていない (Web ブラウザ専用)。
- 元々 Leaflet / Mapbox.js ベースで開発されたが、のちに Mapbox GL JS ベースへ刷新された。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 背景地図・衛星画像 | Mapbox / OpenStreetMap | 画面上のスタイル切替および帰属表示 |
| 編集対象データ | ユーザーの入力・持ち込みファイル | サービス仕様 |
