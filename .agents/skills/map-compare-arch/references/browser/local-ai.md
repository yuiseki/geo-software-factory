# ブラウザの中の AI

対象: WebNN、ブラウザ組み込みの AI API (Prompt API など)、WebGPU 上での推論 (ONNX Runtime Web、Transformers.js、WebLLM)。地図での使いどころ (検索語の解釈、画像からの抽出、要約)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 (JST)。この日の安定版は Chrome 157、Firefox 159.0.1 |
| 仕様と標準化の段階 (W3C / WHATWG / WICG、草案か勧告か) | WebNN は W3C Web Machine Learning Working Group の Candidate Recommendation Draft (2026-10-21 版、最後の CR Snapshot は 2026-01-22)。Prompt API、Writing Assistance APIs (Summarizer / Writer / Rewriter)、Translator と Language Detector はいずれも W3C Web Machine Learning Community Group の Draft Community Group Report (標準化トラックではない。2026-11-09 更新) |
| Baseline の状態 (Widely available / Newly available / 未達) | すべて未達 (Limited availability)。組み込み AI は Chromium 系だけ、WebNN はどのブラウザも既定では出荷していない。WebGPU 上の推論ライブラリは WebGPU の対応に従い、WebGPU 自体も未達 ([webgpu.md](webgpu.md) を参照) |

## ブラウザの対応

API ごとに、対応した版を書く。iOS では全ブラウザが WebKit を使うので、iOS Safari の欄が iOS 全体の対応になる。

