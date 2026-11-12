# 地図のアクセシビリティ

対象: WCAG 2.2 の地図に関わる達成基準、スクリーンリーダー、キーボード操作、地図以外での情報の提供 (一覧、表)、主要な地図ライブラリの対応

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 確かめた版 | WCAG 2.2 (W3C 勧告、2024-12-12、REC-WCAG22-20241212)、MapLibre GL JS 6.17.0 のソース、Leaflet の Accessible maps の文書と 1.9.4 のリファレンス、Google Maps JavaScript API の Advanced Markers の accessible markers の文書 |

## 概要

地図は画像であり、そのままでは目の見えない人に中身が届かず、ドラッグとピンチでしか動かせないとキーボードや指 1 本の人が使えない。地図そのものをすべて読み上げ可能にするのは難しいので、地図が伝える情報 (どこに何があるか) を一覧や表でも出し、地図の操作はキーボードとボタンでもできるようにする。どのライブラリも、キャンバスとコントロールに最低限のラベルとキー操作を持つが、マーカーと主題データの読み上げは作る側の仕事である。

## WCAG 2.2 の地図に関わる達成基準

本文は https://www.w3.org/TR/WCAG22/ (2026-11-11 に確かめた)。地図への当てはめは、注記のないものは推測である。

| 達成基準 (レベル) | 要求の要点 | 地図での当てはめ |
|---|---|---|
| 1.1.1 非テキストコンテンツ (A) | テキストでない内容に、同じ目的のテキストの代替を | 地図が伝える内容 (場所の一覧、範囲、要点) をテキストで出す。飾りの地図は支援技術から隠す |
| 1.3.1 情報及び関係性 (A) | 見た目で伝える構造をプログラムで判別できるように | 凡例と分類を見出しや表で出す |
| 1.4.1 色の使用 (A) | 色だけで情報を伝えない | 分類を色だけで分けず、形、模様、ラベルを足す ([cartography](cartography.md)) |
| 1.4.3 コントラスト (最低限) (AA) | 文字は 4.5:1 以上 | 地図の注記、ポップアップ、凡例の文字。注記を画像の上に載せるときは縁取り (halo) |
| 1.4.10 リフロー (AA) | 2 次元のスクロールなしで読める | 例外: 「使い方や意味に 2 次元の配置が要る部分」。Note に「理解に必要な画像 (地図や図など)」が例として挙がる。地図以外の部分 (一覧、パネル) は例外にならない |
| 1.4.11 非テキストのコントラスト (AA) | 理解に要る図形と UI 部品は 3:1 以上 | マーカー、境界線、ボタンの輪郭と背景の地図 |
| 1.4.13 ホバー又はフォーカスで表示されるコンテンツ (AA) | ホバーやフォーカスで出る内容を消せる、ホバーできる、消えない | ツールチップとポップアップ。Escape で閉じ、マウスを載せても消えない |
| 2.1.1 キーボード (A) | すべての機能をキーボードで | 移動、ズーム、マーカーの選択、ポップアップ |
| 2.1.2 キーボードトラップなし (A) | キーボードでフォーカスを外へ移せる | 地図の canvas から Tab で抜けられる。矢印キーを地図が使うので、Tab の振る舞いを壊さない |
| 2.3.3 インタラクションによるアニメーション (AAA) | 操作で起きる動きを止められる | `flyTo` の長い動き、慣性。`prefers-reduced-motion` に合わせる |
| 2.4.3 フォーカス順序 (A) | 意味と操作を保つ順序 | 検索、一覧、地図、コントロールの順序 |
| 2.4.7 フォーカスの可視化 (AA) | フォーカスが見える | 地図の canvas とマーカーのフォーカスの枠 |
| 2.4.11 フォーカスが隠されない (最低限) (AA、2.2 で追加) | フォーカスのある部品が作者の内容で完全に隠れない | ボトムシートや固定のヘッダーがフォーカスしたマーカーを隠す |
| 2.5.1 ポインタのジェスチャ (A) | 複数点や経路のジェスチャを 1 本で | 解説の例: ピンチで拡大する地図に、プラスとマイナスのボタンも置く |
| 2.5.7 ドラッグ動作 (AA、2.2 で追加) | ドラッグの機能をドラッグなしの 1 本のポインタで | 解説の例: 地図をドラッグで動かせ、上下左右のボタンでも動かせる。キーボードの代替だけでは満たさない |
| 2.5.8 ターゲットのサイズ (最低限) (AA、2.2 で追加) | 24 x 24 CSS px 以上 (間隔、同等の別の部品、文中、ユーザーエージェント、必須の例外) | マーカーとコントロール。地図の点は、同じ機能の一覧があれば「同等」の例外に当たりうる (推測) |
| 4.1.2 名前 (name)・役割 (role)・値 (value) (A) | 部品の名前と役割をプログラムで判別できる | コントロールのボタンのラベル、マーカーの名前 |
| 4.1.3 ステータスメッセージ (AA) | フォーカスを移さずに状態を支援技術へ | 「12 件見つかりました」「現在地を取得できません」を `aria-live` などで |

