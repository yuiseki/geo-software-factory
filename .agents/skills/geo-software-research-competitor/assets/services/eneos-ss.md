---
financial: commercial
organization: corp-ent
first_seen: 2010-07-09
first_seen_by: wayback
---

# ENEOS サービスステーション検索

- URL: https://eneos-ss.com/search/ss/pc/top.php
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ストアロケーター、店舗検索、ガソリンスタンド、SS検索、ENEOS、エネオス、24時間営業、洗車、EV充電、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の ENEOS サービスステーション (SS) を、現在地・エリア・24 時間営業・洗車・EV 充電などの設備条件から検索して地図上に表示する公式検索サイト |
| 提供する価値 | 走行中や旅行先で条件に合う最寄りのガソリンスタンドや EV 充電拠点、営業時間、取り扱いサービス (セルフ給油、車検、EneKey 対応等) を素早く見つけられる |
| 想定する利用者 | 給油や洗車、車検、EV 充電を行いたい一般ドライバーおよび法人車両の利用者 |
| 商用か非商用か | 商用 (全国の ENEOS 系列 SS への送客および燃料・カーメンテナンス利用促進のために提供。利用料は無料) |
| 推定の売上 | 推測: 検索サイト単体の売上は 0 円。系列 SS での給油・カーメンテナンス・EV 充電売上への送客基盤 |
| 運営 | 企業 (ENEOS株式会社) |
| 推定の運用費 | 推測: 月数十万円。ジオテクノロジーズ (GeoTechnologies / 旧インクリメントP) の MapFan 法人向け地図・検索基盤利用料およびサーバー運用費がかかる |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapFan / GeoTechnologies 地図基盤 (ブラウザ観測で「©INCREMENT P」表記および MapFan 系地図を確認) |
| フレームワーク | jQuery 3.3.1 + 従来型 JS (`prottype.lite.js`、`moo.fx.js` 等) |
| 背景の地図とタイル | MapFan / GeoTechnologies (©INCREMENT P) の地図データ・タイル |
| 投稿やデータの保存先 | SS 検索システム (PHP ベースのサーバーサイド `/search/ss/pc/top.php`、API 詳細は未確認) |
| 配信 | Apache (`server: Apache`) |

メモ:

- 2026-11-16 のブラウザ観測で、地図基盤に MapFan / GeoTechnologies (©INCREMENT P) が採用されていることを確認した
- 一次 HTTP 取得 (`https://eneos-ss.com/search/ss/pc/top.php`) ではステータス 200、`server: Apache`、HTML タイトル「サービスステーション検索｜ＥＮＥＯＳ」を確認した
- 公式スマートフォンアプリとして「ENEOS公式アプリ」が提供されている

データの出どころ (2026-11-16):

- 店舗データ: ENEOS株式会社自社管理のサービスステーション情報
- 背景地図・タイル: ジオテクノロジーズ株式会社 (MapFan / ©INCREMENT P)
