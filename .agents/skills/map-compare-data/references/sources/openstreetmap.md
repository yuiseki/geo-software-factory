# OpenStreetMap のデータ

対象: OSM の地物データ (planet、地域の抽出、Overpass API)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 提供者 | OpenStreetMap Foundation (OSMF) が配布する。データは世界の貢献者が編集したもの |
| 配布ページ | planet: https://planet.openstreetmap.org/ 、地域の抽出 (第三者): https://download.geofabrik.de/ 、日本: https://download.geofabrik.de/asia/japan.html |
| 利用規約・ライセンス | Open Database License (ODbL) 1.0。著作権と出典表示の説明は https://www.openstreetmap.org/copyright |

## 概要

OpenStreetMap は、貢献者が編集する世界規模の地物データベースである。道路、建物、POI、行政界、土地利用などを、ノード、ウェイ、リレーションと自由形式のタグ (キーと値) で表す。全体のダンプ (planet) は毎週出ており、差分は分単位で出る。データは ODbL 1.0 で、派生データベースを公に使うときは同じライセンスでの提供が求められる。

## 収録範囲と詳しさ

| 項目 | 値 | 出典 |
|---|---|---|
| 地域 | 全世界。日本の抽出は Geofabrik が全国と 8 地方 (北海道、東北、関東、中部、近畿、中国、四国、九州) で配っている | https://download.geofabrik.de/asia/japan.html |
| 主なテーマ・レイヤー | タグで決まるため固定のレイヤーはない。日本の抽出での件数は `building` 31,199,146、`amenity` 1,442,211、`addr:block_number` 325,404、`addr:housenumber` 262,105 (いずれもオブジェクト数、2026-11-10 05:44 JST 時点のデータ) | https://taginfo.geofabrik.de/asia:japan/ の API (`/api/4/key/stats`) |
| 件数・大きさの目安 | planet の PBF は 89 GB (`planet-261102.osm.pbf`)。日本全体の PBF は 2.4 GB、地方別は 87 MB (四国) から 499 MB (関東) | https://planet.openstreetmap.org/pbf/ 、https://download.geofabrik.de/asia/japan.html |
| 位置の精度・縮尺 | 公式の精度規定は確認できなかった。貢献者がどの画像や現地調査を元に描いたかで変わる (推測) | 未確認 |
| 時点と更新頻度 | planet は毎週の完全版。差分は `replication/` に `minute/`、`hour/`、`day/` がある。Geofabrik の日本抽出は確認時点で 2026-11-09 06:21 JST までのデータで、`.osc.gz` の差分も置かれている (Geofabrik のページに更新頻度の明記はない) | https://planet.openstreetmap.org/ 、https://planet.openstreetmap.org/replication/ 、https://download.geofabrik.de/asia/japan.html |

## 形式と取得方法

- 配布形式 (Shapefile、GeoJSON、GeoParquet、PMTiles、CSV など): planet は PBF と XML。Geofabrik の日本の地方別は `.osm.pbf` と `.gpkg.zip`。日本全体の Shapefile (`japan-latest-free.shp.zip`) は「この地域では提供していない、地方別を使え」と表示される。
- 取得方法 (一括ダウンロード、API、範囲を絞った取得): planet の一括取得 (89 GB)、Geofabrik の地域抽出、Overpass API (範囲とタグを絞って取得)。公開の overpass-api.de の目安は「1 日あたり約 10,000 リクエスト、ダウンロード量 約 1 GB/日以下」で、既定の実行時間上限 180 秒、メモリ 512 MiB、超過時は HTTP 429 や 504 が返る。それ以上の需要は自前インスタンスを勧めている。編集用 API (api.openstreetmap.org) は読み取り目的の大量取得に使ってはならず、大量利用は planet などを使うよう求められている。
- 座標参照系: 公式ページでの明記は確認できなかった。OSM のノードは緯度経度で持つ。WGS84 (EPSG:4326) とする説明が一般的だが、本調査では公式文書で確かめていない (推測)。

## ライセンスと出典表示

- ライセンス: ODbL 1.0 (2012-09-12 以降に公開されたファイル)。地図の文書類は CC BY-SA 2.0 で、データとは別である。
- 出典表示の書き方 (公式の例): OSMF の Attribution Guidelines (2021-06-25 理事会採択) は、「OpenStreetMap」へのクレジットと、データが ODbL で使えることの明示を求める。「OpenStreetMap」を https://www.openstreetmap.org/copyright へのリンクにすることがその方法の一つ。従来の「© OpenStreetMap contributors」も可。対話型の地図では四隅のどこかに置くのが典型で、操作後や 5 秒後に畳んでもよいが「(i)」ボタンなどから見つけられる必要がある。印刷物では copyright ページの URL を印字する。
- 加工したときの表示: 自分のデザインで描き直した場合は「Map data from OpenStreetMap」のように限定した書き方ができる。ODbL 4.3 により、Produced Work (画像など) を公に使うときはデータベース由来であることを示す通知が要る。
- 商用利用、再配布、加工したものの再配布: 商用も再配布も可。改変・翻案したデータは元と同じライセンスでのみ配布が認められる (copyright ページ)。ODbL 4.4 により公に使う派生データベースは ODbL (または後継・互換ライセンス) にし、4.6 により派生データベースか、それから作った Produced Work を公に使うときは、派生データベース全体または変更点を機械可読で提供する申し出が要る。
- 他のデータと混ぜたとき (ODbL、CC BY、PDL、政府標準利用規約など) の条件: OSMF の Collective Database Guideline (2016-06-17 承認) と Horizontal Map Layers Guideline (2014-06-06 承認) が判断基準を示す。地物の種類ごとに「同じ地域の切り出しの中で全部 OSM か全部 OSM 以外か」なら共有義務は OSM 部分だけに及び、同じ種類で OSM と他データを突き合わせたり補い合ったりすると共有義務が他データにも及ぶ。詳しくは `../license-mixing.md`。CC BY 4.0 のデータを OSM 本体に取り込むには、技術的保護手段の禁止 (CC BY 4.0 第 2a5B 節) の放棄を含む明示の許諾が要る、と OSMF は扱っている。

