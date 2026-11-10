# 月間の地図表示回数の見積もり

対象: アクセス解析の値からの見積もり、提供元ごとの「1 回の表示」の数え方の違い (ページ表示、地図の初期化、画面に出た回数、時間枠のセッション、MAU)、試作での数え方

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

各社の課金単位の定義は、map-compare-infra の provider の reference (2026-11-10 確認) から引いた。料金はここに書かず、各 reference と公式の料金ページで確かめる。

## 概要

map-compare-infra の費用は「月間の地図表示回数」で規模をそろえて比べる ([criteria](../../map-compare-infra/references/criteria.md) の「規模の指標を揃える」)。ところが「1 回の表示」の数え方は提供元ごとに違い、同じアプリでもページ表示、地図の初期化、画面に出た回数、セッション、MAU のどれで数えるかで値が変わる。この文書は、アクセス解析の値から月間の地図表示回数を見積もる式と、試作でその式の係数 (1 ページ表示あたりの地図の初期化の回数など) を測る手順を書く。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| アクセス解析のページ表示と訪問 | 地図のあるページの月間ページ表示、訪問、利用者数を得る。既存のサイトがあるときの出発点 | 新しいサービスには値が無い。ページ表示と地図の初期化は 1 対 1 とは限らない | Google Analytics などの解析ツール (版は問わない) | 未確認 (解析ツールごとの定義はこの文書で確かめていない) |
| 地図の初期化を数える仕掛け | 試作の画面で、地図を作った回数 (`new Map()`) と、地図が描けた回数 (`load` イベント) を数え、解析ツールにイベントとして送る | 利用者の操作の筋書きが本番と違えば値も違う | MapLibre GL JS の `load` (「必要な資源がすべて読み込まれた直後」に発火) | https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapEventType/ |
| 画面に出たかを数える仕掛け | 地図がページの下の方にあって、画面に出ないまま離脱される割合を見る。画面に出た回数で課金する提供元の見積もりに使う | `IntersectionObserver` で地図の要素が画面に入ったかを見る方法は、提供元の数え方と一致するとは限らない (推測) | ブラウザの標準 API | 未確認 |
| 提供元の利用量の画面 | 試験公開の期間に、提供元が数えた値を直接読む。見積もりの式の答え合わせになる | 契約と API キーが要る | 各社のダッシュボード | 各 provider の reference |

## 提供元ごとの「1 回」

料金ではなく数え方だけを並べる。定義の出典は各 reference にある。

| 数え方 | 提供元と経路 | 何で 1 回になるか | reference |
|---|---|---|---|
| 地図の初期化 | Mapbox GL JS | `new mapboxgl.Map()` の呼び出しごと。12 時間のタイムアウトがある | [mapbox](../../map-compare-infra/references/providers/mapbox.md) |
| 地図の読み込みの成功 | Google の Maps JavaScript API、モバイルの Maps SDK | 地図の読み込みが成功するごと。パン、ズーム、レイヤーの切り替えでは増えない | [google-maps](../../map-compare-infra/references/providers/google-maps.md) |
| ページの読み込み | MapTiler SDK (Map Session) | 地図を初期化したページかアプリの読み込み 1 回。その後の操作は無制限 | [maptiler](../../map-compare-infra/references/providers/maptiler.md) |
| 画面に出た回数 | Geolonia Maps | 地図が利用者の画面に表示された回数。画面外の地図は数えず、再読み込みで再表示すると 2 回 | [geolonia-maps](../../map-compare-infra/references/providers/geolonia-maps.md) |
| PV | ZENRIN Maps API | JS の地図はローダーの読み込みごとに 1 PV、Web API は原則 1 リクエスト 1 PV | [zenrin-maps-api](../../map-compare-infra/references/providers/zenrin-maps-api.md) |
| 時間枠のセッション | Esri (セッション方式) | 1 セッション最長 12 時間 | [esri-arcgis-location-platform](../../map-compare-infra/references/providers/esri-arcgis-location-platform.md) |
| MAU | Mapbox のモバイル SDK | 課金月の間にアプリ内で Mapbox のサービスを使った利用者 | [mapbox](../../map-compare-infra/references/providers/mapbox.md) |
| タイルのリクエスト | HERE、TomTom、Stadia Maps、CARTO、Google の Map Tiles API、他のライブラリから使う Mapbox と MapTiler など | タイル 1 件ごと (換算のある提供元もある) | [criteria](../../map-compare-infra/references/criteria.md)、測り方は [tiles-per-view](tiles-per-view.md) |

## 判断を左右すること

