# kepler.gl

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | v3.2.6 (2026-03-16)。以後は v3.3.0-alpha 系のみで、最新は v3.3.0-alpha.20 (2026-11-08)。npm の `latest` タグも 3.3.0-alpha.20 を指している |
| リポジトリ | https://github.com/keplergl/kepler.gl |
| ドキュメント | https://docs.kepler.gl/ |
| ライセンス (LICENSE ファイルで確かめる) | MIT (LICENSE の本文で確認。著作権表示は「Copyright contributors to the kepler.gl project」) |
| 運営主体 | OpenJS Foundation のプロジェクト (Open Visualization collaboration space)。Uber で生まれ、2019 年に Urban Computing Foundation、2022 年に OpenJS Foundation へ移った (https://openjsf.org/blog/openjs-world-2022-openjs-foundation-welcomes-urban-computing-foundation-vis-gl-and-kepler-gl) |

## 概要

kepler.gl は大量の位置データを可視化して探索するための Web アプリケーションで、MapLibre GL と deck.gl の上に作られている (https://github.com/keplergl/kepler.gl)。数百万点の描画や、その場での空間集計ができると README は説明している。同時に Redux で状態を管理する React コンポーネントでもあり、自分の React-Redux アプリに組み込める。つまり単体の分析ツールとしても、プロダクトに組み込む部品としても使える。

## 下にある描画ライブラリ

- deck.gl (データレイヤーの描画) と MapLibre GL JS (ベースマップ)。既定のベースマップは MapLibre で、Mapbox がホストするスタイルだけを使うなら `mapbox-gl` を入れる (https://github.com/keplergl/kepler.gl)。
- ドキュメントの一部には「Mapbox アクセストークンが必要」という古い記述が残っており (https://docs.kepler.gl/)、HTML 書き出しの説明も Mapbox トークンを前提にしている (https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/k-save-and-export.md)。

## 最初から手に入るもの

- UI (レイヤー一覧、凡例、検索、時間スライダーなど): レイヤーパネル、フィルター、時間再生 (playback)、ツールチップ、ブラッシング、座標表示、ベースマップのスタイル切り替え、凡例付きの画像書き出しがある (https://docs.kepler.gl/docs/user-guides)。レイヤーの種類は Point、Arc、Line、Grid、Polygon、Cluster、Icon、Hexbin、Heatmap、H3、Trip、S2、ベクトルタイル、ラスタータイル、WMS。master のドキュメントには SQL データエクスプローラー、注記、地図上の描画、AI アシスタントの項目もある (https://github.com/keplergl/kepler.gl/tree/master/docs/user-guides)。
- データの読み込み (対応形式、データカタログ): CSV、GeoJSON、GeoJSONL/NDJSON、KML、GPX、TCX、Shapefile、Excel、FlatGeobuf、GeoArrow、Parquet、それらの zip、kepler.gl の JSON。ローカルファイル、URL (CORS 設定が必要)、サンプルデータから読み込む。座標系は WGS84 (Web Mercator 表示) のみ。ファイルはブラウザ内で解析されるため、扱える大きさはメモリで決まり、収まらないデータにはタイルセットを使うよう案内している (https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/b-kepler-gl-workflow/a-add-data-to-the-map.md)。データカタログ機能は無い。この一覧は master ブランチのドキュメントで、未リリースの 3.3 系の内容を含みうる。
- 共有・埋め込み: 画像、CSV (フィルター後のデータも可)、単体で動く HTML、設定とデータを含む JSON、動画として書き出せる。デモアプリからは Dropbox 経由の公開 URL 共有もできる (https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/k-save-and-export.md)。自分のアプリには React コンポーネントとして埋め込むか、UMD ビルドを script タグで読み込む (https://github.com/keplergl/kepler.gl)。Jupyter 用ウィジェット `keplergl` (PyPI 最新 0.4.0) もある (https://pypi.org/project/keplergl/)。
- 開発せずに使えるか (ノーコード / 設定ファイル / コードが必要): 公式のデモアプリ https://kepler.gl/demo はブラウザだけで使え、データはブラウザ外に送られないと説明されている。自分のプロダクトに組み込むには React と Redux のコードが必要。

## 縛りになること

- カスタマイズの限界: テーマ、地図スタイル、コンポーネントの差し替え (component injection)、多言語化で見た目を変えられる (https://docs.kepler.gl/)。ただし状態は kepler.gl 独自の Redux reducer に載せる必要があり、アプリ側の状態管理もこれに合わせることになる (https://github.com/keplergl/kepler.gl)。保存される設定は `dataId` でデータセットと結びついており、設定だけを別のデータに使い回すには ID をそろえる必要がある (https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/k-save-and-export.md)。
- 必要なサーバー・インフラ: kepler.gl 自体はクライアントだけで動き、サーバーは不要 (https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/k-save-and-export.md)。地図の保存・共有を自前で提供するなら、保存先 (クラウドストレージ連携や自前 API) を用意する。ブラウザのメモリを超えるデータには別途タイル配信が要る。

## ライセンスと費用

- OSS 版のライセンス: MIT (https://github.com/keplergl/kepler.gl/blob/master/LICENSE)。Mapbox のスタイルを使う場合は Mapbox の料金と規約が別にかかる。
- 提供元のホスティング版・有償版と料金: OSS としての有償版は無い。デモアプリ https://kepler.gl/demo は無料で使える。別製品として Foursquare が「Powered by Kepler.gl & DuckDB」とうたう FSQ Spatial Desktop を提供しており、Basic は 2026 年中 $0/月、Standard は $25/月、Pro は $100/月 (米ドル表記、ユーザー単位かは記載なし。https://foursquare.com/pricing/ 、2026-11-10 確認)。これは kepler.gl プロジェクトのホスティング版ではなく、Foursquare の製品である。

## 実例

- kepler.gl デモアプリ: https://kepler.gl/demo
- Jupyter ウィジェット: https://pypi.org/project/keplergl/ (ソースは同リポジトリの `bindings/python`)
- Foursquare の FSQ Spatial Desktop: https://foursquare.com/products/spatial-desktop/

## 開発の活発さ

- 直近 1 年のリリース数: 27 件 (2025-11-10 以降の GitHub Releases)。内訳は安定版 5 件 (v3.2.2 から v3.2.6)、v3.3.0-alpha 系 21 件 (alpha.0 から alpha.20)、skill-v0.0.1 が 1 件。
- 最終コミット日: 2026-11-09 (master)。

## 環境の違いと保守

- ブラウザ間の互換: 文書でうたう対応ブラウザの一覧は見つからなかった (未確認)。CI は ubuntu-latest の上で Jest と tape のテストを `xvfb-run` で回す (https://github.com/keplergl/kepler.gl/blob/master/.github/workflows/test.yml)。tape の「browser」のテストは jsdom の上で動く (`test/js-dom.js`、https://github.com/keplergl/kepler.gl/blob/master/package.json)。実ブラウザを動かす `test-headless` (`test/browser-drive.js`) のスクリプトはあるが CI の手順には無く、puppeteer を入れる手順はコメントアウトされている (同、https://github.com/keplergl/kepler.gl/blob/master/.github/workflows/test.yml)。つまり CI で実ブラウザの描画は確かめていない。Firefox で NYC タクシーのデモが描画されない不具合 (#822) や Firefox での Dropbox アップロードの修正のように、ブラウザ固有の不具合は個別に直されてきた (https://github.com/keplergl/kepler.gl/issues/822 、https://github.com/keplergl/kepler.gl/blob/master/CHANGELOG.md)。
- OS 間の互換: OS ごとの動作確認の記述は見つからなかった (未確認)。`windows` ラベルはあるが付いた Issue は 1 件である (`repo:keplergl/kepler.gl is:issue label:windows`、2026-11-12 検索)。モバイルでは 3.3.0-alpha.1 (2026-06-01) にヒートマップのレイヤーがモバイルで落ちる不具合の修正が 2 件入っている (https://github.com/keplergl/kepler.gl/blob/master/CHANGELOG.md)。メモリについて FAQ は、ファイルの大きさの上限は設けておらず、ブラウザで読むので使えるメモリが上限になり、大きなファイルはタブを固めたり落としたりすると書き、メモリに収まらないデータはタイル (ベクトルタイル、COG、PMTiles) にするよう勧めている (https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/i-FAQ.md)。
- 操作の網羅: 地図の操作は下の deck.gl と MapLibre GL JS (または Mapbox GL JS) に任せている (推測、依存は https://github.com/keplergl/kepler.gl/blob/master/package.json)。kepler.gl 自身の文書で、キーボード操作、タッチの身ぶり、ページのスクロールとの両立を説明したものは見つからなかった (未確認)。
- エッジケースへの対応: GPU のコンテキストの喪失については、地図を分割、統合するたびに WebGL のコンテキストが漏れる不具合 (#1492) が解決済みで、ベースマップやレイヤーのコンテキストの喪失を検知して再読み込みのボタンを出す提案 (#1272) は未解決である (https://github.com/keplergl/kepler.gl/issues/1492 、https://github.com/keplergl/kepler.gl/issues/1272)。日付変更線は Issue の検索で「antimeridian」「dateline」とも 0 件で、扱いは未確認 (`repo:keplergl/kepler.gl is:issue`、2026-11-12 検索)。読み込みの再試行とオフラインは未確認。
- 継続的な保守: deck.gl、luma.gl、loaders.gl の更新に追随しており、deck.gl 9.2 への更新 (#3271) と 9.3.1 への更新後の退行の修正 (#3396) が変更履歴にある (https://github.com/keplergl/kepler.gl/blob/master/CHANGELOG.md)。CSP の文書は見つからなかった (未確認)。ブラウザ別のラベルは無い (https://github.com/keplergl/kepler.gl/labels)。Issue で「safari」を含むものは 195 件 (未解決 7 件) あるが、不具合報告の雛形のブラウザ欄に書かれた分を含むため、Safari 固有の不具合の数ではない (推測) (`repo:keplergl/kepler.gl is:issue safari`、2026-11-12 検索)。

## 向いている場面

- 大量の点、移動軌跡、OD データなどを分析者が手早く可視化し、フィルターや時間再生で探索したいとき。
- データを外部サーバーに送らずにブラウザ内だけで分析したいとき。
- React-Redux のアプリに、完成された分析画面を部品として組み込みたいとき。
- 分析結果を単体 HTML や画像、動画として配りたいとき。

## 向いていない場面

- 一般利用者向けの軽い地図アプリ (店舗地図など)。分析ツールとしての UI が前面に出るうえ、バンドルも大きくなる (推測)。
- ブラウザのメモリに載らない規模の生データをそのまま扱いたいとき。タイル化などの前処理が要る。
- WGS84 以外の座標系のデータを扱うとき。
- 安定版だけを追いたいとき。2026-03 以降は alpha 版しか出ておらず、npm の `latest` も alpha を指している。

## 出典

- https://github.com/keplergl/kepler.gl
- https://github.com/keplergl/kepler.gl/blob/master/LICENSE
- https://github.com/keplergl/kepler.gl/releases
- https://github.com/keplergl/kepler.gl/tree/master/docs/user-guides
- https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/b-kepler-gl-workflow/a-add-data-to-the-map.md
- https://github.com/keplergl/kepler.gl/blob/master/docs/user-guides/k-save-and-export.md
- https://docs.kepler.gl/
- https://docs.kepler.gl/docs/user-guides
- https://docs.kepler.gl/contributing/code_of_conduct
- https://kepler.gl/demo
- https://www.npmjs.com/package/kepler.gl
- https://pypi.org/project/keplergl/
- https://openjsf.org/blog/openjs-world-2022-openjs-foundation-welcomes-urban-computing-foundation-vis-gl-and-kepler-gl
- https://foursquare.com/pricing/
- https://foursquare.com/products/spatial-desktop/

## 未確認のこと

- 現在の主なメンテナーの所属: OpenJS Foundation 配下であることは確かめたが、コミッターの所属企業を一次情報で確かめていないため。
- 対応形式の一覧のうち、Parquet など一部が安定版 v3.2.6 で使えるか: 確かめた一覧は master ブランチのドキュメントで、未リリースの 3.3 系の内容を含む可能性があるため。
- FSQ Spatial Desktop の料金がユーザー単位か: 料金ページに記載が無いため。
