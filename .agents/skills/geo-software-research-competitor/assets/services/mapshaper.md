---
financial: non-commercial
organization: individual
---

# Mapshaper

- URL: https://mapshaper.org
- ソース: https://github.com/mbloch/mapshaper (MPL-2.0 License)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Mapshaper、Shapefile、TopoJSON、GeoJSON、FlatGeobuf、GeoParquet、ポリゴン簡素化、トポロジー、形式変換、CLI

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ポリゴンの境界トポロジーを保ったまま地理空間データの簡素化・編集・形式変換を高速に行えるブラウザおよび CLI ツール |
| 提供する価値 | 隣接する行政界などに隙間や重なりを生じさせずに軽量化 (Visvalingam / Douglas-Peucker) でき、Shapefile・GeoJSON・TopoJSON・GeoPackage・FlatGeobuf・GeoParquet・KML・CSV 等をサーバーに送信せず手元で安全に高速処理できる |
| 想定する利用者 | データジャーナリスト、地図製作者、GIS エンジニア、重い統計境界データを Web 向けに軽量化・変換したい開発者 |
| 商用か非商用か | 非商用・無料 OSS (MPL-2.0 ライセンス。Web 版・Node.js CLI 版ともに完全無料) |
| 推定の売上 | 直接の売上なし (個人による OSS 開発・無償公開) |
| 運営 | 個人 (Matthew Bloch、元 The New York Times グラフィックスエディタ) |
| 推定の運用費 | 推測: 月数千円〜数万円程度 (処理はすべてユーザーのブラウザ内またはローカル CLI で完結するため、サーバー計算コストはほぼなく GitHub Pages による静的配信のみ) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 独自の HTML5 Canvas レンダリング + 背景地図表示用の Mapbox (`basemap.js` および `tech_hits` で `Mapbox` を確認) |
| フレームワーク | 独自の JavaScript バンドル (`mapshaper.js`, `mapshaper-gui.js`, `basemap.js` を確認) |
| 背景の地図とタイル | 既定では背景タイルなしの白紙上にベクター描画。オプションで Mapbox のベースマップを重ねることが可能 |
| 投稿やデータの保存先 | 保存先サーバーなし (アップロードしたファイルはサーバーに送られずブラウザメモリ内で処理され、ローカルへ書き出す) |
| 配信 | GitHub Pages + Varnish (`server: GitHub.com`、`via: 1.1 varnish` を応答ヘッダーで確認) |

メモ:

- iOS / Android の専用アプリは提供されていない (Web ブラウザおよび Node.js CLI ツール)。
- ブラウザ上の対話コンソールから CLI と同じ強力な空間演算・属性編集コマンドを実行できる。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 編集・変換データ | ユーザーの持ち込みファイル | 公式サイト・README |
| オプション背景地図 | Mapbox / OpenStreetMap | `basemap.js` および画面 UI |
