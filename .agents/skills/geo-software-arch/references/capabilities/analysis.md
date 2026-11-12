# 解析

対象: 空間結合、集計、バッファ、ラスタの計算、H3 などのグリッド集計

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |

## 3 つの型

この機能を実現する型は 3 つある: 外部の API、常駐する DB やバッチ基盤 (PostGIS、Spark など)、ファイルと関数 (GeoParquet や COG を DuckDB、GDAL で直接読む。関数かブラウザで動かす)。

| 型 | 主なツール・サービス (版、ライセンス) | 保存の置き場所 | 計算の置き場所 | 表現 (応答の形式) | 出典 |
|---|---|---|---|---|---|
| 外部の API | クラウドのマネージドなデータウェアハウスの地理関数 (例として BigQuery の GEOGRAPHY 型と地理関数。ラスタは別の手順と衛星データ基盤との連携で扱う)。ライセンスと課金は各社の規約による | 提供者のクラウド (データを取り込むか外部テーブルで参照する) | 提供者のクラウド | SQL の結果表、GeoJSON などへの変換 (`ST_ASGEOJSON`) | https://docs.cloud.google.com/bigquery/docs/geospatial-intro |
| 常駐するサーバー | PostGIS 3.7.0 (2026-10-30 タグ、GPL-2.0 以降。依存の GEOS は LGPL、PROJ と GDAL は MIT 系、SFCGAL は GPL-2.0 以降)、Apache Sedona 1.9.1 (2026-08-05 公開、Apache-2.0。Spark と Flink 上で大きなベクタとラスタを分散処理する。単一ノード向けの SedonaDB もある)、TiTiler 2.4.0 (2026-09-21 公開、MIT。FastAPI の動的タイル、COG と STAC に対応) | DB のディスク、クラスタの分散ストレージ、オブジェクトストレージ上の COG | 常駐の DB、Spark や Flink のクラスタ、タイルサーバー | SQL の結果、ベクトルタイル、ラスタタイル | https://github.com/postgis/postgis/blob/master/LICENSE.TXT 、 https://github.com/postgis/postgis/blob/master/NEWS 、 https://github.com/apache/sedona 、 https://github.com/developmentseed/titiler |
| ファイルと関数 | DuckDB v2.0.0 (2026-10-21 公開、MIT) と spatial 拡張 (MIT。GEOS、PROJ、GDAL を静的に組み込み、`ST_Read` で GDAL の形式を読む) で GeoParquet (仕様 v2.0.0、2026-11-05 公開、Apache-2.0) を HTTP 越しに読む。GDAL v3.13.3 (2026-08-18 公開、MIT 系) の `/vsicurl/` と `/vsis3/` で COG を Range 読みする。TiTiler を短命な関数に載せる (公式手順に AWS Lambda への配置がある)。ブラウザでは DuckDB-Wasm (spatial 拡張を読み込める)、gdal3.js 2.8.1 (LGPL-2.1)、turf.js v7.4.0 (MIT)、h3-js v4.5.0 (Apache-2.0)、geos-wasm (LGPL) | オブジェクトストレージや CDN 上の GeoParquet、COG、FlatGeobuf などの単一ファイル | 短命な関数、ブラウザ (Wasm、Worker)、ブラウザの GPU | 関数が返す JSON や画像タイル、ブラウザ内の表、deck.gl などの描画 | https://github.com/duckdb/duckdb 、 https://github.com/duckdb/duckdb-spatial/blob/main/vcpkg.json 、 https://github.com/duckdb/duckdb-spatial/blob/main/docs/functions.md 、 https://github.com/opengeospatial/geoparquet 、 https://gdal.org/en/stable/user/virtual_file_systems.html 、 https://developmentseed.org/titiler/deployment/aws/lambda/ 、 https://duckdb.org/docs/2.0/clients/wasm/extensions.html 、 https://github.com/bugra9/gdal3.js 、 https://github.com/Turfjs/turf 、 https://github.com/uber/h3-js 、 https://github.com/chrispahm/geos-wasm |

## 置き場所ごとの実現手段

