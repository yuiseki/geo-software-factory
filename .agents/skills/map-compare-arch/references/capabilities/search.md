# 検索 (ジオコーディング、POI 検索)

対象: 住所から座標、座標から住所、名称や種別での POI 検索

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |

## 3 つの型

この機能を実現する型は 3 つある: 外部の API、常駐する検索サーバー (Nominatim、Pelias、Photon など)、ファイルと関数 (DuckDB や SQLite の全文検索の索引を 1 ファイルで配り、関数かブラウザで引く)。

| 型 | 主なツール・サービス (版、ライセンス) | 保存の置き場所 | 計算の置き場所 | 表現 (応答の形式) | 出典 |
|---|---|---|---|---|---|
| 外部の API | 商用のジオコーディング API (例: Google Geocoding API、Mapbox Geocoding、HERE。提供元ごとの条件は map-compare-infra で扱う)、OpenStreetMap 財団が運営する公開の Nominatim、オープンデータを統合した国内の POI 検索 API の OpenPOI API (結果を保存して使える。条件は map-compare-infra の [search/openpoiapi](../../../map-compare-infra/references/search/openpoiapi.md))。公開の Nominatim は 1 アプリあたり毎秒 1 リクエストが絶対上限、結果のキャッシュが必須、クライアント側の入力補完 (autocomplete) は禁止、大量の一括ジオコーディングは推奨されない | 提供元のクラウド | 提供元のクラウド | JSON (GeoJSON を返すものもある) | https://operations.osmfoundation.org/policies/nominatim/ |
| 常駐するサーバー | Nominatim v5.3.3 (2026-10-15 JST、Python のコードは GPL-3.0 以降、osm2pgsql 用の Lua 設定は Apache-2.0、それ以外のファイルは GPLv2)、Photon 1.3.0 (2026-08-08 JST、Apache-2.0、OpenSearch ベースで組み込みサーバーか外部の OpenSearch 3.x を使う、Java 21 以上)、Pelias (MIT、api v7.11.0 は 2026-09-26 JST、Elasticsearch 7 系を推奨し 8 系も対応、住所解析に libpostal)。汎用の全文検索エンジンとして OpenSearch 3.9.0 (2026-09-30 JST、Apache-2.0) と Elasticsearch v9.5.6 (2026-11-02 JST、AGPL-3.0 と SSPL と Elastic License 2.0 の三択、x-pack は Elastic License 2.0 のみ) | サーバーのディスク上のデータベース (Nominatim は PostgreSQL + PostGIS、Photon と Pelias は OpenSearch か Elasticsearch の索引) | 常駐プロセス | JSON、GeoJSON | https://github.com/osm-search/Nominatim 、https://github.com/komoot/photon 、https://github.com/pelias/documentation/blob/master/requirements.md 、https://github.com/opensearch-project/OpenSearch 、https://github.com/elastic/elasticsearch/blob/main/LICENSE.txt |
| ファイルと関数 | DuckDB v2.0.0 (2026-10-21 JST、MIT) の fts 拡張 (MIT)、SQLite の FTS5 (SQLite 本体は public domain)、SQLite の公式 Wasm 版 @sqlite.org/sqlite-wasm 3.54.1-build1 (2026-10-19 JST、ラッパーは Apache-2.0、SQLite 本体は public domain)、DuckDB-Wasm v1.33.0 (2025-12-16 JST、MIT)、JS の索引ライブラリ FlexSearch (npm 0.8.212、Apache-2.0)。日本の住所に特化したものとして、デジタル庁の abr-geocoder 3.0.52 (2026-10-05 JST、MIT) が PostgreSQL から DuckDB のキャッシュファイルを作り、それを読む API サーバーと CLI を持つ | 1 ファイルの索引 (DuckDB、SQLite) を静的ホスティングかオブジェクトストレージ、関数のパッケージ、端末に置く | 関数 (サーバーレス) か、ブラウザやアプリの中 | 関数経由なら JSON。ブラウザ内なら JS のオブジェクト | https://duckdb.org/docs/2.0/core_extensions/full_text_search.html 、https://www.sqlite.org/fts5.html 、https://github.com/sqlite/sqlite-wasm 、https://github.com/duckdb/duckdb-wasm 、https://github.com/nextapps-de/flexsearch 、https://github.com/digital-go-jp/abr-geocoder |

