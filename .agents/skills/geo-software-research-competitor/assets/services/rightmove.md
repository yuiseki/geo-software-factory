---
financial: commercial
organization: corp-ent
first_seen: 2000-03-02
first_seen_by: wayback
---

# Rightmove

- URL: https://www.rightmove.co.uk
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Rightmove、英国不動産、ロンドン、住宅検索、賃貸、Draw a Search、Google Maps、ポリゴン検索

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 英国の売買・賃貸・新築・商業不動産を網羅し、地図上の手描き範囲指定検索 (Draw a Search) で物件を探せる英国最大の不動産ポータル |
| 提供する価値 | 地図上に自分で描いたポリゴン範囲や駅・学校・施設との位置関係から物件を直感的に絞り込め、英国の過去の成約価格履歴や AI 自然言語検索と合わせて住まい探しができる |
| 想定する利用者 | 英国で住宅購入・賃貸を探す一般消費者、および物件を掲載する英国の不動産仲介会社・新築デベロッパー |
| 商用か非商用か | 商用 (一般利用者は無料。不動産会社・デベロッパー向けの月額掲載サブスクリプション、エージェント向け CRM/SaaS ツール、金融・データサービスで収益化) |
| 推定の売上 | 約3億8,990万ポンド (2024年実績、Rightmove plc) |
| 運営 | 企業 (Rightmove plc、英国ミルトン・キーンズ、ロンドン証券取引所上場) |
| 推定の運用費 | 推測: 年数十億〜百億円規模。英国全土の物件・画像配信、Google Maps API / Google Cloud 基盤、Varnish 等の配信インフラ運用 |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (`https://www.rightmove.co.uk` は HTTP 403 Forbidden のため直接観測不可。公開情報では Google Maps API を用いて物件ピン表示や Draw a Search 機能を提供していると報告されている) |
| フレームワーク | 未確認 (HTTP 403 Forbidden のため HTML/JS の直接観測不可) |
| 背景の地図とタイル | 未確認 (HTTP 403 のため直接のタイル通信先は未確認。公開事例では Google Maps Platform / Google Cloud を利用) |
| 投稿やデータの保存先 | Rightmove 自社基盤 (英国の不動産会社から入稿される物件データ、成約履歴データ) |
| 配信 | Varnish (`server: Varnish`、`via: 1.1 varnish` を確認。HTTP 403 Forbidden) |

メモ:

- 2026-11-16 時点の HTTP 観測では `HTTP 403 Forbidden` (`Server: Varnish`) が返却されたため、フロントエンドの地図実装は直接観測できていない。
- ウェブ版のほか iOS / Android アプリも提供されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 売買・賃貸物件情報 | 加盟不動産会社・ディベロッパー | Rightmove 公式サイト |
| 過去の成約価格データ | HM Land Registry (英国土地登記所) 等の公的データ | Rightmove 公式サイト |
| ベースマップ・地域情報 | Google Maps Platform (公開情報による。直接通信は未確認) | Google Cloud / Rightmove 公開事例 |
