# VersaTiles Frontend

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-16 |
| 最新の安定版 (リリース日) | versatiles-frontend v3.17.2 (2026-11-11)。同梱するスタイルの `@versatiles/style` は v9.1.0 (2026-11-09)、サーバーの versatiles-rs は v5.12.0 (2026-11-13) (GitHub、2026-11-16 取得) |
| リポジトリ | https://github.com/versatiles-org/versatiles-frontend |
| ドキュメント | https://docs.versatiles.org/basics/frontend |
| ライセンス (LICENSE ファイルで確かめる) | リポジトリは MIT (GitHub の API で確認)。同梱物の MapLibre GL JS は BSD-3-Clause、フォントは書体ごとに別のライセンス (一覧は未確認) |
| 運営主体・ガバナンス | VersaTiles プロジェクト。寄付が資金で、有償の運営会社は見当たらない |

## 概要

地図の画面を作るためのライブラリそのものではなく、`versatiles serve` が配るウェブの資産の一式である。MapLibre GL JS、5 つのスタイル (colorful、natural、muted、gray、toner と各ダーク版、衛星)、10 の書体の SDF フォント、スプライトを 1 つの tar にまとめてある。サーバーに `-s frontend.br.tar.gz` と渡すと、タイルと同じオリジンから地図のページ、スタイル、フォント、アイコンが出る (https://docs.versatiles.org/basics/versatiles_server)。

- `frontend` (約 91MB): 標準。フォントとスプライトとライブラリがすべて入る。`/editor/` に地図の編集 UI も入る
- `frontend-dev`: 標準と同じで、開発向けの UI
- `frontend-min` (約 39MB): Noto Sans だけ
- `frontend-blank` (約 89MB): フォントとスプライトだけ。自分の JavaScript を持ち込む
- `frontend-tiny` (約 1MB): MapLibre、スタイル 1 つ、スプライト、ラテン文字だけの Noto Sans

描画のライブラリ自体は MapLibre GL JS なので、描画の性能、API、対応するデータは [MapLibre GL JS](../libraries/maplibre-gl-js.md) の reference を読む。ここでは、配信の構成を含めた「一式」としての扱いを書く。

周辺の部品もある (すべて GitHub の versatiles-org、確かめた日は同じ)。

- `@versatiles/style`: MapLibre のスタイルを JavaScript で組み立てる (MIT)。テーマ、言語、フォントの指定ができる
- `node-versatiles-svelte`: MapLibre を Svelte で使うコンポーネント (MIT、v4.0.1)
- `maplibre-versatiles-styler`: MapLibre のスタイルをブラウザで編集するプラグイン (Unlicense)
- `versatiles-map-editor`: 地物を描いてスタイルを付ける埋め込み可能な編集器 (MIT、v4.3.0、2026-06 に作成)
- `versatiles-svg-renderer`: 地図を SVG として描く (作業中と書かれている)
- `versatiles-glyphs-rs`、`versatiles-fonts`: SDF のグリフの生成と、フォントの一式

## 描画方式

MapLibre GL JS と同じ (WebGL)。このフロントエンドは描画エンジンを持たない。

## 対応するデータ

[MapLibre GL JS](../libraries/maplibre-gl-js.md) と同じ。同梱のスタイルは、VersaTiles の Shortbread スキーマのベクトルタイルと、衛星のラスタタイルを前提にする。別のスキーマ (OpenMapTiles など) のタイルには、そのままでは合わない。`@versatiles/style` の `omt()` が OpenMapTiles 向けのスタイルを作る記載があるが、動作は確かめていない。

## 組み合わせの制約

- タイルの供給元: 同梱のスタイルは Shortbread スキーマ前提。[VersaTiles の reference](../../../geo-software-infra/references/providers/versatiles.md) のタイルか、自前で生成した同じスキーマのタイルを使う
- 配信側: `versatiles-rs` か `node-versatiles-server` が、tar をそのまま配る
- API キー・アカウントの要否: 不要
- 公開デモ tiles.versatiles.org の資産 (MapLibre、スタイル) を直接読むと、破壊的な更新が入りうると公式が警告している。固定したいときは、リリースの tar を自分で配る (https://docs.versatiles.org/guides/use_tiles_versatiles_org)

## ライセンスと費用

- ライセンス: 一式のリポジトリは MIT。MapLibre は BSD-3-Clause。フォントは書体ごとに異なる (公式の説明では「オープンソースの書体」)。配布形態ごとに、同梱の書体の一覧とライセンスを確かめる
- 利用料: 無料。商用の提供は無い。実費は自前のサーバーだけ

## 性能と規模

- 配信の資産は Brotli で事前圧縮されていて、サーバーが CPU をほとんど使わずに配る (https://docs.versatiles.org/basics/frontend)
- `frontend-tiny` は約 1MB で、ラテン文字だけ。日本語の注記が要るなら、日本語を含む書体が入る版を選ぶ必要があり、どの書体が CJK を含むかは未確認

## エコシステム

- MapLibre の周辺 (プラグイン、Maputnik、MapLibre Native) と、そのまま組み合わせられる。モバイルは、サーバーのスタイル URL を MapLibre Native に渡す (https://docs.versatiles.org/guides/what_about_mobile)
- 地図に載せる自前のデータは、`versatiles serve` に別のタイルのファイル (`.pmtiles`、`.mbtiles` など) を足して、同じサーバーから配れる

## 開発の活発さ

- 2026-11-15 までに versatiles-rs、スタイル、フロントエンドのいずれも更新されていた (GitHub、2026-11-16 確認)。リリースの頻度は高く、メジャー版の更新で名前の変更が入ることがある (旧名のスタイル `graybeard` などは別名で残る)

## 環境の違いと保守

- 一式の更新は、タイル、スタイル、フォントの版を揃えて入れ替える。スタイルが期待するタイルの層の構成は、スタイルの版で変わる (v8 で土地被覆の扱いが変わった記載)
- フロントエンドの tar を差し替えるだけで、サーバーを止めずに更新できるかは未確認

## 向いている場面

- 自前のサーバー 1 つで、タイルと地図のページを丸ごと出したい。外部の CDN や API に頼らない構成にしたい
- 閉域網やオフライン、データの持ち出し制限がある環境で、MapLibre の地図を出す
- 試作を速く立てたい。`versatiles serve -s frontend.br.tar.gz osm.versatiles` で、地図のページまで動く

## 向いていない場面

- 自分のアプリの画面に地図を組み込む場合 (この一式は、地図の画面を丸ごと配るもので、アプリのフレームワークには入らない)。MapLibre GL JS と `@versatiles/style` を直接使う
- Shortbread 以外のスキーマ (OpenMapTiles など) のタイルを主に使う場合
- 日本語の注記を前提にし、書体と言語の対応を確かめられていない場合

## 出典

- https://docs.versatiles.org/basics/frontend
- https://docs.versatiles.org/basics/versatiles_server
- https://docs.versatiles.org/guides/use_tiles_versatiles_org
- https://docs.versatiles.org/guides/what_about_mobile
- https://github.com/versatiles-org/versatiles-frontend
- https://github.com/versatiles-org/versatiles-style
- https://github.com/versatiles-org/node-versatiles-svelte
- https://github.com/versatiles-org/maplibre-versatiles-styler
- https://github.com/versatiles-org/versatiles-map-editor
- 2026-11-16 に gh で取得したリリースとライセンス

## 未確認のこと

- 同梱の 10 書体の一覧とライセンス、日本語の字形を含む書体の有無
- `@versatiles/style` の `text.language` が日本語を受けるか
- OpenMapTiles スキーマのタイルで `omt()` のスタイルが動くか
- 同梱の MapLibre GL JS の版 (リリースノートに記載があるとされるが読んでいない)
- tar の差し替えによる無停止の更新
