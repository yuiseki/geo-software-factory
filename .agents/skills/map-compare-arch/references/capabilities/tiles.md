# タイル配信

対象: ベースマップと主題図のベクトルタイル、ラスタタイル、地形タイル、3D Tiles

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |

## 3 つの型

この機能を実現する型は 3 つある: 外部の API (商用・公開のタイル API)、常駐するタイルサーバー (Martin、TileServer GL、t-rex など)、ファイルと関数 (PMTiles を静的ホスティングや CDN から配る、リクエスト時にタイルを計算する関数、ブラウザで PMTiles を直接読む)。

| 型 | 主なツール・サービス (版、ライセンス) | 保存の置き場所 | 計算の置き場所 | 表現 (応答の形式) | 出典 |
|---|---|---|---|---|---|
| 外部の API | 商用のタイル API (例: MapTiler、Stadia Maps、Mapbox、Google Map Tiles API。提供元ごとの条件は map-compare-infra で扱う)、公開のタイル (例: OpenStreetMap 財団の tile.openstreetmap.org、国土地理院の地理院タイル)。tile.openstreetmap.org は SLA が無く、大量利用とオフライン用の一括取得を禁じている | 提供元のクラウド | 提供元のクラウドと CDN | Z/X/Y の URL で返すベクトルタイル (MVT) かラスタ画像、スタイル JSON、TileJSON | https://operations.osmfoundation.org/policies/tiles/ |
| 常駐するサーバー | Martin martin-v1.16.1 (2026-09-10 JST、Apache-2.0 か MIT の選択)、TileServer GL v5.7.0 (2026-10-24 JST、BSD-2-Clause)、pg_tileserv v1.0.11 (2024-02-02 JST、Apache-2.0)、BBOX v0.6.2 (2024-11-15 JST、Apache-2.0 か MIT の選択)、t-rex v0.14.3 (2022-01-30 JST、MIT、保守終了で BBOX tile server に置き換え)、GeoServer 3.0.2 (2026-10-17 JST、GPL-2.0 以降) | サーバーの手元のファイル (MBTiles、PMTiles) か PostGIS。Martin は PMTiles を HTTP 越しにも読む | 常駐プロセス。Martin と pg_tileserv は PostGIS の表や関数からリクエスト時に MVT を作る。TileServer GL はベクトルタイルを MapLibre Native でラスタに描いて返せる | MVT、ラスタ画像 (PNG など)、TileJSON、スタイル JSON、スプライトとグリフ (Martin はその場で生成) | https://github.com/maplibre/martin 、https://github.com/maptiler/tileserver-gl 、https://github.com/CrunchyData/pg_tileserv 、https://github.com/bbox-services/bbox 、https://github.com/t-rex-tileserver/t-rex 、https://github.com/geoserver/geoserver/blob/main/LICENSE.md |
| ファイルと関数 | PMTiles (仕様 v3 は public domain か CC0、参照実装は BSD-3-Clause。npm の pmtiles 4.5.0、CLI の go-pmtiles v1.31.2 (2026-07-23 JST))。PMTiles をそのまま静的ホスティングから HTTP Range で読む、Cloudflare Workers + R2 か AWS Lambda + S3 + CloudFront の関数で Z/X/Y に変換して返す、Martin のように GeoParquet (DuckDB 経由、Martin は unstable と明記) からリクエスト時にタイルを作る | オブジェクトストレージか静的ホスティングに置いた 1 ファイル | 関数 (Workers、Lambda) か、ブラウザやアプリの中 | ブラウザ直読みでは PMTiles の範囲読み出し、関数経由では Z/X/Y の MVT かラスタと TileJSON | https://github.com/protomaps/PMTiles/blob/main/LICENSE 、https://docs.protomaps.com/deploy/ 、https://docs.protomaps.com/deploy/cloudflare 、https://docs.protomaps.com/deploy/aws 、https://github.com/maplibre/martin |

地形と 3D:

- 地形は raster-dem のタイルとして配る。MapLibre のスタイル仕様では raster-dem の encoding に terrarium、mapbox (既定)、custom の 3 つがある。PMTiles にラスタとして入れれば、上の 3 つの型のどれでも配れる。TileServer GL の設定例には S3 上の terrain.pmtiles を読む例がある。出典: https://maplibre.org/maplibre-style-spec/sources/ 、https://github.com/maptiler/tileserver-gl/blob/master/docs/config.rst
- 3D Tiles は OGC Community Standard で、1.0 は 2018-12-14 に承認、1.1 は glTF をタイルの中身として直接扱い、旧形式 (b3dm、i3dm、pnts、cmpt) を非推奨にした。tileset.json と glTF のファイル群なので静的ホスティングで配れる (推測: ファイル群をそのまま置けば常駐サーバーは要らない)。出典: https://github.com/CesiumGS/3d-tiles 、https://www.ogc.org/standards/3dtiles/

