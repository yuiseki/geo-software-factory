# Leaflet

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 1.9.4 (2023-05-18)。npm の `latest` タグも 1.9.4 である。2.0 系はプレリリースで、最新は 2.0.0-beta.3 (2026-11-10、npm の `beta` タグ、2026-11-11 確認) (https://github.com/Leaflet/Leaflet/releases, https://www.npmjs.com/package/leaflet) |
| リポジトリ | https://github.com/Leaflet/Leaflet |
| ドキュメント | https://leafletjs.com/ (API リファレンスは https://leafletjs.com/reference.html) |
| ライセンス (LICENSE ファイルで確かめる) | BSD 2-Clause。著作権表記は Volodymyr Agafonkin (2010-2026) と CloudMade (2010-2011) (https://github.com/Leaflet/Leaflet/blob/main/LICENSE) |
| 運営主体・ガバナンス | 作者の Volodymyr Agafonkin が始め、現在は多数のコントリビュータが開発する (https://leafletjs.com/)。2.0 alpha の告知は「The Leaflet Team」名義である (https://leafletjs.com/2025/05/18/leaflet-2.0.0-alpha.html)。法人や委員会の規程は確かめられなかった |

## 概要

Leaflet はモバイル対応の対話的な地図を作る JavaScript ライブラリで、公式サイトは「約 40 KB の JS」と説明している (https://leafletjs.com/)。タイル、WMS、ベクター、GeoJSON、画像や動画のオーバーレイをレイヤーとして重ね、パン、ズーム、マーカー、ポップアップを扱う (https://leafletjs.com/)。地図画像そのものは提供せず、利用者がタイルサービスを選んで組み合わせる (https://github.com/Leaflet/Leaflet/blob/main/FAQ.md)。コアを小さく保ち、それ以外はプラグインに任せる方針である (同 FAQ)。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): タイルとマーカーは DOM 要素、ベクターは SVG か Canvas 2D を選ぶ (https://leafletjs.com/, https://github.com/Leaflet/Leaflet/blob/main/FAQ.md)。ソースの `src/layer/vector` には `SVG.js` と `Canvas.js` のレンダラーがある (https://github.com/Leaflet/Leaflet/tree/main/src/layer/vector)。WebGL / WebGPU のレンダラーはコアにない。
- 2D / 2.5D (傾き・回転) / 3D: 2D のみ。地図の傾き (pitch) や回転はコアにない。2.0.0-beta.1 でマーカー単体の回転 (`rotation` オプション) が加わった (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.1)。
- 地球儀表示: 対象外。コアに地球儀表示はない。
- 対応する投影法: コアの CRS は EPSG:3857 (既定)、EPSG:4326、EPSG:3395、Simple (非地理座標) である (https://github.com/Leaflet/Leaflet/tree/main/src/geo/crs, https://leafletjs.com/reference.html)。他の投影法はプラグイン Proj4Leaflet で扱う (https://github.com/kartena/Proj4Leaflet)。ただし Proj4Leaflet の最終 push は 2020-02-14 で、2.0 対応は未確認。

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | `TileLayer` が基本機能である (https://leafletjs.com/reference.html)。2.0.0-beta.1 からタイル取得の既定 `referrerPolicy` が `strict-origin-when-cross-origin` になり、`http://` の OSM タイル URL を https に上げる (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.1) |
| ベクトルタイル (MVT / PMTiles / MLT) | コアは非対応。プラグインで一部対応 | protomaps-leaflet (BSD-3-Clause) が MVT の Z/X/Y URL と PMTiles を描画し、ラベル配置まで行う。ただし README は「Maintenance Mode」と明記し、新機能は追加せず、既存の Leaflet システム以外では MapLibre GL JS を勧めている (https://github.com/protomaps/protomaps-leaflet)。スタイルは JavaScript で書き、MapLibre Style は読まない (同 README の「Configurable via plain JavaScript」)。他に Leaflet.VectorGrid がある (最終 push 2025-01-09、https://github.com/Leaflet/Leaflet.VectorGrid)。MapLibre GL JS の地図を Leaflet のレイヤーとして載せる maplibre-gl-leaflet (ISC) もある (https://github.com/maplibre/maplibre-gl-leaflet)。MLT 対応は未確認 |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 非対応 | コアに Style 仕様の読み込みはない。Style で描くなら maplibre-gl-leaflet 経由で MapLibre GL JS に描かせる (https://github.com/maplibre/maplibre-gl-leaflet) |
| GeoJSON | 対応 | `GeoJSON` レイヤー (https://leafletjs.com/reference.html)。2.0.0-beta.1 で `filter` / `onEachFeature` への引数と null ジオメトリの扱いが変わった (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.1) |
| 3D Tiles / glTF | 非対応 | 3D 描画の仕組みがない |
| 地形 (標高タイル) | 非対応 | 標高タイルを 3D 地形として描く機能はない。陰影図などを画像タイルにしたものは XYZ として重ねられる |
| WMS / WMTS | WMS は対応、WMTS は一部 | WMS は `WMSTileLayer` (1.x では `TileLayer.WMS`) がコアにある (https://github.com/Leaflet/Leaflet/tree/main/src/layer/tile)。WMTS 専用クラスはコアにない。XYZ 形式の URL テンプレートで呼べる WMTS なら `TileLayer` で読める (推測) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリ側の制限はなく、タイル提供者の利用規約に従う必要がある (https://github.com/Leaflet/Leaflet/blob/main/FAQ.md)。OpenStreetMap 財団の標準タイル (tile.openstreetmap.org) は、帰属表示、アプリを識別できる User-Agent と Referer、表示していないタイルの一括取得 (オフライン保存を含む) の禁止、過度な利用の禁止を定め、SLA はなく予告なく遮断されうる (https://operations.osmfoundation.org/policies/tiles/)。Google のタイルは Map Tiles API を規約 (API キー、セッショントークン、帰属) に沿って `TileLayer` で使える、と FAQ は書く (https://github.com/Leaflet/Leaflet/blob/main/FAQ.md)。
- API キー・アカウントの要否: ライブラリ自体には不要 (https://github.com/Leaflet/Leaflet/blob/main/FAQ.md)。タイル提供者によっては必要になる。

## ライセンスと費用

- ライセンス: BSD 2-Clause (https://github.com/Leaflet/Leaflet/blob/main/LICENSE)。FAQ は、アプリの UI か配布物のどこかで Leaflet の利用を表示するよう求めている (https://github.com/Leaflet/Leaflet/blob/main/FAQ.md)。
- 利用料 (無料 / 従量 / 有料の機能): ライブラリは無料。費用はタイル提供者の料金で決まる (https://github.com/Leaflet/Leaflet/blob/main/FAQ.md)。
- 版によるライセンスの変化: なし (2.0 系の npm パッケージも BSD-2-Clause、https://www.npmjs.com/package/leaflet)

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 1.9.4 は 42.7 kB、2.0.0-beta.2 は 40.7 kB (bundlephobia、https://bundlephobia.com/package/leaflet@1.9.4, https://bundlephobia.com/package/leaflet@2.0.0-beta.2)。2.0.0-beta.1 のリリースノートは、tree shaking によりタイルレイヤー 1 枚の地図が 25.6 kB (gzip) になったと書く (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.1)。
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 公式に数値の目安はない。FAQ は、数千のマーカーには Leaflet.markercluster を、数千点のベクターには SVG から Canvas レンダラーへの切り替えを勧め、それでも多すぎるなら画像タイルにするよう書く (https://github.com/Leaflet/Leaflet/blob/main/FAQ.md)。
- 低性能端末・モバイルブラウザでの注意: 1.x はモバイル対応を掲げる (https://leafletjs.com/)。2.0.0-beta.1 は Baseline 2022 のブラウザ (Safari 15.4 以降) を対象とし、Internet Explorer の対応は 2.0 で外れた (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.1, https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-alpha)。2.0.0-beta.1 は `prefers-reduced-motion` に従って動きを抑える (同 beta.1 ノート)。

## エコシステム

- 主なプラグイン・拡張: 公式のプラグイン一覧に数百件が載る (https://leafletjs.com/plugins.html, https://github.com/Leaflet/Leaflet/blob/main/FAQ.md)。例として Leaflet.markercluster (MIT、https://github.com/Leaflet/Leaflet.markercluster)、Leaflet.heat (BSD-2-Clause、https://github.com/Leaflet/Leaflet.heat)、Esri Leaflet (Apache-2.0、https://github.com/Esri/esri-leaflet)、Leaflet-Geoman (MIT、https://github.com/geoman-io/leaflet-geoman)、protomaps-leaflet と maplibre-gl-leaflet (上記) がある。2.0.0-beta.2 から、2.0 で動くプラグインはプラグイン一覧で「Ready for Leaflet 2」として区別される。markercluster と heat は 1.9 と 2.0 の両方に対応した例として挙げられている (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.2)。
- React / Vue などのラッパー: React は react-leaflet (5.0.0、2024-12-14)。ライセンスは OSI 承認ではない Hippocratic License 2.1 である (https://github.com/PaulLeCam/react-leaflet, https://www.npmjs.com/package/react-leaflet)。Vue は vue-leaflet (MIT、最終 push 2024-07-10、https://github.com/vue-leaflet/vue-leaflet)。いずれも Leaflet 2.0 対応は未確認。
- SSR のフレームワーク (Next.js、Astro など) で使うとき: 2026-11-11 に Node.js 23.9.0 で試すと、Leaflet 1.9.4 は `import` しただけで `ReferenceError: window is not defined` になり、2.0.0-beta.3 は `import` が通った (実測)。1.x ではモジュールの読み込み自体をブラウザだけで行う必要がある。Next.js の App Router では、`'use client'` を付けた Client Component も初回はサーバーで事前レンダリングされるので (https://nextjs.org/docs/app/getting-started/server-and-client-components)、地図のコンポーネントを Client Component の中から `next/dynamic` の `{ ssr: false }` で読み込む。`ssr: false` は Server Component では使えない (https://nextjs.org/docs/app/guides/lazy-loading)。Astro では `client:only="react"` のようにフレームワークを添えて付ける (https://docs.astro.build/en/reference/directives-reference/)。react-leaflet を使う場合も、Leaflet 本体を読み込む点は変わらない (推測)。
- TypeScript の型: 1.x は DefinitelyTyped の `@types/leaflet` (最新 1.9.22、https://www.npmjs.com/package/@types/leaflet)。2.0.0-beta.1 からは型をパッケージに同梱し、`@types/leaflet` は使わない (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.1)。
- ネイティブ版・兄弟プロジェクト: なし (公式のネイティブ SDK は確認した範囲で見当たらない)
- 日本語の情報 (公式翻訳、国内コミュニティ): 公式サイトのトップページに日本語版への導線は見当たらなかった (https://leafletjs.com/)。国内コミュニティは未確認。

## 開発の活発さ

- 直近 1 年のリリース数: 安定版 0 件、プレリリース 2 件 (2.0.0-beta.1 が 2026-11-02、2.0.0-beta.2 が 2026-11-06)。対象期間は 2025-11-10 から 2026-11-10 (https://github.com/Leaflet/Leaflet/releases)
- 最終コミット日: 2026-11-10 (JST、main ブランチ、https://github.com/Leaflet/Leaflet/commits/main)
- 近年の大きな破壊的変更: 2.0 で大きく変わる。2.0.0-alpha (2025-05-18) で ESM 化、グローバル `L` をコアから外す (`leaflet-global.js` に分離)、`L.marker()` などのファクトリをコンストラクタ (`new Marker()`) に置き換え、Pointer Events への移行、IE の対応終了を行った (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-alpha, https://leafletjs.com/2025/05/18/leaflet-2.0.0-alpha.html)。2.0.0-beta.1 (2026-11-02) で default export の廃止、クラス名の平坦化 (`TileLayer.WMS` → `WMSTileLayer` など)、`preferCanvas` の廃止、`Class.extend()` の廃止、型の同梱などが加わった (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.1)。古いプラグイン向けに Leaflet V1 Polyfill がある (https://github.com/Falke-Design/Leaflet-V1-polyfill)。移行ガイドは https://github.com/Leaflet/Leaflet/blob/main/MIGRATION.md 。2.0 安定版の時期は公表されていない (未確認)。

## 環境の違いと保守

- ブラウザ間の互換: 文書でうたうのは「Works in all modern browsers」と「all major desktop and mobile platforms」で動くという記述である (https://leafletjs.com/)。2.0.0-beta.1 は Baseline 2022 のブラウザ (Safari 15.4 以降) を対象にした (https://github.com/Leaflet/Leaflet/blob/main/CHANGELOG.md)。CI で確かめているのは Chromium、Firefox、WebKit の 3 種で、Vitest のブラウザモードを Playwright で動かし、WebKit の job だけを macOS で回す (https://github.com/Leaflet/Leaflet/blob/main/.github/workflows/main.yml, https://github.com/Leaflet/Leaflet/blob/main/vitest.config.js)。同じ CI で Node から import する SSR の確認 (`spec/ssr.js`) も回す (同 main.yml)。
- OS 間の互換: 文書は「Mouse, touch and pen support」をうたう (https://leafletjs.com/)。CI の OS は Ubuntu (Chromium、Firefox) と macOS (WebKit) で、iOS や Android の実機やエミュレータでの自動テストは CI 設定に見当たらない (https://github.com/Leaflet/Leaflet/blob/main/.github/workflows/main.yml)。iOS 固有の修正は続いており、2.0.0-beta.2 でキャンバスレンダラーの二度タップが `dblclick` を 3 回発火する不具合と、長押しの `contextmenu` の後に click が出る不具合を直した (https://github.com/Leaflet/Leaflet/blob/main/CHANGELOG.md)。DOM と SVG と Canvas 2D で描くため GPU に依存しないが、メモリ上限への対応を述べた文書は未確認。
- 操作の網羅: Map のオプションにドラッグ (`dragging`)、慣性 (`inertia`、`inertiaDeceleration`)、ホイール (`scrollWheelZoom`)、ピンチ (`pinchZoom`)、ダブルクリック (`doubleClickZoom`)、Shift ドラッグの範囲ズーム (`boxZoom`)、キーボード (`keyboard`、`keyboardPanDelta`)、長押し (`tapHold`) がある (https://leafletjs.com/reference.html 、2.0.0-beta.3 の版)。2.0 で Pointer Events に移り、マウスとタッチとペンを同じ経路で扱う (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-alpha)。地図の回転はコアにない。ページのスクロールと両立させる設定 (二本指でだけ動かす、修飾キーでだけズームする) はコアのオプションに見当たらない (https://leafletjs.com/reference.html)。
- エッジケースへの対応: 日付変更線は `worldCopyJump` で世界の複製の間を移る扱いがあり、2.0.0-beta.3 でも `setView` との組み合わせの不具合を直している (https://github.com/Leaflet/Leaflet/blob/main/CHANGELOG.md)。タイルの読み込み失敗は `tileerror` イベントで受け、ズーム中に取り除いたタイルが `tileerror` を出す不具合を 2.0.0-beta.1 で直した (同 CHANGELOG)。失敗したタイルの自動の再試行は未確認。GeoJSON の null ジオメトリの扱いは 2.0.0-beta.1 で変わった (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.1)。WebGL を使わないので GPU のコンテキスト喪失は対象外である。浮動小数点の精度と壊れたデータの扱いを述べた文書は未確認。
- 継続的な保守: CSP についての公式文書は未確認 (タイトルに CSP を含む issue は 3 件、検索語 `repo:Leaflet/Leaflet CSP in:title`、2026-11-12)。対応ブラウザの方針は 2.0 で IE を外し Baseline 2022 に上げた (https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-alpha, https://github.com/Leaflet/Leaflet/blob/main/CHANGELOG.md)。直近では 2.0.0-beta.1 で iOS 18.2 以降のダブルタップズームと、Chrome 144 以降で `pointerover` 中に `bringToFront` を呼ぶと hover が壊れる不具合を直した (同 CHANGELOG)。ブラウザ固有の不具合には `ios` と `mobile` のラベルがあり、`label:ios` は 22 件、`label:mobile` は 94 件、タイトルに Safari を含む issue は 85 件、Firefox は 113 件である (GitHub の issue 検索、`repo:Leaflet/Leaflet` に各条件を付けて、2026-11-12)。

## 向いている場面

- 背景をラスタタイル (XYZ) か WMS で済ませ、マーカー、ポップアップ、GeoJSON を重ねる軽い地図。
- 依存を増やさず小さなバンドルで地図を入れたいとき。
- 既存のプラグイン (クラスタリング、作図、Esri サービス連携など) をそのまま使いたいとき。

## 向いていない場面

- ベクトルタイルを Style 仕様で描く地図。protomaps-leaflet は保守モードで、作者自身が新規には MapLibre GL JS を勧めている (https://github.com/protomaps/protomaps-leaflet)。
- 傾き、回転、3D 地形、3D 建物、地球儀が要る地図。
- 数万件以上の地物をクライアントで直接描く用途 (FAQ はクラスタリングか画像タイル化を勧める)。
- 2026-11 時点で新規に始め、長く使う予定の案件。安定版 1.9.4 は 2023-05 以降更新がなく、2.0 は beta で API が大きく変わるため、どちらを選んでも移行の手間が見込まれる。

## 出典

- https://leafletjs.com/
- https://leafletjs.com/reference.html
- https://leafletjs.com/plugins.html
- https://leafletjs.com/2025/05/18/leaflet-2.0.0-alpha.html
- https://github.com/Leaflet/Leaflet
- https://github.com/Leaflet/Leaflet/blob/main/LICENSE
- https://github.com/Leaflet/Leaflet/blob/main/FAQ.md
- https://github.com/Leaflet/Leaflet/blob/main/MIGRATION.md
- https://github.com/Leaflet/Leaflet/releases
- https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-alpha
- https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.1
- https://github.com/Leaflet/Leaflet/releases/tag/v2.0.0-beta.2
- https://github.com/Leaflet/Leaflet/commits/main
- https://github.com/Leaflet/Leaflet/tree/main/src/geo/crs
- https://github.com/Leaflet/Leaflet/tree/main/src/layer/tile
- https://github.com/Leaflet/Leaflet/tree/main/src/layer/vector
- https://www.npmjs.com/package/leaflet
- https://www.npmjs.com/package/@types/leaflet
- https://bundlephobia.com/package/leaflet@1.9.4
- https://bundlephobia.com/package/leaflet@2.0.0-beta.2
- https://operations.osmfoundation.org/policies/tiles/
- https://github.com/protomaps/protomaps-leaflet
- https://github.com/Leaflet/Leaflet.VectorGrid
- https://github.com/maplibre/maplibre-gl-leaflet
- https://github.com/kartena/Proj4Leaflet
- https://github.com/Leaflet/Leaflet.markercluster
- https://github.com/Leaflet/Leaflet.heat
- https://github.com/Esri/esri-leaflet
- https://github.com/geoman-io/leaflet-geoman
- https://github.com/Falke-Design/Leaflet-V1-polyfill
- https://github.com/PaulLeCam/react-leaflet
- https://www.npmjs.com/package/react-leaflet
- https://github.com/vue-leaflet/vue-leaflet
- https://nextjs.org/docs/app/getting-started/server-and-client-components
- https://nextjs.org/docs/app/guides/lazy-loading
- https://docs.astro.build/en/reference/directives-reference/
- 2026-11-11 に Node.js 23.9.0 で leaflet 1.9.4 と 2.0.0-beta.3 を import した実測

## 未確認のこと

- 運営体制: 法人、委員会、意思決定の規程を記した文書を見つけられなかった。
- 2.0 安定版の公開時期と 1.x の保守方針: 2.0 alpha の告知とリリースノートに記述がなかった。
- MLT への対応: Leaflet 本体にも protomaps-leaflet にも記述が見当たらなかった。
- WMTS を `TileLayer` で読めるかは公式の記述を確かめておらず、推測である。
- Proj4Leaflet、react-leaflet、vue-leaflet の Leaflet 2.0 対応: 各リポジトリで明示を確かめていない。
- 国内コミュニティ: 調べる時間内に一次情報を確かめられなかった。
