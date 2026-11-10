# データの大きさの測り方

対象: PMTiles の範囲とズームを絞った大きさ (`pmtiles extract --dry-run`)、GeoJSON の大きさと圧縮、GeoParquet、検索の索引、ルート検索のグラフの大きさと、作るときのメモリと時間の測り方

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

実測は 2026-11-11 に行った。道具の版は go-pmtiles 1.30.3、Python 3.12.2 (標準の `gzip` モジュール、圧縮レベル 9)。

## 概要

データの大きさは置き場所を決める。端末に同梱できるか、ブラウザが 1 回で読めるか、オブジェクトストレージの保存料がいくらか、生成にどれだけの計算機が要るかが、この値で変わる ([cloud-native-formats](../../map-compare-arch/references/formats/cloud-native-formats.md) の「置き場所との関係」)。この文書は、対象範囲とズームを絞った PMTiles の大きさ、ブラウザに直接読ませる GeoJSON の大きさ、索引やグラフを作るときの資源を、条件をそろえて測る手順を書く。全球や国、都県の PMTiles の大きさの目安は、map-compare-arch の [capabilities/tiles](../../map-compare-arch/references/capabilities/tiles.md) の「データの大きさの目安」にあるので、ここでは繰り返さない。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| `pmtiles show` | PMTiles の版、ズーム範囲、タイル数、圧縮方式、メタデータを、ヘッダーとメタデータだけ読んで見る。URL を直接渡せる | ファイル全体の大きさは出ない (HTTP の Content-Length で見る) | go-pmtiles 1.30.3 で実測 | https://docs.protomaps.com/pmtiles/cli |
| `pmtiles extract --dry-run` | 大きな PMTiles から `--bbox` か `--region` (GeoJSON の多角形) と `--maxzoom` で切り出したときの大きさを、タイルを取らずに計算する | 範囲の内部ディレクトリは読みに行くので、リモートのファイルでも数十件のリクエストが出る (下の実測で 17〜51 件) | go-pmtiles 1.30.3 (`--dry-run` は `pmtiles extract --help` で確かめた) | https://docs.protomaps.com/pmtiles/cli |
| `pmtiles verify` | 作った PMTiles の並びとヘッダーが正しいかを確かめる | 中身の地物の正しさは見ない | go-pmtiles | https://docs.protomaps.com/pmtiles/cli |
| ファイルの大きさと gzip の大きさ | GeoJSON をそのまま配るときの転送量を見積もる。座標の桁を落としたとき、空白を除いたときの差を見る | 配信の圧縮方式 (gzip、Brotli) と圧縮レベルで値が変わる | Python 3.12.2 の `gzip`、`gzip` コマンド 1.12、`brotli` 1.1.0 | 下の実測 |
| 作るときの資源の計測 | タイル生成、索引の構築、グラフの構築にかかる時間、メモリの山、ディスクを測る | 入力の大きさに比例しないことがある。最初は小さい範囲で測ってから広げる | `/usr/bin/time -v` (最大常駐メモリ)、systemd-run の MemoryMax で上限を掛ける | [self-hosting](../../map-compare-arch/references/self-hosting.md) の「タイルの生成」 |

## 判断を左右すること

- ズームを 1 段上げると、大きさはおよそ 2〜3 倍になる。Protomaps は全球でズーム 1 段ごとにおよそ 2 倍と書いている ([capabilities/tiles](../../map-compare-arch/references/capabilities/tiles.md))。下の東京 23 区の実測では、z13 から z14 で 2.3 倍、z14 から z15 で 3.4 倍だった。最大ズームを決めると大きさがほぼ決まる。
- 範囲の形: 矩形の `--bbox` は海や隣の自治体を含む。行政区域の多角形を `--region` に渡すと減る (推測。下の実測は矩形だけ)。
- GeoJSON をそのまま読ませるか、タイルにするか: ブラウザは GeoJSON を全部読み込んでから描く。地物の数が少なく、座標が粗くてよいならそのままでよく、大きくなればベクトルタイルか PMTiles にする。どこで切り替えるかは、端末で描画の速さとメモリを測って決める ([render-performance](render-performance.md))。
- 座標の桁: 経緯度の小数 5 桁はおよそ 1 m、4 桁はおよそ 10 m の細かさ (緯度 1 度が約 111 km であることからの換算)。表示の目的に要る桁まで落とすと、下の実測で gzip 後の大きさが 4 割ほど減った。
- 作るときの資源: 全球のタイル生成や、広い範囲のルート検索のグラフは、メモリとディスクを数十 GB 使う。手順の時間と計算機の費用は [self-hosting](../../map-compare-arch/references/self-hosting.md) の「タイルの生成」と「費用の見積もり」にある。

## 手順

1. 何の大きさが判断を左右するかを決める: 端末への同梱 (アプリの大きさ)、ブラウザの 1 回の読み込み、ストレージの保存料、生成の計算機。
2. 対象範囲とズームを要件から決める。範囲は矩形 (`--bbox=西,南,東,北`) か、行政区域の GeoJSON (`--region`) で書く。
3. 既存の PMTiles から切り出せるなら、まず `pmtiles show <URL>` で版とズーム範囲を確かめ、`pmtiles extract <URL> out.pmtiles --bbox=... --maxzoom=N --dry-run` を N を変えて数回流す。出力の「archive size」が切り出したときの大きさになる。
4. 自前のデータなら、まず小さな標本 (1 つの区や市) で作り、大きさ、時間、メモリの山を測ってから、範囲を広げたときの値を比で見積もる。広げる前に、メモリの上限を掛けて流す (OOM で同じ機械の別のサービスを巻き込まないため)。
5. GeoJSON は、そのままの大きさ、空白を除いた大きさ、座標の桁を落とした大きさを、配信と同じ圧縮で測る。
6. 版 (データの日付、ビルドの日付)、範囲、ズーム、道具の版を添えて、map-compare-arch の判断 (同梱か配信か、GeoJSON かタイルか) に渡す。

