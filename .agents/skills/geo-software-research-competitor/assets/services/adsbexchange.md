---
financial: commercial
organization: corp-smb
---

# ADS-B Exchange

- URL: https://www.adsbexchange.com/ (地図: https://globe.adsbexchange.com/)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ADS-B Exchange、ADSBx、航空機追跡、ADS-B、tar1090、無修正フライト追跡、軍用機、flight tracker、OSINT

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中の有志が設置した受信機からの ADS-B 信号をブロックやフィルタリングなしで地図表示・提供する航空機追跡サービス |
| 提供する価値 | 商用大手サイトが非表示にする軍用機・政府機関機・プライベートジェット等を含む、生かつ無フィルタの航空機位置データのリアルタイム閲覧 |
| 想定する利用者 | 航空愛好家、OSINT 調査者、ジャーナリスト、航空データを利用する法人および金融・市場調査関係者 |
| 商用か非商用か | 商用 (一般向けライブマップは広告付き無料、エンタープライズ向けデータフィードや市場分析パッケージを親会社 JETNET 経由で有料提供) |
| 推定の売上 | 未確認 (2023 年 1 月に航空市場情報企業 JETNET が推定約 2,000 万ドルで買収。買収後の単体売上は非公開) |
| 運営 | 企業 (JETNET 傘下、プライベートエクイティ Silversmith Capital Partners の支援を受ける) |
| 推定の運用費 | 未確認 (25,000 台超の受信機から毎秒 75 万件以上のメッセージを収集・MLAT 計算し、Cloudflare 越しに配信) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | OpenLayers + HTML5 Canvas (バンドル JS 内に `ol.` および HTML 内に `Canvas` を確認。OSS の `tar1090` ベース) |
| フレームワーク | jQuery (バンドル JS 内に `jQuery` を確認。また HTML 内に `tar1090` の記述を確認) |
| 背景の地図とタイル | OpenStreetMap 等 (HTML 内に `Osm` の記述を確認) |
| 投稿やデータの保存先 | ADS-B Exchange 自社サーバー (有志の ADS-B / Mode S / MLAT フィーダーからの集約データ) |
| 配信 | Cloudflare (`server: cloudflare`, `cf-ray` ヘッダーを確認) |

メモ:

- 2023 年の JETNET による買収後、無償で受信機を提供していたコミュニティから反発が起き、adsb.lol などのフォーク・代替ネットワークが生まれるきっかけとなった。
- `globe.adsbexchange.com` は `tar1090` をカスタマイズした Web UI を採用している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 航空機位置・ADS-B / Mode S / MLAT | 世界中のボランティアフィーダーの受信機ネットワーク | ADS-B Exchange 公式サイトおよび JETNET 発表 |
| 地図ライブラリ・背景地図・配信基盤 | OpenLayers (`ol.`)、jQuery、OSM、`tar1090`、Cloudflare | `https://globe.adsbexchange.com/` の HTTP 応答ヘッダー、HTML、JS バンドル (2026-11-16 観測) |
