---
financial: commercial
organization: corp-ent
first_seen: 2019-07-20
first_seen_by: wayback
---

# アパホテル 地図検索

- URL: https://map.apahotel.com/map
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ホテル検索、アパホテル、APA HOTEL、ビジネスホテル、地図検索、GOGA、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 国内外のアパホテルネットワーク (直営・FC・アパ直参画ホテル等) をインタラクティブな地図上から検索し、予約ページへ進める公式地図検索サイト |
| 提供する価値 | 駅・エリア・現在地周辺のホテルの立地関係と価格帯・空室状況への導線を地図上で一覧比較しながら選べる |
| 想定する利用者 | 出張や観光でアパホテルや提携ホテルの宿泊先を立地重視で探している旅行者・ビジネス客 |
| 商用か非商用か | 商用 (自社予約サイト「アパ直」への宿泊予約送客として提供。検索ページの利用料は無料) |
| 推定の売上 | 推測: 地図検索単体の売上は 0 円。アパグループ (2025年11月期連結売上高 約2,667億円、アパホテルネットワーク 1,056ホテル) の宿泊予約売上に貢献 |
| 運営 | 企業 (アパホテル株式会社 / アパグループ。地図検索システムは株式会社ゴーガの StoreLocator を採用) |
| 推定の運用費 | 推測: 月数十万円。nginx + CloudFront + Amazon S3 による配信費に加え、GOGA StoreLocator の SaaS 利用料および Google Maps JavaScript API の従量課金がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`//maps.google.com/maps/api/js?v=quarterly&libraries=geometry&key=...`) + 株式会社ゴーガ (GOGA) StoreLocator (`/static/js/sl/common.js`、`/static/js/sl/hybrid.js`、`geolocation-marker.js`) |
| フレームワーク | jQuery 1.9.1 + Underscore.js + Backbone.js (`jquery-1.9.1.min.js`、`underscore-min.js`、`backbone-min.js`) |
| 背景の地図とタイル | Google マップ (Google Maps JavaScript API 経由) |
| 投稿やデータの保存先 | GOGA StoreLocator 基盤およびアセット配信用 S3 (`//sl-goga-jp.s3.amazonaws.com/resource/apahotel/...`) |
| 配信 | nginx + Amazon CloudFront (`server: nginx`、`via: ...cloudfront.net`) |

メモ:

- URL サブドメイン (`map.apahotel.com`) を用いた専用の地図検索サイトとして構築されており、Backbone.js ベースの GOGA StoreLocator テンプレートと S3 上の専用アセット (`sl-goga-jp.s3.amazonaws.com`) を読み込んでいる

データの出どころ (2026-11-17):

- ホテルデータ: アパホテル株式会社管理のホテル情報
- 背景地図: Google (Google Maps Platform)
- 地図検索システム: 株式会社ゴーガ (GOGA StoreLocator)
