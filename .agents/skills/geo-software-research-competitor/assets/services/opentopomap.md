---
financial: non-commercial
organization: individual
---

# OpenTopoMap

- URL: https://opentopomap.org
- ソース: https://github.com/der-stefan/OpenTopoMap (CC-BY-SA / Garmin 版は CC-BY-NC-SA)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: OpenTopoMap、地形図、等高線、陰影起伏、SRTM、OpenStreetMap、登山地図、Garmin、Leaflet

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | OpenStreetMap と標高データを組み合わせて、ドイツ等の公式地形図に似た等高線・陰影起伏付きのウェブ地形図と Garmin 用地図を生成・公開するオープンソースプロジェクト |
| 提供する価値 | 等高線や地形の陰影、登山道、山小屋などを視認性高く描いた世界の地形図タイルを無料で閲覧・利用できる |
| 想定する利用者 | 登山者、ハイカー、アウトドア愛好家、地図作成者、非商用・小規模な地図アプリのタイル利用者 |
| 商用か非商用か | 非商用 (ボランティアによるコミュニティ運営の無料サービス。Garmin 用地図は CC-BY-NC-SA で商用禁止、公開タイルサーバーも公平利用の制限あり) |
| 推定の売上 | なし (非商用プロジェクト) |
| 運営 | コミュニティ・個人有志 (`derstefan` / Stefan Erhardt らドイツの開発者有志) |
| 推定の運用費 | 推測: 月数万円〜十数万円規模。コミュニティサーバーやミラー (`openmaps.fr` 等) で重いラスタタイルの生成・配信を維持している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet + D3.js (応答 HTML 内に `leaflet/leaflet.js` および `d3.min.js` の読み込みを確認) |
| フレームワーク | 静的 HTML / バニラ JavaScript (`L.Grid.js`、`L.Control.Locate.js`、`leaflet-search.js` 等のプラグイン構成) |
| 背景の地図とタイル | 自前の OpenTopoMap ラスタタイル (Mapnik スタイルシートで生成) |
| 投稿やデータの保存先 | 自前 DB なし (OpenStreetMap 本体のデータを参照してタイルを生成) |
| 配信 | Apache/2.4.58 (Ubuntu) (`server: Apache/2.4.58 (Ubuntu)` を応答ヘッダーで確認) |

メモ:

- 公式の単体 iOS / Android アプリはないが、公開タイル URL を経由して各種サードパーティの登山・地図アプリに背景地図として組み込まれている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 道路・登山道・地物 | OpenStreetMap contributors (ODbL) | GitHub リポジトリ・公式サイト |
| 標高・等高線・陰影 | NASA SRTM (Shuttle Radar Topography Mission) 等の標高データ | GitHub リポジトリ・OSM Wiki |
