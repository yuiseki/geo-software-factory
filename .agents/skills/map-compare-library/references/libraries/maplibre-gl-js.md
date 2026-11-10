# MapLibre GL JS

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 6.17.0 (2026-11-08 JST)。npm の `latest` タグも 6.17.0 (https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.17.0, https://www.npmjs.com/package/maplibre-gl) |
| リポジトリ | https://github.com/maplibre/maplibre-gl-js |
| ドキュメント | https://maplibre.org/maplibre-gl-js/docs/ (スタイル仕様は https://maplibre.org/maplibre-style-spec/) |
| ライセンス (LICENSE ファイルで確かめる) | BSD 3-Clause (MapLibre contributors, 2023)。同じ LICENSE に、mapbox-gl-js v1.13 以前由来のコード (BSD-3-Clause, Mapbox) と glfx.js 由来のコード (MIT 形式) の表記を含む (https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt)。npm の license 欄は BSD-3-Clause |
| 運営主体・ガバナンス | MapLibre Organization。憲章 (Charter) で、Technical Steering Committee (誰でも参加できる月例の技術会議)、Governing Board (5 名、方向性と財務を担う)、Voting Members (Board を選ぶ) の 3 機関を定める (https://github.com/maplibre/maplibre/blob/main/CHARTER.md)。財務は公開されており、四半期報告がある (https://maplibre.org/about/) |

## 概要

MapLibre GL JS は、WebGL でベクトルタイルから対話的な地図をブラウザに描く TypeScript のライブラリである (https://maplibre.org/maplibre-gl-js/docs/)。地図の見た目は MapLibre Style Spec に沿ったスタイル文書で決める (同ページ)。mapbox-gl-js v1.13 以前のコードを引き継いだフォークで (https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt)、Android や iOS 向けの MapLibre Native と同じエコシステムに属する (https://maplibre.org/maplibre-gl-js/docs/)。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): WebGL。v6.0.0 で WebGL 1 の対応を外し、WebGL2 が必須になった (https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0)。マーカーとポップアップは DOM 要素。WebGPU は公式ドキュメントのトップに記述がない (https://maplibre.org/maplibre-gl-js/docs/)。
- 2D / 2.5D (傾き・回転) / 3D: 傾き、回転に対応する。v5.0.0 で 90 度を超える pitch とカメラの roll が加わった (https://github.com/maplibre/maplibre-gl-js/releases/tag/v5.0.0)。建物の押し出し (fill-extrusion)、3D 地形を描ける (https://maplibre.org/maplibre-gl-js/docs/examples/display-buildings-in-3d/, https://maplibre.org/maplibre-gl-js/docs/examples/3d-terrain/)。任意の 3D モデルはカスタムレイヤーで three.js や Babylon.js と組み合わせる (https://maplibre.org/maplibre-gl-js/docs/examples/add-a-3d-model-with-babylonjs/)。
- 地球儀表示: 対応。v5.0.0 (2024-12-31) で globe、大気表現、GlobeControl、地球儀上の地形が入った (https://github.com/maplibre/maplibre-gl-js/releases/tag/v5.0.0, https://maplibre.org/maplibre-gl-js/docs/examples/display-a-globe-with-a-vector-map/)。
- 対応する投影法: スタイル仕様に定義された投影は `mercator` (既定) と `vertical-perspective` の 2 つで、`globe` はズーム 10 から 12 の間で `vertical-perspective` から `mercator` に切り替えるプリセットである (https://maplibre.org/maplibre-style-spec/types/)。6.15 から実験的に `addProjection` / `removeProjection`、`identity` 投影、タイル URL の `{bbox}` トークンが加わり、独自のタイル格子を持つ平面 CRS (例: `EPSG:2193`) の地図を扱える (https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md の 6.15.0, https://maplibre.org/maplibre-style-spec/types/)。

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | `raster` ソース。6.0.0 で `RasterTileSource#setPremultiplyAlpha(false)` が加わった (https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0)。COG はプロトコル拡張の例がある (https://maplibre.org/maplibre-gl-js/docs/examples/add-a-cog-raster-source/) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT と MLT は標準、PMTiles はプラグイン | MVT は `vector` ソースの基本形式。MLT (MapLibre Tiles) は 5.12.0 (2025-11-09) から vector ソースの `encoding: 'mlt'` で読める (https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md の 5.12.0, https://maplibre.org/maplibre-gl-js/docs/examples/display-a-map-with-mlt/)。6.16.0 で MLT 用の Accept ヘッダーが加わった (同 CHANGELOG)。PMTiles は `pmtiles` パッケージのプロトコル (`addProtocol`) で読む (https://maplibre.org/maplibre-gl-js/docs/examples/pmtiles-source-and-protocol/, https://maplibre.org/maplibre-gl-js/docs/plugins/) |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 対応 (MapLibre Style Spec) | 6.0.0 で style-spec v25 に上がり、旧式の式に出会うと警告扱いのエラーを投げるようになった (https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0)。Mapbox GL JS v2 以降のスタイル独自機能との互換は未確認。Mapbox からの移行ガイドがある (https://github.com/maplibre/maplibre-gl-js/tree/main/docs/guides) |
| GeoJSON | 対応 | `geojson` ソース。ワーカーでタイル化し、点のクラスタリングを持つ (https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/)。6.0.0 で properties の入れ子オブジェクトを保持するようになり、`setData` の第 2 引数が消えた (https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0) |
| 3D Tiles / glTF | 標準では非対応。カスタムレイヤーで対応 | three.js を使って 3D Tiles を表示する例と、Babylon.js で 3D モデルを置く例がある (https://maplibre.org/maplibre-gl-js/docs/examples/add-3d-tiles-3d-objects-and-models-using-threejs/, https://maplibre.org/maplibre-gl-js/docs/examples/add-a-3d-model-with-babylonjs/)。プラグイン一覧の maplibre-three-plugin も同じ方式 (https://maplibre.org/maplibre-gl-js/docs/plugins/) |
| 地形 (標高タイル) | 対応 | `raster-dem` ソースで 3D 地形、陰影 (hillshade、多方向 hillshade)、`color-relief` を描く (https://maplibre.org/maplibre-gl-js/docs/examples/3d-terrain/, https://maplibre.org/maplibre-gl-js/docs/examples/add-a-multidirectional-hillshade-layer/, https://maplibre.org/maplibre-gl-js/docs/examples/add-a-color-relief-layer/)。quantized-mesh の地形を読む例もある (https://maplibre.org/maplibre-gl-js/docs/examples/add-3d-terrain-from-quantized-mesh-tiles/) |
| WMS / WMTS | WMS は対応、WMTS は一部 | WMS は raster ソースの URL に `{bbox-epsg-3857}` を入れて読む (https://maplibre.org/maplibre-gl-js/docs/examples/add-a-wms-source/)。WMTS 専用のソース型はない。Web メルカトルのタイル行列を持つ WMTS なら XYZ 形式の URL で raster ソースとして読める (推測)。Capabilities 文書を読む機能は確かめた範囲で見当たらない |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリ側の制限はなく、タイルとスタイルの提供者の規約に従う。OpenStreetMap 財団の標準ラスタタイルは、帰属表示、識別できる User-Agent と Referer、表示外タイルの一括取得の禁止、過度な利用の禁止を定め、SLA はない (https://operations.osmfoundation.org/policies/tiles/)。Mapbox のタイルやスタイルを MapLibre GL JS で使えるかは Mapbox の規約次第で、未確認。
- API キー・アカウントの要否: ライブラリ自体には不要。タイル提供者によっては必要になる。

## ライセンスと費用

- ライセンス: BSD 3-Clause。mapbox-gl-js v1.13 以前由来の部分も BSD-3-Clause で、glfx.js 由来の部分は MIT 形式である (https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt)。
- 利用料 (無料 / 従量 / 有料の機能): ライブラリは無料。ライブラリ側で地図ロード数を数える仕組みは CHANGELOG と LICENSE に記述がない。費用はタイル配信側で決まる。
- 版によるライセンスの変化: なし (MapLibre GL JS の範囲では BSD-3-Clause のまま)。README によれば、mapbox-gl-js が 2020-12 に OSS でないライセンスへ切り替える前にフォークしたのが始まりで、旧 BSD-3 の範囲外にある mapbox-gl-js のコードを持ち込むことを禁じている (https://github.com/maplibre/maplibre-gl-js/blob/main/README.md)。

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 6.17.0 で 296.7 kB (bundlephobia、https://bundlephobia.com/package/maplibre-gl@6.17.0)。v6 は本体 `maplibre-gl.mjs` とワーカー `maplibre-gl-worker.mjs` の 2 ファイル構成で (https://github.com/maplibre/maplibre-gl-js/blob/main/docs/guides/v5-to-v6-migration-guide.md)、bundlephobia の値にワーカーが含まれるかは未確認。
- バンドラー (Vite など) で使うとき: ワーカーの URL を `setWorkerUrl()` で渡す。渡さないと、Vite 8.3.7 の開発サーバーで `.vite/deps/maplibre-gl-worker.mjs` が 504 になり「Worker failed to load」で地図が描かれなかった (2026-11-11 実測)。6.17.0 の `maplibre-gl-worker.mjs` は他のファイルを読み込まない単体のファイルなので、Vite では `import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?url"` でも `?worker&url` でも本番のビルドで動いた (2026-11-10、11-11 実測)。以前の 6 系の版で `?url` だと隣の `maplibre-gl-shared.mjs` を伴わずに壊れたという記録があるが、どの版かは確かめていない。v6 には default export が無いので、`Map` などは名前で import する。クリックした地物の `properties` は、v5 の JSON 文字列ではなく値のまま返る。初回に読むのは本体とワーカーの 2 つで、6.17.0 で本体は gzip -9 で 294,764 B、ワーカーは 147,035 B だった (2026-11-11 実測)。bundlephobia の 296.7 kB は本体だけと考えられる (推測)
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 公式に件数や MB の閾値はない。大きなデータの手引きは、不要な属性の削除、座標精度を小数 6 桁程度に落とす、形状の簡略化、2〜3 分割、点ソースの maxzoom を 12 程度に下げる、クラスタリング、ベクトルタイル化 (大規模ならサーバー側で Martin などを使う) を勧める (https://maplibre.org/maplibre-gl-js/docs/guides/large-data/)。
- 低性能端末・モバイルブラウザでの注意: v6 は WebGL2 必須で、WebGL が使えない環境ではマップの `error` イベントで検知する (https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0)。v6 は ES2022 を対象にビルドされ、2022 年より前のブラウザやツールでは変換が要る場合がある (同ノート)。6.17.0 で iOS 15 の ANGLE シェーダーコンパイラ不具合により記号と文字が描かれない問題が直った (https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md の 6.17.0)。

## エコシステム

- 主なプラグイン・拡張: 公式のプラグイン一覧に、PMTiles、deck.gl、maplibre-three-plugin、Terra Draw、maplibre-gl-geocoder、maplibre-cog-protocol、maplibre-contour などが載る (https://maplibre.org/maplibre-gl-js/docs/plugins/)。
- React / Vue などのラッパー: React は react-map-gl (MIT、8.1.3、`@vis.gl/react-maplibre` として MapLibre 向けパッケージがある、https://github.com/visgl/react-map-gl, https://www.npmjs.com/package/@vis.gl/react-maplibre) ほか。Vue は @indoorequal/vue-maplibre-gl (MIT)、Svelte は svelte-maplibre (MIT)、Angular は ngx-maplibre-gl (https://maplibre.org/maplibre-gl-js/docs/plugins/, https://github.com/indoorequal/vue-maplibre-gl, https://github.com/dimfeld/svelte-maplibre)。各ラッパーの v6 対応は未確認。
- SSR のフレームワーク (Next.js、Astro など) で使うとき: 地図はブラウザでだけ作る。2026-11-11 に Node.js 23.9.0 で maplibre-gl 6.17.0 を試すと、`import` は通り、`new Map()` は `ReferenceError: document is not defined` で失敗した (実測)。そのため地図を作る処理はサーバーで動かない場所 (React なら `useEffect` の中) に置く。Next.js の App Router では、`'use client'` を付けた Client Component も初回はサーバーで HTML に事前レンダリングされる (https://nextjs.org/docs/app/getting-started/server-and-client-components)。サーバーで描かせたくなければ、Client Component の中で `next/dynamic` に `{ ssr: false }` を付けて読み込む。`ssr: false` は Server Component では使えずエラーになる (https://nextjs.org/docs/app/guides/lazy-loading)。Astro では、地図のコンポーネントに `client:only="react"` のように使うフレームワークを添えて付けると、サーバーでの HTML のレンダリングを飛ばす (https://docs.astro.build/en/reference/directives-reference/)。2026-11-11 の観察では、ラズリマップが Next.js、Proton の Flock の地図が Astro と React、全国Q地図が Astro で作られていた。
- TypeScript の型: 本体が TypeScript で書かれ、型を同梱する (https://maplibre.org/maplibre-gl-js/docs/, https://www.npmjs.com/package/maplibre-gl)。
- ネイティブ版・兄弟プロジェクト: MapLibre Native (Android、iOS ほか) が同じ組織にあり、スタイル仕様を共有する (https://maplibre.org/maplibre-gl-js/docs/)。6.0.0 のアイコン拡大の変更は gl-js と native の両方に入れると明記されている (https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0)。
- 日本語の情報 (公式翻訳、国内コミュニティ): 公式ドキュメントの日本語訳は確かめられなかった。国内コミュニティとして MapLibre User Group Japan (MUG-JP) が 2023-01 に発足し、MapLibre 公式ニュースでも紹介された (https://www.maplibre.org/news/2023-01-23-maplibre-user-group-japan/)。年次の活動まとめを dev.to や Zenn に公開している (https://dev.to/mug-jp, https://zenn.dev/mugjp/articles/try-118-maplibre-2025)。

## 開発の活発さ

- 直近 1 年のリリース数: 安定版 37 件 (5.13.0 から 5.24.0 まで、6.0.0 から 6.17.0 まで)、プレリリース 23 件 (6.0.0 のプレリリース)。対象期間は 2025-11-10 から 2026-11-10 (https://github.com/maplibre/maplibre-gl-js/releases)
- 最終コミット日: 2026-11-10 (JST、main ブランチ、https://github.com/maplibre/maplibre-gl-js/commits/main)
- 近年の大きな破壊的変更: v5.0.0 (2024-12-31) は WebGL のコンテキスト指定を `canvasContextAttributes` に移す、`on` の戻り値を `Subscription` に変える、非圧縮の本番ビルドを外すなど (https://github.com/maplibre/maplibre-gl-js/releases/tag/v5.0.0)。v6.0.0 (2026-07-23 JST) は、ESM のみの配布 (UMD、CSP 版、CommonJS の廃止)、WebGL2 必須、ES2022 対象、`styleimagemissing` の通知専用化、`map.transform` の削除、GeoJSON の入れ子 properties の保持、`zoomLevelsToOverscale` の既定値変更など (https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0)。v6 では `<script src>` を `<script type="module">` に変え、バンドラー利用時は `setWorkerUrl()` の呼び出しが要る。`@latest` で読み込むページは v6 以降で白紙になると移行ガイドが警告している (https://github.com/maplibre/maplibre-gl-js/blob/main/docs/guides/v5-to-v6-migration-guide.md)。

- Mapbox のタイルを MapLibre GL JS で使う場合: Mapbox Product Terms (2026-10-20 版) 2.8.3 は、純正の描画ライブラリ (Qualified Renderer) を使わない場合は、地図ロードではなく API の要求の回数で課金すると定めている。Web で他のライブラリから使うことを禁じる条文は見当たらない (条文に禁止の文が無いことからの推測を含む)。モバイルアプリでは 2.9.1 により Mobile SDK が唯一の利用手段で、MapLibre Native からは使えない (map-compare-infra の providers/mapbox.md、2026-11-11 確認)

## 向いている場面

- ベクトルタイル (MVT、PMTiles、MLT) をスタイル文書で描くベース地図。
- 傾き、回転、3D 建物、3D 地形、地球儀を使う地図。
- 自前配信のタイルや複数の提供元を差し替えながら使い、ライブラリ側の利用料を避けたいとき。
- MapLibre Native と同じスタイルを Web とモバイルアプリで共有したいとき。

## 向いていない場面

- WebGL2 が使えない環境を相手にする場合 (v6 以降)。
- バンドルを数十 kB に抑えたい、ラスタタイルとマーカーだけの軽い地図。
- Web メルカトル以外の多様な投影法や、WMTS の Capabilities 読み込みを前提とする GIS 業務 (独自 CRS は 6.15 で実験的に入った段階)。
- 3D Tiles を標準機能として扱いたい場合 (three.js などとの組み合わせが要る)。
- マイナー版が月に数回出る速さに追随できない保守体制の案件。

## 出典

- https://maplibre.org/maplibre-gl-js/docs/
- https://maplibre.org/maplibre-gl-js/docs/plugins/
- https://maplibre.org/maplibre-gl-js/docs/guides/large-data/
- https://maplibre.org/maplibre-gl-js/docs/examples/display-buildings-in-3d/
- https://maplibre.org/maplibre-gl-js/docs/examples/3d-terrain/
- https://maplibre.org/maplibre-gl-js/docs/examples/add-a-3d-model-with-babylonjs/
- https://maplibre.org/maplibre-gl-js/docs/examples/add-3d-tiles-3d-objects-and-models-using-threejs/
- https://maplibre.org/maplibre-gl-js/docs/examples/display-a-globe-with-a-vector-map/
- https://maplibre.org/maplibre-gl-js/docs/examples/add-a-cog-raster-source/
- https://maplibre.org/maplibre-gl-js/docs/examples/display-a-map-with-mlt/
- https://maplibre.org/maplibre-gl-js/docs/examples/pmtiles-source-and-protocol/
- https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/
- https://maplibre.org/maplibre-gl-js/docs/examples/add-a-multidirectional-hillshade-layer/
- https://maplibre.org/maplibre-gl-js/docs/examples/add-a-color-relief-layer/
- https://maplibre.org/maplibre-gl-js/docs/examples/add-3d-terrain-from-quantized-mesh-tiles/
- https://maplibre.org/maplibre-gl-js/docs/examples/add-a-wms-source/
- https://maplibre.org/maplibre-style-spec/
- https://maplibre.org/maplibre-style-spec/types/
- https://maplibre.org/about/
- https://github.com/maplibre/maplibre/blob/main/CHARTER.md
- https://github.com/maplibre/maplibre-gl-js
- https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt
- https://github.com/maplibre/maplibre-gl-js/blob/main/README.md
- https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md
- https://github.com/maplibre/maplibre-gl-js/blob/main/docs/guides/v5-to-v6-migration-guide.md
- https://github.com/maplibre/maplibre-gl-js/tree/main/docs/guides
- https://github.com/maplibre/maplibre-gl-js/releases
- https://github.com/maplibre/maplibre-gl-js/releases/tag/v5.0.0
- https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0
- https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.17.0
- https://github.com/maplibre/maplibre-gl-js/commits/main
- https://www.npmjs.com/package/maplibre-gl
- https://bundlephobia.com/package/maplibre-gl@6.17.0
- https://operations.osmfoundation.org/policies/tiles/
- https://github.com/visgl/react-map-gl
- https://www.npmjs.com/package/@vis.gl/react-maplibre
- https://github.com/indoorequal/vue-maplibre-gl
- https://github.com/dimfeld/svelte-maplibre
- https://nextjs.org/docs/app/getting-started/server-and-client-components
- https://nextjs.org/docs/app/guides/lazy-loading
- https://docs.astro.build/en/reference/directives-reference/
- 2026-11-11 に Node.js 23.9.0 で maplibre-gl 6.17.0 を import し、`new Map()` を呼んだ実測
- https://www.maplibre.org/news/2023-01-23-maplibre-user-group-japan/
- https://dev.to/mug-jp
- https://zenn.dev/mugjp/articles/try-118-maplibre-2025

## 未確認のこと

- WebGPU への取り組み: 公式ドキュメントと CHANGELOG に記述が見当たらず、計画の有無を確かめられなかった。
- bundlephobia の 296.7 kB にワーカーファイルが含まれるか: bundlephobia の結果に内訳がなく判断できなかった。
- Mapbox GL JS v2 以降のスタイル独自機能との互換範囲: 公式の一覧を確かめていない。
- WMTS を XYZ 形式の URL で読めるかは公式の例で確かめておらず、推測である。
- 公式ドキュメントの日本語訳の有無: 公式サイト上に見当たらなかったが、存在しないとは断定できない。
- 各ラッパー (react-map-gl、vue-maplibre-gl ほか) の v6 対応状況: 各リポジトリで確かめていない。
- 各ラッパーが SSR のフレームワークでサーバー側の実行を避けてくれるか: ラッパーごとの文書を確かめていない。
- Governing Board の構成員や法人格: 憲章に人数 (5 名) はあるが、現在の構成員と法人の有無は確かめていない。
