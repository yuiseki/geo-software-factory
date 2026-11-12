# 地図データとタイルの更新

対象: タイルや索引の作り直し、版ごとの別名での配置と切り替え、CDN のキャッシュの無効化、スタイルの更新と利用者側のキャッシュ

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

## 概要

外部の提供元のタイルを使うなら、データの更新は提供元の仕事で、こちらの仕事はスタイルの版と帰属表示を追うことになる。自前で配信するなら、新しいデータの取得、タイルの生成、検査、配置、参照の切り替え、キャッシュの無効化、帰属表示とデータの日付の更新までが自分の運用になる。同じ名前で上書きすると、CDN や利用者の端末に残った古い断片と新しい断片が混ざるので、版ごとに別名で置いて参照を切り替えるのが基本形である。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| 生成済みのタイルを取得する | 生成の計算機と時間を省く | 中身とスキーマは配布元が決める | Protomaps の basemap は毎日、OpenFreeMap は毎週ビルドを公開 (geo-software-arch の self-hosting、2026-11-10 確認) | [self-hosting](../../geo-software-arch/references/self-hosting.md) |
| 自分で生成する | 範囲、スキーマ、主題データを自分で決める | planet の pbf は 89GB で、生成に大きな計算機が要る | OSM の planet は毎週公開。Planetiler、tilemaker など | [self-hosting](../../geo-software-arch/references/self-hosting.md) |
| 版ごとに別名で置き、参照を切り替える | 古い索引と新しい本体が混ざるのを防ぎ、すぐに戻せる | 古い版を消すまで保存料が 2 倍かかる | PMTiles (例 `basemap-20261111.pmtiles`)、z/x/y のディレクトリ (例 `/v20261111/{z}/{x}/{y}.mvt`) | 下の手順 |
| 上書きして ETag で検出させる | URL を変えずに更新する | 強い ETag を返し、CORS で `ETag` を公開し、`If-Match` を許す設定が要る。弱い ETag (`W/`) は無視される | PMTiles JS は ETag の不一致か 416 を受けると、ブラウザのキャッシュを使わずに読み直す | PMTiles のソース、cloud-storage の文書 |
| CDN のキャッシュを消す | 古いタイルやスタイル JSON を配り続けるのを止める | 消し方と回数に上限がある | Cloudflare は Free を含む全プランで URL、ホスト名、タグ、プレフィックス、全消去が使える。Free はホスト名・タグ・プレフィックス・全消去が毎分 5 回、URL は 1 要求 100 件まで | Cloudflare purge cache |
| スタイル JSON の参照先を変える | タイルの版、スプライト、フォントを一度に切り替える | 開いたままの画面は古いスタイルのまま (推測) | MapLibre GL JS などはスタイル JSON の `sources` の URL を読む | 推測 |

## 判断を左右すること

- 更新の頻度: 道路や店舗の変化を追う必要があるか。月 1 回で足りるか、毎週か。生成済みのタイルを使えば、配布元の頻度 (Protomaps は毎日、OpenFreeMap は毎週) 以上には速くならない。
- 切り替えの単位: PMTiles 1 本なら URL の文字列を 1 か所変えるだけで済む。z/x/y を大量のファイルで置くなら、ディレクトリの接頭辞で版を分ける。
- キャッシュの有効期間: `Cache-Control` を長くするほど配信は安くなり、更新は遅れる。protomaps の Cloudflare 用 Worker の既定は `public, max-age=86400` ([edge-functions](../../geo-software-arch/references/edge/edge-functions.md))。版ごとに URL を変えるなら、タイルは長く、参照を持つスタイル JSON や TileJSON は短くする。
- スキーマの版: スタイルのパッケージとタイルのスキーマの版を合わせる必要がある (Protomaps の v4 など。[self-hosting](../../geo-software-arch/references/self-hosting.md))。データだけでなくスキーマが変わる更新は、スタイルと同時に切り替える。

## 手順

