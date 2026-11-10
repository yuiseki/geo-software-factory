# 配色と注記

対象: ベースマップと主題データの配色、色覚の多様性への配慮、日本語の注記とフォント、ズームごとの表示の出し分け、コロプレスの階級区分

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 確かめた版 | MapLibre Style Spec (main、2026-11-11)、MapLibre GL JS 6.17.0、ColorBrewer (axismaps/colorbrewer)、d3-scale-chromatic の文書、Axis Maps の Cartography Guide、CUDO のカラーユニバーサルデザイン推奨配色セットのページ、Chrome DevTools の Rendering の文書、WCAG 2.2 |

## 概要

地図の配色は、背景の地図 (ベースマップ) の上に主題データを載せるので、主題の色が背景の道路や緑地、水域と紛れないことと、色覚の多様性があっても分類が分かれて見えることの 2 つを満たす必要がある。注記は、背景の上で読めるコントラストと縁取り、日本語のフォント、重なりの出し分けで決まる。主題図 (コロプレス) は、数をそのまま塗ると面積の大きい区画が目立つので、率や密度に直し、階級区分の方法を選ぶ。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| 注記の縁取り (halo) | 背景の地図や航空写真の上で文字を読ませる | MapLibre の `text-halo-width` の上限はフォントの大きさの 1/4 | MapLibre の `text-halo-color`、`text-halo-width`、`text-halo-blur` | https://github.com/maplibre/maplibre-style-spec/blob/main/src/reference/v8.json |
| 注記の重なりの出し分け | 注記が重なって読めない | 出ない注記がある。優先度を決める | MapLibre の symbol レイヤは既定で重なる注記を出さない (`text-allow-overlap` の既定 false)。`symbol-sort-key` で優先度 | 同上 |
| 縦書き | 日本語の縦の注記 | 値は「ヒント」で、縦にできない文字は横になる | MapLibre の `text-writing-mode` (`horizontal`、`vertical`) | 同上 |
| 日本語のフォント | 漢字とかなのグリフ | 端末のフォントで描くと見た目が端末ごとに変わる | MapLibre の `localIdeographFontFamily` ([initial-load](initial-load.md)) | https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/map.ts |
| 面の注記の代表点を別に作る | MultiPolygon の各部分に同じ注記が出る (飛び地のある区) | 前処理が要る | 地物ごとに 1 つの代表点を作り、点のソースで注記する。代表点は最大の部分の、内側でいちばん縁から遠い点 (polylabel、ISC) を使う | 実測 (下の「実測」)、https://github.com/mapbox/polylabel |
| 色覚の多様性に配慮した配色 | 分類が色覚によって見分けられない | 色の数に限りがある (分類は多くて 7〜8 程度、推測) | ColorBrewer (Apache-2.0。順序、発散、分類の配色)。viridis (matplotlib 由来の知覚的に一様な配色)、cividis (色覚の多様性に最適化された配色)。d3-scale-chromatic で使える。国内では CUDO の「カラーユニバーサルデザイン推奨配色セット」(ガイドブック第 3 版の PDF が無料で配布されている。利用条件はページに書かれていない) | https://github.com/axismaps/colorbrewer 、https://d3js.org/d3-scale-chromatic/sequential 、https://cudo.jp/?page_id=1565 |
| 色だけに頼らない | 1.4.1 色の使用 | 記号の種類が増える | 形、模様、ラベル、凡例の並び。線は太さと破線 | https://www.w3.org/TR/WCAG22/ |
| 色覚の模擬 | 作った配色を確かめる | 模擬は近似 | Chrome DevTools の Rendering の Emulate vision deficiencies (Blurred vision、Reduced contrast、Protanopia、Deuteranopia、Tritanopia、Achromatopsia) | https://developer.chrome.com/docs/devtools/rendering/apply-effects |
| コロプレスの正規化 | 数をそのまま塗ると面積や人口の大きい区画が目立つ | 分母のデータ (面積、人口) が要る | Axis Maps の Cartography Guide は、コロプレスには数そのものを使わず、率や比に直すよう書く (例: 人数ではなく 1 平方マイルあたりの人数)。数を見せたいなら比例シンボル (円の大きさ) を使う | https://www.axismaps.com/guide/choropleth |
| 階級区分 | 値の分け方で印象が変わる | 方法ごとに偏りがある | 等間隔 (偏ったデータでは空の階級が出る)、分位 (同じ件数ずつ。近い値を分け、遠い値をまとめることがある)、自然分類 (Jenks。データごとに区切りが変わり、地図どうしを比べにくい)、手動 (意味のある閾値、連続する地図で区切りをそろえる)。階級の数は 3〜7 が無難 | https://www.axismaps.com/guide/data-classification |

## 判断を左右すること

- 背景の地図: 淡い背景 (主題を載せる用のスタイル) か、色の多い背景か、航空写真か。主題の色は背景の色と同時に確かめる。
- 主題データの種類: 順序のある量 (順序の配色)、中央の値から上下に分かれる量 (発散の配色)、順序の無い分類 (分類の配色)。
- 分類の数: 色で分けられる数を超えるなら、分類をまとめるか、形やラベルを足す。
- 比べる相手: 年ごとや地域ごとに複数の地図を並べるなら、区切りを固定する (手動か、全期間で決めた区切り)。
- 日本語の注記の量: 地名が多いスタイルは、グリフの量と重なりの出し分けが効く。

