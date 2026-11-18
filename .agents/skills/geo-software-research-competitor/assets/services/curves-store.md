---
financial: commercial
organization: corp-ent
---

# カーブス (Curves) 店舗一覧・店舗検索

- URL: https://www.curves.co.jp/search/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、カーブス、Curves、女性専用フィットネス、体操教室、筋トレ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国 2,000 店舗以上の女性専用フィットネス「カーブス」を都道府県・市区町村から検索し、各店舗のアクセスや体験予約へ進める公式店舗検索ページ |
| 提供する価値 | 身近な駅や生活圏にあるカーブス店舗を探し、店舗ごとのアクセス案内図 (静止地図画像) や Google マップで場所を確かめて無料体験に申し込める |
| 想定する利用者 | 運動習慣をつけたい女性 (特に中高年層を中心とする一般利用者) で、自宅近くの店舗を探している人 |
| 商用か非商用か | 商用 (女性専用フィットネスの無料体験予約・入会導線として提供。検索ページの利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。株式会社カーブスホールディングス (2025年8月期連結売上高 376億円、国内カーブス約2,013店舗) の新規会員獲得に貢献 |
| 運営 | 企業 (株式会社カーブスジャパン / 株式会社カーブスホールディングス) |
| 推定の運用費 | 推測: 月数万〜数十万円。nginx による Web 配信費と、店舗詳細ページにおける Google Maps Embed API および Google Maps JavaScript API (ジオコーディング・地図連携) の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | トップ (`/search/`) には埋め込み地図なし。個別店舗ページ (例: `/search/hokkaido/hokkaido/cat-1/90514.php`) では自社制作の静止地図画像 (`/search/images/map/<id>.jpg`) と Google マップ埋め込み (`google.com/maps/embed/v1/place`)・Google Maps JavaScript API (`maps.googleapis.com/maps/api/js?key=...&callback=initLatLng`) を併用 |
| フレームワーク | jQuery 3.4.1 (`jquery-3.4.1.min.js`、地図画像マップ用に `imageMapResizer.min.js` と `search2105.js`) |
| 背景の地図とタイル | 自社製静止地図画像 + Google マップ (Embed API / Maps JavaScript API) |
| 投稿やデータの保存先 | サーバー側で生成された PHP ページ (`/search/<area>/<pref>/<cat>/<id>.php`) |
| 配信 | nginx (`server: nginx`) |

メモ:

- トップの `/search/` には地図が埋め込まれておらず都道府県・エリア選択のみだが、個別店舗ページでは分かりやすい自社製の静止地図画像と Google マップ埋め込み・Google マップリンクの両方を切り替えて確認できる作りになっている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社カーブスジャパン自社管理の店舗情報
- 背景地図: 自社製静止地図画像および Google (Google Maps Platform)
