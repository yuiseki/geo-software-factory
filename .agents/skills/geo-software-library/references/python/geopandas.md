# GeoPandas

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 1.2.0 (PyPI、2026-09-28)。Python 3.11 以上 (https://pypi.org/project/geopandas/) |
| リポジトリ | https://github.com/geopandas/geopandas |
| ドキュメント | https://geopandas.org/ |
| ライセンス (LICENSE ファイルで確かめる) | BSD-3-Clause |
| 運営主体・ガバナンス | geopandas の組織。コミットは jorisvandenbossche、kjordahl、martinfleis、m-richards など 100 人以上 (GitHub の contributors、2026-11-13) |

## 概要

pandas の表に、図形の列 (shapely) を足して、地理のデータを表として扱うライブラリ。地図を描くための専用のライブラリではないが、2 つの描き方を持つ。`GeoDataFrame.plot()` は matplotlib で静止画を描き、`GeoDataFrame.explore()` は folium で Leaflet の対話の地図を描く。読み書きは pyogrio (GDAL)、座標の変換は pyproj が受け持つ。

## 描画方式

- レンダリング: `plot()` は matplotlib (静止画、PNG や PDF)、`explore()` は folium (ブラウザの Leaflet)
- 2D / 2.5D / 3D: 2D
- 地球儀表示: なし
- 対応する投影法: データの CRS のまま描く (`plot()`)。地図の投影を選んで描くなら cartopy と組み合わせる。`explore()` は Web メルカトルに変換して描く

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ベクトルのファイル (GeoPackage、Shapefile、GeoJSON、FlatGeobuf、GeoParquet など) | 対応 | pyogrio (GDAL) で読み書きする。GeoParquet は pyarrow で読み書きする |
| ラスタタイル (XYZ) | 背景として | `plot()` は contextily と、`explore()` は folium の背景のタイルと組み合わせる |
| ベクトルタイル | 非対応 | |
| PostGIS | 対応 | `read_postgis`、`to_postgis` |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: 背景のタイルは組み合わせる側 (folium、contextily) の規約による
- API キー・アカウントの要否: 不要

## ライセンスと費用

- ライセンス: BSD-3-Clause。主な依存 (pandas、shapely、pyproj、pyogrio) も許容的なライセンス。pyogrio の wheel が同梱する GDAL などのライセンスは、配布するときに確かめる (未確認)
- 利用料: 無料

## 性能と規模

- 扱える地物の数の目安: メモリに載る範囲 (pandas と同じ)。空間索引 (`sindex`) がある。それより大きいデータは dask-geopandas や DuckDB の spatial を使う (推測: 公式の目安は未確認)

## エコシステム

- 主なプラグイン・拡張: mapclassify (`explore()` と `plot()` の分類)、contextily (背景のタイル)、dask-geopandas
- 日本語の情報: 解説記事と書籍が多い (未確認の数)

## 開発の活発さ

- 直近 1 年のリリース数: 4
- 最終コミット日: 2026-10-31 (push)
- 近年の大きな破壊的変更: 1.0 で、古い読み書き (fiona) から pyogrio を既定にするなどの変更があった (推測: 版ごとの詳細は CHANGELOG で確かめる)

## 環境の違いと保守

- ブラウザ間の互換: `explore()` の描画は folium と Leaflet に任せる
- OS 間の互換: CI (`tests.yaml`) は Ubuntu で、依存の組み合わせ (最新、最小、pyogrio なし、pyproj なし、任意の依存なし) を変えて回し、Windows と macOS の組も含む。PostGIS と組む試験もある
- 操作の網羅: 該当しない (データのライブラリ)
- エッジケースへの対応: 任意の依存が無いときの振る舞いを、依存を外した環境で試している (`ci/envs/313-no-optional-deps.yaml` など)
- 継続的な保守: 開いている issue 344 件、全体 1,758 件 (GitHub の検索、2026-11-13)。地理の Python の基盤で、多くのライブラリ (leafmap、geoai など) が依存する

## 向いている場面

- 地図を描く前の、データの読み込み、結合、空間の演算、座標の変換
- 分析の途中で、データを静止画 (`plot()`) や対話の地図 (`explore()`) ですぐ確かめたい場合

## 向いていない場面

- 地図の見た目を作り込みたい場合 (静止画なら cartopy と matplotlib、対話なら leafmap や folium を直接使う)
- 利用者向けの地図の画面

## 出典

- https://github.com/geopandas/geopandas (README、.github/workflows/tests.yaml、geopandas/explore.py。2026-11-13)
- https://pypi.org/project/geopandas/ (版、依存。2026-11-13)
