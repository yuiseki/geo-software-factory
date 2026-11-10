# クラウドネイティブな地理空間データ形式

対象: PMTiles、COG、GeoParquet、FlatGeobuf、STAC、Zarr、GeoPackage、MBTiles、MLT (MapLibre Tile)。ファイルのまま置き、必要な部分だけを読める形式

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 (ライブラリの版は npm レジストリの latest、仕様の版は各リポジトリのリリースで確かめた。日付は JST) |

## 形式ごとの性質

| 形式 | 中身 (ベクタ、ラスタ、タイル、目録) | 範囲を絞って読む仕組み (Range、索引、分割) | 仕様の管理と版 | ブラウザで読むライブラリ | エッジ・関数で読む手段 | 出典 |
|---|---|---|---|---|---|---|
| PMTiles | タイルの入れ物。MVT、PNG、JPEG、WebP、AVIF、MapLibre Vector Tile (MLT) を入れられる | 127 バイトのヘッダーと圧縮したルートディレクトリを先頭 16 KiB に収め、最初の 1 回の Range でそれを読む。タイル ID は Hilbert 曲線の順で、葉ディレクトリは 1 段までを推奨。ディレクトリとタイルの圧縮は none、gzip、brotli、zstd から選ぶ | Protomaps の PMTiles リポジトリが管理。仕様は v3 で、仕様そのものはパブリックドメイン (CC0)、参照実装は BSD-3-Clause | pmtiles (npm 4.5.0、BSD-3-Clause)。MapLibre GL JS には `pmtiles://` のプロトコルとして足す | Protomaps が Cloudflare Workers と R2 で z/x/y に変換して配る実装を公開している。go-pmtiles (v1.31.2、BSD-3-Clause) の `pmtiles serve` は z/x/y で配るが、元ファイルへの Range の中継はしない | PMTiles の spec/v3/spec.md、LICENSE、docs.protomaps.com の cli と deploy/cloudflare |
| COG (Cloud Optimized GeoTIFF) | ラスタ (衛星画像、標高など) | タイル分割した GeoTIFF の先頭に索引 (IFD) を置き、縮小版 (overview) を持つ。Range でタイル単位に読む | OGC の実装標準 1.0 (文書番号 21-026、2023-05-08 承認、2023-07-14 公開) | geotiff (geotiff.js、npm 3.0.5、MIT)。`fromUrl` で開き、縮小版の自動選択、範囲と帯の切り出し、Deflate、JPEG、LERC、Zstandard の展開、Web Worker のプールを持つ | TiTiler (2.4.0、MIT。Python で COG から動的にタイルを作る)。GDAL の `/vsicurl/` でも読める (推測。GDAL の文書は未確認) | docs.ogc.org/is/21-026、geotiff.js の README、TiTiler の GitHub |
| GeoParquet | ベクタ (表形式。属性の列と幾何の列) | Parquet の行グループと列単位の配置により、必要な列と行グループだけを Range で読む。2.0 では Parquet の GEOMETRY / GEOGRAPHY 型が持つ行グループごとの空間の統計で絞り込む。1.1 の `bbox` 列も任意で使える | OGC のリポジトリで管理 (OGC で標準化の途中と geoparquet.org は書く)。最新は 2.0.0 (2026-11-05 21:26 JST 公開)。1.1.0 は 2024-06-20 公開。2.0 は Parquet 本体の GEOMETRY / GEOGRAPHY 論理型 (parquet-format 2.11、2025 年 3 月に追加) を土台にし、1.1 で入った GeoArrow 符号化は外して WKB だけに戻した。parquet-format の最新は 2.14.0 (2026-09-11 公開) | hyparquet (npm 1.33.0、MIT。GEOMETRY / GEOGRAPHY 型の列を GeoJSON に変換する。gzip、brotli、zstd などは hyparquet-compressors 1.1.3 で足す)。DuckDB-Wasm (npm @duckdb/duckdb-wasm、MIT。spatial 拡張を実行時に読み込む) | Range が使える実行環境なら hyparquet をそのまま使える (推測。Workers での動作は未確認)。サーバー側では DuckDB で読める | GeoParquet v2.0.0 のリリースノート、geoparquet.org、hyparquet の README と CHANGELOG、DuckDB-Wasm の文書 |
| FlatGeobuf | ベクタ (地物の列) | 任意で packed Hilbert R-tree の空間索引を先頭に置き、範囲に入る地物だけを Range で読む。索引を省けば書きながら流せる | flatgeobuf リポジトリ (BSD-2-Clause) が管理。マジックバイトの 4 バイト目が仕様の主版 (3)、最後のバイトが修正版を表す | flatgeobuf (npm 4.6.1)。地物を 1 件ずつ返し、範囲を指定して読める | 同じ JS 実装を Workers などで使える (推測)。GDAL に FlatGeobuf のドライバがある | flatgeobuf の README |
| STAC | 目録 (衛星画像などの資産の JSON のカタログ) | ファイルを読むのではなく、JSON のカタログ、コレクション、アイテムをたどって、必要な資産 (多くは COG) の URL を見つける | radiantearth/stac-spec が管理。最新は 1.1.0 (2024-09-11 公開) | stac-js (npm 0.5.9、Apache-2.0) | 静的な JSON なので CDN に置くだけで配れる。検索 API を持つには STAC API のサーバーが要る (推測) | stac-spec のリリース |
| Zarr | 多次元の配列 (時系列のラスタ、気象、海洋など) | 配列をチャンクに分け、チャンクごとに別のオブジェクトとして置く。v3 では複数のチャンクを 1 つのシャードにまとめ、Range で中のチャンクを読める (ZEP2 Sharding) | zarr-developers が管理。コア仕様は 3.1 (ZEP0001 が v3)。地理空間の規約 GeoZarr は OGC の GeoZarr SWG が作業中で、まだ OGC 標準ではない。現在は multiscales、proj、spatial の 3 つの規約に分けて進めている | zarrita (npm 0.7.5、MIT)。v2 と v3、シャーディングに対応し、`FetchStore` で HTTP から読む | 同じ zarrita を使える (推測)。Python では zarr と xarray | zarr-specs の docs/v3/core/index.rst、geozarr-spec の README、zarrita.js の README |
| GeoPackage | ベクタ、ラスタのタイル、属性 (SQLite のデータベース 1 個) | SQLite のページ単位の構造と R-tree の索引。HTTP の Range で読むことは想定していない | OGC の標準。最新は 1.4.0 (2024-01-31 公開) | @ngageoint/geopackage (npm 4.2.10、MIT) | 関数の中でファイル全体を持つか、ローカルの記憶域に置いて SQLite で開く (推測) | opengeospatial/geopackage のリリース、npm |
| MBTiles | タイルの入れ物 (SQLite のデータベース 1 個) | SQLite の表を z/x/y で引く。HTTP の Range で読むことは想定していない | mapbox/mbtiles-spec が管理。仕様の最新のディレクトリは 1.3 | ブラウザで直接読む定番のライブラリは無い (推測)。`pmtiles convert` で MBTiles を PMTiles に変換できる | タイルサーバーで配るのが普通 (推測) | mbtiles-spec のリポジトリ、docs.protomaps.com/pmtiles/cli |
| MLT (MapLibre Tile) | ベクタタイル (MVT の代わり) | タイル 1 枚の形式なので、範囲を絞る仕組みは入れ物 (PMTiles や z/x/y) 側に任せる。中身は列指向で、大きなタイルでは MVT より最大 6 倍よく圧縮できる | maplibre/maplibre-tile-spec が管理 (Apache-2.0)。MapLibre は 2026-01-23 に公開を告知。実装状況のページは MLT v2 を experimental としている。型が地物ごとに変わる列は扱えない | MapLibre GL JS 5.12.0 以降 (ソースの `encoding` を `"mlt"` にする)。@maplibre/mlt (npm 1.3.0、MIT または Apache-2.0)。loaders.gl 4.4 以降 | Martin 1.3.0 以降が MLT を配り、1.9.0 以降はヘッダーに応じて MLT と MVT を変換する。Rust の mlt-wasm もある | maplibre.org の発表記事と実装状況のページ |

