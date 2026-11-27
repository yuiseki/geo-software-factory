---
financial: public-service
organization: gov-central
first_seen: 2012-05-17
first_seen_by: wayback
---

# NASA FIRMS

- URL: https://firms.modaps.eosdis.nasa.gov/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: NASA FIRMS、山火事、火災検知、熱異常、MODIS、VIIRS、衛星観測、LANCE、防災マップ

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 衛星観測 (MODIS・VIIRS) による世界中の火災・熱異常を準リアルタイムで可視化・配信する NASA の公式火災情報システム |
| 提供する価値 | 地球観測衛星が検知した火災ホットスポットを発生から数時間以内に世界地図上で確認でき、CSV / Shapefile / WMS / API で無償取得できる |
| 想定する利用者 | 消防機関、森林・防災担当者、環境研究者、報道機関、災害マップ開発者 |
| 商用か非商用か | 非商用 (米国政府機関 NASA による公共事業。閲覧・アラート・API・データダウンロードすべて無料、要無料 Map Key) |
| 推定の売上 | 0 円 (連邦政府予算による公的運営であり、商業売上はない) |
| 運営 | 政府機関 (アメリカ航空宇宙局 NASA / Goddard Space Flight Center、LANCE EOSDIS プログラム) |
| 推定の運用費 | 推測: 政府予算による運用 (衛星データの受信・処理基盤 LANCE/EOSDIS の一部として維持されており、単独の運用費は非公開) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (2026-11-16 のトップページ観測では地図ライブラリ未検出。NASA GIBS/FIRMS の公開マップ連携では OpenLayers / Leaflet / Mapbox Vector Tiles の利用例が案内されている) |
| フレームワーク | 未確認 |
| 背景の地図とタイル | NASA GIBS (Global Imagery Browse Services) の衛星画像タイルや背景図等を配信 |
| 投稿やデータの保存先 | NASA EOSDIS / LANCE の地球観測データ基盤 |
| 配信 | nginx (`server: nginx` を応答ヘッダーで確認) |

メモ:

- モバイルアプリは提供しておらず、Web マップ、メールアラート、WMS/WFS/REST API を通じてデータを提供している。
- Watch Duty など多くの民間の山火事・防災地図サービスが、この FIRMS の MODIS / VIIRS データを一次情報源として利用している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 火災・熱異常データ | NASA MODIS (Terra/Aqua) および VIIRS (Suomi NPP/NOAA-20/NOAA-21) | 公式サイト (https://firms.modaps.eosdis.nasa.gov/) |
| 衛星背景画像 | NASA GIBS (EOSDIS) | NASA 公式ドキュメント |