1. 新しいデータを取得するか生成する。取得したら、配布元の版と日付を記録する。
2. 検査する: ファイルの大きさが前の版から大きく変わっていないか、代表の地点 (自社の拠点、対象地域の中心) のタイルが描けるか、属性の名前が変わっていないか。PMTiles なら `pmtiles show` でヘッダーとメタデータを見る (go-pmtiles)。
3. 版ごとの別名でストレージに置く。同じ名前で上書きしない。
4. ステージングのスタイルで新しい版を参照させ、画面で確かめる。
5. 本番のスタイル JSON か TileJSON の参照を新しい版に切り替える。
6. キャッシュを消す: 参照を持つファイル (スタイル JSON、TileJSON) を URL かタグで消す。タイルを同じ URL で上書きした場合だけ、タイルのプレフィックスやホスト名で消す。全消去はゾーン全体に効くので使わない。
7. 帰属表示とデータの日付を更新する: 地図の帰属表示や「データについて」のページに、元データの版の日付 (例: OSM 2026-11-04 時点) を書いているなら書き換える。帰属表示の要件そのものは geo-software-legal-check の attribution を見る。
8. 古い版は、戻す期間 (例: 1〜2 週間) を過ぎてから消す。

## 落とし穴

- PMTiles を同じ名前で上書きすると、CDN に残った古いヘッダーや索引と新しい本体の範囲が混ざるおそれがある (推測。PMTiles JS は ETag で検出して読み直すが、CDN が強い ETag を返さないと検出できない)。
- CORS で `ETag` を公開していないと、PMTiles JS は版の違いに気付けない。Nginx の例のように `Range` だけ許して `If-Match` を許さない設定もある。
- Cloudflare Free のホスト名、タグ、プレフィックスでの消去は毎分 5 回までで、細かく何度も消すと上限に当たる。
- スタイル JSON の参照を変えても、開いたままのタブや、スタイルをアプリに同梱したモバイルアプリは古い版を読み続ける (推測)。古い版をしばらく残す理由になる。
- 外部の提供元のスタイル (Mapbox、MapTiler など) は提供元が更新するので、独自に作ったスタイルのレイヤ名や属性が、提供元のスキーマの更新で合わなくなることがある (推測)。スキーマの版を固定できるかを provider の reference で確かめる。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- OSM 由来のタイルは、更新しても ODbL の帰属表示 (OpenStreetMap への帰属と ODbL で使えることの表示) を保つ。主題データを OSM と混ぜて新しいデータベースとして配るなら継承条件が関わる。詳細は geo-software-legal-check の odbl と attribution、[self-hosting](../../geo-software-arch/references/self-hosting.md) のライセンスの節。
- OpenMapTiles スキーマのタイルは「© OpenMapTiles」の表示も要る ([self-hosting](../../geo-software-arch/references/self-hosting.md))。生成の道具やスキーマを替えたら、表示も見直す。

## 出典

- https://github.com/protomaps/PMTiles/blob/main/js/src/index.ts (ETag の不一致か 416 で読み直す、弱い ETag を無視する。2026-11-11 に main を取得)
- https://docs.protomaps.com/pmtiles/cloud-storage (CORS で `range` と `if-match` を許し、`etag` を公開する例。2026-11-11)
- https://developers.cloudflare.com/cache/how-to/purge-cache/ (全プランで URL、ホスト名、タグ、プレフィックス、全消去。プランごとの回数の上限。2026-11-11)
- [self-hosting](../../geo-software-arch/references/self-hosting.md) (planet は毎週、Protomaps は毎日、OpenFreeMap は毎週。別名で置く手順。2026-11-10 確認の値)

## 未確認のこと

- 主要な CDN (CloudFront、Fastly など) で、Range 要求の応答が版をまたいで混ざる条件。
- MapLibre GL JS がスタイル JSON をブラウザの HTTP キャッシュに従ってどれだけ保持するか (ライブラリ側の独自キャッシュの有無)。
- 外部の提供元が、スタイルやスキーマの版を固定する手段を持つか (Mapbox のスタイルの版、MapTiler の v4 など、提供元ごとに未確認)。
