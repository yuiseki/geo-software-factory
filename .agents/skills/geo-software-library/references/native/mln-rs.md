# mln-rs

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 0.0.10 (crates.io、2026-11-06)。main の `Cargo.toml` は 0.0.11 で、まだ出ていない。0.0.x で、API は固まっていない (https://crates.io/crates/mln-rs 、https://github.com/louwers/mln-rs/releases) |
| リポジトリ | https://github.com/louwers/mln-rs (旧名 maplibre-native-next。旧名の URL はこのリポジトリに転送される) |
| ドキュメント | https://docs.rs/mln-rs 、ブラウザ版のデモ https://louwers.github.io/mln-rs/ 、`examples/web/README.md` |
| ライセンス (LICENSE ファイルで確かめる) | BSD-2-Clause (LICENSE.md。著作権の表示は MapLibre contributors、MapTiler.com、Mapbox で、MapLibre Native と同じ)。`vendor/` の移植 (earcut、geojson-vt、kdbush など) は、それぞれのライセンスのファイルを同梱する (`Cargo.toml` の説明) |
| 運営主体・ガバナンス | 個人のアカウント (louwers) のリポジトリで、MapLibre の組織の下ではない。コミットは sargunv が 121 件、louwers が 84 件、johncarmack1984 が 11 件 (GitHub の contributors、2026-11-13)。sargunv と louwers は、どちらも MapLibre の GitHub 組織の公開メンバーである (GitHub の API、2026-11-13) |

## 概要

MapLibre Native の地図の描画の中核 (C++) を、Rust に移したもの (README の「A Rust port of the MapLibre Native map rendering core」)。スタイルの式、タイルの取り込み、ラベルの配置、描画を Rust で持ち、描画の土台を複数持つ。同じコードをブラウザ向け (WebAssembly) にも出しており、デモはブラウザの WebGPU で描き、WebGPU が無ければ WebGL2 で描く。デスクトップの窓の例 (`examples/desktop`) もある。

移した結果が C++ と同じかは、別のリポジトリの差分テスト (louwers/mln-rs-difftests) で、出した版の crate と、移す前の C++ のコードに同じ入力を与え、同じ結果を求めて確かめている。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): 土台が 5 つある。wgpu を通した WebGPU (`mln_webgpu`)、Vulkan (`mln_vulkan`)、Metal (`mln_mtl`)、OpenGL ES 3.0 と WebGL2 (`mln_gl`)。描画の土台は環境変数 `MLN_RENDER_BACKEND` で選ぶ。画面の無い描画 (`mln_headless`) と、C から呼ぶための ABI (`mln_c`) がある
- 2D / 2.5D (傾き・回転) / 3D: MapLibre Native の移植なので 2.5D と考えられる (推測)。ファイルの名前に、建物の立ち上げ (fill-extrusion)、陰影 (hillshade)、地形の色 (color-relief)、地球儀 (globe) が見える。どこまで動くかは確かめていない
- 地球儀表示: `globe` を含むファイルが多数ある。動作は未確認
- 対応する投影法: 未確認

## 対応するデータ

ファイルの名前と依存から読んだもので、どの機能がどこまで動くかは確かめていない。

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | あると考えられる | ブラウザ版の README が raster のタイルを Web Worker で復号すると書く |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT はあると考えられる。PMTiles と MLT はファイルと依存がある | MLT は `mlt-core` 0.22 に依存する (`Cargo.toml` の注記)。PMTiles の名前のファイルがある |
| スタイル仕様 (MapLibre/Mapbox Style 等) | MapLibre Style | スタイルの式の試験 (`tools/expression-test`) と描画の試験 (`tools/render-test`) がある |
| GeoJSON | あると考えられる | geojson と geojson-vt の移植を持つ |
| 3D Tiles / glTF | 未確認 | |
| 地形 (標高タイル) | raster-dem があると考えられる | ブラウザ版の README が raster-dem のタイルを、隣のタイルから縁を埋めて渡すと書く |
| WMS / WMTS | 未確認 | |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリとして禁じる記述は見当たらない。Mapbox のタイルをモバイルアプリで使うことは、Mapbox の規約で Mapbox の SDK に限られる (geo-software-infra の mapbox)。MapLibre Native と同じ扱いになる
- API キー・アカウントの要否: 不要

## ライセンスと費用

- ライセンス: BSD-2-Clause。コピーレフトではない。組み込み、改変、配布、SaaS のいずれも、著作権の表示と免責の文を残せばよい
- 利用料 (無料 / 従量 / 有料の機能): 無料
- 版によるライセンスの変化: 未確認 (若いリポジトリ)

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 未確認。ブラウザ版は WebAssembly のモジュールを 1 つ読み、WebGPU 版と WebGL2 版のどちらか一方だけを読む。フォントの形を作る別のモジュールは、フォントを使うスタイルのときだけ読む (`examples/web/README.md`)
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 未確認。ベンチマークの道具 (`tools/bench`) と、コミットどうしを比べる手順 (`just bench-compare`) がある
- 低性能端末・モバイルブラウザでの注意: ブラウザ版はスレッドと共有メモリを使わない (COOP と COEP のヘッダが要らない)。地図とタイルの処理を Web Worker に分ける。モバイルの端末での動作は未確認

