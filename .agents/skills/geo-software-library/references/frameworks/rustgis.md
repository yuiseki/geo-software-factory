# RustGIS

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 0.6.0 (GitHub のリリースと PyPI、2026-11-09)。最初のリリースは 0.1.0 (2026-10-12) で、1 か月で 6 回 (https://github.com/opengeos/RustGIS/releases 、https://pypi.org/project/rustgis/) |
| リポジトリ | https://github.com/opengeos/RustGIS |
| ドキュメント | https://rustgis.app/ (利用者の手引き、QGIS、ArcGIS、GeoLibre との比較、動画)、Web 版 https://web.rustgis.app 、プラグインの登録所 https://plugins.rustgis.app |
| ライセンス (LICENSE ファイルで確かめる) | Apache-2.0。依存の crate のライセンスは THIRD-PARTY-LICENSES.txt に、取り込んだデータとコードの出典は ATTRIBUTION.md にある。`deny.toml` が依存に許すライセンスを、許容的なもの (MIT、BSD、Apache-2.0、ISC、Zlib、CC0、OFL など) に限り、CI の `cargo deny` で確かめる |
| 運営主体・ガバナンス | opengeos の組織 (leafmap、geemap、geoai と同じ作者の Qiusheng Wu が中心)。コミットは giswqs が 441 件、pick2510 が 153 件、jgregoriorincon が 143 件など 61 人 (GitHub の contributors、2026-11-13)。README は「primarily built with Claude Opus 5.5 ... working under human direction and review」と、主に AI のモデルで作っていると明記している |

## 概要

純粋な Rust で書いた、デスクトップと Web の GIS のアプリ (README の「A fast, free and open-source GIS in pure Rust」)。QGIS や ArcGIS Pro と同じ種類の、データを読み、地図を作り、解析し、版面を作って共有する道具である。地図のライブラリではないが、次の 3 つの点で、地図のプロダクトの選定に関わる。

- 作らずに使う: 社内の地図の作業や解析なら、アプリを作らずにこれを使う案がある (geo-software-research-competitor の「既存のものを使う」)
- Python から使う: PyPI の `rustgis` パッケージが、エンジンを同じプロセスで動かし、Jupyter の地図 (`rustgis.Map`) と Qt のアプリのウィジェット (`rustgis.qt.MapWidget`) を持つ
- 広げる: WebAssembly のプラグイン (サンドボックスで動く) で、コマンド、道具、リボンのタブを足せる

ボタンの操作はすべて ID を持つコマンドで、コマンドライン (`rustgis-cli`)、ノートブック、AI のアシスタントから同じものを動かせる。

## 描画方式

- レンダリング: 地図の画像は tiny-skia (CPU) で描く (`rustgis-render`)。GPU の描画器もあり、README は「GPU renderer (beta)」とする (謝辞に wgpu が挙がるので、wgpu で描くと考えられる。推測)。画面は egui
- 2D / 2.5D / 3D: 2D と、傾き、回転、地形、建物の立ち上げ
- 地球儀表示: あり (3D の地球儀。月や火星などの天体の地図も)
- 対応する投影法: Equal Earth など多数。座標系は EPSG の番号で引く (PROJ の定義を crs-definitions の crate から組み込む。ATTRIBUTION.md)

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ベクターのファイル | 多数 | GeoJSON、CSV、Excel、Shapefile、GeoPackage、GeoParquet、FlatGeobuf、KML、GPX、GML など。GDAL の形式は GDAL のプログラムを通して読む (README の Data の項、構成の表) |
| ラスタ | 多数 | GeoTIFF と COG、Zarr、ASCII のグリッド、JPEG 2000、NetCDF、HDF など |
| ラスタタイル (XYZ / TMS / WMS) | 対応 | |
| ベクトルタイル (MVT / PMTiles / MBTiles) | 対応 | MapLibre のスタイル (スプライト、模様、式) も読む |
| Web のサービス | 対応 | WMS、WMTS、WFS、WCS、OGC API Features と Tiles、ArcGIS REST |
| データベース | 対応 | PostGIS、MySQL。DuckDB の問い合わせはそのプログラムを通す |
| 開かれたデータの検索 | 対応 | STAC (Planetary Computer)、NASA Earthdata、Hugging Face、Overture Maps、OSM の範囲の取得など |
| 書き出し | 対応 | 600 DPI までの PNG、PDF、Web の地図のページ、MapLibre のスタイル、ベクターとラスタの PMTiles、glTF、STL |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: アプリとして禁じる記述は見当たらない。背景の地図の既定は OpenFreeMap のベクトルタイル (README の謝辞)。使う背景の規約と帰属表示は、供給元の側で確かめる
- API キー・アカウントの要否: 不要。AI のアシスタントは、利用者が選んだ提供元 (Anthropic、OpenAI、Gemini など) の鍵か、サインインが要る
- データの送り先: README は、ファイルは手元で読み書きし、勝手には送らないと書く。ただし AI のアシスタントを使うと、問いと、答えるために読んだデータが、選んだ AI のモデルに送られる。個人情報や非公開のデータでは、使う前に方針を決める (geo-software-legal-check)

## ライセンスと費用

- ライセンス: Apache-2.0。依存も許容的なライセンスに限っている (`deny.toml`)。crs-definitions に無い EPSG の番号を補う表は、EPSG のデータセット (IOGP の利用条件) から作ったもので、その旨を同梱の文書に書いている (ATTRIBUTION.md)
- 利用料: 無料。GitHub Sponsors などの寄付を受ける
- 版によるライセンスの変化: 未確認 (若いプロジェクト)

## 性能と規模

- 配布: デスクトップは Windows、macOS、Linux (Microsoft Store、winget、Homebrew、AUR、Fedora の COPR)。Python の wheel は macOS (x86_64、arm64)、Linux (x86_64、aarch64)、Windows (amd64、arm64) で、Python 3.12 以上 (PyPI、0.6.0)
- 扱える地物の数の目安: 未確認。ファジングの CI (`fuzz.yml`) がある

## エコシステム

- 主なプラグイン・拡張: WebAssembly のプラグインと登録所。GeoLibre の道具の集まり (John Lindsay の WhiteboxTools にならったもの) と Whitebox の道具で、地形、水文、LiDAR、リモートセンシングの 1,000 を超える道具を使える (README。GeoLibre の道具の入手とライセンスの細部は確かめていない)
- ネイティブ版・兄弟プロジェクト: leafmap、geemap、geoai (同じ組織)
- 日本語の情報: 画面は 21 の言語 (README のバッジ。日本語が含まれるかは確かめていない)。JAXA Earth の API のカタログを読む試験がある (ATTRIBUTION.md)

## 開発の活発さ

- 直近 1 年のリリース数: 6 (2026-10-12 から 2026-11-09)
- 最終コミット日: 2026-11-12 (push)
- 近年の大きな破壊的変更: 0.x のため、版ごとに変わりうる。ROADMAP.md がある
- 開発の進め方: Claude で PR をレビューし、自動で直す CI がある (`claude-code-review.yml`、`claude-autofix.yml`)。リポジトリに AGENTS.md と `skills/` がある

## 環境の違いと保守

- ブラウザ間の互換: Web 版は WebAssembly のビルドを CI で作る (`ci.yml` の wasm32 の段)。ブラウザで動かす試験の段は見当たらない。Web 版でできないことは、手引きに「desktop」と印を付けている
- OS 間の互換: 毎晩の試験 (`nightly.yml`) は Ubuntu、macOS、Windows、Windows の ARM。PR の試験は、変更に応じて OS を選ぶ (`ci.yml` が計画して `test-rust.yml` を呼ぶ)。Python のパッケージの試験 (`test-python.yml`) もある
- 操作の網羅: リボン、ペイン、キーボードの近道、コマンドの検索、取り消し、編集の道具 (頂点の編集、スナップ) を持つ。どこまで試験しているかは未確認
- エッジケースへの対応: QGIS で作ったスタイルとプロジェクトの試験の集まり、解析の基準の結果の集まり (別の GIS で計算した期待値と比べる)、ファジングがある (ATTRIBUTION.md、`fuzz.yml`)
- 継続的な保守: 開いている issue 84 件、全体 508 件、PR 1,323 件 (GitHub の検索、2026-11-13)。作られて 1 か月で利用者と寄稿者が多い。開発の速さを AI のモデルが支えていて、README は結果を自分で確かめるよう求めている

## 向いている場面

- 社内や研究で、地図を作り、解析し、版面を作って共有する作業に、アプリを作らずに既製の GIS を使いたい場合 (QGIS の代わりの候補)
- Python や Qt のアプリに、GIS の地図の画面とエンジンを組み込みたい場合
- Web のブラウザだけで、インストールなしに GIS の作業をしたい場合

## 向いていない場面

- 利用者向けの製品の地図の画面を、独自の見た目で作る場合 (Web やネイティブの地図ライブラリを使う)
- 長い保守と API の安定の約束が要る組み込み (0.x で、1 か月の歴史)
- AI のアシスタントにデータを送れない環境で、その機能を前提にする場合

## 出典

- https://github.com/opengeos/RustGIS (README、LICENSE、ATTRIBUTION.md、deny.toml、.github/workflows/ci.yml、test-rust.yml、nightly.yml。2026-11-13)
- https://pypi.org/project/rustgis/ (版、wheel。2026-11-13)
- GitHub の API (contributors、issue と PR の数。2026-11-13)
