---
name: geo-software-arch
description: 地図プロダクトのアーキテクチャを、保存・計算・表現の 3 つの要素と、クラウド・エッジ・ブラウザ/アプリの 3 つの置き場所の組み合わせとして比較し決める。タイル配信、検索 (ジオコーディング、POI)、ルート検索、解析、正本と更新のそれぞれで、外部の API に任せるか、常駐するサーバーを自前で動かすか、ファイルと関数で済ませるかを比べる。ブラウザの最先端の API (Service Worker、OPFS、WebAssembly、WebGPU など) で保存と計算をブラウザに置けるかを先に検討する。「地図サービスの構成を考えたい」「タイルを自前で配信したい」「PMTiles を使いたい」「オフラインで地図を使いたい」「検索やルート検索を自前で持ちたい」「サーバーレスで地図」「地物を編集・更新したい」「正本の DB をどうするか」と言われたら使う。
---

# geo-software-arch

地図プロダクトの要件から、機能ごとに保存・計算・表現をクラウド、エッジ、ブラウザ・アプリのどこに置くかを決める。外部の API に任せる、常駐するサーバーを自前で動かす、ファイルと関数で済ませる、の 3 つの型を同じ軸で並べ、ブラウザに寄せられるかを最初に検討してから、足切り、軸ごとの評価、費用の順に比べて推奨を出す。比較の軸は [criteria](references/criteria.md) にあり、各技術の事実は下の表の reference にある。ここで置き場所を決めてから、geo-software-infra (どの地図データか) と geo-software-library (どのライブラリで描くか) に進む。

| reference | 読むとき | 中身 |
|---|---|---|
| [criteria](references/criteria.md) | 比較を始める前に、いつも | 3 つの要素と 3 つの置き場所による判断の軸 |
| [self-hosting](references/self-hosting.md) | タイルを自前で配信するとき | 自前でのタイル生成と配信の構成、費用、運用の負担 |
| [capabilities/tiles](references/capabilities/tiles.md) | タイル配信の置き場所を決めるとき | 3 つの型と置き場所ごとの実現手段 |
| [capabilities/search](references/capabilities/search.md) | 検索の置き場所を決めるとき | 同上 |
| [capabilities/routing](references/capabilities/routing.md) | ルート検索の置き場所を決めるとき | 同上 |
| [capabilities/analysis](references/capabilities/analysis.md) | 解析の置き場所を決めるとき | 同上 |
| [capabilities/source-of-truth](references/capabilities/source-of-truth.md) | 地物を書き換える機能があるとき、正本をどこに置くかを決めるとき | 正本の候補、強い整合性とトランザクション、成果物への反映 |
| [hosting/static-hosting](references/hosting/static-hosting.md) | アプリやデータのファイルを GitHub Pages、Cloudflare Pages、Vercel などに置くとき | Range への応答、1 ファイルとサイトの上限、無料枠と超えたとき、商用利用、大きな JSON のキャッシュ |
| [formats/cloud-native-formats](references/formats/cloud-native-formats.md) | ファイルのまま置いて読む構成を考えるとき | PMTiles、COG、GeoParquet などの性質 |
| [browser/service-worker](references/browser/service-worker.md) | ブラウザに置けるかを考えるとき、いつも | Service Worker、Cache Storage、PWA |
| [browser/storage](references/browser/storage.md) | 同上 | OPFS、IndexedDB、容量と退避 |
| [browser/wasm](references/browser/wasm.md) | 同上 | WebAssembly、スレッド、クロスオリジン分離 |
| [browser/webgpu](references/browser/webgpu.md) | 同上 | WebGPU と WebGL |
| [browser/workers](references/browser/workers.md) | 同上 | Web Workers、OffscreenCanvas |
| [browser/network](references/browser/network.md) | 同上 | Range、Streams、圧縮、HTTP/3 |
| [browser/device](references/browser/device.md) | 位置、向き、AR などを使うとき | 端末の機能 |
| [browser/local-ai](references/browser/local-ai.md) | ブラウザの中で推論させたいとき | WebNN、組み込み AI、WebGPU での推論 |
| [edge/edge-functions](references/edge/edge-functions.md) | エッジに置けるかを考えるとき | CDN のエッジ関数の制約 |
| [edge/near-user-servers](references/edge/near-user-servers.md) | 閉域網、現地、オフラインで動かすとき | 利用者の近くに置くサーバー |
| [app/native-runtime](references/app/native-runtime.md) | ネイティブアプリの端末に置くとき | アプリの中の保存と計算 |

## 入力

比較の前に、次の要件をそろえる。プロダクト概要があればそこから読み、無ければ依頼から読み取る。

- 要る機能: タイル配信、検索 (住所、POI)、ルート検索、解析、書き込み (誰が、どれくらいの頻度で、同時に何人で)
- データ: 種類、件数と大きさ、対象範囲 (市区町村、都道府県、国、全球)、更新頻度、変更を読み出し側に反映するまでに許される遅れ
- ルールの強制: アクセス制御 (誰が何を見られるか)、不正の防止、監査と履歴が要るか
- 対象端末: ブラウザ (iOS、Android の WebView、Firefox を含むか)、ネイティブアプリ
- 通信: 常時接続か、オフラインや通信が途切れる現場か、閉域網か
- 規模: 月間の地図表示回数、利用者数。小さなアプリを多数作るのか
- 配布形態: SaaS、アプリのストア配布、受託で納品、OSS として公開
- 運用体制と予算

機能、データの大きさと対象範囲、ルールの強制の有無、対象端末の 4 つが分からないまま比較に入らない。足切りがこの 4 つで決まるので、分からなければ先に聞く。聞くときは選択肢で答えられる形にし、1 回に聞く数を絞る。要件が全体に曖昧なら、比較の前にプロダクトの価値から聞き直す (geo-software-product-grilling に当たる手順)。