## 置き場所との関係

形式を選ぶと、保存をどこに置き、計算をどこでするかが変わる。

- 静的ホスティングや CDN に置くだけで、ブラウザから直接読めるもの: PMTiles、COG、GeoParquet、FlatGeobuf、Zarr、STAC (JSON)。いずれも Range か小さなファイルへの分割で必要な部分だけを読む。サーバーの側の条件は、Range に 206 で答えること、CORS で `Range` (と必要なら `If-Match`) を許し、`ETag` を `Access-Control-Expose-Headers` で公開すること (PMTiles の文書)。
- 関数を挟む必要があるもの (CORS、認証、形式の変換): GeoPackage と MBTiles は SQLite なので、普通はサーバーか関数で開いて配る。PMTiles でも、z/x/y の URL しか扱えないクライアント (古い地図 SDK など) に配るとき、利用者ごとの認証を入れるとき、CDN のキャッシュを効かせたいときは関数を挟む。Protomaps の Workers 実装は、Worker を自分のドメインに割り当てないとキャッシュが効かないと書いている。COG を任意の色づけや再投影で配るときは TiTiler のような動的タイルサーバーを挟む。
- 端末に持ち出す (一部を切り出す) ときの手段: `pmtiles extract` は元のアーカイブがリモートでも、`--bbox`、`--region` (GeoJSON)、`--maxzoom` で一部を切り出せる (元のアーカイブがクラスタ化されていることが前提)。GeoParquet と FlatGeobuf は範囲で読んだ地物を端末の中で別のファイルに書き出せる (推測)。GeoPackage はそれ自体が持ち出し用の 1 ファイルの形式である。