4.1.1 構文解析は WCAG 2.2 で「廃止」とされている (同ページ)。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| 一覧や表を地図と並べる | 地図を見られない人に中身を届ける (1.1.1、1.3.1)。2.5.8 の「同等」の代替にもなる | 一覧の設計が要る | 一覧と地図の切り替え、分類の見出しと畳み、重要度で並べる (2026-11-10 実測、[unlock-your-trip](../../../../examples/unlock-your-trip/README.md)) | 実測 |
| 地図の canvas のラベルとキー操作 | キーボードで地図を動かす (2.1.1) | 地図全体で 1 つの要素。中の地物は読み上げない | MapLibre 6.17.0: canvas に `tabindex="0"` (操作できる地図のとき)、`role="region"`、`aria-label` (既定 "Map")。`keyboard` (既定 true) で、`+` / `-` でズーム 1 (Shift で 2)、矢印で 100 px 移動、Shift と左右で 15 度回転、Shift と上下で 10 度傾ける。Leaflet: `keyboard` (既定 true)、`keyboardPanDelta` (既定 80 px) | https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/map.ts 、https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/handler/keyboard.ts 、https://leafletjs.com/reference-1.9.4.html |
| UI の文言を日本語に | スクリーンリーダーが英語のラベルを読む | 文言の ID を知る必要がある | MapLibre の `locale` (`Map.Title`、`NavigationControl.ZoomIn`、`Popup.Close` など)。Leaflet は `translate` の地図の設定か i18n の関数 (Leaflet の Accessible maps の文書の記述) | https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/default_locale.ts 、https://leafletjs.com/examples/accessibility/ |
| マーカーに名前とフォーカス | どの点か読み上げる (4.1.2)、キーボードで選ぶ | 件数が多いと Tab の回数が増える | MapLibre 6.17.0 の `Marker`: 既定のマーカーに `aria-label` (既定 "Map marker") を付ける。`tabindex="0"` を付けるのは、ポップアップを持つときと、既定のマーカーで `draggable` のとき (ドラッグできるマーカーは矢印で 1 px、Shift で 10 px 動く)。自前の要素のマーカーのフォーカスは作る側に任される。Leaflet: マーカーの `keyboard` (既定 true)、`title`、`alt` (既定 'Marker') を一意で説明的に。Google の Advanced Markers: `gmpClickable` を true にし `title` を付ける。Tab で最初のマーカー、矢印でマーカー間を移り、Enter で押す | https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/marker.ts 、https://leafletjs.com/examples/accessibility/ 、https://developers.google.com/maps/documentation/javascript/advanced-markers/accessible-markers |
| 描画のレイヤの地物を読めるようにする | canvas の中の地物はフォーカスも読み上げもできない | 自分で作る | 地物を一覧に出し、一覧で選ぶと地図が寄ってポップアップを開く。表示範囲が変わったら件数を `aria-live` で知らせる (推測) | (推測) |
| ポップアップのフォーカス | 開いた中身を読ませる、閉じたら戻す | | MapLibre の Popup は `focusAfterOpen` (既定 true) で最初のフォーカスできる要素に移り、閉じるボタンに `aria-label` (`Popup.Close`)。Google の情報ウィンドウは閉じるとマーカーにフォーカスが戻る | https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/popup.ts 、https://developers.google.com/maps/documentation/javascript/advanced-markers/accessible-markers |
| 動きを減らす | 2.3.3、前庭障害 | | MapLibre の `reduceMotion` (既定 undefined。未指定なら端末の設定に従い、true で慣性を止める)。CSS とアプリの `flyTo` は `prefers-reduced-motion` を見て `jumpTo` に (推測) | https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/map.ts 、https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion |
| 飾りの地図を隠す | 意味の無い地図をフォーカスさせない | | Leaflet の文書は、飾りの地図にはフォーカスできる子を置かず、`inert` などで支援技術から隠すよう勧める。MapLibre は `interactive: false` で canvas の `tabindex` が -1 になる | https://leafletjs.com/examples/accessibility/ 、https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert |

## 判断を左右すること

