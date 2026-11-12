# Cartopy

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 0.26.0 (PyPI、2026-09-17)。Python 3.11 以上 (https://pypi.org/project/Cartopy/) |
| リポジトリ | https://github.com/SciTools/cartopy |
| ドキュメント | https://scitools.org.uk/cartopy/docs/latest/ |
| ライセンス (LICENSE ファイルで確かめる) | BSD-3-Clause |
| 運営主体・ガバナンス | SciTools の組織。コミットは QuLogic、pelson、greglucas、dopplershift など 100 人以上 (GitHub の contributors、2026-11-13) |

## 概要

matplotlib に地図の投影を足すライブラリ (README の「a cartographic python library with matplotlib support」)。データの座標系と、描く地図の投影を分けて指定し、海岸線、国境、経緯線、ラスタ、図形を、正距円筒、ランベルト正角円錐、極投影、正射図法など多くの投影で描く。気象、気候、海洋の分野でよく使われる。

## 描画方式

- レンダリング: matplotlib (静止画)
- 2D / 2.5D / 3D: 2D
- 地球儀表示: 正射図法で地球儀風に描ける (回転はしない)
- 対応する投影法: 多数 (PROJ を pyproj 経由で使う)

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| 海岸線、国境などの基本の地図 | 対応 | Natural Earth と GSHHS。初めて使うときにダウンロードする (下の注意) |
| ラスタタイル (XYZ) | 対応 | `cartopy.io.img_tiles` |
| WMS / WMTS | 対応 | `add_wms`、`add_wmts` (OWSLib が要る) |
| 図形 (Shapefile、shapely) | 対応 | pyshp と shapely |
| ベクトルタイル | 非対応 | |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリとして禁じる記述は見当たらない。タイルを使うときは、その規約と帰属表示による
- API キー・アカウントの要否: 不要
- ネットワークの注意: Natural Earth などのデータを、使うときにインターネットから取り、データのディレクトリ (既定は XDG_DATA_HOME の下の cartopy) に保存する。ネットワークの無いサーバーや CI では、先に取っておき、環境変数 `CARTOPY_DATA_DIR` で場所を渡す (`lib/cartopy/__init__.py` の `pre_existing_data_dir`)

## ライセンスと費用

- ライセンス: BSD-3-Clause。Natural Earth のデータはパブリックドメイン (推測: Natural Earth の利用条件で確かめる)
- 利用料: 無料

## 性能と規模

- 扱える地物の数の目安: matplotlib に従う。高い解像度の海岸線 (10m) は描くのが遅い (推測)

## エコシステム

- 主なプラグイン・拡張: matplotlib、shapely、pyproj、pyshp。xarray の図から使える
- 日本語の情報: 解説記事は多い (未確認の数)

## 開発の活発さ

- 直近 1 年のリリース数: 1 (0.26.0)
- 最終コミット日: 2026-11-10 (push)
- 近年の大きな破壊的変更: 0.x のまま長く続いている。依存の版の下限を上げることが多い (推測)

## 環境の違いと保守

- ブラウザ間の互換: 該当しない
- OS 間の互換: CI (`ci-testing.yml`) は Ubuntu、macOS、Windows で、Python 3.11〜3.15 と、GIL の無い版 (3.14t、3.15t) も試す
- 操作の網羅: matplotlib の画面の土台に従う。地図の操作としては最小限
- エッジケースへの対応: 日付変更線や極をまたぐ図形の切り分けを、投影の変換の中で扱う (推測: 試験の範囲は未確認)
- 継続的な保守: 開いている issue 281 件、全体 1,360 件 (GitHub の検索、2026-11-13)。リリースの頻度は低い

## 向いている場面

- 気象、気候、海洋のデータを、目的に合った投影で静止画にする場合
- 論文や報告書の地図の図

## 向いていない場面

- 対話の地図、Web の地図の画面
- ネットワークの無い環境で、準備なしに動かす場合 (データを先に置く)

## 出典

- https://github.com/SciTools/cartopy (README、lib/cartopy/__init__.py、lib/cartopy/io/shapereader.py、.github/workflows/ci-testing.yml。2026-11-13)
- https://pypi.org/project/Cartopy/ (版、依存。2026-11-13)
