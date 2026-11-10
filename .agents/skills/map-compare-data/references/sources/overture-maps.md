# Overture Maps

対象: Overture Maps Foundation のデータ (places、buildings、transportation、addresses、divisions、base)。テーマごとのライセンス

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 提供者 | Overture Maps Foundation (OMF) |
| 配布ページ | https://docs.overturemaps.org/getting-data/ 、リリース一覧 (STAC): https://stac.overturemaps.org/catalog.json |
| 利用規約・ライセンス | テーマごとに異なる。buildings、divisions、transportation、base は ODbL。places は単一のテーマライセンスがなく、出所ごとに CDLA-Permissive-2.0、Apache-2.0、CC0-1.0。addresses も出所ごと (CC BY 4.0、CC0、各国の政府ライセンスなど)。https://docs.overturemaps.org/attribution/ |

## 概要

Overture Maps は、OpenStreetMap、企業の提供データ、機械学習で抽出したデータ、公的データを突き合わせて 1 つのスキーマにまとめた世界規模の地図データである。6 テーマ (addresses、base、buildings、divisions、places、transportation) を GeoParquet で毎月出している。主要な地物には GERS ID という UUID が付き、リリースをまたいで地物を対応づけられる。テーマごとにライセンスが違い、OSM 由来を含むテーマは ODbL になる。

## 収録範囲と詳しさ

