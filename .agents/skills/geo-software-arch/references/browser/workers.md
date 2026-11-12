# Web Workers と OffscreenCanvas

対象: Dedicated / Shared Worker、OffscreenCanvas、Transferable と SharedArrayBuffer、Atomics、Web Locks、BroadcastChannel、scheduler.postTask

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 (ブラウザ対応は MDN browser-compat-data 8.1.8 (2026-11-02 生成) と web-features 3.45.0 で照合) |
| 仕様と標準化の段階 (W3C / WHATWG / WICG、草案か勧告か) | Dedicated / Shared Worker、OffscreenCanvas、BroadcastChannel、`structuredClone()`、`postMessage()` の transfer は WHATWG HTML Living Standard。SharedArrayBuffer と Atomics は ECMAScript (TC39) の標準。Web Locks は W3C Web Applications WG の Editor's Draft (2026-11-09 版)。`scheduler.postTask()` と `scheduler.yield()` は WICG の Prioritized Task Scheduling (草案) |
| Baseline の状態 (Widely available / Newly available / 未達) | Widely available: Dedicated Worker、Worker でのモジュール (2025-12-06 に到達)、OffscreenCanvas (2025-09-27)、Worker での `requestAnimationFrame()`、SharedArrayBuffer と Atomics、BroadcastChannel、Web Locks、`structuredClone()`、`ArrayBuffer.prototype.transfer()` (2026-09-05)。Newly available: Shared Worker と Shared Worker でのモジュール (Android 版 Chrome 148 の対応で 2026-05-05)、`Atomics.waitAsync()` (2025-11-11)、`Atomics.pause()` (2025-04-01)。未達: Scheduler API (Safari 未対応)、Transferable Streams (Safari 未対応)、Shared Worker の extendedLifetime (Chromium のみ) |

## ブラウザの対応

API ごとに、対応した版を書く。iOS では全ブラウザが WebKit を使うので、iOS Safari の欄が iOS 全体の対応になる。

