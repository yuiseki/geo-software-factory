---
financial: commercial
organization: corp-smb
---

# Transitland

- URL: https://www.transit.land
- ソース: https://github.com/transitland/transitland-atlas (GPL-3.0 / 商用ライセンスのデュアル構成を含む各種関連リポジトリ)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Transitland、GTFS、GTFS Realtime、GBFS、公共交通データ、バス、鉄道、Interline、MapLibre

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中のバス・鉄道・地下鉄・フェリー等の公共交通データ（GTFS / GTFS-RT / GBFS）を集約し、API・アーカイブ・地図で提供する交通データ基盤 |
| 提供する価値 | 各交通事業者がバラバラに公開している時刻表や路線・停留所データを統一形式で検索・ダウンロードでき、過去の履歴アーカイブまで開発や分析に使える |
| 想定する利用者 | 乗換案内・MaaS アプリ開発者、交通計画・都市研究のデータアナリスト、自治体、交通事業者 |
| 商用か非商用か | 商用 (個人・研究・非商用向けの無料枠あり。商用利用は従量課金プランまたは Enterprise 契約が必要) |
| 推定の売上 | 推測: 年数千万円〜数億円規模 (米国の Interline Technologies が開発・運営し、API 課金や交通データ基盤の受託・エンタープライズ契約で収益化。非公開) |
| 運営 | 企業 (Interline Technologies, LLC、米国。公共交通標準化団体 MobilityData ともエコシステムで連携) |
| 推定の運用費 | 推測: 月数十万〜数百万円規模。世界中の数千の GTFS フィードの定期取得・検証・履歴アーカイブ保存と API・Nuxt サイト配信を維持している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre (応答 HTML 内に `maplibre` の記述を確認) |
| フレームワーク | Nuxt (`x-powered-by: Nuxt` 応答ヘッダーおよび `/_nuxt/UNsuUV4O.js` を確認。一部 `React` の記述も検出) |
| 背景の地図とタイル | 自前ホストまたは外部のベクタタイル (公共交通路線・停留所を重畳表示) |
| 投稿やデータの保存先 | Transitland データベース + GitHub (`transitland-atlas` にフィード定義を集約管理) |
| 配信 | Cloudflare (`server: cloudflare` を応答ヘッダーで確認) |

メモ:

- 一般消費者向けの公式 iOS / Android アプリはなく、開発者・アナリスト向けの API・データセット・ウェブビューアとして提供されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 時刻表・路線・停留所データ | 世界中の公共交通事業者が公開する GTFS / GTFS Realtime / GBFS フィード (Transitland Atlas 経由で登録) | 公式サイト・GitHub |