## 置き場所ごとの実現手段

| 置き場所 | 実現手段 (ツール、形式、API) | 制約 (データの大きさ、メモリ、起動時間、更新) | 出典 |
|---|---|---|---|
| クラウド | Nominatim、Photon、Pelias を VM かコンテナで常駐させる。日本の住所なら abr-geocoder の API サーバー (`/geocode`、`/normalize`、実験的な `/reverse`)。索引ファイルを Lambda などの関数から引く方式もある | Nominatim の全球は 1 TB 以上のディスク、128 GB 以上の RAM を強く推奨、取り込みは NVMe で約 2.5 日、従来の SSD で 4〜5 日。Photon の全球は約 95 GB のディスク (年に約 10% 増)、64 GB 以上の RAM を推奨。Pelias の全球は 6 億件超で Elasticsearch に約 450 GB、36 コアの機械で構築に約 16 時間。abr-geocoder は全国データと住居表示・地番データに PostgreSQL が要り、DuckDB キャッシュの構築時メモリ上限は既定 8 GB。Lambda のメモリ上限は 10,240 MB | https://nominatim.org/release-docs/latest/admin/Installation/ 、https://github.com/komoot/photon 、https://github.com/pelias/documentation/blob/master/full_planet_considerations.md 、https://github.com/digital-go-jp/abr-geocoder 、https://github.com/digital-go-jp/abr-geocoder/blob/main/abrg/README.ja.md 、https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html |
| エッジ (CDN のエッジ関数、利用者の近くに置く小さなサーバー) | 小さな索引を関数に同梱するか、KV や R2 などのストアから引く (推測: 下の制約から、全国規模の索引をメモリに載せる方式は向かない) | Cloudflare Workers は isolate あたりメモリ 128 MB (JS ヒープと Wasm の確保を含む)、Worker の大きさは 64 MiB まで。公式文書は大きなデータを Worker のメモリに持たず KV、R2、D1 に置くよう勧めている | https://developers.cloudflare.com/workers/platform/limits/ |
| ブラウザ | sqlite-wasm で SQLite の FTS5 索引を引く (OPFS に置いて永続化できる VFS が複数ある)。DuckDB-Wasm でも fts 拡張が使え、HTTP 読み込みは JS で再実装した httpfs を使う。FlexSearch は IndexedDB に索引を永続化できる。住所の正規化はブラウザでも動く JS ライブラリがある (例: normalize-japanese-addresses、MIT、v3.1.3、住所データを Web API から取得する) | 索引ファイルをダウンロードする量と、端末のメモリ。DuckDB-Wasm の httpfs はブラウザのセキュリティ規則に従うのでネイティブ版と同じことはすべてはできない。browser/ の reference と合わせて読む | https://sqlite.org/wasm/doc/trunk/persistence.md 、https://duckdb.org/docs/2.0/clients/wasm/extensions.html 、https://github.com/nextapps-de/flexsearch 、https://github.com/geolonia/normalize-japanese-addresses |
| アプリ (ネイティブ、端末内) | 端末の SQLite (FTS5) か DuckDB に索引を入れて引く (推測: どちらも組み込み用のライブラリで、端末内に置ける) | 索引の大きさがアプリ配布や端末容量に効く (推測)。FTS5 の trigram は 3 文字未満の語では全文検索でヒットしない | https://www.sqlite.org/fts5.html |

## データの大きさの目安

国、都道府県、市区町村の範囲で、索引やファイルがどれくらいの大きさになるか。公式の記述か、測った条件つきで書く。

