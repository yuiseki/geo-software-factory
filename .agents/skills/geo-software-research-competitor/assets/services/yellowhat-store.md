---
financial: commercial
organization: corp-ent
---

# イエローハット 店舗検索

- URL: https://www.yellowhat.jp/yellowhat/store
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、カー用品、イエローハット、ピット作業、車検、オイル交換、タイヤ交換、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のイエローハット店舗を都道府県・現在地・キーワードや取扱サービスから検索し、Google Maps 上に表示する公式店舗検索サイト |
| 提供する価値 | 近くの店舗の位置や営業時間・ピットメニュー対応状況を確認し、そのまま作業予約や店舗詳細確認へ進める |
| 想定する利用者 | カー用品の購入やタイヤ交換・オイル交換・車検などの整備を希望する自動車保有者・ドライバー |
| 商用か非商用か | 商用 (直営・フランチャイズを含む実店舗への来店・作業予約の送客基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。グループ国内約 765 店舗の商品販売およびピット整備・車検事業の売上向上に貢献 |
| 運営 | 企業 (株式会社イエローハット) |
| 推定の運用費 | 推測: 月数十万円。Google Maps Platform (Maps JavaScript API / Places API) の従量課金と Amazon CloudFront の配信費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`maps.googleapis.com/maps/api/js?libraries=places,marker&loading=async`) |
| フレームワーク | jQuery 3.4.1 (`jquery-3.4.1.min.js`)、jQuery Japan Map (`jquery-cf9b056175.japan-map.js`) |
| 背景の地図とタイル | Google マップ (Google Maps Platform) |
| 投稿やデータの保存先 | 自社店舗検索基盤 (店舗情報はサーバー側の HTML および設定 JS 経由で取得) |
| 配信 | Amazon CloudFront (`via: 1.1 ...cloudfront.net (CloudFront)`、`x-amz-cf-pop: NRT20-P3`) |

メモ:

- トップ画面に都道府県選択用の日本地図 UI (`jquery-cf9b056175.japan-map.js`) と検索フォームを備え、地図描画には Google Maps Platform の `places` および `marker` ライブラリを読み込んでいる

データの出どころ (2026-11-17):

- 店舗データ: 株式会社イエローハット自社管理の店舗情報
- 背景地図・場所検索: Google (Google Maps Platform)
