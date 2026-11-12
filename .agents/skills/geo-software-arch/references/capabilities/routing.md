# ルート検索

対象: 経路、所要時間、到達圏 (isochrone)、距離行列

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |

## 3 つの型

この機能を実現する型は 3 つある: 外部の API、常駐するルートサーバー (Valhalla、OSRM、GraphHopper など)、ファイルと関数 (ルート用のグラフを 1 ファイルにして関数や端末で引く)。

| 型 | 主なツール・サービス (版、ライセンス) | 保存の置き場所 | 計算の置き場所 | 表現 (応答の形式) | 出典 |
|---|---|---|---|---|---|
| 外部の API | 地図事業者の経路 API と距離行列 API (例として大手地図プラットフォームの Routes API。経路は要求 1 件ごと、距離行列は要素 = 出発地数 × 目的地数ごとに課金され、1 要求あたり標準 625 要素、交通状況を考慮する設定や公共交通では 100 要素が上限)。ライセンスは各社の利用規約による | 提供者のクラウド | 提供者のクラウド | HTTP の JSON (経路の折れ線、所要時間、距離、行列) | https://developers.google.com/maps/documentation/routes/usage-and-billing |
| 常駐するサーバー | Valhalla 3.9.1 (2026-10-06 公開、MIT。route、optimized route、matrix、isochrone、map matching、elevation など。GTFS による multimodal 経路も持つ)、OSRM v26.11.0 (2026-11-01 公開、BSD-2-Clause。route、nearest、table、match、trip、tile。isochrone は API に無い)、GraphHopper 11.1 (2026-09-29 公開、Apache-2.0。/route、/isochrone、/spt と GTFS による公共交通)、OpenTripPlanner v2.10.0 (2026-09-09 公開、LGPL-3.0 以降。GTFS と OSM PBF から公共交通を含む経路を引き、GTFS GraphQL API と Transmodel GraphQL API を出す) | サーバーのディスクとメモリ (前処理したグラフ) | 常駐プロセス (VM、コンテナ) | HTTP の JSON、GraphQL (OTP)、ベクトルタイル (OSRM tile) | https://github.com/valhalla/valhalla 、 https://valhalla.github.io/valhalla/api/ 、 https://github.com/Project-OSRM/osrm-backend 、 https://project-osrm.org/docs/v5.24.0/api/ 、 https://github.com/graphhopper/graphhopper 、 https://github.com/graphhopper/graphhopper/blob/master/docs/web/api-doc.md 、 https://github.com/opentripplanner/OpenTripPlanner 、 https://docs.opentripplanner.org/en/latest/Basic-Tutorial/ |
| ファイルと関数 | Valhalla のタイル tar (valhalla_build_extract で作る) を pyvalhalla (Python 3.12 以上の abi3 wheel) の `get_config(tile_extract=...)` で開き `Actor` で引く。Valhalla は `mjolnir.tile_url` で HTTP からタイルを読める。Rati (Apache-2.0) は S3 かローカルの tar から Range 読みでタイルを 1 枚ずつ返す小さなサーバー。OSRM の Node.js バインディング (@project-osrm/osrm、読み取り専用)。ブラウザでは route_snapper 0.4.9 (Rust を Wasm にしたもの、Apache-2.0) や Valhalla を Wasm にした小規模な npm パッケージ (v0.1.2、MIT) がある。端末内では OsmAnd (コードは GPLv3) と Organic Maps (Apache-2.0) がオフラインで経路を引く | オブジェクトストレージ上の tar、関数のローカルディスク、端末のストレージ | 短命な関数、ブラウザ、端末 | 関数が返す JSON、端末内の描画 | https://valhalla.github.io/valhalla/bindings/python/ 、 https://github.com/valhalla/valhalla/blob/master/scripts/valhalla_build_config 、 https://github.com/valhalla/rati 、 https://github.com/Project-OSRM/osrm-backend#using-the-nodejs-bindings 、 https://github.com/dabreegster/route_snapper 、 https://www.npmjs.com/package/@jansoft/mbujkanji-valhalla-wasm 、 https://github.com/osmandapp/OsmAnd 、 https://github.com/organicmaps/organicmaps |

## 置き場所ごとの実現手段