| 置き場所 | 実現手段 (ツール、形式、API) | 制約 (データの大きさ、メモリ、起動時間、更新) | 出典 |
|---|---|---|---|
| クラウド | 常駐の PostGIS、Sedona のクラスタ、マネージドなデータウェアハウスの地理関数。短命な関数で DuckDB spatial や GDAL を動かし、オブジェクトストレージの GeoParquet と COG を読む。TiTiler を関数に載せてラスタを動的にタイル化する | 関数はメモリ 128 MB から 10,240 MB、実行は最長 900 秒、同期応答は 6 MB まで、/tmp は 512 MB から 10,240 MB。TiTiler の Lambda 配置の既定はメモリ 1,536 MB、タイムアウト 10 秒。大きな結合や全国の集計は関数の時間とメモリに収まらない場合があり、その場合はバッチか常駐の DB に回す (推測) | https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html 、 https://developmentseed.org/titiler/deployment/aws/lambda/ |
| エッジ (CDN のエッジ関数、利用者の近くに置く小さなサーバー) | GeoParquet、COG、PMTiles などのファイルを CDN に置き、Range 要求で必要な部分だけ返す。軽い集計 (turf.js や h3-js のような JS ライブラリ) をエッジ関数で回す | 代表的なエッジ関数はアイソレートあたり 128 MB (JS ヒープと Wasm を含む)、スクリプトは非圧縮 64 MiB まで、CPU 時間は無料枠で 10 ms、有料で最長 5 分。GDAL や DuckDB を丸ごと載せた重い処理には向かない (推測) | https://developers.cloudflare.com/workers/platform/limits/ |
| ブラウザ | DuckDB-Wasm に spatial 拡張を読み込み、GeoParquet を HTTP で読んで SQL で結合と集計をする。gdal3.js で ogr2ogr、gdal_translate、gdalwarp などをブラウザで動かす。turf.js でバッファや点の内外判定、h3-js でグリッド集計、geos-wasm で GEOS の幾何演算。集計の描画は deck.gl の集計レイヤー (GPU 集計) で行う。browser/ の reference の Wasm、Worker、OPFS の項と結びつく | Wasm のメモリは 4 GB が上限で、ブラウザはさらに低く制限しうる。DuckDB-Wasm は既定で 1 スレッド (マルチスレッドは実験的)。JS の httpfs 経路は必要な Range だけを取るが、組み込みの httpfs 拡張経由では「ファイル全体を落とすことがある」と文書にある。spatial 拡張の依存定義では、GDAL のネットワーク機能と curl は wasm32 で無効になっている。deck.gl の GPU 集計は 10 万点を超える大きなデータで速く、小さなデータではかえって遅いことがある。WebGPU 対応は main ブランチの文書で集計レイヤーが v9.4 から対応と書かれているが、最新リリースは v9.3.12 (2026-10-31 公開) で、文書自体も本番向けではないと注意している | https://duckdb.org/docs/2.0/clients/wasm/overview.html 、 https://duckdb.org/docs/2.0/clients/wasm/extensions.html 、 https://github.com/duckdb/duckdb-spatial/blob/main/vcpkg.json 、 https://github.com/bugra9/gdal3.js 、 https://deck.gl/docs/api-reference/aggregation-layers/overview 、 https://github.com/visgl/deck.gl/blob/master/docs/developer-guide/webgpu.md |
| アプリ (ネイティブ、端末内) | DuckDB、GDAL、GEOS、H3 はいずれも C/C++ のライブラリで、端末に組み込める (推測。端末向けの公式配布の有無は個別に確かめていない)。duckdb-spatial の依存定義は iOS と Android を対象プラットフォームとして扱い、そこでは curl と GDAL のネットワーク機能を外している | 端末のメモリとストレージに収まる範囲のデータに限られる。LGPL の GEOS を静的に組み込むと再リンク可能性の義務が出る (下のライセンスの項) | https://github.com/duckdb/duckdb-spatial/blob/main/vcpkg.json 、 https://github.com/libgeos/geos |

## データの大きさの目安

国、都道府県、市区町村の範囲で、索引やファイルがどれくらいの大きさになるか。公式の記述か、測った条件つきで書く。

- 入力の OSM PBF は日本全体で 2.4 GB、関東 499 MB、四国 87 MB (Geofabrik、2026-11-08 時点のデータ)。解析で GeoParquet に変換したときの大きさは公式の数字が無い。出典 https://download.geofabrik.de/asia/japan.html
- ブラウザで扱える上限は Wasm のメモリ上限 4 GB が天井で、実際はブラウザの制限でそれより下がる。都道府県単位のベクタは Range 読みと列の絞り込みで扱える見込みがあるが、日本全体の建物などを丸ごと読み込むのは厳しい (推測)。出典 https://duckdb.org/docs/2.0/clients/wasm/overview.html
- 短命な関数の /tmp は最大 10,240 MB、メモリは最大 10,240 MB。国単位のファイルを /tmp に置いて処理する形は上限の内側に収まりうる (推測)。出典 https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
- GDAL の `/vsicurl/` は既定で 16 MB の LRU キャッシュを全ダウンロードで共有する。COG や GeoParquet を Range 読みするとき、キャッシュを超えるアクセスは再取得になる。出典 https://gdal.org/en/stable/user/virtual_file_systems.html

