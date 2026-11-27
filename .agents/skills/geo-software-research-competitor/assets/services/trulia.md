---
financial: commercial
organization: corp-ent
first_seen: 2005-10-13
first_seen_by: wayback
---

# Trulia

- URL: https://www.trulia.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Trulia、トゥルーリア、不動産、米国、住宅購入、賃貸、近隣情報、治安マップ、学校区、Zillow Group

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 米国の売買・賃貸物件を検索でき、治安・学校区・通勤時間・生活環境などの近隣インサイトを地図上のレイヤーで可視化する不動産ポータル |
| 提供する価値 | 物件情報だけでなく、地元の住民レビューや犯罪・学校・交通などの近隣データ (Neighborhoods) を地図上で重ねて確認でき、住みやすさまで含めて判断できる |
| 想定する利用者 | 米国で住宅購入や賃貸物件を探す消費者、および購入・入居見込み客を獲得したい不動産業者・エージェント |
| 商用か非商用か | 商用 (消費者の利用は無料。不動産業者・エージェント向けのリード送客・広告サービス等により収益化) |
| 推定の売上 | 親会社 Zillow Group 全体の 2024 年通期売上は 22 億ドル (Trulia 単体の売上は非開示) |
| 運営 | 企業 (Zillow Group, Inc.、米国。2015年に Zillow が Trulia を買収) |
| 推定の運用費 | 推測: 月数千万円〜数億円規模 (全米の MLS 物件データ、高解像度写真、近隣統計・地図レイヤー、CloudFront 配信の維持) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (`https://www.trulia.com/` は HTTP 403 となり HTML/JS の直接観測不可。公開情報では Google Maps API を用いた物件マップ、ヒートマップ、Street View 連携の歴史的採用が知られる) |
| フレームワーク | 未確認 (HTTP 403 のため直接観測不可) |
| 背景の地図とタイル | 未確認 (HTTP 403 のため直接観測不可。公開情報では Google Maps を中心に治安・学校区等の独自オーバーレイを表示) |
| 投稿やデータの保存先 | Zillow Group 自社基盤 (MLS 物件データ、近隣統計、住民レビュー) |
| 配信 | Amazon CloudFront (`Server: CloudFront`、`x-cache: LambdaGeneratedResponse from cloudfront` ヘッダーを確認。HTTP 403) |

メモ:

- 2026-11-16 時点の HTTP 一次観測では `HTTP 403` (`Server: CloudFront`) が返却されたため、フロントエンドの地図ライブラリの直接観測はできていない。
- ウェブ版のほか、iOS / Android 向けの公式モバイルアプリ（Trulia Real Estate & Rentals 等）を提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 売買・賃貸物件情報 | 米国 MLS (Multiple Listing Service) および不動産仲介会社 | Trulia 公式サイトおよび Zillow Group 公開情報 |
| 近隣・学校・治安情報 | 公的統計、学校データ、住民コミュニティ投稿 | Trulia 公式サイト |
