# Mapbox からの移行

対象: Mapbox GL JS v2 以降、Mapbox Maps SDK、Mapbox のスタイルとタイルからの移行 (MapLibre への移行を含む)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 根拠の版 | Mapbox Product Terms (2026-10-20 版、PDF)、MapLibre GL JS の CHANGELOG (main、2.0.0 の項)、MapLibre の Mapbox からの移行ガイド、MapLibre Style Spec と Mapbox Style Spec のルートとレイヤーの一覧 |

## 移行元の特徴

Mapbox GL JS は v1.13 以前が BSD-3-Clause、v2.0.0 (2020-12-08) 以降は Mapbox のアカウントと規約に結びついた独自ライセンスである ([mapbox-gl-js](../../geo-software-library/references/libraries/mapbox-gl-js.md))。MapLibre GL JS は v1.13 以前のコードから分岐したので、v1 の書き方はほぼそのまま移る。v2 以降、とくに v3 の Mapbox Standard スタイルと 3D の機能は MapLibre に無いものが多い。

縛りは 3 つある。スタイル: Studio で作った、または Studio から書き出したスタイルは、Studio 内か Mapbox Map (Mapbox の地図コンテンツを含む地図) でしか使えない (Product Terms 2.11)。データ: 地図コンテンツの書き出し、ダウンロード、キャッシュ、保存は原則禁止で、例外は同じ端末で 30 日までのキャッシュ (1.9、2.8.1)。モバイル: Mobile SDK をモバイルアプリでの唯一のアクセス手段とする (2.9.1)。課金とその他の条件は [mapbox](../../geo-software-infra/references/providers/mapbox.md) にある。

## 移行先の候補と API の対応

ここでは Web の MapLibre GL JS への移行を中心に書く。モバイルの Mapbox Maps SDK から MapLibre Native への移行の手順は確かめていない (未確認)。

| 移行元の機能・API | 移行先 (ライブラリ・サービス) | 違いと注意 | 出典 |
|---|---|---|---|
| npm の `mapbox-gl` | `maplibre-gl` | パッケージを入れ替え、名前空間 `mapboxgl` を `maplibregl` に、CSS のクラス接頭辞 `mapboxgl-` を `maplibregl-` に、CSS を `maplibre-gl/dist/maplibre-gl.css` に変える。MapLibre GL JS v6 は ESM のみで default export が無いので、`import * as maplibregl from "maplibre-gl"` か名前付きの import にし、バンドラーでは `setWorkerUrl()` を呼ぶ | https://maplibre.org/maplibre-gl-js/docs/guides/mapbox-migration-guide/, [maplibre-gl-js](../../geo-software-library/references/libraries/maplibre-gl-js.md) |
| CDN (`api.mapbox.com` の script と CSS) | unpkg などの `maplibre-gl@版/dist/maplibre-gl.mjs` | `@latest` で読むと v6 以降で白紙になると移行ガイドが警告しているので、版を固定する | https://maplibre.org/maplibre-gl-js/docs/guides/mapbox-migration-guide/ |
| `mapboxgl.accessToken`、`accessToken` オプション | 削除 | MapLibre GL JS 2.0.0 で `accessToken` の関連コード、`baseApiUrl`、テレメトリが外された。タイル提供者が鍵を求めるなら、URL のクエリか `transformRequest` で付ける | MapLibre CHANGELOG 2.0.0 (https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md) |
| `mapbox://` で始まるスタイル、ソース、スプライト、グリフの URL | 移行先の https の URL | MapLibre 2.0.0 で `mapbox://` の解決が外された。スタイル文書の中の `sources`、`sprite`、`glyphs` も全部書き換える。Mapbox のタイルを残すなら https の API の URL を直接書くことになるが、地図ロードでなくタイルのリクエスト数で課金される (Product Terms 2.8.3) | MapLibre CHANGELOG 2.0.0, [mapbox](../../geo-software-infra/references/providers/mapbox.md) |
| TypeScript の型 (`MapboxOptions`、`AnyLayer`、`AnySourceData`、`MapboxGeoJSONFeature` など) | `MapOptions`、`LayerSpecification`、`SourceSpecification`、`GeoJSONFeature` など | MapLibre 2.0.0 で名前が変わった。型の置き換えは機械的にできる | MapLibre CHANGELOG 2.0.0 |
| スタイルのルートの `imports`、`schema` (Mapbox Standard の設定)、`lights`、`models`、`camera`、`fog`、`color-theme`、`featuresets`、`iconsets`、`rain`、`snow`、`fragment` | 対応するものが無い。`light` (単数)、`sky` (霧の色を含む)、`terrain`、`projection`、`state` はある | Mapbox Standard を使っているなら、スタイルは丸ごと作り直す。`fog` は MapLibre の `sky` の `fog-color` などで近い表現にする (推測。見た目の一致は確かめていない) | https://docs.mapbox.com/style-spec/reference/root/, https://maplibre.org/maplibre-style-spec/root/ |
| レイヤーの型 `model`、`building`、`clip`、`raster-particle`、`slot`、`placement-group`、`sky`、レイヤーの `slot` 属性 | MapLibre のレイヤーの型は `background`、`fill`、`line`、`symbol`、`raster`、`circle`、`fill-extrusion`、`heatmap`、`hillshade`、`color-relief` | 3D モデルはカスタムレイヤー (three.js など) で置く。`slot` による差し込み位置は、`addLayer` の `beforeId` で指定する | https://docs.mapbox.com/style-spec/reference/layers/, https://maplibre.org/maplibre-style-spec/root/, [maplibre-gl-js](../../geo-software-library/references/libraries/maplibre-gl-js.md) |
| 投影法 (Albers、Equal Earth など Mapbox の `projection`) | MapLibre は `mercator`、`vertical-perspective`、`globe` プリセット。6.15 から実験的に `addProjection` | Mapbox の投影法の多くは移らない | https://maplibre.org/maplibre-style-spec/types/ |
| mapbox-gl-geocoder、Mapbox Search JS | maplibre-gl-geocoder にジオコーダを渡す | Mapbox の POI の検索結果は Mapbox Map と組み合わせてしか使えない (2.7.5)。ジオコーダは geo-software-arch の [search](../../geo-software-arch/references/capabilities/search.md) で選ぶ | https://github.com/maplibre/maplibre-gl-geocoder |
| mapbox-gl-draw | Terra Draw (MapLibre のプラグイン一覧に載る) | mapbox-gl-draw を MapLibre でそのまま動かせるかは確かめていない (未確認) | https://maplibre.org/maplibre-gl-js/docs/plugins/ |
| Directions、Navigation | geo-software-arch の [routing](../../geo-software-arch/references/capabilities/routing.md) で選ぶ | Navigation API の結果は書き出し、キャッシュ、保存が禁止 (2.10) なので、保存した経路は移行後に使えない | Product Terms 2.10 |
| react-map-gl の `react-map-gl/mapbox` | `react-map-gl/maplibre` | `mapboxAccessToken` が不要になり、スタイルは完全な URL で渡す。v1 系の mapbox-gl なら `react-map-gl/mapbox-legacy` から移る | https://visgl.github.io/react-map-gl/docs/get-started |

