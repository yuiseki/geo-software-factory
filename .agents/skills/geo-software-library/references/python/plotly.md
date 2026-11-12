# Plotly (plotly.py)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 7.1.0 (PyPI、2026-09-15)。Python 3.8 以上 (https://pypi.org/project/plotly/) |
| リポジトリ | https://github.com/plotly/plotly.py (依頼の URL は組織の https://github.com/plotly 。地図を描く本体は plotly.py と、その中で動く plotly.js) |
| ドキュメント | https://plotly.com/python/ (地図は https://plotly.com/python/maps/) |
| ライセンス (LICENSE ファイルで確かめる) | MIT (plotly.py)。plotly.js も MIT (推測: plotly.js のリポジトリで確かめる) |
| 運営主体・ガバナンス | Plotly 社の組織。コミットは nicolaskruchten、LiamConnors、theengineear、Kully など 100 人以上 (GitHub の contributors、2026-11-13) |

## 概要

Python の対話のグラフのライブラリ。地図は図の種類の 1 つで、タイルの地図 (`scatter_map`、`choropleth_map`、`density_map`) と、タイルを使わない地理の図 (`scatter_geo`、`choropleth` の geo) がある。描画はブラウザの plotly.js が行い、Jupyter、HTML のファイル、Dash のアプリで表示する。グラフと地図を同じ書き方で並べられる。

## 描画方式

- レンダリング: ブラウザの plotly.js。タイルの地図は MapLibre GL JS で描く (変更履歴に、`scattermap`、`choroplethmap`、`densitymap` と map の subplot を MapLibre で描く新しい図を足し、Mapbox の図を非推奨にした記録がある。Mapbox から MapLibre への移行の文書 https://plotly.com/python/mapbox-to-maplibre/)。地理の図は SVG
- 2D / 2.5D / 3D: 2D (タイルの地図は傾けられる。推測)
- 地球儀表示: 地理の図の正射図法で地球儀風に描ける
- 対応する投影法: 地理の図は多数の投影、タイルの地図は Web メルカトル

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 (タイルの地図の背景と層) | |
| ベクトルタイル | MapLibre のスタイルで背景に使える (推測: 自前のスタイルの URL を渡せるかは文書で確かめる) | |
| GeoJSON | 対応 (コロプレス図の境界) | |
| 3D Tiles / 地形 | 非対応 | |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: 旧来の Mapbox の図は Mapbox のアクセストークンが要り、Mapbox の規約による。MapLibre の図は、使うタイルの規約による
- API キー・アカウントの要否: MapLibre の図は不要 (タイルによっては要る)

## ライセンスと費用

- ライセンス: MIT
- 利用料: 無料。Plotly 社の有料の製品 (Dash Enterprise など) は別 (未確認)

## 性能と規模

- 扱える地物の数の目安: 未確認。点が多いときは WebGL で描く図の種類がある (推測)
- 画像の書き出し: 静止画の書き出し (kaleido) に、Chrome を使う試験の段が CI にある (`run-pytest.yml`)

## エコシステム

- 主なプラグイン・拡張: Dash (Python で Web アプリを作る、同じ会社)、plotly express (短い書き方)
- 日本語の情報: 多い (未確認の数)

## 開発の活発さ

- 直近 1 年のリリース数: 10
- 最終コミット日: 2026-11-06 (push)
- 近年の大きな破壊的変更: Mapbox の図の非推奨と MapLibre の図への移行。古い Figure Factory の関数の削除 (CHANGELOG)

## 環境の違いと保守

- ブラウザ間の互換: 描画は plotly.js に任せる。plotly.js の開発版との組み合わせを試す CI (`test-plotlyjs-dev.yml`) と、画像の差を見る Percy の CI (`run-percy.yml`) がある
- OS 間の互換: 試験 (`run-pytest.yml`) は Ubuntu で、Python 3.8〜3.13。Windows と macOS の試験は見当たらない
- 操作の網羅: 拡大、移動、ホバーの表示、選択は plotly.js が持つ
- エッジケースへの対応: タイルの地図の初めの中心とズームを、データから自動で決めるようにした (`layout.map.fitbounds`、CHANGELOG)。MapLibre GL JS の脆弱性 (CVE) に合わせて版を上げた記録がある
- 継続的な保守: 開いている issue 648 件、全体 3,399 件 (GitHub の検索、2026-11-13)。企業が主に保守する

## 向いている場面

- グラフと地図を同じ書き方で作り、Jupyter や Dash のアプリで見せたい場合
- 国や地域のコロプレス図、点の散布図を、対話の地図にすばやく出したい場合

## 向いていない場面

- 地図の見た目を作り込みたい、ベクトルタイルの配色を細かく作りたい場合 (MapLibre GL JS を直接、または leafmap の maplibre の描き方)
- 印刷の品質の静止画の地図 (cartopy と matplotlib)

## 出典

- https://github.com/plotly/plotly.py (README、CHANGELOG.md、.github/workflows/run-pytest.yml ほか。2026-11-13)
- https://pypi.org/project/plotly/ (版、依存。2026-11-13)