## 手順

1. 背景の地図を決める。主題を載せる地図なら、背景の色を淡くし、注記を減らしたスタイルを選ぶ (提供元は map-compare-infra)。
2. 主題データの種類から配色の種類を選び、ColorBrewer、viridis、cividis などから選ぶ。分類の色は、色だけでなく形かラベルでも分ける。
3. 主題図なら、数を率か密度に直すか、比例シンボルにするかを決める。直すなら分母の出どころを書く。
4. 階級区分の方法と数を決め、ヒストグラムで分布を見てから区切る。方法と区切りを凡例に書く。
5. 注記の縁取りを入れ、文字と背景のコントラストを 4.5:1 以上、マーカーや境界線と背景は 3:1 以上にする (WCAG 2.2 の 1.4.3、1.4.11)。
6. 面の注記が飛び地ごとに重複しないか確かめ、重複するなら代表点のソースに分ける。
7. 色覚の模擬 (Protanopia、Deuteranopia、Tritanopia、Achromatopsia) で、分類が分かれて見えるかを画面で確かめる。

## 実測

- 飛び地のある区 (MultiPolygon) の面に symbol レイヤで注記すると、各部分に同じ区名が出た (2026-11-11 実測)。地物ごとに 1 つの代表点を作って注記すると直る (代表点の作り方は推測。polylabel は 1 つの Polygon の内側の点を返すので、MultiPolygon では最大の部分に使う)。
- 東京 23 区のセブン-イレブンの図は、区ごとの店舗数をそのまま塗った ([seven-eleven-tokyo23](../../../../examples/seven-eleven-tokyo23/README.md))。Axis Maps の手引きに従えば、面積あたりか人口あたりの店舗数にするか、比例シンボルにする場面である (推測)。

## 落とし穴

- 赤と緑だけで分類を分けると、P 型と D 型の色覚では見分けにくい (Chrome DevTools の模擬の説明でも、Protanopia と Deuteranopia は緑、赤、黄の混同とされる)。
- 虹色の配色 (jet など) は、順序のある量に使うと境目でない所に境目が見える (推測。viridis が作られた理由として知られるが、ここでは原典を確かめていない)。
- `text-halo-width` をフォントの大きさの 1/4 より大きくしても効かない (スタイル仕様の記述)。
- 分位の階級区分は見た目が整うが、近い値の区画を別の色に分けることがある。
- 背景の地図の色 (公園の緑、水域の青) と主題の色がかぶると、主題が背景に見える。
- CUDO の推奨配色セットは、利用条件がページに書かれていない。製品に使う前にガイドブックか CUDO に確かめる。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- ColorBrewer の配色とソフトウェアは Apache-2.0 (Copyright 2002 Cynthia Brewer, Mark Harrower, and The Pennsylvania State University)。配色をコードに組み込んで配るときは、ライセンス文と著作権表示を残す (https://github.com/axismaps/colorbrewer の LICENCE.txt、2026-11-11)。
- d3-scale-chromatic は ISC 形式のライセンス (Copyright 2010-2026 Mike Bostock) で、同じ LICENSE に ColorBrewer の Apache-2.0 の表記を含む (https://github.com/d3/d3-scale-chromatic 、2026-11-11)。
- polylabel は ISC。
- CUDO の推奨配色セットの利用条件は未確認。
- 背景の地図のスタイルを変えて配るときは、スタイルとデータのライセンス (OSM の ODbL、スタイルの著作権) を確かめる (map-compare-infra、map-legal-check)。

## 出典

- https://github.com/maplibre/maplibre-style-spec/blob/main/src/reference/v8.json (`text-halo-width` の上限、`text-writing-mode`、`symbol-placement`。2026-11-11)
- https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/map.ts (`localIdeographFontFamily`。2026-11-11)
- https://github.com/axismaps/colorbrewer (Apache-2.0。2026-11-11)
- https://d3js.org/d3-scale-chromatic/sequential (viridis と cividis の説明。2026-11-11)
- https://cudo.jp/?page_id=1565 (推奨配色セットとガイドブック第 3 版。2026-11-11)
- https://developer.chrome.com/docs/devtools/rendering/apply-effects (色覚の模擬の種類。2026-11-11)
- https://www.axismaps.com/guide/choropleth と https://www.axismaps.com/guide/data-classification (正規化と階級区分。2026-11-11)
- https://github.com/mapbox/polylabel (ISC、内側の点の求め方。2026-11-11)
- https://www.w3.org/TR/WCAG22/ (1.4.1、1.4.3、1.4.11。2026-11-11)

## 未確認のこと

- CUDO の推奨配色セットの利用条件 (商用の製品に使ってよいか、表示が要るか)。
- MapLibre で MultiPolygon の面に symbol を置いたときに、部分ごとに注記を出す振る舞いのソースの該当箇所。実測だけで、ソースは読んでいない。
- 国内の地図の配色の公的な基準 (国土地理院の地図記号や、ハザードマップの色の決まり)。ハザードマップの浸水深の配色には国の手引きがあるが、ここでは確かめていない。
