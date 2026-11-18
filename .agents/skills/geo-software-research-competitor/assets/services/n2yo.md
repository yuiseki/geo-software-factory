---
financial: commercial
organization: individual
---

# N2YO

- URL: https://www.n2yo.com
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: N2YO、人工衛星追跡、ISS、スターリンク、TLE、軌道予測、可視パス、Leaflet、satellite.js

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 国際宇宙ステーション (ISS) やスターリンクなど数万個の人工衛星の現在位置・軌道・上空通過予測をリアルタイム地図で追えるウェブサイト |
| 提供する価値 | 専門知識なしで任意の人工衛星の現在地、太陽光の昼夜境界線 (Terminator)、自宅上空の肉眼観測・無線交信向け通過予測を無料で確認でき、REST API も個人向けに無料開放している |
| 想定する利用者 | 天体観測・宇宙ファン、アマチュア無線家、衛星の位置予測データを使いたい開発者・学生 |
| 商用か非商用か | 商用・広告モデル (Web サイトは Google AdSense 広告付きで無料。REST API v1 も個人キー発行で 1時間あたり 100〜1,000 リクエストまで無料、大口商用利用は個別相談) |
| 推定の売上 | 推測: 年数百万円〜数千万円規模 (世界的な宇宙・アマチュア無線ファン向けトラフィックによる広告収入が主体) |
| 運営 | 個人 (Ciprian Sufitchi、アマチュア無線家・ソフトウェア開発者) |
| 推定の運用費 | 推測: 月数万円〜数十万円程度 (Apache + PHP サーバー。軌道伝播計算はブラウザ側の `satellite.js` でも処理するためサーバー負荷が抑えられている) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (`/js/leaflet/leaflet.js`, `L.Terminator.js`, `Leaflet.Antimeridian.js` を確認) + `satellite.js` (`/js/satellite-js/dist/satellite.min.js` でクライアント側 SGP4 軌道計算) |
| フレームワーク | jQuery + PHP/8.5.12 (`x-powered-by: PHP/8.5.12` および `/js/jquery.js`, `/js/n2yo4.0.js` を確認) |
| 背景の地図とタイル | OpenStreetMap タイル (Leaflet の帰属表示で確認) |
| 投稿やデータの保存先 | 自前サーバー (無料ユーザーアカウント、API キー、通過アラート通知設定) |
| 配信 | Apache (`server: Apache` を応答ヘッダーで確認) |

メモ:

- 専用の iOS / Android ネイティブアプリは提供されていない (モバイルブラウザ対応のレスポンシブ Web サイトおよび REST API を提供)。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 人工衛星の軌道要素 (TLE) | CelesTrak、米国宇宙軍 / Space-Track 等の公開軌道カタログ | API ドキュメント・サイト説明 |
| 背景地図 | OpenStreetMap contributors (ODbL) | 地図上の帰属表示 |
