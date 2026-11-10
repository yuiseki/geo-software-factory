# 比較の軸 (アーキテクチャ)

地図プロダクトの構成を、機能ごとに「何を、どこに置くか」で決めるための手順。比較を始める前に読む。各技術の事実は `capabilities/`、`browser/`、`edge/`、`app/`、`formats/`、[self-hosting](self-hosting.md) にあり、この文書には軸と判定の手順だけを書く。例として挙げる事実は、各 reference に 2026-11-10 時点で書かれていたもの。

## 考え方: 3 つの要素と 3 つの置き場所

地図プロダクトのアーキテクチャは、3 つの要素をそれぞれどこに置くかの組み合わせで決まる。

| 要素 | 中身 |
|---|---|
| 保存 | データをどこに、どの形式で持つか。正本 (書き込みを受ける元のデータ) と、読み出し用の成果物 (タイル、索引、グラフ、GeoParquet など) を分けて考える |
| 計算 | 選択、絞り込み、結合、変換、検索、経路計算、集計、ルールの強制を、どこで実行するか |
| 表現 | 計算の結果を、どの形 (ベクトルタイル、ラスタ画像、JSON、GeoJSON) にして、どこで描くか |

| 置き場所 | 含むもの |
|---|---|
| クラウド | リージョンのサーバー、管理型 DB、オブジェクトストレージ、短命な関数 (Lambda など)、外部の API |
| エッジ | CDN のエッジ関数とキャッシュ ([edge-functions](edge/edge-functions.md))、利用者の近くに置く小さなサーバーやクラスタ ([near-user-servers](edge/near-user-servers.md)) |
| ブラウザ・アプリ | ブラウザ (Service Worker、OPFS、Wasm、Workers、WebGPU など、`browser/`)、ネイティブアプリの端末 ([native-runtime](app/native-runtime.md)) |

機能は 5 つに分ける: タイル配信 ([tiles](capabilities/tiles.md))、検索 ([search](capabilities/search.md))、ルート検索 ([routing](capabilities/routing.md))、解析 ([analysis](capabilities/analysis.md))、正本と更新 ([source-of-truth](capabilities/source-of-truth.md))。各機能は、外部の API に任せる、常駐するサーバーを自前で動かす、ファイルと関数で済ませる、の 3 つの型のどれかで実現する。正解は 1 つではなく、データの大きさ、転送時間、実行環境の制約、更新頻度、技術の進み具合で変わる。

## 進め方

1. 要件 (プロダクト概要) から、要る機能を 5 つの中から選ぶ。書き込みが無ければ「正本と更新」は外部のデータを取り込む手順だけになる。
2. 機能ごとに、足切りの条件で置けない場所を消す。足切りは「点数を下げる」ではなく「候補から外す」。
3. ブラウザ・アプリに置けるかを最初に検討する (評価の軸 1)。置けない理由が足切りか評価の軸で説明できるときだけ、エッジ、クラウドへ上げる。
4. 残った案を、評価の軸で比べる。軸の重みは「要件から初期案を決める」の表を出発点にする。
5. 機能 × 要素の表 (「出力の表」の節) に置き場所を埋め、案ごとに費用を見積もる。
6. 推奨を先に書き、続けて軸と案ごとの評価を表で示す。確かめられなかった項目は「未確認」のまま残し、推測で埋めない。

## 足切りの条件

要件に当てはまるものだけを当てる。