| 置き場所 | 実現手段 (ツール、形式、API) | 制約 (データの大きさ、メモリ、起動時間、更新) | 出典 |
|---|---|---|---|
| クラウド | 常駐の Valhalla、OSRM、GraphHopper、OTP。短命な関数で Valhalla の tar や OSRM のデータを読む形もとれる (関数のメモリは 128 MB から 10,240 MB、実行は最長 900 秒、/tmp は 512 MB から 10,240 MB、コンテナイメージは最大 10 GB) | 全球の OSRM は car で実行時に約 123 GiB の RAM (v5.26、2021-11 の planet での目安)。GraphHopper の全球取り込みは約 60 GB の RAM (MMAP で 31 GB に減るが数日かかる)、CH の準備は約 120 GB。関数で全球のグラフを丸ごと持つのは無理で、国単位の tar を /tmp に置くか、`mjolnir.tile_url` で必要なタイルだけ取る形になる (推測) | https://github.com/Project-OSRM/osrm-backend/wiki/Disk-and-Memory-Requirements 、 https://github.com/graphhopper/graphhopper/blob/master/docs/core/deploy.md 、 https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html |
| エッジ (CDN のエッジ関数、利用者の近くに置く小さなサーバー) | Valhalla のタイル tar を Rati のような Range 読みの配信で CDN に載せ、端末や Valhalla 本体が `tile_url` で 1 枚ずつ取る。Rati の README はこれを CDN 向けの経路タイル先読み (オフライン案内用) と、全球 tar を落とさずに起動する用途として挙げている | 代表的なエッジ関数はアイソレートあたり 128 MB (JS ヒープと Wasm を含む)、スクリプトは非圧縮 64 MiB まで、CPU 時間は無料枠で 10 ms、有料で最長 5 分。経路計算そのものをエッジ関数で回すのは国単位でもメモリが足りない見込みで、エッジはタイル配信に向く (推測) | https://github.com/valhalla/rati 、 https://developers.cloudflare.com/workers/platform/limits/ |
| ブラウザ | Wasm にした経路エンジン (route_snapper、Valhalla の Wasm 版パッケージ) を Web Worker で動かし、グラフを OPFS や Cache に置く。browser/ の reference の Wasm、Worker、OPFS の項と結びつく | Wasm のメモリは 4 GB が上限で、ブラウザはさらに低く制限しうる (DuckDB-Wasm の文書の記述)。route_snapper は線を道路網に沿わせて描く用途で、汎用の経路サービスの代わりではない。Valhalla の Wasm 版は利用者が Docker で自分でビルドする前提の小規模パッケージで、成熟した選択肢とは言えない | https://duckdb.org/docs/2.0/clients/wasm/overview.html 、 https://github.com/dabreegster/route_snapper 、 https://www.npmjs.com/package/@jansoft/mbujkanji-valhalla-wasm |
| アプリ (ネイティブ、端末内) | OsmAnd と Organic Maps は事前に落とした地図データで車、自転車、徒歩の経路を端末内で引く。Valhalla は階層タイル構造でメモリの少ない端末とオフライン経路と地域抽出を設計目標に掲げる。GraphHopper は過去に Android 版のデモを出していた (1.0 まで) | 端末のストレージに地域単位のデータを落とす。データ更新はアプリ側の地図更新に依存する | https://github.com/osmandapp/OsmAnd 、 https://github.com/organicmaps/organicmaps 、 https://github.com/valhalla/valhalla 、 https://github.com/graphhopper/graphhopper |

## データの大きさの目安

国、都道府県、市区町村の範囲で、索引やファイルがどれくらいの大きさになるか。公式の記述か、測った条件つきで書く。

- 入力の OSM PBF: 日本全体 2.4 GB (Geofabrik、2026-11-08 時点のデータ)。地方別は関東 499 MB、中部 495 MB、近畿 339 MB、九州 302 MB、東北 297 MB、中国 228 MB、北海道 181 MB、四国 87 MB。都道府県と市区町村の単位は Geofabrik の配布に無い。出典 https://download.geofabrik.de/asia/japan.html
- OSRM の全球 (v5.26、2021-11 の planet、PBF 61 GiB): 前処理は car で extract 415 GiB、partition 220 GiB、customize 174 GiB、contract 230 GiB のメモリ、生成物のディスクは約 300 GB、実行時の RAM は約 123 GiB。小さい抽出は入力の大きさにほぼ比例し、foot は car より重い。出典 https://github.com/Project-OSRM/osrm-backend/wiki/Disk-and-Memory-Requirements
- 比例の記述から日本全体 (2.4 GB) の OSRM car の実行時 RAM を見積もると数 GiB 程度になる (推測。61 GiB で 123 GiB という比を当てただけで、測っていない)
- GraphHopper の全球: 取り込み約 60 GB の RAM で約 3 時間、MMAP なら 31 GB、CH は約 120 GB、LM は約 80 GB。出典 https://github.com/graphhopper/graphhopper/blob/master/docs/core/deploy.md
- Valhalla の全球タイル tar はおよそ 80 GB (Rati の README の記述)。出典 https://github.com/valhalla/rati
- OpenTripPlanner は Portland の TriMet のデータで最低 1 GB のメモリ、大きな入力では数 GB が要る。出典 https://docs.opentripplanner.org/en/latest/Basic-Tutorial/