## 判断を左右すること

- 更新頻度: 常駐の DB は差分の書き込みと即時の問い合わせに強い。ファイルと関数の型は、データを GeoParquet や COG に作り直して置き換える運用になるので、日次や月次の一括更新に向く (推測)
- 応答の速さ: 関数とブラウザは起動のたびにファイルの必要部分を HTTP で取りに行くので、索引を持つ常駐の DB より初回の応答が遅くなりやすい (推測)。DuckDB-Wasm は既定で単一スレッド。ブラウザ内の集計は deck.gl の GPU 集計で 10 万点超を速く扱える
- オフラインで使いたいか: ブラウザ内の DuckDB-Wasm、turf.js、h3-js、gdal3.js はサーバーなしで動く。ファイルを OPFS などに置けばオフラインでも解析できる (推測)。外部 API と常駐の DB はオフラインで使えない
- 費用 (外部 API の課金単位、自前の計算と転送): マネージドなデータウェアハウスは読んだデータ量か確保した計算資源で課金されるのが典型 (推測。具体的な単価は確かめていない)。常駐の PostGIS や Sedona はサーバーやクラスタの常時の費用がかかる。ファイルと関数は保存と転送と関数の実行時間だけになり、ブラウザで計算すれば計算費用は利用者の端末に移る

## ライセンス上の注意

コピーレフトのツール (GPL、AGPL など) と、データの継承条件 (ODbL など) を、組み込み、改変、配布、SaaS 提供のそれぞれで書く。

- PostGIS (GPL-2.0 以降): DB サーバーとして動かし SQL で使うだけなら、SaaS 提供でもソース開示の義務は生じない (GPL はネットワーク越しの提供を配布とみなさない)。PostGIS を改変して配布する場合、PostGIS をリンクした製品を配布する場合は GPL でソースを出す。PostGIS を同梱したアプライアンスやイメージを配布する場合も PostGIS 部分のソース提供が要る
- GEOS (LGPL-2.1)、gdal3.js (LGPL-2.1)、geos-wasm (GitHub 上は LGPL-2.1、npm の表記は LGPL-3.0 以降): SaaS のサーバー側で使うだけなら開示の義務は無い。ブラウザやアプリに組み込んで配る場合は配布にあたるので、ライブラリ部分のソースの入手手段を示し、利用者がライブラリを差し替えられる形にする。Wasm を 1 ファイルに静的に結合して配るとこの要件を満たしにくいので、ライブラリ部分を別ファイルで配るなどの工夫が要る (推測)。ライブラリ自体を改変したら改変部分を LGPL で出す
- DuckDB と spatial 拡張 (MIT)、GDAL (MIT 系)、PROJ (MIT 系)、turf.js (MIT)、TiTiler (MIT)、deck.gl (MIT)、h3-js と H3 (Apache-2.0)、Sedona (Apache-2.0): 組み込み、改変、配布、SaaS のいずれも、著作権表示とライセンス文を残せば自由。Apache-2.0 は NOTICE の継承と改変の明示が要る。ただし DuckDB spatial は GEOS (LGPL) を静的に組み込んでいるので、spatial 拡張を同梱して配布するときは GEOS の LGPL の条件を確かめる必要がある (推測)
- OSM 由来のデータ (ODbL): 解析で作った結合結果や集計表は派生データベースにあたりうる。公開する場合は ODbL で出し、OSM の帰属と ODbL である旨を示す。地図画像のように元データの抽出を目的としない出力は Produced Work として扱われ、帰属表示が要る
- 外部 API: 結果の保存や再配布、他サービスとの組み合わせに規約上の制限がありうる。採用前に利用規約を読む

## 出典

