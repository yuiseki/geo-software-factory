# GeoAI (geoai-py)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 0.43.1 (PyPI の geoai-py、2026-09-21)。Python 3.12 以上 (https://pypi.org/project/geoai-py/) |
| リポジトリ | https://github.com/opengeos/geoai |
| ドキュメント | https://opengeoai.org/ (リポジトリのホームページ)。論文 Wu, Q. (2026), Journal of Open Source Software 11(118), 9605 |
| ライセンス (LICENSE ファイルで確かめる) | MIT (パッケージ)。使うモデルの重みやデータセットのライセンスは別 |
| 運営主体・ガバナンス | opengeos の組織。コミットは giswqs (Qiusheng Wu) が 494 件で、ほかは数十件以下 (GitHub の contributors、2026-11-13) |

## 概要

地理のデータに AI (深層学習) を使うためのライブラリ。地図を描くライブラリではなく、衛星や航空の画像の取得、学習データの作成 (画像の切り出しとラベル)、セグメンテーション (建物、水域、湿地、太陽光パネルなど) の学習と推論、結果のベクターへの変換と書き出しを受け持つ。結果を見るのに leafmap と MapLibre を使う。QGIS のプラグインもある。

## 描画方式

- レンダリング: 自分では描かない。leafmap (MapLibre GL JS など) で地図に出す
- 2D / 2.5D / 3D: leafmap に従う

## 対応するデータ

画像 (Sentinel、Landsat、NAIP などの取得の道具)、ベクター (GeoJSON、Shapefile、GeoPackage、GeoParquet で書き出し)、Overture Maps のデータ、Planetary Computer。依存は多く、深層学習の環境 (PyTorch など) を前提にする (推測: 依存の一覧の先頭だけ確かめた)。

## 組み合わせの制約

- 画像の供給元 (Planetary Computer など) と、モデルの配布元 (Hugging Face など) の規約による
- API キー・アカウントの要否: 使うサービスによる

## ライセンスと費用

- ライセンス: MIT。学習済みのモデルの重みと、学習に使ったデータのライセンスは、モデルごとに違う。製品に組み込むときは、重みのライセンスを版ごとに確かめる
- 利用料: 無料。GPU の計算機は別

## 性能と規模

- 深層学習の学習と推論は GPU を前提にする (推測)。CPU だけで動く範囲は未確認

## エコシステム

- 主なプラグイン・拡張: leafmap、segmentation_models.pytorch、Hugging Face のモデル、QGIS のプラグイン (CI の `qgis-plugin.yml`)
- 日本語の情報: 未確認

## 開発の活発さ

- 直近 1 年のリリース数: 37
- 最終コミット日: 2026-11-09 (push)
- 近年の大きな破壊的変更: 未確認 (0.x)
- 開発の進め方: Claude で PR のレビューと自動修正をする CI がある (`claude-code-review.yml`、`claude-autofix.yml`)

## 環境の違いと保守

- ブラウザ間の互換: 該当しない (表示は leafmap に任せる)
- OS 間の互換: CI は Ubuntu と Windows (Python 3.12〜3.14)、macOS (`ubuntu.yml`、`windows.yml`、`macos.yml`)。最小の依存で import できるかを試す CI (`minimal-import.yml`) と、QGIS の依存を解く CI がある
- 操作の網羅: 該当しない
- エッジケースへの対応: 未確認
- 継続的な保守: 開いている issue 8 件、全体 244 件 (GitHub の検索、2026-11-13)。リリースは多く、主な作者への依存が大きい。深層学習の依存の版の変化に追随し続ける必要がある

## 向いている場面

- 衛星や航空の画像から、建物や水域などを抽出する解析を、Jupyter で試す場合 (研究、教育、試作)
- 抽出した結果を、すぐ地図で確かめたい場合

## 向いていない場面

- 地図を描くことが目的の場合 (このスキルの他のライブラリを使う)
- 製品に学習済みのモデルを組み込むが、重みのライセンスを確かめられない場合

## 出典

- https://github.com/opengeos/geoai (README、.github/workflows。2026-11-13)
- https://pypi.org/project/geoai-py/ (版、依存。2026-11-13)
