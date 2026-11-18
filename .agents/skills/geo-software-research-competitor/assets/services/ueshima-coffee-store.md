---
financial: commercial
organization: corp-ent
---

# 上島珈琲店 (UFS) 店舗検索

- URL: https://shop.ufs.co.jp/ufs/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、カフェ、上島珈琲店、UCC、ユーシーシーフードサービスシステムズ、NAVITIME、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 上島珈琲店をはじめとする UCC フードサービスシステムズ各業態の店舗をエリア・キーワード・条件から検索できる公式店舗検索サイト |
| 提供する価値 | ブランドやエリア、禁煙・喫煙、Wi-Fi などの条件で上島珈琲店や UCC カフェプラザ等を横断検索し、地図や最寄駅案内を確認できる |
| 想定する利用者 | 上島珈琲店など UCC グループのカフェを利用したい一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する送客チャネル |
| 運営 | 企業 (ユーシーシーフードサービスシステムズ株式会社。店舗検索・地図基盤は株式会社ナビタイムジャパンの NAVITIME Location Cloud を利用) |
| 推定の運用費 | 推測: 月十万〜数十万円。NAVITIME Location Cloud (法人向け店舗検索 ASP) の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME Location Cloud による店舗検索・地図描画 (`navitime.co.jp` アセットおよび NAVITIME 店舗検索 ASP テンプレート) |
| フレームワーク | jQuery 3.7.1、`iframeResizer` (ヘッダ・フッタを `image.pkg.navitime.co.jp/citrus/180/html/` から読み込み) |
| 背景の地図とタイル | NAVITIME の地図データ・タイル |
| 投稿やデータの保存先 | NAVITIME Location Cloud 側で管理された UFS 店舗情報データ (`citrus/180/`) |
| 配信 | Apache (`server: Apache`) |

メモ:

- 上島珈琲店は国内に約 90〜110 店舗以上を展開している
- フッタやリンクに `navitime.co.jp/?frm=pwd&utm_source=ufs&utm_medium=banner&utm_campaign=store_locator` のクレジット表記がある

データの出どころ (2026-11-17):

- 店舗データ: ユーシーシーフードサービスシステムズ株式会社
- 店舗検索基盤・背景地図: 株式会社ナビタイムジャパン (NAVITIME Location Cloud)