| 条件 | 何を確かめるか | 外れる例 (各 reference の記述) |
|---|---|---|
| 信頼の境界 | 計算が、アクセス制御、不正の防止 (位置の偽装、得点、ポイント、決済)、正解の判定のような、ルールの強制を含むか | ブラウザ・アプリは利用者の手元にあり改ざんされうるので、ルールを強制する計算は置けない。公開してよいデータの絞り込みや表示は置ける |
| 外部通信とオフライン | 閉域網か、通信が途切れる現場か、データの国内保持が要るか | 閉域網なら外部の API と CDN のエッジ関数が外れ、利用者の近くに置くサーバーか端末に限られる ([near-user-servers](edge/near-user-servers.md))。オフラインなら、索引やグラフを端末に置く形に限られる ([search](capabilities/search.md)、[native-runtime](app/native-runtime.md)) |
| 対象ブラウザと端末 | iOS、Android の WebView、Firefox、古い端末を含むか | Android の WebView では SharedArrayBuffer と Wasm のスレッドが使えず、DuckDB-Wasm のスレッド版と SQLite の `opfs` VFS が動かない ([wasm](browser/wasm.md))。WebGPU は Baseline 未達で、Firefox の Linux と Android では使えない ([webgpu](browser/webgpu.md))。Background Fetch、Background Sync、Storage Buckets は Chromium 系だけ ([storage](browser/storage.md)、[service-worker](browser/service-worker.md))。ブラウザ組み込みの AI はデスクトップの Chromium 系だけ ([local-ai](browser/local-ai.md)) |
| データの大きさと置き場所の上限 | 正本、索引、グラフ、タイルの大きさが、置き場所の上限に収まるか | Workers のメモリは 128 MB ([edge-functions](edge/edge-functions.md))。Wasm のメモリは 4 GB までで、iOS の Safari は Memory64 に未対応 ([wasm](browser/wasm.md))。Firefox の保存容量は 10% か 10 GiB の小さいほう ([storage](browser/storage.md))。OSRM の全球の経路は RAM が約 123 GiB ([routing](capabilities/routing.md)) |
| 整合性と書き込み | 同じものへの同時の書き込み、二重登録の禁止、監査と履歴が要るか | 要るなら、正本をファイルや結果整合のエッジ DB に置く案が外れ、トランザクションを持つ DB に置く ([source-of-truth](capabilities/source-of-truth.md))。ファイルでも条件付き書き込みでファイル単位の楽観ロックはできるが、行単位の制御、複数ファイルの原子的な更新、参照整合性はできない |
| 更新頻度 | 正本の変更を、読み出し側にどれだけ早く反映する必要があるか | 秒単位の反映が要るなら、成果物 (PMTiles、索引) を作り直して配る形は外れ、正本から直接読むか、変更を通知する形にする ([source-of-truth](capabilities/source-of-truth.md)) |
| ライセンス | 使うツールとデータの義務が、配布形態 (SaaS、アプリ配布、受託納品) と両立するか | Wasm やアプリに LGPL のもの (GEOS、gdal3.js、geos-wasm) を入れて配ると LGPL の配布条件がかかる ([analysis](capabilities/analysis.md)、[wasm](browser/wasm.md))。Nominatim の Python のコードは GPL-3.0 以降 ([search](capabilities/search.md))。OsmAnd の UI とアートワークは CC-BY-NC-ND ([native-runtime](app/native-runtime.md))。OSM 由来のデータは ODbL |

## 評価の軸

### 1. ブラウザ・アプリに寄せられるか

最初に検討する。ブラウザは表示の場所であると同時に、保存と計算の場所でもある。寄せられれば、サーバーの費用と運用が減り、オフラインで動き、応答が速くなる。次を順に確かめる。

- 保存: OPFS と同期アクセスハンドルは全ブラウザで使える (Baseline Widely available)。容量の上限は、Chrome と Safari 17 以降がディスク全体の 60%、WKWebView が 15%、Firefox が 10% か 10 GiB の小さいほう。退避はオリジン単位で全部まとめて消える。Safari は、タブで使うだけのサイトを 7 日使わないと保存ごと消すので、オフライン地図はホーム画面への追加を前提にする ([storage](browser/storage.md))。
- 取得とキャッシュ: `Cache.put()` は 206 応答を受け付けないので、PMTiles や COG の Range の結果は Cache Storage にそのまま置けない。OPFS に置くか、ファイル全体を取って置く ([service-worker](browser/service-worker.md))。MapLibre GL JS は v3 以降タイルを Cache Storage に入れず、PMTiles の JS もヘッダーとディレクトリしかキャッシュしないので、オフライン化はアプリ側で作る。
- 計算: Wasm で DuckDB、SQLite、GEOS、GDAL がブラウザで動く。スレッドには COOP/COEP によるクロスオリジン分離が要り、他社の iframe やポップアップでの連携が止まりやすい。分離の要らない構成 (シングルスレッドの版、SQLite の `opfs-sahpool`) を選べるかを見る ([wasm](browser/wasm.md)、[workers](browser/workers.md))。
- GPU: 主要な地図ライブラリの描画は WebGL 系で、WebGPU は集計や点群など一部の処理で使う段階。WebGL2 への切り替えを必ず用意する ([webgpu](browser/webgpu.md))。
- 推論: ブラウザ組み込みの AI は、使えたら速くなる追加の機能として設計し、クラウドへの切り替えを用意する ([local-ai](browser/local-ai.md))。
- 端末の機能: iOS では Push、通知、Badging はホーム画面の Web アプリだけで使える。AR (WebXR) は Android の Chrome だけ ([device](browser/device.md))。
- ネイティブアプリ: OS ごとの保存とバックグラウンドの制約、オフラインパックの対象 (MapLibre Native では PMTiles はオフラインパックの対象外と公式に書かれている) を確かめる ([native-runtime](app/native-runtime.md))。

