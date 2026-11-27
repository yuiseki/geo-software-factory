---
financial: commercial
organization: corp-ent
first_seen: 2004-10-23
first_seen_by: wayback
---

# アート引越センター 引越ネットワーク

- URL: https://www.the0123.com/company/network.html
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、拠点検索、支社一覧、引越、引っ越し、アート引越センター、0123、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のアート引越センターの支店・センターやグループ会社の所在地と管轄エリアを確認できる公式拠点一覧ページ |
| 提供する価値 | 引越し予定地域に対応する支店やグループ拠点を地方別に探し、企業情報や連絡先の確認ができる |
| 想定する利用者 | アート引越センターの利用を検討している個人・法人顧客、および取引先・採用応募者 |
| 商用か非商用か | 商用 (企業案内および引越サービスへの信頼感醸成・問い合わせ導線として提供。利用料は無料) |
| 推定の売上 | 推測: 拠点検索単体の売上は 0 円。引越受注および見積もり問い合わせに貢献する公式企業情報の一部 |
| 運営 | 企業 (アート引越センター株式会社) |
| 推定の運用費 | 推測: 月数万円程度。Apache + Amazon CloudFront による配信費および地図関連の利用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (参考の事前調査による。一次 HTTP 取得の `/company/network.html` 本文中では地図埋め込みスクリプトを直接確認できず) |
| フレームワーク | jQuery 3.5.1 (`jquery.min.js`)、Swiper 8 (`swiper-bundle.min.js`)、AMP 関連スクリプト (`cdn.ampproject.org/v0.js`) |
| 背景の地図とタイル | Google Maps (参考の事前調査による。一次 HTTP 取得では詳細未確認) |
| 投稿やデータの保存先 | 自社 Web 基盤 (`www.the0123.com/company/network.html`) |
| 配信 | Apache + Amazon CloudFront (`server: Apache`、`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 観測 (`/company/network.html`) では `HTTP/2 200`、Apache + CloudFront 配信を確認した
- 同一ページ上に北海道から九州までの拠点一覧が配置されており、地図表示は参考の事前調査では Google Maps とされているが一次取得 HTML からは直接確認できなかった

データの出どころ (2026-11-17):

- 店舗データ: アート引越センター株式会社自社管理の拠点情報
- 背景地図: Google Maps (参考の事前調査による)