## 置き場所ごとの実現手段

| 置き場所 | 実現手段 (ツール、形式、API) | 制約 (データの大きさ、メモリ、起動時間、更新) | 出典 |
|---|---|---|---|
| クラウド | 常駐サーバー (Martin、TileServer GL、pg_tileserv、GeoServer) をコンテナや VM で動かす。または AWS Lambda + S3 + CloudFront で PMTiles を Z/X/Y に変換する (CloudFormation で一式を作る) | Lambda の応答は 6 MB まで。Protomaps の文書では適切に構成した AWS で p50 125 ms、p99 800 ms。キャッシュの一括削除をすると Lambda 実行と S3 読み出しがまた課金される。Lambda のメモリ上限は 10,240 MB | https://docs.protomaps.com/deploy/aws 、https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html |
| エッジ (CDN のエッジ関数、利用者の近くに置く小さなサーバー) | Cloudflare Workers + R2 で PMTiles を `/NAME/z/x/y.mvt` と `/NAME.json` (TileJSON) として返す。CDN のキャッシュが当たれば 100 ms 以下で返せると Protomaps の文書は書く | キャッシュを効かせるには workers.dev でなく自分のドメインに置く。既定の Cache-Control は 1 日。R2 は他のクラウドストレージより遅延が大きい (500 ms 以上) が、読み出しはキャッシュが外れたときだけ。Web UI からの upload は 300 MB まで。Workers のメモリは isolate あたり 128 MB (タイルを返すだけなら PMTiles 全体をメモリに載せないので効かない (推測)) | https://docs.protomaps.com/deploy/cloudflare 、https://docs.protomaps.com/deploy/ 、https://developers.cloudflare.com/workers/platform/limits/ |
| ブラウザ | npm の pmtiles の Protocol を MapLibre GL JS の addProtocol に登録し、`pmtiles://https://.../x.pmtiles` をソースにする。Leaflet、OpenLayers 用の実装もある。ブラウザは PMTiles の必要な範囲だけを HTTP Range で取る | 置き場所に CORS と Range 要求への対応が要る。Protomaps の比較では、静的な PMTiles を直接読む方式は Z/X/Y 互換もエッジのキャッシュも無く、遅延がもっとも大きい区分になる。単一リージョンのバケットは遠い利用者に数秒の遅延が出うる | https://github.com/protomaps/PMTiles/blob/main/js/README.md 、https://docs.protomaps.com/deploy/ |
| アプリ (ネイティブ、端末内) | MapLibre Native は `pmtiles://` を扱う (iOS 6.10.0、Android 11.8.0 で追加)。Android 13.7.1 では APK の assets に同梱した PMTiles を `pmtiles://asset://...` で読み、要求した範囲だけを読む。13.3.0 (Android) と 6.27.0 (iOS) で PMTiles ソースの ambient cache が入った | 端末の容量に収まる範囲とズームに絞る必要がある (下の大きさの目安を参照)。同梱すればアプリ配布の大きさに効く (推測) | https://github.com/maplibre/maplibre-native/blob/main/platform/android/CHANGELOG.md 、https://github.com/maplibre/maplibre-native/blob/main/platform/ios/CHANGELOG.md |

## データの大きさの目安

国、都道府県、市区町村の範囲で、索引やファイルがどれくらいの大きさになるか。公式の記述か、測った条件つきで書く。

- 全球 (OSM ベース、Protomaps basemap): 公式文書では z0〜15 でおよそ 120 GB、ズームを 1 段増やすごとにおよそ 2 倍になる。2026-11-10 に https://build.protomaps.com/20261109.pmtiles の Content-Length を測ると 139,407,008,771 バイト (約 139 GB、basemap version 4.15.2、z0〜15、OSM の差分は 2026-11-09 13:00 JST 時点) だった。出典: https://docs.protomaps.com/basemaps/downloads
- 日本 (上の全球ファイルから切り出し): `pmtiles extract --bbox=122.9,24.0,153.99,45.6 --dry-run` (go-pmtiles、2026-11-10 に測定) で z0〜15 が約 3.7 GB、`--maxzoom=12` を付けると約 405 MB。この範囲は海と近隣国の一部を含む
- 都県 (東京都の本土部分を矩形で近似、`--bbox=138.94,35.50,139.92,35.90`): 同じ方法で z0〜15 が約 175 MB
- 日本 (国土地理院の最適化ベクトルタイル、PMTiles 版、試験公開): https://cyberjapandata.gsi.go.jp/xyz/optimal_bvmap-v1/optimal_bvmap-v1.pmtiles の Content-Length は 16,900,763,181 バイト (約 16.9 GB、Last-Modified 2026-09-17 16:32 JST)。z4〜16 (z17 の情報は z16 に含めてオーバーズーム)、データ更新は 2026-07-01 時点。出典: https://github.com/gsi-cyberjapan/optimal_bvmap
- 単一データセットの例: 国土数値情報の行政区域 (2024 年) は GeoJSON 452 MB が PMTiles で 76 MB になった (ズーム範囲の記載なし)。出典: https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/tochi_fudousan_kensetsugyo_tk17_000001_00056.html

