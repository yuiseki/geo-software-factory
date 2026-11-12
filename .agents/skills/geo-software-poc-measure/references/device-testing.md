# 対象端末での確かめ方

対象: 実機、iOS シミュレータ、Android エミュレータ、クラウドの実機サービス、WebView での確かめ方。ブラウザの機能の対応を実行時に調べる方法。ヘッドレスのブラウザで地図を動かすときの注意

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

ヘッドレスのブラウザについての実測は 2026-11-11 に行った (Playwright 1.58.2、HeadlessChrome 145.0.7632.6、Linux、NVIDIA GeForce RTX 3060 のある計算機)。

## 概要

地図の描画は GPU と端末のメモリに強く依存し、エミュレーションでは再現しきれない。DevTools の CPU の throttling は手元の計算機に対する比で、携帯端末の CPU を本当には再現できない ([render-performance](render-performance.md))。この文書は、どの段階でどの手段を使うか (ヘッドレスの自動テスト、エミュレータ、実機、WebView の中) と、実機をつないで DevTools で見る手順、ブラウザの機能の対応を実行時に確かめる方法を書く。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| ヘッドレスのブラウザ (Playwright) | 画面の大きさ、DPR、タッチ (`isMobile`) をそろえて、同じ筋書きを自動で繰り返す。タイル数や回帰の比較に向く | GPU が使えず SwiftShader になることがある (下の実測)。Safari の実機の挙動は再現しない | Playwright 1.58.2 で実測 | https://playwright.dev/docs/api/class-browser |
| Android の実機 + chrome://inspect | 実機の Chrome や WebView を、USB でつないだ PC の DevTools で調べる | アプリの WebView は、アプリの側で `setWebContentsDebuggingEnabled(true)` を呼ばないと出ない (Android 4.4 以降) | Chrome DevTools | https://developer.chrome.com/docs/devtools/remote-debugging/webviews |
| iOS の実機とシミュレータ + Mac の Safari の Web インスペクタ | iOS の Safari や WKWebView の中の地図を、Mac の Safari の開発メニューから調べる | アプリの WKWebView は `isInspectable` を true にしないと調べられない (iOS 16.4、macOS 13.3 から。既定は false)。Mac が要る | Safari、WebKit | https://webkit.org/blog/13936/enabling-the-inspection-of-web-content-in-apps/ 、手順は https://developer.apple.com/documentation/safari-developer-tools/inspecting-ios (2026-11-11 に本文を取れず未確認) |
| クラウドの実機サービス | 手元に無い機種で、実機のブラウザを遠隔で動かす | 料金、機種、GPU の扱いはこの文書では確かめていない | BrowserStack、Sauce Labs、AWS Device Farm など | 未確認 |
| 実行時の機能の検出 | 端末で WebGL2 が使えるか、描画器の名前、最大のテクスチャの大きさ、WebGPU の有無、クロスオリジン分離の有無を、ページの中で調べて記録する | 拡張 `WEBGL_debug_renderer_info` が無い、または値をぼかすブラウザがある (推測) | ブラウザの標準 API | WebGPU は [webgpu](../../geo-software-arch/references/browser/webgpu.md)、クロスオリジン分離は https://developer.mozilla.org/en-US/docs/Web/API/Performance/measureUserAgentSpecificMemory |

## 判断を左右すること

- 対象端末の下限: 要件の対象端末のうち、いちばん遅い機種 (古い Android の低価格機など) を決める。速い機種で動いても、下限の機種で動く根拠にならない。
- ブラウザかアプリか: アプリの WebView は、ブラウザと版や機能が違うことがある。WebView で配るなら WebView の中で測る。
- ネイティブ SDK か Web か: MapLibre Native などのネイティブの SDK は、WebView の測り方とは別に、各 OS の道具で測る (未確認: この文書では手順を確かめていない)。
- 使う機能: WebGPU、Wasm のスレッド (クロスオリジン分離が要る)、オフラインの保存。端末ごとに使えるかが違うので、実行時に検出して記録する ([webgpu](../../geo-software-arch/references/browser/webgpu.md))。
- 何を確かめるか: 動くか (描ける、落ちない)、速さ ([render-performance](render-performance.md))、メモリで落ちないか (長く使ったとき、地物を増やしたとき)、操作 (タッチ、ピンチ、回転)。

## 手順

