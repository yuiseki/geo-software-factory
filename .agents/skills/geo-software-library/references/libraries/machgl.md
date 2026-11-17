# MachGL

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-17 |
| 最新の安定版 (リリース日) | v0.1.1 (タグは 2026-11-16 JST)。v0.1.0 は 2026-11-12 JST。npm には出しておらず、CDN だけで配る (`https://cdn.geolonia.com/machgl/v0.1.1/`、版の URL は中身を変えない)。`/machgl/main/` は main ブランチの最新を配り、マージのたびに変わる (README) |
| リポジトリ | https://github.com/geolonia/machgl |
| ドキュメント | https://geolonia.github.io/machgl/ (英語)、https://geolonia.github.io/machgl/ja/ (日本語)。対応する機能と対応しない機能は「Supported features and behavior」(https://geolonia.github.io/machgl/reference.html) にまとまっている。告知は https://www.geolonia.com/news/2026-10-21-machgl-release/ と https://www.geolonia.com/news/2026-11-16-machgl-release/ |
| ライセンス (LICENSE ファイルで確かめる) | MIT (リポジトリの LICENSE)。earcut (ISC) の移植と、MapLibre GL JS / Mapbox GL JS (BSD-3-Clause) に沿ったシェーダーと MVT の読み取りを含み、著作権表示は THIRD-PARTY-NOTICES.md にある。`bld.js` は brotli の復号器 (MIT、復号器本体は Apache-2.0) を同梱する |
| 運営主体・ガバナンス | 株式会社 Geolonia が開発し、cdn.geolonia.com で配る。貢献の決まりと行動規範は Geolonia 共通のもの (CONTRIBUTING.md)。外部の参加者を含む運営組織は確認できなかった |

## 概要