## 落とし穴

- CDN の Range キャッシュ: Cloudflare は Free、Pro、Business で 1 ファイル 512 MB を超えるとキャッシュしない (判定はファイル全体の大きさ)。全国の PMTiles や GeoParquet は簡単にこれを超えるので、Enterprise の上限 (既定 5 GB) か、Workers で z/x/y にしてタイル単位でキャッシュする構成にする。Cloudflare は拡張子でキャッシュ対象を決め、`.pmtiles` と `.parquet` は既定で対象外なので Cache Rule が要る。CloudFront は 50 GB を超える物体をキャッシュしないが、Range で取った部分はキャッシュする。
- CORS: 単一範囲の Range はプリフライト無しで送れるが、`If-Match` や `Authorization` を付けると毎回プリフライトが起きる。pmtiles の JS はこれを避けるために `If-Match` を送らない。Tigris はプリフライトのためにメソッドとヘッダーを `*` にする必要があり、Supabase の公開バケットは全オリジンを許す (PMTiles の文書)。
- HTTP/2 の多重化: S3、Azure、DigitalOcean (CDN を有効にしても)、Backblaze B2、Scaleway は HTTP/1.1 だけを話す (PMTiles の文書)。多数の Range を並べるタイル読みでは、HTTP/2 以上を話す CDN を前に置く (推測)。
- ファイルの差し替え中の不整合: 同じ URL のファイルを差し替えると、古いディレクトリと新しいタイルを混ぜて読む恐れがある。pmtiles の JS は最初に読んだ ETag を覚え、違う ETag か 416 が返ったら `cache: "reload"` で取り直し、それでも違えばエラーにする。弱い ETag (`W/` で始まる) は無視する。コードの注記は Cloudflare R2 をこの点で振る舞いのおかしいストレージとして挙げている。ファイル名に版や日付を入れて別の URL として置き、参照を切り替えるほうが確実である (推測)。
- 課金: Range の 1 回はストレージの GET 1 回として課金される (PMTiles の文書)。CDN を前に置かないと、タイル 1 枚ごとにストレージの要求料金がかかる。
- Range と HTTP の圧縮: アーカイブに `Content-Encoding` をかけると範囲が圧縮後のバイトを指してしまい、Cloudflare はオリジンの 206 をキャッシュしない。中身を形式の側で圧縮し、配信時の圧縮はかけない。
- PMTiles の圧縮の選び方: 仕様は brotli と zstd を許すが、pmtiles の JS の既定の展開関数は gzip と無圧縮しか扱わず、Chrome の DecompressionStream は brotli に対応していない (browser/network.md)。ブラウザで直接読むなら gzip にする。
- GeoParquet の版の混在: 2.0 はまだ出たばかり (2026-11-05) で、1.1 の GeoArrow 符号化は 2.0 で外された。Cloud Native Geo のブログは、道具が Parquet の地理空間型に追いつくまで本番では 1.1 を使い続けるよう勧めている (2025 年 10 月の記事)。読む側のライブラリがどの版を読めるかを確かめてから出力の版を決める。
- DuckDB-Wasm は Firefox で Range が失敗することがあり、S3 の署名付き URL では Range の対応を正しく判定できない場合がある。メモリは 4 GB まで。
- MLT は MapLibre GL JS 5.12.0 以降と MapLibre Native (Android 12.1.0、iOS 6.2.0) 以降でしか描けない。他の描画ライブラリに渡すなら MVT を残すか、Martin で MVT に変換して配る。
- LGPL のライブラリ: GDAL を Wasm にした gdal3.js (npm 2.8.1) は LGPL-2.1-or-later である。組み込みは別のモジュールとして読み込む形なら可能で、ライブラリ自体を改変して配布するときは改変部分を LGPL で公開する。配布するときは LGPL の部分のソースの入手手段を示し、利用者がその部分を差し替えられるようにする義務がある。サーバーの中だけで使う SaaS には配布の義務は生じない。ブラウザに Wasm を送るのは配布にあたると考えるのが安全である (推測。法的な判断は未確認)。

