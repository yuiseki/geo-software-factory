---
financial: commercial
organization: corp-ent
first_seen: 2019-10-16
first_seen_by: wayback
---

# AOKI 店舗検索

- URL: https://www.aoki-style.com/shop/storeTop
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、スーツ、紳士服、AOKI、アオキ、ORIHICA、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の AOKI 店舗を都道府県やフリーワード・条件から検索し、店舗情報やアクセスを確認できる公式通販内店舗検索ページ |
| 提供する価値 | AOKI 公式通販サイトと同一ドメイン上で最寄り店舗を探し、店舗の営業時間や店舗受取・在庫関連の導線を確認できる |
| 想定する利用者 | ビジネススーツやフォーマルウェア、ビジネスカジュアルの購入で AOKI 店舗へ来店する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客および公式通販サイトとのオムニチャネル連携として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗売上および EC 送客に貢献する集客基盤 |
| 運営 | 企業 (株式会社AOKI / 株式会社AOKIホールディングス) |
| 推定の運用費 | 推測: 月数万〜数十万円。EC 統合基盤と Amazon CloudFront の運用費、Google Maps 関連の利用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (参考の事前調査による。一次 HTTP 取得の `/shop/storeTop` および `/shop/storeList` では地図描画スクリプトを直接確認できず) |
| フレームワーク | jQuery 3.3.1 (`jquery-3.3.1.min.js`)、jQuery UI、Bootstrap、独自 EC 基盤 (`martha_app.js`、`vue_extract.css`) |
| 背景の地図とタイル | Google Maps (参考の事前調査による。一次 HTTP 取得では詳細未確認) |
| 投稿やデータの保存先 | 自社 EC 統合基盤 (`www.aoki-style.com/shop/storeList`) |
| 配信 | nginx + Amazon CloudFront (`server: nginx`、`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 観測では、`HEAD` 要求に対して HTTP/2 404 を返す一方、`GET` 要求では HTTP/2 200 を返す挙動を確認した
- 店舗検索が独立したサブドメインではなく、EC サイト (`/shop/storeTop`) 内の機能として統合されている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社AOKI 自社管理の店舗情報
- 背景地図: Google Maps (参考の事前調査による)