| API | Chrome / Edge | Firefox | Safari (macOS) | Safari (iOS / iPadOS) | Android の WebView | 出典 |
|---|---|---|---|---|---|---|
| Dedicated Worker | Chrome 4 (Android 版は 18) / Edge 12 | 4 | 4 | 5 | 4.4 | [webstatus dedicated-workers](https://webstatus.dev/features/dedicated-workers) |
| モジュール Worker (`new Worker(url, {type: 'module'})`) | Chrome 80 / Edge 80 | 114 | 15 | 15 | 80 | [webstatus js-modules-workers](https://webstatus.dev/features/js-modules-workers) |
| Shared Worker | Chrome 5 (Android 版 Chrome は 148) / Edge 79 | 29 (Android 版は 33) | 16 (5〜6 で一度対応し 7 で削除) | 16 | 148 | [webstatus shared-workers](https://webstatus.dev/features/shared-workers) |
| Shared Worker でのモジュール | Chrome 80 (Android 版は 148) / Edge 80 | 114 | 16 | 16 | 148 | [webstatus js-modules-shared-workers](https://webstatus.dev/features/js-modules-shared-workers) |
| Shared Worker の `extendedLifetime` | Chrome 148 / Edge 148 | 未対応 | 未対応 | 未対応 | 未確認 | [webstatus shared-workers-extended-lifetime](https://webstatus.dev/features/shared-workers-extended-lifetime) |
| OffscreenCanvas と `transferControlToOffscreen()` (2D) | Chrome 69 / Edge 79 | 105 | 16.4 | 16.4 | 69 | [webstatus offscreen-canvas](https://webstatus.dev/features/offscreen-canvas) |
| OffscreenCanvas の WebGL / WebGL2 | Chrome 69 / Edge 79 | 105 | 17 | 17 | 69 | [MDN BCD](https://github.com/mdn/browser-compat-data) (`api.OffscreenCanvas.getContext.webgl_context`) |
| OffscreenCanvas の WebGPU | Chrome 113 (ChromeOS、macOS、Windows。144 から Linux の一部 GPU も)、Android 版 Chrome 121 / Edge 同じ | 141 (Windows のみの部分対応) | 26 | 26 | 121 | [MDN BCD](https://github.com/mdn/browser-compat-data) (`api.OffscreenCanvas.getContext.webgpu_context`) |
| Worker での `requestAnimationFrame()` | Chrome 69 (入れ子の Worker では不可) / Edge 79 | 99 | 16.4 | 16.4 | 67 | [webstatus request-animation-frame-workers](https://webstatus.dev/features/request-animation-frame-workers) |
| `structuredClone()` | Chrome 98 / Edge 98 | 94 | 15.4 | 15.4 | 98 | [webstatus structured-clone](https://webstatus.dev/features/structured-clone) |
| `ArrayBuffer.prototype.transfer()` | Chrome 114 / Edge 114 | 122 | 17.4 | 17.4 | 114 | [webstatus transferable-arraybuffer](https://webstatus.dev/features/transferable-arraybuffer) |
| Transferable Streams | Chrome 87 / Edge 87 | 103 | 未対応 | 未対応 | 未確認 | [webstatus transferable-streams](https://webstatus.dev/features/transferable-streams) |
| `SharedArrayBuffer` (クロスオリジン分離が必要) | Chrome 68 (Android 版は 89) / Edge 79 | 79 | 15.2 | 15.2 | 未対応 | [webstatus shared-memory](https://webstatus.dev/features/shared-memory) |
| `Atomics.wait()` (Worker のみ) | Chrome 68 (Android 版は 89) / Edge 79 | 78 (Android 版は 79) | 15.2 | 15.2 | 89 | [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics/wait) |
| `Atomics.waitAsync()` | Chrome 90 (87〜89 はタイムアウトしない部分実装) / Edge 90 | 145 | 16.4 | 16.4 | 90 | [webstatus atomics-wait-async](https://webstatus.dev/features/atomics-wait-async) |
| `Atomics.pause()` | Chrome 133 / Edge 133 | 137 | 18.4 | 18.4 | 133 | [webstatus atomics-pause](https://webstatus.dev/features/atomics-pause) |
| Web Locks (`navigator.locks`) | Chrome 69 / Edge 79 | 96 | 15.4 | 15.4 | 69 | [webstatus web-locks](https://webstatus.dev/features/web-locks) |
| BroadcastChannel | Chrome 54 / Edge 79 | 38 | 15.4 | 15.4 | 54 | [webstatus broadcast-channel](https://webstatus.dev/features/broadcast-channel) |
| `scheduler.postTask()` | Chrome 94 / Edge 94 | 142 | 未対応 | 未対応 | 94 | [webstatus scheduler](https://webstatus.dev/features/scheduler) |
| `scheduler.yield()` | Chrome 129 / Edge 129 | 142 | 未対応 | 未対応 | 129 | [webstatus scheduler](https://webstatus.dev/features/scheduler) |

Chrome の対応版は Android 版 Chrome も同じ (違うものは欄内に書いた)。主な版の公開日: Chrome 148 は 2026-05-05、Firefox 142 は 2025-08-19、Firefox 145 は 2025-11-11、Safari 16.4 は 2023-03-27 (BCD の browsers データ)。

## 概要

Web Worker はメインスレッドとは別のスレッドで JavaScript (と Wasm) を動かす仕組みで、Dedicated Worker は 1 つのページ専用、Shared Worker は同じオリジンの複数のタブから共有される。スレッド間のデータは `postMessage()` で構造化複製されるか、`ArrayBuffer` などを transfer リストに入れてコピーなしで所有権ごと移すか、クロスオリジン分離されたページでは `SharedArrayBuffer` と `Atomics` でメモリを共有して受け渡す。OffscreenCanvas を使うと canvas の描画 (2D、WebGL、WebGPU) を Worker に移せる。Web Locks と BroadcastChannel はタブや Worker をまたいだ排他制御と通知、`scheduler.postTask()` はメインスレッドの仕事に優先度を付ける API である。

## 地図プロダクトでの使いどころ

保存、計算、表現のどれを、ブラウザ・アプリの層に置けるようにするか。

- 保存: OPFS の同期アクセスを使う SQLite Wasm の VFS (`opfs`、`opfs-sahpool`、`opfs-wl`) はどれも Worker でしか動かない ([SQLite persistence](https://sqlite.org/wasm/doc/trunk/persistence.md))。オフライン地図のタイルや POI を端末の DB に持つなら、DB を Worker に置き、複数タブからの書き込みは Web Locks で直列化し、更新の通知は BroadcastChannel で配る構成になる (推測)。`opfs-wl` は Web Locks を使って FIFO で順番を回す ([SQLite persistence](https://sqlite.org/wasm/doc/trunk/persistence.md))。Shared Worker に DB を 1 つだけ置けばタブ間の競合自体を避けられるが、Android 版 Chrome での対応は 148 (2026-05-05) からと新しい。
- 計算: ベクタタイルのデコード、GeoJSON のタイル分割やクラスタリング、ラベル用の配置計算、座標変換、Wasm の空間演算 (GEOS、DuckDB など) を Worker に置けば、パンやズーム中のメインスレッドを止めずに済む。MapLibre GL JS はタイルの解析と GeoJSON の処理を Worker で行い、6.15.0 からは登録した CRS への GeoJSON の投影も Worker で行う ([CHANGELOG](https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md))。
- 表現: OffscreenCanvas の WebGL を Worker で使えば、地図の描画そのものをメインスレッドから外せる。WebGL の OffscreenCanvas は Safari 17 から対応なので、iOS 17 未満を切れば全主要ブラウザで成り立つ。ただし MapLibre GL JS 6.17.0 は `transferControlToOffscreen` を使っておらず、描画はメインスレッドの WebGL で行う (コード検索の結果からの推測)。MapLibre は 6.9.0 から、スプライトの画素を読み戻すときに 2D の OffscreenCanvas を使ってメインスレッドの数十ミリ秒の停止を避けている ([CHANGELOG](https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md))。

## 制約

- 容量と寿命: Dedicated Worker の寿命は作ったページに従う。iOS はページがバックグラウンドにある間にメモリ節約のため Worker を止めることがあり、MapLibre GL JS では復帰後にタイルを一切読めなくなる不具合が起き、6.16.0 (2026-10-25 公開) で Worker を作り直す処理 (`WorkerPool.restart()`) が入った ([CHANGELOG](https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md)、[issue #8461](https://github.com/maplibre/maplibre-gl-js/issues/8461)、[worker_pool.ts](https://github.com/maplibre/maplibre-gl-js/blob/main/src/util/worker_pool.ts))。Worker に状態を持たせる設計では、Worker が消えたときに状態を送り直せるようにしておく。Shared Worker は最後のクライアントが閉じると終わるが、Chromium 148 からは `extendedLifetime` で延ばせる ([webstatus](https://webstatus.dev/features/shared-workers-extended-lifetime))。
- 権限とユーザーの操作が要るか: どの API も権限プロンプトは出ない。CSP を設定しているページでは Worker のスクリプトの取得元を `worker-src` (なければ `script-src`) で許可する必要がある (推測。MDN は確かめていない)。
- セキュアコンテキスト、クロスオリジン分離 (COOP/COEP) などの前提: `SharedArrayBuffer` を作ったり `postMessage()` で渡したりするには、セキュアコンテキストかつクロスオリジン分離されたページである必要がある。条件を満たさないと SAB を `postMessage()` すると例外になる ([MDN SharedArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer))。分離のコストは [wasm.md](wasm.md) の「制約」を参照。`Atomics.wait()` はメインスレッドでは呼べず、メインスレッドで待つには `Atomics.waitAsync()` を使う ([MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics/wait))。transfer (`ArrayBuffer` などの所有権の移動) は分離を必要としないので、地図ライブラリの多くは SAB ではなく transfer でタイルのバイト列を渡す (MapLibre はソースで確認、ほかは推測)。
- iOS / Safari での制限: `scheduler.postTask()` と `scheduler.yield()` がなく、Transferable Streams もない。OffscreenCanvas の WebGL は Safari 17 から、WebGPU は Safari 26 から。Shared Worker の中では Worker を作れない (Safari、Chromium とも。BCD の注記)。
- WebView (アプリに埋め込んだブラウザ) での制限: Android の WebView は `SharedArrayBuffer` に対応しない (BCD) ので、SAB と Atomics を前提にしたスレッド共有は使えず、transfer で組む。Shared Worker は Android の WebView では 148 から。

## 地図の実装例

この API を使っている OSS やライブラリ (地図ライブラリ、PMTiles、DuckDB-Wasm など)。

- MapLibre GL JS 6.17.0 (2026-11-08 JST、UTC では 11-07 公開): Worker のプールを持ち、既定の数は Safari では論理コア数の半分 (1 以上 3 以下)、それ以外では 1 である。数は `setWorkerCount()` で変えられる ([worker_pool.ts](https://github.com/maplibre/maplibre-gl-js/blob/main/src/util/worker_pool.ts))。メインスレッドと Worker の通信 (`Actor`) は独自の serialize の後に `postMessage(message, {transfer: buffers})` で `ArrayBuffer` を transfer する ([actor.ts](https://github.com/maplibre/maplibre-gl-js/blob/main/src/util/actor.ts))。6.0.0 (2026-07-22 公開) で ESM のみの配布になり、Worker は実ファイルの URL からモジュール Worker として読み込まれるので `worker-src blob:` が不要になり、CSP 専用ビルドは廃止された。モジュール Worker を作れない環境ではクラシック Worker に戻り、`setWorkerUrl()` で URL を指定できる ([CHANGELOG](https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md)、[web_worker.ts](https://github.com/maplibre/maplibre-gl-js/blob/main/src/util/web_worker.ts))。6.13.0 から既定の Worker の URL に版をクエリ `v` として付け、古い Worker がキャッシュから読まれて壊れるのを防いでいる。`addProtocol()` で登録したプロトコルや `registerWorkerSource()` で、利用者のコードも Worker 側で動かせる。
- DuckDB-Wasm: 本体は Worker で動き、`coi` バンドルでは pthread 用の Worker も使う ([instantiation](https://duckdb.org/docs/2.0/clients/wasm/instantiation.html))。
- SQLite Wasm: OPFS を使う VFS は Worker 専用 ([sqlite-wasm](https://github.com/sqlite/sqlite-wasm))。
- gdal3.js: Worker で動かす版と動かさない版、そのモジュール版がある ([README](https://github.com/bugra9/gdal3.js))。

## 落とし穴

- `postMessage()` で `ArrayBuffer` を transfer に入れ忘れると構造化複製でコピーされ、大きなタイルや点群で時間とメモリを食う。transfer した後は送った側のバッファは切り離されて使えなくなる。
- MapLibre GL JS の既定の Worker 数は Safari 以外では 1 なので、大量の GeoJSON や重いタイルを扱う地図では解析がボトルネックになりうる。Worker は最初の地図を作るときに遅延して作られ、`prewarm()` を使う場合は `setWorkerUrl()` と `setWorkerCount()` をその前に呼ばないと効かない ([global_worker_pool.ts のコメント](https://github.com/maplibre/maplibre-gl-js/blob/main/src/util/global_worker_pool.ts))。
- `GeoJSONSource.setData()` を Worker の処理より速く呼び続けると、MapLibre 6.12.0 より前はメモリが増え続けてページが落ちた ([CHANGELOG](https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md))。リアルタイムの位置情報を流す地図では、更新の頻度を Worker の処理能力に合わせて間引く。
- フィンガープリント対策をしているブラウザでは、OffscreenCanvas の `getImageData()` が改変された画素を返すことがある。MapLibre はこれを検出する関数 (`offscreen_canvas_distorted.ts`) を持っている ([ソース](https://github.com/maplibre/maplibre-gl-js/blob/main/src/util/offscreen_canvas_distorted.ts))。画素を読み戻して判定する処理 (色による当たり判定など) は、この環境で誤動作しうる (推測)。
- iOS ではバックグラウンドで Worker が止められることがある。MapLibre の 6.16.0 より前の版、または独自の Worker を使うコードでは、タブ復帰後に地図が更新されなくなる ([issue #8461](https://github.com/maplibre/maplibre-gl-js/issues/8461))。
- Worker の数を増やすと、Worker ごとにスクリプトと Wasm のインスタンス (メモリ) を持つので、モバイルでは逆にメモリ不足になりうる (推測)。
- `scheduler.postTask()` は Safari で使えないので、使うなら機能検出して `setTimeout` などに戻す。

## まだ使えないもの、これから使えるもの

提案中、Origin Trial 中、一部のブラウザだけのもの。

- `scheduler.postTask()` と `scheduler.yield()`: Chromium と Firefox 142 から。Safari は未対応で Baseline 未達。
- Shared Worker の `extendedLifetime`: Chromium 148 のみ。
- Transferable Streams: Chromium と Firefox だけで、Safari は未対応。タイルのストリームを Worker へそのまま渡す構成は iOS で使えない。
- OffscreenCanvas の WebGPU: Chrome は 144 で Linux の一部 GPU に広がった段階、Firefox は Windows のみの部分対応、Safari 26 は対応。
- Wasm の Shared-Everything Threads (Worker を立てずにスレッドを持つ提案) は Phase 1 ([WebAssembly proposals](https://github.com/WebAssembly/proposals))。

## 出典

- https://github.com/mdn/browser-compat-data (8.1.8、2026-11-02 生成。`api.Worker`、`api.SharedWorker`、`api.OffscreenCanvas.*`、`api.HTMLCanvasElement.transferControlToOffscreen`、`api.DedicatedWorkerGlobalScope.requestAnimationFrame`、`api.LockManager`、`api.BroadcastChannel`、`api.Scheduler.*`、`api.structuredClone`、`javascript.builtins.SharedArrayBuffer`、`javascript.builtins.Atomics.*`、`javascript.builtins.ArrayBuffer.transfer` の対応版と注記、各版の公開日)
- https://github.com/web-platform-dx/web-features (3.45.0。Baseline の状態と到達日。https://webstatus.dev/features/<id> で同じデータを見られる)
- https://w3c.github.io/web-locks/ (Web Locks が W3C Web Applications WG の Editor's Draft であること)
- https://wicg.github.io/scheduling-apis/ (Scheduler API の仕様。BCD の spec_url)
- https://html.spec.whatwg.org/multipage/workers.html と https://html.spec.whatwg.org/multipage/canvas.html#the-offscreencanvas-interface (Worker と OffscreenCanvas の仕様。BCD の spec_url)
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer (SAB の前提条件と postMessage の挙動)
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics/wait (メインスレッドで使えないこと)
- https://sqlite.org/wasm/doc/trunk/persistence.md (OPFS の VFS が Worker 専用であること、`opfs-wl` の要件)
- https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md (6.0.0 の ESM 化と Worker の読み込み方、6.9.0 の OffscreenCanvas、6.12.0 の setData のメモリ、6.13.0 の Worker の URL、6.15.0 の Worker での投影、6.16.0 の iOS の Worker 停止への対処)
- https://github.com/maplibre/maplibre-gl-js/blob/main/src/util/worker_pool.ts、https://github.com/maplibre/maplibre-gl-js/blob/main/src/util/web_worker.ts、https://github.com/maplibre/maplibre-gl-js/blob/main/src/util/actor.ts (Worker 数の既定値、モジュール Worker と既定の URL、transfer の使い方)
- https://registry.npmjs.org/maplibre-gl (6.0.0 は 2026-07-22、6.16.0 は 2026-10-25、6.17.0 は 2026-11-07 公開)
- https://duckdb.org/docs/2.0/clients/wasm/instantiation.html (DuckDB-Wasm の Worker と pthread Worker)
- https://github.com/bugra9/gdal3.js (Worker 版の有無)

## 未確認のこと

- Android の WebView での Shared Worker の `extendedLifetime` と Transferable Streams の対応
- iOS が Worker を止める条件 (どの iOS の版から、どのくらいバックグラウンドにあると止まるか)。MapLibre の issue #8461 の本文は読めなかった
- CSP の `worker-src` の扱いの各ブラウザでの違い
- OpenLayers、deck.gl、loaders.gl など MapLibre 以外の地図ライブラリが Worker、OffscreenCanvas、SharedArrayBuffer をどう使っているか
- OffscreenCanvas の WebGL で地図全体を Worker 描画する OSS の地図ライブラリがあるか
- Worker を増やしたときのモバイルでのメモリ増加の実測値
