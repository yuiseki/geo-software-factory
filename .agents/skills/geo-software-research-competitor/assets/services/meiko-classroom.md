# 明光義塾 教室検索

- URL: https://www.meikogijuku.jp/school/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、教室検索、学習塾、個別指導、明光義塾、塾、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の明光義塾教室を都道府県・市区町村やキーワードから検索し、教室ごとの詳細や問い合わせ導線を確認できる公式教室検索ページ |
| 提供する価値 | 自宅や学校近くの明光義塾教室を探し、所在地やアクセス・教室情報を確認して無料体験授業や資料請求を申し込める |
| 想定する利用者 | 小学生・中学生・高校生の通塾先を探している保護者および生徒本人 |
| 商用か非商用か | 商用 (体験授業・教室見学・入会問い合わせの獲得のために提供。利用料は無料) |
| 推定の売上 | 推測: 教室検索単体の売上は 0 円。直営およびフランチャイズ教室の生徒募集に貢献する主要集客基盤 |
| 運営 | 企業 (株式会社明光ネットワークジャパン) |
| 推定の運用費 | 推測: 月数万〜数十万円。Drupal を用いた自社 CMS 運用費および Google Maps JavaScript API の利用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (`maps.googleapis.com/maps/api/js?key=...&callback=onLoadMap` の読込を `/school/` および市区町村一覧で確認) |
| フレームワーク | Drupal (`/sites/default/files/js/...`、`/core/assets/vendor/jquery/jquery.min.js?v=4.0.0`)、jQuery 3.6.0、Slick Carousel |
| 背景の地図とタイル | Google Maps (Maps JavaScript API) |
| 投稿やデータの保存先 | 自社 CMS 基盤 (Drupal、`www.meikogijuku.jp/school/`) |
| 配信 | Apache (`server: Apache`) |

メモ:

- 参考の事前調査では「埋め込み地図なし（Googleマップへのリンク）」とされていたが、2026-11-17 の一次 HTTP 観測では `/school/` および `/school/tokyo/akishima-shi/` 双方の HTML で `maps.googleapis.com/maps/api/js` と `onLoadMap` の読込を確認した
- バックエンド CMS として Drupal (`/core/assets/vendor/...`、`/sites/default/files/...`) が稼働している

データの出どころ (2026-11-17):

- 店舗データ: 株式会社明光ネットワークジャパン自社管理の教室情報
- 背景地図: Google Maps
