# 自前でのタイル配信 (self-hosting)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |

リリース日は GitHub API (`gh api repos/OWNER/REPO/releases/latest`) の `published_at` を日本時間に直した日付である。価格は米ドル (USD) で、2026-11-10 に各社の公式料金ページで確かめた。

## いつ候補に入れるか

- 表示回数が多く、商用タイル API の従量課金が月額の大部分を占める。自前配信の費用は保存と転送の単価でほぼ決まり、地図ロード数に対する単価が商用 API より低くなる場合がある (下の「費用の見積もり」で損益分岐を求める)。
- 外部の地図 API に通信できない、または利用者の位置や閲覧範囲を第三者に送れない (閉域網、自治体の内部システム、オフライン端末など)。PMTiles 1 ファイルを手元のストレージに置けば外部通信なしで配信できる。
- 地図の中身 (どの地物を何ズームから出すか、属性の持ち方) を自分で決めたい。Planetiler や tilemaker はプロファイルや Lua スクリプトでスキーマを書き換えられる。
- 自前データ (施設、区画、計画線など) をベースマップのタイルに焼き込みたい、または同じ配信基盤で重ねたい。Planetiler は GeoPackage、GeoJSON、Shapefile、GeoParquet を入力に取れる ([Planetiler README](https://github.com/onthegomap/planetiler#features))。
- 商用サービスの規約 (キャッシュ禁止、オフライン保存禁止、表示先の制限など) が要件と合わない。

## 構成の型

| 型 | 構成 | 必要なもの | 長所 | 短所 |
|---|---|---|---|---|
| 静的 PMTiles | PMTiles 1 ファイルをオブジェクトストレージ + CDN で配信 | PMTiles ファイル、HTTP Range リクエストに応じるストレージ (R2、S3 など)、CDN。z/x/y の URL で配る場合は Range 変換用の関数 (Cloudflare Workers、AWS Lambda など) ([Protomaps: Deploy](https://docs.protomaps.com/deploy/)) | 常駐サーバーが無く、通信が無ければ費用がほぼ保存料だけになる (Cloudflare と AWS は scale-to-zero、[Protomaps: Deploy](https://docs.protomaps.com/deploy/))。更新はファイルの差し替えで済む | 関数なしの素の PMTiles は z/x/y 互換でなく、クライアントに pmtiles ライブラリが要る。単一リージョンのバケットだけでは遠い利用者に数秒かかることがあり CDN が要る ([Protomaps: Deploy](https://docs.protomaps.com/deploy/)) |
| タイルサーバー | MBTiles / PostGIS からサーバーで配信 | 常駐するサーバー (Martin、tileserver-gl など)、PostGIS を使う場合はデータベース、前段の CDN | PostGIS のテーブルや関数から動的にタイルを返せる、スタイル・スプライト・グリフも同じサーバーで返せる ([Martin](https://maplibre.org/martin/))。tileserver-gl はサーバー側でラスタ化もできる ([tileserver-gl README](https://github.com/maptiler/tileserver-gl)) | サーバーの監視、更新、スケールの手間がかかる。通信が無くても稼働費がかかる |
| 静的 z/x/y | 事前生成したタイル群を静的に置く | タイルを 1 枚ずつファイルとして置けるストレージと Web サーバー (または CDN) | z/x/y の URL をそのまま静的ファイルとして返せ、特別なソフトが要らない。OpenFreeMap は nginx が Btrfs イメージ上のファイルを返す構成で、タイルサーバーを使わない ([OpenFreeMap](https://openfreemap.org/)) | ファイル数が膨大になる (OpenFreeMap の planet はハードリンク込みで 3 億ファイル、[OpenFreeMap](https://openfreemap.org/))。アップロード、差し替え、オブジェクトストレージの書き込み回数課金の負担が大きい |

## タイルの生成

| ツール | 入力 | 出力スキーマ | 全球 (planet) 生成の資源と時間 (公式の数字、出典つき) | ライセンス | 最終リリース |
|---|---|---|---|---|---|
| Planetiler | OSM `.osm.pbf`、Natural Earth、GeoPackage、GeoJSON、Shapefile、GeoParquet (Overture Maps) ([README](https://github.com/onthegomap/planetiler#features)) | 既定は OpenMapTiles。Protomaps Basemaps、Shortbread のプロファイルもある。Java または YAML で独自スキーマを書ける。出力は MBTiles / PMTiles、タイル形式は MVT または MLT (`--tile-format=mlt`) ([README](https://github.com/onthegomap/planetiler)) | OpenMapTiles プロファイル、planet 92GB (2026-03-02 版) を v0.10.1、h4d-standard-192 (192 CPU / 720GB) で 19 分、出力 81GB の PMTiles。v0.7.0、c7gd.16xlarge (64 CPU / 128GB) で planet 73GB を 42 分、出力 69GB。v0.5.0、c6gd.4xlarge (16 CPU / 32GB) で 2 時間 38 分 ([README Benchmarks](https://github.com/onthegomap/planetiler#benchmarks))。目安として RAM は入力 pbf の 0.5 倍以上、ディスクは 1GB + pbf の 5〜10 倍 ([README](https://github.com/onthegomap/planetiler)) | Apache-2.0 | v0.10.2 (2026-03-29) |
| tilemaker | OSM `.osm.pbf`、海岸線や土地被覆の Shapefile ([README](https://github.com/systemed/tilemaker)) | 同梱の設定は OpenMapTiles 互換。JSON 設定と Lua スクリプトで独自スキーマを書ける。出力はファイル群、MBTiles、PMTiles ([README](https://github.com/systemed/tilemaker)) | 作者の発表 (2024-01-15) で、3.0 は planet を 24GB RAM、4.5 時間 (古いハードウェア)、2.0 は同じ機械で 130GB RAM、37 時間。新しいハードウェアなら 90 分未満 ([OSM Community: Tilemaker 3.0](https://community.openstreetmap.org/t/tilemaker-3-0-creating-vector-tiles/108111))。マシン構成の詳細は書かれていない | FTWPL (独自の寛容なライセンス、無保証) ([LICENCE.txt](https://github.com/systemed/tilemaker/blob/master/LICENCE.txt)) | v3.2.0 (2026-08-30) |
| OpenMapTiles | OSM `.osm.pbf` を imposm で PostGIS に取り込む ([README](https://github.com/openmaptiles/openmaptiles)) | OpenMapTiles スキーマ (このリポジトリがスキーマ本体と PostGIS ベースの生成手順) | 未確認 (公式 README に planet の所要時間と資源の数字が無い) | コードは BSD-3-Clause、スキーマのデザイン (look and feel) は CC-BY 4.0 で「© OpenMapTiles」の表示が要る ([LICENSE.md](https://github.com/openmaptiles/openmaptiles/blob/master/LICENSE.md)) | v3.16 (2025-12-18) |
| Protomaps basemaps | OSM、Natural Earth、osmdata.openstreetmap.de の海陸ポリゴン ([LICENSE_DATA.md](https://github.com/protomaps/basemaps/blob/main/LICENSE_DATA.md))。Overture のダウンロード用スクリプトもある | Protomaps Basemap スキーマ (Planetiler のプロファイルとして実装)。出力は PMTiles ([README](https://github.com/protomaps/basemaps)) | README に「modest computer で 2〜3 時間」とあるが、機械の構成は書かれていない ([README](https://github.com/protomaps/basemaps)) | コードは BSD-3-Clause、スタイルのデザインは CC0 ([LICENSE.md](https://github.com/protomaps/basemaps/blob/main/LICENSE.md))。出力データは入力データのライセンス (OSM なら ODbL) に従う | GitHub Release は無い。タイルのプロファイルは 4.15.2 (CHANGELOG の最終更新 2026-08-12)、スタイルの npm パッケージ `@protomaps/basemaps` は 5.7.2 |

- 生成済みのタイルを配布しているところと利用条件:
  - Protomaps: v4 の planet ビルドを毎日 `maps.protomaps.com/builds` で公開している。z0〜15 で約 120GB。ODbL の Produced Work として配布し、OpenStreetMap の帰属表示が要る。URL は変わりうるのでホットリンクせず自分のストレージへコピーするよう求めている。過去 1 週間分と各パッチ版の最新が残る ([Protomaps: Downloads](https://docs.protomaps.com/basemaps/downloads))。
  - OpenFreeMap: OpenMapTiles スキーマ (無改変) を Planetiler で生成し、公開インスタンスを無料で提供している。商用利用可、帰属表示が要る、地図表示回数とリクエスト数の制限は無い、SLA は無い。オフライン用の一括ダウンロードは 3,000 タイルまたは 50MB まで。planet の Btrfs イメージと MBTiles を毎週公開し、自前配信もできる ([OpenFreeMap](https://openfreemap.org/))。プロジェクトのコードは MIT ([LICENSE.md](https://github.com/hyperknot/openfreemap/blob/main/LICENSE.md))。
  - MapTiler: OpenMapTiles の planet を配布している (tileserver-gl の README からリンクされる [data.maptiler.com](https://data.maptiler.com/downloads/planet/))。利用条件と価格は未確認。

## 配信

| 方法 | 概要 | ライセンス | 最終リリース | 備考 |
|---|---|---|---|---|
| PMTiles + オブジェクトストレージ + CDN | PMTiles は 1 ファイルにタイルと索引を収めた形式で、クライアントは HTTP Range で必要な部分だけ読む。z/x/y の URL で返す場合はストレージ、Range に変換する関数、エッジキャッシュの 3 つで組む ([Protomaps: Deploy](https://docs.protomaps.com/deploy/))。CLI の `pmtiles` (go-pmtiles) で抽出 (`pmtiles extract`)、検査、`pmtiles serve` による配信ができる | 仕様は public domain / CC0、参照実装は BSD-3-Clause ([PMTiles LICENSE](https://github.com/protomaps/PMTiles/blob/main/LICENSE))。go-pmtiles は BSD-3-Clause | go-pmtiles v1.31.2 (2026-07-23)、JS ライブラリ `pmtiles` は npm 4.5.0。PMTiles リポジトリ自体に GitHub Release は無い | 仕様の現行版は v3 ([spec](https://github.com/protomaps/PMTiles/tree/main/spec))。Protomaps の比較表では Cloudflare を予算重視の初心者向けに推している ([Protomaps: Deploy](https://docs.protomaps.com/deploy/)) |
| Martin | Rust 製のタイルサーバー。PostGIS のテーブルと関数 (自動検出)、PMTiles、MBTiles、COG、GeoJSON、GeoParquet を配信し、スタイル配信、スプライトとグリフのその場生成もする。`martin cp` で一括生成もできる ([Martin](https://maplibre.org/martin/)) | Apache-2.0 | 安定版 martin-v1.16.1 (2026-09-10)、プレリリース martin-v2.0.0-beta.6 (2026-11-05) | v1.9.0 から要求ヘッダに応じて MLT と MVT を相互変換できる ([MLT implementation status](https://maplibre.org/maplibre-tile-spec/implementation-status/))。スタイルからのラスタ化は公式ページに記述が無く未確認 |
| tileserver-gl | Node.js 製。MBTiles と PMTiles (ローカル、URL、S3) を入力に、ベクトルタイル、スタイル、フォント、WMTS、静止画像を配信する ([README](https://github.com/maptiler/tileserver-gl)、[config.rst](https://github.com/maptiler/tileserver-gl/blob/master/docs/config.rst)) | BSD-2-Clause ([LICENSE.md](https://github.com/maptiler/tileserver-gl/blob/master/LICENSE.md)) | v5.7.0 (2026-10-24) | ラスタ化できる。`tileserver-gl` は MapLibre Native によるサーバー側ラスタ化を含み、ネイティブ依存がある。`tileserver-gl-light` は純 JavaScript でラスタ化を含まない ([README](https://github.com/maptiler/tileserver-gl)) |

## タイル形式

- MVT: Mapbox Vector Tile。Protocol Buffers でレイヤー、地物、属性を 1 タイルに収める形式で、仕様の現行版は 2.1 ([mapbox/vector-tile-spec](https://github.com/mapbox/vector-tile-spec/tree/master/2.1))。Planetiler、tilemaker、Martin、tileserver-gl、MapLibre GL JS / Native など、この文書で扱うツールはすべて MVT を扱える。
- MLT (MapLibre Tile, https://github.com/maplibre/maplibre-tile-spec): MVT を参考に列指向で設計し直した形式で、大きなタイルで最大 6 倍の圧縮率をうたう。仕様は 2025 年 10 月に stable とされたが、実験的な機能は変わりうる ([README](https://github.com/maplibre/maplibre-tile-spec))。MVT とは完全には互換でなく、同じレイヤーの属性は 1 つの型に揃える必要があるなどの制約がある ([README](https://github.com/maplibre/maplibre-tile-spec))。デコードは MapLibre GL JS 5.12.0 以降、MapLibre Android 12.1.0 / iOS 6.2.0 以降、loaders.gl 4.4 以降が対応。生成は Planetiler 0.10.0 以降、Martin 1.9.0 以降 (MVT との変換)。tippecanoe と tilemaker は C++ エンコーダ待ち ([implementation status](https://maplibre.org/maplibre-tile-spec/implementation-status/))。ライブラリは Java、JavaScript、Rust、Python などが言語別にリリースされている (例: java-v0.0.12、2026-10-31)。仕様は CC0、コードは Apache-2.0 と MIT のデュアル。
- PMTiles / MBTiles (コンテナ形式): どちらもタイルを 1 ファイルにまとめる入れ物で、中身は MVT、MLT、PNG、WebP などを入れられる。MBTiles は SQLite データベースで (仕様の最新は 1.3、[mbtiles-spec](https://github.com/mapbox/mbtiles-spec/blob/master/1.3/spec.md))、読むにはサーバーが要る。PMTiles は HTTP Range で直接読める単一ファイル形式で、サーバーなしでオブジェクトストレージから配信できる ([PMTiles spec v3](https://github.com/protomaps/PMTiles/tree/main/spec/v3))。PMTiles は MLT を格納できるが MLT を生成はしない ([implementation status](https://maplibre.org/maplibre-tile-spec/implementation-status/))。

## 地形タイル

- 標高タイルの形式: MapLibre の `raster-dem` ソースは `encoding` に `mapbox` (Mapbox Terrain-RGB、既定値)、`terrarium` (Terrarium 形式)、`custom` (`redFactor`、`greenFactor`、`blueFactor`、`baseShift` で線形に復号) を指定できる。`custom` は MapLibre GL JS 3.4.0 以降で、MapLibre Native は未対応 ([MapLibre Style Spec: Sources](https://maplibre.org/maplibre-style-spec/sources/))。国土地理院の PNG 標高タイルは x = 2^16 R + 2^8 G + B、分解能 0.01m で、x が 2^23 以上なら負の値、(128, 0, 0) が無効値という独自の符号化である ([国土地理院: 標高タイルの詳細仕様](https://maps.gsi.go.jp/development/demtile.html))。推測: 負の値の扱いが線形でないため、`custom` だけでは海面下の値を正しく復号できず、Terrarium などへの変換か独自のプロトコル処理が要る。
- Mapterhorn (https://github.com/mapterhorn/mapterhorn): 公開の地形タイルを提供している。`https://tiles.mapterhorn.com/{z}/{x}/{y}.webp` で、Terrarium 符号化の WebP、512px タイル。AWS の Terrain Tiles (Tilezen Joerd) からの移行手順も README にある ([README](https://github.com/mapterhorn/mapterhorn)、[Data Access](https://mapterhorn.com/data-access))。PMTiles もダウンロードでき、planet.pmtiles は z0〜12 で 355,579,263,191 バイト (約 356GB)、z13 以上は地域ごとのファイルに分かれる ([download_urls.json](https://download.mapterhorn.com/download_urls.json)、v0.0.13)。全球は Copernicus GLO-30 (30m)、日本は国土地理院の基盤地図情報 数値標高モデル (1m、5m、10m) を使い、そのライセンス欄は「国土地理院コンテンツ利用規約／測量法に基づく国土地理院長承認（使用）R 8JHs 131」である ([source-catalog/jpdem1a](https://github.com/mapterhorn/mapterhorn/blob/main/source-catalog/jpdem1a/metadata.json)、[glo30](https://github.com/mapterhorn/mapterhorn/blob/main/source-catalog/glo30/metadata.json))。コードは BSD-3-Clause、データの出典一覧は [mapterhorn.com/attribution](https://mapterhorn.com/attribution)。利用規約、ホットリンクの可否、必要な帰属表示の文言は未確認。
- 国内の標高データの入手先: 国土地理院の基盤地図情報ダウンロードサービスで数値標高モデル (1m、5m、10m) を入手できる ([基盤地図情報ダウンロードサービス](https://service.gsi.go.jp/kiban/app/))。タイル化済みのものとして国土地理院の標高タイル (PNG / テキスト) がある ([標高タイルの詳細仕様](https://maps.gsi.go.jp/development/demtile.html))。

## スタイル・フォント・スプライト

- タイル以外に自前で用意するもの: スタイル JSON (MapLibre Style Spec)、グリフ (フォントを範囲ごとに PBF にしたもの)、スプライト (アイコン画像と索引 JSON)、TileJSON (必要なら)、帰属表示の文言。Protomaps basemaps はスタイルを npm パッケージで生成し、フォントとスプライトを [basemaps-assets](https://github.com/protomaps/basemaps-assets) で配布している ([README](https://github.com/protomaps/basemaps))。Martin はスプライトとグリフをその場で生成して配信できる ([Martin](https://maplibre.org/martin/))。地形を使うなら標高タイルも要る。
- 日本語フォント (グリフ) の用意: MapLibre GL JS は `localIdeographFontFamily` (既定値 `'sans-serif'`) で CJK の文字をブラウザのローカルフォントで描き、グリフサーバーへの重い取得を避ける。`false` にするとスタイルのフォント設定が CJK にも効く ([MapLibre GL JS: MapOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapOptions/))。サーバー側で日本語グリフを配る場合は、日本語を含むフォント (Noto Sans CJK JP など) から PBF を生成するか、Martin のようにフォントファイルからグリフを生成するサーバーを使う。推測: 漢字の範囲は PBF の数と容量が大きくなるので、既定のローカル描画で足りるかを先に確かめるのがよい。

## タイル以外を自前で持つ: ジオコーディング

| ツール | データ源 | 日本の住所への対応 | ライセンス | 最終リリース |
|---|---|---|---|---|
| Pelias | OpenStreetMap、OpenAddresses、Who's on First、GeoNames ([data sources](https://github.com/pelias/documentation/blob/master/data-sources.md))。Elasticsearch を使う | 2025-02-04 にマージされた pelias/schema #498 で ICU tokenizer を使い、日本語、タイ語、中国語の解析を改善した ([PR #498](https://github.com/pelias/schema/pull/498))。日本の住所での実用的な精度と、日本の住所データの収録状況は未確認 | MIT (pelias/pelias) | pelias/api v7.11.0 (2026-09-26)。pelias/pelias に GitHub Release は無い |
| Photon | OpenStreetMap。Nominatim のデータベースから取り込む、または GraphHopper が毎週公開するダンプ (全世界と一部の国) を使う。OpenSearch ベース。planet で約 95GB のディスク、64GB 以上の RAM を推奨 ([README](https://github.com/komoot/photon)) | 配布ダンプには英語、ドイツ語、フランス語、現地語の名称が入る ([README](https://github.com/komoot/photon))。日本の住所文字列の解析への対応は未確認 | Apache-2.0 | 1.3.0 (2026-08-08) |
| Nominatim | OpenStreetMap。PostgreSQL / PostGIS。planet の取り込みは 128GB 以上の RAM を強く推奨、ディスク 1TB 以上、NVMe で約 2.5 日 ([Installation](https://nominatim.org/release-docs/latest/admin/Installation/)) | クエリ前処理 `split-japanese-phrases` があり、日本の住所を都道府県、市区町村、その他に分割する。`query_preprocessing.yaml` に手順として加えて使う ([Query Preprocessing](https://nominatim.org/release-docs/develop/customize/Query-Preprocessing/))。v5.3.3 のタグにも実装 (`split_japanese_phrases.py`) がある ([ソース](https://github.com/osm-search/Nominatim/blob/v5.3.3/src/nominatim_api/query_preprocessing/split_japanese_phrases.py))。OSM 上の日本の住所データの充実度に精度が左右される (推測) | GPL-3.0 | v5.3.3 (2026-10-15) |

## 費用の見積もり

- planet の PMTiles のおおよそのサイズ: Protomaps basemaps の planet (z0〜15) が約 120GB ([Protomaps: Downloads](https://docs.protomaps.com/basemaps/downloads))。Planetiler の OpenMapTiles プロファイルで 2026-03 版の planet から 81GB ([Planetiler Benchmarks](https://github.com/onthegomap/planetiler#benchmarks))。地形の Mapterhorn planet (z0〜12) は約 356GB ([download_urls.json](https://download.mapterhorn.com/download_urls.json))。
- 保存と転送の単価の例 (USD、2026-11-10 確認):
  - Cloudflare R2 (Standard): 保存 $0.015/GB-月、Class A 操作 $4.50/100 万、Class B 操作 (読み取り) $0.36/100 万、インターネットへの転送は無料。無料枠は月 10GB-月、Class A 100 万、Class B 1,000 万 ([R2 pricing](https://developers.cloudflare.com/r2/pricing/))。
  - Cloudflare Workers (z/x/y 変換を Workers でする場合): Paid プラン月 $5 で 1,000 万リクエストと 3,000 万 CPU ミリ秒を含み、超過は $0.30/100 万リクエスト、$0.02/100 万 CPU ミリ秒 ([Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/))。
  - AWS S3 Standard (東京): 保存 $0.025/GB-月 (最初の 50TB)、GET $0.0037/1 万リクエスト ([AWS Price List API](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/ap-northeast-1/index.json)、公開日 2026-11-09)。S3 から CloudFront への転送は無料 ([S3 pricing](https://aws.amazon.com/s3/pricing/))。
  - AWS CloudFront 従量課金: 日本向けの転送は最初の 1TB 無料、次の 9TB が $0.114/GB、HTTPS リクエスト $0.0120/1 万。米国・メキシコ・カナダは $0.085/GB、$0.0100/1 万。無料枠は毎月 1TB の転送と 1,000 万リクエスト ([CloudFront pay-as-you-go](https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/))。
  - AWS CloudFront 定額プラン (1 ディストリビューションあたり月額、超過料金なし): Free $0 (100 万リクエスト、100GB)、Pro $15 (1,000 万リクエスト、50TB)、Business $200 (1.25 億リクエスト、50TB)、Premium $1,000 (5 億リクエスト、50TB) ([CloudFront pricing](https://aws.amazon.com/cloudfront/pricing/))。
- 月 100 万 / 1,000 万 地図ロードの概算: 仮定は、1 ロードあたりタイル 20 リクエスト、タイルの平均 50KB (どちらも仮定で、画面サイズ、操作量、スキーマで大きく変わる)、保存は 120GB (Protomaps planet 1 本)、1TB = 1,000GB で計算、スタイル・グリフ・スプライトの通信は除く。キャッシュヒット率は 0% として、すべての読み取りがストレージに届く上限で見積もる。
  - 月 100 万ロード: 2,000 万リクエスト、転送 2,000 万 × 50KB = 1,000GB。
    - Cloudflare R2 + Workers: R2 保存 (120 − 10) × 0.015 = $1.65、R2 Class B (2,000 万 − 1,000 万) × 0.36 / 100 万 = $3.60、Workers $5 + (2,000 万 − 1,000 万) × 0.30 / 100 万 = $8.00 (CPU 時間の超過は含めない)。計 約 $13/月。
    - S3 (東京) + CloudFront 従量 (日本向け): 保存 120 × 0.025 = $3.00、S3 GET 2,000 万 × 0.0037 / 1 万 = $7.40、転送 1,000GB は無料枠内で $0、リクエスト (2,000 万 − 1,000 万) × 0.012 / 1 万 = $12.00。計 約 $22/月。z/x/y 変換の Lambda の費用は含めない。
    - CloudFront 定額: 2,000 万リクエストは Pro (1,000 万) を超えるので Business $200。
  - 月 1,000 万ロード: 2 億リクエスト、転送 10,000GB。
    - Cloudflare R2 + Workers: R2 保存 $1.65、R2 Class B 1.9 億 × 0.36 / 100 万 = $68.40、Workers $5 + 1.9 億 × 0.30 / 100 万 = $62.00。計 約 $132/月。
    - S3 (東京) + CloudFront 従量 (日本向け): 保存 $3.00、S3 GET 2 億 × 0.0037 / 1 万 = $74.00、転送 (10,000 − 1,000) × 0.114 = $1,026.00、リクエスト 1.9 億 × 0.012 / 1 万 = $228.00。計 約 $1,331/月。
    - CloudFront 定額: 2 億リクエストと 10TB は Premium $1,000 に収まる。
  - 実際はエッジキャッシュに当たった分の R2 / S3 の読み取りが減るので、上の値は上限に近い。人件費、生成用の計算機、監視の費用は含めない。
- 商用サービスとの損益分岐の求め方: 月間ロード数を L とし、商用サービスの月額を C(L) (無料枠と従量単価から計算)、自前配信の月額を S(L) = 固定費 (保存料、定額プラン、Workers 基本料) + 変動費 (L × 1 ロードあたりのリクエスト数 × リクエスト単価 + L × 1 ロードあたりの転送量 × 転送単価) + 運用の人件費 (データ更新、監視、障害対応の時間 × 時間単価) とおく。C(L) = S(L) となる L が損益分岐点である。上の概算のとおり自前配信の変動費は小さいことが多く、分岐点は人件費と、帰属表示やスキーマの作り込みなどの初期費用でほぼ決まる。1 ロードあたりのタイル数と平均サイズは、実際の画面で開発者ツールのネットワークタブを見て測った値を使う。

## 運用の負担

- データ更新の頻度と手順: OSM の planet は毎週公開される (現在の pbf は 89GB、[planet.openstreetmap.org](https://planet.openstreetmap.org/))。生成済みのタイルを使うなら、Protomaps は毎日 ([Downloads](https://docs.protomaps.com/basemaps/downloads))、OpenFreeMap は毎週 ([OpenFreeMap](https://openfreemap.org/)) 新しいビルドを出す。手順は、新しい PMTiles を取得または生成し、検査し、ストレージに別名で置いて配信側の参照を切り替え、CDN のキャッシュを無効化する。PMTiles を同じ名前で上書きすると、キャッシュに残った古い索引と新しい本体が混ざるおそれがあるので、版ごとに別名にするのが安全である (推測)。スタイルのパッケージとタイルのスキーマの版を合わせる必要がある (Protomaps の v4 ビルドは style v4.0.0 以降と互換、[Downloads](https://docs.protomaps.com/basemaps/downloads))。
- 監視と障害対応: 静的 PMTiles + CDN は常駐サーバーが無いので、監視対象は CDN と関数のエラー率、レイテンシ、請求額になる。Protomaps は 200ms 以下を速い、500ms 以上を遅いとしている ([Deploy](https://docs.protomaps.com/deploy/))。タイルサーバー型ではサーバーのプロセス、ディスク、PostGIS も監視対象に入る。いずれも SLA は自分で持つことになる。
- 帰属表示 (ODbL の要件): OSM 由来のタイルを表示するときは「OpenStreetMap」への帰属と、データが ODbL で使えることが分かる表示が要る。「OpenStreetMap」を openstreetmap.org/copyright へのリンクにする方法がある。インタラクティブな地図では地図の隅に表示するのが通例で、閉じる操作、地図の操作、または 5 秒後に畳んでよいが、利用者が探せばライセンス情報に辿り着けなければならない ([OSMF Attribution Guidelines](https://osmfoundation.org/wiki/Licence/Attribution_Guidelines))。OpenMapTiles スキーマを使う場合は「© OpenMapTiles」の表示も要る ([OpenMapTiles LICENSE.md](https://github.com/openmaptiles/openmaptiles/blob/master/LICENSE.md))。標高データを使うなら、その出典 (国土地理院、Copernicus など) の表示条件にも従う。

## 向いている場面

- 月間ロード数が多く、商用タイル API の従量課金が R2 や CloudFront の保存・転送の費用より明らかに高い。
- 閉域網、オフライン端末、外部通信の制限がある環境で地図を出す必要がある。
- ベースマップの中身 (地物の選び方、属性、ズームごとの出し分け) を自分で決めたい、または自前データと合わせたタイルを作りたい。
- 地図の表示に関する規約上の制約 (キャッシュ、オフライン保存、利用先) を避けたい。
- 更新頻度が週次や月次で足りる (最新の道路や店舗の反映を急がない)。

## 向いていない場面

- 表示回数が少なく、商用サービスの無料枠や低額プランで収まる。運用の人件費のほうが高くなる。
- 運用に割ける人がいない。データ更新、スタイルとスキーマの版合わせ、障害対応を自分で持つことになる。
- 最新の POI、交通情報、ストリートビュー、ルート検索など、タイル以外の機能を同じ品質で揃える必要がある。
- 日本の住所検索の精度が要件の中心にある。この文書で扱った OSS ジオコーダーの日本の住所への対応は限定的で、精度は未確認である。
- OSM のデータに無い、または薄い情報 (詳細な建物名、住所の網羅性など) を地図の主要な価値にしたい。

## 出典

- https://github.com/onthegomap/planetiler
- https://github.com/onthegomap/planetiler#features
- https://github.com/onthegomap/planetiler#benchmarks
- https://github.com/systemed/tilemaker
- https://github.com/systemed/tilemaker/blob/master/LICENCE.txt
- https://community.openstreetmap.org/t/tilemaker-3-0-creating-vector-tiles/108111
- https://github.com/openmaptiles/openmaptiles
- https://github.com/openmaptiles/openmaptiles/blob/master/LICENSE.md
- https://github.com/protomaps/basemaps
- https://github.com/protomaps/basemaps/blob/main/LICENSE.md
- https://github.com/protomaps/basemaps/blob/main/LICENSE_DATA.md
- https://github.com/protomaps/basemaps-assets
- https://docs.protomaps.com/basemaps/downloads
- https://docs.protomaps.com/deploy/
- https://github.com/protomaps/PMTiles/blob/main/LICENSE
- https://github.com/protomaps/PMTiles/tree/main/spec
- https://github.com/protomaps/PMTiles/tree/main/spec/v3
- https://github.com/protomaps/go-pmtiles
- https://openfreemap.org/
- https://github.com/hyperknot/openfreemap/blob/main/LICENSE.md
- https://data.maptiler.com/downloads/planet/
- https://maplibre.org/martin/
- https://github.com/maplibre/martin
- https://github.com/maptiler/tileserver-gl
- https://github.com/maptiler/tileserver-gl/blob/master/docs/config.rst
- https://github.com/maptiler/tileserver-gl/blob/master/LICENSE.md
- https://github.com/mapbox/vector-tile-spec/tree/master/2.1
- https://github.com/mapbox/mbtiles-spec/blob/master/1.3/spec.md
- https://github.com/maplibre/maplibre-tile-spec
- https://maplibre.org/maplibre-tile-spec/implementation-status/
- https://maplibre.org/maplibre-style-spec/sources/
- https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapOptions/
- https://maps.gsi.go.jp/development/demtile.html
- https://service.gsi.go.jp/kiban/app/
- https://github.com/mapterhorn/mapterhorn
- https://github.com/mapterhorn/mapterhorn/blob/main/source-catalog/jpdem1a/metadata.json
- https://github.com/mapterhorn/mapterhorn/blob/main/source-catalog/glo30/metadata.json
- https://mapterhorn.com/data-access
- https://mapterhorn.com/attribution
- https://download.mapterhorn.com/download_urls.json
- https://github.com/pelias/pelias
- https://github.com/pelias/documentation/blob/master/data-sources.md
- https://github.com/pelias/schema/pull/498
- https://github.com/pelias/api
- https://github.com/komoot/photon
- https://github.com/osm-search/Nominatim
- https://nominatim.org/release-docs/latest/admin/Installation/
- https://nominatim.org/release-docs/develop/customize/Query-Preprocessing/
- https://github.com/osm-search/Nominatim/blob/v5.3.3/src/nominatim_api/query_preprocessing/split_japanese_phrases.py
- https://developers.cloudflare.com/r2/pricing/
- https://developers.cloudflare.com/workers/platform/pricing/
- https://aws.amazon.com/s3/pricing/
- https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/ap-northeast-1/index.json
- https://aws.amazon.com/cloudfront/pricing/
- https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/
- https://planet.openstreetmap.org/
- https://osmfoundation.org/wiki/Licence/Attribution_Guidelines

## 未確認のこと

- OpenMapTiles (PostGIS + imposm の手順) で planet を生成するときの資源と時間: 公式 README に数字が無い。
- Protomaps basemaps の「modest computer で 2〜3 時間」の機械構成と、tilemaker 3.0 の「古いハードウェア」の具体的な構成: 公式の記述に無い。
- MapTiler が配布する planet の利用条件と価格: 今回は料金ページを確かめていない。
- Martin がスタイルからラスタタイルを描画できるか: 公式トップページと README に記述が見当たらなかった。
- Mapterhorn の利用規約、ホットリンクの可否、必要な帰属表示の文言: Data Access と Attribution のページから読み取れなかった (attribution.json は JSON として取得できなかった)。
- Pelias と Photon の日本の住所文字列に対する実際の精度、Pelias が使うデータ源の日本の住所の収録状況: 公式に評価の記述が無く、自分で計測もしていない。
- 1 ロードあたりのタイル数 (20) と平均サイズ (50KB) は仮定であり、公式の数字は無い。
- CloudFront の従量単価は公式ページを WebFetch で要約して読んだ値で、Price List API での照合はしていない。
