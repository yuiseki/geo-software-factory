# 取得とストリーム

対象: fetch の Range リクエスト、Streams API、Compression Streams (gzip、deflate、brotli、zstd の対応)、HTTP/3、WebTransport、Fetch Priority、Speculation Rules、CORS と Range の組み合わせ

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 (版の数字は MDN browser-compat-data 8.1.8 (2026-11-02 23:19 JST 生成) と web-features 3.45.0 で確かめた) |
| 仕様と標準化の段階 (W3C / WHATWG / WICG、草案か勧告か) | Fetch (Range、CORS、fetch の priority 指定)、Streams、Compression は WHATWG の Living Standard。Fetch Priority の `fetchpriority` 属性と Speculation Rules は WHATWG HTML 標準に入っている (HTML の speculative-loading 節)。WebTransport は W3C の Candidate Recommendation Snapshot。HTTP/3 は IETF の RFC 9114 |
| Baseline の状態 (Widely available / Newly available / 未達) | Fetch、Streams、CORS は Widely available。Compression Streams は Widely available (2025-11-09 から)。HTTP/3 は Newly available (2024-09-16 から)。Fetch Priority は Newly available (2024-10-29 から)。WebTransport は Newly available (2026-03-24 から)。読み取り用のバイトストリーム (ReadableByteStreamController) は Newly available (2026-03-24 から)。ストリームの `for await...of` は Newly available (2026-09-14 から)。HTTP の zstd 圧縮は Newly available (2026-02-11 から)。Speculation Rules、fetch のリクエスト本体のストリーム送信、Compression Dictionary Transport は未達 |

## ブラウザの対応

API ごとに、対応した版を書く。iOS では全ブラウザが WebKit を使うので、iOS Safari の欄が iOS 全体の対応になる。

| API | Chrome / Edge | Firefox | Safari (macOS) | Safari (iOS / iPadOS) | Android の WebView | 出典 |
|---|---|---|---|---|---|---|
| fetch | 42 / 14 | 39 | 10.1 | 10.3 | 42 | MDN BCD `api.fetch` |
| Range ヘッダー (単一範囲) を CORS のプリフライト無しで送れる | 99 | 117 | 対応済み (WebKit bug 231174 が 2022 年に修正済み。初めて入った Safari の版は未確認) | 同左 | 99 | chromestatus 5652396366626816、Mozilla bug 1733981、WebKit bug 231174 |
| `Access-Control-Expose-Headers` | 4 / 12 | 3.5 | 4 | 3.2 | 2 | MDN BCD `http.headers.Access-Control-Expose-Headers` |
| ReadableStream (`Response.body`) | 43 / 14 | 65 | 10.1 | 10.3 | 43 | MDN BCD `api.ReadableStream`、`api.Response.body` |
| TransformStream | 67 / 79 | 102 | 14.1 | 14.5 | 67 | MDN BCD `api.TransformStream` |
| 読み取り用バイトストリーム (ReadableByteStreamController、BYOB) | 89 | 102 | 26.4 | 26.4 | 89 | MDN BCD `api.ReadableByteStreamController`、WebKit の Safari 26.4 記事 |
| ReadableStream の非同期反復 (`for await...of`) | 124 | 110 | 27 | 27 | 124 | MDN BCD `api.ReadableStream.@@asyncIterator` |
| fetch のリクエスト本体をストリームで送る (`duplex: "half"`) | 105 | 未対応 (preview 版のみ) | 未対応 | 未対応 | 未対応 | MDN BCD `api.fetch.options_parameter.duplex`、web-features `fetch-request-streams` |
| CompressionStream / DecompressionStream (gzip、deflate) | 80 | 113 | 16.4 | 16.4 | 80 | MDN BCD `api.CompressionStream`、web-features `compression-streams` |
| 同 `deflate-raw` | 103 | 113 | 16.4 | 16.4 | 103 | MDN BCD `api.CompressionStream.CompressionStream.deflate-raw` |
| 同 `brotli` | 未対応 | 147 | 18.4 | 18.4 | 未対応 | MDN BCD `api.CompressionStream.CompressionStream.brotli`、Mozilla bug 1921583 (147 で修正) |
| 同 `zstd` | 仕様に無い | 仕様に無い | 仕様に無い | 仕様に無い | 仕様に無い | WHATWG Compression 標準 (2026-10-19 版の CompressionFormat は brotli、deflate、deflate-raw、gzip の 4 つ) |
| HTTP の `Content-Encoding: br` (自動で展開) | 50 / 15 | 44 | 11 (macOS 10.13 以降) | 11 | 51 | MDN BCD `http.headers.Content-Encoding.br` |
| HTTP の `Content-Encoding: zstd` (自動で展開) | 123 | 126 | 26.3 (macOS 26.3 Tahoe より前の macOS では展開できない) | 26.3 | 123 | MDN BCD `http.headers.Content-Encoding.zstd`、chromestatus 6186023867908096 |
| Compression Dictionary Transport (共有辞書の Brotli / Zstandard) | 130 | 未対応 | 未対応 | 未対応 | 130 | web-features `compression-dictionary-transport`、chromestatus 5124977788977152 |
| HTTP/3 | 87 | 88 | 18 | 18 | 未確認 (Chrome Android は 87) | web-features `http3` |
| WebTransport | 97 | 114 | 26.4 | 26.4 | 97 | MDN BCD `api.WebTransport`、WebKit の Safari 26.4 記事 |
| Fetch Priority (`fetchpriority` 属性、fetch の `priority`) | 101 (`<link>` は 102) | 132 | 17.2 | 17.2 | 101 | MDN BCD `html.elements.img.fetchpriority`、`api.fetch.options_parameter.priority` |
| HTTP の `Priority` ヘッダー (RFC 9218) を送る | 124 | 128 | 未対応 | 未対応 | 124 | MDN BCD `http.headers.Priority` |
| Speculation Rules (`<script type="speculationrules">`) | 109 | 未対応 (preview 版で URL 一覧の prefetch のみ) | 26.2 から既定で無効 (フラグ) | 26.2 から既定で無効 (フラグ) | 109 | MDN BCD `html.elements.script.type.speculationrules` |
| `Speculation-Rules` HTTP ヘッダー | 121 | 未対応 | 26.2 から既定で無効 (フラグ) | 26.2 から既定で無効 (フラグ) | 121 | MDN BCD `http.headers.Speculation-Rules` |
| Service Worker の静的ルーティング (`InstallEvent.addRoutes`) | 123 | 未対応 | 27 | 27 | 123 | MDN BCD `api.InstallEvent.addRoutes`、WebKit の Safari 27.0 記事 |