## 出典

- https://github.com/protomaps/PMTiles/blob/main/spec/v3/spec.md (ヘッダー 127 バイト、先頭 16 KiB、Hilbert 順、圧縮とタイル種別の一覧、葉ディレクトリの段数)
- https://github.com/protomaps/PMTiles/blob/main/LICENSE (仕様は CC0、参照実装は BSD-3-Clause)
- https://github.com/protomaps/PMTiles/blob/main/js/src/index.ts (Range の送り方、ETag と 416 の扱い、gzip だけを展開する既定の関数、R2 についての注記)
- https://docs.protomaps.com/pmtiles/cloud-storage (各ストレージの CORS の設定例、HTTP/1.1 だけのストレージ、Range 1 回が GET 1 回であること)
- https://docs.protomaps.com/pmtiles/cli (`convert`、`extract`、`serve` の機能と制約)
- https://docs.protomaps.com/deploy/cloudflare (Workers と R2 での配信、独自ドメインが要ること)
- https://docs.ogc.org/is/21-026/21-026.html (COG 1.0 の承認日と公開日)
- https://github.com/geotiffjs/geotiff.js (geotiff.js の機能と展開できる圧縮形式)
- https://github.com/developmentseed/titiler (TiTiler の版とライセンス)
- https://github.com/opengeospatial/geoparquet/releases/tag/v2.0.0 (2.0 の変更点、Parquet 2.11 の GEOMETRY / GEOGRAPHY 型、GeoArrow 符号化の削除、bbox 列の扱い)
- https://geoparquet.org/ (OGC で標準化の途中であること)
- https://github.com/apache/parquet-format/releases (parquet-format 2.14.0 の公開日)
- https://cloudnativegeo.org/blog/2025/10/geoparquet-parquet-geospatial-types-a-time-of-transition/ (本番では 1.1 を使い続けるよう勧める記事)
- https://github.com/hyparam/hyparquet (README の Range 読み、GEOMETRY / GEOGRAPHY 型の扱い、圧縮形式。CHANGELOG の地理空間型の対応)
- https://duckdb.org/docs/2.0/clients/wasm/extensions.html と https://duckdb.org/docs/2.0/clients/wasm/troubleshoot (spatial 拡張、httpfs、Firefox と S3 の既知の問題、4 GB の上限)
- https://github.com/flatgeobuf/flatgeobuf (packed Hilbert R-tree、マジックバイトと版、HTTP Range と CDN の注意)
- https://github.com/radiantearth/stac-spec/releases (STAC 1.1.0 の公開日)
- https://github.com/zarr-developers/zarr-specs/blob/main/docs/v3/core/index.rst (Zarr コア仕様 3.1)
- https://github.com/zarr-developers/geozarr-spec (GeoZarr の進め方と 3 つの規約)
- https://www.ogc.org/standards-working-gr/geozarr-swg-geozarr-swg/ (GeoZarr SWG)
- https://github.com/manzt/zarrita.js (v2 と v3、シャーディング、FetchStore)
- https://github.com/opengeospatial/geopackage/releases (GeoPackage 1.4.0 の公開日)
- https://github.com/mapbox/mbtiles-spec (MBTiles 仕様のディレクトリ 1.0〜1.3)
- https://maplibre.org/news/2026-01-23-mlt-release/ (MLT の公開、圧縮率、型の制約)
- https://maplibre.org/maplibre-tile-spec/implementation-status/ (MapLibre GL JS 5.12.0、Native、Martin、Planetiler、loaders.gl の対応版、v2 が experimental であること)
- https://developers.cloudflare.com/cache/concepts/default-cache-behavior/ と https://developers.cloudflare.com/cache/reference/range-requests/ (Cloudflare のキャッシュの上限、拡張子、206 をキャッシュする条件)
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RangeGETs.html (CloudFront の Range と 50 GB の上限)
- https://registry.npmjs.org/ (各ライブラリの latest の版とライセンス表記。pmtiles、geotiff、hyparquet、hyparquet-compressors、@duckdb/duckdb-wasm、flatgeobuf、stac-js、zarrita、@ngageoint/geopackage、@maplibre/mlt、@loaders.gl/core、gdal3.js)

## 未確認のこと

- GeoParquet 2.0 (Parquet の GEOMETRY / GEOGRAPHY 型) を DuckDB-Wasm の spatial 拡張が読めるか、どの版からか。
- hyparquet、flatgeobuf、zarrita、geotiff.js が Cloudflare Workers などのエッジ関数でそのまま動くか。
- GDAL の `/vsicurl/` での COG と FlatGeobuf の読み方の公式の記述。
- @ngageoint/geopackage がブラウザでファイル全体を読み込むのか、部分的に読めるのか。
- MBTiles と GeoPackage を HTTP Range で読む方法 (sql.js-httpvfs などの SQLite を Range で読む仕組み) の現在の保守状況。sql.js-httpvfs のリポジトリの最終更新は 2024-08-07 (JST) だった。
- MLT のどの版 (v1、v2) を各実装が読み書きするか。
- flatgeobuf の npm パッケージのライセンス表記 (BSD-3-Clause) とリポジトリのライセンス (BSD-2-Clause) が食い違う理由。
- MBTiles 仕様の最新版 1.3 の公開日。
- STAC が OGC の Community Standard になっているか。
- LGPL のライブラリをブラウザ向けの Wasm として配る場合の義務の法的な解釈。
