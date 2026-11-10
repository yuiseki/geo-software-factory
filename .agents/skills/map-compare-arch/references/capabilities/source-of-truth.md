# 正本と更新 (SSoT)

対象: 地物を作成、更新、削除する機能と、その正本 (Single Source of Truth) をどこにどう持つか。強い整合性とトランザクション (ACID、同時編集の排他、履歴) を、読み出しの速さや置き場所の自由より優先する場合を含む。正本から、配信用の成果物 (PMTiles、検索索引、ルート用グラフ、GeoParquet) を作って配る流れも扱う

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 確かめた版 | PostgreSQL 18.6 (2026-08-13 公開、19 は RC 1 が 2026-10-15 に出た段階)、PostGIS 3.7.0 (2026-10-30 公開)、MongoDB マニュアル 9.0 (Current)、Debezium 3.7、SpatiaLite 5.1.0 (2023-08-04)、GeoPackage 1.4.0 (OGC 12-128r19)、Orion-LD 1.12.0 (2026-01) |

## 正本と配信用の成果物を分ける考え方

書き込みは、整合性の強い 1 か所 (正本) に集める。読み出しは、正本から作った成果物 (PMTiles、検索索引、ルート用グラフ、GeoParquet など) をオブジェクトストレージ、CDN、エッジ、ブラウザに配って行う。成果物は正本に対して遅れる (結果整合) ことを受け入れ、その代わりに読み出しの速さ、配る先の自由、正本の負荷の小ささを得る。この分け方は CQRS (コマンドとクエリの責務分離) と同じ考え方である (推測: 用語の対応づけは筆者の整理)。

成果物の遅れを受け入れられず、読み出しも正本から直接行うべきなのは次の場合である (推測: 設計上の整理であり、特定の出典はない)。

- 書いた本人がすぐに結果を確かめる画面 (編集画面、保存直後の詳細表示)。少なくとも書いた本人には自分の書き込みが見える (read-your-writes) 必要がある
- 読んだ値をもとに次の書き込みを決める処理 (在庫や予約の残りを見て確保する、台帳の現在値を見て更新する)。古い値を読むと二重確保や上書きが起きる
- 権限によって見える行が変わるデータ。成果物を全員に同じ形で配ると、見せてはいけない行も届く
- 監査や法定の記録として「その時点の正しい値」を示す必要がある照会

## ファイルで済むか、DB が要るか

### 置き場所の段階

| 段階 | 中身 | 空間索引と空間演算 | 書き込みの整合性 | 出典 |
|---|---|---|---|---|
| (a) ファイルだけ、DB なし | GeoJSON、PMTiles、GeoParquet などをオブジェクトストレージや静的ホスティングに置き、クライアントが取得して絞り込む | ファイル形式の内部構造 (PMTiles のタイル索引など) に依存する。任意の空間演算はクライアント側で行う | オブジェクト単位の上書き。条件付き書き込み (後述) を使えばオブジェクト単位の楽観的排他はできる | https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html |
| (b) サーバーレス、管理型の DB サービス | PostgreSQL 系のサービスで PostGIS 拡張を有効にできるものがある (例: Supabase、Neon はともに `CREATE EXTENSION postgis` を文書化)。SQLite 系のエッジ DB (Cloudflare D1) は文書化された拡張が FTS5、JSON、数学関数のみで、空間拡張は文書にない | PostGIS 系は PostgreSQL + PostGIS と同じ。D1 は空間索引の記載がない | PostGIS 系は PostgreSQL と同じ。D1 は 1 データベースが単一スレッドでクエリを 1 つずつ処理する | https://supabase.com/docs/guides/database/extensions/postgis 、 https://neon.com/docs/extensions/postgis 、 https://developers.cloudflare.com/d1/sql-api/sql-statements/ 、 https://developers.cloudflare.com/d1/platform/limits/ |
| (c) 管理型 DB を自分で運用し、自前の API を置く | Amazon Aurora PostgreSQL や Cloud SQL for PostgreSQL に PostGIS を入れ、その前に自前の API サーバーを置く。Cloud SQL は全メジャーバージョンで PostGIS を提供し、PostgreSQL 18 では PostGIS 3.6.0 | PostGIS と同じ。拡張の版は事業者が提供するものに限られ、PostgreSQL 本体を上げても PostGIS は自動では上がらない | PostgreSQL と同じ | https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Appendix.PostgreSQL.CommonDBATasks.PostGIS.html 、 https://docs.cloud.google.com/sql/docs/postgres/extensions |
| (d) イベント、ストリーム指向の置き場所 | 機械 (センサー、車両) からの高頻度の書き込みと購読を扱う。FIWARE の Context Broker 実装 (Orion: NGSIv2、AGPL-3.0。Orion-LD: NGSI-LD、MongoDB 4.2 以上が必要、AGPL-3.0、履歴は TRoE で PostgreSQL に保存。Scorpio: NGSI-LD、PostgreSQL + PostGIS を使う、BSD-3-Clause) や、MQTT (OASIS 標準 v5.0、2019-03-07。QoS 0 は最大 1 回、1 は最低 1 回、2 はちょうど 1 回) と時系列 DB の組み合わせ | 実装による。Scorpio は PostGIS を使う | 実装による。MQTT は配送保証 (QoS) を定めるが、複数の値をまとめて原子的に書く仕組みではない (推測) | https://github.com/telefonicaid/fiware-orion 、 https://github.com/FIWARE/context.Orion-LD 、 https://github.com/ScorpioBroker/ScorpioBroker 、 https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html |

