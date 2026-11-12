# leafmap

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 0.64.5 (PyPI、2026-11-12)。Python 3.9 以上 (https://pypi.org/project/leafmap/) |
| リポジトリ | https://github.com/opengeos/leafmap |
| ドキュメント | https://leafmap.org/ |
| ライセンス (LICENSE ファイルで確かめる) | MIT |
| 運営主体・ガバナンス | opengeos の組織。コミットは giswqs (Qiusheng Wu) が 1,505 件で、ほかは数十件以下 (GitHub の contributors、2026-11-13)。実質 1 人の開発 |

## 概要

Jupyter で、少ないコードで対話の地図と地理の解析を行うライブラリ (README)。geemap から分かれ、Earth Engine を要さない。地図の描き方 (バックエンド) を切り替えられ、README は ipyleaflet、folium、MapLibre GL JS、lonboard、pydeck、kepler.gl、plotly、bokeh を挙げる。MapLibre の描き方では、ベクトルタイル、PMTiles、3D の地形、3D の建物、自前のスタイルを使える。

## 描画方式

- レンダリング: ブラウザ。選んだバックエンド (Leaflet、MapLibre GL JS、deck.gl など) に任せる
- 2D / 2.5D / 3D: バックエンドによる。MapLibre の描き方は 2.5D と 3D の地形
- 地球儀表示: MapLibre の描き方で地球儀が使えるか未確認
- 対応する投影法: バックエンドに従う

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ)、COG | 対応 | |
| ベクトルタイル (MVT / PMTiles) | MapLibre の描き方で対応 | |
| GeoJSON、GeoPandas | 対応 | |
| STAC | 対応 (推測: 文書で確かめる) | |
| 3D の地形と建物 | MapLibre の描き方で対応 | |

依存に duckdb、geopandas、folium、ipyleaflet、maplibre (Python のパッケージ) などがあり、入れるものが多い。

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: バックエンドと、使うタイルの規約による。kepler.gl や Mapbox 系の背景はトークンや規約に注意 (推測)
- API キー・アカウントの要否: 不要 (使うタイルやサービスによる)

## ライセンスと費用

- ライセンス: MIT。バックエンドのライセンスもそれぞれ確かめる (多くは許容的)
- 利用料: 無料

## 性能と規模

- 扱える地物の数の目安: バックエンドによる。大量の地物は lonboard や MapLibre の描き方の方が向く (推測)

## エコシステム

- 主なプラグイン・拡張: geemap (兄弟)、geoai (leafmap で見せる)。Docker のイメージを配る CI がある
- 日本語の情報: 解説記事がある (未確認の数)

## 開発の活発さ

- 直近 1 年のリリース数: 22
- 最終コミット日: 2026-11-12 (push)
- 近年の大きな破壊的変更: 未確認 (0.x)
- 開発の進め方: Claude Code で PR をレビューする CI がある (`claude-code-review.yml`)

## 環境の違いと保守

- ブラウザ間の互換: 描画はバックエンドに任せる。Jupyter の種類 (JupyterLab、VS Code、Colab) の違いは未確認
- OS 間の互換: CI は Ubuntu (Python 3.11〜3.14)、Windows (3.13、3.14)、macOS (`ubuntu.yml`、`windows.yml`、`macos.yml`)。インストールを試す CI もある
- 操作の網羅: バックエンドの操作に、道具の画面を足す
- エッジケースへの対応: 未確認
- 継続的な保守: 開いている issue 0 件、全体 324 件 (GitHub の検索、2026-11-13)。対応は速いが、主な作者への依存が大きい。多くのバックエンドを束ねるので、それぞれの変化への追随が要る

## 向いている場面

- Jupyter で、いろいろなデータ (GeoJSON、COG、PMTiles、STAC) を、1 行でとりあえず地図に出したい場合
- バックエンドを比べながら、表現を選びたい場合

## 向いていない場面

- 利用者向けの製品の地図の画面 (JavaScript の地図ライブラリを直接使う)
- 依存を少なくしたい環境

## 出典

- https://github.com/opengeos/leafmap (README、.github/workflows。2026-11-13)
- https://pypi.org/project/leafmap/ (版、依存。2026-11-13)
