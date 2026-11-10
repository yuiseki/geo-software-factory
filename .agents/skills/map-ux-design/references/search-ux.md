# 地図の検索と入力補完

対象: 検索ボックス、入力補完、結果の一覧と地図の連動、表示範囲での絞り込み、0 件のとき

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 確かめた版 | WAI-ARIA Authoring Practices Guide の Combobox Pattern、MDN (KeyboardEvent.isComposing、keydown)、Nominatim Usage Policy、Google Maps JavaScript API の Place Autocomplete (New) |

## 概要

地図の検索には、住所や地名から場所を引く (ジオコーディング)、施設や店を引く (POI 検索)、自分のデータの中を引く、の 3 種類があり、同じ検索ボックスに混ぜると結果の並びが読めなくなる。日本語では、IME で変換している間のキー入力と、住所の表記ゆれ (漢数字と算用数字、「丁目」「番地」「-」、旧字体) が、入力補完と照合の両方を壊しやすい。結果は一覧と地図を連動させ、0 件のときに何をすればよいかを示す。検索の提供元 (API) は map-compare-infra で選ぶ。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| 入力補完 (combobox) | 打ち終える前に候補を出す | 1 文字ごとに問い合わせると、提供元の回数制限と課金に当たる | WAI-ARIA の combobox パターン (`role="combobox"`、`aria-expanded`、`aria-controls`、`aria-activedescendant`、`aria-autocomplete`、一覧は `role="listbox"`) | https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ |
| IME の変換中を無視する | 変換を確定する Enter で検索が走る、変換途中の文字で問い合わせる | ブラウザで振る舞いが違う | `keydown` で `event.isComposing` か `event.keyCode === 229` のときは処理しない。`compositionend` の後に問い合わせる | https://developer.mozilla.org/en-US/docs/Web/API/Element/keydown_event 、https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/isComposing |
| 問い合わせを遅らせる (debounce)、最小文字数 | 問い合わせの回数と費用を減らす | 遅らせすぎると候補が遅く感じる | Google は Place Autocomplete (New) を自前で呼ぶ場合に「最初の 3〜4 文字を打つまで遅らせる」ことを案内する。日本語の地名は 2 文字 (例: 渋谷) で意味を持つので、そのまま当てはめない (推測) | https://developers.google.com/maps/documentation/javascript/place-autocomplete-new |
| セッション単位の課金 | 入力補完と選んだ後の詳細取得をまとめて課金する | 提供元ごとに課金単位が違う | Google の Place Autocomplete (New) はセッショントークンを使うとセッション単位の課金になり、JavaScript の `PlaceAutocompleteElement` (`gmp-place-autocomplete`) はセッションを自動で扱う。住所と座標だけなら、選んだ候補を Geocoding API で引くほうが安い場合がある (約 4 回以内で選ばれるとき) | https://developers.google.com/maps/documentation/javascript/place-autocomplete-new |
| 住所の正規化 | 表記ゆれで同じ住所が別物になる | 正規化の規則を自分で持つか、外部に任せるか | アドレス・ベース・レジストリ (町字の漢字、カナ、ローマ字の表記を持つ) を正本にして照合する | map-compare-data の [abr](../../map-compare-data/references/sources/abr.md) |
| 表示範囲での絞り込み | 「この辺りで探す」 | 範囲の外に正解があると 0 件に見える | 地図を動かしたら自動で検索せず、「この範囲で再検索」のボタンを出す (推測)。範囲内で 0 件なら範囲を広げる API もある (OpenPOI API の suggest は bbox 内で 0 件なら全国に広げる) | map-compare-infra の [openpoiapi](../../map-compare-infra/references/search/openpoiapi.md) |
| 結果の一覧と地図の連動 | どの点がどの結果か分からない | 件数が多いと地図の点が重なる | 一覧の項目にフォーカスやホバーしたら地図の点を強調し、点を押したら一覧の項目へ移る。件数が多ければ [many-features](many-features.md) の手段を使う | (推測) |

## 判断を左右すること