## 概要

fetch は `Range: bytes=開始-終了` を付けて、大きなファイルの一部だけを取れる。Streams API は応答を届いた順に少しずつ処理でき、Compression Streams はその途中で gzip などを展開できる。HTTP/3 は QUIC の上で複数の要求を並べて送る通信路で、WebTransport はその上で双方向のストリームとデータグラムを JavaScript から扱う API である。Fetch Priority は要求の優先度をブラウザに伝え、Speculation Rules は次に開きそうなページの先読みと事前描画をブラウザに頼む。

## 地図プロダクトでの使いどころ

保存、計算、表現のどれを、ブラウザ・アプリの層に置けるようにするか。

- 保存: タイルやベクタを 1 つの大きなファイル (PMTiles、FlatGeobuf、GeoParquet、COG) として静的ホスティングや CDN に置き、ブラウザが Range で必要な部分だけを読む。タイルサーバーやデータベースを置かずに済む。pmtiles の JS ライブラリは `range: bytes=開始-終了` を付けた fetch で、ヘッダーとディレクトリとタイルを読み分ける (PMTiles の js/src/index.ts で確認)。
- 計算: Range で読んだ部分をブラウザの中で展開、絞り込み、集計する。pmtiles の JS ライブラリは gzip のタイルとディレクトリを `DecompressionStream("gzip")` で展開し、無い環境では fflate に切り替える。hyparquet は Range で Parquet の必要な列と行グループだけを読み、DuckDB-Wasm は Range で読んだ Parquet に SQL をかける。FlatGeobuf は packed Hilbert R-tree の索引を先に読み、範囲に入る地物だけを Range で取る。
- 表現: Streams で届いた順に地物を描けるので、全件を待たずに地図を描き始められる (FlatGeobuf の JS 実装は地物を 1 件ずつ返す)。WebTransport は車両位置のような更新の多いデータを、WebSocket の代わりに順序の要らないデータグラムで送る用途に使える (推測。地図での採用例は未確認)。Fetch Priority で画面中央のタイルを `high`、先読みのタイルを `low` にする使い方もできる (推測。主要な地図ライブラリが使っているかは未確認)。

