---
financial: commercial
organization: corp-ent
first_seen: 2023-02-03
first_seen_by: wayback
---

# chocoZAP (チョコザップ) 店舗検索

- URL: https://chocozap.jp/studios/search/area
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、チョコザップ、chocoZAP、コンビニジム、24時間ジム、RIZAP、フィットネス、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国 1,800 店舗以上の chocoZAP (チョコザップ) をエリア・都道府県や地図から検索できる公式店舗検索ページ |
| 提供する価値 | 自宅や職場の近くの chocoZAP 店舗の場所や導入マシン・サービス設備 (セルフエステ、脱毛、ランドリー等) を確認し、入会の判断につなげられる |
| 想定する利用者 | chocoZAP への入会を検討している一般利用者、および外出先・出張先で使える店舗を探す既存会員 |
| 商用か非商用か | 商用 (月額会員制コンビニジムの集客・入会導線および既存会員向けの店舗案内として提供。検索ページの利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。RIZAPグループ (2026年3月期連結売上収益 約1,672億円) の主力事業である chocoZAP の新規入会および利用継続に貢献 |
| 運営 | 企業 (RIZAP株式会社 / RIZAPグループ株式会社) |
| 推定の運用費 | 推測: 月数十万円。Amazon S3 + CloudFront による静的ホスティング費に加え、1,800 店舗以上を展開するサイトでの Google Maps JavaScript API の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`https://maps.googleapis.com/maps/api/js?key=...&callback=initMap`) |
| フレームワーク | Nuxt (`/_nuxt/SK_xAtQN.js`、静的プリレンダリングと `_payload.json` の構成) |
| 背景の地図とタイル | Google マップ (Google Maps JavaScript API 経由で取得) |
| 投稿やデータの保存先 | 静的生成された `_payload.json` (`/studios/search/area/_payload.json`) および自社店舗情報基盤 |
| 配信 | Amazon S3 + Amazon CloudFront (`server: AmazonS3`、`via: ...cloudfront.net`、`x-cache: Hit from cloudfront`) |

メモ:

- `/studios/search/area` は `AmazonS3` と `CloudFront` から配信される Nuxt の静的生成ページで、ページ内に Google Maps JavaScript API のスクリプトを読み込んでいる

データの出どころ (2026-11-17):

- 店舗データ: RIZAP株式会社自社管理の chocoZAP 店舗情報
- 背景地図: Google (Google Maps Platform)