## 実測

### PMTiles を東京 23 区の矩形で切り出した大きさ

2026-11-11 に、`https://build.protomaps.com/20261110.pmtiles` (Protomaps Basemap 4.15.2、z0〜15、Planetiler 0.10.2、OSM の差分は 2026-11-10T04:00:00Z まで) から、`--bbox=139.56,35.52,139.92,35.82` (23 区を囲む矩形。川崎市、埼玉県、千葉県の一部と東京湾を含む) で `--dry-run` を流した。go-pmtiles 1.30.3。1 回の実行は 3〜5 秒だった。

| `--maxzoom` | タイル (件) | 切り出しの大きさ | 必要なリクエスト | 前の段からの増え方 |
|---|---|---|---|---|
| 10 | 14 | 1.4 MB | 17 | |
| 12 | 53 | 5.5 MB | 24 | |
| 13 | 143 | 12 MB | 30 | 2.2 倍 (z12 から) |
| 14 | 446 | 28 MB | 41 | 2.3 倍 |
| 15 | 1,554 | 94 MB | 51 | 3.4 倍 |

z15 まで含めたときの 1 タイルの平均は約 60 KB (94 MB / 1,554) だった。タイルの件数は go-pmtiles の出力の「fetching N tiles」で、同じ中身のタイルをまとめた後の件数と考えられる (推測)。同じ範囲を z14 まで持つ OpenFreeMap のタイルは、東京駅付近で 1 枚平均約 413 KB だった ([tiles-per-view](tiles-per-view.md) の実測)。スキーマと最大ズームが違うと、同じ範囲でもタイルの大きさが桁で違う。

### GeoJSON の大きさ

examples の `seven-eleven-tokyo23/wards.geojson` (東京 23 区の境界、23 地物、頂点 3,867、国土数値情報の行政区域 2026 年版を加工したもの) を測った。

| 形 | 大きさ (B) | gzip -9 (B) | Brotli -q 11 (B) |
|---|---|---|---|
| そのまま (座標は小数 9 桁、インデントあり) | 141,099 | 39,803 | 26,561 |
| 空白を除いた | 117,679 | 36,835 | 未測定 |
| 座標を小数 6 桁に丸めた | 91,867 | 25,688 | 未測定 |
| 小数 5 桁 | 84,168 | 21,319 | 13,474 |
| 小数 4 桁 | 76,375 | 16,804 | 未測定 |

Brotli は brotli 1.1.0 の `-q 11` で測った。空白を除くだけでは gzip 後は 7% しか減らず、座標の桁を 9 桁から 5 桁に落とすと 46% 減った。圧縮して配るなら、効くのは座標の桁と頂点の数で、整形の有無ではない。

## 落とし穴

- `--dry-run` の値をダウンロードの量と取り違える: 出力の「transferred」は切り出すときに取る量で、利用者が地図を見るときの転送量ではない。利用者の転送量は [tiles-per-view](tiles-per-view.md) で測る。
- 日付つきのビルドを指定しない: `build.protomaps.com` は日ごとにファイルが入れ替わる。測った版のファイル名を書く。
- 圧縮前の大きさで比べる: ファイルの大きさと転送量は違う。PMTiles の中のタイルは gzip 済み (`pmtiles show` の tile compression) で、GeoJSON は配信の圧縮に任せることが多い。比べるときは両方とも転送時の大きさにそろえる。
- 小さな標本の値を比で延ばす: 索引やグラフは、範囲を広げると比例以上に増えることがある。2 つ以上の大きさで測って、伸び方を確かめてから延ばす。
- メモリの上限を掛けずに生成を流す: 生成ツールの必要量は事前に読めない。DuckDB の `memory_limit` のようなツール側の設定は、OS のメモリ上限の代わりにならない。

## ライセンス上の注意

- go-pmtiles は BSD-3-Clause で、道具として使う分には義務は生じない ([capabilities/tiles](../../map-compare-arch/references/capabilities/tiles.md) の出典)。
- Protomaps Basemap のタイルは OSM 由来で ODbL の帰属表示が要る。切り出した PMTiles を配るときの扱い (Produced Work か派生データベースか) は、[self-hosting](../../map-compare-arch/references/self-hosting.md) の「ライセンス上の注意」で確かめる。
- 国土数値情報の行政区域は CC BY 4.0 で、加工して使うときは出典と加工の表示が要る (map-compare-data の [ksj](../../map-compare-data/references/sources/ksj.md))。

## 出典

- https://docs.protomaps.com/pmtiles/cli (`show`、`verify`、`extract` の `--maxzoom`、`--bbox`、`--region`。2026-11-11 確認。`--dry-run` はこのページに無く、go-pmtiles 1.30.3 の `pmtiles extract --help` で確かめた)
- https://build.protomaps.com/20261110.pmtiles (2026-11-11 に `pmtiles show` と `pmtiles extract --dry-run` で測定)
- https://build-metadata.protomaps.dev/builds.json (20261110.pmtiles の大きさ 139,416,504,818 B と版 4.15.2。2026-11-11 確認)

## 未確認のこと

- `--region` に行政区域の多角形を渡したときに、矩形よりどれだけ減るか。
- 検索の索引 (全文検索、ジオコーダ) とルート検索のグラフの大きさ。この文書では測っていない。
- GeoParquet で同じ境界を持ったときの大きさ。
- CDN が実際に使う圧縮レベルで配ったときの大きさ (上の表は最大の圧縮レベル)。
