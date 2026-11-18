---
financial: commercial
organization: corp-ent
---

# Realtor.com

- URL: https://www.realtor.com
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Realtor.com、Move Inc、News Corp、米国不動産、MLS、住宅検索、3Dマップ、Google Maps、FlyAround

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全米リアルター協会 (NAR) との提携のもと、米国の売買・賃貸・新築物件を MLS 連動の最新情報と 3D 地図検索で探せる大手不動産ポータル |
| 提供する価値 | 地図上で学区・洪水/山火事リスク・騒音・周辺環境を重ねて比較でき、Google 3D Maps を活用した「FlyAround」等で現地に行かずに街並みや地形を立体的に確認できる |
| 想定する利用者 | 米国で住宅購入・賃貸・売却を検討する一般消費者、および見込み客 (リード) を獲得したい不動産エージェント・ディベロッパー |
| 商用か非商用か | 商用 (一般利用者は無料。不動産エージェントへのリード紹介・成約課金、エージェント向け SaaS、新規物件・賃貸広告収入で運営) |
| 推定の売上 | 約5.44億ドル (2024年6月期)、約5.52億ドル (2025年6月期、Move, Inc. 実績・News Corp 開示) |
| 運営 | 企業 (Move, Inc.、米国、News Corp 傘下) |
| 推定の運用費 | 推測: 年百億円以上。全米 MLS データ連携基盤、Google Maps Platform (3D Maps 等)、CloudFront / Kasada ボット防御の運用 |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (`https://www.realtor.com` は HTTP 429 のため直接観測不可。Google Maps Platform の公開事例では 3D Maps 等を用いた「FlyAround」機能を提供していると報告されている) |
| フレームワーク | 未確認 (HTTP 429 のため HTML/JS の直接観測不可) |
| 背景の地図とタイル | 未確認 (HTTP 429 のため直接のタイル通信先は未確認。公開事例では Google Maps Platform を利用) |
| 投稿やデータの保存先 | Move, Inc. 自社基盤 (全米 MLS 物件情報、不動産エージェント・リード管理データ) |
| 配信 | Amazon CloudFront + Kasada (`server: CloudFront`、`x-cache: LambdaGeneratedResponse`、`/ips.js?KP_UIDz=...` を確認。HTTP 429) |

メモ:

- 2026-11-16 時点の HTTP 観測では CloudFront + Kasada によるアクセス制限 (`HTTP 429`) が返却されたため、フロントエンドの地図実装は直接観測できていない。
- ウェブ版のほか iOS / Android アプリも提供されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 売買・賃貸物件情報 | 米国各地の MLS、不動産ブローカー、新築デベロッパー | Realtor.com 公式サイト |
| ベースマップ・3D 空間地図 | Google Maps Platform (公開導入事例による。直接通信は未確認) | Google Maps Platform 公式ケーススタディ |
