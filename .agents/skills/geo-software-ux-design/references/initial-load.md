# 地図の初期表示の速さ

対象: 地図ライブラリの遅延読み込み、スタイルとフォントの読み込み、静的な地図画像での代替、Core Web Vitals (LCP、CLS) への影響

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 確かめた版 | MapLibre GL JS 6.17.0、web.dev の LCP (2025-09-04 更新) と CLS の記事、MDN (動的 import、Intersection Observer、preconnect) |

## 概要

地図のライブラリは大きい (MapLibre GL JS 6.17.0 は本体が gzip で約 295 kB、ワーカーが約 147 kB、[maplibre-gl-js](../../geo-software-library/references/libraries/maplibre-gl-js.md))。そのあとにスタイル、タイル、スプライト、グリフを読むので、地図が主役でないページで最初に読むと、本文の表示まで遅らせる。初期表示で読むものと後回しにするものを分け、地図の場所を先に確保して、画面のずれ (CLS) を起こさない。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| 地図が要るときだけライブラリを読む (動的 import) | 最初の JS の大きさ | 地図を開いたときに待ち時間が出る | `import()` で地図のモジュールを読む。タブを開いたとき、ボタンを押したとき、地図の領域が画面に入ったとき (Intersection Observer)。旅の名所のアプリでは、地図のタブを開いたときに MapLibre を読むようにして、最初に読む JS が約 9 kB になった (Vite のビルドの表示。圧縮前か gzip 後かは記録に無い。2026-11-10 実測、[unlock-your-trip](../../../../examples/unlock-your-trip/README.md)) | https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import 、https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API |
| 地図の場所を先に確保する | 地図が後から出てページがずれる (CLS) | 高さを決める必要がある | 地図の要素に高さか `aspect-ratio` を CSS で与える。web.dev は CLS を 0.1 以下にするよう勧め、利用者の操作で後から出るものは「すぐに場所を作り、読み込み中の表示を出す」のがよいとする | https://web.dev/articles/cls |
| 静的な地図画像で代える | ライブラリとタイルを読まずに場所を示す | 画像の帰属表示が要る。提供元の Static API の規約と課金 | 最初は画像を見せ、押したら対話的な地図に切り替える。画像は LCP の候補になる (`<img>` は候補、`<canvas>` は web.dev の候補の一覧に無い) | https://web.dev/articles/lcp |
| 日本語のグリフを端末のフォントで描く | 漢字とかなのグリフの取得 (範囲ごとの PBF) | 端末ごとにフォントが違い、スタイルのフォント指定は太さ以外効かない | MapLibre の `localIdeographFontFamily` (既定 `'sans-serif'`)。CJK の文字はスタイルのフォント設定を無視して端末のフォントで描く。`false` にするとスタイルのフォントを使う | https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/map.ts 、https://maplibre.org/maplibre-gl-js/docs/examples/use-locally-generated-ideographs/ |
| 接続を先に張る | タイルとスタイルの配信元への接続の待ち | 使わない接続は無駄になる | `<link rel="preconnect">` で配信元に先に接続する | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/preconnect |
| 最初の表示範囲と主題データを小さくする | 最初に読むタイルとデータの量 | 範囲を決める根拠が要る | 最初の範囲は利用者の地域に合わせ、主題データは範囲内だけかベクトルタイルにする ([many-features](many-features.md)) | (推測) |
| 一覧を先に出す | 地図を待たずに中身を見せる | 一覧の設計が要る | 一覧を正本にして先に描き、地図は後から読む。地図が出ない間も一覧を止めない (geo-software-ops の fallback の考え方と同じ) | (推測) |

## 判断を左右すること

- 地図の役割: 主役なら地図の読み込みを最優先にし、脇役なら後回しにする。
- 最初の画面に地図が入っているか: 入っていなければ、画面に入るまで読まない。
- 利用者の回線と端末: 移動中のスマートフォンが主なら、最初の JS の大きさが効く (推測)。
- スタイルが読むもの: スプライト、グリフ、ソースの数。日本語の注記が多いスタイルはグリフが重い。

## 手順

1. 最初の画面で必要なものを書き出す (本文、一覧、地図、検索)。
2. 地図が最初の画面に要らないなら、地図のモジュールを動的 import に分ける。ビルドの出力で、最初に読む JS の大きさを確かめる。
3. 地図の要素に高さを与え、読み込み中の表示を出す。
4. 地図が主役でないなら、静的な画像で代えるかを比べる。
5. スタイルの読み込みを見る (開発者ツールのネットワーク)。グリフの取得が多ければ `localIdeographFontFamily` を確かめる。配信元に `preconnect` する。
6. Lighthouse か PageSpeed Insights で LCP と CLS を測る。結論が数値に左右されるなら geo-software-poc-measure で想定の端末と回線で測る。

## 落とし穴

- バンドラーで MapLibre GL JS 6 を分割すると、ワーカーの URL を渡さないと地図が出ない (`setWorkerUrl()`、[maplibre-gl-js](../../geo-software-library/references/libraries/maplibre-gl-js.md))。
- 地図の CSS (`maplibre-gl.css`) を読み忘れると、コントロールやポップアップの配置が崩れる。動的 import に分けたときは CSS も一緒に読む (推測)。
- `localIdeographFontFamily` を使うと、漢字とかなは端末のフォントになり、スタイルで指定したフォントは太さ以外効かない。見た目をそろえたいなら `false` にしてグリフを配信する (グリフの作り方は geo-software-infra の範囲)。
- 地図の canvas は LCP の候補の一覧に無いので、地図が主役のページでは LCP の値が地図の表示の速さを表さないことがある (推測)。
- 地図を表示しない間 (タブの裏) にライブラリを初期化すると、大きさが 0 の要素で地図ができ、開いたときに描き直しが要る。開いたときに作るか、`resize()` を呼ぶ (推測)。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- 静的な地図画像にも、地図データの帰属表示が要る。OSM の静止画は基本はインタラクティブ地図と同じ扱いになる (geo-software-legal-check の [attribution](../../geo-software-legal-check/references/attribution.md))。
- 提供元の Static API の画像を保存して配ってよいかは、提供元の規約で決まる (geo-software-legal-check の [api-terms](../../geo-software-legal-check/references/api-terms.md))。
- 端末のフォントで描く場合は、フォントを配らないのでフォントのライセンスの論点は無い。グリフを自分で配るなら、フォントのライセンス (SIL OFL など) を確かめる。

## 出典

- https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/map.ts (`localIdeographFontFamily` の説明と既定値。2026-11-11)
- https://web.dev/articles/lcp (LCP の候補の要素、良い値は 2.5 秒以下。2025-09-04 更新、2026-11-11 に確かめた)
- https://web.dev/articles/cls (良い値は 0.1 以下、後から出るものの場所の確保。2026-11-11)
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import 、https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API 、https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/preconnect (2026-11-11)
- geo-software-library の [maplibre-gl-js](../../geo-software-library/references/libraries/maplibre-gl-js.md) (本体とワーカーの大きさ、`setWorkerUrl()`)

## 未確認のこと

- `<canvas>` が LCP の候補から外れることの、仕様 (Largest Contentful Paint の仕様) での確かめ。web.dev の一覧に無いことだけを見た。
- `localIdeographFontFamily` で、iOS と Android の既定の日本語フォントの見た目と、読み込みの差。測っていない。
- 地図を動的 import に分けたときの、地図のタブを開いてから描き終わるまでの時間。旅の名所のアプリでは測っていない。
