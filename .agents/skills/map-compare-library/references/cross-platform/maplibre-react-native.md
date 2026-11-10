# MapLibre React Native

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 11.5.1 (2026-10-30 JST)。npm パッケージ名は `@maplibre/maplibre-react-native` (https://github.com/maplibre/maplibre-react-native/releases/tag/v11.5.1 、 https://www.npmjs.com/package/@maplibre/maplibre-react-native) |
| リポジトリ | https://github.com/maplibre/maplibre-react-native |
| ドキュメント | https://maplibre.org/maplibre-react-native/ |
| ライセンス (LICENSE ファイルで確かめる) | MIT (Copyright (c) 2022 MapLibre contributors、Copyright (c) 2015-2020 Mapbox) (https://github.com/maplibre/maplibre-react-native/blob/main/LICENSE.md) |
| 運営主体・ガバナンス | MapLibre Organization の GitHub 上のプロジェクト。描画エンジンの MapLibre Native も同じ Organization が保守する (https://github.com/maplibre) |

## 概要

React Native から MapLibre Native (Android / iOS) を使うためのラッパー (README)。スタイル JSON とベクトルタイルを扱え、地図の提供元を固定しない。もとは @rnmapbox/maps のフォークで、Mapbox SDK と MapLibre の分岐が進んだため描画エンジンごとにラッパーを分けた、と README が説明している (https://github.com/maplibre/maplibre-react-native#readme)。v11 から New Architecture 専用になり、API を MapLibre GL JS に寄せた (https://maplibre.org/maplibre-react-native/docs/setup/migrations/v11)。

## 対応プラットフォーム

| プラットフォーム | 対応 | 最低 OS 版・備考 |
|---|---|---|
| Android | 対応 | ドキュメントは「Android API Level ≥ 23」と書くが、ライブラリの `gradle.properties` の `minSdkVersion` は 24。同梱する MapLibre Native Android は 13.6.1。`nativeVariant` で `opengl` (既定) か `vulkan` を選べる (https://maplibre.org/maplibre-react-native/docs/setup/getting-started 、 https://github.com/maplibre/maplibre-react-native/blob/main/package/android/gradle.properties 、 https://maplibre.org/maplibre-react-native/docs/setup/library-customizations) |
| iOS | 対応 | MapLibre Native iOS 6.31.0 を Swift Package Manager で取り込む。最低版は React Native の `min_ios_version_supported` に従う (https://github.com/maplibre/maplibre-react-native/blob/main/package/MapLibreReactNative.podspec) |
| Web | 非対応 | リポジトリに `.web.*` 実装が無く、ドキュメントの対象も Android と iOS のみ。Web では MapLibre GL JS を別に使う |
| デスクトップ (macOS / Windows / Linux) | 非対応 | 対象外。MapLibre Native 自体はデスクトップでも動くが、このラッパーは Android と iOS のみ |

- フレームワークの版の要件: v11 以降は New Architecture のみ。React Native 0.80.0 以上 (それ未満も動くかもしれないとドキュメントは書く)、peerDependencies は `react >= 19.1.0`、`react-native >= 0.80.0`、Expo を使う場合は `expo >= 54.0.0`。Expo では config plugin で組み込み、Expo Go では使えない (https://maplibre.org/maplibre-react-native/docs/setup/getting-started 、 https://github.com/maplibre/maplibre-react-native/blob/main/package/package.json 、 https://maplibre.org/maplibre-react-native/docs/setup/expo)

## 描画方式

- 自前で描画するか、OS や他の SDK のラッパーか: MapLibre Native (C++ の描画エンジン、Android と iOS の SDK) のラッパー。Android は既定で `GLSurfaceView` を使い、`androidView="texture"` で `TextureView` に戻せる (https://maplibre.org/maplibre-react-native/docs/setup/migrations/v11)
- ラスタ / ベクトルタイル、2D / 3D: ベクトルタイルとラスタタイルの両方。MapLibre Style Spec のスタイル JSON で描く。カメラの傾き (pitch) は MapLibre Native の機能として使える。地形 3D などの対応範囲は MapLibre Native の版に依存する (未確認)

## 対応するタイル・データ

- 表示できるタイル・地図データ: MapLibre Style Spec に沿ったスタイル JSON、ベクトルタイル (MVT)、ラスタタイル、GeoJSON。PMTiles はリポジトリにサンプル (`examples/shared/src/examples/protocols/PMTilesVectorSource.tsx` など) があり、MapLibre Native 側に PMTiles の読み込みがある。ドキュメントは開発用に MapLibre Demo Tiles を使い、本番では自前のスタイルとタイルか Stadia Maps、MapTiler などの提供元を使うよう書く (https://maplibre.org/maplibre-react-native/docs/setup/getting-started 、 https://github.com/maplibre/maplibre-react-native/tree/main/examples/shared/src/examples/protocols 、 https://github.com/maplibre/maplibre-native/blob/main/platform/android/CHANGELOG.md)
- 組み合わせの制約 (下にある SDK の規約・課金を引き継ぐか): ライブラリと MapLibre Native に利用料や API キーは無い。タイルの提供元を選んだ場合は、その提供元の料金と規約 (帰属表示、キャッシュの扱いなど) に従う。v10 で `setAccessToken` を廃止し、提供元のトークンはスタイルやタイルの URL に含める形にした (https://maplibre.org/maplibre-react-native/docs/setup/migrations/v10)
- オフライン地図: `OfflineManager` で地域を指定したオフラインパックを作り、端末のデータベースに保存できる (https://maplibre.org/maplibre-react-native/docs/modules/offline-manager)。提供元のタイルを保存してよいかは提供元の規約による

## ライセンスと費用

- ライセンス: MIT。下の MapLibre Native は BSD-2-Clause (https://github.com/maplibre/maplibre-native/blob/main/LICENSE.md)
- 下にある SDK の費用: MapLibre Native は無料。費用はタイルの配信 (自前配信のインフラ費、または提供元の料金) で決まる
- ライセンス上の注意: なし。依存の @maplibre/maplibre-gl-style-spec は BSD 系、Turf は MIT、MapLibre Native が同梱する第三者コードは ISC、Boost Software License、MIT などの許容型で、コピーレフトは見当たらない。配布時は MIT / BSD-2-Clause と第三者ライセンスの著作権表示をアプリ内やドキュメントに含める必要がある。タイルに OpenStreetMap 由来のデータを使う場合は ODbL の帰属表示が要る (https://github.com/maplibre/maplibre-native/blob/main/LICENSES.core.md 、 https://github.com/maplibre/maplibre-style-spec/blob/main/LICENSE.txt)

## エコシステム

- 主なプラグイン・拡張: Expo config plugin、Android の位置情報エンジンを `default` か `google` (Google Play 開発者サービスの位置情報) から選ぶ設定、MapLibre Native の版や variant を差し替える設定 (https://maplibre.org/maplibre-react-native/docs/setup/library-customizations)。MapLibre Style Spec に沿うので、MapLibre GL JS 向けのスタイルをそのまま使える
- 似た位置づけの他のライブラリとの違い: @rnmapbox/maps は分岐元で、旧版 (v10.0 系の CHANGELOG) では MapLibre 実装を選べたが、現在の README は Mapbox Maps SDK v11 向けと書いており、Mapbox のアクセストークンと料金が前提になる。react-native-maps は Google / Apple の地図のラッパーで、自前のベクトルタイルとスタイルを扱えない (https://github.com/rnmapbox/maps 、 https://github.com/rnmapbox/maps/blob/main/CHANGELOG.md 、 https://github.com/react-native-maps/react-native-maps)

分岐の経緯: npm の `@maplibre/maplibre-react-native` の最初の版は 8.6.0-beta.0 (2022-12-30 JST)。9.0.0 (2023-01-13) の CHANGELOG に「RNMapbox からのフォークを完了し、プロプライエタリな Mapbox SDK の対応を外し、最新の MapLibre GL Native SDK に更新した」とある。v10.0.0 は 2025-01-15 JST、New Architecture 専用の v11.0.0 は 2026-04-18 JST に出た (https://github.com/maplibre/maplibre-react-native/blob/main/CHANGELOG.md 、 https://www.npmjs.com/package/@maplibre/maplibre-react-native)

## 開発の活発さ

- 直近 1 年のリリース数: 安定版 26 (v10.4.1、v10.4.2 と v11.0.0 から v11.5.1)、プレリリース 68 (v11 の alpha と beta) (2025-11-10 から 2026-11-10 の GitHub Releases)
- 最終コミット日: 2026-10-30 JST (main、`chore(release): 11.5.1`)
- 主なメンテナー (個人か組織か): MapLibre Organization のプロジェクト。直近 1 年の人間のコミットは KiwiKilian が大半を占め、次いで tyrauber。累計では mfazekas (分岐元の rnmapbox 時代を含む)、KiwiKilian、ferdicus が多い (https://github.com/maplibre/maplibre-react-native/graphs/contributors)

## 向いている場面

- React Native アプリで、自前のベクトルタイルやスタイル JSON、PMTiles を使いたいとき。
- 地図の提供元を固定したくない、API キーや従量課金の無い描画層が欲しいとき。
- Web 版を MapLibre GL JS で作っていて、同じスタイルをモバイルでも使いたいとき。
- オフラインパックで地域単位の地図を端末に保存したいとき。

## 向いていない場面

- Old Architecture のままのアプリ (v11 は非対応。v10 系に留まる必要がある)。
- Expo Go だけで開発を済ませたいとき (使えない)。
- Google / Apple の地図の見た目や POI をそのまま使いたいとき。
- Web やデスクトップも同じコンポーネントで出したいとき。

## 出典

- https://github.com/maplibre/maplibre-react-native
- https://github.com/maplibre/maplibre-react-native#readme
- https://github.com/maplibre/maplibre-react-native/blob/main/LICENSE.md
- https://github.com/maplibre/maplibre-react-native/blob/main/CHANGELOG.md
- https://github.com/maplibre/maplibre-react-native/releases/tag/v11.5.1
- https://github.com/maplibre/maplibre-react-native/blob/main/package/package.json
- https://github.com/maplibre/maplibre-react-native/blob/main/package/android/gradle.properties
- https://github.com/maplibre/maplibre-react-native/blob/main/package/MapLibreReactNative.podspec
- https://github.com/maplibre/maplibre-react-native/tree/main/examples/shared/src/examples/protocols
- https://github.com/maplibre/maplibre-react-native/graphs/contributors
- https://maplibre.org/maplibre-react-native/
- https://maplibre.org/maplibre-react-native/docs/setup/getting-started
- https://maplibre.org/maplibre-react-native/docs/setup/expo
- https://maplibre.org/maplibre-react-native/docs/setup/library-customizations
- https://maplibre.org/maplibre-react-native/docs/setup/migrations/v10
- https://maplibre.org/maplibre-react-native/docs/setup/migrations/v11
- https://maplibre.org/maplibre-react-native/docs/modules/offline-manager
- https://www.npmjs.com/package/@maplibre/maplibre-react-native
- https://github.com/maplibre
- https://github.com/maplibre/maplibre-native/blob/main/LICENSE.md
- https://github.com/maplibre/maplibre-native/blob/main/LICENSES.core.md
- https://github.com/maplibre/maplibre-native/blob/main/platform/android/CHANGELOG.md
- https://github.com/maplibre/maplibre-style-spec/blob/main/LICENSE.txt
- https://github.com/rnmapbox/maps
- https://github.com/rnmapbox/maps/blob/main/CHANGELOG.md
- https://github.com/react-native-maps/react-native-maps

## 未確認のこと

- iOS の最低版の具体的な数字: podspec は React Native の `min_ios_version_supported` を参照しており、React Native の版ごとの値を確かめていない。
- Android の最低 API レベルが 23 か 24 か: ドキュメントは 23、ライブラリの既定設定は 24 で食い違っている。どちらが実際のビルド要件かは試していない。
- 地形 3D、globe 投影など MapLibre Native の新しい機能がこのラッパーから使えるか: API リファレンスを確かめていない。
- ドキュメントサイトの各ページの内容はリポジトリの `docs/content/` のソースで読んだ。サイト上の URL は HTTP 200 が返ることだけを確かめた。