## 判断を左右すること

- 更新頻度: 自前のエンジンはどれも OSM PBF からグラフを前処理し直す必要があり、全球では前処理に数時間から 1 日以上かかる (GraphHopper の全球取り込み約 3 時間、CH の準備は car で約 25 時間)。日本だけなら入力が全球の 25 分の 1 程度なので、日次の作り直しも現実的な範囲になる (推測)。外部 API は更新を提供者が持つ
- 応答の速さ: OSRM は `--mmap` でデータファイルを直接マップでき、追加のメモリを使わずに起動できる。Valhalla は tar を mmap して読む (graphreader.h のコメントに「mmapped extract」とある)。短命な関数で毎回グラフを開く場合、起動時間は tar の取得と mmap の速さで決まる (推測)
- オフラインで使いたいか: 端末内で経路を引くなら OsmAnd、Organic Maps のようなアプリか、Valhalla のタイルを端末に落とす形になる。ブラウザ内の経路は成熟した選択肢が少ない
- 費用 (外部 API の課金単位、自前の計算と転送): 外部 API は経路が要求単位、距離行列が要素単位の課金が例としてある (行列は出発地 × 目的地で一気に膨らむ)。自前は常駐サーバーのメモリが主な費用で、全球の OSRM は 100 GiB 超の RAM を常時持つ。到達圏が要るなら OSRM は API に isochrone が無いので Valhalla か GraphHopper を選ぶ。公共交通 (GTFS) が要るなら OTP、Valhalla の multimodal、GraphHopper の GTFS 読み込みが候補

## ライセンス上の注意

コピーレフトのツール (GPL、AGPL など) と、データの継承条件 (ODbL など) を、組み込み、改変、配布、SaaS 提供のそれぞれで書く。

- Valhalla (MIT)、OSRM (BSD-2-Clause)、GraphHopper (Apache-2.0)、Rati と route_snapper (Apache-2.0)、Organic Maps (Apache-2.0): 組み込み、改変、配布、SaaS 提供のいずれも、著作権表示とライセンス文を残せば自由。Apache-2.0 は改変したファイルに変更の旨を示すこと、NOTICE の継承が要る
- OpenTripPlanner (LGPL-3.0 以降): 改変せずにサーバーとして動かし SaaS で応答を返すだけなら、ソースの開示義務は生じない (LGPL は AGPL と違いネットワーク越しの提供を配布とみなさない)。OTP 自体を改変して配布する場合は改変部分を LGPL で出す。OTP をライブラリとして自社製品に組み込んで配布する場合は、利用者が OTP 部分を差し替えられる形 (動的リンクや再リンク可能な形) にする必要がある
- OsmAnd (コードは GPLv3、アートワークは CC BY-NC-ND 4.0、一部は独占ライセンス): コードを組み込んだアプリを配布すると、アプリ全体を GPLv3 でソース公開する義務が出る。SaaS としてサーバー側で動かすだけなら GPLv3 の配布には当たらない。アートワークは非営利かつ改変禁止なので、商用アプリに流用できない
- OSM データ (ODbL): 経路グラフは OSM から作った派生データベースにあたる。グラフそのものを公開、配布する場合は ODbL で出す必要がある。経路の結果や地図画像のように元データの抽出を目的としない出力は Produced Work として扱われうるが、その場合も OSM の帰属表示と ODbL である旨の明示が要る。経路の応答 (折れ線と案内文) が Produced Work にあたるかを OSMF の指針は明示していない
- 外部 API: 応答の保存期間、キャッシュ、他社地図への重ね表示に規約上の制限があることが多い。採用前に利用規約を読む