## 規約上の注意

- 移行元のデータ (キャッシュ、ジオコーディングの結果、プレイス ID) を移行後も使えるか: Studio のスタイルは Mapbox 以外の地図に使えない (2.11)。Mapbox の地図コンテンツ (タイル) を書き出して自前で配ることもできない (1.9)。Temporary Geocoding の結果は保存もキャッシュもできない (2.7.2)。Permanent Geocoding の結果は永続的に保存できるが、使い道は自社の内部の業務か、アプリの付随的な機能に限られ、利用者アカウントごとに別の API 要求が要るなどの条件がある (2.7.3)。どの Geocoding の結果も、汎用の POI や住所のデータベース、汎用の地図、別のジオコーダの開発やテストに使ってはならない (2.7.1)。
- スタイルの扱い: Studio で作ったスタイル JSON を、Mapbox 以外のタイルに向けて書き換えて使う案は 2.11 に反すると読める (推測)。配色を参考に、別のスタイル (OpenMapTiles 系や移行先の提供元のスタイル) から作り直す。Mapbox の公開スタイル (Streets、Standard など) も同じ扱いになると読める (推測)。
- 移行中に移行元と移行先を併用してよいか: Web では、MapLibre GL JS から Mapbox のタイルを直接取ることは規約上禁じられておらず、課金がタイルのリクエスト数に変わる (2.8.3、3.57、[mapbox](../../geo-software-infra/references/providers/mapbox.md))。この形なら Studio のスタイルも Mapbox Map の上で使うことになる (推測)。モバイルアプリでは Mobile SDK が唯一のアクセス手段なので (2.9.1)、MapLibre Native に替えた時点で Mapbox のタイルは使えない。他社の地図を同じ画面に並べることを直接禁じる条項は Product Terms に見当たらない ([mapbox](../../geo-software-infra/references/providers/mapbox.md))。

## 費用の変化

- Web の GL JS は地図ロード (`new Map()` ごと、12 時間で区切り) で課金され、タイルは含まれる。MapLibre から Mapbox のタイルを取ると、ベクトルタイルのリクエスト数で課金される。1 地図ロードあたりのタイル枚数で損得が変わるので、移行の途中で Mapbox のタイルを残すなら実測する ([mapbox](../../geo-software-infra/references/providers/mapbox.md) の概算、[criteria](../../geo-software-infra/references/criteria.md) の「費用の見積もり方」)。
- モバイルは MAU 課金で、移行先が MapLibre Native なら Mapbox の費用は消え、移行先のタイルの費用に置き換わる。

## 移行の手順