## 制約

- 容量と寿命: Range 読みはファイルの大きさに上限を作らないが、CDN 側には上限がある。Cloudflare は Free、Pro、Business で 1 ファイル 512 MB、Enterprise で既定 5 GB までしかキャッシュせず、小さな範囲を要求しても判定はファイル全体の大きさで行う。CloudFront は 50 GB を超える物体をキャッシュしないが、Range で取った部分はキャッシュできる。DuckDB-Wasm は WebAssembly のメモリ上限 4 GB の中で動く。
- 権限とユーザーの操作が要るか: どれも利用者の許可は要らない。別オリジンから読むときはサーバー側の CORS 設定が要る。
- セキュアコンテキスト、クロスオリジン分離 (COOP/COEP) などの前提: WebTransport は HTTPS (HTTP/3) のサーバーが要る。Fetch と Streams と Compression Streams は HTTP でも動く。DuckDB-Wasm のマルチスレッド版は `SharedArrayBuffer` を使うので、ページに COOP と COEP のヘッダーが要り、無ければ単一スレッド版に切り替わる。
- iOS / Safari での制限: Safari は fetch のリクエスト本体のストリーム送信に対応していない。WebTransport とバイトストリームは Safari 26.4 から、`for await...of` は Safari 27 からなので、iOS 26.3 以前の端末では使えない。Safari の Speculation Rules は既定で無効である。Safari の zstd 展開は OS が macOS 26.3 以上であることが前提 (MDN BCD の注記)。
- WebView (アプリに埋め込んだブラウザ) での制限: Android の WebView は Chrome と同じ版で fetch、Streams、Compression Streams、WebTransport、Speculation Rules に対応するが、fetch のリクエスト本体のストリーム送信には対応していない (MDN BCD)。iOS の WKWebView は Safari と同じ WebKit を使う。

## 地図の実装例

この API を使っている OSS やライブラリ (地図ライブラリ、PMTiles、DuckDB-Wasm など)。

- pmtiles (npm 4.5.0、BSD-3-Clause): Range の fetch、`DecompressionStream("gzip")`、ETag による差し替え検出を実装している。既定の展開関数は gzip と無圧縮だけを扱い、brotli と zstd では例外を投げる (js/src/index.ts の `defaultDecompress`)。
- flatgeobuf (npm 4.6.1): Range で索引と地物を読み、地物を順に返す。README は別オリジンの CDN から読むと Range ヘッダーのためにプリフライトが起きると書いている。
- hyparquet (npm 1.33.0、MIT): `asyncBufferFromUrl` で Parquet を Range 読みする。`byteLength` を渡すとファイルの大きさを知るための HEAD を省ける。
- DuckDB-Wasm (npm @duckdb/duckdb-wasm、MIT): `LOAD httpfs` でブラウザ向けに作り直した HTTP 実装を使い、Range で Parquet を部分読みする。要求は常に HTTPS に上げられる。
- loaders.gl (npm @loaders.gl/core 4.5.4、MIT): MLT の展開は 4.4 から (MapLibre Tile の実装状況ページ)。

## 落とし穴