ブラウザでベクトルタイルの地図を描く、WebGL2 の描画ライブラリである。MapLibre GL JS の派生ではなく、描画、MVT の読み取り、三角形分割、式の評価を自前で書き直している (README の Design decisions)。MapLibre Style Spec の一部を読み、`style.json` は変換なしで使えるが、JavaScript の API は MapLibre GL JS の置き換えではないと明記している (https://geolonia.github.io/machgl/reference.html)。

Geolonia の告知は、Geolonia Maps (embed) を埋め込んだページは、読み込むスクリプトの URL を MachGL に替えるだけで切り替わると書く。HTML の `data-*` 属性は Geolonia Embed と同じものを読む (https://www.geolonia.com/news/2026-11-16-machgl-release/、https://geolonia.github.io/machgl/guide/html-embed.html)。目玉は軽さと PLATEAU の建物で、建物は独自の `.bld` 形式のタイルで描く。

## 描画方式

- レンダリング: WebGL2 だけ。WebGL1 への切り替えは無い (README の Scope and limits)。
- 2D / 2.5D / 3D: 回転と傾き (0〜85°)、地形 (`raster-dem` と `setTerrain`)、陰影、空とかすみ (`sky`)、建物の立ち上げ (`fill-extrusion`) に対応する (https://geolonia.github.io/machgl/reference.html)。
- 地球儀表示: 無い。ソースに globe の実装が無く、Web メルカトルだけである (`src/geo.ts`、2026-11-17 に v0.1.1 以降の main で確認)。
- 注記: 文字はブラウザの Canvas2D で、端末のフォントで描く。SDF のグリフを取りに行かないので、日本語の注記にフォントの配信が要らない。代わりに字形が端末ごとに少し変わり、`text-pitch-alignment: map` (地面に寝かせた文字) は描けない (adr/0002-labels-canvas2d.md)。
- タイルの取得、読み取り、図形の生成は Web Worker で行う (README)。

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | `raster` ソースの zxy (https://geolonia.github.io/machgl/reference.html) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT は対応。PMTiles をブラウザで直接読むのは非対応。MLT は記載が無い | `vector` ソース (zxy か TileJSON)。PMTiles は README の「Not supported」にある。リポジトリの `worker/` に、PMTiles からタイルを配る Cloudflare Worker がある |
| スタイル仕様 | MapLibre Style Spec の一部 | 対応しない設定は `console.warn` を出して飛ばす。`color-relief`、`fill-extrusion-pattern`、`fog`、`mapbox://` の URL、`canvas` ソースなどは描かない。`setStyle` の `diff` は受けるが、常にスタイル全体を入れ替える (同上) |
| GeoJSON | 対応 | Worker の中でタイルに分ける。クラスタリング、ヒートマップ、地物ごとの状態 (`feature-state`)、`queryRenderedFeatures` がある。タッチ端末では既定で頂点数に上限を掛け、iPhone の Safari がメモリの使い過ぎでページを読み直すのを避ける (https://geolonia.github.io/machgl/guide/performance.html) |
| 3D Tiles / glTF | 点群 (pnts) だけ | 3D Tiles 1.0 の点群を `machgl/pointcloud` で読む (README)。ただし v0.1.1 の後、弧、MCT、点群は公開ページと API リファレンスから外された (issue #673 の関連コミット)。CDN の v0.1.1 の URL にはファイルが残っている (2026-11-17 に取得して確認)。glTF のメッシュとカスタムレイヤーは見当たらない |
| PLATEAU の建物 | 対応 (独自形式) | `.bld` タイル (平面形と屋根面) を `machgl/bld` で描く。LOD1〜LOD3 のデータをそのまま描けると告知は書く。CityGML から `.bld` を作る道具はリポジトリの `scripts/` にある (README、https://www.geolonia.com/news/2026-10-21-machgl-release/) |
| 地形 (標高タイル) | 対応 | `raster-dem` で地形と陰影 (同上) |
| WMS / WMTS | 記載が無い | ソースに `{bbox-epsg-3857}` の置き換えが見当たらない (2026-11-17、main で確認) |

## 組み合わせの制約

- API キー・アカウントの要否: Geolonia のスタイル (`geolonia/basic-v2` など、名前で指定) を使うときだけ `apiKey` が要る。キーは Geolonia のサーバーへのリクエストにだけ付き、外部のスタイル (例: OpenFreeMap) ならキー無しで描ける (https://geolonia.github.io/machgl/reference.html の Geolonia API key)。localhost ではデモキー `YOUR-API-KEY` が使える (README)。
- Geolonia Maps のタイルとの関係: Geolonia は MachGL を「これまでの Geolonia Maps と置き換えて」使えるものとして出している (https://www.geolonia.com/news/2026-11-16-machgl-release/)。2D では既存の Geolonia のスタイルをそのまま指定できる。3D の PLATEAU 用には `geolonia/toranomon` のスタイルがある (同)。
- MapLibre のプラグインとの組み合わせ: API が MapLibre GL JS と別なので、MapLibre 向けのプラグイン (描画ツール、ジオコーダーの UI など) はそのままでは載らない (推測。「JavaScript の API は置き換えではない」の記述から)。
- 縮尺、現在地、全画面のボタンは本体に無く、`machgl/controls` から読む (README)。

## ライセンスと費用

- ライセンス: MIT。
- 利用料: ライブラリは無料。Geolonia のスタイルとタイルを使えば、Geolonia Maps の地図の表示回数の課金に入るはずである (推測。料金は geo-software-infra の Geolonia Maps の項)。MachGL で数え方が変わるかは公開の資料に無い。
- ライセンス上の注意: コピーレフトの依存は無い。`package.json` の依存は `brotli` 1 つで、`bld.js` にだけ入る。本体の `machgl.js` は依存なし (README)。

## 性能と規模

- バンドルサイズ: CDN の v0.1.1 を 2026-11-17 に取得し、`gzip -9` で測った。`machgl.js` は 372,778 バイト、gzip 後 約 134 kB。`bld.js` は 364,506 バイト、gzip 後 約 190 kB (README の「約 80 KB」とは合わない。測り方の違いは未確認)。`controls.js` は gzip 後 約 7 kB。比べると、MapLibre GL JS を同梱する Geolonia embed v6 は gzip 後 約 471 kB ([geolonia-maps](geolonia-maps.md))。
- 2026-10-21 の告知は「gzip で約 98 KB、依存は 1 つ」と書き、README (2026-11-11 測定) は約 132 KB、依存なしと書く。リリースまでに機能が増えた分だと読める (推測)。
- 公式のベンチマーク (README、`npm run bench`、Apple M2 Max、headless Chromium + SwiftShader、OpenFreeMap の liberty、東京 z13、3 回の中央値): 読み込みと評価 14 ms、最初の描画完了 283 ms、待機後の JS ヒープ 41.9 MB。パン 120 フレームのメインスレッドの CPU は 2,601 ms で、同じ回の MapLibre GL JS は約 290 ms。GPU を使った同じ機械では MachGL 約 230 ms、MapLibre 約 310 ms。SwiftShader では回ごとのばらつきが大きいと README は注記している。本リポジトリでは測っていない。
- PLATEAU の建物を、スマートフォンでも速く出すことを主な狙いにしている (https://www.geolonia.com/news/2026-11-16-machgl-release/)。CI に性能の検査 (perf.yml、`bench/perf-budget.json`) がある。

## エコシステム

- プラグイン: MachGL 向けのものは公開されていない。
- React / Vue のラッパー: 見当たらない。npm に無いので、バンドラーからは CDN の ES モジュールを読む形になる。
- TypeScript の型: ソースは TypeScript で、`package.json` が `dist/index.d.ts` を指す。ただし npm に無いので、型を使うにはリポジトリからビルドする (推測)。
- 兄弟プロジェクト: `mach-tiles` (MachGL 向けの追加データを持つ MVT を作る道具) は README からリンクされているが、2026-11-17 時点で外部からは開けない (GitHub が 404 を返す)。デモ集 https://geolonia.github.io/machgl-apps/ は開ける。ネイティブ版は無い。
- 日本語の情報: ドキュメントの日本語版がある。コミットの説明も日本語が多い。

## 開発の活発さ

- リポジトリの作成は 2026-09-29、最初のタグは 2026-11-12。コミットは 1,463 件 (2026-11-17、main)。issue と PR の番号は 690 まで進み、開いている issue は 31 件である (GitHub、2026-11-17)。
- 版は 0.1 で、README は「API は変わりうる」と書く。
- 公開の前後で、公開する機能の範囲が動いている (弧、MCT、点群を v0.1.1 の後に公開ページから外した)。使う機能は、その時点のドキュメントに載っているかを確かめる。

## 環境の違いと保守

- ブラウザ間の互換: 自動テストは Chromium だけで、Firefox と Safari (iOS を含む) はテストしていないと README とドキュメントが明記している。題名に Safari を含む issue は 4 件 (GitHub の検索、2026-11-17)。
- OS 間の互換: CI は Ubuntu だけ (`.github/workflows/`)。
- 操作の網羅: ドラッグ、ズーム、回転、傾け、タッチと右クリックのイベントがある (https://geolonia.github.io/machgl/reference.html)。
- エッジケース: タイル取得の再試行 (5xx、408、429)、WebGL のコンテキスト喪失 (`webglcontextlost` / `webglcontextrestored`) の扱いが文書にある (同)。ADR が 5 本あり、待機の定義、入力の境界などの判断を残している (`adr/`)。
- CSP: `blob:` の Worker を許さないページ向けに、Worker のファイルを別に配っている (README、https://geolonia.github.io/machgl/guide/csp.html)。

## 向いている場面

- 日本語の注記を、フォントの配信なしで出したい。
- 地図以外の処理が重いページや、ダウンロードの量に予算があるページ (README の Use cases)。
- Geolonia Maps (embed) を使っているページを、HTML を変えずに軽くしたい。
- PLATEAU の建物を、スマートフォンのブラウザで出したい。

## 向いていない場面

- MapLibre GL JS の API やプラグインに頼ったコードがある (API に互換が無い)。
- 地球儀表示、PMTiles の直接の読み込み、WMS、3D Tiles のメッシュが要る。
- Firefox や Safari での動作を、提供元のテストで保証してほしい。
- npm でのバージョン管理、型、依存の監査を前提にした開発の流れ (2026-11-17 時点で npm に無い)。
- API の安定を求める長期の保守 (0.1 版)。

## 出典

- https://github.com/geolonia/machgl (README、package.json、LICENSE、THIRD-PARTY-NOTICES.md、CONTRIBUTING.md、adr/、.github/workflows/、2026-11-17 に clone)
- https://geolonia.github.io/machgl/
- https://geolonia.github.io/machgl/reference.html
- https://geolonia.github.io/machgl/guide/performance.html
- https://geolonia.github.io/machgl/guide/html-embed.html
- https://geolonia.github.io/machgl/guide/csp.html
- https://www.geolonia.com/news/2026-10-21-machgl-release/
- https://www.geolonia.com/news/2026-11-16-machgl-release/
- https://geolonia.github.io/machgl-apps/
- https://cdn.geolonia.com/machgl/v0.1.1/ (2026-11-17 に取得して大きさを測った)

## 未確認のこと

- Firefox、Safari、iOS での実際の描画と操作
- MachGL で Geolonia のタイルを使うときの課金の数え方と、サポートの範囲
- `bld.js` の大きさが README と手元の測定で違う理由
- MLT のベクトルタイルを読めるか
- 本リポジトリの条件 (geo-software-poc-measure) で MapLibre GL JS と並べた性能
- `.bld` 形式の仕様が、MachGL の外でも使える形で公開されているか
