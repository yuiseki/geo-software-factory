---
financial: commercial
organization: corp-ent
first_seen: 1996-12-20
first_seen_by: wayback
---

# アットホーム (at home)

- URL: https://www.athome.co.jp/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: アットホーム、at home、athome、不動産、賃貸、売買、地図検索、ATBB、不動産情報サイト

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国数万店の加盟不動産会社ネットワークを基盤に、賃貸・売買・事業用物件を地図やエリアから探せる老舗の不動産情報ポータル |
| 提供する価値 | 地域密着の不動産会社が登録する豊富な物件情報を地図上でエリア・路線別に絞り込め、周辺環境や街情報とともに比較できる |
| 想定する利用者 | 住まいや事業用物件を探す一般消費者・法人、および不動産会社間情報流通システム (ATBB 等) を利用する加盟不動産会社 |
| 商用か非商用か | 商用 (一般利用者は無料。加盟不動産会社向けのネットワーク利用料、物件掲載・広告・業務支援システム利用料で運営) |
| 推定の売上 | 約 359 億 1,500 万円 (アットホーム株式会社 2025 年 6 月期〜2026 年 5 月期の売上高。非上場企業) |
| 運営 | 企業 (アットホーム株式会社、1967 年設立) |
| 推定の運用費 | 未確認 (消費者向けサイトと不動産会社間ネットワーク ATBB の基盤、外部地図 API 利用料、CloudFront 配信の運用) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (`https://www.athome.co.jp/chintai/tokyo/map/` の初期 HTML は Angular の SPA シェルであり、地図用遅延読み込みチャンクの直接取得は未完了。公開情報では Google Maps Platform やいつもNAVI、MapFan API 等の採用が知られる) |
| フレームワーク | Angular (`polyfills-*.js`, `scripts-*.js`, `main-*.js` の構成と `pc-area-map-rent-living-routing.module-*.js` 等の Angular ルーティングチャンクを確認) |
| 背景の地図とタイル | 未確認 (公開資料では Google Maps、ゼンリンデータコム「いつもNAVI」、ジオテクノロジーズ「MapFan API」等の利用事例あり) |
| 投稿やデータの保存先 | アットホーム自社基盤 (加盟不動産会社からの入稿データおよび ATBB 流通データ) |
| 配信 | Amazon CloudFront (`server: CloudFront`, `via: ... cloudfront.net (CloudFront)` ヘッダーを確認) |

メモ:

- 地図検索ページ (`https://www.athome.co.jp/chintai/tokyo/map/`) は Angular 製の SPA で構成されており、地図画面のモジュールが遅延読み込みされる設計になっている。
- 2026-11-16 時点の `curl` 観測ではルーティングチャンクの直接取得が制限されたため、実際にロードされる地図描画ライブラリの特定は未確認とし、公開技術情報と併記した。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| フロントエンド構成・配信基盤 | Angular SPA、Amazon CloudFront | `https://www.athome.co.jp/chintai/tokyo/map/` の応答ヘッダーと HTML/JS (2026-11-16 観測) |
| 地図 API 採用事例 | Google Maps、いつもNAVI、MapFan API 等 | 公開技術資料・導入事例 |
| 売上高・会社概要 | アットホーム株式会社 公開会社情報 | 採用情報・会社概要ページ |
