# WebGPU と WebGL

対象: WebGPU (描画と計算シェーダー)、WebGL2、WGSL、地図ライブラリと可視化ライブラリの対応状況

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 (JST)。この日の安定版は Chrome 157、Firefox 159.0.1 |
| 仕様と標準化の段階 (W3C / WHATWG / WICG、草案か勧告か) | WebGPU は W3C GPU for the Web Working Group の Candidate Recommendation Draft (2026-09-15 版)。WGSL も同 WG の Candidate Recommendation Draft (2026-11-06 版)。WebGL2 は Khronos の仕様で W3C の外 |
| Baseline の状態 (Widely available / Newly available / 未達) | WebGPU は未達 (Limited availability)。Firefox が Linux、Intel Mac、Android で未出荷のため。WebGL2 は Widely available (Newly 2021-09-20、Widely 2024-03-20) |

## ブラウザの対応

API ごとに、対応した版を書く。iOS では全ブラウザが WebKit を使うので、iOS Safari の欄が iOS 全体の対応になる。

| API | Chrome / Edge | Firefox | Safari (macOS) | Safari (iOS / iPadOS) | Android の WebView | 出典 |
|---|---|---|---|---|---|---|
| WebGPU (描画と計算) | Windows / macOS / ChromeOS は 113。Linux は 144 (Intel Gen12 以降の GPU のみ)、NVIDIA は 147 (Wayland、ドライバ 535.183.01 以上)。Windows ARM64 はフラグのみ。Android 版 Chrome は 121 (Android 12 以上、Qualcomm / ARM の GPU)、Imagination の GPU は 139 (Android 16 以上)。Edge も同じ版 | Windows は 141。macOS は Apple シリコンの macOS 26 で 145、それより古い macOS の Apple シリコンで 147。Intel Mac、Linux、Android は未出荷 (Linux は Nightly のみ) | 26 (macOS 26 Tahoe 以降が必要。Safari 26 を macOS 15 で動かしても使えない) | 26 (iOS / iPadOS 26 以降) | MDN の互換表は Android 版 Chrome をミラーして 121 とする。WebView 個別の出荷記録は確かめられなかった | [gpuweb 実装状況](https://github.com/gpuweb/gpuweb/wiki/Implementation-Status)、[MDN BCD GPU.json](https://github.com/mdn/browser-compat-data/blob/main/api/GPU.json)、[webstatus.dev](https://webstatus.dev/features/webgpu)、[WebKit bug 299237](https://bugs.webkit.org/show_bug.cgi?id=299237) |
| WGSL (WebGPU のシェーダー言語) | WebGPU と同じ | WebGPU と同じ | WebGPU と同じ | WebGPU と同じ | WebGPU と同じ | [WGSL 仕様](https://www.w3.org/TR/WGSL/)、[WebKit Features in Safari 26.0](https://webkit.org/blog/17333/) |
| WebGPU 互換モード (`featureLevel: "compatibility"`、OpenGL ES 3.1 や Direct3D 11 の端末向け) | 146 (デスクトップ、Android)。Origin Trial は 139〜145 | 未対応 | 出荷予定なし (Intent に「Apple は Safari で出荷する見込みはない」とある) | 出荷予定なし | 146 | [chromestatus 6436406437871616](https://chromestatus.com/feature/6436406437871616)、[Intent to Ship](https://go.mail-archive.com/blink-dev@chromium.org/msg15559.html) |
| WebGPU subgroups | 144 (Android 版も 144) | 未対応 | 未対応 | 未対応 | 確かめられなかった | [webstatus.dev webgpu-subgroups](https://webstatus.dev/features/webgpu-subgroups) |
| WebGL2 (フォールバック先) | 56。Android 版 Chrome は 58。Edge は 79 | 51 | 15 | 15 | 58 (MDN の互換表のミラー値) | [webstatus.dev webgl2](https://webstatus.dev/features/webgl2)、[MDN BCD WebGL2RenderingContext.json](https://github.com/mdn/browser-compat-data/blob/main/api/WebGL2RenderingContext.json) |

## 概要

WebGPU は GPU を描画と汎用計算 (compute シェーダー) の両方に使う API で、シェーダーは WGSL で書く。WebGL2 には compute シェーダーがなく、集計や画像処理は描画パイプラインに押し込む工夫が要ったが、WebGPU ではストレージバッファを読み書きする計算をそのまま書ける。Worker からも `WorkerNavigator.gpu` で使える。2026-11 時点で Chromium と Safari 26 は既定で有効だが、Firefox は Windows と Apple シリコンの Mac だけで、Baseline には届いていない。

## 地図プロダクトでの使いどころ

保存、計算、表現のどれを、ブラウザ・アプリの層に置けるようにするか。

- 保存: WebGPU は保存の API ではない。GPU のバッファとテクスチャはページ (正確には GPUDevice) が生きている間だけのもので、永続化は OPFS、IndexedDB、Cache API など別の API に任せる。PMTiles や GeoParquet をブラウザに置く構成と組み合わせ、読み込んだデータを GPU に上げて使う形になる (推測)
- 計算: 点群やポイントデータの集計 (グリッド、六角形、ヒートマップ)、ラスターの再分類や陰影計算、等値線の生成、点群の間引きといった並列処理をクライアントに移せる。deck.gl 9.4 は ScreenGridLayer、HexagonLayer、ContourLayer、GridLayer、HeatmapLayer の集計を WebGPU で動かす。サーバーで事前集計していた処理をブラウザで対話的にやり直せるので、クラウド側の計算を減らせる (推測)
- 表現: 大量の点、線、メッシュ、点群、ガウシアンスプラットの描画。MapLibre GL JS など主要な地図ライブラリの描画は 2026-11 時点で WebGL2 なので、ベースマップは WebGL2、重い重ね合わせ (点群、集計) は WebGPU という分担が現実的になる (推測)

## 制約

- 容量と寿命: 仕様の既定の上限は `maxBufferSize` が 268,435,456 バイト (256 MiB)、`maxStorageBufferBindingSize` が 134,217,728 バイト (128 MiB)、`maxStorageBuffersPerShaderStage` が 8、`maxComputeInvocationsPerWorkgroup` が 256、`maxComputeWorkgroupStorageSize` が 16,384 バイト。これを超える値は `requestDevice()` で要求でき、端末が許す範囲で使える。GPU 側のデータはデバイスが失われる (device lost) と消えるので、作り直す処理が要る
- 権限とユーザーの操作が要るか: 権限ダイアログもユーザー操作も要らない
- セキュアコンテキスト、クロスオリジン分離 (COOP/COEP) などの前提: セキュアコンテキスト (HTTPS) が必須。COOP/COEP は要らない (ただし Wasm のマルチスレッドと組み合わせる場合はそちらが要る)。Firefox は Service Worker からは使えない
- iOS / Safari での制限: iOS / iPadOS / macOS とも 26 以降でないと `navigator.gpu` が無い。iOS 18 以前の端末には WebGL2 のフォールバックが必須。Safari は互換モードを出荷しない見込みなので、互換モード前提の設計は Safari では効かない (コア機能の範囲で書けば動く)
- WebView (アプリに埋め込んだブラウザ) での制限: Android WebView は MDN の互換表上は Android 版 Chrome と同じ扱いで、端末の GPU と Android の版に左右される。iOS の WKWebView については、Apple の開発者フォーラムで WebKit 側の回答者が「既定で有効になれば WKWebView でも動く」と書いているが、公式文書では確かめられなかった

## 地図の実装例

この API を使っている OSS やライブラリ (地図ライブラリ、PMTiles、DuckDB-Wasm など)。

- MapLibre GL JS (BSD-3-Clause): 2026-11-07 の v6.17.0 時点で描画は WebGL2 のみ。v6.0.0 (2026-07-22) で WebGL1 を廃止し WebGL2 必須にした。WebGPU は追跡 Issue #7640 の Phase 5 として「同じ drawable を実行する 2 つ目のバックエンドを遅延読み込みのチャンクで出す」計画で、Phase 1 と 2 が完了、Phase 3 (drawable 化) の途中。PoC の PR #7411 は閉じられた
- MapLibre Native: WebGPU バックエンドを 2025-10 に出した (Dawn と wgpu の両対応)。ネイティブ向けだが、ロードマップには Web ターゲットとしても使う意図が書かれている
- deck.gl (MIT): luma.gl の WebGPU アダプターを `deviceProps: {type: 'webgpu', adapters: [webgpuAdapter]}` で明示的に選ぶと WebGPU で動く。公式ガイドは「v9 の WebGPU 対応は作業中で本番向けではない」と明記。9.4 (2026-09-05) でコア、集計、メッシュ、Geo の主要レイヤーが対応、ピッキングも非同期で対応。一方で拡張の多く、PostProcessEffect、ベースマップとのインターリーブ、GPU transform は未対応で、TextLayer の背景と衝突判定は WebGL が要る。CARTO のレイヤーは WebGPU 実装なし
- luma.gl (MIT): 9.2 で「本番品質の WebGPU バックエンド」をうたい、全サンプルが WebGPU と WebGL の両方で動く。v10 は 2026-11 時点で alpha (v10.0.0-alpha.12、2026-11-10 JST)。compute と描画のパイプラインをまとめて扱う command graph は実験的
- three.js (MIT): `WebGPURenderer` は WebGPU が使えればそれを使い、使えなければ WebGL2 バックエンドに自動で落ちる。`forceWebGL: true` で WebGL2 を強制できる。最新は r187 (2026-10-30)
- CesiumJS (Apache-2.0): 1.147 (2026-11-02) 時点で WebGPU 対応は無い。2017 年からの Issue #4989 「WebGPU renderer」が開いたまま。WebGL2 が既定で、ボクセル描画などは WebGL2 必須
- ArcGIS Maps SDK for JavaScript (商用): 5.1 のシステム要件は「WebGL2 が使える 64 ビットのブラウザのみ」。WebGPU の記載は無い
- Mapbox GL JS: v3 で WebGL1 をやめ WebGL2 必須にした。最新 v3.34.2 (2026-11-03) までの変更履歴に WebGPU の記載は無い。ライセンスは v2 以降 OSI のオープンソースではなく Mapbox の利用規約に基づくもので、有効な Mapbox アカウントがある開発者が Mapbox の製品と組み合わせる場合に限り利用と改変が認められる。課金や計測に関わる部分の改変は不可、アカウントを失うとライセンスも終わる。再配布や Mapbox 以外のタイルとの組み合わせ、SaaS への組み込みは規約の範囲でしかできない
- OpenLayers (BSD-2-Clause): 10.11.0 (2026-10-04) 時点で WebGL レイヤーは WebGL1 のコンテキスト (`webgl` / `experimental-webgl`) を取る。WebGL2 への移行 Issue #13367 が開いたままで、WebGPU の計画は見当たらない
- Potree-Next: 大規模点群を WebGPU で描く Potree の書き直し。3D Tiles とガウシアンスプラットも扱う。ライセンスは AGPL-3.0 (別ライセンスは作者に要相談)。組み込んで配布する場合はアプリ全体を AGPL で公開する義務が及びうる。改変して配布するなら改変後のソースを AGPL で公開する。SaaS としてネットワーク越しに使わせる場合も、利用者に改変後のソースを提供する義務がある (AGPL 第 13 条)。作者自身が「AGPL は SaaS の抜け穴を塞ぐ」と書いている

## 落とし穴

- `navigator.gpu` があっても `requestAdapter()` が null を返すことがある (ブロックリストの GPU、ドライバの問題)。機能検出は `navigator.gpu` の有無と adapter の取得の両方で行い、WebGL2 への切り替えを用意する
- WGSL には 64 ビット浮動小数点型が無い。緯度経度や Web メルカトルの座標を 32 ビット浮動小数点で扱うと高ズームで精度が足りないので、タイル原点からの相対座標や分割した高精度表現にする必要がある (WebGL2 と同じ問題)
- WGSL のアトミック型は `u32` と `i32` (と拡張の `vec2<u32>`) だけで、浮動小数点のアトミック加算が無い。重み付き集計は固定小数点に変換して整数で足し込む工夫が要る (推測)
- 既定の上限は 1 回のバインドで 128 MiB。大きな点群や高解像度ラスターは分割して扱う前提で設計する
- WebGPU の描画と WebGL2 のベースマップは別のコンテキストになる。deck.gl の WebGPU はベースマップとのインターリーブ (地図のラベルの下に差し込む) に未対応で、重ね合わせしかできない
- Linux の Chrome は 144 まで既定で無効、Intel Gen12 より古い GPU や AMD はまだ対象外。社内の検証端末が Linux だと「動かない」と誤解しやすい
- Firefox の Android 版、Linux 版、Intel Mac 版は 2026-11 時点で未出荷。Firefox 利用者には WebGL2 の経路が必ず要る

## まだ使えないもの、これから使えるもの

提案中、Origin Trial 中、一部のブラウザだけのもの。

- Firefox の Linux 版 (Bugzilla 2006676 「[meta] Release WebGPU on Linux」が NEW のまま) と Intel Mac 版 (2004105) と Android 版。gpuweb の実装状況ページは Linux を 2026 年中の出荷見込みとしている
- WebGPU 互換モードは Chromium だけ。Safari は出荷しない見込み
- subgroups は Chromium 144 以降だけ
- MapLibre GL JS の WebGPU バックエンドは計画段階 (Phase 5)。時期の記載は無い
- deck.gl の WebGPU は「本番向けではない」と公式が明記している段階
- luma.gl v10 は alpha

## 出典

- https://github.com/gpuweb/gpuweb/wiki/Implementation-Status (ブラウザと OS ごとの WebGPU の出荷版、Linux と Android の GPU 条件)
- https://github.com/mdn/browser-compat-data/blob/main/api/GPU.json (Chrome 144 で Linux を追加、Firefox の OS ごとの注記、WebView のミラー値)
- https://api.webstatus.dev/v1/features/webgpu (Baseline が limited、各ブラウザの版と日付)
- https://api.webstatus.dev/v1/features?q=name:webgl2 (WebGL2 の Baseline と版)
- https://www.w3.org/TR/webgpu/ (Candidate Recommendation Draft 2026-09-15、既定の上限値)
- https://www.w3.org/TR/WGSL/ (Candidate Recommendation Draft 2026-11-06、アトミック型が u32 / i32)
- https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API (セキュアコンテキスト必須、Worker での利用、Baseline 未達)
- https://caniuse.com/webgpu (Safari 26 は部分対応の扱い、Firefox は既定で無効の扱い)
- https://webkit.org/blog/17333/ (Safari 26.0 で macOS、iOS、iPadOS、visionOS に WebGPU を出荷)
- https://bugs.webkit.org/show_bug.cgi?id=299237 (navigator.gpu は macOS Tahoe、iOS 26、visionOS 26 以降が必要)
- https://developer.apple.com/forums/thread/770862 (WKWebView での扱いについての WebKit 側の回答。公式文書ではない)
- https://developer.chrome.com/blog/new-in-webgpu-121 (Android 版 Chrome 121 の条件)
- https://chromestatus.com/feature/6436406437871616 と https://go.mail-archive.com/blink-dev@chromium.org/msg15559.html (互換モードの出荷版と Safari の見込み)
- https://bugzilla.mozilla.org/show_bug.cgi?id=2006676 と https://bugzilla.mozilla.org/show_bug.cgi?id=2004105 (Firefox の Linux と Intel Mac が未出荷)
- https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md (v6.0.0 で WebGL1 廃止、WebGPU の記載なし)
- https://github.com/maplibre/maplibre-gl-js/issues/7640 (Graphics Modernization の各 Phase と進み具合)
- https://maplibre.org/roadmap/maplibre-gl-js/graphics-modernization (GL JS の WebGPU 計画)
- https://maplibre.org/roadmap/maplibre-native/webgpu (MapLibre Native の WebGPU バックエンド、2025-10 リリース)
- https://deck.gl/docs/developer-guide/webgpu (deck.gl の WebGPU 対応表、有効化の方法、本番向けでない旨)
- https://luma.gl/docs/whats-new (luma.gl 9.2、9.3、10.0 の WebGPU 関連)
- https://threejs.org/docs/pages/WebGPURenderer.html (WebGL2 への自動フォールバックと forceWebGL)
- https://github.com/CesiumGS/cesium/blob/main/CHANGES.md と https://github.com/CesiumGS/cesium/issues/4989 (WebGPU 未対応)
- https://developers.arcgis.com/javascript/latest/guide/system-requirements/ (5.1 は WebGL2 必須)
- https://github.com/mapbox/mapbox-gl-js/blob/main/CHANGELOG.md と https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt (WebGL2 必須化、ライセンス条件)
- https://github.com/openlayers/openlayers/blob/main/src/ol/webgl.js と https://github.com/openlayers/openlayers/issues/13367 (WebGL1 のコンテキスト、WebGL2 移行が未完)
- https://github.com/m-schuetz/Potree-Next (WebGPU による点群描画、AGPL-3.0)
- 各リポジトリの GitHub Releases (deck.gl 9.4.0 / 9.4.1、MapLibre GL JS 6.17.0、CesiumJS 1.147、three.js r187、Mapbox GL JS 3.34.2、OpenLayers 10.11.0、luma.gl 10.0.0-alpha.12 の日付)

## 未確認のこと

- Android WebView で WebGPU が実際に既定で有効になった版 (MDN の互換表は Android 版 Chrome のミラー値 121 としているだけ)
- iOS の WKWebView と SFSafariViewController で WebGPU が Safari と同じ条件で使えるか (フォーラムの回答のみ)
- Firefox の Linux 版の出荷時期 (2026 年中という見込みしか無い)
- Samsung Xclipse など Android の他の GPU での出荷時期 (gpuweb の表で TBD)
- iOS の Safari で WebGPU に使えるメモリの実効上限 (仕様の既定値以外の、端末ごとの値)
- ArcGIS Maps SDK for JavaScript と Mapbox GL JS に WebGPU の非公開の計画があるか
- caniuse が Safari 26 を「部分対応」とする理由の詳細
