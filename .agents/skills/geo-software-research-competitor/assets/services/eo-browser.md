---
financial: commercial
organization: corp-smb
first_seen: 2017-03-22
first_seen_by: wayback
---

# EO Browser (Sentinel Hub / Copernicus Browser)

- URL: https://apps.sentinel-hub.com/eo-browser/ (Copernicus 公式版: https://browser.dataspace.copernicus.eu/)
- ソース: https://github.com/sentinel-hub/EOBrowser (2026-11-16 確認)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: EO Browser、Copernicus Browser、Sentinel Hub、衛星画像、地球観測、Sentinel-2、Landsat、NDVI、リモートセンシング、Evalscript

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | Sentinel や Landsat などの衛星画像をブラウザ上で検索し、バンド演算や時系列比較・書き出しができる地球観測データ閲覧サービス |
| 提供する価値 | 巨大な衛星データ (SAFE ファイル等) を手元にダウンロードせずに、クラウド上のオンザフライ処理で NDVI 等の解析画像やタイムラプスを即座に可視化・比較できる |
| 想定する利用者 | 地球観測・リモートセンシングの研究者、教育関係者、環境モニタリングや農業・防災分野の分析者 |
| 商用か非商用か | 商用基盤上の無償提供 (EO Browser および Copernicus Browser での閲覧・非商用研究は無料。API の商用利用や高解像度商用衛星データの利用は Sentinel Hub の従量課金・サブスクリプション) |
| 推定の売上 | 未確認 (開発元の Sinergise は 2023 年に Planet Labs に買収されており、単体売上は非公開。Sentinel Hub API の PU 課金や商用データ連携が収益源) |
| 運営 | 企業 (Sinergise / Planet Labs が開発し、Copernicus Browser は欧州連合の Copernicus Data Space Ecosystem 向けに提供) |
| 推定の運用費 | 未確認 (ペタバイト級の衛星アーカイブ処理とオンザフライ画像生成を行うクラウド基盤および CloudFront 配信の運用費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (`leaflet`, `react-leaflet`)、MapLibre GL JS (`maplibre-gl`) も依存パッケージに含まれる |
| フレームワーク | React + Redux Toolkit + Vite (`@vitejs/plugin-react-swc`) |
| 背景の地図とタイル | Sentinel Hub Processing API / WMS / WMTS による衛星画像タイル (Sentinel-1/2/3/5P、Landsat、DEM 等) およびベースマップ |
| 投稿やデータの保存先 | Sentinel Hub クラウド (カスタムの Evalscript、ピン、比較設定等の保存機能。アカウント連携時) |
| 配信 | Amazon CloudFront (`via: CloudFront`) |

メモ:

- JavaScript ベースの `Evalscript` をブラウザ上で編集し、任意のバンド組み合わせや指数 (NDVI、NDWI 等) をリアルタイム計算できる。
- EU の Copernicus Data Space Ecosystem 向けに同系統のコードベースを用いた Copernicus Browser が運用されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 衛星観測データ (Sentinel, Landsat 等) | 欧州宇宙機関 (ESA) Copernicus 計画、USGS / NASA 等 | EO Browser および Copernicus Browser のデータセット説明 |
| アプリケーションの依存ライブラリ | GitHub (`sentinel-hub/EOBrowser`) の `package.json` | GitHub リポジトリ公開情報 |
