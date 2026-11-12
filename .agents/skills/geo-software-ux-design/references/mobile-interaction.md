# モバイルでの地図の操作

対象: ページのスクロールと地図の操作の奪い合い (cooperative gestures)、ジェスチャ、タッチの的の大きさ、ボトムシートと一覧の切り替え、全画面表示

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 確かめた版 | MapLibre GL JS 6.17.0 (`src/ui/map.ts`、`src/ui/handler/cooperative_gestures.ts`、`src/ui/control/attribution_control.ts`)、Google Maps JavaScript API (Controlling Zoom and Pan)、Leaflet 1.9.4、leaflet-gesture-handling 1.2.2、WCAG 2.2 (W3C 勧告 2024-12-12) |

## 概要

ページの中に埋め込んだ地図は、指でページをスクロールしようとすると地図が動き、ページが進まなくなる (スクロールの奪い合い)。全画面の地図では、地図と一覧、詳細をどう切り替えるかと、指で押せる的の大きさが問題になる。ドラッグとピンチは、片手や指 1 本で操作する人には難しいので、ボタンでも同じことができるようにする (WCAG 2.2 の 2.5.1、2.5.7)。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| cooperative gestures | スクロールの奪い合い | 地図を動かすのに 2 本指、ズームに Ctrl かコマンドキーとホイールが要る。知らないと戸惑う (案内が出る) | MapLibre の `cooperativeGestures` (既定 false)。有効にすると、モバイルは 2 本指、デスクトップは Ctrl (Mac はコマンドキー) を押したときだけ動き、普通の操作では案内の画面が出る。傾けるのは 3 本指になる。FullscreenControl で全画面にすると無効になる。案内の文言は `locale` で日本語にできる (`CooperativeGesturesHandler.MobileHelpText` など)。Google の `gestureHandling` は `cooperative`、`greedy`、`none`、`auto` (既定。iframe の中なら cooperative、外なら greedy)。Leaflet はコアに無く、プラグイン leaflet-gesture-handling (MIT、npm 1.2.2、リポジトリの最後のコミットは 2021-10-22) | https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/map.ts 、https://maplibre.org/maplibre-gl-js/docs/examples/cooperative-gestures/ 、https://developers.google.com/maps/documentation/javascript/interaction 、https://github.com/elmarquis/Leaflet.GestureHandling |
| 静的な画像と「地図を開く」ボタン | 奪い合いをそもそも起こさない、初期表示を軽くする | 操作するには 1 回押す | 静的な地図画像 (提供元の Static API か、自分で撮った画像) を置き、押したら対話的な地図か全画面に切り替える ([initial-load](initial-load.md)) | (推測) |
| ズームと移動のボタン | ピンチとドラッグができない人の代わり | ボタンの場所を取る | MapLibre の NavigationControl (ズームと方位)。WCAG の 2.5.7 の解説は、地図をドラッグで動かせるうえに上下左右のボタンもある例を挙げる。移動のボタンはどのライブラリも既定では持たないので自分で足す (推測) | https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html 、https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html |
| タッチの的の大きさ | 押し間違い | 地図の上のマーカーとボタンが場所を取る | WCAG 2.2 の 2.5.8 (AA) は 24 x 24 CSS px 以上 (間隔などの例外あり)、2.5.5 (AAA) は 44 x 44 CSS px 以上。Google の Advanced Markers の文書は、既定のマーカーは AA の最小の大きさを満たし、AAA には大きくする必要があるとする | https://www.w3.org/TR/WCAG22/ 、https://developers.google.com/maps/documentation/javascript/advanced-markers/accessible-markers |
| 一覧と地図の切り替え (タブ、ボトムシート) | 小さな画面で地図と一覧を両立させる | 地図を開くたびに位置や選択を保つ設計が要る | 一覧を正本にし、地図はタブで切り替える。一覧は分類の見出しで分け、分類ごとに畳めるようにし、分類の中は重要度 (1〜5 の星) で並べる (2026-11-10 実測、[unlock-your-trip](../../../../examples/unlock-your-trip/README.md)) | 実測 |
| 全画面表示 | 埋め込みの小さな地図で操作しにくい | iOS の Safari では Fullscreen API が要素に使えない場合がある (未確認) | MapLibre の FullscreenControl (全画面中は cooperative gestures が外れる) | https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/map.ts |
| `touch-action` と画面の高さの単位 | ブラウザの既定のジェスチャと地図のジェスチャの衝突、アドレスバーで高さが変わる | 地図のライブラリが自分で設定することがある | CSS の `touch-action`、`dvh` などの単位、ノッチを避ける `env(safe-area-inset-*)`。MapLibre は cooperative gestures を有効にすると `touch-action: pan-x pan-y` のクラスを付ける (ソースの注記) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/touch-action 、https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/env 、https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/handler/cooperative_gestures.ts |