- 1 ページ表示あたりの地図の初期化の回数: SPA で画面を行き来するたびに地図を作り直す実装では、1 回の訪問で何度も初期化され、初期化ごとに数える提供元 (Mapbox GL JS) で回数が増える。地図を 1 つ作って使い回す実装なら、ページの読み込みと同じ回数に近づく (推測)。
- 地図が画面に出る割合: 地図がページの下にあり、多くの利用者がそこまで見ないなら、画面に出た回数で数える提供元では、ページ表示より少なくなる。
- 1 画面に置く地図の数: 一覧の各行に小さな地図を置くと、1 ページで何回にもなる。静的な地図画像に替えると課金単位が変わる (Mapbox の Static Images API などは別の SKU。[mapbox](../../map-compare-infra/references/providers/mapbox.md))。
- 開いている時間: 業務システムのように 1 日開いたままの画面では、時間枠のセッション (Esri) は表示回数より少なくなる ([criteria](../../map-compare-infra/references/criteria.md))。
- 利用者の数と回数の比: モバイルの MAU 課金は 1 人が何回開いても 1 になる。1 人あたりの起動回数が多いアプリほど、表示回数の課金より MAU の課金が有利になる (推測。単価は reference で比べる)。

## 手順

1. 見積もりの式を書く。月間の地図表示回数 L = 月間の地図ページの表示 P × 1 ページ表示あたりの地図の初期化 i × 地図が画面に出る割合 v (画面に出た回数で数える提供元だけ)。モバイルの MAU 課金なら、月間の利用者数 U を別に置く。
2. P を決める。既存のサイトがあれば、アクセス解析で地図のあるページの月間ページ表示を読む。新しいサービスなら、要件の利用者数 × 1 人あたりの月の訪問 × 1 訪問あたりの地図ページの表示で置き、置いた値を仮定として書く。
3. 試作で i と v を測る。地図を作る箇所で回数を数え、地図の `load` で描けた回数を数え、`IntersectionObserver` で地図の要素が画面に入ったかを数える。典型的な操作の筋書き (一覧から詳細へ行って戻る、など) を手で通し、筋書きごとの回数を書く。
4. 候補ごとに、その提供元の数え方で L を計算する (上の表)。タイル数で課金される経路は、L に 1 回の表示あたりのタイル数を掛ける ([tiles-per-view](tiles-per-view.md))。
5. 月 10 万、100 万、1,000 万回のどこに当たるかを書き、[criteria](../../map-compare-infra/references/criteria.md) の費用表に渡す。式の各係数に、測った値か仮定かを添える。
6. 試験公開ができるなら、提供元の利用量の画面の値と式の値を比べ、ずれが大きい係数を測り直す。

## 落とし穴

- ページ表示をそのまま表示回数にする: SPA の画面遷移で地図を作り直す実装では、初期化の回数がページ表示より多くなる。逆に、地図が画面に出ないページ表示は、画面に出た回数で数える提供元では数えられない。
- 開発中のアクセスを数え忘れる: 開発、検証、自動テスト、監視でも地図は読み込まれる。ヘッドレスブラウザの自動テストを毎回流すと、そのぶん課金単位が増える (推測。テスト用のキーやモックのタイルを使う)。
- 数え方の細部を推測で埋める: 再読み込み、タブの複製、画面の回転で 1 回と数えるかは提供元ごとに違い、公表されていないことがある。分からないものは「未確認」として幅で示す。
- 利用者数と表示回数を混ぜる: MAU と表示回数は別の量で、片方からもう片方を換算するには 1 人あたりの回数の仮定が要る。

## ライセンス上の注意

- 地図の初期化の回数をアクセス解析に送るのは、利用者の行動の計測になる。利用者の位置や閲覧範囲 (地図の中心座標) を一緒に送るなら、プライバシーポリシーとの整合を map-legal-check で確かめる。
- この文書が扱う道具に、コピーレフトなどの継承条件は無い。

## 出典

- https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapEventType/ (`load` イベントの説明。2026-11-11 確認)
- 提供元ごとの課金単位: map-compare-infra の [mapbox](../../map-compare-infra/references/providers/mapbox.md)、[google-maps](../../map-compare-infra/references/providers/google-maps.md)、[maptiler](../../map-compare-infra/references/providers/maptiler.md)、[geolonia-maps](../../map-compare-infra/references/providers/geolonia-maps.md)、[zenrin-maps-api](../../map-compare-infra/references/providers/zenrin-maps-api.md)、[esri-arcgis-location-platform](../../map-compare-infra/references/providers/esri-arcgis-location-platform.md) (各 reference の確認日は 2026-11-10。それぞれの公式の出典は各 reference にある)

## 未確認のこと

- アクセス解析ツールごとのページ表示とセッションの定義。
- 各提供元が、再読み込み、タブの複製、bfcache からの復帰、画面の回転を 1 回と数えるか。
- `IntersectionObserver` で数えた「画面に出た回数」が、Geolonia Maps の数え方と一致するか。
- この文書では、試作の画面で初期化の回数を実測していない。上の手順は、測る仕掛けの組み方だけである。