## 進め方

1. [criteria](references/criteria.md) を読み、要る機能を 5 つの中から選ぶ。「要件から初期案を決める」の表で、出発点の案と重くする軸を決める。
2. 機能ごとに、足切りの条件で置けない場所を消す。信頼の境界 (ルールの強制はブラウザに置けない) と、データの大きさと置き場所の上限を必ず当てる。
3. ブラウザ・アプリに寄せられるかを、`browser/` と [native-runtime](references/app/native-runtime.md) で確かめる。対象端末ごとの対応 (iOS、Android の WebView、Firefox) を表で残す。寄せられない理由が足切りか評価の軸で説明できるときだけ、エッジ、クラウドへ上げる。
4. 機能ごとに `capabilities/` を開き、3 つの型と置き場所ごとの実現手段から案を作る。書き込みがあれば [source-of-truth](references/capabilities/source-of-truth.md) で保存の段階と正本の置き場所を決める。
5. 案を評価の軸で比べる。値は各 reference から写し、reference に「未確認」とあるものは未確認のまま書く。性能や大きさが結論を左右するなら、対象範囲のデータで試作して測ることを勧める。
6. 費用を見積もる。[criteria](references/criteria.md) の「費用の見積もり方」に従う。タイルを自前で配るなら [self-hosting](references/self-hosting.md) で外部の API との損益分岐を求める。
7. ブラウザの対応状況、エッジの上限、料金は、答える前に公式の文書 (MDN、webstatus.dev、各社の制限と料金のページ) で確かめ直す。reference の確認日 (2026-11-10 など) から変わっていれば新しい値を使い、変わったことを書く。
8. 「出力」の形で答える。

## 最初の当たり

案を作るときの出発点。どれも足切りと評価の軸で確かめてから推奨する。

- 閲覧だけの地図: タイルは外部の API か、PMTiles を Range に 206 で答える静的ホスティングや CDN から配る。表示するデータはファイルに置き、ブラウザで絞り込む
- 小さな地図アプリを無料で公開する: アプリは静的ホスティングに置き、PMTiles は Range に 206 で答える置き場所に置く。Cloudflare Pages は 200 を返し、Vercel Hobby と GitHub Pages は商用に制限がある ([static-hosting](references/hosting/static-hosting.md))
- 全国規模の PMTiles を CDN から配る: オブジェクトストレージに置き、エッジ関数で z/x/y に変換してタイル単位でキャッシュする
- オフラインの Web 地図: ホーム画面への追加を前提に、Service Worker と OPFS にタイルと索引を置く
- 住所や POI の検索を自前で持つ: 国や都道府県の範囲なら DuckDB や SQLite の索引を 1 ファイルにして関数かブラウザで引く。日本語の分かち書きに注意する。全球なら常駐の検索サーバー
- 外部の POI 検索で、結果を保存して使いたい: 結果の保存を許す API (geo-software-infra の `search/`) を、正本や索引の初期データの取り込み先にする
- ルート検索を自前で持つ: 国の範囲なら Valhalla のグラフを 1 ファイルにして関数で引く。到達圏が要るなら Valhalla か GraphHopper。公共交通なら GTFS を読むもの
- 大きなデータの解析: GeoParquet や COG を DuckDB や GDAL で直接読む。ブラウザでは DuckDB-Wasm
- 複数人の編集、予約や台帳: 正本はトランザクションを持つ DB (PostgreSQL と PostGIS など)。読み出しは正本から作った成果物
- 位置情報ゲーム、ポイント、決済: 判定と正本はクラウド。ブラウザは表示と入力だけ
- 閉域網、現場: 利用者の近くに置くサーバーに、ファイルと関数を載せる

## 出力

答えは次の順に並べる。

1. 推奨: 1 つ (条件で分かれるなら条件ごとに 1 つ) と、その理由を 2〜3 文。
2. 機能 × 要素の表: [criteria](references/criteria.md) の「出力の表」の形で、各セルに置き場所と手段を書く。
3. 足切りで外した置き場所と理由。
4. 比較表: 案が複数あるとき、行に評価の軸、列に案。各セルに値と reference の根拠。
5. 対象端末ごとの対応: ブラウザに寄せた機能について、iOS、Android の WebView、Firefox などで動くか。
6. 費用表: 規模ごとの月額と、仮定 (1 回の表示あたりのリクエスト数、データの大きさ)。
7. 次に決めること: geo-software-infra で選ぶ地図データ、geo-software-library で選ぶライブラリへの条件 (例: PMTiles を読めること、Wasm を使うならクロスオリジン分離と両立すること)。
8. 確かめた日と、未確認のこと: 結論を左右するのに確かめられなかったこと。試作して測る手順を添える。

## 注意

- ブラウザの対応状況、エッジ関数の上限、料金は頻繁に変わる。reference の値をそのまま最新として出さない。
- 「ブラウザで動く」と「対象の端末で動く」を区別する。iOS と Android の WebView を対象に含むなら、必ずそこで確かめる。
- データの大きさは、対象範囲で測った値で判断する。全球の値から比で推測したものは推測と書く。
- ライセンス (GPL、LGPL、AGPL、ODbL など) は、配布形態ごとに何が求められるかを書く。規約やライセンスの解釈は、条文から読んだものと推測を分けて書き、法的な判断を断定しない。
- 利害関係の開示: このスキル集の作者は、Geolonia Maps を提供する株式会社 Geolonia に関係している。Geolonia の製品やライブラリを特別扱いせず、候補に入れたときは開示を答えに添える。 このスキルの reference には、Geolonia の住所正規化ライブラリ (normalize-japanese-addresses) が住所の検索の例として出てくる。
