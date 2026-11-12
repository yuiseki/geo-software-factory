# geemap

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 0.38.9 (PyPI、2026-10-01)。Python 3.12 以上 (https://pypi.org/project/geemap/) |
| リポジトリ | https://github.com/gee-community/geemap |
| ドキュメント | https://geemap.org/ |
| ライセンス (LICENSE ファイルで確かめる) | MIT |
| 運営主体・ガバナンス | gee-community の組織。コミットは giswqs (Qiusheng Wu) が 1,482 件、schwehr が 328 件、naschmitz が 73 件など 70 人 (GitHub の contributors、2026-11-13)。主に 1 人が書き、Google の Earth Engine の関係者も加わっている (推測: schwehr の所属は確かめていない) |

## 概要

Google Earth Engine (GEE) を Jupyter で対話的に使うためのライブラリ (README の「interactive geospatial analysis and visualization with Google Earth Engine」)。Earth Engine の画像や地物の集まりを、ipyleaflet や folium の地図に載せ、地図の上の操作 (範囲の描画、値の表示) と Python の解析をつなぐ。leafmap はこれから分かれたプロジェクトである。

## 描画方式

- レンダリング: ブラウザ。ipyleaflet (Jupyter の中で Python と双方向)、folium (HTML) など。依存に plotly、bqplot がある
- 2D / 2.5D / 3D: 2D が中心
- 地球儀表示: 未確認
- 対応する投影法: 地図は Web メルカトル。Earth Engine の解析は任意の投影

## 対応するデータ

Earth Engine の画像、画像の集まり、地物の集まりが中心。手元のベクターやラスタも載せられる (推測: 範囲は文書で確かめる)。

## 組み合わせの制約

- Earth Engine が要る: Google のアカウントと Google Cloud のプロジェクトで Earth Engine を有効にし、認証する必要がある。2026-04-27 から、非商用のプロジェクトには、毎月の無料の計算の枠 (EECU の時間) がある。商用の利用は Google Cloud の有料の契約になる (https://developers.google.com/earth-engine/guides/noncommercial_tiers 、https://earthengine.google.com/commercial/)。製品や受託で使うときは、商用か非商用かを昼に決めて、契約を先に頼む
- 背景のタイル: 組み合わせるタイルの規約による

## ライセンスと費用

- ライセンス: MIT (ライブラリ)。Earth Engine の利用規約と、データセットごとのライセンスは別
- 利用料: ライブラリは無料。Earth Engine は非商用なら無料の枠の中、商用は有料

## 性能と規模

- 計算は Earth Engine のサーバーで行うので、手元の計算機の大きさに左右されにくい。代わりに、Earth Engine の枠と待ち時間に左右される

## エコシステム

- 主なプラグイン・拡張: leafmap (兄弟)、eerepr、earthengine-api。Docker のイメージを配る CI がある
- 日本語の情報: 解説記事がある (未確認の数)

## 開発の活発さ

- 直近 1 年のリリース数: 24
- 最終コミット日: 2026-11-11 (push)
- 近年の大きな破壊的変更: 未確認 (0.x)

## 環境の違いと保守

- ブラウザ間の互換: 描画は ipyleaflet と folium に任せる。Jupyter、JupyterLab、Google Colab などの表示の違いは未確認
- OS 間の互換: Ubuntu (`ubuntu.yml`)、Windows (`windows.yml`、Python 3.13)、macOS (`macos.yml`) の CI がある。インストールを試す CI (`installation.yml`) もある
- 操作の網羅: ipyleaflet の地図の操作に、範囲の描画、値の表示、道具の画面を足す
- エッジケースへの対応: 未確認
- 継続的な保守: 開いている issue 26 件、全体 681 件 (GitHub の検索、2026-11-13)。主な作者への依存が大きい

## 向いている場面

- Earth Engine の衛星画像の解析を、Jupyter で地図を見ながら進めたい場合 (研究、教育、非商用)

## 向いていない場面

- Earth Engine を使わない地図 (leafmap を使う)
- 利用者向けの製品の地図の画面
- 商用で、Earth Engine の契約の見通しが立たない場合

## 出典

- https://github.com/gee-community/geemap (README、.github/workflows。2026-11-13)
- https://pypi.org/project/geemap/ (版、依存。2026-11-13)
- https://developers.google.com/earth-engine/guides/noncommercial_tiers 、https://earthengine.google.com/commercial/ (Earth Engine の非商用の枠と商用。2026-11-13)
