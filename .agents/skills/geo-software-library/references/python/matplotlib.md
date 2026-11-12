# Matplotlib

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 3.11.2 (PyPI、2026-09-11)。Python 3.11 以上 (https://pypi.org/project/matplotlib/) |
| リポジトリ | https://github.com/matplotlib/matplotlib |
| ドキュメント | https://matplotlib.org/ |
| ライセンス (LICENSE ファイルで確かめる) | Matplotlib 独自のライセンス (「License agreement for matplotlib versions 1.3.0 and later」、PSF のライセンスと同じ形。PyPI の分類は「OSI Approved :: Python Software Foundation License」)。コピーレフトではない。同梱のフォントや一部のコードは、LICENSE ディレクトリの別のライセンス (STIX、BaKoMa、FreeType、HarfBuzz など) |
| 運営主体・ガバナンス | matplotlib の組織 (NumFOCUS の支援を受けるプロジェクト)。コミットは tacaswell、QuLogic、timhoffm、anntzer など 100 人以上 (GitHub の contributors、2026-11-13) |

## 概要

Python の汎用の図のライブラリ。地図の専用のライブラリではないが、Python の静止画の地図の多くは、これを土台に描かれる (GeoPandas の `plot()`、cartopy、contextily)。PNG、PDF、SVG などに書き出す。地図の投影は持たないので、投影を選んで描くなら cartopy と組み合わせる。

## 描画方式

- レンダリング: 書き出しの土台 (Agg のラスタ、PDF、SVG、PS など) と、画面の土台 (Qt、Tk、macOS、Jupyter の ipympl など)
- 2D / 2.5D / 3D: 2D が中心 (mplot3d で簡単な 3D)
- 地球儀表示: なし (cartopy の正射図法で地球儀風には描ける)
- 対応する投影法: 地図の投影は持たない (cartopy が足す)

## 対応するデータ

地図のデータを読む機能は持たない。座標の配列、画像の配列、図形 (GeoPandas と cartopy 経由) を描く。

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: 該当しない。背景のタイルを描く contextily などは、そのタイルの規約による
- API キー・アカウントの要否: 不要

## ライセンスと費用

- ライセンス: 上のとおり。配布するときは LICENSE ディレクトリの同梱物のライセンスも確かめる
- 利用料: 無料

## 性能と規模

- 扱える地物の数の目安: 図形の数が多いと遅くなる (推測: 公式の数値は未確認)。地図の静止画では、ラスタにしてから描く、図形を単純にするなどで対処する

## エコシステム

- 主なプラグイン・拡張: cartopy (地図の投影)、contextily (背景のタイル)、GeoPandas (`plot()`)、mapclassify (分類)
- ネイティブ版・兄弟プロジェクト: Pyodide (ブラウザの Python) で動かす CI がある (`wasm.yml`)
- 日本語の情報: 多い。日本語のフォントの設定は別に要る (推測: 既定のフォントに日本語の字形が無いため)

## 開発の活発さ

- 直近 1 年のリリース数: 7
- 最終コミット日: 2026-11-11 (push)
- 近年の大きな破壊的変更: 非推奨を 2 版かけて外す方針 (推測: 詳細は API の変更の文書で確かめる)

## 環境の違いと保守

- ブラウザ間の互換: 該当しない (画像を書き出す)。Jupyter の対話の表示は ipympl などの別の土台
- OS 間の互換: CI は Ubuntu (22.04、24.04)、macOS (15、26)、Windows (`windows-tests.yml`)、Cygwin、Pyodide (WebAssembly) で、Python 3.12〜3.15 (`.github/workflows/tests.yml` ほか)。wheel は cibuildwheel で作る
- 操作の網羅: 画面の土台ごとの拡大、移動の道具がある。地図の操作としては最小限
- エッジケースへの対応: 画像を比べる試験 (基準の画像) を多数持つ (推測: 試験の数は未確認)
- 継続的な保守: 開いている issue 1,044 件、全体 11,445 件 (GitHub の検索、2026-11-13)。利用者と保守者の層が厚い

## 向いている場面

- 論文、報告書、印刷向けの静止画の地図を、再現できるコードで作る場合 (cartopy、GeoPandas と組み合わせる)
- 地図と、グラフ (時系列、ヒストグラム) を 1 枚の図に並べる場合

## 向いていない場面

- 拡大、移動する対話の地図 (folium、leafmap、plotly)
- タイルやベクトルタイルを主に描く地図

## 出典

- https://github.com/matplotlib/matplotlib (LICENSE ディレクトリ、.github/workflows/tests.yml、windows-tests.yml、wasm.yml、cygwin.yml。2026-11-13)
- https://pypi.org/project/matplotlib/ (版、依存、ライセンスの分類。2026-11-13)