- 適合の要件: 公共案件では JIS X 8341-3 や WCAG 2.x の AA への適合が求められることがある。要件の版と達成基準の範囲を先に聞く。
- 地図の役割: 地図が主役でも、地図で伝える情報を一覧や表で出せるか。出せないもの (形、広がり) は要約の文で出す。
- マーカーの件数: 数十件を超えるなら、Tab で 1 つずつ回すより一覧から選ぶほうが速い (推測)。
- 使うライブラリ: 既定のラベルとキー操作は版で変わる。使う版のソースで確かめる。

## 手順

1. 地図が伝える情報を書き出し、一覧、表、文に置き換える。地図を見ない人がそれで用を足せるかを確かめる。
2. 地図の canvas のラベルを日本語にし (MapLibre の `locale` の `Map.Title`、Leaflet の translate)、地図が何の地図かを名前に含める。
3. キーボードだけで、検索、一覧、地図の移動とズーム、マーカーの選択、ポップアップの開閉、地図の外へのフォーカスの移動を試す。
4. ズームと移動のボタンを置く (2.5.1、2.5.7)。的を 24 x 24 CSS px 以上にする (2.5.8)。
5. 色、コントラスト、注記を [cartography](cartography.md) の手順で確かめる (1.4.1、1.4.3、1.4.11)。
6. 状態の変化 (件数、現在地の失敗、読み込み中) を `aria-live` で知らせる (4.1.3)。
7. スクリーンリーダーで試す。Leaflet の文書は Narrator、Orca、TalkBack、VoiceOver を挙げ、キーボードだけとスクリーンリーダーの両方で試すよう勧める。

## 落とし穴

- MapLibre の canvas の `aria-label` の既定は英語の "Map" で、日本語のページでも英語で読まれる。`locale` で直す。
- MapLibre 6.17.0 では、ポップアップを持たない既定のマーカーは `tabindex` を持たず、Tab で選べない。クリックで何かするマーカーは、ポップアップを付けるか、自分で `tabindex` とキー操作を足す。
- 地図の矢印キーの操作は、canvas にフォーカスがあるときだけ効く。ページのスクロールのつもりで矢印を押すと地図が動く場合があることを、利用者は知らない (推測)。
- 2.5.7 は、キーボードの代替だけでは満たさない (解説の記述)。ポインタで押せる移動のボタンか、一覧から選んで寄る手段が要る。
- 1.4.10 のリフローの例外は地図そのものだけで、地図の横のパネルや一覧には及ばない。
- 色覚の模擬やコントラストの計算は、背景の地図の色 (道路、緑地、水域) との組み合わせで確かめる。白地の上だけで確かめない (推測)。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- ライセンスの論点は無い。WCAG 2.2 は W3C の文書で、引用と参照に使う。ここで挙げたライブラリの機能は本体の一部である (MapLibre GL JS は BSD 3-Clause、Leaflet は BSD-2-Clause)。
- 読み上げ用の一覧に出す名称や住所にも、元データの帰属と条件 (ODbL など) が及ぶ (geo-software-legal-check の [attribution](../../geo-software-legal-check/references/attribution.md))。

## 出典

- https://www.w3.org/TR/WCAG22/ (達成基準の本文、レベル、1.4.10 の例外と Note、2.5.8 の例外、4.1.1 の廃止。2026-11-11)
- https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html (地図を上下左右のボタンでも動かせる例、キーボードの代替だけでは満たさないこと、ユーザーエージェントのスクロールは対象外。2026-11-11)
- https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html (ピンチの地図にプラスとマイナスのボタンを置く例。2026-11-11)
- https://github.com/maplibre/maplibre-gl-js/tree/v6.17.0/src/ui (map.ts の canvas の属性と `keyboard`、`locale`、`reduceMotion`、keyboard.ts のキー操作、marker.ts の `_updateTabIndex` と `aria-label`、popup.ts の `focusAfterOpen`、default_locale.ts の文言の ID。2026-11-11)
- https://leafletjs.com/examples/accessibility/ (Leaflet の Accessible maps。2026-11-11)
- https://leafletjs.com/reference-1.9.4.html (`keyboard`、`keyboardPanDelta`、マーカーの `keyboard`、`title`、`alt`。2026-11-11)
- https://developers.google.com/maps/documentation/javascript/advanced-markers/accessible-markers (`gmpClickable`、`title`、マーカー間のキー操作、既定のマーカーの大きさ。2026-11-11)

## 未確認のこと

- Google Maps JavaScript API の地図そのもののキーボードショートカットの一覧。accessible markers のページには無かった。
- JIS X 8341-3 の現行版が WCAG 2.2 の追加の達成基準 (2.4.11、2.5.7、2.5.8 など) を取り込んでいるか。
- スクリーンリーダーごとに、MapLibre の canvas (`role="region"`) がどう読まれるか。実機で試していない。
- OpenLayers、Mapbox GL JS、Geolonia Maps の既定のアクセシビリティの対応。読んでいない。