## 判断を左右すること

- 更新頻度: PMTiles は 1 ファイルを丸ごと作り直して差し替える方式で、Protomaps の basemap は日次でビルドが出ている (build.protomaps.com に日付名のファイルが並ぶ)。差し替え後は CDN のキャッシュを消す必要がある。Protomaps の手順は「Cloudflare の Purge Cache はゾーン全体に効く」として専用ゾーンを勧めているが、Cloudflare は Free プランでも URL、ホスト名、タグ、プレフィックスの単位で消せる。ゾーン全体に効くのは Purge Everything だけである (https://developers.cloudflare.com/cache/how-to/purge-cache/、2026-11-10 確認)。編集が頻繁なデータは PostGIS から都度タイルを作る Martin や pg_tileserv が合う (推測)。出典: https://docs.protomaps.com/deploy/cloudflare
- 応答の速さ: CDN のキャッシュが当たれば 100 ms 以下、AWS の関数経由で p50 125 ms と p99 800 ms、静的 PMTiles の直読みは最も遅い区分で、遠いリージョンだと数秒になりうる。出典: https://docs.protomaps.com/deploy/ 、https://docs.protomaps.com/deploy/aws
- オフラインで使いたいか: PMTiles を端末に置けば MapLibre Native で読める。tile.openstreetmap.org はオフライン利用と一括取得を禁じているので、オフラインには自前の PMTiles か、オフライン利用を許す提供元が要る。出典: https://operations.osmfoundation.org/policies/tiles/ 、https://github.com/maplibre/maplibre-native/blob/main/platform/android/CHANGELOG.md
- 費用 (外部 API の課金単位、自前の計算と転送): 外部 API は多くがタイル数か地図の読み込み回数で課金する (提供元ごとの単価は map-compare-infra で扱う)。Cloudflare Workers は月 5 ドルで 1,000 万リクエストを含み、超過は 100 万あたり 0.30 ドル。R2 は保存、書き込み、読み出しで課金され、読み出しはキャッシュが外れたときだけ起きる。AWS では CloudFront の invalidation は月 1,000 回まで無料。常駐サーバーは負荷が無くても動かし続ける費用がかかる (推測)。出典: https://docs.protomaps.com/deploy/cloudflare 、https://docs.protomaps.com/deploy/aws

## ライセンス上の注意

コピーレフトのツール (GPL、AGPL など) と、データの継承条件 (ODbL など) を、組み込み、改変、配布、SaaS 提供のそれぞれで書く。

- GeoServer (GPL-2.0 以降): 組み込み (自社製品に同梱して配る) と改変して配布する場合は、ソースを GPL で開示する義務が生じる。SaaS として外部に提供するだけなら GPL-2.0 は配布にあたらないので開示義務は生じない (AGPL でないため)。改変せずに別プロセスとして HTTP で使うだけなら自社コードには及ばない (推測: GPL の一般的な解釈で、個別事案は法務の確認が要る)。出典: https://github.com/geoserver/geoserver/blob/main/LICENSE.md
- Martin、TileServer GL、pg_tileserv、BBOX、t-rex、PMTiles の参照実装はいずれも寛容なライセンス (Apache-2.0、MIT、BSD) で、著作権表示とライセンス文を残せば組み込み、改変、配布、SaaS 提供ができる。TileServer GL の npm パッケージと Docker イメージには MapLibre GL Native が入る (同梱物のライセンスは別に確認する (推測))
- OSM 由来のタイル (Protomaps basemap など) は ODbL の Produced Work として配られ、OpenStreetMap の帰属表示が要る。ODbL の要約では、データベースやそこから作った作品を公に使うときは帰属表示が要り、改変したデータベースを公に使うならそのデータベースも ODbL で提供する (share-alike)。タイルを描いた画像 (ラスタ) は通常 Produced Work 側に入る。ベクトルタイルは地物の座標と属性をそのまま持ち、データを取り出せるので、データベースとみなされる余地がある (推測。Protomaps は planet ビルドを Produced Work として配っている。詳しくは [self-hosting](../self-hosting.md) の ODbL の項と OSMF の Produced Work Guideline で確かめる)。出典: https://docs.protomaps.com/basemaps/downloads 、https://opendatacommons.org/licenses/odbl/summary/
- 国土地理院の最適化ベクトルタイルは国土地理院コンテンツ利用規約に従い、「国土地理院最適化ベクトルタイル」などの出典明示が要る。出典: https://github.com/gsi-cyberjapan/optimal_bvmap

## 出典

- https://docs.protomaps.com/basemaps/downloads (全球ファイルが約 120 GB、z0〜15、ズーム 1 段で約 2 倍、ODbL の Produced Work、pmtiles extract)
- https://build.protomaps.com/20261109.pmtiles (2026-11-10 に Content-Length と pmtiles show で大きさ、版、ズームを測定)
- https://github.com/protomaps/PMTiles と https://github.com/protomaps/PMTiles/blob/main/LICENSE (仕様 v3、ライセンス、Lambda と Workers の配置)
- https://github.com/protomaps/PMTiles/blob/main/js/README.md (MapLibre の addProtocol、Leaflet、CORS)
- https://github.com/protomaps/go-pmtiles/releases (CLI v1.31.2、BSD-3-Clause)
- https://docs.protomaps.com/deploy/ 、https://docs.protomaps.com/deploy/cloudflare 、https://docs.protomaps.com/deploy/aws (配置方式ごとの遅延、URL 形式、費用、制約)
- https://github.com/maplibre/martin (版、ライセンス、対応ソース、GeoParquet が unstable)
- https://github.com/maptiler/tileserver-gl と https://github.com/maptiler/tileserver-gl/blob/master/docs/config.rst (版、BSD-2-Clause、ラスタ描画、PMTiles の指定)
- https://github.com/CrunchyData/pg_tileserv (PostGIS 専用、版、Apache-2.0)
- https://github.com/bbox-services/bbox と https://github.com/t-rex-tileserver/t-rex (BBOX の構成とライセンス、t-rex の保守終了)
- https://github.com/geoserver/geoserver/releases と https://github.com/geoserver/geoserver/blob/main/LICENSE.md (3.0.2、GPL-2.0 以降)
- https://github.com/maplibre/maplibre-native (Android と iOS の CHANGELOG で PMTiles 対応の版)
- https://maplibre.org/maplibre-style-spec/sources/ (raster-dem の encoding)
- https://github.com/CesiumGS/3d-tiles と https://www.ogc.org/standards/3dtiles/ (3D Tiles 1.0/1.1、OGC Community Standard、glTF)
- https://github.com/gsi-cyberjapan/optimal_bvmap と https://cyberjapandata.gsi.go.jp/xyz/optimal_bvmap-v1/optimal_bvmap-v1.pmtiles (ズーム、更新時点、利用規約、2026-11-10 に Content-Length を測定)
- https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/tochi_fudousan_kensetsugyo_tk17_000001_00056.html (行政区域データの GeoJSON と PMTiles の大きさ)
- https://operations.osmfoundation.org/policies/tiles/ (tile.openstreetmap.org の利用条件)
- https://opendatacommons.org/licenses/odbl/summary/ (ODbL の 3 条件)
- https://developers.cloudflare.com/workers/platform/limits/ (Workers のメモリ 128 MB)
- https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html (Lambda のメモリ上限 10,240 MB)

## 未確認のこと

- 公式に公表された「日本だけ」「都道府県だけ」の PMTiles の大きさ。上の日本と東京の値は矩形での dry-run の見積もりで、行政界で切った値ではない
- 市区町村単位の大きさ (測っていない)
- 地形タイル (raster-dem) と 3D Tiles の全国規模の大きさ
- Lambda で PMTiles を返すときのコールドスタートの長さ (Protomaps の文書に記載が無い)
- GeoParquet からリクエスト時にタイルを作る方式の応答速度と、Martin で unstable が外れる時期
- 3D Tiles を常駐サーバー無しの静的ホスティングだけで運用したときの制約 (推測で書いた部分)
- TileServer GL が同梱する MapLibre Native の配布物のライセンス条件の詳細
- Cloudflare R2 と AWS S3 の保存と転送の単価 (このファイルでは確かめていない)
