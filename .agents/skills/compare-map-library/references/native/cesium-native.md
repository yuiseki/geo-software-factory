# Cesium Native

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (プラットフォームごと、リリース日) | Cesium Native: v0.66.0 (2026-11-02、GitHub Releases は使わずタグと CHANGES.md で版を出す) ([CHANGES.md](https://github.com/CesiumGS/cesium-native/blob/main/CHANGES.md))。Cesium for Unreal: v2.31.0 (2026-11-02、Unreal Engine 5.6 / 5.7 / 5.8 向け) ([cesium-unreal Releases](https://github.com/CesiumGS/cesium-unreal/releases/tag/v2.31.0))。Cesium for Unity: v1.26.1 (GitHub Release は 2026-10-29) ([cesium-unity Releases](https://github.com/CesiumGS/cesium-unity/releases/tag/v1.26.1)) |
| リポジトリ | https://github.com/CesiumGS/cesium-native 、https://github.com/CesiumGS/cesium-unreal 、https://github.com/CesiumGS/cesium-unity |
| ドキュメント | https://cesium.com/learn/cesium-native/ref-doc/ |
| ライセンス | Apache-2.0 (Cesium Native、Cesium for Unreal、Cesium for Unity とも)。商用・非商用とも無料 ([README](https://github.com/CesiumGS/cesium-native)) |
| 運営主体 | Cesium GS, Inc. (GitHub の CesiumGS organization) |

## 概要

3D Tiles のストリーミング、glTF の読み書き、WGS84 楕円体を含む高精度の地理空間計算、WMS / TMS / WMTS などのラスターを 3D タイルセットに貼り付ける機能を持つ C++ ライブラリ群である ([README](https://github.com/CesiumGS/cesium-native))。自身では描画せず、ゲームエンジンなどの描画側が `IPrepareRendererResources` を実装してタイルを描画用の資源に変換する ([IPrepareRendererResources.h](https://github.com/CesiumGS/cesium-native/blob/main/Cesium3DTilesSelection/include/Cesium3DTilesSelection/IPrepareRendererResources.h))。Cesium for Unreal、Cesium for Unity、Cesium for Omniverse、Cesium for O3DE の土台であり、地図アプリに組み込む場合は通常これらのプラグインを経由する ([README](https://github.com/CesiumGS/cesium-native))。1.0 前で、後方互換のための非推奨期間を設けず破壊的変更を入れる方針である ([README](https://github.com/CesiumGS/cesium-native))。

## 対応プラットフォーム

| プラットフォーム | 対応 | 最低 OS 版・備考 |
|---|---|---|
| Android | Unreal / Unity 経由で対応 | Cesium for Unreal v2.31.0 は Android を対象に含む。Cesium for Unity は Android (ARM64、x86-64) ([cesium-unreal v2.31.0](https://github.com/CesiumGS/cesium-unreal/releases/tag/v2.31.0)、[cesium-unity README](https://github.com/CesiumGS/cesium-unity))。最低 OS 版は未確認 |
| iOS | Unreal / Unity 経由で対応 | Cesium for Unreal v2.31.0、Cesium for Unity とも iOS を対象に含む。最低 OS 版は未確認 |
| デスクトップ (macOS / Windows / Linux) | 対応 | Cesium Native 自体は Visual Studio 2019 以上、GCC 11 以上、Clang 12 以上と CMake 3.15 以上でビルドする ([developer-setup.md](https://github.com/CesiumGS/cesium-native/blob/main/doc/topics/developer-setup.md))。Cesium for Unreal は Windows / Linux / macOS、Cesium for Unity は Windows (x86-64)、macOS (x86-64、Apple Silicon)、UWP |
| ゲームエンジン (Unreal / Unity など) | 対応 (主用途) | Cesium for Unreal: Unreal Engine 5.6 / 5.7 / 5.8 (v2.31.0)。古い UE には対応する旧版がある (例: UE 5.5 は v2.28.0 まで) ([cesium-unreal README](https://github.com/CesiumGS/cesium-unreal))。Cesium for Unity: Unity 2022.3 以上 ([package.json](https://github.com/CesiumGS/cesium-unity/blob/main/package.json))、Web は Unity 6 以上のみ。他に Omniverse、O3DE の公式統合と、Godot、VulkanSceneGraph、osgEarth、Dart/Flutter、Python などのコミュニティ統合がある ([README](https://github.com/CesiumGS/cesium-native)) |

- UI フレームワーク (Jetpack Compose / SwiftUI / Flutter / React Native) への対応 (公式か非公式か): Compose / SwiftUI / React Native への公式の統合は無い。Flutter (Dart) はコミュニティの [cesium_3d_native](https://github.com/odd-io/cesium_3d_native) が Cesium Native を包んでいる (非公式、[README](https://github.com/CesiumGS/cesium-native))。モバイルアプリでは Unreal / Unity のアプリとして組むのが公式の経路である。

## 描画方式

- グラフィックス API (OpenGL ES / Metal / Vulkan など): Cesium Native は描画 API を持たず、ホストのエンジンに任せる ([IPrepareRendererResources.h](https://github.com/CesiumGS/cesium-native/blob/main/Cesium3DTilesSelection/include/Cesium3DTilesSelection/IPrepareRendererResources.h))。実際の API は Unreal / Unity のプラットフォームごとの設定で決まる。
- 2D / 2.5D / 3D、地球儀: 3D の地球儀が前提。WGS84 楕円体上に 3D Tiles と地形を置く ([README](https://github.com/CesiumGS/cesium-native))。2D の地図 SDK のような平面表示は主用途ではない。

## 対応するタイル・データ

- 表示できるタイル・地図データ: 3D Tiles、glTF (Draco 圧縮などの拡張、`KHR_gaussian_splatting` と SPZ 圧縮を含む)、quantized-mesh-1.0 の地形 ([README](https://github.com/CesiumGS/cesium-native)、[CHANGES.md](https://github.com/CesiumGS/cesium-native/blob/main/CHANGES.md))。ラスターの貼り付け元は WMS、TMS、WMTS、URL テンプレート、Bing Maps、Azure Maps、Google の Map Tiles、Cesium ion ([CesiumRasterOverlays](https://github.com/CesiumGS/cesium-native/tree/main/CesiumRasterOverlays/include/CesiumRasterOverlays))。GeoJSON などのベクターデータはラスターにして重ねる (CesiumVectorData、CesiumVectorOverlays)。Bentley iTwin の取得機能もある。
- 組み合わせの制約 (特定のタイルでしか使えない等): 特定の提供元に縛られない。Cesium ion は使える配信元の一つで必須ではない。MVT などのベクタータイルを直接描く機能の記載はない。
- オフライン地図: 未確認。

## ライセンスと費用

- SDK 自体のライセンス: Apache-2.0。商用・非商用とも無料 ([README](https://github.com/CesiumGS/cesium-native))。
- 従量課金 (MAU、地図ロードなど、単価と無料枠): SDK 自体には無い。Cesium ion を配信元に使う場合の料金 (USD、2026-11-10 確認): Community は無料で保存 10 GB・配信月 15 GB、個人・非商用向け (FAQ では商用の試作は可)。Commercial は月 $149 (個人) / $524 (チーム) で保存 100 GB・配信月 150 GB。Premium は月 $499 (個人) / $874 (チーム) で保存 500 GB・配信月 500 GB。Custom と Self-Hosted は要問い合わせ ([Cesium 料金](https://cesium.com/pricing/))。Google Photorealistic 3D Tiles などを使う場合は、その提供元の料金がかかる。

## Web 版との関係

- 同じスタイル仕様・同じ API の Web 版: Web 版にあたるのは CesiumJS で、同じ 3D Tiles を扱うが、別の JavaScript 実装であり Cesium Native の API とは共有しない (CesiumJS は Cesium Native の README の統合一覧に含まれない、[README](https://github.com/CesiumGS/cesium-native))。Cesium for Unity は Unity 6 以上で Web 向けビルドにも対応する ([cesium-unity README](https://github.com/CesiumGS/cesium-unity))。

## 開発の活発さ

- 直近 1 年のリリース数: Cesium Native は 2025-11-10 から 2026-11-10 に v0.54.0 から v0.66.0 まで 13 版 (ほぼ毎月 1 日前後) ([CHANGES.md](https://github.com/CesiumGS/cesium-native/blob/main/CHANGES.md))。同期間の GitHub Releases は Cesium for Unreal 14 件、Cesium for Unity 12 件。
- 最終コミット日: Cesium Native 2026-11-09、Cesium for Unreal 2026-11-09、Cesium for Unity 2026-11-06 (いずれも main ブランチ)。

## Cesium for Unity / Unreal

<!-- 追記テンプレート: この節の [記入] だけを埋める -->
- 何をするプラグインか、最新の版、対応するエンジンの版: [記入]
- ライセンスと費用 (プラグイン、Cesium ion、Google 3D Tiles): [記入]
- 配布元 (Fab、Unity Asset Store、GitHub): [記入]
- Google Photorealistic 3D Tiles や PLATEAU を読み込む手順の有無: [記入]

## 向いている場面

- 3D 都市モデル、点群、写実的な 3D タイル、地形を地球儀上で扱うアプリ。
- Unreal Engine や Unity でシミュレーション、デジタルツイン、XR を作る場合。
- 3D Tiles を独自のエンジンに読み込みたい場合 (C++ で描画側を実装する)。

## 向いていない場面

- 一般的な 2D の地図アプリ (ベクタータイルのスタイル描画、道路地図の表示)。
- Compose / SwiftUI のネイティブ UI に軽量な地図を埋め込みたい場合 (Unreal / Unity のアプリになる)。
- API の安定性を重視する場合 (1.0 前で、予告なく破壊的変更が入る方針)。

## 出典

- https://github.com/CesiumGS/cesium-native
- https://github.com/CesiumGS/cesium-native/blob/main/CHANGES.md
- https://github.com/CesiumGS/cesium-native/blob/main/doc/topics/developer-setup.md
- https://github.com/CesiumGS/cesium-native/blob/main/Cesium3DTilesSelection/include/Cesium3DTilesSelection/IPrepareRendererResources.h
- https://github.com/CesiumGS/cesium-native/tree/main/CesiumRasterOverlays/include/CesiumRasterOverlays
- https://cesium.com/learn/cesium-native/ref-doc/
- https://github.com/CesiumGS/cesium-unreal
- https://github.com/CesiumGS/cesium-unreal/releases/tag/v2.31.0
- https://github.com/CesiumGS/cesium-unity
- https://github.com/CesiumGS/cesium-unity/releases/tag/v1.26.1
- https://github.com/CesiumGS/cesium-unity/blob/main/package.json
- https://github.com/odd-io/cesium_3d_native
- https://cesium.com/pricing/

## 未確認のこと

- Unreal / Unity 経由で動かす場合の Android / iOS の最低 OS 版。プラグインのドキュメントで記載を確かめていない。
- オフライン利用 (ローカルのタイルセットを読む方法と、Cesium ion のデータを端末に保存してよいかの規約)。調べきれなかった。
- Cesium for Unreal / Unity の Fab や Unity Asset Store での配布条件。GitHub のライセンス (Apache-2.0) のみ確かめた。
