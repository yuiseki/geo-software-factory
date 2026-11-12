# MapLibre Native (Android / iOS)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (プラットフォームごと、リリース日) | Android: android-v13.7.1 (2026-10-15)。なお 13.5 系の保守版 android-v13.5.4 が 2026-11-09 に出ている。iOS: ios-v7.0.0 (2026-10-28)。地球儀対応の `-globe` 付きプレリリース (android-v2026.11.2-globe / ios-v2026.11.2-globe、2026-11-02) が別にある ([Releases](https://github.com/maplibre/maplibre-native/releases)) |
| リポジトリ | https://github.com/maplibre/maplibre-native |
| ドキュメント | https://maplibre.org/maplibre-native/android/examples/getting-started/ (Android)、https://maplibre.org/maplibre-native/ios/latest/documentation/maplibre/ (iOS)、https://maplibre.org/maplibre-native/docs/book/ (開発者向け) |
| ライセンス | BSD 2-Clause ([LICENSE.md](https://github.com/maplibre/maplibre-native/blob/main/LICENSE.md)) |
| 運営主体 | MapLibre (GitHub の maplibre organization、maplibre.org)。2020 年 12 月に Mapbox GL Native が非 OSS ライセンスへ移る前の版から分岐したもの ([README](https://github.com/maplibre/maplibre-native)) |

## 概要

MapLibre Style Spec に従うスタイルを読み、ベクタータイル・ラスタータイルを GPU で描画する C++ 製の地図レンダラーと、その Android / iOS 向け SDK である ([README](https://github.com/maplibre/maplibre-native))。Mapbox GL Native の OSS 版から分岐した BSD ライセンスの実装で、地図データの提供元を選ばない。地図データや API キーは同梱されず、タイルとスタイルは利用者が用意する。

## 対応プラットフォーム

| プラットフォーム | 対応 | 最低 OS 版・備考 |
|---|---|---|
| Android | 対応 | `minSdk = 23` (Android 6.0) ([build.gradle.kts](https://github.com/maplibre/maplibre-native/blob/main/platform/android/MapLibreAndroid/build.gradle.kts))。Maven の `org.maplibre.gl:android-sdk` で配布 |
| iOS | 対応 | ios-v7.0.0 で最低 iOS 15.5 に引き上げ ([ios-v7.0.0 リリースノート](https://github.com/maplibre/maplibre-native/releases/tag/ios-v7.0.0))。Swift Package / CocoaPods で配布。UIKit ベース ([README](https://github.com/maplibre/maplibre-native)) |
| デスクトップ (macOS / Windows / Linux) | 対応 (コアのビルド) | Linux / Windows / macOS 向けのビルド手順がある。Node.js 版 `@maplibre/maplibre-gl-native`、Qt 版 (別リポジトリ maplibre-native-qt) もある ([README](https://github.com/maplibre/maplibre-native)、[Platforms](https://maplibre.org/maplibre-native/docs/book/platforms/index.html)) |
| ゲームエンジン (Unreal / Unity など) | 公式の統合なし | README とプラットフォーム表に Unreal / Unity の記載がない |

- UI フレームワーク (Jetpack Compose / SwiftUI / Flutter / React Native) への対応 (公式か非公式か): SDK 本体は Android の View (`MapView`) と iOS の UIKit で、Compose / SwiftUI のビューは本体に含まれない。いずれも maplibre organization 配下の別リポジトリとして提供されている。Compose: MapLibre Compose (Compose Multiplatform、Android / iOS / Desktop / Web、v0.20.0、BSD 3-Clause、[maplibre-compose](https://github.com/maplibre/maplibre-compose))。SwiftUI: MapLibreSwiftUI (v0.26.1、1.0 前で API 安定を約束していない、Stadia Maps から移管、[swiftui-dsl](https://github.com/maplibre/swiftui-dsl))。Flutter: [flutter-maplibre-gl](https://github.com/maplibre/flutter-maplibre-gl)。React Native: [maplibre-react-native](https://github.com/maplibre/maplibre-react-native) (Expo 対応を掲げる)。

## 描画方式

- グラフィックス API (OpenGL ES / Metal / Vulkan など): Android は OpenGL ES 3.0 と Vulkan 1.0、iOS は Metal。WebGPU バックエンドも Android / iOS / Linux / macOS で対応と表にある ([Platforms](https://maplibre.org/maplibre-native/docs/book/platforms/index.html))。Android の既定の成果物 `android-sdk` は Vulkan で、OpenGL ES 版 `android-sdk-opengl`、実行時に両者を切り替える `android-sdk-vulkan-opengl` が別にある ([Artifacts](https://maplibre.org/maplibre-native/android/examples/artifacts/))。
- 2D / 2.5D / 3D、地球儀: 2D の地図に傾き・回転と `fill-extrusion` による建物の押し出しがある (13.7.1 のリリースノートに fill-extrusion の修正がある、[android-v13.7.1](https://github.com/maplibre/maplibre-native/releases/tag/android-v13.7.1))。地球儀はスタイルの `"projection": {"type": "globe"}` で描画する機能が `-globe` 付きのプレリリースで提供されており、安定版にはまだ入っていない ([android-v2026.11.2-globe](https://github.com/maplibre/maplibre-native/releases/tag/android-v2026.11.2-globe))。地形の 3D 表示は未確認。

## 対応するタイル・データ

- 表示できるタイル・地図データ: MapLibre Style Spec のスタイルで、ベクタータイル (MVT)、ラスタータイル、raster-dem、GeoJSON、画像ソースを扱う。PMTiles を `pmtiles://` URL で読み、Android では APK の assets に同梱した PMTiles も読める ([android-v13.7.1](https://github.com/maplibre/maplibre-native/releases/tag/android-v13.7.1))。
- 組み合わせの制約 (特定のタイルでしか使えない等): 特定の提供元に縛られない。スタイルとタイルは利用者が用意する。
- オフライン地図: Android に `OfflineManager` があり、領域を指定したダウンロードができる ([OfflineManager.kt](https://github.com/maplibre/maplibre-native/blob/main/platform/android/MapLibreAndroid/src/main/java/org/maplibre/android/offline/OfflineManager.kt))。PMTiles をアプリに同梱する方法も取れる。

## ライセンスと費用

- SDK 自体のライセンス: BSD 2-Clause ([LICENSE.md](https://github.com/maplibre/maplibre-native/blob/main/LICENSE.md))。
- 従量課金 (MAU、地図ロードなど、単価と無料枠): SDK 自体には無い。費用はタイル配信元 (自前配信や商用タイルサービス) の料金で決まる。

## Web 版との関係

- 同じスタイル仕様・同じ API の Web 版: MapLibre GL JS が同じ MapLibre Style Spec を使う。API はプラットフォームごとに別で、Android (Java/Kotlin) と iOS (Swift/Objective-C) の API は GL JS と一致しない。描画結果を GL JS に合わせる修正が続いている (例: line-pattern の大きさを GL JS に合わせた、[android-v13.7.1](https://github.com/maplibre/maplibre-native/releases/tag/android-v13.7.1))。

## 開発の活発さ

- 直近 1 年のリリース数: 2025-11-10 から 2026-11-10 の GitHub Releases で、Android の安定版 28 件 (プレリリースを含めると 38 件)、iOS の安定版 19 件 (同 28 件) ([Releases](https://github.com/maplibre/maplibre-native/releases))。
- 最終コミット日: 2026-11-09 (main ブランチ)。

## 環境の違いと保守

- ブラウザ間の互換: ネイティブ SDK なので、代わりに描画 API の違いを見る。文書でうたう描画 API は Android が OpenGL ES 3.0 と Vulkan 1.0、iOS が Metal で、WebGPU も表にある ([Platforms](https://maplibre.org/maplibre-native/docs/book/platforms/index.html))。CI で確かめているのは、Android の `opengl`、`vulkan`、`multiBackend` の 3 種のビルドと単体テスト ([android-ci.yml](https://github.com/maplibre/maplibre-native/blob/main/.github/workflows/android-ci.yml))、iOS の Metal ([ios-ci.yml](https://github.com/maplibre/maplibre-native/blob/main/.github/workflows/ios-ci.yml))、Linux の Vulkan と OpenGL (Mesa の lavapipe を使う、[linux-ci.yml](https://github.com/maplibre/maplibre-native/blob/main/.github/workflows/linux-ci.yml))、Windows の OpenGL、EGL、Vulkan ([windows-ci.yml](https://github.com/maplibre/maplibre-native/blob/main/.github/workflows/windows-ci.yml))、macOS の Metal と WebGPU ([macos-ci.yml](https://github.com/maplibre/maplibre-native/blob/main/.github/workflows/macos-ci.yml)) である。Web の対象は無く、Web は MapLibre GL JS の担当である。
- OS 間の互換: 文書でうたう最低版は Android 6.0 (`minSdk = 23`) と iOS 15.5 (上の「対応プラットフォーム」)。CI では、Android の OpenGL 版と Vulkan 版の描画テストを、iOS の描画テストと C++ の単体テストを、それぞれ android-ci と ios-ci の完了後に AWS Device Farm の実機で回す ([android-device-test.yml](https://github.com/maplibre/maplibre-native/blob/main/.github/workflows/android-device-test.yml)、[ios-device-test.yml](https://github.com/maplibre/maplibre-native/blob/main/.github/workflows/ios-device-test.yml))。実機のプールに入っている機種と OS の版は ARN でしか書かれておらず未確認。iOS の単体テストは macOS の CI のシミュレーターで回す ([ios-ci.yml](https://github.com/maplibre/maplibre-native/blob/main/.github/workflows/ios-ci.yml))。GPU とドライバの違いには個別の回避策を入れており、Adreno 600 系の Vulkan で `VK_ERROR_DEVICE_LOST` を避ける回避策 (android-v13.5.0、13.7.1 で全テクスチャに拡大) や、Adreno 3xx の OpenGL ES でラスターレイヤーが見えない不具合の修正 (android-v13.7.1) がある ([android-v13.7.1](https://github.com/maplibre/maplibre-native/releases/tag/android-v13.7.1)、[android-v13.5.0](https://github.com/maplibre/maplibre-native/releases/tag/android-v13.5.0))。メモリの上限への対応の文書は未確認。
- 操作の網羅: Android の `UiSettings` は、移動 (横方向だけの移動も別に切り替え可)、ズーム、回転、傾き、ダブルタップ、片手でのクイックズーム、フリングの慣性、回転と拡大縮小の慣性を個別に有効、無効にできる ([UiSettings.java](https://github.com/maplibre/maplibre-native/blob/main/platform/android/MapLibreAndroid/src/main/java/org/maplibre/android/maps/UiSettings.java))。iOS の `MLNMapView` は `zoomEnabled`、`scrollEnabled`、`rotateEnabled`、`pitchEnabled`、減速の割合 `decelerationRate`、触覚フィードバック、回転とズームを画面中心に固定する設定を持つ ([MLNMapView.h](https://github.com/maplibre/maplibre-native/blob/main/platform/ios/src/MLNMapView.h))。キーボード、マウス、ペンの扱いは未確認。
- エッジケースへの対応: 日付変更線は、`pixelForLatLng()` が経度 180 超で不正な値を返す不具合 (#2960) が解決済みで、世界のコピーと日付変更線が絡むと座標が曖昧になる問題 (#1681) と `getVisibleRegion(true)` が不正な座標を返す問題 (#2951) が未解決である ([#2960](https://github.com/maplibre/maplibre-native/issues/2960)、[#1681](https://github.com/maplibre/maplibre-native/issues/1681)、[#2951](https://github.com/maplibre/maplibre-native/issues/2951))。オフラインは Android の `OfflineManager` で領域をダウンロードできる ([offline パッケージ](https://github.com/maplibre/maplibre-native/tree/main/platform/android/MapLibreAndroid/src/main/java/org/maplibre/android/offline))。スタイルの通信失敗の再試行とオフラインには C++ のテスト (`Map.StyleNetworkErrorRetry`、`Map.Offline`) があり、macOS の WebGPU のジョブではこの 2 つを除外している ([macos-ci.yml](https://github.com/maplibre/maplibre-native/blob/main/.github/workflows/macos-ci.yml))。MapView を外したあとに描画器への参照が残る不具合 (#4549) が解決済みで、アプリのバックグラウンド移行やコンテキストの喪失の扱いを説明した文書は未確認 ([#4549](https://github.com/maplibre/maplibre-native/issues/4549))。
- 継続的な保守: プラットフォームと描画 API ごとのラベル (`android`、`iOS`、`Vulkan`、`metal`、`OpenGL`、`WebGPU`、`simulator`、`windows`、`linux`、`macOS`) で Issue を分けている ([labels](https://github.com/maplibre/maplibre-native/labels))。Issue の数は `android` が 385 件 (未解決 151)、`iOS` が 204 件 (同 55)、`metal` が 58 件 (同 14)、`Vulkan` が 31 件 (同 4) である (`repo:maplibre/maplibre-native is:issue label:<名前>`、2026-11-12 検索)。新しい OS への追随として、ios-v7.0.0 で最低 iOS を 15.5 に引き上げ、CI は macos-26 の上で回している ([ios-v7.0.0](https://github.com/maplibre/maplibre-native/releases/tag/ios-v7.0.0)、[ios-ci.yml](https://github.com/maplibre/maplibre-native/blob/main/.github/workflows/ios-ci.yml))。Android の既定を Vulkan にしたこと (上の「描画方式」) が描画 API の移行にあたる。

## 向いている場面

- 地図の提供元を自分で選びたい、自前のタイルや PMTiles を配信したい場合。
- SDK の利用料や MAU 課金を避けたい場合。
- Web 版 (MapLibre GL JS) と同じスタイルを Android / iOS でも使いたい場合。
- Android で Vulkan、iOS で Metal を使う描画が必要な場合。

## 向いていない場面

- 地図データ・検索・経路などをひとつの事業者からまとめて調達したい場合 (SDK は描画だけで、データは別途用意が要る)。
- 地球儀表示を安定版で使いたい場合 (2026-11-10 時点でプレリリースのみ)。
- Compose / SwiftUI の API 安定性を重視する場合 (ラッパーはいずれも 1.0 前)。

## 出典

- https://github.com/maplibre/maplibre-native
- https://github.com/maplibre/maplibre-native/releases
- https://github.com/maplibre/maplibre-native/blob/main/LICENSE.md
- https://github.com/maplibre/maplibre-native/releases/tag/ios-v7.0.0
- https://github.com/maplibre/maplibre-native/releases/tag/android-v13.7.1
- https://github.com/maplibre/maplibre-native/releases/tag/android-v2026.11.2-globe
- https://github.com/maplibre/maplibre-native/blob/main/platform/android/MapLibreAndroid/build.gradle.kts
- https://github.com/maplibre/maplibre-native/blob/main/platform/android/MapLibreAndroid/src/main/java/org/maplibre/android/offline/OfflineManager.kt
- https://maplibre.org/maplibre-native/android/examples/getting-started/
- https://maplibre.org/maplibre-native/android/examples/artifacts/
- https://maplibre.org/maplibre-native/ios/latest/documentation/maplibre/
- https://maplibre.org/maplibre-native/docs/book/
- https://maplibre.org/maplibre-native/docs/book/platforms/index.html
- https://github.com/maplibre/maplibre-compose
- https://github.com/maplibre/swiftui-dsl
- https://github.com/maplibre/flutter-maplibre-gl
- https://github.com/maplibre/maplibre-react-native

## 未確認のこと

- 地形 (raster-dem による 3D 地形) の表示に対応するか。公式ドキュメントで明記した箇所を見つけられなかった。
- iOS の `OfflineManager` 相当 (MLNOfflineStorage) の詳細。Android 側のソースのみ確かめた。
- 地球儀機能が安定版に入る時期。プレリリースのリリースノートに予定の記載がない。
