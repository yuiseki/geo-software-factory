# 作法の出典

2026-11-13 に、ライセンスを確かめた非 GPL のライブラリとアプリのリポジトリを読んで集めた。すべて許容的なライセンス (BSD、MIT、Apache-2.0、matplotlib の PSF 型) である。GPL 系のもの (research-competitor のカードの uMap、StreetComplete、Every Door、MapComplete など) は読んでいない。コードは写さず、何をしているかを自分の言葉で書いた。パスは各リポジトリの中の場所で、`(確)` を付けたものは、このスキルを書くときに原典を開いて確かめた。ほかは調査の報告から写したもので、版が進むと場所が変わることがある。

## Web の地図ライブラリ

| リポジトリ | 作法 | 場所 |
|---|---|---|
| maplibre/maplibre-gl-js (BSD-3-Clause) | 試験のスタイルの URL を手元のサーバーに書き換える | `test/integration/lib/localize-urls.ts` (確) |
| 同 | Chromium を SwiftShader で起動する設定 | `test/integration/lib/puppeteer_config.ts` (確、ファイルの存在) |
| 同 | 描画の試験 (事例ごとのスタイルと期待の画像、環境ごとに複数の期待の画像、失敗時の再試行とログ) | `test/integration/render/render.test.ts`、`test/integration/README.md` |
| 同 | ブラウザでの操作、WebGL のコンテキストの喪失と復帰 | `test/integration/browser/browser.test.ts` |
| 同 | 式の仕様の試験 | `test/integration/expression/expression.test.ts` (式の事例は maplibre-style-spec) |
| 同 | エージェントが試験を書くときの決まり (通信は層で差し替える、回帰の試験は直す前に落ちる) | `AGENTS.md` |
| Leaflet/Leaflet (BSD-2-Clause) | 配布物の大きさを基準の枝と比べ、上限を超えたら落とす | `build/size.js` (確) |
| 同 | 偽の時計で CSS の遷移も止める、ポインターの合成 | `spec/suites/SpecHelper.js` |
| 同 | タイルの URL の確かめと data URI のタイル | `spec/suites/layer/tile/TileLayerSpec.js` |
| 同 | 縮めた配布物に対する試験、ツリーシェイキングの試験 | `spec/dist.js`、`spec/tree_shaking.js` |
| openlayers/openlayers (BSD-2-Clause) | 試験のあとにページに `<div>` が残っていたら落とす | `test/browser/test-extensions.js` (確) |
| 同 | WMS や ArcGIS の偽のエンドポイント | `test/browser/vite-plugin-ol-fixtures.mjs` |
| 同 | Node の試験とブラウザの試験を分ける、試験の書き方の決まり | `test/README.md` |
| CesiumGS/cesium (Apache-2.0) | WebGL を要る試験を分け、CI では WebGL の代役で動かす | `Specs/getWebGLStub.js`、`Documentation/Contributors/TestingGuide/README.md` |
| 同 | 例のページを時計を止めて全部撮る | `Specs/e2e/playwright.config.js`、`sandcastle.spec.js` |
| visgl/deck.gl (MIT) | MapLibre の 4、5、6 で試す (npm の別名) | `modules/maplibre/package.json` |
| 同 | 下流のアプリ向けの試験の道具 | `modules/test-utils/src/snapshot-test-runner.ts`、`docs/api-reference/test-utils/overview.md` |
| maplibre/navara (MIT OR Apache-2.0) | MapLibre GL JS の描画の事例を、コミットを固定して使い回す | `maplibre.lock.json`、`supported.json` |

## ネイティブ、Rust、Python

