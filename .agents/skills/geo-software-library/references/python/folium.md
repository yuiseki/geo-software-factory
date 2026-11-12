# folium

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 0.20.0 (PyPI、2026-07-26)。Python 3.9 以上 (https://pypi.org/project/folium/) |
| リポジトリ | https://github.com/python-visualization/folium |
| ドキュメント | https://python-visualization.github.io/folium/ |
| ライセンス (LICENSE ファイルで確かめる) | MIT (LICENSE.txt の本文。GitHub の判定は NOASSERTION だが、本文は MIT の許諾の文。PyPI の表記も MIT) |
| 運営主体・ガバナンス | python-visualization の組織。コミットは ocefpaf が 834 件、Conengmo が 342 件、hansthen が 132 件など、100 人以上 (GitHub の contributors、2026-11-13) |

## 概要

Python のデータを、Leaflet.js の地図の HTML にするライブラリ (README の「Python Data. Leaflet.js Maps.」)。地図は Python の側で組み立て、HTML (と JavaScript) として書き出す。Jupyter ではそのまま表示され、ファイルに保存すればブラウザで開ける。Python とブラウザの間で値をやりとりする双方向の仕組みは持たない (双方向が要るなら ipyleaflet を使う。leafmap と geemap は両方を使い分ける)。

## 描画方式

- レンダリング: ブラウザの Leaflet.js (DOM と Canvas)。Python は HTML を作るだけ
- 2D / 2.5D / 3D: 2D
- 地球儀表示: なし
- 対応する投影法: Leaflet に従う (既定は Web メルカトル)

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | 供給元の一覧は xyzservices に依存する |
| ベクトルタイル (MVT / PMTiles / MLT) | 中核では非対応とみられる | プラグインの有無は未確認 |
| スタイル仕様 | 非対応 | 見た目は Python の引数で指定する |
| GeoJSON | 対応 | GeoPandas の GeoDataFrame の `explore()` も folium で描く |
| 3D Tiles / 地形 | 非対応 | |
| WMS / WMTS | WMS は対応 (WmsTileLayer)。WMTS は URL のひな形として読める (推測) | |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリとして禁じる記述は見当たらない。使うタイルの規約と帰属表示は、供給元の側で確かめる (geo-software-infra)。公開の OSM のタイルを既定で使う例が多いので、製品では使用の方針を確かめる
- API キー・アカウントの要否: 不要 (タイルによっては要る)

## ライセンスと費用

- ライセンス: MIT。依存の branca、jinja2 も許容的なライセンス (branca は同じ組織)
- 利用料: 無料
- 版によるライセンスの変化: 未確認

## 性能と規模

- バンドルサイズ: 該当しない (出力の HTML が Leaflet を CDN から読む)
- 扱える地物の数の目安: GeoJSON をそのまま HTML に埋め込むので、件数が多いと HTML が大きくなり、ブラウザが重くなる (推測: 数値の公式の目安は未確認)。大量の点はマーカーのクラスタのプラグインで束ねる

## エコシステム

- 主なプラグイン・拡張: `folium.plugins` (マーカーのクラスタ、ヒートマップ、時間の次元など)。Streamlit に埋め込む streamlit-folium があり、CI で組み合わせを試す (`test_streamlit_folium.yml`)
- ネイティブ版・兄弟プロジェクト: 色の対応表などの branca
- 日本語の情報: 解説記事は多い (未確認の数)

## 開発の活発さ

- 直近 1 年のリリース数: 1 (0.20.0)
- 最終コミット日: 2026-11-10 (push)
- 近年の大きな破壊的変更: 未確認 (0.x のまま長く続いている)

## 環境の違いと保守

- ブラウザ間の互換: 描画はブラウザの Leaflet に任せる。CI に Selenium と Playwright でブラウザを動かす試験と、描いた地図の画像を比べる試験 (`test_selenium.yml`、`test_snapshots.yml`) がある。使うブラウザの種類は Ubuntu の上のもの (詳細は未確認)
- OS 間の互換: 中心の試験 (`test_code.yml`) は Ubuntu、Windows、macOS で、Python 3.10 と 3.14
- 操作の網羅: 操作は Leaflet が受け持つ (geo-software-library の leaflet の reference)
- エッジケースへの対応: GeoPandas や branca の最新版との組み合わせを、別の CI で試す (`test_geopandas.yml`、`test_latest_branca.yml`)
- 継続的な保守: 開いている issue 58 件、全体 1,188 件 (GitHub の検索、2026-11-13)。リリースの頻度は低い

## 向いている場面

- Jupyter や Python のスクリプトで、GeoJSON や点のデータを、Leaflet の地図の HTML にすばやく出したい場合
- Streamlit などの Python の Web アプリに地図を埋め込みたい場合

## 向いていない場面

- 地図で選んだ範囲を Python に返すような、双方向の操作が要る場合 (ipyleaflet、leafmap)
- ベクトルタイルや大量の地物を描く場合 (MapLibre を使う leafmap の maplibre の描き方、lonboard、pydeck)
- 利用者向けの製品の Web の画面 (JavaScript の地図ライブラリを直接使う)

## 出典

- https://github.com/python-visualization/folium (README、LICENSE.txt、.github/workflows。2026-11-13)
- https://pypi.org/project/folium/ (版、依存。2026-11-13)
