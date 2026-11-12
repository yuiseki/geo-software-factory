# maplibre-native-rs (crate: maplibre_native)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 0.10.0 (crates.io と GitHub、2026-10-02)。0.x 系 (https://crates.io/crates/maplibre_native 、https://github.com/maplibre/maplibre-native-rs/releases) |
| リポジトリ | https://github.com/maplibre/maplibre-native-rs |
| ドキュメント | https://docs.rs/maplibre_native 、README |
| ライセンス (LICENSE ファイルで確かめる) | Apache-2.0 (GitHub の判定と README のバッジ)。中で使う MapLibre Native の中核は BSD-2-Clause |
| 運営主体・ガバナンス | MapLibre の組織のリポジトリ。コミットは CommanderStorm が 73 件、ciscorn が 39 件、nyurik が 24 件など (dependabot を除く。GitHub の contributors、2026-11-13) |

## 概要

MapLibre Native (C++) の地図の描画エンジンを、Rust から使うためのバインディング。描画そのものは MapLibre Native の C++ の中核 (静的ライブラリ) が行い、Rust の側は呼び出しの層を持つ。描き方は 3 つあり、決まったカメラで 1 枚を描く static、対話のための continuous、タイルの配信のための tile である (README)。

Rust に移した [mln-rs](mln-rs.md) とは違い、C++ の中核をそのまま使う。描画の結果は MapLibre Native と同じになる一方、ビルドに C++ の中核が要る。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): MapLibre Native の Vulkan、Metal、OpenGL の土台を、cargo の feature で選ぶ (`vulkan` は Linux と Windows の既定、`metal` は macOS と iOS の既定、`opengl`)。Linux の OpenGL は、画面の無い描画のために EGL を使う。X11 の GLX は `glx` の feature で選ぶ
- 2D / 2.5D (傾き・回転) / 3D: MapLibre Native と同じ (2.5D)
- 地球儀表示: MapLibre Native に従う。バインディングから使えるかは未確認
- 対応する投影法: MapLibre Native に従う

## 対応するデータ

MapLibre Native の中核が描くので、MapLibre Native で描けるもの (MapLibre Style、ベクトルタイル、ラスタタイル、GeoJSON、raster-dem) を描ける (推測: バインディングがどこまで API を出しているかは確かめていない)。スタイルは URL か JSON から読む (`json` の feature、既定で有効)。GeoJSON は `geojson` の crate とやりとりできる (`geojson` の feature)。

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: MapLibre Native と同じ。Mapbox のタイルをモバイルアプリで使うことは、Mapbox の規約で Mapbox の SDK に限られる (geo-software-infra の mapbox)
- API キー・アカウントの要否: 不要

## ライセンスと費用

- ライセンス: Apache-2.0 (バインディング) と BSD-2-Clause (中核)。どちらもコピーレフトではない。組み込み、改変、配布、SaaS のいずれも、著作権の表示と、Apache-2.0 の NOTICE などの条件を守ればよい
- 利用料 (無料 / 従量 / 有料の機能): 無料
- 版によるライセンスの変化: 未確認

## 性能と規模

- バンドルサイズ: 該当しない (Rust の crate。中核の静的ライブラリを含む)
- 扱える地物の数の目安: MapLibre Native に従う。バインディングでの測定は未確認
- 低性能端末での注意: GPU の API で描く。GPU の無いサーバーでは、ソフトウェアの Vulkan や OpenGL (Mesa の lavapipe や llvmpipe) が要る (推測: CI の環境から)

## エコシステム

- 主なプラグイン・拡張: 無い
- React / Vue などのラッパー: 該当しない
- TypeScript の型: 該当しない
- ネイティブ版・兄弟プロジェクト: MapLibre Native が元。CI で Slint (Rust の GUI のライブラリ) の例をビルドしている (`.github/workflows/ci.yml`)。Rust に移した mln-rs は別のプロジェクト
- 日本語の情報 (公式翻訳、国内コミュニティ): 未確認

## 開発の活発さ

- 直近 1 年のリリース数: 23 (GitHub のリリース。最初は 0.1.1 の 2025-03-07、全部で 30)
- 最終コミット日: 2026-11-09 (push)
- 中核の版の追随: 使う MapLibre Native の版を `Cargo.toml` で決め、毎月 1 日に新しい版を確かめて、あれば PR を作る仕組みがある (README、`.github/workflows/update-maplibre-native.yml`)
- 近年の大きな破壊的変更: 0.x のため、版ごとに変わりうる。未確認

## 環境の違いと保守

- ブラウザ間の互換: 該当しない (ブラウザ版は無い)
- OS 間の互換: README の表では、Linux の x86 と ARM で Vulkan と OpenGL、macOS の ARM で Metal と Vulkan (MoltenVK 経由) を CI で試している。Windows の x86 と ARM は「動くはずだが、今は試していない」で、macOS で OpenGL、Linux と Windows で Metal は使えない (README の Platform Support)。CI の試験の行列は ubuntu-latest (Vulkan、GLX など) と、macOS、ARM の Linux での Slint の例のビルド (`.github/workflows/ci.yml`)
- 操作の網羅: 画像を描く API が中心で、利用者の操作を受ける層は持たない。対話は continuous のモードと、組み込む先 (Slint など) が受け持つ
- エッジケースへの対応: 描画の試験の集合は MapLibre Native の側にあり、README は Metal と Vulkan が上流の試験を通ると書く。バインディングの側の試験の範囲は未確認
- 継続的な保守: MapLibre の組織のプロジェクトで、中核の版を毎月確かめて上げる仕組みを持つ。issue は 25 件 (開いているもの 7 件)、PR は 282 件 (GitHub の検索、2026-11-13)。描画の保守の大部分は MapLibre Native の側にあり、ブラウザや OS の変化への追随も主にそちらで行われる

## 向いている場面

- Rust のサーバーやアプリで、MapLibre Native と同じ見た目の地図の画像やタイルを描きたい場合 (タイルの配信のモードがある)
- Slint などの Rust の GUI に、MapLibre の地図を組み込みたい場合
- C++ の中核をビルドするか、ビルド済みのものを取り寄せることを受け入れられる場合

## 向いていない場面

- ビルドに C++ のツールチェーンを一切持ち込みたくない場合 (Rust だけで描く [mln-rs](mln-rs.md) か、CPU だけで描く [ezu](../server/ezu.md) を比べる)
- Windows が必須の製品 (CI で試していない)
- ブラウザで描きたい場合

## 出典

- https://github.com/maplibre/maplibre-native-rs (README、.github/workflows/ci.yml、update-maplibre-native.yml、リリース。2026-11-13)
- https://crates.io/crates/maplibre_native (版。2026-11-13)
- GitHub の API (contributors、issue と PR の数。2026-11-13)
