---
financial: commercial
organization: corp-smb
---

# Outdooractive

- URL: https://www.outdooractive.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Outdooractive、アウトドアナビ、ドイツ、公式地形図、Ordnance Survey、Swisstopo、ルートプランナー、観光 DMO

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 欧州を中心に各国の公的地形図と観光団体公式ルート・ユーザー投稿ルートを統合したアウトドア向け地図・ナビゲーションプラットフォーム |
| 提供する価値 | 英国 Ordnance Survey、スイス Swisstopo、ドイツ BKG、日本国土地理院などの公式地形図を切り替えながらルート計画・オフライン案内ができ、観光局向け CMS (MyBusiness) も備える |
| 想定する利用者 | 欧州および世界のハイカー・サイクリスト・スキーヤー、地域の観光協会 (DMO)・自治体、アウトドアメディア |
| 商用か非商用か | 商用 (B2C は広告付き無料プランのほか Pro / Pro+ 年額約 €29.99〜€59.99。B2B 向けに観光団体・企業向け SaaS「MyBusiness」や Map/Data API を提供) |
| 推定の売上 | 推測: 年数百万〜十数億円以上 (欧州最大級のアウトドアプラットフォームとして B2C 課金と観光局・企業向け B2B SaaS を展開。非上場のため公式売上は非公開) |
| 運営 | 企業 (Outdooractive AG、ドイツ・バイエルン州インメンシュタット) |
| 推定の運用費 | 推測: 月数万〜数十万ユーロ規模 (多数の各国公的機関からの地図ライセンス料、高精度ベクトル/ラスタタイル配信、B2B API 基盤の維持) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (2026-11-16 の HTTP 観測ではルート URL `/` が HTTP 404 Not Found となり HTML/JS を取得できず。開発者向けに独自 Map API / FlexView API を提供) |
| フレームワーク | 未確認 |
| 背景の地図とタイル | 各国の公式地形図 (Ordnance Survey、Swisstopo、USGS、BKG、BEV、IGN、CNIG、GSI 等) および自社アウトドアベクター地図 |
| 投稿やデータの保存先 | 自社のルート・POI データベース (MyBusiness 経由で観光団体が公式データを管理) |
| 配信 | nginx (`server: nginx` を応答ヘッダーで確認) |

メモ:

- 2026-11-16 の一次 HTTP 観測ではトップ URL `https://www.outdooractive.com` が HTTP 404 を返した (通常は `/en/` や `/de/` 等の言語パスへ誘導される構成とみられる)。
- ウェブ版のほか iOS / Android アプリ (一般向けおよび編集者向け「Outdooractive MyBusiness」) を提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 公式地形図・登山地図 | Ordnance Survey、USGS、BKG、BEV、Swisstopo、IGN、CNIG、Lantmäteriet、Kartverket、国土地理院 (GSI)、アルプス協会等 | アプリストア説明・公式サイト |
| トレイル・POI データ | 観光協会 (DMO)・自治体パートナーおよびユーザー投稿 | 公式サイト |
