# WebAssembly

対象: WebAssembly 本体、SIMD、スレッド (SharedArrayBuffer と COOP/COEP によるクロスオリジン分離)、Memory64、JSPI、GC、Component Model、Wasm の取得と起動の速さ

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 (ブラウザ対応は MDN browser-compat-data 8.1.8 (2026-11-02 生成) と web-features 3.45.0、WebAssembly 公式サイトの features.json で照合) |
| 仕様と標準化の段階 (W3C / WHATWG / WICG、草案か勧告か) | コア仕様は W3C WebAssembly Working Group が出す。Wasm 2.0 (WebAssembly Core Specification) は W3C の Candidate Recommendation Draft (最新は 2025-06-16 版) のままで、WG は勧告 (Recommendation) へ進めず CR を随時更新する evergreen 方式に切り替えた。最新の CR Draft を現行標準とみなす。2025-09-17 に Wasm 3.0 が公開され、Memory64、Multiple memories、GC、型付き参照、末尾呼び出し、例外処理 (exnref)、Relaxed SIMD、JS String Builtins が入った。JSPI は提案段階で Phase 5 (標準化済み、仕様への統合待ち)、Threads は Phase 4、ESM Integration と Stack Switching は Phase 3、Component Model は Phase 1。COOP/COEP と crossOriginIsolated は WHATWG HTML Living Standard、Document-Isolation-Policy は WICG の草案 |
| Baseline の状態 (Widely available / Newly available / 未達) | Widely available: WebAssembly 本体、固定幅 SIMD (2025-09-27 に到達)、スレッドと Atomics、SharedArrayBuffer と Atomics、例外処理 (旧方式)、BigInt と i64 の相互変換。Newly available: GC と末尾呼び出し (2024-12-11)、型付き関数参照 (2024-09-16)、exnref (2025-05-29)、Branch hinting (2026-02-24)、JSPI (2026-09-14)。未達: Memory64、Multi-memory、Relaxed SIMD (Safari 未対応)、JS String Builtins (web-features 3.45.0 時点。BCD では Safari 26.2 で対応済みとされ食い違う)、Document-Isolation-Policy |

## ブラウザの対応

API ごとに、対応した版を書く。iOS では全ブラウザが WebKit を使うので、iOS Safari の欄が iOS 全体の対応になる。

