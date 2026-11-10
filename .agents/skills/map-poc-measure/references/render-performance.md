# 描画の速さの測り方

対象: 地図ライブラリの `idle` などのイベント、フレームの間隔、メモリ、Core Web Vitals、Lighthouse の測り方と、測る条件のそろえ方

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

実測は 2026-11-11 に行った。条件は下の「実測」の節に書く。

## 概要

描画の速さは「最初に地図が描き終わるまでの時間」「パン、ズーム、回転のときのフレームの間隔」「地図が使うメモリ」の 3 つに分けて測る。どれも端末の CPU と GPU、画面の大きさ、地物の数、ネットワークで大きく変わるので、値そのものより「同じ条件で案 A と案 B を比べた差」に意味がある。この文書は、条件のそろえ方と、ブラウザの中で測る仕掛けを書く。低価格の端末での確かめ方は [device-testing](device-testing.md) にある。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| 地図ライブラリのイベント | 最初の描画の終わり (`idle` と `areTilesLoaded()`) までの時間を、ページの中で `performance.now()` で取る | ライブラリごとにイベントの意味が違う | MapLibre GL JS 6.17.0 で実測 | https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapEventType/ |
| `requestAnimationFrame` の間隔 | 動かしている間のフレームの間隔を記録し、中央値、95 パーセンタイル、50 ms を超えた数を出す | ブラウザが描画を間引くと間隔に出る。GPU の処理の重さは直接は見えない | ブラウザの標準 API | 下の実測 |
| Chrome DevTools の Performance パネル | フレームごとの処理、落ちたフレーム (赤で表示)、メモリ (Memory のチェック) を記録する。FPS メーターは実行中のおおよその FPS を重ねて出す | CPU の throttling は手元の計算機に対する比で、DevTools は携帯端末の CPU を本当には再現できない。カスタムの設定は Calibrate で合わせられる | Chrome | https://developer.chrome.com/docs/devtools/performance/reference |
| CPU の throttling (CDP `Emulation.setCPUThrottlingRate`) | Playwright などから CPU を N 倍遅くして、遅い端末に近い条件を作る | 手元の計算機に対する比なので、計算機が変わると意味が変わる。GPU は遅くならない | Chrome DevTools Protocol、Playwright 1.58.2 の CDP セッションで実測 | https://chromedevtools.github.io/devtools-protocol/tot/Emulation/ (2026-11-11 にページの本文を取れず、説明は未確認) |
| Lighthouse | ページの読み込みの指標を同じ設定で繰り返し測る。既定はシミュレーションによる throttling で、モバイルは 150 ms の遅延、下り 1.6 Mbps、上り 750 Kbps、CPU 4 倍の遅さ | CPU の遅さは手元の計算機に対する比で、`benchmarkIndex` で較正することを勧めている。読み込みの指標が中心で、操作中のフレームの間隔は測らない | Lighthouse | https://github.com/GoogleChrome/lighthouse/blob/main/docs/throttling.md |
| `performance.memory` | JS ヒープの使用量を取る | 非標準で非推奨、Chromium だけ。ワーカーや別のヒープの分は入らず、地図のワーカーと GPU のメモリは見えない | Chromium | https://developer.mozilla.org/en-US/docs/Web/API/Performance/memory |
| `performance.measureUserAgentSpecificMemory()` | ページが使うメモリをワーカーも含めて見積もる | セキュアコンテキストかつクロスオリジン分離 (`crossOriginIsolated`) が要る。実験的で Baseline でない | 一部のブラウザ | https://developer.mozilla.org/en-US/docs/Web/API/Performance/measureUserAgentSpecificMemory |
| CDP の `Performance.getMetrics` | 自動の計測で、JS ヒープの使用量などを取る | `performance.memory` と同じく JS ヒープの値で、GPU のメモリは入らない (推測) | Playwright 1.58.2 の CDP セッションで実測 | 未確認 (CDP の文書を確かめていない) |
| WebPageTest | 遠隔の地点とブラウザ、回線の設定で読み込みを測る | 2026-11-11 に公式の文書のページを取れず、地点や端末の選択肢、無料の範囲は未確認 | WebPageTest | 未確認 |

## 判断を左右すること