- 単一範囲の Range はプリフライト無しで送れるが、複数範囲 (`bytes=0-99,200-299`) と末尾指定 (`bytes=-500`) は CORS で許可された形ではないのでプリフライトが起きる (Fetch 標準の CORS-safelisted request-header)。`If-Match` や `Authorization` など独自のヘッダーを付けても毎回プリフライトが起きる。
- 応答の `Content-Range` と `ETag` は CORS で読める応答ヘッダーに入っていない。Fetch 標準の既定で読めるのは `Cache-Control`、`Content-Language`、`Content-Length`、`Content-Type`、`Expires`、`Last-Modified`、`Pragma` だけなので、`Access-Control-Expose-Headers` に `ETag` (必要なら `Content-Range`) を書く。PMTiles の文書は R2 と S3 で許可するヘッダーを `range`、`if-match`、公開するヘッダーを `etag` としている。
- pmtiles の JS は `If-Match` を送らない。コードの注記の理由は「Chromium でブラウザのキャッシュが完全に無効になる」「タイルごとにプリフライトが要る」「If-Match は CORS で許可されたヘッダーでない」の 3 つである。代わりに応答の ETag の食い違いか 416 で差し替えを検出し、`cache: "reload"` で 1 度取り直す。また Windows 上の Chromium 系ブラウザでは常に `cache: "no-store"` で取る (理由はコードに書かれていない)。
- サーバーが Range を無視して 200 で全体を返すと、ブラウザは大きなファイルを丸ごと落とす。pmtiles の JS は `Content-Length` が要求より大きい 200 を検出して中断する。
- Cloudflare は既定で拡張子だけを見てキャッシュし、`.pmtiles` と `.parquet` は既定の一覧に無い。キャッシュするには Cache Rule が要る。オリジンへの Range は 1 MiB 単位にそろえて取りに行くので、1 KiB の要求でもオリジンへの取得は 1 MiB になりうる。オリジンの 206 をキャッシュするには、応答が無圧縮で、正しい `Content-Range` と `Content-Length` を持ち、`Transfer-Encoding` が無いことが要る。Workers の前では Range ヘッダーが外され、Worker が返す 206 はキャッシュされない。
- CloudFront はオリジンが `Transfer-Encoding: chunked` で返すと、Range の要求に対して物体全体を返す。圧縮した物体では、バイト範囲は圧縮後の大きさで数える。
- Range で読むファイルに HTTP の圧縮 (`Content-Encoding: br` や `zstd`) をかけると、範囲が圧縮後のバイトを指すことになり、Cloudflare でもキャッシュできない。アーカイブ形式は中身を自分で圧縮しておき、配信時の圧縮はかけない (Cloudflare と CloudFront の文書からの推論)。
- PMTiles の中身を brotli か zstd で圧縮すると、Chrome の DecompressionStream では展開できず (brotli は Chrome 未対応、zstd は仕様に無い)、pmtiles の既定の展開関数も扱わない。ブラウザで直接読むなら gzip か無圧縮にする。
- S3、Azure、DigitalOcean (CDN を有効にしても)、Backblaze B2、Scaleway は HTTP/1.1 だけを話し、R2 と Google Cloud は HTTP/2 を話す (PMTiles の文書)。HTTP/1.1 では同時に送れる要求が少なく、Range で多数のタイルを読むと詰まりやすい (推測。ブラウザの同時接続数の上限は未確認)。
- DuckDB-Wasm の文書は、Firefox で Range 要求が失敗することがある点と、S3 の署名付き URL で Range 対応を正しく判定できない場合がある点を既知の問題として挙げている。
- CDN はプリフライトの OPTIONS を既定ではキャッシュしないことがある。FlatGeobuf の README は CloudFront で OPTIONS のキャッシュを有効にするよう勧めている。
- Safari の Speculation Rules は既定で無効なので、地図ページの先読みは Chrome 系だけで効く前提で設計する。

## まだ使えないもの、これから使えるもの

提案中、Origin Trial 中、一部のブラウザだけのもの。

- CompressionStream の brotli: Firefox 147 と Safari 18.4 は対応済みで、Chrome と Android の WebView は未対応 (MDN BCD 8.1.8)。
- CompressionStream の zstd: WHATWG Compression 標準 (2026-10-19 版) に入っていない。HTTP の `Content-Encoding: zstd` は全主要ブラウザで使える。
- Compression Dictionary Transport (前に取った応答を辞書にして brotli、zstd で差分を送る): Chrome 130 から。Firefox と Safari は未対応。chromestatus は Firefox を Positive、Safari を Support と記録している。
- fetch のリクエスト本体のストリーム送信: Chrome 105 だけ。Firefox は preview 版、Safari は未対応 (WebKit bug 245671)。
- Speculation Rules: Firefox は preview 版で同一オリジンの prefetch の試作を始めている (Mozilla bug 2020702)。Safari は 26.2 から既定で無効のまま入っている。
- `fetchLater` API: Chrome 135 から Origin Trial (chromestatus 4654499737632768)。

## 出典

