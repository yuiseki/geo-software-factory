---
financial: commercial
organization: corp-ent
first_seen: 2020-12-01
first_seen_by: github
---

# Microsoft Planetary Computer

- URL: https://planetarycomputer.microsoft.com
- ソース: https://github.com/microsoft/PlanetaryComputer (MIT License)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Microsoft Planetary Computer、STAC、Azure、COG、GeoParquet、TiTiler、MapLibre、衛星データ、環境データ

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界の衛星画像や環境データセットを STAC API とクラウドネイティブ形式 (COG / GeoParquet) で統一公開し、ブラウザや Python から解析できる基盤 |
| 提供する価値 | Landsat や Sentinel などのペタバイト級データを登録不要・無料で STAC 検索や動的タイル表示 (TiTiler) でき、オープンな標準仕様のままクラウド環境で解析できる |
| 想定する利用者 | 環境・気候研究者、地理空間データエンジニア、AI/機械学習開発者、衛星データを自前アプリに組み込みたい企業 |
| 商用か非商用か | 非商用・無料カタログ + 商用エンタープライズ版ハイブリッド (公開データカタログ・STAC API・Explorer は無料。自社データ管理向けの Microsoft Planetary Computer Pro は Azure 従量課金) |
| 推定の売上 | 単体売上は非公開 (Microsoft Azure のクラウド利用促進および Planetary Computer Pro の Azure 収益) |
| 運営 | 企業 (Microsoft Corporation、米国) |
| 推定の運用費 | 推測: 月数千万円〜億円規模 (Azure Blob Storage 上でのペタバイト級データ保管および動的タイル生成・JupyterHub 基盤) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS (Explorer 等の地図描画で MapLibre 採用・公式ライブラリ `maplibre-gl-planetary-computer` 等を提供) |
| フレームワーク | React (`/assets/index-DFNtrImA.js` および `tech_hits` の `React` を確認) |
| 背景の地図とタイル | Azure Maps / OpenStreetMap 系ベースマップおよび TiTiler + STAC API による動的衛星タイル |
| 投稿やデータの保存先 | Microsoft Azure Blob Storage (公開データカタログ、GeoCatalog、JupyterHub ユーザー環境) |
| 配信 | Microsoft Azure / Azure Front Door (`consentdeliveryfd.azurefd.net`、`x-cache: CONFIG_NOCACHE` を確認) |

メモ:

- 専用の iOS / Android アプリは提供されていない (Web Explorer、STAC API、Python JupyterHub 環境)。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 衛星・環境・気象データ | ESA (Sentinel)、USGS/NASA (Landsat, NAIP, MODIS)、NOAA、GBIF、ECMWF (ERA5) 等 | Planetary Computer Data Catalog |
