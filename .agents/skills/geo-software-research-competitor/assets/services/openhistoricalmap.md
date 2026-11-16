# OpenHistoricalMap

- URL: https://www.openhistoricalmap.org/
- ソース: https://github.com/OpenHistoricalMap (openstreetmap-website や iD エディタのフォーク `ohm-editor`、スタイル定義 `map-styles` 等を公開)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: OpenHistoricalMap、OHM、歴史地図、古地図、時系列地図、OpenStreetMap、タイムスライダー、歴史地理、ベクトルタイル

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | OpenStreetMap の仕組みを拡張し、過去のあらゆる時代における国境や都市や道路や建物の変遷をタイムスライダーで辿れる共同編集型の世界歴史地図 |
| 提供する価値 | 時代ごとの地理情報の変化を単一の空間データベースに記録し、任意の年代を指定して当時の地図をベクトルタイルで表示・再利用 (CC0 等) できる |
| 想定する利用者 | 歴史研究者、教育関係者、郷土史家、OpenStreetMap の編集経験者、歴史的な地図をアプリや教材に組み込みたい開発者 |
| 商用か非商用か | 非商用 (OpenStreetMap US の公式チャータープロジェクトとして運営される非営利のオープンソース・オープンデータプロジェクト) |
| 推定の売上 | 未確認 (商用サービスではなく売上はない。OpenStreetMap US を財政スポンサーとし、寄付や助成金、ボランティアや支援企業の開発協力で維持されている) |
| 運営 | 非営利団体 (OpenStreetMap US のチャータープロジェクト。Development Seed や GreenInfo Network 等が技術・運営を支援) |
| 推定の運用費 | 未確認 (時代フィルタ対応のベクトルタイル生成サーバーや OSM フォークの Rails サーバーを運用しているが、単体の運用費は公表されていない) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet と MapLibre GL JS (HTML 内で `leaflet` と `maplibre` の両方のキーワードを確認。時間フィルタ対応ベクトルタイルの表示に MapLibre GL JS を活用) |
| フレームワーク | Ruby on Rails + Hotwire Turbo (応答ヘッダーの `x-powered-by: Phusion Passenger(R) 6.1.3` および HTML 内の `turbo-*.js` を確認) |
| 背景の地図とタイル | OpenHistoricalMap 自前の時系列ベクトルタイル (`vtiles.openhistoricalmap.org`) |
| 投稿やデータの保存先 | 自前の PostgreSQL + PostGIS データベース (OSM データベースを開始日・終了日等の時間属性対応に拡張したもの) |
| 配信 | Cloudflare + Phusion Passenger (`server: cloudflare`、`cf-ray` ヘッダーを確認) |

メモ:

- 全時代分の静的ラスタタイルを事前生成するのではなく、ベクトルタイルとクライアント側の日付フィルタリングによって時系列表示を実現している。
- 地図データは原則として CC0 (パブリックドメイン) で公開されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 歴史地図データ | OpenHistoricalMap contributors (CC0) | https://www.openhistoricalmap.org/ |
| ソフトウェア基盤 | OpenStreetMap ソフトウェアのフォークおよび OpenHistoricalMap 開発コミュニティ | https://github.com/OpenHistoricalMap |
