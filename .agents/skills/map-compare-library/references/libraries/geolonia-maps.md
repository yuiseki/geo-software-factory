# Geolonia Maps SDK (embed, maps-suite, maps-react, maps-core)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 4 パッケージで版が別々である。@geolonia/embed 5.2.2 (2026-04-03 JST、npm の `next` タグは 6.0.0-pre.6、2026-10-30 JST)、@geolonia/maps-suite 2.2.0 (2026-11-09 JST)、@geolonia/maps-react 0.5.0 (2026-10-30 JST)、@geolonia/maps-core 0.8.0 (2026-10-26 JST) (https://www.npmjs.com/package/@geolonia/embed, https://www.npmjs.com/package/@geolonia/maps-suite, https://www.npmjs.com/package/@geolonia/maps-react, https://www.npmjs.com/package/@geolonia/maps-core)。公式ドキュメントのチュートリアルは embed を CDN の `embed/v6` で読み込んでおり、この URL が配信するのは 6.0.0-pre.6 である (https://docs.geolonia.com/tutorials/embed/publish/、配信ファイル内の版文字列で確認) |
| リポジトリ | embed は https://github.com/geolonia/embed 、maps-core は https://github.com/geolonia/maps-core 。maps-suite と maps-react はリポジトリが非公開で、npm のパッケージだけが公開されている (提供元への聞き取り、2026-11-10) |
| ドキュメント | https://docs.geolonia.com/ (リファレンスは https://docs.geolonia.com/reference/) |
| ライセンス (LICENSE ファイルで確かめる) | MIT。maps-core はリポジトリの LICENSE が MIT (Copyright (c) 2026 Geolonia Inc.) (https://github.com/geolonia/maps-core/blob/main/LICENSE)。maps-suite と maps-react は npm パッケージに同梱の LICENSE が MIT。embed はリポジトリと npm パッケージに LICENSE ファイルがなく、package.json の license 欄が MIT である (https://github.com/geolonia/embed) |
| 運営主体・ガバナンス | 株式会社 Geolonia が開発し配布している (LICENSE の著作権表記、https://docs.geolonia.com/)。外部の参加者を含む運営組織や憲章は確認できなかった |

## 概要

Geolonia Maps SDK は、Geolonia が配信する地図を Web サイトとアプリケーションに組み込むための JavaScript ライブラリ群である (https://docs.geolonia.com/)。基盤の maps-core の `GeoloniaMap` は MapLibre GL JS の `Map` を継承し、API キーによる認証、Geolonia のスタイルとタイルへの接続、PMTiles プロトコルの登録、既定のコントロール、simplestyle による GeoJSON 表示などを足したものである (https://docs.geolonia.com/reference/core/Class.GeoloniaMap/)。その上に、HTML の属性だけで使う embed、JavaScript から命令的に操作する maps-suite、React 向けの maps-react の 3 つがあり、公式は「いずれのライブラリでも同じ機能を実装できます」とする (https://docs.geolonia.com/tutorials/)。地図インスタンスから MapLibre GL JS の API をそのまま呼べる (https://docs.geolonia.com/howto/maps-core-access/)。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): WebGL。描画は MapLibre GL JS が行う (https://docs.geolonia.com/reference/)。maps-core、maps-suite、maps-react と embed 6.0.0-pre 系は MapLibre GL JS v6 系に依存するので、WebGL2 が必須になる (推測。MapLibre GL JS v6 の要件から)。WebGL が使えない端末では、地図の代わりに対処法を示すメッセージを出す (`errorMessage` オプション、https://www.npmjs.com/package/@geolonia/maps-core)。
- 2D / 2.5D (傾き・回転) / 3D: 傾き、回転に対応する。3D 建物は Geolonia の標準スタイルに含まれ、embed は `data-3d="on"`、maps-suite は既定で有効、maps-react は `3d` を渡して有効にする。外部スタイルを指定した場合はこの切り替えが効かない (https://docs.geolonia.com/howto/3d/)。
- 地球儀表示: 対応。maps-suite と maps-react で基盤の地図の `setProjection({ type: "globe" })` を呼ぶ。embed の HTML 属性だけでは使えない (https://docs.geolonia.com/howto/globe/)。
- 対応する投影法: 公式ドキュメントが案内するのは `mercator` と `globe` である (https://docs.geolonia.com/howto/globe/)。基盤が MapLibre GL JS の Map なので、MapLibre GL JS v6 が持つ投影はそのまま呼べる (推測)。

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 (maps-suite、maps-react) | `{z}/{x}/{y}` のテンプレート URL を raster ソースとして追加する。例は地理院タイル。embed の HTML 属性だけではこの機能は使えない (https://docs.geolonia.com/howto/custom-source/) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT と PMTiles は対応。MLT は未確認 | Geolonia の標準スタイルは MVT を使う。外部の MVT も vector ソースとして追加できる (https://docs.geolonia.com/howto/custom-source/)。`GeoloniaMap` は PMTiles プロトコルを登録する (https://docs.geolonia.com/reference/core/Class.GeoloniaMap/)。公式スタイル `geoloniamaps/smartcity-base` は国土地理院の最適化ベクトルタイルを PMTiles 形式で読む (https://docs.geolonia.com/explanation/styles/)。MLT は公式ドキュメントに記述がない |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 対応 (MapLibre Style Spec) | Geolonia のスタイル名 (`geolonia/basic-v2` など) か、スタイル JSON の URL を指定する。外部スタイルの例は `https://tile.openstreetmap.jp/styles/osm-bright/style.json` (https://docs.geolonia.com/howto/change-style/, https://docs.geolonia.com/explanation/map-style/) |
| GeoJSON | 対応 | embed は `data-geojson`、maps-core は `geojson` オプションと `SimpleStyle` で、simplestyle-spec に沿って描く。クラスタリング、コロプレス、ヒートマップ、値による円の大きさと色の描き分けがある (https://www.npmjs.com/package/@geolonia/maps-core, https://github.com/geolonia/embed/blob/master/CHANGELOG.md の v6.0.0-pre.6)。maps-suite には型の混在した GeoJSON を描く `Data` レイヤーがある (https://docs.geolonia.com/reference/) |
| 3D Tiles / glTF | 未確認 | 公式ドキュメントに記述がない。基盤の MapLibre GL JS のカスタムレイヤーは使えるはずである (推測) |
| 地形 (標高タイル) | 対応 (標準スタイル) | 標準スタイル `geolonia/basic-v2` は国土地理院の標高タイルを raster-dem ソース (`dem`) として持つ (https://cdn.geolonia.com/style/geolonia/basic-v2/ja.json)。地形の表示手順を説明したハウツーは見つからなかった |
| WMS / WMTS | 未確認 | 公式ドキュメントに記述がない。基盤が MapLibre GL JS の Map なので、raster ソースの URL に `{bbox-epsg-3857}` を入れる MapLibre の方法で WMS を読めるはずである (推測) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: SDK 側の制限は公式資料に記述がない。外部のタイルを重ねるときは、配信元の利用規約が求める出典を `attribution` に入れるよう案内している (https://docs.geolonia.com/howto/custom-source/)。
- API キー・アカウントの要否: Geolonia のスタイルとタイルを使うときだけ必要で、外部のスタイルを使うときは API キーなしで地図を作れる。maps-core の README は「Geolonia API key is only required when using Geolonia's hosted styles and tiles.」とする (https://www.npmjs.com/package/@geolonia/maps-core)。本番のドメインで Geolonia の地図を出すには、ダッシュボードで API キーを発行し、利用する URL を登録する。localhost、GitHub Pages など許可された環境ではデモキー `YOUR-API-KEY` で描画できる (https://docs.geolonia.com/explanation/free-referers/, https://docs.geolonia.com/tutorials/embed/publish/)。
- Geolonia Maps のタイルを使うのに、この SDK が必須か (公式の記述): 必須ではないが、SDK 以外から使うのはサポートの対象外である。技術的には使えるが、提供元は推奨しない (提供元への聞き取り、2026-11-10)。ドキュメントの「はじめに」、チュートリアル、リファレンス、FAQ、利用規約を調べたが、SDK 以外から使うことを禁じる、または SDK を必須とする文言は見つからなかった (https://docs.geolonia.com/, https://www.geolonia.com/products/faq/, https://www.geolonia.com/terms/)。関連する公開情報として、SDK は Geolonia のソースとスプライトへのリクエストに `key` と `sessionId` を付けており、`setTransformRequest()` でこの処理を外した場合は利用者が自分で付ける必要がある (https://www.npmjs.com/package/@geolonia/maps-core, https://github.com/geolonia/embed/blob/master/CHANGELOG.md の v6.0.0-pre.6)。`keyring` は SDK 全体で共有される API キー、ステージ、Geolonia スタイルの判定を保持する (https://docs.geolonia.com/reference/core/Variable.keyring/)。
- この SDK で Geolonia 以外のタイルやスタイルを表示できるか: できる。外部スタイル JSON の URL を指定でき (https://docs.geolonia.com/howto/change-style/)、外部のラスタタイルやベクトルタイルをソースとして追加できる (https://docs.geolonia.com/howto/custom-source/)。ただし 3D 建物の切り替えは Geolonia のスタイルでしか効かない (https://docs.geolonia.com/howto/3d/)。

## ライセンスと費用

- ライセンス: MIT (maps-core、maps-suite、maps-react は LICENSE ファイル、embed は package.json の license 欄)。
- 利用料 (無料 / 従量 / 有料の機能): SDK 自体は MIT で無料である。Geolonia のスタイルとタイルを使うと、地図の表示回数による従量課金の対象になる (料金は map-compare-infra の Geolonia Maps の項を参照、https://www.geolonia.com/pricing/)。Geolonia のスタイルとタイルを読まず、外部のスタイルとタイルだけを表示する場合は課金されない (提供元への聞き取り、2026-11-10。公開文書に記述はない)。
- 版によるライセンスの変化: なし (確かめた範囲で、どのパッケージもライセンスを変えた記録はない)。
- ライセンス上の注意 (コピーレフト、OSI 非承認の依存があれば、組み込み、改変、配布、SaaS 提供で求められること): embed の配布ファイルと maps-suite の script タグ用ビルドは MapLibre GL JS (BSD 3-Clause) を同梱する。BSD 3-Clause は再配布時に著作権表示と許諾条件の表示を求める。embed は 6.0.0-pre.5 で、同梱する maplibre-gl のライセンス表記が `dist/embed-core.js` から落ちていた問題を直した (https://github.com/geolonia/embed/blob/master/CHANGELOG.md)。コピーレフトの依存は、npm の dependencies に載る直接の依存の範囲では見当たらない (推測。間接依存までは調べていない)。

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): bundlephobia の値ではなく、2026-11-10 に配布ファイルを取得して `gzip -9` で手元で測った値である。
  - embed 5.2.2 の `dist/embed.js` (npm): 1,235,244 バイト、gzip 後 約 330 kB。MapLibre GL JS 5.19.0 を同梱する。
  - embed 6.0.0-pre.6 (CDN `embed/v6/embed`): 1,722,713 バイト、gzip 後 約 471 kB。MapLibre GL JS 6.12.0 とワーカーを同梱する。
  - maps-suite 2.2.0 の `dist/npm/index.js` (npm): 654,938 バイト、gzip 後 約 179 kB。maplibre-gl 本体は含まないが、約 498 KB (min) のワーカーを文字列として同梱する (https://www.npmjs.com/package/@geolonia/maps-suite)。
  - maps-suite の CDN `maps-suite/v2/maps-suite.js`: 1,987,551 バイト、gzip 後 約 551 kB。MapLibre GL JS 6.11.2 を同梱する。
  - maps-core 0.8.0 の `dist/npm/index.js` (npm): 85,977 バイト、gzip 後 約 21 kB。maplibre-gl は peer 依存で含まない。
  - maps-react 0.5.0 の `dist/index.js` (npm): 26,509 バイト、gzip 後 約 6 kB。maps-core と maplibre-gl は含まない。
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 公式の記述はない。3D 表示は負荷が高めで、表示範囲を絞るか必要な場面だけ有効にするよう案内している (https://docs.geolonia.com/howto/3d/)。描画は MapLibre GL JS なので、規模の目安は MapLibre GL JS の大規模データの手引きに従う (推測)。
- 低性能端末・モバイルブラウザでの注意: スクロールできるページで地図がスクロールを奪わないようにするジェスチャ制御 (`gestureHandling`) がある (https://www.npmjs.com/package/@geolonia/maps-core)。embed は画面に入ったときに地図を作り、画面外の地図はスクロールされるまで作らない (https://docs.geolonia.com/howto/maps-core-access/)。embed と maps-suite はワーカーを Blob URL から起動するので、Content-Security-Policy を設定したページでは `worker-src blob:` が要る (https://docs.geolonia.com/tutorials/embed/publish/, https://www.npmjs.com/package/@geolonia/maps-suite)。

## エコシステム

- 主なプラグイン・拡張: embed はプラグインの仕組みを持つ (`EmbedPlugin` 型、https://docs.geolonia.com/reference/embed/TypeAlias.EmbedPlugin/)。API キーの管理と利用量の確認に Geolonia CLI がある (https://docs.geolonia.com/explanation/cli/)。Claude Code 向けの Geolonia Agent Skills (MIT) があり、Google Maps JavaScript API から maps-suite へ移行する手順と、`google.maps.*` と `geolonia.maps.*` の対応表を含む (https://docs.geolonia.com/explanation/agent-skills/)。基盤が MapLibre GL JS の Map なので、MapLibre GL JS のプラグインを組み合わせられるはずである (推測)。
- React / Vue などのラッパー: React は公式の maps-react (`Map`、`Source`、`Layer`、`Marker`、`Popup`、各種コントロール、`MapProvider`、`useMap` などのフック、react と react-dom は 18 以上) (https://docs.geolonia.com/reference/, https://www.npmjs.com/package/@geolonia/maps-react)。Vue と Svelte の公式ラッパーはないが、maps-suite のカスタム要素 `<geolonia-map>` をテンプレートにそのまま書ける (https://docs.geolonia.com/howto/web-component/)。
- TypeScript の型: 4 パッケージとも型定義 (`.d.ts`) を同梱する (npm パッケージの中身で確認)。リファレンスは型定義から生成されている。maps-react だけは生成されたリファレンスがない (https://docs.geolonia.com/reference/)。
- ネイティブ版・兄弟プロジェクト: Android / iOS のネイティブ SDK は公開ドキュメントにない。FAQ はプログラミング言語について「JavaScript の SDK があります」とする (https://www.geolonia.com/products/faq/)。描画エンジンを共有する兄弟プロジェクトとして MapLibre Native を使えるかは公式資料に記述がない。
- 日本語の情報 (公式翻訳、国内コミュニティ): 公式ドキュメントは日本語で書かれ、英語版 (`/en/` 以下) もある (https://docs.geolonia.com/)。SDK 固有の国内コミュニティは確認できなかった。

## 開発の活発さ

- 直近 1 年のリリース数: 対象期間は 2025-11-10 から 2026-11-10 で、npm の公開記録で数えた (各パッケージの npm ページ)。
  - embed: 安定版 5 件 (5.0.2、5.0.3、5.1.0、5.2.1、5.2.2)、プレリリース 5 件 (6.0.0-pre.2 から 6.0.0-pre.6)。GitHub の Releases は 2023 年の v4.2.1 が最後で、以後はタグだけが付いている (https://github.com/geolonia/embed/releases, https://github.com/geolonia/embed/tags)。
  - maps-core: 13 件 (0.0.1 から 0.8.0)。初版は 2026-03-31 JST で、すべて 0.x である (https://github.com/geolonia/maps-core/releases)。
  - maps-suite: 12 件 (0.0.1 から 2.2.0)。初版は 2026-04-02 JST。
  - maps-react: 10 件 (0.0.1 から 0.5.0)。初版は 2026-06-09 JST。
- 最終コミット日: embed は 2026-11-10 JST (master ブランチ、https://github.com/geolonia/embed/commits/master)、maps-core は 2026-10-30 JST (main ブランチ、https://github.com/geolonia/maps-core/commits/main)。maps-suite と maps-react はリポジトリが非公開のため未確認。npm への最終公開は maps-suite が 2026-11-09 JST、maps-react が 2026-10-30 JST。
- 近年の大きな破壊的変更: embed 6.0.0-pre.4 で同梱する maplibre-gl を v6 系に上げた。maplibre-gl v6 にはデフォルトエクスポートがなく、`window.geolonia` 経由で MapLibre の API を触っている場合は v6 の変更点を確かめる必要がある (https://github.com/geolonia/embed/blob/master/CHANGELOG.md)。maps-core、maps-suite、maps-react は ESM のみの配布で `require()` の入口がなく、MapLibre GL JS v6 に合わせてバンドラー利用時にワーカーの設定 (`setWorkerUrl`) が要る。maps-suite はワーカーを同梱するので設定は不要である (https://www.npmjs.com/package/@geolonia/maps-core, https://www.npmjs.com/package/@geolonia/maps-suite, https://www.npmjs.com/package/@geolonia/maps-react)。maps-suite は 2.0.0 (2026-10-02 JST) で版の先頭が上がり、CDN の `maps-suite/v1` は MapLibre GL JS 5.23.0、`maps-suite/v2` は 6.11.2 を同梱している (配信ファイル内の版文字列で確認)。2.0.0 の変更内容を記した公開の変更履歴は見つからなかった。

## 4 つのパッケージの使い分け

| パッケージ | 版 | 使い方 (script タグ、npm、Web Components、React) | 位置づけ | 出典 |
|---|---|---|---|---|
| @geolonia/embed | 5.2.2 (npm `latest`)、6.0.0-pre.6 (npm `next`、CDN `embed/v6`) | script タグで CDN (`https://cdn.geolonia.com/embed/v6/embed?geolonia-api-key=...`) を読み、`<div class="geolonia" data-lat="..." data-lng="..." data-zoom="...">` のように `data-*` 属性で設定する。ビルドツールと npm は不要。`new geolonia.Map("#map")` で JavaScript から地図を作ることもでき、`window.geolonia` から MapLibre GL JS のクラスを直接使える。unpkg と jsDelivr からも読める。MapLibre GL JS を同梱する (5.2.2 は 5.19.0、6.0.0-pre.6 は 6.12.0) | HTML のタグだけで地図を埋め込む場合向け。外部タイルソースの追加や地球儀表示は HTML 属性だけではできない | https://docs.geolonia.com/tutorials/ , https://docs.geolonia.com/tutorials/embed/publish/ , https://docs.geolonia.com/howto/maps-core-access/ , https://www.npmjs.com/package/@geolonia/embed , https://github.com/geolonia/embed/blob/master/CHANGELOG.md |
| @geolonia/maps-suite | 2.2.0 | npm (`npm install @geolonia/maps-suite maplibre-gl`、maplibre-gl は peer 依存で `^6.11.2`) で `new geolonia.maps.Map(要素, { center: { lat, lng }, zoom, apiKey })` のように命令的に操作する。`importLibrary()` でクラスを読み込む。`Map`、`Marker`、`AdvancedMarkerElement`、`MarkerClusterer`、`InfoWindow`、`OverlayView`、`Polyline`、`Polygon`、`Circle`、`Data`、`Geocoder` などを持つ。CDN の script タグ用ビルドと、カスタム要素 `<geolonia-map api-key="..." center="緯度,経度" zoom="...">` (Web Components) もある。`getGeoloniaMap()` で基盤の地図を取り出す | 公式は「他の地図サービスからの移行、および既存の JavaScript 資産がある場合」に適するとする。公式の Agent Skills は Google Maps JavaScript API からの移行先として maps-suite を案内している | https://docs.geolonia.com/tutorials/ , https://docs.geolonia.com/tutorials/maps-suite/first-map/ , https://docs.geolonia.com/howto/web-component/ , https://docs.geolonia.com/explanation/agent-skills/ , https://www.npmjs.com/package/@geolonia/maps-suite |
| @geolonia/maps-react | 0.5.0 | npm (`npm install @geolonia/maps-react maplibre-gl`、peer 依存は react と react-dom が 18 以上、maplibre-gl が `^6.0.0`) で `<Map>`、`<Source>`、`<Layer>`、`<Marker>` などの React コンポーネントとして使う。`<Map>` の ref が基盤の `GeoloniaMap` である | React で作るサイトとアプリケーション向け。0.x の版である | https://docs.geolonia.com/tutorials/ , https://docs.geolonia.com/reference/ , https://docs.geolonia.com/howto/maps-core-access/ , https://www.npmjs.com/package/@geolonia/maps-react |
| @geolonia/maps-core | 0.8.0 | npm (`npm install @geolonia/maps-core maplibre-gl`、maplibre-gl は peer 依存で `^6.0.0`) で `new GeoloniaMap({ container, apiKey, style, center, zoom })` と書く。GitHub Releases に script タグ用の UMD ビルドを添付している | 上の 3 つが共通の土台として使う。公式は「直接使う場面は多くありません」とする。0.x の版である | https://docs.geolonia.com/reference/ , https://www.npmjs.com/package/@geolonia/maps-core , https://github.com/geolonia/maps-core/releases |

## 向いている場面

- Geolonia Maps のタイルとスタイルを使う Web の地図。API キーの付与、スタイル名の解決、3D 建物の切り替えを SDK が受け持つ。
- ビルド環境のない静的な HTML や CMS に、属性だけで地図を置きたい場合 (embed、または `<geolonia-map>`)。
- MapLibre GL JS の API とスタイル仕様を使いつつ、マーカー、ポップアップ、GeoJSON の描き分け (クラスタリング、コロプレス、ヒートマップ) を設定だけで済ませたい場合。
- `google.maps.*` に近いクラス構成 (`Map`、`Marker`、`InfoWindow` など) で書かれた既存の JavaScript を移したい場合 (maps-suite)。
- 開発中やプロトタイプを、キーを発行せずに localhost や GitHub Pages などで動かしたい場合。

## 向いていない場面

- Android / iOS のネイティブアプリに組み込む場合。公開されているのは JavaScript の SDK だけである。ネイティブアプリに近いものを作るなら、提供元が公開している PWA の地図アプリのテンプレート Geolonia PWAマップ (MIT、https://github.com/geoloniamaps/pwamap) がある。提供元によれば利用は定着している (提供元への聞き取り、2026-11-10)。
- 版の安定を重視する案件。maps-core と maps-react は 0.x で、embed の v6 系はプレリリースのまま公式ドキュメントが案内している。
- ソースコードと変更履歴を公開リポジトリで追いたい場合。maps-suite と maps-react のリポジトリは非公開である。
- WebGL2 が使えない環境を相手にする場合 (MapLibre GL JS v6 に依存する版。MapLibre GL JS v6 の要件からの推測)。
- 3D Tiles、WMTS の Capabilities 読み込みなど、公式ドキュメントにない形式を標準機能として扱いたい場合。

## 出典

- https://docs.geolonia.com/
- https://docs.geolonia.com/tutorials/
- https://docs.geolonia.com/tutorials/embed/publish/
- https://docs.geolonia.com/tutorials/maps-suite/first-map/
- https://docs.geolonia.com/reference/
- https://docs.geolonia.com/reference/core/Class.GeoloniaMap/
- https://docs.geolonia.com/reference/core/Variable.keyring/
- https://docs.geolonia.com/reference/embed/TypeAlias.EmbedPlugin/
- https://docs.geolonia.com/explanation/free-referers/
- https://docs.geolonia.com/explanation/map-style/
- https://docs.geolonia.com/explanation/styles/
- https://docs.geolonia.com/explanation/agent-skills/
- https://docs.geolonia.com/explanation/cli/
- https://docs.geolonia.com/howto/maps-core-access/
- https://docs.geolonia.com/howto/web-component/
- https://docs.geolonia.com/howto/custom-source/
- https://docs.geolonia.com/howto/change-style/
- https://docs.geolonia.com/howto/3d/
- https://docs.geolonia.com/howto/globe/
- https://cdn.geolonia.com/style/geolonia/basic-v2/ja.json
- https://www.geolonia.com/products/faq/
- https://www.geolonia.com/terms/
- https://www.geolonia.com/pricing/
- https://github.com/geolonia/embed
- https://github.com/geolonia/embed/blob/master/CHANGELOG.md
- https://github.com/geolonia/embed/releases
- https://github.com/geolonia/embed/tags
- https://github.com/geolonia/embed/commits/master
- https://github.com/geolonia/maps-core
- https://github.com/geolonia/maps-core/blob/main/LICENSE
- https://github.com/geolonia/maps-core/releases
- https://github.com/geolonia/maps-core/commits/main
- https://www.npmjs.com/package/@geolonia/embed
- https://www.npmjs.com/package/@geolonia/maps-suite
- https://www.npmjs.com/package/@geolonia/maps-react
- https://www.npmjs.com/package/@geolonia/maps-core

## 未確認のこと

- SDK 以外からの利用の扱いを書いた公式文書: 提供元への聞き取りでは、技術的には使えるがサポート外である。ただし、ドキュメント、FAQ、利用規約に該当する文言は見つからなかった。SDK を使わずに MapLibre GL JS 単体、Leaflet、OpenLayers から使う公式の手順もない。
- maps-suite と maps-react のソースコードと変更履歴: リポジトリが非公開で、npm のパッケージと公式ドキュメントしか確かめられなかった。そのため両者の最終コミット日と、maps-suite 2.0.0 の破壊的変更の内容は確かめていない。
- MLT、3D Tiles / glTF、WMS / WMTS への対応: 公式ドキュメントに記述がない。基盤が MapLibre GL JS の Map であることからの推測にとどまる。
- 地形 (3D 地形) の表示手順: 標準スタイルが標高タイルのソースを持つことは確かめたが、地形を立体表示する手順の公式ドキュメントが見つからなかった。
- バンドルサイズ: bundlephobia などの第三者の値ではなく、手元で `gzip -9` した値である。配信時の圧縮方式 (brotli など) では値が変わる。
- 間接依存のライセンス: 直接の依存しか見ていない。
- MapLibre Native との組み合わせ: Geolonia のスタイルとタイルを MapLibre Native から使えるか、使ってよいかを示す公式資料がない。