## 品質の限界

- 日本の住所タグは少ない。Geofabrik の日本の taginfo では `building` が約 3,120 万に対し、`addr:block_number` 約 32.5 万、`addr:housenumber` 約 26.2 万で、建物数の 1% 程度にとどまる。住所の地図やジオコーディングの元には向かない。
- 日本の住所は `addr:block_number` (街区符号・番地) と `addr:housenumber` (住居番号・枝番) に分け、`addr:street` は使わない、とする日本語 Wiki の記述がある。他国のツールが `addr:street` 前提だと日本の住所を正しく扱えない (推測)。
- タグは自由形式で、同じものに複数の書き方が混ざる。地域ごとの密度と鮮度は貢献者の数に左右される (推測)。
- 位置の精度の保証はない。

## 地図プロダクトでの使いどころ

- 全世界を同じスキーマで扱いたいときのベース。道路網、建物形状、POI を 1 つのソースで揃えられる。
- 差分が分単位で出るため、自前で更新を回せば最新に近い状態を保てる。
- 小さな範囲や特定のタグだけなら Overpass API で取れる。試作向き。
- 住所、統計、行政の公式データと重ねる場合は、地物の種類ごとに出所を分ける設計にすると共有義務の範囲を絞りやすい (Collective Database Guideline の考え方、`../license-mixing.md`)。

## 向いていない場面

- 派生データベースを ODbL で出したくない (自社のデータと同じ種類の地物を突き合わせて統合したい) 場合。
- 日本の住所 (番地・住居番号) のデータとして使う場面。
- 公式の精度や網羅性の保証が契約上要る場面 (自治体の台帳、法定の図面など)。
- 高頻度の本番アクセスに公開 Overpass API を使う場面。

## 出典

- https://planet.openstreetmap.org/ : 毎週の完全版、ODbL 1.0 の適用時期 (2012-09-12 以降)。
- https://planet.openstreetmap.org/pbf/ : 最新ファイル `planet-261102.osm.pbf` が 89 GB。
- https://planet.openstreetmap.org/replication/ : `minute/`、`hour/`、`day/` の差分ディレクトリ。
- https://download.geofabrik.de/asia/japan.html : 日本の抽出 2.4 GB、地方別の大きさ、Shapefile 非提供、データ時点。
- https://taginfo.geofabrik.de/asia:japan/api/4/key/stats?key=building ほか : 日本のタグ件数 (`building`、`amenity`、`addr:housenumber`、`addr:block_number`)。
- https://dev.overpass-api.de/overpass-doc/en/preface/commons.html : 公開 Overpass の利用目安と制限。
- https://operations.osmfoundation.org/policies/api/ : 編集用 API を読み取り目的に使わないこと、大量利用は planet を使うこと。
- https://www.openstreetmap.org/copyright/ja : 出典表示の 2 条件、改変データの配布条件、文書の CC BY-SA 2.0。
- https://osmfoundation.org/wiki/Licence/Attribution_Guidelines : 出典表示の書き方、置き場所、他ソースとの並べ方 (2021-06-25 採択)。
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Collective_Database_Guideline_Guideline : 他データと混ぜたときの判断基準。
- https://osmfoundation.org/wiki/Licence/Licence_Compatibility : CC BY 系は明示の許諾なしでは OSM に取り込めない、CDLA Permissive 2.0 は互換。
- https://blog.openstreetmap.org/2017/03/17/use-of-cc-by-data/ : CC BY 4.0 の許諾が要る理由。
- https://wiki.openstreetmap.org/JA:Key:addr:block_number : 日本の住所タグの使い分け。
- https://opendatacommons.org/licenses/odbl/1-0/ : ODbL 4.3、4.4、4.6。

## 未確認のこと

- OSM の座標参照系を明記した公式文書。
- Geofabrik の日本抽出の更新頻度 (ページに明記がない。確認時点では約 1 日前のデータ)。
- planet のファイル一覧の時刻のタイムゾーン (一覧では `planet-261102.osm.pbf` が 2026-11-05 17:40 と表示。UTC と推測)。
- 日本の建物データの網羅率 (実在の建物数に対する割合) と、建物データの主な出所 (公的データの取り込みか手作業か)。
- 日本の公的データ (国土数値情報、基盤地図情報など) の OSM への取り込み許諾の現状。OSM Wiki の Contributors ページの目次に「Kokudo Suchi Joho」などの項目があることだけ確認した。
- 公開 Overpass インスタンスの目安が overpass-api.de 以外のインスタンス (日本向けなど) でどうなっているか。
