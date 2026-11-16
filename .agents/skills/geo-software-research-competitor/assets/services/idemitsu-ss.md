# 出光 (apollostation) SS検索サービス

- URL: https://map.idemitsu.com/b/a/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ガソリンスタンド、SS検索、出光、apollostation、アポロステーション、給油、EV充電、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の apollostation (出光興産系サービスステーション) を地図・現在地・取扱サービス条件から検索できる公式 SS 検索サイト |
| 提供する価値 | 24 時間営業、セルフ給油、洗車、車検、EV 充電、利用可能な決済手段など細かな条件で最寄りの SS を絞り込み、地図上で位置を確認できる |
| 想定する利用者 | 出光 / apollostation で給油・洗車・EV 充電・メンテナンスを行いたいドライバー、法人カード利用者 |
| 商用か非商用か | 商用 (全国の特約店・販売店 SS への送客基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 検索サイト単体の売上は 0 円。全国約 5,900 ヵ所の SS における燃料販売やカーケア事業の売上に貢献 |
| 運営 | 企業 (出光興産株式会社) |
| 推定の運用費 | 推測: 月数十万〜百数十万円。ONE COMPATH (旧 Mapion) の法人向け店舗検索 ASP (`SpotSearch`) 利用料と Amazon CloudFront 配信費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet + ONE COMPATH (旧 Mapion) 店舗検索基盤 (`/f/a/dist/js/base.js` 内に Leaflet、`lbs.mapion.co.jp/jslibs/JSPack.2.1.0.js` を確認) |
| フレームワーク | jQuery 3.6.0 (`jquery-3.6.0.min.js`)、ONE COMPATH `SpotSearch.js` (`common-ss2.0` / `ss5_5`) |
| 背景の地図とタイル | ONE COMPATH (Mapion) 地図タイル (`lbs.mapion.co.jp`) |
| 投稿やデータの保存先 | ONE COMPATH (旧 Mapion) のクラウド店舗検索基盤 (`SpotSearch.js` 経由の API) |
| 配信 | nginx + Amazon CloudFront (`server: nginx`、`via: 1.1 ...cloudfront.net (CloudFront)`、`x-amz-cf-pop: NRT57-P6`) |

メモ:

- `/b/a/` の URL パスおよび `/f/common-ss/common-ss2.0/js/client_js/SpotSearch.js` 構成は、株式会社 ONE COMPATH (旧マピオン) が提供するクラウド型店舗検索サービスの特徴的な構成である
- `proj4.js` も読み込んでおり、座標変換や最寄り検索 (`closest.js`) をフロントエンド側でも補助している

データの出どころ (2026-11-17):

- SS データ: 出光興産株式会社管理のサービスステーション情報
- 背景地図・店舗検索基盤: 株式会社 ONE COMPATH (Mapion 地図)