| API | Chrome / Edge | Firefox | Safari (macOS) | Safari (iOS / iPadOS) | Android の WebView | 出典 |
|---|---|---|---|---|---|---|
| WebAssembly 本体 (JS API) | Chrome 57 / Edge 16 | 52 | 11 | 11 | 57 | [webstatus wasm](https://webstatus.dev/features/wasm) |
| `WebAssembly.compileStreaming()` / `instantiateStreaming()` | Chrome 60 / Edge 16 | 58 | 15 | 15 | 60 | [MDN](https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/instantiateStreaming_static) |
| 固定幅 SIMD (128bit) | Chrome 91 / Edge 91 | 89 | 16.4 | 16.4 | 91 | [webstatus wasm-simd](https://webstatus.dev/features/wasm-simd) |
| Relaxed SIMD | Chrome 114 / Edge 114 | 146 (BCD)。WebAssembly 公式の表は 145 | 未対応 (Technology Preview のみ。公式の表では JavaScriptCore のフラグが必要) | 未対応 | 114 | [webstatus wasm-simd-relaxed](https://webstatus.dev/features/wasm-simd-relaxed)、[features.json](https://github.com/WebAssembly/website/blob/main/features.json) |
| スレッドと Atomics (共有 `WebAssembly.Memory`) | Chrome 74 (Android 版 Chrome は 88) / Edge 79。どちらもクロスオリジン分離が必要 | 79 (分離が必要) | 15.2 (分離が必要) | 15.2 (分離が必要) | 未対応 | [webstatus wasm-threads](https://webstatus.dev/features/wasm-threads)、[MDN BCD](https://github.com/mdn/browser-compat-data) |
| `SharedArrayBuffer` | Chrome 68 (デスクトップは 92 から分離が必須。分離なしで使い続ける試用は Chrome 124 まで延長された。Android 版 Chrome は 89) / Edge 79 | 79 | 15.2 | 15.2 | 未対応 | [webstatus shared-memory](https://webstatus.dev/features/shared-memory)、[Chrome blog](https://developer.chrome.com/blog/enabling-shared-array-buffer) |
| `crossOriginIsolated` | Chrome 87 / Edge 87 | 72 (Android 版は 79) | 15.2 | 15.2 | 87 | [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated) |
| `Cross-Origin-Opener-Policy` ヘッダー | Chrome 83 / Edge 83 | 79 | 15.2 | 15.2 | 未対応 | [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy) |
| `Cross-Origin-Embedder-Policy: require-corp` | Chrome 83 / Edge 83 | 79 | 15.2 | 15.2 | 86 | [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy) |
| `Cross-Origin-Embedder-Policy: credentialless` | Chrome 96 / Edge 96 | 119 (デスクトップのみ。Android 版は未対応) | 未対応 | 未対応 | 96 | [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy) |
| `Document-Isolation-Policy` ヘッダー | Chrome 137 (デスクトップ。Android 版 Chrome は 146) / Edge 137 | 未対応 | 未対応 | 未対応 | 未対応 | [webstatus document-isolation-policy](https://webstatus.dev/features/document-isolation-policy)、[Chrome blog](https://developer.chrome.com/blog/document-isolation-policy) |
| Memory64 | Chrome 133 / Edge 133 | 134 | 未対応 (Technology Preview 251 でフラグ付き) | 未対応 | 133 | [webstatus wasm-memory64](https://webstatus.dev/features/wasm-memory64)、[features.json](https://github.com/WebAssembly/website/blob/main/features.json) |
| Multi-memory | Chrome 120 / Edge 120 | 125 | 未対応 (Technology Preview のみ) | 未対応 | 120 | [webstatus wasm-multi-memory](https://webstatus.dev/features/wasm-multi-memory) |
| JSPI (JavaScript Promise Integration) | Chrome 137 / Edge 137 | 153 | 27 | 27 | 137 | [webstatus wasm-jspi](https://webstatus.dev/features/wasm-jspi) |
| GC | Chrome 119 / Edge 119 | 120 | 18.2 | 18.2 | 119 | [webstatus wasm-garbage-collection](https://webstatus.dev/features/wasm-garbage-collection) |
| 型付き関数参照 | Chrome 119 / Edge 119 | 120 | 18 | 18 | 119 | [webstatus wasm-typed-fun-refs](https://webstatus.dev/features/wasm-typed-fun-refs) |
| 例外処理 (旧方式) | Chrome 95 / Edge 95 | 100 | 15.2 | 15.2 | 95 | [webstatus wasm-exception-handling](https://webstatus.dev/features/wasm-exception-handling) |
| 例外処理 (exnref、Wasm 3.0 の方式) | Chrome 137 / Edge 137 | 131 | 18.4 | 18.4 | 137 | [webstatus wasm-exnref-exceptions](https://webstatus.dev/features/wasm-exnref-exceptions) |
| 末尾呼び出し | Chrome 112 / Edge 112 | 121 | 18.2 | 18.2 | 112 | [webstatus wasm-tail-call-optimization](https://webstatus.dev/features/wasm-tail-call-optimization) |
| JS String Builtins | Chrome 130 / Edge 130 | 134 | 26.2 (BCD。web-features 3.45.0 は未対応扱い) | 26.2 (同左) | 130 | [webstatus wasm-string-builtins](https://webstatus.dev/features/wasm-string-builtins)、[MDN BCD](https://github.com/mdn/browser-compat-data) |
| Component Model | 未対応 | 未対応 | 未対応 | 未対応 | 未対応 | [WebAssembly proposals](https://github.com/WebAssembly/proposals) (Phase 1) |

Chrome の対応版は Android 版 Chrome も同じ (違うものは欄内に書いた)。主な版の公開日: Chrome 133 は 2025-02-04、Chrome 137 は 2025-05-27、Firefox 134 は 2025-01-07、Firefox 153 は 2026-07-21、Safari 18.2 は 2024-12-11、Safari 27 は 2026-09-14 (BCD の browsers データ)。

## 概要

WebAssembly は、C、C++、Rust などからコンパイルしたバイナリをブラウザで JavaScript とほぼ同じ安全性の枠の中で、ネイティブに近い速さで動かす仕組みである。地図の分野では GDAL、GEOS、PROJ、SQLite、DuckDB のような C/C++ 製の空間処理ライブラリを、サーバーを置かずにブラウザへ持ち込む手段になる。SIMD で数値計算を速くでき、SharedArrayBuffer と Worker を組み合わせればマルチスレッドで動かせるが、スレッドはページを COOP/COEP でクロスオリジン分離したときだけ使える。Memory64 で 4GB を超えるメモリを扱え、JSPI で同期的な C/C++ の I/O を JavaScript の Promise につなげられる。

## 地図プロダクトでの使いどころ

保存、計算、表現のどれを、ブラウザ・アプリの層に置けるようにするか。

- 保存: SQLite Wasm を OPFS の上で動かすと、端末内に永続する SQLite データベース (GeoPackage や MBTiles のような SQLite 形式のファイルを含む) を持てる。OPFS の VFS は Worker でしか動かない。`opfs` VFS は COOP/COEP が必要で、`opfs-sahpool` VFS (SQLite 3.43 から) は COOP/COEP が要らない代わりに同じ DB への同時接続ができない。`opfs-wl` VFS (3.53.0 から) は `Atomics.waitAsync()` と Web Locks を使う ([SQLite persistence](https://sqlite.org/wasm/doc/trunk/persistence.md))。DuckDB-Wasm は `INSTALL` しても永続しない (セッションをまたぐ保存先がない) ([DuckDB-Wasm extensions](https://duckdb.org/docs/2.0/clients/wasm/extensions.html))。
- 計算: DuckDB-Wasm に `spatial` 拡張を `LOAD` すると、ブラウザ内で GeoParquet などを SQL で空間結合・集計できる ([DuckDB-Wasm extensions](https://duckdb.org/docs/2.0/clients/wasm/extensions.html))。gdal3.js で ogr2ogr、gdal_translate、gdalwarp、gdal_rasterize をブラウザで動かし、形式変換や再投影をサーバーなしでできる ([gdal3.js](https://github.com/bugra9/gdal3.js))。geos-wasm でバッファや交差などの幾何演算、wasm-proj で PROJ の座標変換ができる ([geos-wasm](https://github.com/chrispahm/geos-wasm)、[wasm-proj](https://github.com/jjimenezshaw/wasm-proj))。いずれもサーバーの計算を端末に移すので、クラウド側の CPU 原価と往復の待ち時間を減らせる (推測)。
- 表現: 描画そのものは WebGL/WebGPU が担い、Wasm は描画の前処理 (タイルのデコード、ジオメトリの切り出し、ラベル配置の計算など) に使う形になる (推測)。MapLibre GL JS 6.17.0 は Wasm も SharedArrayBuffer も使っておらず、タイルの解析は JavaScript の Worker で行う (ソースで確認。[workers.md](workers.md) を参照)。

## 制約

- 容量と寿命: 32bit の Wasm メモリは上限 4GB で、ブラウザはさらに低い上限を課すことがある ([DuckDB-Wasm overview](https://duckdb.org/docs/2.0/clients/wasm/overview.html))。Memory64 でもウェブでは 1 つのメモリは 16GB までに制限される ([Wasm 3.0](https://webassembly.org/news/2025-09-17-wasm-3.0/))。Wasm のメモリはページを閉じれば消えるので、残したいデータは OPFS や IndexedDB に書く。
- 権限とユーザーの操作が要るか: Wasm 自体に権限プロンプトはない。CSP を厳しくしているページでは Wasm のコンパイルが止められる ([MDN instantiateStreaming](https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/instantiateStreaming_static))。`script-src` に `'wasm-unsafe-eval'` を足すのが通例である (MDN の該当ページには明記されておらず、未確認のことへ回した)。
- セキュアコンテキスト、クロスオリジン分離 (COOP/COEP) などの前提: `SharedArrayBuffer` はセキュアコンテキストかつクロスオリジン分離されたページでだけ使え、条件を満たさないと `SharedArrayBuffer` コンストラクターが隠され、`postMessage()` で SAB を渡すと例外になる ([MDN SharedArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer))。分離には `Cross-Origin-Opener-Policy: same-origin` と `Cross-Origin-Embedder-Policy: require-corp` (または `credentialless`) の両方を返す。分離すると次のものが壊れる ([web.dev COOP/COEP](https://web.dev/articles/coop-coep)): 別オリジンのポップアップとの `window.opener` での通信、CORP も CORS もない別オリジンの画像やスクリプト、CORP を返さない別オリジンの iframe (iframe 側に `allow="cross-origin-isolated"` も要り、親子の全文書が分離されている必要がある)。`credentialless` は CORP のない no-cors の資源をクッキーなしで読み込めるようにするが、Safari と Android 版 Firefox は対応していない。`Document-Isolation-Policy` はフレーム単位で分離でき、子フレームに条件を課さないが、Chromium 系だけである ([Chrome blog](https://developer.chrome.com/blog/document-isolation-policy))。
- iOS / Safari での制限: Memory64、Multi-memory、Relaxed SIMD が未対応なので、これらを前提にしたビルドは iOS で動かない。JSPI は Safari 27 (2026-09-14) からなので、それより古い iOS では Asyncify などの代替が要る。`credentialless` がないので、iOS でスレッドを使うには第三者の no-cors 資源に CORP を付けてもらうか、CORS で読むしかない。
- WebView (アプリに埋め込んだブラウザ) での制限: Android の WebView は `SharedArrayBuffer`、COOP、Wasm スレッドがいずれも未対応 (BCD)。DuckDB-Wasm の `coi` バンドルや SQLite の `opfs` VFS のような分離前提の構成は Android アプリ内では使えず、シングルスレッドのバンドルか `opfs-sahpool` に落とす設計が要る。iOS の WKWebView は BCD 上 15.2 から SAB と COOP に対応する。

## 地図の実装例

この API を使っている OSS やライブラリ (地図ライブラリ、PMTiles、DuckDB-Wasm など)。

- DuckDB-Wasm (MIT): `mvp` (Wasm 1.0)、`eh` (Wasm 例外処理)、`coi` (スレッド) の 3 バンドルがあり、`selectBundle` がブラウザの機能を調べて選ぶ。`coi` はクロスオリジン分離、例外処理、SIMD、スレッドがそろったときだけ選ばれ、`getJsDelivrBundles()` には含まれない。既定はシングルスレッドで、マルチスレッドは実験的扱い ([instantiation](https://duckdb.org/docs/2.0/clients/wasm/instantiation.html)、[README](https://github.com/duckdb/duckdb-wasm))。`spatial` 拡張は本体に同梱されず、`LOAD` 時に extensions.duckdb.org から取得し署名を検証して読み込む。ネイティブの httpfs は入っておらず JavaScript 実装で代替し、取得先には CORS が要る ([extensions](https://duckdb.org/docs/2.0/clients/wasm/extensions.html))。`spatial` 拡張は GEOS、PROJ、GDAL、SQLite に依存する ([vcpkg.json](https://github.com/duckdb/duckdb-spatial/blob/main/vcpkg.json))。
- SQLite Wasm (`@sqlite.org/sqlite-wasm` 3.54.1-build1、2026-10-19 公開。SQLite 本体はパブリックドメイン、npm パッケージは Apache-2.0): OPFS を使うには Worker で動かす ([sqlite-wasm](https://github.com/sqlite/sqlite-wasm))。VFS の選び方は上の「保存」を参照。
- gdal3.js 2.8.1 (2024-02-22 公開、LGPL-2.1-or-later): GDAL 3.8.4 と PROJ、GEOS、SpatiaLite、SQLite などを Emscripten 3.1.51 でまとめて Wasm にしたもの。PMTiles、MBTiles、FlatGeobuf、GPKG、GeoTIFF などを読み書きでき、Worker 版と非 Worker 版がある ([README](https://github.com/bugra9/gdal3.js))。
- geos-wasm 3.1.1 (2024-12-09 公開): GEOS の C API をそのまま JavaScript から呼ぶ形で、ポインタの確保と解放を呼び出し側が行う ([README](https://github.com/chrispahm/geos-wasm))。ライセンスは GitHub では LGPL-2.1、npm では LGPL-3.0-or-later と表示が食い違う。
- wasm-proj (MIT): PROJ をブラウザで動かし、グリッドファイルはリモートから使う ([wasm-proj](https://github.com/jjimenezshaw/wasm-proj))。PROJ 本体の CI には `emscripten.yml` がある ([PROJ workflows](https://github.com/OSGeo/PROJ/tree/master/.github/workflows))。
- h3-js 4.5.0 (Apache-2.0、2026-07-01 公開): H3 の C 実装を Emscripten で変換しているが、ビルドは `-s WASM=0` で Wasm ではなく JavaScript を出力している ([update-emscripten.sh](https://github.com/uber/h3-js/blob/master/scripts/update-emscripten.sh)、[README](https://github.com/uber/h3-js))。h3-js は Wasm の対応状況や COOP/COEP の影響を受けない。
- parquet-wasm 0.9.0 (MIT OR Apache-2.0、2026-09-25 公開) と geoarrow-rs (Apache-2.0): Rust 製で Parquet と GeoArrow をブラウザで扱う ([parquet-wasm](https://github.com/kylebarron/parquet-wasm)、[geoarrow-rs](https://github.com/geoarrow/geoarrow-rs))。
- ルート検索: Valhalla の公式な Wasm ビルドは見つからなかった。第三者の npm パッケージ `@jansoft/mbujkanji-valhalla-wasm` 0.1.2 があるが中身は確かめていない ([pkgstats](https://www.pkgstats.com/pkg:@jansoft/mbujkanji-valhalla-wasm))。
- MapLibre GL JS と PMTiles (`pmtiles` 4.5.0) はどちらも Wasm を使わない JavaScript 実装である (MapLibre はソースで確認。PMTiles は未確認のことへ)。

## 落とし穴

- `.wasm` を `Content-Type: application/wasm` で返さないと `instantiateStreaming()` は `TypeError` で失敗する ([MDN](https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/instantiateStreaming_static))。CDN やオブジェクトストレージの MIME 設定を確かめる。
- Chrome (V8) は Wasm を Liftoff で素早く動かし始め、TurboFan で裏で最適化し直す。大きなモジュールでは最適化に 30 秒から 1 分以上かかることがある。コンパイル結果のキャッシュは、ストリーミング API を使い、128kB 以上で、同じ URL (クエリ文字列も含む) で、TurboFan の最適化が終わったときだけ効く。`304` ならキャッシュは生き、`200` で更新されると捨てられ、V8 の版が上がっても捨てられる ([V8 blog, 2019-06-17](https://v8.dev/blog/wasm-code-caching))。版ごとに URL を変える配信 (クエリでの cache busting) はコードキャッシュを毎回失う。
- 地図は第三者のタイル、グリフ、スプライト、ロゴ画像、広告や埋め込みの iframe を読むことが多い。COEP `require-corp` を有効にすると、CORS も CORP もない no-cors 資源は読めなくなる。MapLibre GL JS はタイルやスタイルを `fetch` (既定の mode は `cors`) で取得しているので、CORS を返すタイル配信なら COEP では止まらない (ソースを読んだうえでの推測)。止まりやすいのは `<img>` で直接置いたマーカー画像、他社の地図や動画の iframe、OAuth などのポップアップ連携である ([web.dev](https://web.dev/articles/coop-coep))。導入前に `Cross-Origin-Embedder-Policy-Report-Only` で何が止まるかを集めるとよい。
- 地図を顧客サイトに iframe で埋め込んで提供する場合、iframe の中でスレッドを使うには親ページも分離され、iframe に `allow="cross-origin-isolated"` が付いている必要がある ([web.dev](https://web.dev/articles/coop-coep))。埋め込み型の地図製品では顧客側のヘッダーを制御できないので、スレッド前提の設計は成り立たないことが多い (推測)。Chromium だけなら `Document-Isolation-Policy` で回避できる。
- `Atomics.wait()` はメインスレッドでは呼べず `TypeError` になる ([MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics/wait))。Emscripten の pthread ビルドをメインスレッドで動かすと、ブロッキングする箇所で問題になるので、Wasm 本体は Worker に置く。
- DuckDB-Wasm の拡張はバンドルごとのプラットフォーム (`wasm_mvp`、`wasm_eh`、`wasm_threads`) 向けに作られたものしか読めない ([instantiation](https://duckdb.org/docs/2.0/clients/wasm/instantiation.html))。自前の拡張リポジトリを置くなら 3 種類をそろえ、CORS を開ける。
- DuckDB-Wasm の httpfs 経由だと、リモートの Parquet を範囲取得せず全体をダウンロードすることがある (duckdb-wasm issue #2153 として記載) ([overview](https://duckdb.org/docs/2.0/clients/wasm/overview.html))。巨大な GeoParquet を CDN から引く設計では実測が要る。
- ライセンス (LGPL): gdal3.js (LGPL-2.1-or-later)、GEOS (LGPL-2.1)、geos-wasm (LGPL-2.1 または LGPL-3.0-or-later、表示が食い違う) は LGPL である。DuckDB の `spatial` 拡張も GEOS を含む。以下は条文の一般的な読み方であり、法的な確認はしていない (推測)。組み込み: 自社コードと別の `.wasm`/`.js` ファイルとして読み込む形 (動的リンクに近い形) にしておけば、自社コードを LGPL にする必要はない。変更: ライブラリ自体を改変した場合、その改変部分は LGPL で公開する。配布: `.wasm` をブラウザへ配信することは利用者への頒布に当たると考えるのが安全で、ライセンス文の同梱、ライブラリのソース (改変があれば改変後) の入手手段の提示、利用者がライブラリを差し替えられるようにすることが求められる。SaaS: LGPL には AGPL のようなネットワーク条項がないので、サーバー側だけで動かすなら頒布に当たらないが、ブラウザに送る時点でその例外には入らない。

## まだ使えないもの、これから使えるもの

提案中、Origin Trial 中、一部のブラウザだけのもの。

- Memory64: Chrome 133 と Firefox 134 は対応、Safari は Technology Preview 251 のフラグ付きだけ ([features.json](https://github.com/WebAssembly/website/blob/main/features.json))。4GB を超える点群やラスタをブラウザで扱う構成は、iOS を対象から外さない限りまだ成り立たない。
- Relaxed SIMD と Multi-memory: Chromium と Firefox だけ。Safari は Technology Preview のみ。
- Wide Arithmetic: Phase 4。Firefox 155 で有効 (BCD)。Chrome はフラグ、Safari は Technology Preview。
- Stack Switching: Phase 3。Chrome はフラグ (`chrome://flags/#enable-experimental-webassembly-stack-switching`) のみ ([features.json](https://github.com/WebAssembly/website/blob/main/features.json))。
- ESM Integration (`import` で `.wasm` を直接読む): Phase 3。ブラウザはどれも未対応で、Deno 2.1 が対応 ([features.json](https://github.com/WebAssembly/website/blob/main/features.json))。
- Custom Page Sizes、Custom Descriptors: Phase 3。
- Component Model と WASI: Phase 1 で、ブラウザは未対応。ブラウザでコンポーネントを使うには jco などで JavaScript に変換する必要がある (推測。jco は確かめていない)。
- Shared-Everything Threads (Worker を使わないスレッドの提案): Phase 1 ([proposals](https://github.com/WebAssembly/proposals))。
- Document-Isolation-Policy: Chromium 系だけ (デスクトップ Chrome 137、Android 版 Chrome 146)。web-features では実験的扱い。

## 出典

- https://github.com/mdn/browser-compat-data (8.1.8、2026-11-02 生成。`webassembly.*`、`javascript.builtins.SharedArrayBuffer`、`api.crossOriginIsolated`、`http.headers.Cross-Origin-*`、`http.headers.Document-Isolation-Policy` の対応版と各ブラウザ版の公開日)
- https://github.com/web-platform-dx/web-features (3.45.0。Baseline の状態と到達日。https://webstatus.dev/features/<id> で同じデータを見られる)
- https://github.com/WebAssembly/website/blob/main/features.json (WebAssembly 公式の機能対応表のデータ。Safari の Memory64 フラグ、Stack Switching のフラグ、Firefox の Relaxed SIMD 145)
- https://github.com/WebAssembly/proposals (各提案の Phase)
- https://webassembly.org/news/2025-09-17-wasm-3.0/ (Wasm 3.0 の内容、ウェブでの Memory64 の 16GB 上限)
- https://www.w3.org/TR/2025/CRD-wasm-core-2-20250616 と https://webassembly.org/news/2025-03-20-wasm-2.0/ (Wasm 2.0 が CR Draft のまま evergreen 方式になったこと。検索結果の要約で確認)
- https://developer.chrome.com/blog/enabling-shared-array-buffer (Chrome 92 からデスクトップで SAB に分離が必須、Android は 88 から分離が前提、`credentialless` は Chrome 96)
- https://developer.chrome.com/blog/document-isolation-policy (Document-Isolation-Policy の値と性質、Chrome 137 はデスクトップのみ)
- https://web.dev/articles/coop-coep (分離で壊れるもの、Report-Only、iframe の `allow="cross-origin-isolated"`)
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer (SAB の前提条件と postMessage の挙動)
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy (`require-corp` と `credentialless` の違い)
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics/wait (メインスレッドで使えない)
- https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/instantiateStreaming_static (MIME 型の要件、CSP)
- https://v8.dev/blog/wasm-code-caching (V8 の Liftoff/TurboFan と Wasm コードキャッシュの条件)
- https://duckdb.org/docs/2.0/clients/wasm/overview.html、https://duckdb.org/docs/2.0/clients/wasm/extensions.html、https://duckdb.org/docs/2.0/clients/wasm/instantiation.html (DuckDB-Wasm のバンドル、spatial 拡張、制限)
- https://github.com/duckdb/duckdb-spatial/blob/main/vcpkg.json (spatial 拡張の依存)
- https://sqlite.org/wasm/doc/trunk/persistence.md (SQLite Wasm の VFS ごとの要件)
- https://github.com/bugra9/gdal3.js、https://github.com/chrispahm/geos-wasm、https://github.com/jjimenezshaw/wasm-proj、https://github.com/uber/h3-js、https://github.com/kylebarron/parquet-wasm (各ライブラリの内容とライセンス。npm レジストリで最新版と公開日も確認)
- https://github.com/maplibre/maplibre-gl-js (6.17.0、2026-11-07 公開。`SharedArrayBuffer` と `transferControlToOffscreen` がソースに出てこないことをコード検索で確認)

## 未確認のこと

- `script-src 'wasm-unsafe-eval'` の各ブラウザの対応版 (MDN の instantiateStreaming のページには書かれていない)
- iOS Safari で実際に確保できる Wasm メモリの上限 (端末のメモリ量による差を含む)
- Firefox と Safari の Wasm コンパイル結果キャッシュの条件 (V8 以外)
- DuckDB の文書は最新の安定版を 2.0.0 としているが、npm の `@duckdb/duckdb-wasm` の `latest` は 1.33.1-dev57.0 (2026-06-22 公開) で、配布物と文書の対応が取れていない
- DuckDB-Wasm の `spatial` 拡張が `wasm_threads` 向けにも配布されているか
- geos-wasm のライセンス表示の食い違い (GitHub は LGPL-2.1、npm は LGPL-3.0-or-later) のどちらが正しいか
- `@jansoft/mbujkanji-valhalla-wasm` の中身と、ほかにブラウザで動くルート検索エンジン (OSRM、GraphHopper など) の Wasm ビルドがあるか
- PMTiles の JavaScript 実装が Wasm を使っていないことの、ソースでの確認
- Wasm を LGPL ライブラリとして頒布するときの要件の法的な確認 (上の「落とし穴」のライセンスの項は条文の一般的な読み方による推測)
- jco などでの Component Model のブラウザ利用の実態