### 2. 保存の段階

保存は、軽いほうから次の順に重くなる。まずファイルで済まないかを確かめ、下の条件のどれかに当たったら一段上げる ([source-of-truth](capabilities/source-of-truth.md))。

1. ファイル: オブジェクトストレージや静的ホスティングに置くだけで、DB を持たない。
2. サーバーレスの DB サービス。
3. 自前の API を持つ管理型 DB。
4. 高頻度の書き込みと購読に向くイベント型の保存。

一段上げる条件: 同じものへの同時の書き込み、端末に全件を落として絞り込めない量と複雑さ、1 件だけの部分更新、サーバー側で強制するアクセス制御 (行単位の出し分け)、参照の整合性、サーバー側の集計、監査と履歴、変更の即時の通知、サーバー側でのルールの強制。

段階を上げるときは、空間の機能が実際にあるかを確かめる。MongoDB の地理機能は検索だけでバッファや結合を持たない。Spanner と Cloudflare D1 は空間の型や索引が公式文書に見当たらない ([source-of-truth](capabilities/source-of-truth.md))。

### 3. 正本と成果物の分け方

書き込みは整合性の強い正本に集め、読み出しは正本から作った成果物をエッジやブラウザに配る。正本は、遅くても強い整合性とトランザクションを優先して PostGIS や MongoDB などに置くことがある。成果物が正本に対してどれだけ遅れてよいかを要件から決め、変更の検知 (CDC、変更ストリーム、LISTEN/NOTIFY) と作り直しの手順を書く ([source-of-truth](capabilities/source-of-truth.md))。

### 4. 応答の速さと転送

- ファイルを Range で読む構成は、置き場所の遅延がそのまま効く。Protomaps は R2 の遅延を 500ms 以上と書いている ([edge-functions](edge/edge-functions.md))。
- Cloudflare の Free、Pro、Business は 1 ファイル 512 MB までしかキャッシュしないので、全国規模の PMTiles はエッジ関数でタイル単位にしてからキャッシュする ([network](browser/network.md))。
- ブラウザで直接読むファイルの圧縮は gzip にする。Chrome は CompressionStream で brotli に未対応で、zstd は仕様に無い ([network](browser/network.md))。
- 範囲が 1 つだけの Range はプリフライト無しで送れる。複数範囲や `If-Match` はプリフライトを起こす ([network](browser/network.md))。

### 5. 費用

1 回の表示あたりの単価だけでなく、限界費用で見る。

- ファイルで配る構成は、1 回の表示で発生するリクエストの数 (PMTiles の Range 取得など) と転送量に課金される。表示回数で課金されるサービスより高くなることもある。
- 小さな地図アプリを多数作る場合は、無料枠に収まるかが効く。
- 常駐するサーバーは、使われていない時間も費用がかかる。メモリの大きいもの (経路、全文検索) ほど効く。
- 見積もりの手順は「費用の見積もり方」の節。

### 6. 運用の負担

- 常駐するサーバーは、プロセス、ディスク、DB の監視と障害対応を自分で持つ。ファイルと関数の構成では、監視の対象は CDN と関数のエラー率、遅延、請求額になる ([self-hosting](self-hosting.md))。
- 成果物の差し替えは、版ごとに別名で置いて参照を切り替える。同じ名前で上書きすると、キャッシュに残った古い索引と新しい本体が混ざる ([self-hosting](self-hosting.md)、[cloud-native-formats](formats/cloud-native-formats.md))。
- 利用者の近くに置くサーバーは、更新をどう届けるか (オフラインでの導入と更新) を先に決める ([near-user-servers](edge/near-user-servers.md))。

### 7. ロックインと移行

- 認証や行単位のアクセス制御が特定の BaaS の独自関数に結びつくと、正本を移しにくくなる。標準の PostgreSQL や OSS の認証のような逃げ道があるかを書く ([source-of-truth](capabilities/source-of-truth.md))。
- エッジの実行環境は提供者の方針で変わる。Vercel は Edge runtime から Node.js への移行を勧めている ([edge-functions](edge/edge-functions.md))。
- データ形式は、仕様が公開され複数の実装があるもの (PMTiles、GeoParquet、COG、FlatGeobuf) を選ぶと、置き場所を後から変えやすい ([cloud-native-formats](formats/cloud-native-formats.md))。

### 8. 技術の成熟度

置き場所の選択肢は、技術の進み具合で増える。新しいものを選ぶときは、本番で使えるかを確かめる。

