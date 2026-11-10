---
name: map-poc-measure
description: 地図プロダクトの技術選定で、推測ではなく試作して測る手順を組む。1 回の地図表示あたりのタイル数と転送量、表示回数の見積もり、データ (PMTiles、索引、グラフ) の大きさ、対象端末 (iOS、Android の WebView) での動作、描画の速さを測る。「タイルが何枚読まれるか測りたい」「月の表示回数を見積もりたい」「この端末で動くか確かめたい」「PoC を設計したい」と言われたら使う。
---

# map-poc-measure

技術選定で結論を左右する値を、試作して測る。測る値は 5 つある。タイル数で課金される経路と自前配信の費用に効く「1 回の表示あたりのタイル数と転送量」、map-compare-infra の規模をそろえる「月間の地図表示回数」、置き場所を決める「データの大きさ」、対象端末で使えるかを決める「端末での動作」と「描画の速さ」。どれも条件で大きく変わるので、値には必ず測った条件を添え、比べる案ごとに同じ条件で測る。

| reference | 読むとき | 中身 |
|---|---|---|
| [tiles-per-view](references/tiles-per-view.md) | 費用の見積もりに、1 回の表示あたりのリクエスト数が要るとき | 1 回の地図表示あたりのタイル数と転送量の測り方と、OpenFreeMap での実測 |
| [map-load-estimation](references/map-load-estimation.md) | 表示回数を見積もるとき | 月間の地図表示回数の式、提供元ごとの「1 回」の数え方 (初期化、画面に出た回数、セッション、MAU) |
| [data-size](references/data-size.md) | データの大きさが置き場所を左右するとき | PMTiles のズームごとの大きさ (`pmtiles extract --dry-run`)、GeoJSON の大きさと圧縮の実測 |
| [device-testing](references/device-testing.md) | 対象端末で動くか確かめるとき | ヘッドレス、エミュレータ、実機、WebView の確かめ方と、ヘッドレスの Chromium で地図が描けない問題 |
| [render-performance](references/render-performance.md) | 描画の速さが要件に入るとき | 最初の描画までの時間、フレームの間隔、メモリの測り方と、条件のそろえ方 |

測った値を使う先は次のとおり。

- タイル数と転送量: map-compare-infra の [criteria](../map-compare-infra/references/criteria.md) の「費用の見積もり方」と、map-compare-arch の [self-hosting](../map-compare-arch/references/self-hosting.md) の「費用の見積もり」(損益分岐)
- 月間の地図表示回数: map-compare-infra の費用表の規模 (月 10 万、100 万、1,000 万回)
- データの大きさ: map-compare-arch の置き場所の判断 ([cloud-native-formats](../map-compare-arch/references/formats/cloud-native-formats.md)、[capabilities/tiles](../map-compare-arch/references/capabilities/tiles.md))
- 端末での動作と描画の速さ: map-compare-arch の対象端末の条件と、map-compare-library のライブラリの選定

## 入力

測り始める前に、次をそろえる。プロダクト概要があればそこから読み、無ければ依頼から読み取る。

- 何を決めるために測るか: どの段階 (arch、infra、library) のどの判断か。比べる案 (例: 供給元 A と B、GeoJSON とタイル、ライブラリ A と B)
- 課金の経路: 候補の供給元と、使うライブラリ。タイル数を測る意味があるかがこれで決まる ([criteria](../map-compare-infra/references/criteria.md) の「課金単位と経路を先に決める」)
- 利用者と場面: よく開く地点とズーム、典型的な操作の筋書き (開いて閉じるだけか、パンとズームを繰り返すか)、画面に置く地図の数
- 対象端末: 画面の大きさと DPR、下限の機種、ブラウザか WebView かネイティブか
- データ: 対象範囲 (矩形か行政区域)、最大ズーム、地物の数と種類
- 既存の値: アクセス解析のページ表示や利用者数があるか

何を決めるために測るかが分からないまま測り始めない。測った値が判断を変えないなら測らずに済む。分からなければ、比べたい案を選択肢で聞く。課金の経路が決まっていなければ、map-compare-infra の入力 (利用形態、規模、対象地域) の側を先に決める。

## 進め方

