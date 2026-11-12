# forge3d

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 1.48.0 (GitHub のリリースは 2026-11-09。PyPI の最新も 1.48.0)。`Cargo.toml` の版は 1.47.1 のままで、Python のパッケージの版と一致していない (https://github.com/milos-agathon/forge3d/releases 、https://pypi.org/project/forge3d/) |
| リポジトリ | https://github.com/milos-agathon/forge3d |
| ドキュメント | https://milos-agathon.github.io/forge3d/ (Quickstart、Feature Map、Tutorials、Gallery、API Reference) |
| ライセンス (LICENSE ファイルで確かめる) | 中核は Apache-2.0 または MIT のデュアルライセンス (LICENSE は MIT、LICENSE-APACHE は Apache-2.0。PyPI の表記は `Apache-2.0 OR MIT`)。一部の機能は、別の商用のライセンスキーが要る Pro 機能 (下の「ライセンスと費用」) |
| 運営主体・ガバナンス | 個人 (Milos Popovic、GIS のコンサルタント。https://milosgis.com/ で forge3d を「自分のレンダリングエンジン」と紹介している)。コミットは milos-agathon が 1,792 件、ほか 2 人が 53 件と 4 件 (GitHub の contributors、2026-11-13) |

## 概要

Rust と wgpu (WebGPU の実装) で書いた 3D の地形と地図のレンダラーを、Python のパッケージとして配るもの。README は「Path-traced terrain and cartography for Python」とうたう。標高のデータ (GeoTIFF、numpy の配列、COG) を入れ、パストレーシング、PBR、水面、雲と影まで描いて、印刷の解像度 (ギャラリーは最大 7200 x 7200) の静止画や動画のフレームを書き出す。凡例、縮尺、方位記号、ラベルも同じ描画の中で作る。

Web の地図ライブラリやネイティブの SDK とは用途が違う。利用者が操作する地図の画面を作るものではなく、作り手が Python から地図の作品 (ポスター、報道の図、SNS の動画) を作るための道具である。デスクトップの窓で回して見るビューアと、Jupyter のウィジェットもある。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): wgpu 0.19.4 (Vulkan、Metal、DX12 を選ぶ。`Cargo.toml` で `=0.19.4` に固定)。窓は winit 0.29。オフスクリーン (headless) の描画は `Scene`、`Session`、`TerrainRenderer` で行う
- 2D / 2.5D (傾き・回転) / 3D: 3D (地形の斜めからの眺め、平面図、地球儀の ORBIS)。主題のラスタ (人口、土地被覆) を高さと色で立てる 2.5D の表現もある
- 地球儀表示: あり (ORBIS。変更履歴に、地球儀の LOD を GPU と CPU で一致させた記録がある)
- 対応する投影法: CRS の補助関数がある (README の Data の項)。どの投影で描けるかの一覧は未確認

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 未確認 | README の Data の項に XYZ のタイルの記載は無い。`forge3d[tiles]` の追加の依存は pillow だけ |
| ベクトルタイル (MVT / PMTiles / MLT) | 未確認 | README に記載が無い |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 非対応とみられる | 見た目は Python の API (`RasterHeightSurfaceStyle`、`CategoricalRasterStyle`、`BivariateRasterStyle` など) で指定する (推測: スタイル仕様の読み込みの記載が無い) |
| GeoJSON | 対応 | README の Data の項。ベクターのオーバーレイとして載せる |
| 3D Tiles / glTF | 3D Tiles は対応 | README の Data の項。CityJSON と CityGML (建物の取り込みは Pro 機能) も挙がっている |
| 地形 (標高) | 対応 | GeoTIFF、numpy の配列、COG のストリーミング。大きな範囲はクリップマップ。サンプルの標高は `fetch_dem("rainier")` で取れる |
| 点群 | 対応 | LAZ、COPC、EPT |
| WMS / WMTS | 未確認 | |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリとして禁じる記述は見当たらない。読み込む標高や画像のデータの規約は、データの側で確かめる (geo-software-data)
- API キー・アカウントの要否: 中核は不要。Pro 機能にはライセンスキー (`forge3d.set_license_key(...)` か環境変数 `FORGE3D_LICENSE_KEY`) が要る

## ライセンスと費用

- ライセンス: 中核は Apache-2.0 OR MIT。README は「MapPlate composition, vector export and the building import pipelines are Pro features」と書き、地図の版面の合成 (`MapPlate`)、SVG と PDF のベクター書き出し、建物の取り込みが Pro 機能である
- 利用料 (無料 / 従量 / 有料の機能): 中核は無料。Pro 機能の価格と入手の方法は、公開されていない (README の License の節は「Pro-gated features require a commercial license key」とだけ書く。エラーの文言が案内する URL も README の同じ節。2026-11-13)。作者のサイトは連絡先のメールだけを載せる
- ライセンスキーの仕組み: 鍵は `F3D-<段階>-<顧客>-<期限の日付>-<署名>` の形で、段階は PRO と ENTERPRISE。署名は Ed25519 で、ネットワークに問い合わせずに手元で確かめる。期限の後に 14 日の猶予がある (`python/forge3d/_license.py`)。期限付きなので、作品を作り直す時期に鍵が切れていないかを確かめる
- 版によるライセンスの変化: 未確認 (Pro 機能がいつから入ったかは調べていない)
- 注意: 鍵の確かめのコードも MIT と Apache-2.0 で公開されているが、Pro 機能を鍵なしで使えるように改変してよいかは、コードのライセンスとは別の、商用ライセンスの条件の問題である。条件の文書は見つからなかった。案件で Pro 機能を使うなら、作者に条件を書面で確かめる (geo-software-legal-check)

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 該当しない (Python のパッケージ)。wheel は abi3 (Python 3.10 以上で共通) で、macOS (universal2、x86_64 と arm64)、Linux (manylinux2014 の x86_64 と aarch64)、Windows (amd64) がある (PyPI、1.48.0)
- 扱える地物の数の目安 (公式の記述か、測った条件つき): README のトルコの例は、WorldPop 2020 の約 100 万のセルを立てて 1 回の描画で書き出している。変更履歴には、1500 x 1500 の DEM を 1920 x 1080 で RTX 3070 で描いた数字がある。条件の違う端末での数字は未確認
- 低性能端末での注意: GPU が要る。ソフトウェアの GPU (Linux の llvmpipe や lavapipe、Windows の WARP) でも動くが遅く、CI では 1 件の重い試験に 17 分かかった記録がある。Windows では 1 回の GPU の処理が 2 秒を超えると OS がデバイスを失わせる (TDR) ため、大きな地形では処理を分けて送るように直した (CHANGELOG)

## エコシステム

- 主なプラグイン・拡張: 追加の依存のまとまり (`jupyter`、`datasets`、`raster` で rasterio、pyproj、xarray、rioxarray、dask、`cartopy`、`colormaps`、`all`)
- React / Vue などのラッパー: 該当しない。Jupyter のウィジェットがある (`forge3d[jupyter]`)
- TypeScript の型: 該当しない。Python の型スタブ (`__init__.pyi`) がある
- ネイティブ版・兄弟プロジェクト: リポジトリに WebAssembly 向けのコード (`src/wasm_*.rs`) があり、作者のサイトは「forge3d-web (WebGPU)」でブラウザの対話的な地図を描いている。別のリポジトリ milos-agathon/forge3d-web (MIT、2026-11-13 時点で星 3) があるが、中身は確かめていない
- 日本語の情報 (公式翻訳、国内コミュニティ): 未確認

## 開発の活発さ

- 直近 1 年のリリース数: GitHub のリリースが 40 (1.13.0 の 2026-03-17 から 1.48.0 の 2026-11-09 まで。それ以前の GitHub のリリースは無い)。PyPI の最古の版も 1.13.0
- 最終コミット日: 2026-11-11 (push)
- 近年の大きな破壊的変更: 未確認。1.x の中で、ほぼ週に 1 回以上の頻度で版が上がっている
- 開発の進め方: リポジトリに AGENTS.md と `.claude/` があり、`docs/prompts/` にエージェント向けの指示の文書が多数ある。コーディングエージェントを使って開発していると読める (推測)

## 環境の違いと保守

- ブラウザ間の互換: 該当しない (Python のパッケージ)。決定性の検査の CI に、ヘッドレスの Chrome の WebGPU で同じシェーダーの検査を回す段があり、GitHub の共用のランナーでは SwiftShader (ソフトウェア) で動く (`.github/workflows/determinism-matrix.yml`)
- OS 間の互換: CI のビルドと試験は Windows、Ubuntu、macOS の 3 つ (`.github/workflows/ci.yml`)。Python は 3.10〜3.13 の行列。共用のランナーには本物の GPU が無いので、Windows の自前のランナー (NVIDIA、Vulkan) で物理 GPU の全試験を必須にし、ソフトウェアの GPU で省いた試験はその理由を CI の要約に書く (`.github/workflows/test-python-wheel.yml`)。macOS の共用のランナーの GPU は仮想 (Apple Paravirtual device) で、決定性の検査はそれを拒み、欠けたことを記録する。Intel と AMD の物理 GPU の段は、自前のランナーが無いので参考扱い (`determinism-matrix.yml` の冒頭の説明)。macOS で対話のビューアを試す CI の段がある
- 操作の網羅: デスクトップの窓のビューアで、軌道のカメラを回す操作がある (README の `set_orbit_camera`)。マウス、タッチ、キーボードの操作の一覧は未確認。主な使い方は、操作でなくコードでカメラを置いて書き出すことである
- エッジケースへの対応: CHANGELOG に GPU と OS ごとの修正が多い。Windows の 2 秒の制限でデバイスを失う問題、Metal で長い処理が wgpu 0.19 の待ちの時間切れを超える問題、NVIDIA の Vulkan で大きなポスターの描画が時々デバイスを失う問題、ソフトウェアの Vulkan で 5 秒を超える処理が落ちる問題を直した記録がある。描画の結果を GPU の種類をまたいでビット単位で一致させる検査 (決定性) を持つ
- 継続的な保守: 描画の土台の wgpu を 0.19.4 に固定している。wgpu の最新は 30.0.1 (crates.io、2026-08-22 更新) で、大きく離れている。新しい OS や GPU のドライバーへの追随は、wgpu を上げずに forge3d の側で回避を重ねる形になっている (CHANGELOG の Metal の待ちの修正など。推測を含む)。issue は 7 件と少なく (開いているもの 3 件)、タイトルに OS や GPU の名前を含む issue は 0 件、PR は 294 件 (GitHub の検索、2026-11-13)。外部の利用者からの不具合の報告は少なく、作者の手元と CI で見つけて直していると読める (推測)。実質 1 人の保守で、作者が離れたときの引き継ぎ手は見当たらない

## 向いている場面

- Python で、地形や主題のラスタ (人口、土地被覆、気候) を 3D にした地図の作品を、印刷や動画の品質で書き出したい場合
- 報道、ポスター、SNS 向けの地図の静止画や、時間を進めた動画 (フレームを書き出して ffmpeg でつなぐ) を、コードで再現できる形で作りたい場合
- Jupyter で、地形のデータを 3D で確かめながら分析したい場合

## 向いていない場面

- 利用者がブラウザやスマートフォンで操作する地図の画面を作る場合 (Web の地図ライブラリやネイティブの SDK を使う)
- ベクトルタイルと配色の仕様 (MapLibre Style など) で作った地図を、そのまま描きたい場合 (スタイル仕様の読み込みは確かめられなかった)
- GPU の無いサーバーで大量に描く場合 (ソフトウェアの GPU で動くが、遅い)
- SVG や PDF での書き出し、版面の合成、建物の取り込みを使いたいが、商用ライセンスの条件と価格を確かめられない場合

## 出典

- https://github.com/milos-agathon/forge3d (README、LICENSE、LICENSE-APACHE、Cargo.toml、CHANGELOG.md、python/forge3d/_license.py、.github/workflows/ci.yml、test-python-wheel.yml、determinism-matrix.yml。2026-11-13)
- https://pypi.org/project/forge3d/ (版、wheel、Python の版、追加の依存。2026-11-13)
- https://milosgis.com/ (作者のサイト。2026-11-13)
- https://crates.io/crates/wgpu (wgpu の最新の版。2026-11-13)