- Nominatim (全球): ディスク 1 TB 以上が必要 (完成したデータベースの大きさは公式文書に記載が無い)。出典: https://nominatim.org/release-docs/latest/admin/Installation/
- Photon (全球): 約 95 GB のディスク (2026 年時点)。配布されている全球のデータベースダンプ photon-db-planet-1.0-latest.tar.bz2 は bzip2 圧縮で 63,112,939,450 バイト (約 63 GB、Last-Modified 2026-11-03 19:25 JST、2026-11-10 に Content-Length を測定)。出典: https://github.com/komoot/photon 、https://download1.graphhopper.com/public/
- Photon (日本): photon-db-japan-1.0-latest.tar.bz2 は bzip2 圧縮で 1,310,013,218 バイト (約 1.3 GB、Last-Modified 2026-11-03 21:45 JST、同じ方法で測定)。展開後の大きさは測っていない。出典: https://download1.graphhopper.com/public/asia/japan/index.html
- Pelias (全球): Elasticsearch に約 450 GB、Elasticsearch には全体で 600 GB のディスクを用意する例が載っている。補助サービスでは、全球の SQLite DB に約 5 GB、libpostal のデータに約 4 GB。出典: https://github.com/pelias/documentation/blob/master/full_planet_considerations.md 、https://github.com/pelias/documentation/blob/master/requirements.md
- 都道府県、市区町村の範囲の索引の大きさは公式の記述が見つからず、測ってもいない (未確認のこと に移した)

## 判断を左右すること

- 更新頻度: 1 ファイルの索引は作り直して差し替える方式になる。DuckDB の fts 索引は既定では元の表が変わっても自動で更新されず、`incremental = 1` (識別子の列が NOT NULL か PRIMARY KEY であること) で挿入と削除をトリガーで反映するか、作り直す。Photon は新しいダンプに入れ替えるときにデータベースを丸ごと差し替える手順を README に載せている。アドレス・ベース・レジストリは自治体から更新情報を随時集めて提供するとしている。出典: https://duckdb.org/docs/2.0/core_extensions/full_text_search.html 、https://github.com/komoot/photon 、https://www.digital.go.jp/policies/base_registry_address
- 応答の速さ: 入力補完 (autocomplete) を出すなら打鍵ごとに問い合わせが飛ぶので、公開の Nominatim は使えない (クライアント側での実装を禁止)。自前の常駐サーバーかブラウザ内の索引が要る。Pelias の例では 8 CPU・32 GB RAM の機械 2 台で 250 RPS を返す構成が載っている。出典: https://operations.osmfoundation.org/policies/nominatim/ 、https://github.com/pelias/documentation/blob/master/full_planet_considerations.md
- オフラインで使いたいか: 端末内の SQLite か DuckDB、またはブラウザの sqlite-wasm と OPFS、FlexSearch と IndexedDB で索引を持てば通信なしで引ける。住所正規化ライブラリでも住所データを Web API から取るものはオフラインでは動かない (Node.js なら `file://` でローカルのデータを指せるものがある)。出典: https://sqlite.org/wasm/doc/trunk/persistence.md 、https://github.com/geolonia/normalize-japanese-addresses
- 日本語の分かち書き: 日本語は語を空白で区切らないので、全文検索の分かち書きが問題になる。DuckDB の fts 拡張は stemmer に日本語が無く (アラビア語、英語、ヒンディー語、タミル語など、porter を含む 27 種と none)、既定の ignore 正規表現 `(\\.|[^a-z])+` は英小文字以外を捨てるので、日本語にはこの既定のままでは効かない (推測: 事前に分かち書きして空白区切りにすれば使える)。SQLite FTS5 の既定の unicode61 は文字の連続を 1 トークンにするので、漢字かなの連なりは 1 語として扱われる。FTS5 の trigram tokenizer (SQLite 3.34.0 で追加) は 3 文字ずつに分けて部分一致を引けるが、3 文字未満の語は全文検索でヒットしない。OpenSearch と Elasticsearch は kuromoji (IPAdic 辞書の形態素解析) の analysis-kuromoji プラグインで日本語を分かち書きする。FlexSearch は CJK の文字セットに対応している。出典: https://duckdb.org/docs/2.0/core_extensions/full_text_search.html 、https://www.sqlite.org/fts5.html 、https://www.sqlite.org/releaselog/3_34_0.html 、https://docs.opensearch.org/latest/analyzers/tokenizers/kuromoji/ 、https://github.com/nextapps-de/flexsearch
- 日本の住所の表記ゆれ: 住所は全文検索だけでは引きにくく、先に正規化 (都道府県、市区町村、町字、番地への分解と表記の統一) をかけてから照合する構成が使われている。abr-geocoder は `/normalize` (ABR と照合しない表記ゆれの統一) と `/geocode` を分けて持つ。normalize-japanese-addresses は都道府県、市区町村、大字・丁目、街区符号・住居番号か地番のどこまで判別できたかを level で返す。出典: https://github.com/digital-go-jp/abr-geocoder/blob/main/abrg/README.ja.md 、https://github.com/geolonia/normalize-japanese-addresses
- 費用 (外部 API の課金単位、自前の計算と転送): 外部 API は多くがリクエスト数で課金する (提供元ごとの単価は map-compare-infra で扱う)。自前の常駐サーバーは全球規模だと上のとおり数百 GB〜1 TB のディスクと 64〜128 GB の RAM が目安で、負荷が無くても動かし続ける費用がかかる。1 ファイルの索引は保存と転送の費用だけで済むが、ブラウザで引く方式は索引のダウンロード量が利用者ごとにかかる (推測)