- 何を比べるか: ライブラリ (MapLibre GL JS と他) の比較、ベクトルタイルと GeoJSON の比較、地物の数の上限、スタイルの重さ。比べる変数を 1 つにして、他はそろえる。
- GPU があるか: 地図の描画は WebGL (または WebGPU) で GPU を使う。ヘッドレスのブラウザでソフトウェアの描画 (SwiftShader) になると、フレームの間隔は実機の値と桁で違う (下の実測)。ヘッドレスの値は「同じ機械で、変更の前と後を比べる」ことにだけ使う。WebGPU の対応と制約は [webgpu](../../map-compare-arch/references/browser/webgpu.md)。
- 画面の大きさと画素密度: 描く画素の数は、画面の面積と DPR の 2 乗に比例する (画素数の換算)。DPR 3 の端末は同じ CSS の大きさでも DPR 1 の 9 倍の画素を描く。
- ネットワークとキャッシュ: 最初の描画の時間には、タイルの読み込みの時間が入る。描画の速さだけを比べたいなら、2 回目 (キャッシュあり) か、手元の配信で測る。
- 地物の数: GeoJSON をそのまま描く場合、地物と頂点の数が増えると、ワーカーでのタイル化とメモリが増える。数を変えて数回測り、要件の件数で動くかを見る ([data-size](data-size.md))。

## 手順

1. 比べる案と、そろえる条件を書く: ブラウザと版、ビューポートと DPR、地点とズーム、スタイル、地物の数、ネットワーク (キャッシュの有無)、CPU の throttling。
2. ページに計測の仕掛けを入れる。地図の作成の直前と `idle` の時刻、操作中の `requestAnimationFrame` の時刻を記録する。操作は `easeTo` などで決まった時間 (例: 4 秒で 90 度回転し 45 度傾ける) にして、毎回同じにする。
3. 手元の Chrome で DevTools の Performance パネルを使い、1 回記録して、落ちたフレームがどの処理 (スクリプト、描画、GPU) で起きているかを見る。
4. Playwright で自動にする。ケースごとに新しいブラウザコンテキストを作り、CDP セッションで CPU の throttling を掛け、同じ操作を 2 回以上繰り返す。ヘッドレスで WebGL が動くかを先に確かめる ([device-testing](device-testing.md) の「落とし穴」)。WebGL の描画器の名前 (`WEBGL_debug_renderer_info`) を結果に残す。
5. フレームの間隔は平均でなく、中央値、95 パーセンタイル、最大、50 ms を超えた数で書く。平均は少数の長い停止を隠す。
6. 低価格の端末の実機で同じ筋書きを通す ([device-testing](device-testing.md))。ヘッドレスや CPU の throttling の値を、実機の値の代わりにしない。
7. 案ごとの差と条件を表にして、map-compare-library (ライブラリ) や map-compare-arch (GeoJSON かタイルか) の判断に渡す。

## 実測

2026-11-11 に、MapLibre GL JS 6.17.0 で OpenFreeMap の Liberty スタイルを 1366 x 768、DPR 1、東京駅付近 (139.7671, 35.6812) の z14 で開き、`idle` と `areTilesLoaded()` を待ってから、`easeTo({bearing: 90, pitch: 45, duration: 4000})` の間の `requestAnimationFrame` の間隔を記録した。Playwright 1.58.2 (Node 23.9.0)、HeadlessChrome 145.0.7632.6、WebGL は SwiftShader (ANGLE、Vulkan 1.3.0 SwiftShader Device)。計算機は 32 スレッドの CPU で、CPU の throttling は CDP の `Emulation.setCPUThrottlingRate` で掛けた。キャッシュなしで、タイルの読み込みを含む。

| CPU の遅さ | 回 | 最初の idle まで (ms) | フレーム (件) | 中央値 (ms) | 95 パーセンタイル (ms) | 最大 (ms) | 50 ms 超 (件) | JS ヒープ使用 (MB) |
|---|---|---|---|---|---|---|---|---|
| 1 倍 | 1 | 2,515 | 25 | 16.7 | 800.0 | 1,399.9 | 11 | 18.7 |
| 1 倍 | 2 | 1,695 | 23 | 16.7 | 616.7 | 1,099.9 | 11 | 19.6 |
| 4 倍 | 1 | 3,452 | 26 | 100.1 | 400.0 | 483.4 | 20 | 15.8 |
| 4 倍 | 2 | 3,366 | 22 | 183.3 | 416.7 | 500.0 | 19 | 15.4 |

