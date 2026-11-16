# iOverlander

- URL: https://ioverlander.com
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: iOverlander、オーバーランド、車中泊、キャンプ場、野営、バンライフ、オフライン地図、MapLibre、OpenStreetMap

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中のオーバーランダーや車中泊旅行者が野営地・キャンプ場・給水・Wi-Fi・修理工場などの実用スポットを投稿し合い、地図から探せるコミュニティデータベース |
| 提供する価値 | 通常の観光地図には載らない未舗装路奥の野営適地や給水・プロパンガス補充などの生活インフラ情報を、最新の利用者レビューや設備アイコンとともにオフライン環境でも参照できる |
| 想定する利用者 | 長期陸路旅をするオーバーランダー、キャンピングカー・バンライフ旅行者、バイクツーリング愛好家 |
| 商用か非商用か | 商用 (フリーミアム。無料版は地域制限・広告あり。iOverlander 2 以降、Pro 年額約 $59.99、Unlimited 年額約 $99.99 の有料サブスクリプションを導入。草の根コミュニティ発だが法人形態は LLC) |
| 推定の売上 | 未確認 (非公開企業。推測: 年数千万円〜数億円規模) |
| 運営 | 企業 (iOverlander, LLC、米国) |
| 推定の運用費 | 推測: 月数十万〜数百万円規模。自前タイル配信 (`tile2.ioverlander.com`)、MapTiler ジオコーディング API、世界規模のスポット・写真 DB の運用 |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS (Ruby on Rails のバンドル JS `/assets/application-*.js` 内に `maplibre` の実装を確認。HTML 内には `leaflet`・`deck.gl` の文字列も確認) |
| フレームワーク | Ruby on Rails + Hotwire (Turbo) + React (`application-*.js` 内に `rails`, `turbo`, `react` を確認) |
| 背景の地図とタイル | 自前配信の OpenStreetMap ベーススタイル (`https://tile2.ioverlander.com/styles/openstreetmap/style.json` を JS 内で確認) および MapTiler ジオコーディング (`https://api.maptiler.com/geocoding/legacy/q/`) |
| 投稿やデータの保存先 | iOverlander 自社基盤 (Ruby on Rails バックエンドによるスポット座標・カテゴリ・レビュー・写真データ) |
| 配信 | Cloudflare (`server: cloudflare` を確認。Cloudflare Turnstile を利用) |

メモ:

- `https://ioverlander.com` のバンドル JS を直接解析し、`MapLibre` と自前タイルエンドポイント `tile2.ioverlander.com`、および MapTiler のジオコーディング API の利用を観測した。
- ウェブ版のほか iOS / Android アプリ (iOverlander / iOverlander 2) も提供されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 野営地・給水・修理工場等のスポット | 旅行者コミュニティによる投稿・更新レビュー | iOverlander 公式サイト・アプリ |
| 背景地図タイル | OpenStreetMap (自前タイルサーバー `tile2.ioverlander.com` 経由) | `application-*.js` 内のスタイル URL |
| ジオコーディング | MapTiler | `application-*.js` 内の API URL |