| リポジトリ | 作法 | 場所 |
|---|---|---|
| maplibre/maplibre-native (BSD-2-Clause) | 試験のデータを SQLite のキャッシュに入れ、ネットワークは明示の印のときだけ | `metrics/cache-style.db` |
| 同 | 描画の試験と、環境ごとの期待 | `render-test/runner.cpp`、`metrics/` の環境ごとの設定 |
| louwers/mln-rs (BSD-2-Clause) | Mesa の lavapipe を版を固定して入れ、Vulkan の検証の層で誤りがあれば止める | `.github/actions/lavapipe/action.yml`、`.github/workflows/ci.yml` |
| 同 | 比較の仕組みの自己検査 (期待の画像を実際の出力として流す) | `tools/render-test/tests/self_check.rs` (確、ファイルの存在) |
| 同 | 本数が減る方向にだけ動く上限 (panic の箇所) | `tools/ratchet/ratchet.py`、`tools/ratchet/baseline.toml` (確、ファイルの存在) |
| 同 | 落ちると分かっている一覧が、通ったら落ちる | `rust-port.json`、`tools/c-abi-test` |
| 同 | 速さの比較を交互に測って統計で判定 | `tools/bench` |
| louwers/mln-rs-difftests (BSD-2-Clause) | 元の C++ と同じ入力で結果が一致するかの差分の試験 (生成した入力と境目の入力) | `difftest/` (README) |
| maplibre/maplibre-native-rs (Apache-2.0) | `.invalid` の宛先と差し込める取得の部品 | `tests/file_source_cache.rs` |
| 同 | 子のタイルを親のタイルの 4 分の 1 と比べる性質の試験 | `tests/image_renderer.rs` |
| reearth/ezu (MIT OR Apache-2.0) | 隣り合うタイルの境目の試験 | `fill_dabs_seam.rs` |
| 同 | 乱数の配置を対照と比べる統計の試験 | `point_scatter_randomness.rs` |
| 同 | 試験のデータの出どころの一覧 | `crates/ezu-translate/tests/fixtures/SOURCES.md` |
| milos-agathon/forge3d (中核は Apache-2.0 OR MIT) | 走らせない試験の台帳 (担当と期限) | `tests/UNRUN.toml` (確) |
| 同 | 描画の土台ごとの期待の画像、違う土台の期待との照合を拒む | `tests/_golden_variants.py` (確、ファイルの存在) |
| 同 | GPU の種類をまたいだ描画の決定性 | `.github/workflows/determinism-matrix.yml` |
| opengeos/RustGIS (Apache-2.0) | 別の GIS (GEOS、GeographicLib) で期待値を作り、作り直して違えば落とす | `crates/analysis/tests/reference/generate.py` (確)、`crates/analysis/tests/reference.rs` |
| 同 | 手元の OGC のサーバーで要求を記録する | `ogc_server.rs` |
| 同 | ファジング、展開の爆発のメモリの試験 | `.github/workflows/fuzz.yml`、`crates/tiles/tests/picture_probe_memory.rs` |
| 同 | 依存のライセンスの関門 | `deny.toml` |
| geopandas/geopandas (BSD-3-Clause) | 任意の依存を 1 つずつ外した段、最小の版の段 | `.github/workflows/tests.yaml`、`ci/envs/` (`313-no-optional-deps.yaml` など) (確) |
| 同 | 結合の試験が飛ばされたら落とす、CI では試験のデータを必須にする | `geopandas/conftest.py`、`tests.yaml` の PostGIS の段 |
| SciTools/cartopy (BSD-3-Clause) | ソケットを使えなくした段で、通信の印の付け忘れを見つける | `.github/workflows/ci-testing.yml`、`lib/cartopy/tests/conftest.py` |
| matplotlib/matplotlib (PSF 型) | 警告を誤りにする、試験の前にフォントと設定をそろえる、最小の版の段 | `pytest.ini`、`lib/matplotlib/testing/conftest.py`、`ci/minver-requirements.txt` |
| python-visualization/folium (MIT) | 文書の例を本物のブラウザで開いてコンソールを見る、下流 (GeoPandas) の試験を回す | `.github/workflows/test_selenium.yml`、`test_geopandas.yml` |

## OSS の地図アプリ (research-competitor のカードから)

| リポジトリ | 作法 | 場所 |
|---|---|---|
| geolens-io/geolens (Apache-2.0) | 本番と同じ構成を Docker で立て、Playwright で煙の試験 | `.github/workflows/prod-smoke.yml` (確) |
| 同 | ブラウザをまたぐ全部の E2E は毎晩、秘密の漏れの検査 (gitleaks) | `.github/workflows/ci.yml` (確) |
| gsi-cyberjapan/gsi-3d-2025 (BSD-2-Clause) | ビルド、lint、整形、カバレッジつきの単体の試験を別の段に | `.github/workflows/base-check.yml` (確) |
| nanase/kokudo-map (MIT) | 単体の試験、仕様と文書の検査、データを作る Python の構文と lint | `.github/workflows/check.yml` (確) |
| openinframap/openinframap (BSD-3-Clause) | 開発サーバーを立て、待ってから試験を当てる | `.github/workflows/web.yml` (確) |
| open-geocode-rs/open-geocode (MIT) | 依存のライセンスの一覧を作れなければ落とす | `.github/workflows/ci.yml` (確) |

## 調べた範囲で、どこもしていなかったこと

調べた 6 つの Web の地図ライブラリには、自動のファジング、アクセシビリティの自動の試験、速さの退行の関門が無かった。メモリのリークの自動の検査は、OpenLayers の残った `<div>` の検査だけだった (2026-11-13)。