## 判断を左右すること

- 地図がページの一部か、画面の全部か: 一部なら cooperative gestures か静的な画像。全部なら奪い合いは起きないので、普通のジェスチャのままにする。
- 利用者が片手で、歩きながら使うか: 的を大きくし、主な操作を画面の下半分に置く (推測)。
- 地図の役割: 一覧が主なら、地図はタブか折りたたみにする。
- iframe で配るか: Google の `auto` は iframe の中で cooperative になる。MapLibre は自動では切り替わらないので、埋め込み用の設定を別に持つ。

## 手順

1. 地図をページの一部に置くか、全画面にするかを決める。
2. ページの一部なら、cooperative gestures を有効にし、案内の文言を日本語にする。地図が主役でないなら、静的な画像と「地図を開く」ボタンも比べる。
3. ズームのボタンを置き、ドラッグの代わりになる移動の手段 (ボタンか、一覧から選ぶと寄る) を用意する。
4. マーカーとボタンの的を 24 x 24 CSS px 以上にし、近い的どうしは間隔をあける。片手で使うなら 44 x 44 CSS px を目安にする。
5. 一覧と地図を切り替える画面なら、切り替えても選んだ項目と表示範囲を保つ。
6. 実機 (iPhone と Android) で、ページのスクロール、地図の移動、ズーム、全画面、戻るボタンを試す。

## 落とし穴

- cooperative gestures を有効にした地図では、1 本指でドラッグすると案内が出るだけで地図は動かない。全画面の地図で有効にすると、ただ操作しにくくなる。
- MapLibre の帰属表示は、地図の幅が 640 px 以下だと折りたたまれる (`compact` の既定)。スマートフォンでは押さないと出典が見えない。折りたたんでよいかは geo-software-legal-check の [attribution](../../geo-software-legal-check/references/attribution.md) で確かめる (https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/control/attribution_control.ts)。
- ボトムシートが地図の下半分を隠すと、選んだ点がシートの裏に入る。寄せるときにシートの高さ分の padding を渡す (MapLibre の `fitBounds` や `easeTo` の `padding`) (推測)。
- 地図にフォーカスが移ると、フォーカスのある要素がボトムシートや固定のヘッダーに隠れることがある (WCAG 2.2 の 2.4.11、[accessibility](accessibility.md))。
- iOS の Safari のピンチは、ページ全体の拡大と地図のズームが衝突することがある (推測。実機で確かめる)。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- leaflet-gesture-handling は MIT で、著作権表示とライセンス文を残せばよい。2021 年から更新が無く、Leaflet 2.0 で動くかは確かめていない。
- MapLibre GL JS と Google Maps JavaScript API の機能は本体の一部で、追加のライセンスの論点は無い。

## 出典

- https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/map.ts (`cooperativeGestures` の説明と既定値 false、`locale`、`keyboard` 既定 true。2026-11-11)
- https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/handler/cooperative_gestures.ts と https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/default_locale.ts (案内の文言の ID、バイパスのキー。2026-11-11)
- https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/control/attribution_control.ts (640 px 以下で折りたたむ。2026-11-11)
- https://developers.google.com/maps/documentation/javascript/interaction (`gestureHandling` の値と `auto` の振る舞い。2026-11-11)
- https://www.w3.org/TR/WCAG22/ (2.5.1、2.5.5、2.5.7、2.5.8 の本文。2026-11-11)
- https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html と https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html (地図の例。2026-11-11)
- https://developers.google.com/maps/documentation/javascript/advanced-markers/accessible-markers (既定のマーカーの大きさと WCAG。2026-11-11)
- https://github.com/elmarquis/Leaflet.GestureHandling と https://registry.npmjs.org/leaflet-gesture-handling/latest (MIT、1.2.2、最後のコミット。2026-11-11)

## 未確認のこと

- iOS の Safari で、地図の要素に Fullscreen API が使えるか、FullscreenControl が何をするか。
- MapLibre の cooperative gestures が、iframe の中かどうかで自動で切り替わる設定を持つか。6.17.0 の型は `boolean` だけだった。
- Leaflet 2.0 で使えるジェスチャ制御のプラグイン。