## エコシステム

- 主なプラグイン・拡張: 該当するものは見当たらない。crate は `mln-rs-*` に分かれていて、利用者は `mln-rs` だけに依存する
- React / Vue などのラッパー: 無い。ブラウザ版は wasm-bindgen の JavaScript から使う
- TypeScript の型: ブラウザ版のページは、wasm-bindgen が出す型に対して TypeScript で検査している (CI の web の段)
- ネイティブ版・兄弟プロジェクト: MapLibre Native (C++) が元。C の ABI があり、他の言語から呼ぶ道がある (推測: 使い方の文書は確かめていない)
- 日本語の情報 (公式翻訳、国内コミュニティ): 無い

## 開発の活発さ

- 直近 1 年のリリース数: 4 (crates.io の 0.0.7 から 0.0.10。すべて 2026-11-06)。リポジトリの作成は 2026-11-03 で、それ以前の歴史は旧名の maplibre-native-next にある
- 最終コミット日: 2026-11-12 (push)。コミットは約 220 件
- 近年の大きな破壊的変更: 0.0.x のため、版ごとに変わりうる
- 開発の進め方: リポジトリに AGENTS.md がある。PR は準備ができるまで下書きにし、性能の変化をうたう PR には測定を、見た目を変える PR には前後のスクリーンショットを付けると決めている

## 環境の違いと保守

- ブラウザ間の互換: CI の web の段で、ブラウザ版を Playwright の Chromium (版を固定、SwiftShader) で動かし、描画の試験の場面を、ネイティブ (lavapipe) で描いた絵と 1 枚ずつ比べる。WebGPU 版と WebGL2 版の 2 回 (`.github/workflows/ci.yml`)。Firefox と Safari は CI に無い
- OS 間の互換: CI は Ubuntu 26.04 と macOS 26 だけ。Ubuntu では、wgpu (Vulkan の lavapipe)、Vulkan (検証の層で誤りがあれば止める)、OpenGL ES 3.0 (Mesa の llvmpipe) の 3 つ。macOS では、wgpu (Metal) と Metal (API の検証を有効) の 2 つ。どれもソフトウェアか CI の GPU で、物理の GPU の段は無い。Windows、Android、iOS は CI に無い (`.github/workflows/ci.yml`)。C++ との差分テストは、多くの比較を Linux の結果に固定し、macOS では飛ばす (louwers/mln-rs-difftests の README)
- 操作の網羅: 操作の crate (`mln_gestures`) がある。どの操作に対応するかは未確認
- エッジケースへの対応: MapLibre Native の描画の試験とクエリの試験を、Rust でも同じ試験の集合で回す。タイルの処理を Worker に分けて受け渡しの形 (codec) を通した場合でも、もう一度回す。行の網羅率を Codecov に上げる。最古の対応の Rust (1.98) でもビルドする (`ci.yml`)。C++ の元のコードと結果が一致するかは、差分テストで見る
- 継続的な保守: 試験と検証の仕組みは厚いが、リポジトリは作られて 10 日で、公開の利用者や不具合の報告はまだ少ない (issue 15 件、PR 190 件。GitHub の検索、2026-11-13)。主な開発者は 2 人。MapLibre の組織のプロジェクトではないので、MapLibre Native のような組織としての保守の約束は無い

## 向いている場面

- Rust のアプリ (デスクトップ、サーバー、ゲームエンジン) に、MapLibre Style の地図を、C++ のビルドを持ち込まずに組み込みたい場合
- サーバーで、画面無しで地図の画像を描きたい場合 (headless の crate と、Vulkan、OpenGL、WebGPU の土台がある)
- 同じ描画のコードを、ネイティブとブラウザ (WebGPU、WebGL2) の両方で使いたい場合
- MapLibre Native の中身の移植や、描画の土台の実験に関わりたい場合

## 向いていない場面

- 製品として出す Android や iOS のアプリ (CI に無く、0.0.x。MapLibre Native を使う)
- Windows で動かすことが必須の製品 (CI に無い)
- API の安定と長い保守の約束が要る受託の納品 (0.0.x で、組織のプロジェクトではない)
- Web の地図の画面だけを作る場合 (MapLibre GL JS の方が、文書、プラグイン、利用者の数で厚い)

## 出典

- https://github.com/louwers/mln-rs (README、AGENTS.md、LICENSE.md、Cargo.toml、examples/web/README.md、.github/workflows/ci.yml、ファイルの一覧。2026-11-13)
- https://github.com/louwers/mln-rs-difftests (README。2026-11-13)
- https://crates.io/crates/mln-rs (版と公開日。2026-11-13)
- GitHub の API (contributors、issue と PR の数、MapLibre の組織の公開メンバー。2026-11-13)
