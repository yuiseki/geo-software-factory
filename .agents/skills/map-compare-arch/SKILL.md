---
name: map-compare-arch
description: 地図プロダクトのアーキテクチャを、保存・計算・表現の 3 つの要素と、クラウド・エッジ・ブラウザ/アプリの 3 つの置き場所の組み合わせとして比較し決める。タイル配信、検索 (ジオコーディング、POI)、ルート検索、解析、正本と更新のそれぞれで、外部の API に任せるか、常駐するサーバーを自前で動かすか、ファイルと関数で済ませるかを比べる。ブラウザの最先端の API (Service Worker、OPFS、WebAssembly、WebGPU など) で保存と計算をブラウザに置けるかを先に検討する。「地図サービスの構成を考えたい」「タイルを自前で配信したい」「PMTiles を使いたい」「オフラインで地図を使いたい」「検索やルート検索を自前で持ちたい」「サーバーレスで地図」「地物を編集・更新したい」「正本の DB をどうするか」と言われたら使う。
---

# map-compare-arch

後で書く。

| reference | 読むとき | 中身 |
|---|---|---|
| [criteria](references/criteria.md) | 比較を始める前に、いつも | 3 つの要素と 3 つの置き場所による判断の軸 |
| [self-hosting](references/self-hosting.md) | タイルを自前で配信するとき | 自前でのタイル生成と配信の構成、費用、運用の負担 |
| [capabilities/tiles](references/capabilities/tiles.md) | タイル配信の置き場所を決めるとき | 3 つの型と置き場所ごとの実現手段 |
| [capabilities/search](references/capabilities/search.md) | 検索の置き場所を決めるとき | 同上 |
| [capabilities/routing](references/capabilities/routing.md) | ルート検索の置き場所を決めるとき | 同上 |
| [capabilities/analysis](references/capabilities/analysis.md) | 解析の置き場所を決めるとき | 同上 |
| [capabilities/source-of-truth](references/capabilities/source-of-truth.md) | 地物を書き換える機能があるとき、正本をどこに置くかを決めるとき | 正本の候補、強い整合性とトランザクション、成果物への反映 |
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

後で書く:

- 入力 (要件のうち、置き場所を左右するもの)
- 進め方
- 出力の形 (機能ごとに 3 つの要素の置き場所を表にする)
- 注意 (ブラウザの対応状況は変わるので、答える前に確かめ直す)
