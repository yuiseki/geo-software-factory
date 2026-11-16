# VidEarth

- URL: https://virtualvacation.us/videarth
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: VidEarth、Virtual Vacation、Paul McBurney、衛星マップ、現地動画、Leaflet、ArcGIS、Radio Garden風

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 衛星地図上に並んだ無数のドットをクリックして、世界中のその場所で撮影された街歩き・風景動画を視聴できる Web アプリ |
| 提供する価値 | Radio Garden のような「地図上の点を選んで現地の空気感に触れる」体験を、ラジオ音声ではなく現地の動画（街歩き・ドライブ・ライブ映像）で提供する |
| 想定する利用者 | バーチャル旅行を楽しみたいユーザー、世界各地の街並みを動画で探検したい人、City Guesser の利用者 |
| 商用か非商用か | 商用・個人プロジェクト（Virtual Vacation の一部として無料公開。プラットフォーム全体の広告・Ko-fi 寄付で維持） |
| 推定の売上 | 推測: City Guesser を含む Virtual Vacation 全体で年数百万〜数千万円規模（単体での売上は非公開） |
| 運営 | 個人発プロジェクト（Paul McBurney Jr. / Virtual Vacation） |
| 推定の運用費 | 推測: 月数万円程度（GitHub Pages での静的ホスティング、ArcGIS/OSM ベースマップ、YouTube 埋め込みにより低コストで運用） |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet（HTML 内で `leaflet@1.7.1/dist/leaflet.js` の読み込みを確認） |
| フレームワーク | Vue.js + jQuery + Bootstrap 4（HTML 内で Vue 構文および jQuery 3.5.1 / Bootstrap 4.0.0 の読み込みを確認） |
| 背景の地図とタイル | ArcGIS 衛星画像タイルおよび OpenStreetMap（HTML 内に `arcgis` と `osm` への参照を確認） |
| 投稿やデータの保存先 | 静的サイト構成（各地点の座標と YouTube 動画 ID のキュレーションリスト） |
| 配信 | GitHub Pages + Varnish（応答ヘッダーで `server: GitHub.com`、`via: 1.1 varnish` を確認。Google Analytics `UA-153516768-4` を掲載） |

メモ:

- 同じ作者（Paul McBurney Jr.）による City Guesser と共通の Virtual Vacation 基盤上に構築されており、動画データの資産を「ゲーム（City Guesser）」と「探索マップ（VidEarth）」の 2 通りの体験に転用している好例。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 衛星地図・ベースマップ | ArcGIS Online / OpenStreetMap | サイト内 Leaflet レイヤー設定 |
| 各地の現地動画 | YouTube 上の街歩き・風景動画（埋め込み） | https://virtualvacation.us/videarth |