## 出典

- https://github.com/valhalla/valhalla (MIT であること、3.9.1 の公開日、階層タイル構造の設計目標、pyvalhalla の提供)
- https://valhalla.github.io/valhalla/api/ (Valhalla のエンドポイント一覧、GTFS による multimodal)
- https://valhalla.github.io/valhalla/bindings/python/ (pyvalhalla で tile_extract の tar を開く方法、Python 3.12 以上の wheel)
- https://github.com/valhalla/valhalla/blob/master/scripts/valhalla_build_config (tile_extract、tile_dir、tile_url、max_cache_size の設定)
- https://github.com/valhalla/valhalla/blob/master/valhalla/baldr/graphreader.h (tar を mmap した extract から読むこと)
- https://github.com/valhalla/rati (Range 読みでタイルを返すサーバー、全球 tar 約 80 GB の記述、Apache-2.0)
- https://github.com/Project-OSRM/osrm-backend (BSD-2-Clause、v26.11.0、Node.js バインディング) と https://github.com/Project-OSRM/osrm-backend/blob/master/src/tools/routed.cpp (`--mmap` オプション)
- https://project-osrm.org/docs/v5.24.0/api/ (OSRM のサービス一覧に isochrone が無いこと)
- https://github.com/Project-OSRM/osrm-backend/wiki/Disk-and-Memory-Requirements (全球の前処理と実行時のメモリ)
- https://github.com/graphhopper/graphhopper (Apache-2.0、11.1、GTFS、Android デモの履歴、ホスト型の Matrix API の存在)
- https://github.com/graphhopper/graphhopper/blob/master/docs/web/api-doc.md (/route、/isochrone、/spt)
- https://github.com/graphhopper/graphhopper/blob/master/docs/core/deploy.md (全球取り込みのメモリと時間)
- https://github.com/opentripplanner/OpenTripPlanner (LGPL-3.0 以降、v2.10.0)
- https://docs.opentripplanner.org/en/latest/Basic-Tutorial/ (GTFS と OSM PBF の入力、Java 25、メモリの目安、GraphQL API)
- https://github.com/osmandapp/OsmAnd (GPLv3 と CC BY-NC-ND 4.0、オフライン経路)
- https://github.com/organicmaps/organicmaps (Apache-2.0、オフラインの経路案内、最新リリース 2026.09.29)
- https://github.com/dabreegster/route_snapper と https://www.npmjs.com/package/route-snapper (Wasm の経路、0.4.9、Apache-2.0)
- https://www.npmjs.com/package/@jansoft/mbujkanji-valhalla-wasm (Valhalla の Wasm 版パッケージ、v0.1.2、MIT)
- https://developers.google.com/maps/documentation/routes/usage-and-billing (外部 API の課金単位と行列の要素上限の例)
- https://download.geofabrik.de/asia/japan.html (日本と地方別の PBF の大きさ)
- https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html (関数のメモリ、時間、/tmp、イメージの上限)
- https://developers.cloudflare.com/workers/platform/limits/ (エッジ関数のメモリ、CPU 時間、スクリプトの大きさ)
- https://duckdb.org/docs/2.0/clients/wasm/overview.html (Wasm のメモリ上限 4 GB の記述)
- https://www.openstreetmap.org/copyright と https://osmfoundation.org/wiki/Licence/Community_Guidelines/Produced_Work_-_Guideline (ODbL の帰属、継承、Produced Work の定義)

## 未確認のこと

- 日本全体と都道府県単位での Valhalla タイル tar、OSRM、GraphHopper のグラフの実寸と実行時メモリ (公式の数字が無く、測っていない)
- pyvalhalla のバインディングから isochrone と matrix を直接呼べるか (文書は route の例だけ)
- GraphHopper のオープンソース版に距離行列のエンドポイントがあるか (API 文書に記載が無く、README はホスト型の Matrix API を別に挙げている)
- OSRM の全球の数字は v5.26 と 2021-11 の planet のもので、v26.11.0 と現在の planet での値
- OpenTripPlanner で日本全国の GTFS を読み込んだときのメモリ
- Valhalla を Emscripten で Wasm にした公式のビルドがあるか (見つかったのは第三者の小規模パッケージだけ)
- 外部 API 各社の経路と行列の具体的な単価
- 経路の応答が ODbL の Produced Work にあたるかの公式な見解