1. 判断と測る値を対応させる。下の「何を測るか」の表から、比べる案ごとに要る値だけを選ぶ。
2. 条件を書く。ビューポートと DPR、地点とズーム、スタイル、操作の筋書き、キャッシュの有無、CPU の throttling、道具の版。比べる案の間で、比べたい変数の他はそろえる。
3. 手で 1 回通す。Chrome の DevTools (ネットワークパネル、Performance パネル) で、筋書きどおりに操作して値を読み、HAR を残す。ここで、数える対象 (タイルの URL の形、キャッシュから返ったもの) と測り終わりの時点 (地図の `idle`) を決める。
4. 自動にして繰り返す。Playwright でケースごとに新しいブラウザコンテキストを作り、同じ筋書きを 2 回以上通す。ヘッドレスの Chromium では先に WebGL の描画器の名前と地図の `load` の到達を確かめる ([device-testing](references/device-testing.md))。実データを読む処理 (タイル生成、切り出し、大きな GeoJSON) は、OS のメモリと CPU の上限を掛けて流す。
5. 値ごとの reference の手順で測る。タイル数は [tiles-per-view](references/tiles-per-view.md)、表示回数は [map-load-estimation](references/map-load-estimation.md)、大きさは [data-size](references/data-size.md)、速さは [render-performance](references/render-performance.md)、端末は [device-testing](references/device-testing.md)。
6. 実機で確かめる。描画の速さと端末での動作は、ヘッドレスや CPU の throttling の値で結論を出さず、下限の機種の実機で同じ筋書きを通す。
7. 結果を、使う先のスキルの形に合わせて渡す。タイル数は「初回の表示」と「筋書きを通した合計」の 2 つの値を幅として criteria の費用の計算に当てる。表示回数は式と係数を添える。値ごとに測ったものか仮定かを書く。
8. 結果がその段階の前提と食い違ったら (例: 1 回の表示あたりのタイル数が criteria の仮置きと大きく違う、データが端末に収まらない)、その段階に戻って、崩れた前提だけを入れ替えて比べ直す。

## 何を測るか

| 判断 | 測る値 | 測らずに済むとき | reference |
|---|---|---|---|
| タイル数で課金される供給元の月額 | 1 回の表示あたりのタイル数 (初回と筋書き) | 候補がすべて表示回数か MAU で課金される経路のとき | [tiles-per-view](references/tiles-per-view.md) |
| 自前配信と外部の供給元の損益分岐 | 1 回の表示あたりのタイル数と転送量、データの大きさ | 外部通信が許されず、自前配信しか残らないとき | [tiles-per-view](references/tiles-per-view.md)、[data-size](references/data-size.md) |
| 費用表の規模 | 月間の地図表示回数 (と MAU) | 規模が要件で決まっているとき | [map-load-estimation](references/map-load-estimation.md) |
| 端末への同梱か配信か、GeoJSON かタイルか | 範囲とズームごとの大きさ、GeoJSON の圧縮後の大きさ | 大きさが明らかに小さい (数百 KB) か大きい (数十 GB) とき | [data-size](references/data-size.md) |
| ライブラリの選定、地物の数の上限 | 最初の描画までの時間、フレームの間隔、メモリ | 対象端末が限られ、すでに同じ構成が動いているとき | [render-performance](references/render-performance.md) |
| 対象端末で使えるか | 描けるか、機能 (WebGL2、WebGPU、クロスオリジン分離) の有無、落ちないか | なし。下限の機種では必ず一度は確かめる | [device-testing](references/device-testing.md) |

## 出力

答えは次の順に並べる。

1. 結論: 測った値が判断をどう変えたか (例: 「1 回の表示あたりのタイル数は初回 12、筋書きで 23。criteria の仮置き 15〜30 の範囲に収まり、推奨は変わらない」)。
2. 測った値の表: 行にケース (ビューポート、ズーム、操作、機種)、列に値。値ごとに回数とばらつき。
3. 条件: 道具と版 (ブラウザ、ライブラリ、Playwright、go-pmtiles など)、描画器の名前、地点、スタイルとデータの版、キャッシュの有無、throttling、測った日。
4. 使う先: どのスキルの、どの計算や判断に渡したか。費用に渡したなら計算式。
5. 仮定: 測らずに置いた値 (例: 1 人あたりの月の訪問) と、その値が変わると結論が変わるか。
6. 未確認のこと: 実機で確かめていないこと、提供元の数え方で公表されていないこと。

測るための試作のコードは、利用者の作業ディレクトリに置き、出力にはパスと動かし方だけを書く。

## 注意

- 値には必ず条件を添える。条件の無いタイル数や fps は、比較に使えない。
- reference の実測値 (OpenFreeMap、東京駅付近、2026-11-11) を、他の供給元、地点、画面の値として出さない。自分の条件で測り直す。
- ヘッドレスのブラウザで SwiftShader になったときの描画の速さは、実機の値の代わりにしない。描画器の名前を結果に残す。
- 公開のタイル配信を負荷試験に使わない。筋書きを数回通す程度にとどめ、tile.openstreetmap.org などの OSMF の公開サーバーは計測に使わない。大量の繰り返しは自前の配信か、試験を許す契約のある供給元で行う。
- 数える対象をサーバーに届いたものに限る。ブラウザのキャッシュから返ったリクエストを数えると、タイル数が数倍に膨らむ ([tiles-per-view](references/tiles-per-view.md) の z16 の実測)。
- 規約やライセンスの解釈は、条文から読んだものと推測を分けて書く。法的な判断を断定しない。
- 利害関係の開示: このスキル集の作者は、Geolonia Maps を提供する株式会社 Geolonia に関係している。Geolonia の製品やライブラリを特別扱いせず、候補に入れたときは開示を答えに添える。
