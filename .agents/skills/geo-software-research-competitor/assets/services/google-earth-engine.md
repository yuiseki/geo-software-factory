# Google Earth Engine

- URL: https://earthengine.google.com
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Google Earth Engine、GEE、衛星データ解析、Landsat、Sentinel、リモートセンシング、Google Cloud、EECU、Code Editor

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 数十ペタバイト規模の地球観測衛星アーカイブと Google のクラウド分散計算基盤を組み合わせ、地球規模の空間解析を行えるプラットフォーム |
| 提供する価値 | 大容量の衛星画像を手元にダウンロードせずに、ブラウザ上の Code Editor や Python/JavaScript API から過去数十年分の衛星データをオンザフライで解析・可視化できる |
| 想定する利用者 | 気候変動・森林・農業・水資源の研究者、NGO・報道機関、衛星データ解析を業務利用する民間企業・政府機関 |
| 商用か非商用か | 商用・非商用ハイブリッド (学術・教育・非営利・報道・個人の非商用研究は無料。企業や行政の実務利用は Google Cloud 課金による有料プラン: プラットフォーム月額 + ストレージ + EECU 計算量従量課金) |
| 推定の売上 | 非公開 (Google Cloud の地理空間サービス群の一部として展開) |
| 運営 | 企業 (Google LLC、米国) |
| 推定の運用費 | 推測: 月数千万円〜億円以上 (数十ペタバイト級の衛星画像アーカイブ保管と分散並列計算クラスタの運用) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API ベース (Code Editor および Earth Engine Apps 上で計算結果を動的タイル化して表示) |
| フレームワーク | 独自 JavaScript バンドル (`/static/js/main.min.js` を確認) + Google Cloud 基盤 |
| 背景の地図とタイル | Google Maps ベースマップおよび Earth Engine 計算サーバーがオンザフライ生成する解析結果タイル |
| 投稿やデータの保存先 | Google Cloud / Earth Engine Asset Store (解析スクリプト、アセット、BigQuery 連携) |
| 配信 | Google フロントエンド (`server: sffe` を応答ヘッダーで確認) |

メモ:

- 専用の iOS / Android アプリは提供されていない (Web ブラウザ上の Code Editor・Earth Engine Apps および Python/JS クライアントライブラリ)。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 衛星画像・地球観測データカタログ | USGS/NASA (Landsat, MODIS)、ESA (Copernicus Sentinel)、NOAA、JAXA 等 | Earth Engine Data Catalog |
| 背景地図 | Google Maps 基盤データ | サービス画面 |
