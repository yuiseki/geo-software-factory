# OpenRouteService

- URL: https://openrouteservice.org
- ソース: https://github.com/GIScience/openrouteservice (LGPL-3.0 / ウェブUI `ors-map-client` は Apache-2.0)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: OpenRouteService、ORS、HeiGIT、ルート検索、等時間圏、アイソクロン、標高、車椅子ルート、OpenStreetMap、Leaflet

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | OpenStreetMap を基盤に、自動車・自転車・徒歩・車椅子など多彩な移動手段の経路探索や到達圏（アイソクロン）解析を提供するオープンソースのルーティングサービス |
| 提供する価値 | 到達圏分析や時間距離行列、坂道を考慮したルート検索、災害時の迂回経路探索を、公開 API またはセルフホストで柔軟に利用できる |
| 想定する利用者 | 人道支援・災害対応組織、交通・都市計画の研究者、GIS 開発者、アプリ開発者、一般のルート検索利用者 |
| 商用か非商用か | 非商用 (ドイツの研究機関 HeiGIT が運営。アカウント登録で日次制限付きの無料公開 API を提供し、人道・学術向け Collaborative プランやセルフホストにも対応) |
| 推定の売上 | なし (非営利研究機関による運営。助成金・研究資金・パートナー支援で維持) |
| 運営 | 研究機関・非営利組織 (HeiGIT / Heidelberg Institute for Geoinformation Technology、ドイツ) |
| 推定の運用費 | 推測: 月数十万〜数百万円規模。全世界の OSM 道路グラフと標高データを処理し、公開 API (`api.heigit.org` 等) とウェブ地図クライアントを維持している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (および Mapbox GL 互換) (`heigit.org/smart-mobility/` へのリダイレクト先で `leaflet.js`・`mapbox-gl.js`・`leaflet-mapbox-gl.js` を確認。公式クライアント `ors-map-client` は Vue2Leaflet / Leaflet を使用) |
| フレームワーク | ポータル (`heigit.org`) は WordPress + Elementor (`PHP/8.3.36` 確認)。地図アプリ (`maps.openrouteservice.org`) は Vue.js + Vuetify |
| 背景の地図とタイル | OpenStreetMap ベースの背景タイル |
| 投稿やデータの保存先 | 自前ルーティンググラフ (Java 製バックエンドで OSM と標高データから構築) |
| 配信 | Apache/2.4.69 (Debian) (`server: Apache/2.4.69 (Debian)`、`x-powered-by: PHP/8.3.36` を確認。`openrouteservice.org` は `heigit.org/smart-mobility/` へリダイレクト) |

メモ:

- 公式の単体 iOS / Android アプリはなく、ウェブアプリおよび API として提供されている（モバイルアプリへは API 連携またはセルフホストで組み込む）。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 道路ネットワーク・属性 | OpenStreetMap contributors (ODbL) | 公式サイト・API 利用規約 |
| 標高データ | SRTM 等のオープン標高データ | 公式ドキュメント |