### ファイルから DB へ移る理由

各項目は、ファイルで何が足りず、DB で何が得られるかを書く。

- 同じものへの同時の書き込み: ファイルを丸ごと置き換える方式では、条件なしだと後から書いた方が勝ち (last-write-wins)、先の変更が黙って消える。S3 は条件なしで同じキーに書くと上書きする。DB では行単位のロック、トランザクションの分離レベル (PostgreSQL の SERIALIZABLE は直列実行と同じ結果を保証し、衝突時は SQLSTATE 40001 で失敗させて再試行させる)、版番号による楽観的排他 (OSM API の 409 Conflict のような) を行単位で持てる。出典: https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html 、 https://www.postgresql.org/docs/current/transaction-iso.html
- データ量と問い合わせの複雑さ: ファイル方式ではクライアントが必要な部分を取得して絞り込む。データがクライアントに落とせる量を超える、または絞り込み条件が属性と空間の組み合わせで事前にファイルを分けておけない場合、DB の索引 (PostGIS の GiST による R-Tree など) でサーバー側で絞る必要がある (推測: 境界の量は端末と回線による)。出典: https://postgis.net/docs/manual-3.6/using_postgis_dbmanagement.html
- 1 件だけの部分更新: ファイルは 1 件を直すにもファイル全体 (またはタイル群) を作り直して置き換える。DB は該当行だけを UPDATE できる (推測: 形式による一般的な性質)
- サーバー側で強制するアクセス制御: ファイルは取得できた人に中身がすべて見える。オブジェクト単位では署名付き URL で期限付きの許可を出せるが、ファイルの中の行ごとには制御できない。PostgreSQL の行レベルセキュリティ (RLS) は利用者ごとに見える行、書ける行を DB 側で制限し、方針がなければ既定で全行拒否になる。出典: https://www.postgresql.org/docs/current/ddl-rowsecurity.html 、 https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html
- 参照の整合性: 地物と台帳、地物同士の参照 (外部キー) を DB は書き込み時に検査できる。ファイルには検査する主体がない (推測)。なお PostgreSQL の参照整合性の検査は RLS を迂回する。出典: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- サーバー側での集計: 地域ごとの件数や合計を、明細を配らずに返せる。ファイル方式では明細をクライアントに渡すことになる (推測)
- 監査と法定の履歴: 誰がいつ何を変えたかを、トランザクションと同じ単位で記録できる。ファイルではオブジェクトの版 (S3 のバージョニング) は残せるが、版ごとに全体を保存し差分ではない。また「誰が」は別途ログで持つ必要がある (推測: アクセスログとの突き合わせが要る)。出典: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html
- 即時の反映: ファイル方式ではクライアントが定期的に取り直す (ポーリング)。DB には変更通知がある。PostgreSQL の LISTEN/NOTIFY はコミット時にのみ届き、ペイロードは既定で 8000 バイト未満。MongoDB の change streams は過半数のメンバーに永続化された変更だけを通知し、再開トークンで続きから受け取れる (oplog に残っている範囲に限る)。出典: https://www.postgresql.org/docs/current/sql-notify.html 、 https://www.mongodb.com/docs/manual/changestreams/
- 業務ルールと不正対策のサーバー側での強制: 位置情報ゲーム、得点、ポイント、決済のように、ブラウザやアプリの判定を信用できないもの。ブラウザは利用者の手元にあり書き換えられるので、判定と記録はサーバー側の正本で行う必要がある (推測: 一般的なセキュリティ原則)。ファイルを直接書かせる方式では、署名付き URL で書き込み先を限っても中身の正しさは検査できない (推測)

### 境界を緩める事実 (ファイルでもできること)

- 条件付き書き込みによる楽観的排他: S3 は PutObject、CompleteMultipartUpload、CopyObject で `If-None-Match: *` (同名がなければ書く) と `If-Match: <ETag>` (ETag が一致すれば書く) を受け付け、条件が満たされなければ 412 Precondition Failed を返す。同じ名前への条件付き書き込みが重なった場合は先に終わった方が成功する。SigV4 署名が必要で、バケットポリシーで条件付き書き込みを強制できる。出典: https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html
- Cloudflare R2 は Workers API の `put()` に `onlyIf` (etagMatches、etagDoesNotMatch、uploadedBefore、uploadedAfter) を渡せ、条件を満たさないと `null` を返して保存しない。出典: https://developers.cloudflare.com/r2/api/workers/workers-api-reference/
- Google Cloud Storage は `ifGenerationMatch` (XML API では `x-goog-if-generation-match`) と `ifMetagenerationMatch` の事前条件を持ち、失敗時は 412 を返す。世代番号 0 を指定すると、同名の現行オブジェクトがない場合だけ作成する。公式文書が楽観的排他の手順として説明している。XML API のマルチパートアップロードでは事前条件を使えない。出典: https://docs.cloud.google.com/storage/docs/request-preconditions
- オブジェクトの版による履歴: S3 のバージョニングはすべての版を保持し、削除は削除マーカーになる。一度有効にすると無効には戻せず、停止のみできる。版ごとにオブジェクト全体が課金対象になる。出典: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html
- 署名付き URL によるオブジェクト単位のアクセス制御: S3 は CLI、SDK で最長 7 日、作成者の資格情報が一時的ならその期限で切れる。URL は持っている人が使える持参人トークンである。R2 の署名付き URL は GET、HEAD、PUT、DELETE に対応し、最長 604,800 秒 (7 日)。出典: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html 、 https://developers.cloudflare.com/r2/api/s3/presigned-urls/
- これらで得られるのはオブジェクト単位の排他、履歴、アクセス制御までであり、行単位の制御、複数オブジェクトをまたぐトランザクション、参照整合性は得られない (推測: 上記の文書に複数オブジェクトの原子的更新の記載はない)