- https://github.com/postgis/postgis/blob/master/LICENSE.TXT (GPL-2.0 以降と依存ライブラリのライセンス)
- https://github.com/postgis/postgis/blob/master/NEWS と GitHub のタグ 3.7.0 (2026-10-30 JST のタグ、必要な GEOS、PostgreSQL、PROJ の版)
- https://github.com/apache/sedona (Apache-2.0、Spark と Flink での分散処理、SedonaDB、1.9.1)
- https://docs.cloud.google.com/bigquery/docs/geospatial-intro (GEOGRAPHY 型、`ST_ASGEOJSON`、ラスタは別ガイド)
- https://github.com/duckdb/duckdb (MIT、v2.0.0)
- https://github.com/duckdb/duckdb-spatial/blob/main/vcpkg.json (GEOS、PROJ、GDAL への依存、wasm32、iOS、Android で curl と GDAL のネットワーク機能を外していること)
- https://github.com/duckdb/duckdb-spatial/blob/main/docs/functions.md (`ST_Read` が GDAL を使うこと)
- https://duckdb.org/docs/2.0/clients/wasm/overview.html (Wasm のメモリ上限 4 GB、単一スレッド、httpfs の Range 読みの挙動、最新安定版 2.0.0 という記述)
- https://duckdb.org/docs/2.0/clients/wasm/extensions.html (DuckDB-Wasm で spatial 拡張を読み込めること)
- https://github.com/opengeospatial/geoparquet (GeoParquet v2.0.0、Apache-2.0)
- https://gdal.org/en/stable/user/virtual_file_systems.html (`/vsicurl/` の Range 読みと 16 MB のキャッシュ、`/vsis3/`)
- https://github.com/OSGeo/gdal/blob/master/LICENSE.TXT (GDAL が MIT 系であること、v3.13.3)
- https://github.com/developmentseed/titiler (MIT、2.4.0、COG と STAC) と https://developmentseed.org/titiler/deployment/aws/lambda/ (Lambda 配置の既定メモリとタイムアウト)
- https://github.com/bugra9/gdal3.js (LGPL-2.1、2.8.1、ブラウザで動く GDAL のコマンド)
- https://github.com/Turfjs/turf (MIT、v7.4.0)
- https://github.com/uber/h3-js (Apache-2.0、v4.5.0、Emscripten で C から変換) と https://h3geo.org/docs/ (H3 が Apache-2.0)
- https://github.com/chrispahm/geos-wasm と https://www.npmjs.com/package/geos-wasm (GEOS の Wasm 版、ライセンス表記の食い違い)
- https://github.com/libgeos/geos (LGPL-2.1、3.15.0)
- https://deck.gl/docs/api-reference/aggregation-layers/overview (GPU 集計と CPU 集計、10 万点の目安)
- https://github.com/visgl/deck.gl/blob/master/docs/developer-guide/webgpu.md (WebGPU 対応の状況表、本番向けでない旨) と https://github.com/visgl/deck.gl/releases (v9.3.12)
- https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html (関数のメモリ、時間、/tmp、応答サイズの上限)
- https://developers.cloudflare.com/workers/platform/limits/ (エッジ関数のメモリ、CPU 時間、スクリプトの大きさ)
- https://download.geofabrik.de/asia/japan.html (日本と地方別の PBF の大きさ)
- https://www.openstreetmap.org/copyright と https://osmfoundation.org/wiki/Licence/Community_Guidelines/Produced_Work_-_Guideline (ODbL の帰属、継承、Produced Work の定義)

## 未確認のこと

- DuckDB-Wasm の版: DuckDB の文書は最新安定版を 2.0.0 としているが、npm の `@duckdb/duckdb-wasm` の latest タグは 1.33.1-dev57.0、GitHub の最新リリースは v1.33.0 (2025-12-16) で食い違っている
- DuckDB-Wasm で spatial 拡張を使ったとき、GeoParquet を Range 読みで部分取得できるか (GDAL のネットワーク機能が wasm32 で無効なため `ST_Read` で URL を読めるかも含む)
- DuckDB の GEOMETRY 型が本体に入ったか (spatial 拡張の文書には書かれていない)
- geos-wasm のライセンスが LGPL-2.1 か LGPL-3.0 以降か (GitHub と npm で表記が違う)、GitHub 上の最終更新が 2025-01 で保守状況
- gdal3.js の最新リリースは 2024-02 の 2.8.1 で、cpp.js への移行を告知している。今後の保守状況
- マネージドなデータウェアハウスの地理関数の課金単位と単価 (料金ページの本文を取得できなかった)
- 日本全体、都道府県、市区町村の単位で、建物や道路を GeoParquet にしたときの大きさ
- ブラウザごとの Wasm と JS ヒープのメモリ上限の実数 (端末とブラウザで異なり、公式の一覧が無い)
- DuckDB、GDAL、GEOS の iOS と Android 向けの公式配布の有無