1. 対象端末の一覧から、下限の機種、主な機種、配る形 (ブラウザか WebView か) を決める。
2. ヘッドレスのブラウザで、画面の大きさと DPR を対象の機種に合わせて (例: 390 x 844、DPR 3、`isMobile: true`) 地図が描けることを確かめる。まず WebGL の描画器の名前を取り、地図の `idle` まで行くかを見る。
3. ページに機能の検出を入れる: `canvas.getContext('webgl2')` の成否、`WEBGL_debug_renderer_info` の描画器の名前、`MAX_TEXTURE_SIZE`、`'gpu' in navigator`、`crossOriginIsolated`、`devicePixelRatio`、画面の大きさ。結果を画面か計測の送り先に出す。
4. 実機をつなぐ。Android は USB デバッグを有効にし、PC の Chrome で chrome://inspect を開く。WebView は、試作のアプリで `setWebContentsDebuggingEnabled(true)` を呼ぶ。iOS は、試作のアプリで WKWebView の `isInspectable` を true にし、Mac の Safari の開発メニューから端末のページを選ぶ (端末側と Mac 側の設定の名前は、2026-11-11 に Apple の文書の本文を取れず未確認)。
5. 実機で、[tiles-per-view](tiles-per-view.md) と [render-performance](render-performance.md) と同じ筋書きを通し、描画器の名前、最初の idle までの時間、フレームの間隔を記録する。
6. 長く使ったときの確かめ: 同じ筋書きを数十回繰り返し、落ちないか、遅くならないかを見る。
7. 機種ごとの結果と、使えなかった機能を表にして、geo-software-arch (置き場所) と geo-software-library (ライブラリ) に渡す。

## 実測: ヘッドレスの Chromium で地図が描けないことがある

2026-11-11 に、Playwright 1.58.2 の `chromium.launch({headless: true})` を既定の引数で起動し (環境変数 `DISPLAY` は外した)、MapLibre GL JS 6.17.0 で OpenFreeMap の Liberty スタイルを開くと、「WebGL: CONTEXT_LOST_WEBGL」の警告が出て、スタイルの取得が `net::ERR_ABORTED` になり、15 秒たっても地図の `load` が来なかった。`channel: "chromium"` (新しいヘッドレス) でも同じだった。起動の引数に `--use-angle=swiftshader --enable-unsafe-swiftshader` を足すと、描画器が「ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)), SwiftShader driver)」になり、地図が `idle` まで描けた。Xvfb の上で画面つきの Chromium を動かしても、描画器は SwiftShader のままだった。

この計算機では、ヘッドレスで GPU の描画を使えず、ソフトウェアの描画でだけ地図が描けた。SwiftShader でのフレームの間隔は実機とかけ離れる ([render-performance](render-performance.md) の実測で約 6 fps)。ヘッドレスはタイル数と回帰の比較に使い、速さの判断は実機で行う。GPU のあるヘッドレスの構成が、他の計算機や他の版で動くかは確かめていない。

## 落とし穴

- エミュレーションの結果を端末の結果として書く: 画面の大きさと DPR はそろうが、GPU、メモリ、熱による速度の低下はそろわない。
- ヘッドレスで地図が描けないのを、試作の不具合と取り違える: 上の実測のとおり、WebGL の文脈が失われるとタイルを取りに行かず、タイル数も 0 になる。最初に描画器の名前と `load` の到達を確かめる。
- WebView を調べられない: アプリの側でデバッグを有効にしていないと、chrome://inspect にも Safari の開発メニューにも出ない。本番のビルドで有効のまま配らない (推測。公開アプリで有効にする是非はこの文書では確かめていない)。
- 機能の検出をせずに速さを比べる: 同じ機種でも、ブラウザの版や設定で WebGL2 や WebGPU が使えないことがある。描画器の名前と機能の有無を結果に残す。

## ライセンス上の注意

- ここで挙げた道具 (Playwright、Chrome DevTools、Safari の Web インスペクタ) を測るために使う分には、継承の義務は生じない。クラウドの実機サービスの規約 (画面の記録の扱いなど) は未確認。

## 出典

- https://playwright.dev/docs/api/class-browser (`deviceScaleFactor`、`isMobile`。2026-11-11 確認)
- https://developer.chrome.com/docs/devtools/remote-debugging/webviews (Android 4.4 以降、`setWebContentsDebuggingEnabled`、chrome://inspect。2026-11-11 確認)
- https://webkit.org/blog/13936/enabling-the-inspection-of-web-content-in-apps/ (`isInspectable`、既定は false、iOS 16.4 と macOS 13.3 から。2026-11-11 確認)
- https://developer.chrome.com/docs/devtools/performance/reference (DevTools は携帯端末の CPU を本当には再現できない。2026-11-11 確認)

## 未確認のこと

- iOS の端末と Mac の Safari で Web インスペクタを有効にする設定の名前と手順 (Apple の文書の本文を取れなかった)。
- クラウドの実機サービスの料金、機種、GPU の扱い。
- ネイティブの SDK (MapLibre Native など) の描画の速さとメモリを、各 OS の道具で測る手順。
- GPU を使うヘッドレスの Chromium の構成。
