---
name: geo-software-ux-design
description: 地図プロダクトの UI と UX を設計する。マーカーが多すぎるとき (クラスタリング、ヒートマップ、ベクトルタイル化)、検索と入力補完、現在地、モバイルの操作 (スクロールの奪い合い、ジェスチャ)、初期表示の速さ、配色と注記、アクセシビリティ (スクリーンリーダー、キーボード、色覚) を扱う。「マーカーが多くて重い」「地図の検索 UI」「スマホで地図が操作しにくい」「地図のアクセシビリティ」と言われたら使う。
---

# geo-software-ux-design

地図プロダクトの画面と操作を設計する。地図が画面の中で担う役割を先に決め、地物の量、検索、現在地、端末、読み込み、配色、アクセシビリティの順に、手段を 1 つずつ選んで理由を残す。手段の事実と出典は下の表の reference にある。どのライブラリで描くかは geo-software-library で選び、このスキルはそのライブラリで画面をどう作るかを決める。

| reference | 読むとき | 中身 |
|---|---|---|
| [many-features](references/many-features.md) | 表示する地物が数百件を超えるとき | クラスタリング、ヒートマップ、ベクトルタイル化、集計の使い分けと、件数ごとの実測 |
| [search-ux](references/search-ux.md) | 地図に検索をつけるとき | 検索ボックス、入力補完、日本語の入力 (IME) と住所の表記ゆれ、結果と地図の連動 |
| [geolocation-ux](references/geolocation-ux.md) | 現在地を使うとき | 許可を求める時機、誤差の円、追従、許可が無いときの代わり |
| [mobile-interaction](references/mobile-interaction.md) | スマートフォンで使うとき、地図をページに埋め込むとき | スクロールの奪い合い (cooperative gestures)、タッチの的の大きさ、一覧と地図の切り替え |
| [initial-load](references/initial-load.md) | 初期表示を速くしたいとき、地図が主役でないページのとき | 遅延読み込み、日本語のグリフ、場所の確保 (CLS)、静的な画像での代替 |
| [cartography](references/cartography.md) | 配色や注記を決めるとき、主題図を描くとき | 注記の読みやすさ、色覚の多様性に配慮した配色、コロプレスの階級区分 |
| [feedback-from-builds](references/feedback-from-builds.md) | 画面の部品と導線を決めるとき、夜に見た目で迷ったとき | 作ったものへの本人の指摘を一般化した既定: 画面の主役と導線、地図の表示範囲、書けない人への見せ方、常時表示の画面、位置を示す 2 つの縮尺の地図、狭い場所の文字 |
| [accessibility](references/accessibility.md) | 公開するとき、アクセシビリティが要件に入るとき | WCAG 2.2 の地図に関わる達成基準、キーボード、スクリーンリーダー、ライブラリごとの対応 |

ブラウザの API の事実 (Geolocation、Wake Lock、Worker) は geo-software-arch の [device](../geo-software-arch/references/browser/device.md) と [workers](../geo-software-arch/references/browser/workers.md)、ライブラリの版とバンドルの大きさは geo-software-library の各 reference (例: [maplibre-gl-js](../geo-software-library/references/libraries/maplibre-gl-js.md))、帰属表示と位置情報の扱いは geo-software-legal-check の [attribution](../geo-software-legal-check/references/attribution.md) と [location-privacy](../geo-software-legal-check/references/location-privacy.md) にある。ここでは繰り返さず、リンクする。

## 入力

設計の前に、次をそろえる。プロダクト概要 (`product-brief.md`) があればそこから読み、無ければ依頼から読み取る。

- 地図の役割: 主役 / 一覧と半々 / 脇役。プロダクト概要の「地図の役割」の節
- 利用者と場面: 歩きながら片手で使うか、机で見るか。閲覧するだけの人 (公開ページの訪問者) がいるか
- 表示するデータ: 地物の種類と件数 (今の件数と、伸びたときの件数)、点か線か面か、更新の頻度
- 現在地が要るか: 誰に、何のために (近くを探す、記録する、ナビ)
- 対象端末とライブラリ: スマートフォンが主か。geo-software-library で決めたライブラリ (未定なら仮に置く)
- 公開の範囲とアクセシビリティの要件: 社内か一般公開か。公共案件で WCAG や JIS X 8341-3 の適合が求められるか

地図の役割と表示するデータの件数が分からないまま手段を選ばない。どちらも手段の選び方を大きく変えるので、分からなければ先に聞く。聞くときは選択肢で答えられる形にし、1 回に聞く数を絞る。

## 進め方