- https://github.com/mdn/browser-compat-data (npm @mdn/browser-compat-data 8.1.8 の data.json を取得し、表の各 API の版と注記を確かめた)
- https://github.com/web-platform-dx/web-features (npm web-features 3.45.0 の data.json を取得し、Baseline の状態と日付を確かめた)
- https://fetch.spec.whatwg.org/#cors-safelisted-request-header (単一範囲の Range だけがプリフライト無しで送れること、末尾指定と複数範囲は外れること、CORS で読める応答ヘッダーの一覧)
- https://chromestatus.com/feature/5652396366626816 (Chrome 99 で単一範囲の Range をプリフライト無しで送れるようになったこと)
- https://bugzilla.mozilla.org/show_bug.cgi?id=1733981 (Firefox 117 で同じ変更が入ったこと)
- https://bugs.webkit.org/show_bug.cgi?id=231174 (WebKit で同じ変更が修正済みであること)
- https://compression.spec.whatwg.org/ (2026-10-19 版の CompressionFormat が brotli、deflate、deflate-raw、gzip であること)
- https://bugzilla.mozilla.org/show_bug.cgi?id=1921583 (Firefox 147 で Compression Streams の brotli が入ったこと)
- https://caniuse.com/mdn-api_compressionstream_compressionstream_brotli (brotli の対応が Firefox 147、Safari 18.4 からで Chrome が未対応であること)
- https://caniuse.com/zstd (zstd の Content-Encoding の対応版)
- https://chromestatus.com/feature/6186023867908096 (Chrome 123 の Zstd Content-Encoding)
- https://chromestatus.com/feature/5124977788977152 (Compression Dictionary Transport が Chrome 130 から既定で有効)
- https://webkit.org/blog/17862/webkit-features-for-safari-26-4/ (Safari 26.4 の WebTransport、ReadableByteStream、fetch でのバイトストリーム)
- https://webkit.org/blog/18325/webkit-features-for-safari-27-0/ (Safari 27.0 のストリームの非同期反復、`ReadableStream.from()`、Service Worker の静的ルーティング。記事は 2026-09-17 付)
- https://www.w3.org/TR/webtransport/ (WebTransport が Candidate Recommendation Snapshot であること)
- https://html.spec.whatwg.org/multipage/speculative-loading.html (Speculation Rules が HTML 標準にあること)
- https://docs.protomaps.com/pmtiles/cloud-storage (各ストレージの CORS 設定例、HTTP/1.1 だけのストレージの一覧、Range 1 回が GET 1 回として課金されること)
- https://github.com/protomaps/PMTiles/blob/main/js/src/index.ts (Range の送り方、If-Match を送らない理由、ETag と 416 の扱い、Windows の Chromium での no-store、gzip だけを展開する既定の関数)
- https://developers.cloudflare.com/cache/reference/range-requests/ (Cloudflare の Range の扱い、1 MiB 単位のオリジン取得、206 をキャッシュする条件、Workers での扱い)
- https://developers.cloudflare.com/cache/concepts/default-cache-behavior/ (キャッシュできるファイルの大きさの上限と、拡張子による既定のキャッシュ対象)
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RangeGETs.html (CloudFront の Range の扱い、50 GB を超える物体、chunked の場合)
- https://github.com/flatgeobuf/flatgeobuf (README の HTTP Range とプリフライトと CloudFront の注意)
- https://github.com/hyparam/hyparquet (README の `asyncBufferFromUrl` と対応する圧縮形式)
- https://duckdb.org/docs/2.0/clients/wasm/extensions.html (DuckDB-Wasm の httpfs が JavaScript で作り直されていること、HTTPS への格上げ、CORS)
- https://duckdb.org/docs/2.0/clients/wasm/troubleshoot (Firefox での Range の失敗、S3 署名付き URL、4 GB の上限、COOP と COEP)

## 未確認のこと

- 単一範囲の Range をプリフライト無しで送れるようになった Safari の版 (WebKit の修正は 2022 年だが、どの Safari に入ったかは確かめていない)。FlatGeobuf の README の「Range でプリフライトが起きる」という記述が、この変更の前の挙動を書いたものかどうか。
- Safari と iOS Safari の zstd 対応で caniuse が「部分対応」としている中身。
- Android の WebView での HTTP/3 の対応版 (web-features は Chrome Android の値だけを持つ)。
- HTTP/1.1 での同一ホストへの同時接続数の上限が、現行の各ブラウザでいくつか。
- MapLibre GL JS など主要な地図ライブラリが、タイルの取得に Fetch Priority を使っているか。
- Speculation Rules で事前描画したページで、Geolocation など許可の要る API がどう扱われるか。
- WebTransport を地図のリアルタイム配信に使っている OSS の実例。
