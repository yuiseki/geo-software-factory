---
financial: commercial
organization: corp-smb
first_seen: 2021-09-21
first_seen_by: wayback
---

# PurpleAir

- URL: https://map.purpleair.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: PurpleAir、PM2.5、空気質センサー、大気汚染マップ、クラウドソーシング観測、Mapbox、IoT

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中の利用者が設置した Wi-Fi 接続型空気質センサーの PM2.5・PM10 データを 2 分間隔でリアルタイム表示する地図サービス |
| 提供する価値 | 公的観測局の隙間を埋める高密度な市民センサー網により、山火事の煙や局地的な大気汚染の変化をほぼリアルタイムで把握できる |
| 想定する利用者 | 山火事や大気汚染地域の住民、環境研究者、自治体・学校、空気質データを取得したい開発者 |
| 商用か非商用か | 商用 (地図の閲覧は無料。物理センサー販売 $199〜$279 程度が収益柱。API はポイント制の従量課金で、センサー所有者は自機データの取得クレジット優遇あり) |
| 推定の売上 | 推測: 年数億〜十数億円規模 (ハードウェアセンサー販売および従量課金 API を展開する米国非上場企業だが、公式売上は非公開) |
| 運営 | 企業 (PurpleAir, Inc.、米国ユタ州。2015 年に Adrian Dybwad 氏が開始、2016 年法人化) |
| 推定の運用費 | 推測: 月百万円〜数百万円規模。世界中の数万台のセンサーから 2 分ごとに届くテレメトリーの受信・DB 保存と Google Cloud 上での地図・API 配信を維持している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Mapbox (2026-11-16 の `tech_hits` で `Mapbox` を検出、CSP の `connect-src` に `api.mapbox.com` および `api.maptiler.com` を確認) |
| フレームワーク | React (2026-11-16 の `tech_hits` で `React` を検出、`/pa.loader.3.2.7-*.js` を読み込み) |
| 背景の地図とタイル | Mapbox / MapTiler / Google Maps (CSP の `connect-src` と `img-src` で `api.mapbox.com`、`api.maptiler.com`、`maps.googleapis.com`、`maps.google.com` を確認) |
| 投稿やデータの保存先 | 自社の PurpleAir API / センサーデータ基盤 (`www2.purpleair.com` への通信を CSP で確認) |
| 配信 | Google Frontend (`server: Google Frontend` を応答ヘッダーで確認) |

メモ:

- 公式の専用モバイルアプリ (iOS / Android) は原則提供しておらず、Web マップ (`map.purpleair.com`) と API を通じてサードパーティ製アプリや自治体ダッシュボードにデータを提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| PM2.5 / PM10 / 温湿度 | 世界中の個人・研究機関・自治体が設置した PurpleAir センサー | 公式サイトおよび製品説明 |
| 背景地図 | Mapbox / MapTiler / Google Maps | 応答ヘッダー CSP 観測 |