1. 地図の役割を決める。地図が主役でなければ、一覧、映像など利用者が主に見るものを基準にし、地図は切り替えか脇に置く。一覧は地図を読めない人の代わりの手段にもなる ([accessibility](references/accessibility.md))。
2. 件数と形から地物の見せ方を選ぶ ([many-features](references/many-features.md))。件数は伸びたときの値でも確かめる。
3. 検索をつけるなら、何を探すか (住所、施設名、自分のデータ) と、どの API や索引で引くかを分けて決める ([search-ux](references/search-ux.md))。検索の提供元は geo-software-infra で選ぶ。
4. 現在地を使うなら、許可を求める時機、取れないときの代わり、取れたときの表示範囲を決める ([geolocation-ux](references/geolocation-ux.md))。閲覧するだけの人には求めない。
5. スマートフォンでの操作を決める ([mobile-interaction](references/mobile-interaction.md))。ページに埋め込む地図ならスクロールの奪い合いを、全画面の地図なら一覧との切り替えと的の大きさを決める。
6. 初期表示で読むものと後回しにするものを分ける ([initial-load](references/initial-load.md))。地図が主役でないページでは、ライブラリを地図が要るときだけ読む。
7. 配色と注記を決める ([cartography](references/cartography.md))。主題図なら、数を率に直すか、階級区分をどうするかを決める。
8. アクセシビリティの達成基準を、ここまでの決定に当てる ([accessibility](references/accessibility.md))。満たせない基準は、代わりの手段 (一覧、ボタン) で満たすか、満たせないと書く。
9. ライブラリの既定値 (ジェスチャ、ズーム、ラベル、キーボード) は版で変わる。答える前に、使う版の文書かソースで確かめ直す。reference の確認日 (2026-11-11) から変わっていれば新しい値を使い、変わったことを書く。
10. 「出力」の形で答え、プロダクト概要の「技術選定の結果」に「画面と操作 (geo-software-ux-design)」の節を足して書く。前の段階の節は書き換えない。

## 最初の当たり

手段を選ぶときの出発点。どれも reference の条件と、使うライブラリの版で確かめてから推奨する。

- 地物が数百件まで: GeoJSON をそのまま描く。マーカーを DOM 要素で描くライブラリでは、件数が増えたら地図の描画のレイヤ (MapLibre の circle や symbol) に移す
- 点が数千から数十万件で、1 件ずつ選ばせたい: クラスタリング (MapLibre の GeoJSON ソースの `cluster`、Leaflet.markercluster、@googlemaps/markerclusterer)
- 点が多く、分布を見せたい (1 件ずつは選ばせない): ヒートマップか六角形などのグリッドの集計。ヒートマップは値の大きさを読ませる用途には向かない
- データが数 MB を超える、面や線が細かい: ベクトルタイル (tippecanoe で PMTiles に) にして、見えている範囲だけ読む
- 住所の検索: 住所に強いジオコーダーを使い、入力補完は提供元の規約で許されているかを確かめる (Nominatim の公開サーバーは入力補完を禁じている)
- 「近くのものを探す」画面: 現在地はボタンを押したときだけ取り、現在地と近い数件が入るように表示範囲を合わせる
- 記事やページに埋め込む地図: cooperative gestures (2 本指で動かす、Ctrl かコマンドキーとホイールでズーム) を有効にする
- 地図がタブや 2 画面目にある: 地図のライブラリをタブを開いたときに動的 import で読む
- 日本語の注記: MapLibre では `localIdeographFontFamily` (既定は `sans-serif`) で漢字とかなを端末のフォントで描き、グリフの取得を減らす
- 主題図 (コロプレス): 件数ではなく率や密度にし、階級は 3〜7、配色は ColorBrewer や viridis、cividis など色覚の多様性を考えたもの
- 一覧と地図の両方を持つ画面: 一覧を見出しで分類し、分類ごとに畳めるようにし、分類の中は重要度で並べる (旅の名所のチェックリストで使えた、2026-11-10 実測)

## 出力

答えは次の順に並べる。

1. 推奨: 画面の構成 (地図の役割、一覧との関係) と、選んだ手段を 1〜2 文ずつ。
2. 判断を左右した要件: 件数、端末、現在地の要否、公開の範囲。値と出どころ (本人の記録、推測) を添える。
3. 手段の表: 行に課題 (地物の量、検索、現在地、モバイル、初期表示、配色、アクセシビリティ)、列に選んだ手段、外した手段と理由、使うライブラリの機能と版、reference の根拠。
4. 満たす WCAG 2.2 の達成基準と、代わりの手段で満たすもの、満たせないもの。
5. 確かめ方: 実機 (スマートフォン)、キーボードだけ、スクリーンリーダー、色覚の模擬で何を見るか。件数が効く手段は geo-software-poc-measure で測る値を書く。
6. 確かめた日と版: ライブラリの版と、既定値を確かめた日。
7. 未確認のこと: 結論を左右するのに確かめられなかったこと。

## 注意

- ライブラリの既定値は版で変わる。例えば MapLibre GL JS 6.17.0 の GeolocateControl は誤差の円を「95% の信頼水準」と説明するが、W3C の Geolocation の仕様の `accuracy` は 68% の信頼水準であり、説明する文言は仕様に合わせる ([device](../geo-software-arch/references/browser/device.md))。
- 件数の目安は、測った条件 (端末、ブラウザ、ライブラリの版、データの形) と一緒に書く。条件の無い「何件まで大丈夫」は書かない。
- 現在地は、押したときに 1 回だけ取るか、追従するかを分ける。追従するなら電池と画面の点灯 (Wake Lock) も決める。位置をサーバーに送るなら geo-software-legal-check の location-privacy に回す。
- 地図の上の帰属表示を、UI の都合で隠さない。畳む UI を使うときは geo-software-legal-check の attribution で条件を確かめる。
- 見た目の確認は、人が画面で見るのがいちばん確か。スクリーンショットを撮るときは、タイルとフォントが出そろう時間を待ってから撮る。