1. 使っている版を確かめる (`package.json` の `mapbox-gl`)。v1 系なら移行ガイドの手順だけでほぼ移る。v2 以降なら、スタイルとコードから Mapbox だけの機能を洗い出す (`grep -rn "mapbox://\|accessToken\|setConfigProperty\|slot\|imports"` と、スタイル JSON のルートとレイヤーの型)。
2. スタイルを決める。Studio のスタイルは移行先で使わない前提で、移行先の提供元のスタイルを選ぶか作る。タイルの供給元は geo-software-infra で選ぶ。
3. パッケージ、import、CSS、型の名前を置き換える。トークンと `mapbox://` を消す。
4. Mapbox だけの機能 (Standard の設定、3D モデル、`fog`、投影法) を、代わりの表現にするか、やめるかを機能ごとに決める。
5. プラグイン (geocoder、draw、directions) を置き換える。
6. 画面ごとに比べ、[migration-plan](migration-plan.md) の手順で切り替える。最後に Mapbox のトークンを無効にする。

## 既にある移行の道具

- MapLibre の公式の移行ガイド (https://maplibre.org/maplibre-gl-js/docs/guides/mapbox-migration-guide/)。ガイド自身が、mapbox-gl の版によっては正確でないこと、v2 以降は両者が別の機能に分かれたことを断っている。MapLibre GL JS v1 系は Mapbox GL JS v1 と完全に後方互換で、npm の `v1` タグ (1.15.3) にある。
- react-map-gl は Mapbox と MapLibre の両方を入口を分けて持つ (https://visgl.github.io/react-map-gl/docs/get-started)。
- Mapbox Standard のスタイルを MapLibre Style に変換する道具は見つからなかった (未確認)。

## 落とし穴

- スタイル JSON の中の `mapbox://` を置き換え忘れると、スタイルの読み込みで失敗する。エラーが出ずに一部のレイヤーだけ描かれないこともある (推測)。読み込みの `error` イベントを記録する。
- MapLibre v6 は WebGL2 必須で ES2022 を対象にしている。Mapbox GL JS v1 から移るときに古い端末を切り捨てることになりうる ([maplibre-gl-js](../../geo-software-library/references/libraries/maplibre-gl-js.md))。
- 帰属表示が変わる。Mapbox のロゴと「Improve this map」を外し、移行先の帰属表示を出す。Mapbox のタイルを残す間は Mapbox の帰属表示 (1.4) を残す ([attribution](../../geo-software-legal-check/references/attribution.md))。
- MapLibre の README は、旧 BSD-3 の範囲外の mapbox-gl-js のコード (v2 以降) を持ち込むことを禁じている。v2 以降のコードを写して足りない機能を補わない ([maplibre-gl-js](../../geo-software-library/references/libraries/maplibre-gl-js.md))。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- Mapbox GL JS v2 以降は OSS ではなく、アカウントが失効するとライセンスも終わる。MapLibre GL JS は BSD 3-Clause で、再配布の際に著作権表示と許諾条件の表示が要る ([mapbox-gl-js](../../geo-software-library/references/libraries/mapbox-gl-js.md)、[maplibre-gl-js](../../geo-software-library/references/libraries/maplibre-gl-js.md))。
- 移行先のタイルが OpenStreetMap 由来なら ODbL の帰属表示が要る ([odbl](../../geo-software-legal-check/references/odbl.md))。

## 出典

- https://maplibre.org/maplibre-gl-js/docs/guides/mapbox-migration-guide/ (2026-11-11 確認。パッケージ、名前空間、CSS のクラス、CDN の置き換え、v1 の互換)
- https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md (2026-11-11 確認。2.0.0 で `accessToken`、`mapbox://`、`baseApiUrl`、テレメトリの削除と型の名前の変更)
- https://www.mapbox.com/legal/product-terms と、そこから辿る Mapbox Product Terms (October 20, 2026) の PDF (2026-11-11 確認。1.9、2.7.1、2.7.2、2.7.3、2.7.5、2.8.1、2.9.1、2.10、2.11、3.36)
- https://docs.mapbox.com/style-spec/reference/root/、https://docs.mapbox.com/style-spec/reference/layers/ (2026-11-11 確認。ルートの属性とレイヤーの型)
- https://maplibre.org/maplibre-style-spec/root/ (2026-11-11 確認。ルートの属性とレイヤーの型)
- https://visgl.github.io/react-map-gl/docs/get-started (2026-11-11 確認)

## 未確認のこと

- Mapbox Maps SDK (Android、iOS) から MapLibre Native への移行の手順と API の対応。
- mapbox-gl-draw が MapLibre GL JS v6 でそのまま動くか。
- Mapbox Standard のスタイルを MapLibre Style に変換する道具の有無。
- Mapbox の公開スタイル (Streets など) が 2.11 の「Studio で作ったスタイル」に含まれるかの条文上の扱い。