## ライセンス上の注意

コピーレフトのツール (GPL、AGPL など) と、データの継承条件 (ODbL など) を、組み込み、改変、配布、SaaS 提供のそれぞれで書く。

- Nominatim (Python は GPL-3.0 以降、それ以外の多くは GPLv2): 自社製品に組み込んで配る、または改変して配布する場合は、ソースを GPL で開示する義務が生じる。SaaS として HTTP で提供するだけなら GPL は配布にあたらないので開示義務は生じない (AGPL でないため)。Python 部分は GPLv2 でなく GPL-3.0 以降である点に注意する。出典: https://github.com/osm-search/Nominatim
- Elasticsearch: AGPL-3.0、SSPL、Elastic License 2.0 の三択で、x-pack 配下は Elastic License 2.0 のみ。AGPL-3.0 を選ぶと、改変したものをネットワーク越しに利用させる場合にもソース開示の義務が生じる。SSPL と Elastic License 2.0 は OSI 承認のオープンソースライセンスではなく、Elastic License 2.0 はマネージドサービスとして第三者に提供することを制限する (推測: 条項の詳細は https://www.elastic.co/licensing/elastic-license で確かめる)。Pelias は Elasticsearch を前提にするので、この条件を受ける。OpenSearch (Apache-2.0) と Photon (Apache-2.0) にはこの制約が無い。出典: https://github.com/elastic/elasticsearch/blob/main/LICENSE.txt
- Pelias (MIT)、Photon (Apache-2.0)、DuckDB と fts 拡張 (MIT)、DuckDB-Wasm (MIT)、SQLite (public domain)、sqlite-wasm のラッパー (Apache-2.0)、FlexSearch (Apache-2.0)、abr-geocoder (MIT)、normalize-japanese-addresses (MIT) は、著作権表示とライセンス文を残せば組み込み、改変、配布、SaaS 提供ができる。sqlite-wasm は生成された Wasm に第三者の告知が含まれると LICENSE に書いている
- OSM データ (ODbL): OSMF のジオコーディングのガイドラインでは、ジオコーディングの結果は個々には非実質的な抽出として扱い、Produced Work とはしない。OSM をほとんど改変せずに使い、結果から OSM の全体か実質的な部分を作り直さない限り share-alike は生じない。改変した OSM データベースでジオコーダーを動かすと、その改変データベースが share-alike の対象になる。結果を独自データと一緒に保存しても、OSM の実質的な部分を集めない限り独自データには及ばない。公に使うジオコーダーは share-alike の有無にかかわらず OpenStreetMap の帰属表示が要る。出典: https://osmfoundation.org/wiki/Licence/Community_Guidelines/Geocoding_-_Guideline 、https://opendatacommons.org/licenses/odbl/summary/
- アドレス・ベース・レジストリ (ABR): 権利表記が無い限り公共データ利用規約 (第 1.0 版) (PDL1.0) が適用され、出典の記載と、編集・加工したことと加工の主体の記載が要る。加工したものを加工していない公的情報のように公表、利用してはならない。地番マスターと地番マスター位置参照には登記所備付地図データ利用規約も適用される。出典: https://www.digital.go.jp/policies/base_registry_address_tos

## 出典

- https://operations.osmfoundation.org/policies/nominatim/ (公開 Nominatim の毎秒 1 リクエスト、キャッシュ必須、autocomplete 禁止、一括の扱い)
- https://github.com/osm-search/Nominatim (版、ライセンスの区分)
- https://nominatim.org/release-docs/latest/admin/Installation/ (RAM、ディスク、取り込み時間、PostgreSQL と PostGIS の版)
- https://github.com/komoot/photon (版、Apache-2.0、OpenSearch、Java 21、全球 95 GB、RAM 64 GB、ダンプの入れ替え)
- https://download1.graphhopper.com/public/ と https://download1.graphhopper.com/public/asia/japan/index.html (Photon のダンプ一覧、2026-11-10 に Content-Length を測定)
- https://github.com/pelias/documentation/blob/master/requirements.md と https://github.com/pelias/documentation/blob/master/full_planet_considerations.md (Elasticsearch の版、libpostal、全球の件数と大きさ、構築時間、構成例)
- https://github.com/pelias/api/releases (v7.11.0)
- https://github.com/opensearch-project/OpenSearch/releases (3.9.0) と https://docs.opensearch.org/latest/analyzers/tokenizers/kuromoji/ (kuromoji と analysis-kuromoji プラグイン)
- https://github.com/elastic/elasticsearch/blob/main/LICENSE.txt (三択のライセンス、x-pack) と https://github.com/elastic/elasticsearch/releases (v9.5.6)
- https://duckdb.org/docs/2.0/core_extensions/full_text_search.html (create_fts_index の引数、stemmer の一覧、ignore の既定、自動更新されないこと、incremental)
- https://duckdb.org/docs/2.0/clients/wasm/extensions.html (DuckDB-Wasm で使える拡張に fts があること、httpfs の JS 再実装)
- https://github.com/duckdb/duckdb/releases (v2.0.0) と https://github.com/duckdb/duckdb-wasm/releases (v1.33.0)
- https://www.sqlite.org/fts5.html (tokenizer の種類、trigram の 3 文字未満の扱い、unicode61 のトークン規則) と https://www.sqlite.org/releaselog/3_34_0.html (trigram の追加)
- https://github.com/sqlite/sqlite-wasm (版、LICENSE) と https://sqlite.org/wasm/doc/trunk/persistence.md (OPFS の VFS)
- https://github.com/nextapps-de/flexsearch (Apache-2.0、CJK 対応、IndexedDB などへの永続化)
- https://github.com/digital-go-jp/abr-geocoder 、https://github.com/digital-go-jp/abr-geocoder/blob/main/abrg/README.ja.md (版、MIT、PostgreSQL と DuckDB キャッシュの構成、エンドポイント、構築時メモリ)
- https://www.digital.go.jp/policies/base_registry_address (ABR の概要、町字の正式版公開、随時更新、データのダウンロード先 https://dataset.address-br.digital.go.jp/)
- https://www.digital.go.jp/policies/base_registry_address_tos (PDL1.0、出典と加工の記載)
- https://github.com/geolonia/normalize-japanese-addresses (MIT、v3.1.3、level の意味、住所データの取得先、Node.js での `file://`)
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Geocoding_-_Guideline (ジオコーディング結果と ODbL)
- https://opendatacommons.org/licenses/odbl/summary/ (ODbL の 3 条件)
- https://developers.cloudflare.com/workers/platform/limits/ (Workers のメモリ 128 MB、Worker の大きさ 64 MiB)
- https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html (Lambda のメモリ上限 10,240 MB)

## 未確認のこと

- 日本全国、都道府県、市区町村の範囲で、SQLite FTS5 や DuckDB fts の索引ファイルがどれくらいの大きさになるか (公式の記述が無く、測っていない)
- abr-geocoder の全国データの PostgreSQL と DuckDB キャッシュの大きさ、構築時間 (README に記載が無い)
- Photon の日本のダンプを展開した後の大きさと必要な RAM
- Nominatim の日本だけを取り込んだときのディスクと RAM
- Photon のダンプ名の「1.0」が Photon 1.3.0 のデータベース形式に対応するか (推測で 1.x 系向けと読んだが確かめていない)
- Elastic License 2.0 の条項の正確な文言 (このファイルでは条文を読んでいない)
- アドレス・ベース・レジストリの更新の周期 (公式ページは「随時」とだけ書く) と、町字以外 (住居表示、地番) が試験公開版から正式版になる時期
- DuckDB fts で日本語を事前に分かち書きして入れたときの実用性 (推測で書いた)
- 外部 API の課金単位と単価 (map-compare-infra で扱う)
