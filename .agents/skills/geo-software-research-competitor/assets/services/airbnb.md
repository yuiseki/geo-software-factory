# Airbnb

- URL: https://www.airbnb.jp/ (グローバル: https://www.airbnb.com/)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Airbnb、エアビーアンドビー、民泊、バケーションレンタル、価格ピン地図、マップ検索、Mapbox、Google Maps、React

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中の個人宅、別荘、ユニークな宿泊施設、および体験アクティビティを地図と料金ピンで探して予約できるマーケットプレイス |
| 提供する価値 | 地図のパンやズームに連動して価格ピン付きの物件候補を即座に絞り込み、地域の雰囲気や詳細な立地情報をもとに宿を予約できる |
| 想定する利用者 | 世界中の旅行者・長期滞在者 (ゲスト) および空き部屋や宿泊施設を提供するホスト |
| 商用か非商用か | 商用 (ゲストおよびホスト双方からの予約サービス手数料) |
| 推定の売上 | 約 122.4 億米ドル (Airbnb, Inc. 2025 年通期売上高。2024 年は約 111.0 億米ドル) |
| 運営 | 企業 (Airbnb, Inc.、米国サンフランシスコ拠点、NASDAQ 上場) |
| 推定の運用費 | 未確認 (グローバル規模の検索・地図ランキング基盤、Google Maps および Mapbox 等の利用料、決済・信頼安全基盤の運用費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | ウェブ、iOS と Android のアプリ |
| 描画 | Google Maps JavaScript API と Mapbox の併用 (`https://www.airbnb.jp/` の HTML 内に `https://maps.googleapis.com/maps/api/js?language=ja&region=JP&v=3.36&libraries=places` と `https://a0.muscache.com/airbnb/static/client/packages/mapbox.bundle-ab2d6196.js` および `mapbox-*.css` の両方を観測) |
| フレームワーク | React、Next.js (HTML 内に `React`、`NEXT` 関連の記述、および自社公式テックブログで React / サーバー駆動 UI の採用を公開) |
| 背景の地図とタイル | Google Maps および Mapbox / OpenStreetMap ベース (地域や用途・フォールバックに応じて両プロバイダーを切り替えられる構成) |
| 投稿やデータの保存先 | 未確認 (自社クラウド基盤上と推測されるが公開 HTML からは特定できず) |
| 配信 | Envoy プロキシおよび自社 CDN ドメイン `a0.muscache.com` (`server: envoy`、`x-airbnb-internal-trace-id` ヘッダーを観測) |

メモ:

- トップページの初期 HTML データ内に、`maps.googleapis.com` (Google Maps JS API、Places ライブラリ含む) と `mapbox.bundle-*.js` (`airbnb_open_street_map_css_url` と命名された Mapbox 用 CSS) の双方が定義されていることを観測した。
- Airbnb Engineering Tech Blog では、中国など Google Play Services 非対応環境や地域ごとの要件に応じて地図プロバイダーを抽象化・切り替える `AirMapView` や、地図の移動操作に合わせた検索ランキングの最適化、地図バンドルの遅延読み込み (`scheduleAsyncLoad()`) などの技術知見が公開されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 地図ライブラリ・プロキシ・アセット配信 | Google Maps JS API、Mapbox バンドル、Envoy、`a0.muscache.com` | `https://www.airbnb.jp/` の HTTP 応答ヘッダーおよび HTML (2026-11-16 観測) |
| 地図抽象化・検索ランキング技術 | Airbnb Engineering & Data Science | Airbnb 公式テックブログ (`airbnb.tech`) |
| 売上高 | Airbnb, Inc. 2024 年・2025 年通期決算 | Airbnb IR および市場データ |
