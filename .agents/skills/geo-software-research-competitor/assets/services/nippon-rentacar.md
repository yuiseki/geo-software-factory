# ニッポンレンタカー 店舗検索

- URL: https://www.nipponrentacar.co.jp/shop/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、レンタカー、ニッポンレンタカー、マピオン、mapionbiz、Google Maps、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国約 850 箇所のニッポンレンタカー営業所を地域・駅・空港から検索し、店舗位置や営業時間を地図付きで確認できる公式店舗検索ページ |
| 提供する価値 | 出発地の駅や空港から近い営業所の位置・アクセス・営業時間を地図上で比較でき、そのままレンタカー予約へ進める |
| 想定する利用者 | 旅行・出張・引っ越し等でレンタカーを利用したい個人および法人顧客 |
| 商用か非商用か | 商用 (全国営業所への予約送客基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。ニッポンレンタカーサービス株式会社の売上高は 426 億 2,000 万円 (2025 年 12 月期) |
| 運営 | 企業 (ニッポンレンタカーサービス株式会社 / 東京センチュリーグループ) |
| 推定の運用費 | 推測: 月数十万円。Web 基盤・サイト内検索 (MARSFLAG) の運用費に加え、Google Maps API および法人向け地図 ASP (マピオン mapionbiz) の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`maps.googleapis.com/maps/api/js?callback=initMap` および `google.com/maps/embed` をエリア別店舗ページ `/shop/area/hokkaido/sapporo.html` 等で確認。事前調査ではマピオン `mapionbiz` 経由の構成も確認) |
| フレームワーク | jQuery 1.11.1 / 3.3.1 + MARSFLAG サイト内検索 (`mf-search.js`) |
| 背景の地図とタイル | Google Maps (Maps JavaScript API および埋め込み iframe を確認。事前調査ではマピオン mapionbiz 連携あり) |
| 投稿やデータの保存先 | ニッポンレンタカー自社店舗基盤 (静的 HTML および地域別店舗ページ群で構成) |
| 配信 | 未確認 (HTTP/2 200 応答、`server` ヘッダ非公開) |

メモ:

- トップの店舗検索 (`/shop/`) は地域・都道府県一覧の案内ページとなっており、地域別店舗ページ (例: `/shop/area/hokkaido/sapporo.html`) 内に Google Maps JavaScript API (`initMap`) および各営業所の Google Maps 埋め込み iframe が配置されている。

データの出どころ (2026-11-17):

- 店舗検索・技術構成: `https://www.nipponrentacar.co.jp/shop/` および `https://www.nipponrentacar.co.jp/shop/area/hokkaido/sapporo.html` の HTTP 応答ヘッダ・HTML/JS (2026-11-17 観測)
- 背景地図: Google (Google Maps Platform)、および事前調査による株式会社ワン・コンパス (マピオン mapionbiz) 情報
- 運営・業績情報: ニッポンレンタカーサービス株式会社 公開決算情報 (2025 年 12 月期)