JS ヒープは CDP の `Performance.getMetrics` の `JSHeapUsedSize` で、操作の後に取った。

読み取れること:

- 4 秒の操作で 22〜26 フレームしか描けず、およそ 6 fps だった。ソフトウェアの描画 (SwiftShader) ではフレームの間隔が実機の GPU の値とかけ離れるので、ヘッドレスの値で「この端末で滑らかに動く」とは判断できない。
- 同じ条件の 2 回で、最初の idle までの時間は 2,515 ms と 1,695 ms で 1.5 倍違った。ネットワークを含む値は、回数を重ねて幅で書く。
- CPU を 4 倍遅くすると、最初の idle までが約 1.4〜2 倍になり、フレームの中央値は 100〜183 ms になった。
- JS ヒープは 15〜20 MB で、地図のワーカーと GPU のメモリはこの値に入らない。メモリの山を見るなら、実機で OS の道具 (Android の開発者向けオプション、Xcode の Instruments など) を使う (未確認: どの道具で何が見えるかはこの文書では確かめていない)。

## 落とし穴

- ヘッドレスの値を実機の値として出す: 上の実測のとおり、ソフトウェアの描画では桁で違う。描画器の名前を必ず結果に残し、SwiftShader なら「回帰の比較用」と書く。
- CPU の throttling で遅い端末を再現したつもりになる: throttling は手元の計算機に対する比で、GPU とメモリの帯域は遅くならない。Chrome の文書も、DevTools は携帯端末の CPU を本当には再現できないと書いている。
- 平均で書く: 長い停止 (上の 1 倍の最大 1,399.9 ms) は平均に埋もれる。パーセンタイルと最大で書く。
- タイルの読み込みと描画を混ぜる: キャッシュなしの最初の表示は、ネットワークの時間が支配する。描画の比較なら、手元の配信かキャッシュありで測る。
- `performance.memory` を全体のメモリと読む: JS ヒープだけで、ワーカー、GPU、画像のデコードは入らない。

## ライセンス上の注意

- Playwright (Apache-2.0)、Lighthouse (Apache-2.0)、MapLibre GL JS (BSD-3-Clause) を測る道具として使う分には、継承の義務は生じない。測るために表示した地図データの帰属表示は消さない。

## 出典

- https://github.com/GoogleChrome/lighthouse と https://github.com/microsoft/playwright (ライセンスが Apache-2.0 であること。2026-11-11 に GitHub API で確認)
- https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapEventType/ (`idle`、`load`、`render` の説明。2026-11-11 確認)
- https://developer.chrome.com/docs/devtools/performance/reference (CPU の throttling は手元の計算機に対する比、DevTools は携帯端末の CPU を本当には再現できない、Calibrate、落ちたフレーム、Memory のチェック、FPS メーター。2026-11-11 確認)
- https://github.com/GoogleChrome/lighthouse/blob/main/docs/throttling.md (既定はシミュレーションの throttling、モバイルの既定値、CPU 4 倍、`benchmarkIndex` での較正。2026-11-11 確認)
- https://developer.mozilla.org/en-US/docs/Web/API/Performance/memory (非標準、非推奨、Chromium だけ、ワーカーや別のヒープは入らない。2026-11-11 確認)
- https://developer.mozilla.org/en-US/docs/Web/API/Performance/measureUserAgentSpecificMemory (セキュアコンテキストとクロスオリジン分離が要る、Baseline でない。2026-11-11 確認)

## 未確認のこと

- CDP の `Emulation.setCPUThrottlingRate` と `Performance.getMetrics` の公式の説明 (2026-11-11 に文書のページの本文を取れなかった)。
- WebPageTest の地点、端末、回線の選択肢と、無料で使える範囲 (2026-11-11 に公式サイトと文書のページを取れなかった)。
- GPU のある画面つきのブラウザや実機での同じ筋書きの値。Xvfb の上で画面つきの Chromium を動かしたが、描画器は SwiftShader のままで、GPU の値は取れなかった。