### 囲い込み (ロックイン)

- Supabase の RLS の補助関数 `auth.uid()` と `auth.jwt()` は Supabase Auth を使う場合の Supabase 独自の関数で、Supabase の `auth` スキーマにある。RLS そのものは PostgreSQL の機能である。出典: https://supabase.com/docs/guides/database/postgres/row-level-security
- 逃げ道になる標準の部品: PostgreSQL 標準の RLS (`CREATE POLICY`、`ENABLE ROW LEVEL SECURITY`) と、OSS の PostgREST (MIT ライセンス) はリクエストごとに JWT のクレームを `request.jwt.claims` として設定し、SQL から `current_setting('request.jwt.claims', true)` で読める。これを使えば、特定事業者の関数に依存しないポリシーを書ける (推測: 移行時の書き換えの量は個別の実装による)。出典: https://www.postgresql.org/docs/current/ddl-rowsecurity.html 、 https://docs.postgrest.org/en/stable/references/transactions.html 、 https://github.com/PostgREST/postgrest
- 認証基盤と DB の結びつきが強いほど、DB だけを移しても認証とポリシーの書き換えが残る (推測)

## 正本の候補

| 候補 | 整合性とトランザクション (分離レベル、複数文書・複数行) | 空間索引と空間演算 | 書き込みの規模と複製 | ライセンス | 出典 |
|---|---|---|---|---|---|
| PostgreSQL + PostGIS | 複数行、複数テーブルの ACID トランザクション。既定は Read Committed。Read Uncommitted を指定しても Read Committed として動く。Repeatable Read (スナップショット分離)、Serializable (SSI、直列実行と同じ結果を保証) を選べる。Repeatable Read 以上では直列化の失敗 (SQLSTATE 40001) に備えてトランザクション全体を再試行する必要がある | geometry (平面) と geography (球面、測定はメートル) の型。索引は GiST 上の R-Tree (標準)、SP-GiST (四分木、k-d 木、kNN 非対応)、BRIN (空間的に整列しほぼ更新されない大表向け、小さく速く作れる)。PostGIS は数千の関数を追加する | 書き込みは 1 台の主ノード。論理レプリケーションは publish/subscribe で表単位に変更を送り、1 つの購読内ではトランザクションの順序を保つ。DDL、シーケンス値、ラージオブジェクトは複製されず、ビューやマテビューは対象外 | PostgreSQL は PostgreSQL License (BSD、MIT に近い寛容なライセンス)。PostGIS は GPL-2.0-or-later (一部のファイルは MIT 等、依存の GEOS は LGPL) | https://www.postgresql.org/docs/current/transaction-iso.html 、 https://postgis.net/docs/manual-3.6/using_postgis_dbmanagement.html 、 https://www.postgresql.org/docs/current/logical-replication.html 、 https://www.postgresql.org/docs/current/logical-replication-restrictions.html 、 https://www.postgresql.org/about/licence/ 、 https://raw.githubusercontent.com/postgis/postgis/master/LICENSE.TXT |
| MongoDB | 複数文書トランザクションは全ての現行版で使え、FCV はレプリカセットで 4.0 以上、シャードクラスタで 4.2 以上。読み取り懸念は local、majority、snapshot (シャードをまたいで同期したスナップショットは snapshot のみ)。書き込み懸念はコミット時に適用され、5.0 以降のクライアント既定は `w: "majority"`。`w: 1` のコミットはフェイルオーバーで巻き戻りうる。トランザクションは既定で 1 分未満で終える必要がある (`transactionLifetimeLimitSeconds`)。公式文書は、トランザクションは良いスキーマ設計の代わりではなく埋め込み型のモデルを勧めている | 2dsphere 索引 (球面) と 2d 索引 (平面)。問い合わせは `$geoIntersects`、`$geoWithin`、`$near`、`$nearSphere` と集計の `$geoNear` のみで、バッファ、結合、面積などの幾何処理は文書にない。地理索引は問い合わせをカバーできず、シャードキーにできない。1 文書あたりの索引キー数は既定 100,000 が上限。半球を超える多角形は、単一リングで独自 CRS を指定した場合を除き補集合として扱われる。辺や頂点を共有するだけの接触は一致が保証されない。8.3 以降は 2dsphere 索引の版 4 が既定 | レプリカセットとシャーディング。トランザクションを含む読み取りは primary から | Community Server は 2018-10-16 以降の版が SSPL (OSI 非承認)。それより前は AGPL-3.0 | https://www.mongodb.com/docs/manual/core/transactions/ 、 https://www.mongodb.com/docs/manual/core/transactions-production-consideration/ 、 https://www.mongodb.com/docs/manual/core/indexes/index-types/geospatial/2dsphere/ 、 https://www.mongodb.com/docs/manual/core/indexes/index-types/geospatial/restrictions/ 、 https://www.mongodb.com/docs/manual/reference/operator/query/geoIntersects/ 、 https://www.mongodb.com/docs/manual/geospatial-queries/ 、 https://www.mongodb.com/legal/licensing/server-side-public-license/faq |
| CockroachDB (分散 SQL) | 既定は SERIALIZABLE。READ COMMITTED も選べる (クラスタ設定で無効なら SERIALIZABLE に上げられる)。直列化できないと 40001 で失敗し、結果が 16 KiB 以下の単文、一括送信なら自動で再試行、それ以外はクライアント側の再試行が要る | geometry の型と WKT、WKB、GeoJSON。PostGIS 関数は一部のみ対応。空間索引は S2 による空間の分割 (四分木、ヒルベルト曲線) を転置索引 (GIN) に格納する方式で、PostGIS の R-Tree と違う。kNN 問い合わせ、独自 SRID、`spatial_ref_sys` への INSERT (そのため `ogr2ogr -f PostgreSQL`) は非対応。空間型は既定の主キーや一意索引に使えない | 水平分散 (S2 の分割は分散に向くと文書が説明) | 24.3.0 の公開日以降の版は CockroachDB Software License (OSI 承認の OSS ではない)。年商 1,000 万ドル未満の事業者は Enterprise Free を毎年更新で使えるが、政府機関は対象外。Free と Trial はテレメトリ送信が必須で、7 日止まると同時トランザクション 5 に制限される | https://docs.cockroachlabs.com/docs/stable/transactions 、 https://docs.cockroachlabs.com/docs/stable/spatial-data-overview 、 https://docs.cockroachlabs.com/docs/stable/spatial-indexes 、 https://docs.cockroachlabs.com/docs/stable/licensing-faqs |
| クラウドの管理型 PostgreSQL (Amazon Aurora PostgreSQL、Cloud SQL for PostgreSQL、Supabase、Neon など) | PostgreSQL と同じ | PostGIS 拡張を有効にできる。Cloud SQL の PostGIS 版は PostgreSQL 13〜17 で 3.5.2、18 で 3.6.0。Aurora は `rds_superuser` 権限で `CREATE EXTENSION postgis`。拡張の更新は手動 | 事業者の複製機能による | 本体は PostgreSQL と PostGIS のライセンス。サービス自体は各社の利用規約 | https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Appendix.PostgreSQL.CommonDBATasks.PostGIS.html 、 https://docs.cloud.google.com/sql/docs/postgres/extensions 、 https://supabase.com/docs/guides/database/extensions/postgis 、 https://neon.com/docs/extensions/postgis |
| Spanner (GoogleSQL) | (本ファイルでは未確認) | GoogleSQL のデータ型一覧に GEOGRAPHY 型がない。空間の正本にするなら、空間の判定はアプリ側か別の索引で行うことになる (推測) | (未確認) | 商用サービス | https://docs.cloud.google.com/spanner/docs/data-types |
| SQLite + SpatiaLite、GeoPackage (1 ファイルの正本) | SQLite のトランザクションは ACID だが、書き込みは同時に 1 つだけ (RESERVED ロックを持てるのは 1 プロセス、取れなければ SQLITE_BUSY)。WAL モードでも書き込みは 1 つずつ (推測: WAL の文書は未読) | SpatiaLite は SQLite の空間拡張。GeoPackage は SQLite のファイルにベクタ地物、タイル、属性を入れる OGC 標準 (1.4.0、12-128r19) で、R-tree 空間索引の拡張を持つ | 1 ファイルなので配布や持ち出しが簡単 (現地調査用)。多人数の同時書き込みには向かない | SpatiaLite 5.1.0 は MPL 1.1、GPL-2.0-or-later、LGPL-2.1-or-later から選べる三重ライセンス。SQLite 本体はパブリックドメイン (未確認) | https://www.sqlite.org/lockingv3.html 、 https://www.gaia-gis.it/fossil/libspatialite/home 、 https://www.ogc.org/standards/geopackage/ 、 https://www.geopackage.org/spec/ |
| OSM 型の編集 API (OSM API v0.6) | 各要素 (node、way、relation) が版番号を持ち、送った版がサーバーの現在の版と違えば 409 Conflict を返す楽観的排他。差分のアップロード (osmChange) は 1 トランザクションで全部か無しかで適用される。一方で changeset 自体は原子的ではなく、閉じる前に変更が他人に見える。1 changeset は最大 10,000 要素 | (API の範囲外。OSM の公式サーバーは別途データベースを持つ) | 多数の編集者が非同期に編集する前提 | (API 仕様。データは ODbL) (ODbL は未確認) | https://wiki.openstreetmap.org/wiki/API_v0.6 |