| 項目 | 値 | 出典 |
|---|---|---|
| 地域 | 全世界。ただし addresses は 41 か国だけで、日本は含まれる (JP は約 1,960 万件)。米国、ドイツ、台湾などは一部のみ | https://docs.overturemaps.org/guides/addresses/ |
| 主なテーマ・レイヤー | addresses (address)、base (bathymetry、infrastructure、land、land_cover、land_use、water)、buildings (building、building_part)、divisions (division、division_area、division_boundary)、places (place)、transportation (connector、segment) | https://stac.overturemaps.org/2026-10-21.0/catalog.json と各テーマの catalog.json |
| 件数・大きさの目安 | 2026-10-21.0 で building 2,533,842,612 行、place 88,418,121 行、address 475,263,892 行、segment 353,327,860 行、division 4,700,999 行 | 各 collection.json の `table:row_count` (例: https://stac.overturemaps.org/2026-10-21.0/places/place/collection.json) |
| 位置の精度・縮尺 | 位置精度の規定は確認できなかった。places は存在の確からしさ `confidence` (0〜1) を持つが、提供元をまたいで較正されておらず相対的な絞り込みに使うものとされる | https://docs.overturemaps.org/guides/places/ |
| 時点と更新頻度 | 毎月リリース (2023-10 から)。最新は `2026-10-21.0` (スキーマ v2.0.0)。次は `2026-11-18.0`、`2026-12-16.0` の予定。破壊的なスキーマ変更は 3、6、9、12 月だけ。公開リリースは最大 60 日 (2 リリース分) で消える | https://docs.overturemaps.org/release-calendar/ |

## 形式と取得方法

- 配布形式 (Shapefile、GeoJSON、GeoParquet、PMTiles、CSV など): GeoParquet (ファイルのメタデータでは GeoParquet 1.1.0、ジオメトリは WKB、bbox 列による covering 付き)。テーマ別の PMTiles もあるが、公式は本番利用を勧めておらず、レイヤーや属性、ズームは予告なく変わり得るとしている。Explorer や DuckDB 経由で GeoJSON に書き出せる。
- 取得方法 (一括ダウンロード、API、範囲を絞った取得): S3 `s3://overturemaps-us-west-2/release/<RELEASE>/theme=<theme>/type=<type>/*.parquet`、Azure `https://overturemapswestus2.blob.core.windows.net/release/<RELEASE>`。PMTiles は `https://overturemaps-extras-us-west-2.s3.us-west-2.amazonaws.com/tiles/<RELEASE>/<THEME>.pmtiles`。範囲を絞るには overturemaps-py (v2.1.0、2026-11-07 公開) の bbox 指定、DuckDB の SQL (bbox 列で絞る)、ブラウザの Explorer。`https://stac.overturemaps.org/latest.ddb` は最新リリースへのビューを持つ DuckDB ファイル (DuckDB 1.2.0 以上)。
- 座標参照系: 公式ページでの明記は確認できなかった。`2026-10-21.0` の divisions のファイルの GeoParquet メタデータには `crs` がなく、GeoParquet 仕様では `crs` 省略時は OGC:CRS84 (経度・緯度、WGS84) と解釈される。他のテーマのファイルも同じかは確かめていない。

## ライセンスと出典表示

- ライセンス: buildings、divisions、transportation、base は ODbL (OSM を含むため)。places は Meta、Microsoft、BrightQuery など多くが CDLA-Permissive-2.0、Foursquare が Apache-2.0、AllThePlaces が CC0-1.0。places には OSM のデータは入っていない。addresses は出所ごとで、日本 (JP) は出所「Japanese Ministry of Land, Infrastructure and Transport」、CC BY 4.0、OpenAddresses 経由。
- 出典表示の書き方 (公式の例): 出版物では「Overture Maps Foundation, overturemaps.org」とアクセス日。OSM 由来のデータは「© OpenStreetMap contributors, Overture Maps Foundation」。places の Foursquare 分は「Copyright 2024 Foursquare Labs, Inc. All rights reserved.」と NOTICE.txt。
- 加工したときの表示: Overture 独自の書き方は確認できなかった。ODbL のテーマは ODbL 4.3 (Produced Work の通知) と OSMF の出典表示ガイドラインに従う (`./openstreetmap.md`)。CC BY 4.0 の出所 (日本の addresses など) は CC BY 4.0 の改変表示の条件がかかる (推測)。
- 商用利用、再配布、加工したものの再配布: いずれのライセンスも商用利用と再配布を認める。ODbL のテーマから作った派生データベースを公に使うときは ODbL での提供と派生データベースの提供の申し出が要る (ODbL 4.4、4.6)。CDLA-Permissive-2.0 のデータを共有するときは規約の本文を添える (2.1 節)。分析結果 (Results) には制約がない (3.1 節)。
- 他のデータと混ぜたとき (ODbL、CC BY、PDL、政府標準利用規約など) の条件: 公式の places ガイドは「places を OSM と結合すると、結果のデータベースに ODbL が必要になることがある」と書いている。buildings は全ソースが ODbL か CC BY 4.0 などの互換ライセンスであることを Overture が確認してから取り込む。それ以外の組み合わせは `../license-mixing.md`。

## 品質の限界

- places は重複、ゴミデータの率の高さ、属性の欠けが既知の問題として公式に挙げられている。国別の網羅率の測定はまだ途中。2026-07 のリリースで突き合わせをやり直したため、そのリリースでは GERS ID の付け替えが多い。
- buildings は OSM を最優先し、次にコミュニティ提供 (Esri Community Maps など)、残りを機械学習の屋根形状 (Microsoft、Google Open Buildings、東アジアのデータセット) で埋める。ソースにより形状の質が違う (推測)。
- GERS ID は 2025-06-25.0 より前の ID を UUID に置き換えたので、古い ID は今のデータと対応しない。base テーマと building_part の UUID は GERS ID ではなく安定性の約束がない。
- 公開リリースは 60 日で消えるため、過去の版を再現したいなら自分で保存しておく必要がある。
- 日本の places、buildings、transportation の網羅率は公式に示されていない。

## 地図プロダクトでの使いどころ

- 世界規模の POI を、ODbL の共有義務なしに使いたいとき (places は OSM を含まず、主に CDLA-Permissive-2.0)。
- 地物を GERS ID で継続的に追跡したいとき。ブリッジファイルで出所の ID と GERS ID を対応づけられ、変更履歴 (changelog) で前リリースからの変化を取れる。
- GeoParquet をクラウドから直接 SQL で範囲指定して読めるので、必要な地域とテーマだけを取り出したいとき。
- 試作で見た目を確かめるだけなら公式の PMTiles を使える (本番は非推奨)。

## 向いていない場面

- 本番の地図配信にそのまま公式 PMTiles を使う場面。
- 日本の住所の正本として使う場面。日本の addresses は国交省のデータを OpenAddresses 経由で取り込んだもので、元データを直接使うほうが出所と時点を追いやすい (推測)。
- ODbL を避けたいのに buildings、transportation、divisions、base を使う場面。
- 古いリリースを長期に参照し続ける運用 (60 日で消える)。

## 出典

- https://docs.overturemaps.org/attribution/ : テーマごとのライセンス、出典表示の文例、日本の addresses の出所とライセンス。
- https://docs.overturemaps.org/release-calendar/ : 毎月のリリース、最新 `2026-10-21.0`、予定、60 日の保持期間、2026 年のリリース ID。
- https://docs.overturemaps.org/getting-data/ と https://docs.overturemaps.org/getting-data/cloud-sources/ : S3 と Azure のパス、PMTiles の場所と本番非推奨、STAC、`latest.ddb`。
- https://stac.overturemaps.org/catalog.json と各 collection.json : 最新リリース、テーマとタイプ、行数、スキーマ v2.0.0。
- https://overturemaps-us-west-2.s3.us-west-2.amazonaws.com/release/2026-10-21.0/theme=divisions/type=division/ 配下の parquet のフッタ : GeoParquet 1.1.0、`crs` 未記載。
- https://docs.overturemaps.org/gers/ : GERS ID の性質、レジストリ、ブリッジファイル、changelog。
- https://docs.overturemaps.org/guides/places/ : places の出所別件数とライセンス、confidence、既知の問題、OSM と結合したときの注意。
- https://docs.overturemaps.org/guides/buildings/ : buildings の出所と優先順位、ライセンス確認の方針。
- https://docs.overturemaps.org/guides/addresses/ : 41 か国、日本の件数、出所。
- https://github.com/OvertureMaps/overturemaps-py/releases : overturemaps-py v2.1.0。
- https://cdla.dev/permissive-2-0/ : CDLA-Permissive-2.0 の共有条件と Results。

## 未確認のこと

- Overture のデータの座標参照系を明記した公式文書。divisions 以外のファイルの `crs` の有無。
- 日本の places、buildings、transportation の件数と網羅率。
- 日本の addresses の元データが国交省のどのデータセット (位置参照情報など) で、どの時点のものか。元データの約款と CC BY 4.0 の関係。
- buildings の「東アジアのデータセット」の名前とライセンス (公式ページは Zenodo へのリンクだけで、名前を明記していない)。
- Overture 全体の利用規約 (テーマのライセンス以外に Terms of Use があるか)。
- GERS ID の安定性の約束の具体的な内容 (GERS ID Stability のページは読んでいない)。
- CDLA-Permissive-2.0 の places を表示するとき、出典表示が要るか。公式の attribution ページは CDLA の出所について表示の要否を明記していない。CDLA-Permissive-2.0 の本文には出典表示の義務はない。
