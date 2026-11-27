---
financial: commercial
organization: corp-smb
first_seen: 2013-08-07
first_seen_by: wayback
---

# onX

- URL: https://www.onxmaps.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: onX、onXmaps、onX Hunt、onX Offroad、onX Backcountry、公有地境界、地籍図、土地所有者、オフライン GPS

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 米国・カナダの公有地・私有地の境界線と土地所有者情報、オフロード・雪山・登山向けの専門レイヤーを備えたアウトドア GPS 地図アプリ群 |
| 提供する価値 | 圏外の山野や林道でも、現在地が公有地か私有地か (境界線と所有者名) を正確に判別でき、狩猟区画・雪崩地形・林道状況などを確認できる |
| 想定する利用者 | ハンター (onX Hunt)、オフロード車・バギー愛好家 (onX Offroad)、バックカントリー・登山者 (onX Backcountry)、林業・不動産等の業務利用者 |
| 商用か非商用か | 商用 (アプリ別にサブスクリプション課金。例: onX Hunt は 1 州 Premium 年額約 $34.99、全 50 州+カナダ Elite 年額約 $99.99 / 月額約 $14.99。法人向け onX for Business も年額約 $99.99/人) |
| 推定の売上 | 推測: 年数百億円規模 (Series B で 8,740 万ドル等を調達、ARR が 4 年で 10 倍成長と発表され、未上場ながら企業価値は数億〜10 億ドル規模と評価されている) |
| 運営 | 企業 (onXmaps, Inc.、米国モンタナ州ミズーラ。2009 年に Eric Siegfried 氏が創業) |
| 推定の運用費 | 推測: 月数千万円以上 (全米・カナダ全土の地籍・土地所有者データのライセンス取得・正規化、LiDAR・衛星データ処理、GCP 上のマイクロサービス群を維持) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (2026-11-16 のマーケティングサイト観測では WordPress テーマ `onx-core` のみ検出。ネイティブアプリは Swift (iOS) / Kotlin + Jetpack Compose (Android) で構築) |
| フレームワーク | WordPress (マーケティングサイト。バックエンド基盤は Go、Elixir、Python on GCP / Kubernetes を採用) |
| 背景の地図とタイル | 自社整備の衛星画像・LiDAR 地形・地籍レイヤー等 (Apple CarPlay / Android Auto にも対応) |
| 投稿やデータの保存先 | Google Cloud Platform (GCP) 上の自社空間データベース (`via: 1.1 google` を確認) |
| 配信 | Istio Envoy + Google Cloud (`server: istio-envoy`、`via: 1.1 google` を応答ヘッダーで確認) |

メモ:

- ウェブ版マップのほか、用途別の iOS / Android アプリ「onX Hunt」「onX Offroad」「onX Backcountry」を提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 土地境界・所有者データ | 米国各郡 (County) の公的登記・地籍データ、連邦・州の公有地管理機関 (BLM、USFS 等) | 公式サイトおよび製品説明 |
| 地形・林道・雪崩データ | USGS、LiDAR、衛星画像、各種トレイル・林道管理機関 | 公式サイト |