- WebGPU は Baseline 未達。deck.gl は WebGPU を本番向けではないと明記している ([webgpu](browser/webgpu.md))。
- GeoParquet 2.0.0 は 2026-11-05 に出たばかりで、MLT の v2 は実験段階 ([cloud-native-formats](formats/cloud-native-formats.md))。
- ブラウザで動く成熟したルート検索エンジンは見つかっていない ([routing](capabilities/routing.md))。
- WebNN は Origin Trial の段階 ([local-ai](browser/local-ai.md))。

## 要件から初期案を決める

出発点にする置き場所の案。足切りと評価の軸で確かめてから推奨する。

| 要件 | 初期案 | 重くする軸 |
|---|---|---|
| 閲覧だけの地図、データは数千件まで | タイルは外部の API か PMTiles を静的に配る。データはファイルに置き、ブラウザで絞り込む | ブラウザ・アプリに寄せられるか、費用 |
| 閲覧だけで、データが多い (数十万件) | 正本は DB かファイル、読み出しは PMTiles や GeoParquet にしてブラウザかエッジで範囲を絞って読む | 応答の速さと転送、正本と成果物の分け方 |
| 複数人が同じ地物を編集する | 正本はトランザクションを持つ DB。読み出しは正本から作った成果物か、正本から直接 | 保存の段階、正本と成果物の分け方 |
| ルールの強制 (位置情報ゲーム、ポイント、予約) | 判定と正本はクラウド。ブラウザは表示と入力だけ | 信頼の境界 (足切り)、保存の段階 |
| オフライン、通信が途切れる現場 | タイル、索引、グラフを端末に置く。ブラウザならホーム画面への追加と OPFS | ブラウザ・アプリに寄せられるか、運用の負担 |
| 閉域網、庁舎や現場に置く | 利用者の近くに置くサーバーに、ファイルと関数か常駐のサーバー | 運用の負担 |
| 表示回数が多く、外部 API の課金が重い | タイルは PMTiles を CDN から配る。損益分岐を [self-hosting](self-hosting.md) で求める | 費用、運用の負担 |
| 小さな地図アプリを多数作る | ファイルと静的ホスティング、外部 API の無料枠 | 費用 (限界費用) |
| 検索、ルート検索を自前で持ちたい | 国や都道府県の範囲なら、索引やグラフを 1 ファイルにして関数で引く。全球なら常駐のサーバー | データの大きさ (足切り)、運用の負担 |
| 大きなデータの解析を画面で見せる | GeoParquet や COG を DuckDB で直接読む。結果だけをブラウザに送るか、ブラウザで Wasm を使う | ブラウザ・アプリに寄せられるか、技術の成熟度 |

## 費用の見積もり方

- タイルを自前で配る場合は、[self-hosting](self-hosting.md) の「費用の見積もり」に従い、外部の API との損益分岐を求める。外部の API の費用は、map-compare-infra の criteria.md の「費用の見積もり方」で、課金単位と使い方の経路を揃えて出す。
- 1 回の表示あたりのリクエスト数と転送量は仮定せず、実際の画面で開発者ツールのネットワークタブを見て測る。
- 検索、ルート検索、解析は、常駐する場合のメモリとディスク (全球か、国か)、関数で動かす場合の呼び出し回数と実行時間で見積もる。
- 人件費 (データの更新、監視、障害対応) を足す。ファイルと関数の構成では、変動費が小さく、人件費と初期費用で総額がほぼ決まることが多い。

## 出力の表

機能を行に、要素を列にして、各セルに置き場所と手段を書く。

| 機能 | 保存 | 計算 | 表現 |
|---|---|---|---|
| タイル配信 | 例: オブジェクトストレージの PMTiles | 例: エッジ関数で z/x/y に変換 | 例: ベクトルタイルをブラウザで描く |
| 検索 | | | |
| ルート検索 | | | |
| 解析 | | | |
| 正本と更新 | | | |

案が複数あるときは、この表を案ごとに作り、評価の軸で比べる表を続ける。

## この文書で扱っていない軸

- 認証の提供者の比較、リアルタイムの配信 (WebSocket、SSE、購読) の手段の比較: reference で調べていない。要件に入っていれば、候補ごとに公式ドキュメントで確かめる。
- 信頼の境界を超えるセキュリティ (依存の脆弱性、鍵の管理、CSP の設計): reference で調べていない。
- アクセシビリティ: reference で調べていない。

## 利害関係の開示

このスキル集の作者は Geolonia の関係者である。reference には、Geolonia が提供する住所正規化ライブラリ (normalize-japanese-addresses) が、住所の検索の例として出てくる。比較では特別扱いしない。