### 無料枠で正本を置くとき (2026-11-10 確認)

- Cloudflare D1 の Free: 1 日に読み 500 万行、書き 10 万行、1 DB 500 MB。超えるとエラーを返すだけで課金されない (https://developers.cloudflare.com/d1/platform/pricing/)。空間の型と索引は無いので、点の数が少なければ距離の計算はブラウザで行う
- Supabase の Free: データベース 500 MB、認証の MAU 50,000。1 週間使われないとプロジェクトが止まる (https://supabase.com/pricing)。旅行のように使う時期が飛び飛びのサービスでは、使わない間に公開ページが止まる

## 置き場所ごとの書き込み

| 置き場所 | 実現手段 | 整合性で失うもの | 出典 |
|---|---|---|---|
| クラウド | 正本の DB (PostgreSQL + PostGIS、MongoDB、分散 SQL) に、自前の API またはサーバー経由で書く | 失うものは少ない。代わりに書き込みは 1 リージョン (または分散 SQL の合意) を往復するので遅延が増える (推測)。Serializable では 40001 の再試行の実装が要る | https://www.postgresql.org/docs/current/transaction-iso.html |
| エッジ | Cloudflare D1 の読み取り複製: 書き込みは常に主 DB に転送され、複製は読み取りのみ。Sessions API を使うと 1 セッション内で逐次一貫性 (自分の書き込みが後の読み取りで見える) が得られ、ブックマークを渡せば別のリクエストでも少なくともその状態から始められる。`withSession('first-primary')` は最初の問い合わせを主 DB に送る。Sessions API を使わなければ全部が主 DB で動く。`batch()` は SQL トランザクションとして全体が巻き戻る。1 DB は単一スレッドで最大 10 GB (有料プラン)。Turso の組み込み複製 (libSQL、MIT): 既定では書き込みはリモートの主 DB に送られ、書いた複製は即座に見えるが、他の複製は `sync()` か定期同期まで遅れる。`offline: true` でローカル書き込みも可能 | セッションをまたぐと、ブックマークを引き継がない限り古い複製を読む可能性がある。Turso では他の複製の読み取りが同期間隔だけ遅れる。D1 に空間索引の記載はない | https://developers.cloudflare.com/d1/best-practices/read-replication/ 、 https://developers.cloudflare.com/d1/worker-api/d1-database/ 、 https://developers.cloudflare.com/d1/platform/limits/ 、 https://docs.turso.tech/features/embedded-replicas/introduction 、 https://github.com/tursodatabase/libsql |
| ブラウザ・アプリ | ローカルファーストの同期エンジン: Electric (Apache-2.0) は Postgres から Shape 単位でクライアントへ配る読み取り専用の同期で、書き込みは自前の API を通す。PowerSync (サービスのリポジトリは Apache-2.0) はアプリ内の SQLite を Postgres、MongoDB、MySQL (Beta) などと同期し、ローカルの変更は送信キューから自前の API に順に送る。競合はサーバーが決める方式で、最も単純な構成ではフィールド単位の後勝ち、削除は勝つ。API は同じ操作が複数回届いても安全 (冪等) に作る必要がある。Zero (rocicorp、Apache-2.0) は Postgres を論理レプリケーションで zero-cache に複製し、ミューテーターをクライアントで楽観的に実行した後、サーバーの API が Postgres に対して本番の書き込みを行う。CRDT: Yjs (MIT、Map、Array、Text などの共有型、オフライン編集) と Automerge (MIT、JSON に似た CRDT、Rust の中核を WebAssembly で JS に提供)。どちらも幾何専用の型は持たない。GIS の現地同期: Mergin Maps の geodiff (MIT) は GeoPackage と PostGIS の差分を取り、差分同士を rebase して統合し、自動で解けない衝突は別の衝突ファイルに書き出す。QFieldCloud (MIT) は QGIS と QField の間でプロジェクトとデータを同期する | オフライン中の書き込みは正本に届くまで他人に見えず、届いた時点でサーバーに拒否されうる。後勝ちでは同じフィールドへの先の変更が消える。CRDT は自動で統合するが、統合結果が業務ルール (例: 同じ枠の二重予約禁止) を満たす保証はない (推測)。地物の幾何を CRDT で扱うには座標列を共有型に載せる設計が要る (推測) | https://electric.ax/docs/intro 、 https://github.com/electric-sql/electric 、 https://docs.powersync.com/intro/powersync-overview 、 https://docs.powersync.com/usage/lifecycle-maintenance/handling-update-conflicts 、 https://raw.githubusercontent.com/powersync-ja/powersync-service/main/LICENSE 、 https://zero.rocicorp.dev/llms.txt 、 https://github.com/rocicorp/mono 、 https://github.com/yjs/yjs 、 https://github.com/automerge/automerge 、 https://github.com/MerginMaps/geodiff 、 https://merginmaps.com/docs/manage/missing-data/ 、 https://github.com/opengisch/QFieldCloud |

## 正本から成果物への反映

- 変更の検知 (CDC、トリガー、変更ストリーム): PostgreSQL の論理デコーディングを使う Debezium (3.7、Apache-2.0) の PostgreSQL コネクタは、PostgreSQL 10 以降に標準である `pgoutput` を使い、初回は全スキーマの一貫したスナップショットを取り、以後は WAL を最後の位置から読み続ける。レプリケーションスロットは Debezium が止まっている間も必要な WAL を保持する。スロットを作り直すと、飛ばしたイベントが失われる。一部のスナップショット方式では重複したイベントが出うる。PostgreSQL の論理レプリケーションで別の DB に複製して、そちらで成果物を作ることもできる。MongoDB の change streams はレプリカセットかシャードクラスタで使え、過半数に永続化された変更だけを通知し、再開トークン (`resumeAfter`、`startAfter`) で続きから読めるが、oplog から消えた範囲には戻れない。時系列コレクションは非対応。軽い通知には PostgreSQL の LISTEN/NOTIFY (コミット時のみ配送、8000 バイト未満) も使える。出典: https://debezium.io/documentation/reference/stable/connectors/postgresql.html 、 https://github.com/debezium/debezium 、 https://www.postgresql.org/docs/current/logical-replication.html 、 https://www.mongodb.com/docs/manual/changestreams/ 、 https://www.postgresql.org/docs/current/sql-notify.html
- 成果物の作り直し (全体、差分、タイル単位の無効化): (推測: 以下は設計上の整理で、個別の出典はない) 変更イベントから影響する範囲 (変わった地物の新旧の外接矩形) を求め、その範囲にかかるタイルだけを作り直す、または検索索引の該当文書だけを更新するのが差分方式である。PMTiles や GeoParquet のような 1 ファイルの成果物は部分書き換えに向かないので、一定間隔でファイル全体を作り直して差し替えることが多い。ルート用グラフは前処理の重い方式だと全体の作り直しになりやすい。CDN のキャッシュは、ファイル名に版を入れて差し替える方式にすると無効化の漏れが起きにくい
- 反映の遅れの目安と、利用者への見せ方: (推測) 遅れは CDC の遅延と作り直しの時間と CDN のキャッシュ時間の合計で決まり、全体の作り直しなら作り直しの周期が下限になる。利用者には、成果物の生成時刻 (データの時点) を地図上に表示する、編集した本人には正本から直接読んだ結果を重ねて表示する (read-your-writes を成果物の外で補う)、のように見せ方で遅れを補う

## 強い整合性を選ぶべき場面

(推測: 以下は要件からの整理で、個別の出典はない)

- 行政の台帳 (道路台帳、占用許可、固定資産、住所): 正式な記録であり、同じ対象への同時更新で片方の変更が消えることを許せない。変更の履歴と責任者を残す必要がある
- 資産、設備の管理 (管路、電柱、街路灯の点検と補修): 状態の遷移 (点検済み、補修中、完了) を順序どおりに記録し、現場からの報告と事務所での承認が食い違わないようにする
- 予約や在庫、割り当て (駐車枠、施設、配車、区画): 読んだ残数をもとに確保するので、二重確保を防ぐには Serializable か行ロック、または一意制約が必要。PostgreSQL の文書は、Serializable でも一意制約違反は起こりうると明記している (https://www.postgresql.org/docs/current/transaction-iso.html)
- 位置情報ゲームの得点、ポイント、決済: 不正対策として判定と記録をサーバー側の正本で行う
- 監査や法定の履歴が求められるもの: 変更とその記録を同じトランザクションで書くことで、記録漏れを防ぐ

## 判断を左右すること

- 書き込みの頻度と同時に編集する人数: 編集者が 1 人か少数で更新がまれなら、ファイル (条件付き書き込みで楽観的排他) や 1 ファイルの GeoPackage で足りる。多人数が同じ地物を編集するなら、行単位の排他と再試行を持つ DB が要る。機械からの高頻度の書き込みは、トランザクション型の DB よりイベント、ストリーム指向の置き場所 (Context Broker、MQTT と時系列 DB) に向く。SQLite と D1 は 1 DB の書き込みが 1 つずつなので、書き込みの多い用途では上限に当たる (D1 は 1 ms のクエリで秒間約 1,000 件と文書化)
- 読み出しに許される遅れ: 数分から数時間の遅れを許せるなら成果物を配る方式で十分。書いた直後の確認には正本からの読み出しか、D1 の Sessions API のようなセッション単位の一貫性が要る
- 履歴と監査: 「誰が、いつ、何を」をトランザクション単位で残す必要があるなら DB。ファイルの版 (S3 のバージョニング) は全体のコピーを残すだけで差分や操作者を持たない
- オフラインでの編集: 必要なら、ローカルの SQLite や GeoPackage と同期の仕組み (同期エンジン、geodiff、CRDT) を置き、競合の解決方針 (後勝ち、サーバーでの検証と拒否、衝突ファイルを人が解く) を最初に決める。業務ルールの検査は、オフラインの端末ではなく同期を受けるサーバー側に置く (推測)

## ライセンス上の注意

PostGIS (GPL-2.0)、MongoDB (SSPL、OSI 非承認) など、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- PostgreSQL (PostgreSQL License): 著作権表示とライセンス文を残せば、用途を問わず使用、複製、改変、配布できる。出典: https://www.postgresql.org/about/licence/
- PostGIS (GPL-2.0-or-later): GPL は配布を条件に義務が生じるライセンスなので、PostGIS を入れた DB をサーバーで動かしてサービスを提供するだけなら、ソースの公開義務は生じない (GPL-2.0 の条文の一般的な読み方であり推測)。PostGIS (改変版を含む) やそれを組み込んだ製品 (アプライアンス、オンプレミス配布の製品、PostGIS を同梱したアプリ) を配布する場合は、PostGIS 部分のソースを GPL の条件で提供する必要がある。依存の GEOS は LGPL、SFCGAL は GPL-2.0-or-later、CGAL は GPL と LGPL-3.0 で、それぞれの条件も付く。出典: https://raw.githubusercontent.com/postgis/postgis/master/LICENSE.TXT 、 https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
- MongoDB Community Server (SSPL、2018-10-16 以降の版。OSI 非承認で、OSI の定義では OSS ではない): MongoDB を DB として使う一般の SaaS アプリにはコピーレフトの条件はかからない。MongoDB (改変版を含む) の機能そのものを第三者にサービスとして提供する場合は、MongoDB と、そのサービスの提供に使う管理、UI、API、自動化、監視、バックアップ、ストレージ、ホスティングのソフトウェアまでを、誰でも無償でダウンロードできる形で SSPL で公開する必要がある。社内 (子会社を含む) だけでの利用は第三者への提供に当たらない。Atlas の利用者は MongoDB ソフトウェアのライセンシーにならない。2018-10-16 より前の版は AGPL-3.0。出典: https://www.mongodb.com/legal/licensing/server-side-public-license/faq
- CockroachDB (CockroachDB Software License、24.3.0 の公開日以降): OSI 承認の OSS ではない。無償で使える Enterprise Free は年商 1,000 万ドル未満の事業者に限られ、毎年更新とテレメトリ送信が必須で、政府機関は対象外。行政案件で使う場合は有償契約が前提になる (推測: 政府機関が対象外という記載から)。出典: https://docs.cockroachlabs.com/docs/stable/licensing-faqs
- FIWARE Orion、Orion-LD (AGPL-3.0): 改変した版をネットワーク越しに利用者に使わせる場合は、その利用者に改変版のソースを提供する必要がある (AGPL-3.0 第 13 条)。改変せずに使うだけならこの条件は実質的に問題にならない (推測)。Scorpio は BSD-3-Clause。出典: https://github.com/telefonicaid/fiware-orion 、 https://github.com/FIWARE/context.Orion-LD 、 https://github.com/ScorpioBroker/ScorpioBroker 、 https://www.gnu.org/licenses/agpl-3.0.html
- SpatiaLite (MPL 1.1 / GPL-2.0-or-later / LGPL-2.1-or-later の選択): アプリに組み込んで配布する場合は、MPL か LGPL を選べば、SpatiaLite 部分のソース (改変した場合はその改変) を提供する義務に留まり、アプリ全体を公開する必要はない (推測: 各ライセンスの一般的な読み方)。出典: https://www.gaia-gis.it/fossil/libspatialite/home
- 寛容なライセンスのもの: Debezium、Electric、Zero と Replicache のモノレポ、PowerSync のサービスリポジトリは Apache-2.0。libSQL、Yjs、Automerge、geodiff、QFieldCloud、PostgREST は MIT。組み込み、改変、配布、SaaS のいずれでも、著作権表示とライセンス文 (Apache-2.0 では NOTICE と改変の明示も) を残せばよい

## 出典

- https://www.postgresql.org/docs/current/transaction-iso.html (PostgreSQL 18.6 の分離レベル、既定の Read Committed、SSI、40001 と再試行の必要)
- https://www.postgresql.org/ (最新は 18.6、2026-08-13。19 は RC 1、2026-10-15)
- https://www.postgresql.org/docs/current/logical-replication.html 、 https://www.postgresql.org/docs/current/logical-replication-restrictions.html (論理レプリケーションの仕組みと制約)
- https://www.postgresql.org/docs/current/ddl-rowsecurity.html (RLS、既定の全行拒否、迂回する役割)
- https://www.postgresql.org/docs/current/sql-notify.html (NOTIFY のコミット時配送、ペイロード上限)
- https://www.postgresql.org/about/licence/ (PostgreSQL License)
- https://postgis.net/docs/manual-3.6/using_postgis_dbmanagement.html (GiST、SP-GiST、BRIN、geometry と geography)
- https://postgis.net/news/ 、 https://postgis.net/development/source_code/ (PostGIS 3.7.0、2026-10-30)
- https://raw.githubusercontent.com/postgis/postgis/master/LICENSE.TXT (PostGIS のライセンスと依存のライセンス)
- https://www.mongodb.com/docs/manual/core/transactions/ (複数文書トランザクション、読み取り懸念、書き込み懸念)
- https://www.mongodb.com/docs/manual/core/transactions-production-consideration/ (1 分の既定の制限、oplog エントリ 16MB)
- https://www.mongodb.com/docs/manual/core/indexes/index-types/geospatial/2dsphere/ 、 https://www.mongodb.com/docs/manual/core/indexes/index-types/geospatial/restrictions/ 、 https://www.mongodb.com/docs/manual/reference/operator/query/geoIntersects/ 、 https://www.mongodb.com/docs/manual/geospatial-queries/ (2dsphere とその制約、演算子)
- https://www.mongodb.com/docs/manual/changestreams/ (change streams)
- https://www.mongodb.com/legal/licensing/server-side-public-license/faq (SSPL の条件と対象版)
- https://docs.cockroachlabs.com/docs/stable/transactions 、 https://docs.cockroachlabs.com/docs/stable/spatial-data-overview 、 https://docs.cockroachlabs.com/docs/stable/spatial-indexes 、 https://docs.cockroachlabs.com/docs/stable/licensing-faqs (CockroachDB の分離レベル、空間機能、ライセンス)
- https://docs.cloud.google.com/spanner/docs/data-types (Spanner の型一覧に GEOGRAPHY がない)
- https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Appendix.PostgreSQL.CommonDBATasks.PostGIS.html (Aurora での PostGIS)
- https://docs.cloud.google.com/sql/docs/postgres/extensions (Cloud SQL の PostGIS 版)
- https://supabase.com/docs/guides/database/extensions/postgis 、 https://neon.com/docs/extensions/postgis (PostGIS の提供)
- https://supabase.com/docs/guides/database/postgres/row-level-security (`auth.uid()` と `auth.jwt()`)
- https://docs.postgrest.org/en/stable/references/transactions.html 、 https://github.com/PostgREST/postgrest (`request.jwt.claims`、MIT)
- https://www.sqlite.org/lockingv3.html (SQLite の単一書き込み)
- https://www.gaia-gis.it/fossil/libspatialite/home (SpatiaLite 5.1.0 と三重ライセンス)
- https://www.ogc.org/standards/geopackage/ 、 https://www.geopackage.org/spec/ (GeoPackage 1.4.0、R-tree 拡張)
- https://wiki.openstreetmap.org/wiki/API_v0.6 (版番号と 409、差分アップロードの原子性、changeset の上限)
- https://developers.cloudflare.com/d1/best-practices/read-replication/ 、 https://developers.cloudflare.com/d1/worker-api/d1-database/ 、 https://developers.cloudflare.com/d1/sql-api/sql-statements/ 、 https://developers.cloudflare.com/d1/platform/limits/ (D1 の読み取り複製、Sessions API、batch、拡張、上限)
- https://docs.turso.tech/features/embedded-replicas/introduction 、 https://github.com/tursodatabase/libsql (組み込み複製、libSQL の MIT と開発状況)
- https://electric.ax/docs/intro 、 https://github.com/electric-sql/electric (Electric の読み取り同期、Apache-2.0)
- https://docs.powersync.com/intro/powersync-overview 、 https://docs.powersync.com/usage/lifecycle-maintenance/handling-update-conflicts 、 https://raw.githubusercontent.com/powersync-ja/powersync-service/main/LICENSE (PowerSync の構成、競合、ライセンス)
- https://zero.rocicorp.dev/llms.txt 、 https://github.com/rocicorp/mono (Zero の構成、Apache-2.0)
- https://github.com/yjs/yjs 、 https://github.com/automerge/automerge (CRDT、MIT)
- https://github.com/MerginMaps/geodiff 、 https://merginmaps.com/docs/manage/missing-data/ 、 https://github.com/opengisch/QFieldCloud (GIS の現地同期と衝突)
- https://debezium.io/documentation/reference/stable/connectors/postgresql.html 、 https://github.com/debezium/debezium (Debezium 3.7、pgoutput、Apache-2.0)
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html (S3 の条件付き書き込み)
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html (S3 のバージョニング)
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html (S3 の署名付き URL)
- https://developers.cloudflare.com/r2/api/workers/workers-api-reference/ 、 https://developers.cloudflare.com/r2/api/s3/presigned-urls/ (R2 の条件付き put と署名付き URL)
- https://docs.cloud.google.com/storage/docs/request-preconditions (GCS の事前条件)
- https://github.com/telefonicaid/fiware-orion 、 https://github.com/FIWARE/context.Orion-LD 、 https://github.com/ScorpioBroker/ScorpioBroker (FIWARE の Context Broker 実装とライセンス)
- https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html (MQTT 5.0、QoS)
- https://www.gnu.org/licenses/old-licenses/gpl-2.0.html 、 https://www.gnu.org/licenses/agpl-3.0.html (GPL-2.0、AGPL-3.0 の条文。条文の読み方は本文で推測と明記)

## 未確認のこと

- Cloudflare D1 が SQLite の R*Tree モジュールや SpatiaLite を使えるか (文書化された拡張は FTS5、JSON、数学関数のみ)。D1 で明示的な `BEGIN TRANSACTION` が使えるか。D1 の読み取り複製が現在ベータか正式提供か
- Turso (libSQL、Rust 版の Turso database) が空間索引や空間関数を持つか
- Cloudflare R2 がオブジェクトのバージョニング (過去版の保持と取得) に対応しているか
- Spanner の整合性とトランザクションの詳細、GEOGRAPHY 型の追加予定の有無
- MongoDB Atlas 固有の地理機能 (Atlas Search の geo など) が Community Server と違うか
- MongoDB の 1 トランザクションあたりの推奨文書数 (公式の本番運用の頁には記載がなかった)
- SQLite の WAL モードでの同時実行の詳細 (WAL の頁は未読)。SQLite 本体のライセンス (パブリックドメイン) の一次情報
- Debezium の PostGIS 型 (geometry、geography) のイベント上の表現
- GeoPackage 1.4.0 の承認日 (OGC の頁に日付の記載がなかった)
- OSM のデータのライセンス (ODbL) の一次情報、OSM API サーバーの内部 DB
- PowerSync のサービスについて、サービスのリポジトリ以外 (Open Edition の配布物など) に別のライセンスがかかるか
- Zero、Replicache、Electric、Yjs、Automerge の最新版番号と、Zero のオフライン書き込みの扱い、Replicache の開発状況
- QFieldCloud の同期の仕組み (差分の適用方法) と競合の扱い
- Neon の RLS、認証連携が独自関数に依存するか
- 正本から成果物への反映の遅れについて、実測に基づく目安