- 何を探すか: 住所、地名、施設、自分のデータ。混ぜるなら、結果を種類ごとに見出しで分ける。
- どこで引くか: 外部の API か、自前の索引か (map-compare-arch)。自分のデータが数千件までなら、ブラウザの中で引ける (推測)。
- 提供元の規約: 入力補完を許すか、結果を保存してよいか、別の地図の上に出してよいか。Nominatim の公開サーバーは、入力補完を「受け入れられない使い方」として禁じ、上限を 1 秒に 1 回とし、繰り返す同じ問い合わせを障害とみなして止めることがある (https://operations.osmfoundation.org/policies/nominatim/ 、確かめた日 2026-11-11)。Google の検索結果は Google の地図以外に出せない制約がある (map-compare-infra の各 reference)。
- 日本語の入力: 漢字、かな、カナ、ローマ字のどれで打たれるか。かなで引けるか (読みの索引が要る)。

## 手順

1. 何を探すかを決め、種類ごとに引く先 (API、自前の索引) を決める。
2. 検索ボックスは `<input type="search">` にラベルをつけ、入力補完は combobox のパターンで作る。下矢印で候補へ、Enter で確定、Escape で閉じる。
3. IME の変換中のキー入力を無視し、`compositionend` か、変換していない入力のあとに問い合わせる。
4. 問い合わせを遅らせ (debounce)、同じ文字列の結果は端末にキャッシュする。提供元の回数制限と課金単位に合わせる。
5. 住所は正規化してから照合する。打たれた表記と正規化した表記の両方を残し、どちらで当たったかを示す。
6. 結果は一覧と地図の点を連動させ、選んだら地図をその場所に寄せる。地物の大きさに合わせ、点なら決めたズーム、面なら範囲に合わせる。
7. 0 件のときは、範囲を広げる、表記を変える (番地を外す) など、次の一手を示す。候補の件数や 0 件の知らせは `aria-live` などでスクリーンリーダーにも届ける (WCAG 2.2 の 4.1.3、[accessibility](accessibility.md))。

## 落とし穴

- 変換を確定する Enter で検索が走る。Firefox 65 から IME の変換中にも `keydown` が出るようになり、最後の文字で `compositionend` が `keydown` より先に来ると `isComposing` が false になる。MDN は `keyCode` が 229 かも見るよう勧めている (https://developer.mozilla.org/en-US/docs/Web/API/Element/keydown_event 、確かめた日 2026-11-11)。
- 住所の数字の表記ゆれ: 「一丁目」「1丁目」「1-」、「番地」「番」、全角と半角、「ケ」「ヶ」「が」。正規化を通さずに文字列で照合すると当たらない (推測。ABR の町字マスターは漢字、カナ、ローマ字の表記を持つ)。
- 住居表示の地域と地番の地域で、同じ「〇番〇号」の意味が違う。ABR の町字マスターには住居表示か否か (`rsdt_addr_flg`) がある ([abr](../../map-compare-data/references/sources/abr.md))。
- 英語圏の「3〜4 文字まで待つ」をそのまま日本語に当てると、2 文字の地名で候補が出ない (推測)。
- 地図を動かすたびに自動で検索すると、問い合わせが増え、一覧が勝手に入れ替わって読めない (推測)。
- 公開の OSM のサーバー (Nominatim の公開インスタンス) を製品の入力補完に使わない。規約で禁じられている。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- OSM 由来のジオコーディングの結果は ODbL のデータであり、結果を保存して自分のデータベースにすると、派生データベースの扱いが問題になりうる (map-legal-check の [odbl](../../map-legal-check/references/odbl.md))。どこまでが「生成された著作物」かは、ここでは確かめていない。
- 商用の検索 API の結果の保存、表示先の地図の制約は提供元の規約で決まる (map-compare-infra の各 reference と map-legal-check の [api-terms](../../map-legal-check/references/api-terms.md))。
- ABR は公共データ利用規約 (PDL1.0) が基本で、地番マスターには別の規約が加わる ([abr](../../map-compare-data/references/sources/abr.md))。

## 出典

- https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ (combobox の役割、属性、キー操作。2026-11-11)
- https://developer.mozilla.org/en-US/docs/Web/API/Element/keydown_event (IME の変換中の keydown、`keyCode` 229 の扱い。2026-11-11)
- https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/isComposing 、https://developer.mozilla.org/en-US/docs/Web/API/Element/compositionend_event (変換中の判定。2026-11-11)
- https://operations.osmfoundation.org/policies/nominatim/ (入力補完の禁止、1 秒 1 回、キャッシュ。2026-11-11)
- https://developers.google.com/maps/documentation/javascript/place-autocomplete-new (セッション、遅らせる文字数、`PlaceAutocompleteElement`。2026-11-11)

## 未確認のこと

- Safari と iOS の日本語 IME で、確定の Enter の `keydown` が `isComposing` と `keyCode` でどう見えるか。実機で確かめていない。
- Google の旧来の Autocomplete が新規の利用者に提供されているか。Place Autocomplete (New) のページには書かれていなかった。
- 日本語の入力補完に向く最小文字数と遅らせる時間の値。公式の目安を見つけていない。
