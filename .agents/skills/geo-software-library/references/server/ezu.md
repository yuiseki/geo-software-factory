# ezu

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |
| 最新の安定版 (リリース日) | 0.15.0 (GitHub のリリースと crates.io、2026-11-10)。0.x 系 (https://github.com/reearth/ezu/releases 、https://crates.io/crates/ezu) |
| リポジトリ | https://github.com/reearth/ezu |
| ドキュメント | https://reearth.github.io/ezu/ (ガイド、スタイルの仕様、82 の処理の一覧、MapLibre との互換、ギャラリー)、https://docs.rs/ezu |
| ライセンス (LICENSE ファイルで確かめる) | MIT と Apache-2.0 のデュアルライセンス (LICENSE-MIT と LICENSE-APACHE。README の License の節は「either of ... at your option」。GitHub の判定は Apache-2.0) |
| 運営主体・ガバナンス | reearth の組織のリポジトリ (名義は Eukarya, Inc.。https://github.com/reearth)。コミットは rot1024 が 553 件、ほかは 3 件と bot (GitHub の contributors、2026-11-13)。実質 1 人の開発 |

## 概要

ベクトルタイル (MVT と PMTiles) を、GPU を使わずに CPU だけでラスタの画像に描く、純粋な Rust の地図の描画エンジン (README の「pure-Rust, GPU-free CPU renderer」)。2 つの描き方を持つ。

- 絵画風: スタイルは、層の順の一覧ではなく、型付きのノードのグラフで書く。筆のエンジン (hokusai) と約 80 の画像処理で、水彩、水墨、浮世絵のように描く
- MapLibre 互換: `ezu translate` が MapLibre GL のスタイルを ezu のスタイルに変換する。地物ごとに変わる値は MapLibre の式のまま書け、式の評価 (maplibre-expr-rs) は MapLibre の公式の試験の集合に 100 % 合うとうたう

コマンドラインの道具 (`ezu tile`、`ezu bbox`、`ezu frame` で印刷の縮尺と用紙の大きさ、`ezu tiles` で XYZ のピラミッドの一括、`ezu serve` でスタイルの編集画面)、Rust のライブラリ、WebAssembly の npm パッケージ (`@reearth/ezu`)、Go のパッケージがある。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): CPU。GPU も、画面の無いブラウザも使わない。ブラウザでは WebAssembly (scalar、SIMD、Web Worker のスレッドの 3 つのビルド) で描き、PNG、可逆の WebP、RGBA を返す
- 2D / 2.5D (傾き・回転) / 3D: 2D のタイル。カメラが無く、傾けた地図は描かない (下の「MapLibre との違い」)
- 地球儀表示: なし
- 対応する投影法: XYZ のタイル (Web メルカトル) と、経緯度の範囲の画像 (`ezu bbox`)。ほかは未確認

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 (陰影の例がある) | 例のスタイル `hillshade.json` は遠隔のデータだけで描ける (README) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT と PMTiles は対応、MLT は未確認 | MVT は geozero で読む |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 独自のスタイル (ノードのグラフ)。MapLibre GL のスタイルは変換して使う | 変換で近似するもの、飛ばすものは警告に出る (下の「MapLibre との違い」) |
| GeoJSON | 対応 | `ezu-features` |
| 3D Tiles / glTF | 非対応とみられる | 2D の描画器のため (推測) |
| 地形 (標高タイル) | 陰影は描ける | `hillshade-accent-color` は未対応 (gaps-and-differences) |
| WMS / WMTS | 未確認 | |

## MapLibre との違い

公式の文書 (https://reearth.github.io/ezu/maplibre/gaps-and-differences/) から。変換の警告を必ず読む。

- 設計上の違い (変わらない): カメラが無いので、ラベルの衝突は世界の座標で決定的に決まり、画面の中心を優先しない。フェードが無い。`text-overlap: cooperative` は衝突させる扱いになる。ズームは整数で、小数のズームでなめらかに変わるスタイルは段になる。傾きと回転に関わる項目は捨てる
- まだ対応していない: `line-blur`、`line-gradient`、`fill-extrusion` の高さと模様、`text-halo-blur`、`icon-color` と SDF のアイコンの色替え、`text-writing-mode`、`symbol-z-order` など
- 再現の度合い: Protomaps の 68 層のテーマを、変換して ezu で描いた画像と、MapLibre GL JS (ソフトウェアの WebGL) で描いた画像の SSIM は 0.800 (渋谷、z14)、0.874 (東京、z12)、0.846 (z15) (https://reearth.github.io/ezu/maplibre/compatibility/)。見た目を MapLibre GL JS と一致させたい用途には足りないことがある

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリとして禁じる記述は見当たらない。ほかの事業者のタイルを描き直して配るときは、その事業者の規約 (キャッシュ、再配布) に従う (geo-software-infra)
- API キー・アカウントの要否: 不要

## ライセンスと費用

- ライセンス: MIT OR Apache-2.0。コピーレフトではない。組み込み、改変、配布、SaaS のいずれも、著作権の表示と許諾の文を残せばよい
- 利用料 (無料 / 従量 / 有料の機能): 無料。有料版は見当たらない
- 版によるライセンスの変化: 未確認

## 性能と規模

- 公式の測定 (README): Apple M1 で、変換した Protomaps の基本の地図の 512 px のタイルが、1 スレッドで z12〜z15 に 1 枚 約 13〜30 ms、ラベルを含む 68 層の全部で約 42〜105 ms。z13〜z14 の 251 枚を 8 コアで約 9 秒 (1 枚 約 37 ms、HTTP の取得、MVT の復号、PNG の符号化を含む)
- 最初の描画は、グリフと隣のタイルを遅れて取りに行くので、ずっと遅い (README)
- GPU の無いサーバーで動くことが、ほかの描画器との一番の違い

## エコシステム

- 主なプラグイン・拡張: 筆のエンジン hokusai、式の評価 maplibre-expr-rs (どちらも reearth のリポジトリ)
- React / Vue などのラッパー: 無い。npm の `@reearth/ezu` (WebAssembly) を JavaScript から使う
- TypeScript の型: npm のパッケージの型は未確認
- ネイティブ版・兄弟プロジェクト: Go のパッケージ (リポジトリの `go/`)。配布のバイナリは Linux (x86_64、aarch64、gnu と musl)、macOS (x86_64、aarch64)、Windows (x86_64) (`.github/workflows/release.yml`)。macOS は Homebrew でも入る
- 日本語の情報 (公式翻訳、国内コミュニティ): 文書は英語。名前は「絵図」から

## 開発の活発さ

- 直近 1 年のリリース数: 20 (0.2.0 の 2026-05-25 から 0.15.0 の 2026-11-10)。リポジトリの作成は 2026-05-20
- 最終コミット日: 2026-11-10 (push)
- 近年の大きな破壊的変更: 0.x のため、版ごとに変わりうる (CHANGELOG.md がある。中身は確かめていない)

## 環境の違いと保守

- ブラウザ間の互換: WebAssembly のビルド (scalar とスレッド版) を CI で作り、JavaScript からの試験 (`scripts/test-wasm-js.sh`) を回す (`.github/workflows/ci.yml`)。ブラウザごとの試験は CI に無い。スレッド版は、ブラウザで SharedArrayBuffer を使うために COOP と COEP のヘッダが要ると考えられる (推測)
- OS 間の互換: CI の試験は Ubuntu、macOS、Windows の 3 つで、ワークスペース全体をビルドして試験する。musl の Linux 向けのビルドもある (`ci.yml`)。CPU だけで描くので、GPU のドライバーの違いに左右されない
- 操作の網羅: 該当しない (画像を描くもので、地図の操作は持たない。`ezu serve` の編集画面は開発用)
- エッジケースへの対応: タイルの境目で筆とラベルが切れないよう、置き方を世界の座標で決定的にしている (README)。MapLibre との違いは文書に一覧があり、変換は再現できなかったものを警告に出す
- 継続的な保守: 実質 1 人の開発で、issue は 2 件 (開いているもの 0)、PR は 98 件 (GitHub の検索、2026-11-13)。外部からの不具合の報告はまだ少ない。描画をすべて自前で持つので (GPU のドライバーに頼らない代わりに)、MapLibre のスタイル仕様の新しい項目への追随も自前で行う必要がある

## 向いている場面

- GPU の無いサーバーで、ベクトルタイルから地図のタイルや画像を描いて配りたい場合
- 絵画風の地図 (水彩、水墨、鉛筆のスケッチ) を作りたい場合
- 印刷の縮尺と用紙の大きさで、地図の 1 枚を書き出したい場合 (`ezu frame`)
- 同じスタイルで、サーバー (Rust、Go) とブラウザ (WebAssembly) の両方で描きたい場合

## 向いていない場面

- MapLibre GL JS や MapLibre Native と同じ見た目が必要な場合 (変換は近似で、SSIM は 0.80〜0.87。[maplibre-native-rs](../native/maplibre-native-rs.md) か [mln-rs](../native/mln-rs.md) を比べる)
- 傾けた地図、3D、地球儀が要る場合
- 利用者が操作する地図の画面を作る場合 (Web やネイティブの地図ライブラリを使う)

## 出典

- https://github.com/reearth/ezu (README、LICENSE-MIT、LICENSE-APACHE、.github/workflows/ci.yml、release.yml、docs/src/content/docs/maplibre/gaps-and-differences.mdx。2026-11-13)
- https://reearth.github.io/ezu/maplibre/compatibility/ (SSIM の比較。2026-11-13)
- https://crates.io/crates/ezu (版。2026-11-13)
- GitHub の API (contributors、issue と PR の数。2026-11-13)