| API | Chrome / Edge | Firefox | Safari (macOS) | Safari (iOS / iPadOS) | Android の WebView | 出典 |
|---|---|---|---|---|---|---|
| WebNN (`navigator.ml`) | Chrome はフラグで 112 から。Origin Trial はデスクトップで 147 から (blink-dev では 147〜149 の予定。Android は対象外)。Edge は Chrome と同時に出すと chromestatus に記載。Edge の Origin Trial は新規受付を終了 | 未対応 (Mozilla の立場は positive) | 未対応 (Apple は WG に参加しているが実装の表明なし) | 未対応 | 未対応 (Origin Trial から Android を除外) | [chromestatus 5176273954144256](https://chromestatus.com/feature/5176273954144256)、[MDN BCD ML.json](https://github.com/mdn/browser-compat-data/blob/main/api/ML.json)、[blink-dev](https://groups.google.com/a/chromium.org/g/blink-dev/c/5CWKSChYo98) |
| Prompt API (`LanguageModel`) | Chrome はウェブで 148 (2026-05-05)、拡張機能で 138。デスクトップのみ。サンプリング引数は Origin Trial。Edge は Canary / Dev の 138.0.3309.2 以降でフラグを立てた開発者プレビュー (Phi-4-mini、150.0.4070 以降は Aion-1.0-Instruct も選べる) | 未対応 (Mozilla は negative) | 未対応 (Apple は oppose) | 未対応 | 未対応 (Android 版 Chrome も未対応) | [Chrome の Prompt API 文書](https://developer.chrome.com/docs/ai/prompt-api)、[webstatus.dev languagemodel](https://webstatus.dev/features/languagemodel)、[Edge の Prompt API 文書](https://learn.microsoft.com/en-us/microsoft-edge/web-platform/prompt-api) |
| Summarizer API | Chrome 138 (デスクトップのみ)。Edge 138 (webstatus.dev の値。Edge の文書は 138.0.3309.2 以降で既定で有効とするが、ハードウェア要件つきの開発者プレビューとして説明している) | 未対応 (Mozilla は negative) | 未対応 | 未対応 | 未対応 | [Chrome の Summarizer 文書](https://developer.chrome.com/docs/ai/summarizer-api)、[webstatus.dev summarizer](https://webstatus.dev/features/summarizer)、[Edge の Writing Assistance 文書](https://learn.microsoft.com/en-us/microsoft-edge/web-platform/writing-assistance-apis) |
| Translator API | Chrome 138 (デスクトップのみ)。Edge 148 | 未対応 | 未対応 | 未対応 | 未対応 | [Chrome の Translator 文書](https://developer.chrome.com/docs/ai/translator-api)、[webstatus.dev translator](https://webstatus.dev/features/translator) |
| Language Detector API | Chrome 138 (デスクトップのみ)。Edge 148 | 未対応 | 未対応 | 未対応 | 未対応 | [webstatus.dev languagedetector](https://webstatus.dev/features/languagedetector)、[MDN BCD LanguageDetector.json](https://github.com/mdn/browser-compat-data/blob/main/api/LanguageDetector.json) |
| Writer API / Rewriter API | Chrome は Developer trial (フラグ)。Edge は Canary / Dev でフラグ | 未対応 | 未対応 | 未対応 | 未対応 | [Chrome の組み込み AI 一覧](https://developer.chrome.com/docs/ai/built-in-apis)、[chromestatus Writer](https://chromestatus.com/feature/4712595362414592) |
| Proofreader API | Chrome は Origin Trial (chromestatus 上は 141〜146 で登録) | 未対応 | 未対応 | 未対応 | 未対応 | [Chrome の組み込み AI 一覧](https://developer.chrome.com/docs/ai/built-in-apis)、[chromestatus 5164677291835392](https://chromestatus.com/feature/5164677291835392) |
| ONNX Runtime Web 1.31.1 / Transformers.js 4.3.2 (Wasm で実行) | WebAssembly が動くすべてのブラウザ。マルチスレッドはクロスオリジン分離が要る | 同左 | 同左 | 同左 | 同左 | [ONNX Runtime Web](https://onnxruntime.ai/docs/tutorials/web/)、[Transformers.js README](https://github.com/huggingface/transformers.js) |
| ONNX Runtime Web / Transformers.js / WebLLM 0.2.87 (WebGPU で実行) | WebGPU の対応に従う (Windows / macOS / ChromeOS は 113、Linux は 144、Android は 121) | Windows 141、Apple シリコンの macOS 145 / 147 | 26 (macOS 26 以降) | 26 (iOS 26 以降) | MDN の互換表上は 121 (Android 版 Chrome のミラー値) | [webgpu.md](webgpu.md)、[WebLLM](https://github.com/mlc-ai/web-llm) |

## 概要

ブラウザで AI を動かす道は 3 つある。1 つ目はブラウザが持つモデルを呼ぶ組み込み AI API で、Chrome は Gemini Nano (Prompt API、Summarizer など) と専用モデル (Translator、Language Detector) を、Edge は Phi-4-mini を使う。モデルはブラウザが一度だけダウンロードしてサイト間で共有するので、アプリ側の配信は要らないが、使えるのはデスクトップの Chromium 系だけである。2 つ目は自前のモデルを ONNX Runtime Web、Transformers.js、WebLLM などで Wasm か WebGPU の上で動かす方法で、Safari 26 や iOS 26 も含めて動くがモデルの配信と容量は自分で持つ。3 つ目の WebNN は OS の推論機能 (GPU や NPU) を使う低レベル API で、2026-11 時点では Chrome の Origin Trial 段階にある。

## 地図プロダクトでの使いどころ

保存、計算、表現のどれを、ブラウザ・アプリの層に置けるようにするか。

- 保存: 組み込み AI のモデルはブラウザが管理し、アプリからは触れない (Chrome では `chrome://on-device-internals` で大きさを確認できる)。自前のモデルは Cache API、OPFS、IndexedDB に置く。WebLLM は既定で Cache API、選択肢として IndexedDB と OPFS を持つ。ONNX Runtime Web も Cache API か OPFS に置いて再ダウンロードを避けるよう勧めている。埋め込みベクトル (POI 名や説明文の埋め込み) をあらかじめ配っておき、ブラウザ内で意味検索する構成もとれる (推測)
- 計算: 検索語の解釈では、Prompt API の `responseConstraint` に JSON Schema を渡すと出力を決まった形に縛れるので、「駅から歩いて 10 分以内のカフェ」のような自然文を `{category, anchor, max_walk_minutes}` のような構造化した条件に変え、ブラウザ内の PMTiles や DuckDB-Wasm の検索に渡せる (設計例、推測)。Prompt API は日本語 (`ja`) を受け付ける。画像からの抽出では、GeoAI.js (MIT) が Transformers.js と ONNX Runtime Web の上で建物、車両、船、太陽光パネルなどを衛星画像や航空写真から検出し、GeoJSON で返す。ポリゴンを描くとその範囲のタイルを取りにいき、Worker で推論する。要約では、Summarizer で地物の属性や口コミを key-points や tldr にまとめる。Translator と Language Detector で POI 名や説明文を利用者の言語に訳せる。いずれもサーバーに送らないので、位置や検索語のような個人に関わる入力を端末内で閉じられる
- 表現: AI の結果 (検出した地物の GeoJSON、要約、訳) を地図に重ねる。Prompt API は画像も入力に取れるので、地図のスクリーンショットや現地写真を説明する文章を作れる (出力はテキストのみ)

## 制約

- 容量と寿命: Chrome の組み込み AI は Chrome のプロファイルがある領域に 22 GB 以上の空きが要り、ダウンロード後に空きが 10 GB を切るとモデルが消され、条件が戻れば再ダウンロードされる。モデル本体の大きさは版で変わるとしか書かれていない。Edge の開発者プレビューは 20 GB 以上の空き、10 GB を切ると削除。ONNX Runtime Web は Wasm のメモリ上限 4 GB を超えるモデルを動かせない。Chrome の ArrayBuffer は最大 0x7fe00000 バイト (約 2 GB) で、protobuf も 2 GB が上限なので、それより大きいモデルは外部データに分ける
- 権限とユーザーの操作が要るか: 組み込み AI は `availability()` が `downloadable` か `downloading` のとき、`create()` の前にユーザーの操作 (クリックやキー入力) が要る。Translator は `create()` に常にユーザーの操作が要る。権限ダイアログは無い。クロスオリジンの iframe では `allow="language-model"`、`allow="summarizer"`、`allow="translator"` のように Permissions Policy で許可する必要がある (既定ではトップレベルと同一オリジンの iframe だけ)。組み込み AI は Web Worker では使えない (Prompt API、Summarizer、Translator の文書に明記)
- セキュアコンテキスト、クロスオリジン分離 (COOP/COEP) などの前提: WebNN は全インターフェイスがセキュアコンテキスト限定で、Worker からも使える。WebGPU もセキュアコンテキストが必須。ONNX Runtime Web の Wasm マルチスレッドは `crossOriginIsolated` (COOP/COEP) が要り、無ければ単一スレッドになる。COEP を有効にすると、CORP や CORS を返さない外部タイルや画像を読めなくなるので、地図タイルの配信元との相性を確かめる必要がある (推測)
- iOS / Safari での制限: Safari は組み込み AI も WebNN も持たず、Apple は Prompt API に oppose の立場。iOS で使えるのは Wasm か WebGPU (iOS 26 以降) の上で自前のモデルを動かす方法だけ
- WebView (アプリに埋め込んだブラウザ) での制限: Chrome の文書は「Android 版 Chrome、iOS、Chromebook Plus 以外の ChromeOS は基盤モデルを使う API に未対応」とし、Translator と Language Detector もモバイルでは動かないとしている。したがって Android WebView でも組み込み AI は使えないと考えるのが安全 (WebView 個別の記述は無い)。アプリ側では OS のオンデバイス AI を直接呼ぶ方が筋がよい場合がある (推測、未確認のことを参照)

## 地図の実装例

この API を使っている OSS やライブラリ (地図ライブラリ、PMTiles、DuckDB-Wasm など)。

- GeoAI.js (npm の `geoai` 1.0.8、MIT): Transformers.js と ONNX Runtime Web を同梱の前提にした、ブラウザ内の GeoAI ライブラリ。WebGPU か Wasm で推論し、GeoJSON のポリゴンを渡すと検出結果を GeoJSON で返す。画像の取得元として ESRI、Mapbox、COG、TMS、WMS、OpenAerialMap、Google Map Tiles を挙げている。使うモデルごとにライセンスが異なるので個別に確かめること
- Transformers.js 4.3.2 (Apache-2.0): ブラウザでは既定で CPU (Wasm) で動き、`device: 'webgpu'` で WebGPU に切り替える。`dtype` は WebGPU の既定が fp32、Wasm の既定が q8 で、fp16 や q4 も選べる。埋め込み (feature-extraction)、画像分類、音声認識などのパイプラインを持つ
- ONNX Runtime Web 1.31.1 (MIT): 実行プロバイダーは wasm (全演算子に対応)、webgpu、webgl、webnn (webnn は GPU と CPU を選べる)。GPU 系のプロバイダーは演算子の一部にしか対応しない
- WebLLM 0.2.87 (Apache-2.0): WebGPU 必須の LLM 実行環境。OpenAI 互換の API、JSON モード (構造化出力)、Web Worker と Service Worker での実行を持つ。関数呼び出しは作業中。対応モデルに Llama、Phi、Gemma、Mistral、Qwen の系統がある。モデルのライセンスはランタイムと別で、たとえば Llama 3.2 Community License は OSI のオープンソースではなく、組み込んで配布するならライセンスの写しを同梱し「Built with Llama」を目立つように表示し、Notice ファイルを置く必要がある。改変や出力を使って作ったモデルを配布するなら名前の先頭に「Llama」を付ける。利用は Acceptable Use Policy に従う。前月の月間アクティブユーザーが 7 億を超える事業者は Meta から別途ライセンスを得る必要がある。Gemma は Gemma Terms of Use で、配布時は利用制限を受け手との契約に強制可能な条項として入れ、規約の写しを渡す。Hosted Service (SaaS) として提供する場合も規約の「配布」に含まれ、Prohibited Use Policy に従う (Notice ファイルの義務は SaaS では免除)。Google は違反と考える利用を遠隔で制限する権利を持つ。Gemma 4 は別のライセンスを案内している
- Chrome と Edge の組み込み AI のデモ: Edge は Prompt API、Summarizer、Translator のプレイグラウンドを公開している (地図用途ではない)

## 落とし穴

- 組み込み AI は同じ API でもブラウザごとに中身のモデルが違う (Chrome は Gemini Nano、Edge は Phi-4-mini か Aion-1.0-Instruct)。同じプロンプトでも出力が変わるので、構造化出力 (`responseConstraint`) と検証を前提にする
- 端末条件が厳しい (GPU の VRAM が 4 GB 超、または RAM 16 GB 以上と 4 コア以上。Edge は VRAM 5.5 GB 以上)。一般の利用者の多くは `unavailable` になりうるので、必ずクラウドか軽いモデルへの切り替えを用意する (推測)
- 初回はモデルのダウンロードが要り、従量制の回線ではダウンロードされない。初回の体験に待ち時間が入る
- Prompt API はコンテキストの上限を超えると古いやりとりから捨て、それでも足りなければ `QuotaExceededError` になる。JSON Schema も上限を消費する (`omitResponseConstraintInput` で省ける)
- Translator は言語ペアごとのダウンロード状況をプライバシー保護のため隠し、実際に作るまで `downloadable` と答える。翻訳は 1 件ずつ順番に処理され、大きな依頼が後ろを詰まらせる
- MDN の互換表は Summarizer、Translator、Language Detector に「地域によって制限される場合がある」と注記している
- Mozilla は Prompt API と Summarizer に negative、Apple は Prompt API に oppose の立場で、全ブラウザで使える見込みは立っていない。組み込み AI に依存した機能は Chromium 限定の追加機能として設計する
- 衛星画像や航空写真から地物を抽出する場合、画像の提供元の利用規約が機械学習や派生データの作成を禁じていることがある。技術的に取得できても規約上使えるとは限らない (推測。各提供元の規約で確かめる)
- WebGPU で LLM を動かすと GPU メモリを地図の描画と取り合う。地図の描画が落ちる、推論が遅くなるといった干渉がありうる (推測)

## まだ使えないもの、これから使えるもの

提案中、Origin Trial 中、一部のブラウザだけのもの。

- WebNN: Chrome のデスクトップで Origin Trial (147 から)。Android は除外。Edge は Chrome と同時に出す予定。Firefox は positive だが実装なし、Safari は表明なし
- Writer / Rewriter: Chrome は Developer trial (フラグ)、Edge は Canary / Dev でフラグ
- Proofreader: Chrome の Origin Trial
- Prompt API のサンプリング引数 (temperature など): Chrome の Origin Trial
- Embedding API: chromestatus に「提案中」として登録。端末上の共有モデルで埋め込みを作り、意味検索や RAG に使う API。実装の版は未定
- Edge の Aion-1.0-Instruct: Canary / Dev の 150.0.4070 以降でフラグを立てると使える。GPU が弱い端末でも CPU で動くとされる。2026-07 にオープンソースで公開予定と書かれていた
- Prompt API の対応言語は en、ja、es、de、fr で、他の言語は開発中

## 出典

- https://www.w3.org/TR/webnn/ (Candidate Recommendation Draft 2026-10-21、MLContextOptions、Worker への公開、セキュアコンテキスト限定)
- https://chromestatus.com/feature/5176273954144256 (WebNN の Origin Trial 開始 147、Firefox と Safari の立場、Edge の出荷予定)
- https://groups.google.com/a/chromium.org/g/blink-dev/c/5CWKSChYo98 (WebNN の Origin Trial の延期、147〜149、Android の除外)
- https://developer.microsoft.com/microsoft-edge/origin-trials/trials/19857284-cf52-484b-8b09-8ca50ac9dccb (Edge の WebNN Origin Trial が新規受付を終了)
- https://github.com/mdn/browser-compat-data/tree/main/api (ML.json、LanguageModel.json、Summarizer.json、Translator.json、LanguageDetector.json の版と注記)
- https://api.webstatus.dev/v1/features/languagemodel ほか (Prompt API が Chrome 148、Summarizer が Chrome と Edge 138、Translator と Language Detector が Edge 148、Mozilla と Apple の立場)
- https://developer.chrome.com/docs/ai/built-in-apis (各 API の段階)
- https://developer.chrome.com/docs/ai/get-started (OS、空き容量、GPU、RAM、モバイル非対応、ユーザー操作、モデル削除の条件)
- https://developer.chrome.com/docs/ai/prompt-api (ウェブ 148 と拡張 138、マルチモーダル入力、対応言語、responseConstraint、コンテキスト、iframe、Worker 非対応)
- https://developer.chrome.com/docs/ai/summarizer-api (要約の種類と長さ、対応言語、iframe、Worker 非対応)
- https://developer.chrome.com/docs/ai/translator-api (言語ペアの秘匿、ユーザー操作、順次処理、デスクトップのみ、Edge 148)
- https://learn.microsoft.com/en-us/microsoft-edge/web-platform/prompt-api (Edge の Prompt API、Phi-4-mini と Aion-1.0-Instruct、ハードウェア要件)
- https://learn.microsoft.com/en-us/microsoft-edge/web-platform/writing-assistance-apis (Edge の Summarizer、Writer、Rewriter の扱い)
- https://learn.microsoft.com/en-us/microsoft-edge/web-platform/translator-api (Edge の Translator)
- https://webmachinelearning.github.io/prompt-api/ 、https://webmachinelearning.github.io/writing-assistance-apis/ 、https://webmachinelearning.github.io/translation-api/ (Draft Community Group Report)
- https://chromestatus.com/feature/5164677291835392 (Proofreader の Origin Trial)、https://chromestatus.com/feature/5115796490682368 (Embedding API の提案)
- https://onnxruntime.ai/docs/tutorials/web/ (実行プロバイダー)
- https://onnxruntime.ai/docs/tutorials/web/large-models.html (2 GB と 4 GB の上限、キャッシュの勧め)
- https://onnxruntime.ai/docs/tutorials/web/env-flags-and-session-options.html (マルチスレッドに crossOriginIsolated が要る)
- https://github.com/huggingface/transformers.js と https://huggingface.co/docs/transformers.js/guides/webgpu (既定は Wasm、device と dtype)
- https://github.com/mlc-ai/web-llm (WebGPU 必須、OpenAI 互換、JSON モード、キャッシュ、ライセンス)
- https://github.com/decision-labs/geoai.js (ブラウザ内の GeoAI、GeoJSON 入出力、MIT)
- https://dev.meta.ai/llama/llama3_2/license (Llama 3.2 Community License の条件)
- https://ai.google.dev/gemma/terms (Gemma Terms of Use の条件)
- npm レジストリと GitHub Releases (onnxruntime-web 1.31.1、@huggingface/transformers 4.3.2、@mlc-ai/web-llm 0.2.87、geoai 1.0.8 の版)

## 未確認のこと

- WebNN の Origin Trial が 149 で終わったのか、延長や出荷に進んだのか (chromestatus に終了版の記載が無い)
- Proofreader の Origin Trial の現在の終了版 (chromestatus は 146 までと登録、Chrome の文書は Origin Trial と表記)
- Chrome の組み込みモデル (Gemini Nano) のダウンロードサイズの実数
- Summarizer、Translator、Language Detector の「地域による制限」の中身 (日本で使えるか)
- Edge の Summarizer が安定版で既定有効か、Canary / Dev だけか (webstatus.dev と Edge の文書の書きぶりが一致しない)
- Edge の Aion-1.0-Instruct が予定どおり公開されたか、そのライセンス
- Android WebView と iOS の WKWebView での WebGPU 推論の可否と性能
- アプリ層の代替としての OS のオンデバイス AI (Apple の Foundation Models framework、Android の ML Kit GenAI / Gemini Nano) の対応 OS と端末条件 (公式文書の本文を取得できなかった)
- Firefox が内部に持つ AI 実行基盤がウェブに公開されるか
- GeoAI.js の各モデルのライセンスと精度
