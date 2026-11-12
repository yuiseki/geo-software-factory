# react-native-maps

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 1.29.11 (2026-09-28 JST)。npm の `latest` タグも 1.29.11。別に `beta` タグで 2.0.0-beta.15 がある (https://github.com/react-native-maps/react-native-maps/releases/tag/v1.29.11 、 https://www.npmjs.com/package/react-native-maps) |
| リポジトリ | https://github.com/react-native-maps/react-native-maps |
| ドキュメント | 独立したサイトは無く、リポジトリの README と `docs/` 配下 (https://github.com/react-native-maps/react-native-maps/tree/master/docs) |
| ライセンス (LICENSE ファイルで確かめる) | MIT (Copyright (c) 2015 Airbnb) (https://github.com/react-native-maps/react-native-maps/blob/master/LICENSE) |
| 運営主体・ガバナンス | GitHub の `react-native-maps` Organization。README は「少人数のグループが保守している」と書く。もとは Airbnb が公開したもの (LICENSE の著作権表示) |

## 概要

React Native 用の地図コンポーネント。`<MapView />` の子要素として `<Marker />`、`<Polyline />`、`<Polygon />`、`<Circle />`、`<Heatmap />`、`<Geojson />`、タイルのオーバーレイなどを宣言的に置く (https://github.com/react-native-maps/react-native-maps#component-api)。地図そのものは描画せず、Android では Google Maps SDK for Android、iOS では Apple MapKit か Google Maps SDK for iOS をラップする (https://github.com/react-native-maps/react-native-maps/blob/master/docs/installation.md)。

## 対応プラットフォーム

| プラットフォーム | 対応 | 最低 OS 版・備考 |
|---|---|---|
| Android | 対応 | Google Maps SDK for Android を使う。`minSdkVersion` の既定値は 21 (アプリ側で上書きする前提)。端末に Google Play 開発者サービスが必要 (https://github.com/react-native-maps/react-native-maps/blob/master/android/build.gradle 、 https://github.com/react-native-maps/react-native-maps/blob/master/docs/installation.md) |
| iOS | 対応 | podspec の最低版は iOS 15.1。Apple MapKit (既定) か Google Maps SDK for iOS を選ぶ (https://github.com/react-native-maps/react-native-maps/blob/master/react-native-maps.podspec) |
| Web | 非対応 | `src/MapView.web.ts` は react-native-web の `UnimplementedView` を返すだけで、地図は出ない。`react-native-web` は任意の peerDependency (https://github.com/react-native-maps/react-native-maps/blob/master/src/MapView.web.ts) |
| デスクトップ (macOS / Windows / Linux) | 非対応 | 対象外。対応表は iOS と Android のみ (README の見出し「React Native Map components for iOS + Android」) |

- フレームワークの版の要件 (React Native の New Architecture、Flutter の版など): 1.21.0 (2025-04) で Fabric (New Architecture) に移行し、Old Architecture は非対応になった。1.26.1 以降は React Native 0.81.1 以上、1.26.0 以下は 0.76 以上が要る。peerDependencies は `react >= 18.3.1`、`react-native >= 0.76.0`。Expo の config plugin は react-native-maps 1.22 以上と Expo SDK 53 以上で使える (https://github.com/react-native-maps/react-native-maps/releases/tag/v1.21.0 、 https://github.com/react-native-maps/react-native-maps#compatibility 、 https://github.com/react-native-maps/react-native-maps/blob/master/docs/installation.md)

## 描画方式

- 自前で描画するか、OS や他の SDK のラッパーか: ラッパー。Android は Google Maps SDK for Android (`com.google.android.gms:play-services-maps`、既定 19.1.0) と android-maps-utils。iOS は既定で Apple MapKit、`provider={PROVIDER_GOOGLE}` を指定し `react-native-maps/Google` サブスペックを入れると Google Maps SDK for iOS (既定 GoogleMaps 9.4.0、Google-Maps-iOS-Utils 6.1.0) を使う。Google 版の iOS で Fabric 対応した Marker と Polygon は 1.29.0 (2026-06) で入った (https://github.com/react-native-maps/react-native-maps/blob/master/android/build.gradle 、 https://github.com/react-native-maps/react-native-maps/blob/master/react-native-maps.podspec 、 https://github.com/react-native-maps/react-native-maps/releases/tag/v1.29.0)
- ラスタ / ベクトルタイル、2D / 3D: ベース地図の形式と 3D 表現は下にある SDK に依存する。このライブラリが追加できるのは XYZ ラスタタイルのオーバーレイ (`UrlTile`、`LocalTile`) とベクタ図形・GeoJSON で、任意のベクトルタイルやスタイル JSON を読む機能は無い (https://github.com/react-native-maps/react-native-maps#using-a-custom-tile-overlay)

## 対応するタイル・データ

- 表示できるタイル・地図データ: Google または Apple のベース地図、`UrlTile` による XYZ ラスタタイル (`flipY` で TMS も可)、`LocalTile` による端末内 XYZ タイル、GeoJSON (`<Geojson />`)、ヒートマップ。Google 版では Cloud 上で作った Map ID によるスタイル指定 (`googleMapId`) が使える (https://github.com/react-native-maps/react-native-maps#using-a-custom-tile-overlay 、 https://github.com/react-native-maps/react-native-maps#customizing-the-map-style-google-maps-only)
- 組み合わせの制約 (下にある SDK の規約・課金を引き継ぐか): 引き継ぐ。Android は必ず Google Maps Platform を使うので、API キー、課金アカウントの作成、Google Maps Platform Terms of Service が前提になる (installation.md の WARNING)。規約 3.2.3(b) は Google Maps Content のキャッシュを原則禁止し、3.2.3(e) は Google Maps Core Services を Google 以外の地図と同じ画面や近くで使うことを禁じる。`UrlTile` で他社タイルを重ねる、`mapType="none"` で Google の地図を消して自前タイルだけ出す、といった構成がこの条項に当たるかは条文と個別に照らす必要がある (推測。公式の判断は見つけていない)。iOS で Apple MapKit を選ぶと Google の規約は関わらず、Apple Developer Program の規約に従う (https://cloud.google.com/maps-platform/terms 、 https://github.com/react-native-maps/react-native-maps/blob/master/docs/installation.md)
- オフライン地図: Google や Apple のベース地図をオフライン保存する機能は無い。`LocalTile` で端末内のラスタタイルを表示できるが、Android では下の Google タイルも読み込み続けるので、止めたいときは `mapType="none"` にするよう README が書いている (https://github.com/react-native-maps/react-native-maps#tile-overlay-using-local-tiles)

## ライセンスと費用

- ライセンス: MIT。
- 下にある SDK の費用: Google Maps Platform の料金表で、Android と iOS の「Maps SDK」SKU は Essentials 区分で無料利用枠が無制限 (従量課金の単価なし)。ただし課金アカウントの登録は要る。Places など他の API を併用すればそちらは従量課金になる。Apple MapKit (ネイティブ) の料金は Apple の公開ページに記載が無く未確認 (https://developers.google.com/maps/billing-and-pricing/pricing 、 https://developer.apple.com/maps/)
- ライセンス上の注意: ライブラリ本体はなし (MIT の著作権表示を残す)。ただし地図データと SDK は Google / Apple の規約下にあり、キャッシュ、他社地図との併用、車載機器での利用 (Google 規約 3.2.3(f)) などの制限を引き継ぐ。iOS で Google 版を使う場合、位置情報を使わなくても `NSLocationWhenInUseUsageDescription` を Info.plist に書かないと App Store 審査で落ちると installation.md が注意している (https://cloud.google.com/maps-platform/terms 、 https://github.com/react-native-maps/react-native-maps/blob/master/docs/installation.md)

## エコシステム

- 主なプラグイン・拡張: 公式の Expo config plugin (`app.json` の `plugins` に追加)。Google 版ではヒートマップやクラスタ用に Google の utils ライブラリを内部で使う。サードパーティのクラスタリング等の拡張は未確認 (https://github.com/react-native-maps/react-native-maps/blob/master/docs/installation.md)
- 似た位置づけの他のライブラリとの違い: @maplibre/maplibre-react-native や @rnmapbox/maps は MapLibre Native / Mapbox Maps SDK を使い、ベクトルタイルとスタイル JSON を扱える。react-native-maps は OS 標準と Google の地図に寄せた API で、ベクトルタイルの自前スタイルは扱えない代わりに Google / Apple の地図とそのまま揃う (https://github.com/maplibre/maplibre-react-native 、 https://github.com/rnmapbox/maps)

## 開発の活発さ

- 直近 1 年のリリース数: 20 (2025-11-10 から 2026-11-10 の GitHub Releases、すべて安定版。1.26.19 から 1.29.11)
- 最終コミット日: 2026-09-28 JST (master、`chore(release): 1.29.11`)
- 主なメンテナー (個人か組織か): Organization 管理で、直近 1 年の人間のコミットは salah-ghanim が最多。累計では monholm、lelandrichardson、salah-ghanim が多い (https://github.com/react-native-maps/react-native-maps/graphs/contributors)

## 環境の違いと保守

- ブラウザ間の互換: Web は非対応なので対象外 (上の「対応プラットフォーム」)。描画は下にある Google Maps SDK と Apple MapKit が行い、描画 API の違いはそれらが引き受ける (上の「描画方式」)。
- OS 間の互換: 文書でうたう最低版は Android の `minSdkVersion` 21 (既定値) と iOS 15.1 である (上の「対応プラットフォーム」)。CI では、Android は ubuntu-latest で example アプリと計装テストの APK をビルドし (`assembleDebug assembleAndroidTest`)、iOS は macos-latest で example アプリを iOS シミュレーター向けにビルドする ([androidBuild.yml](https://github.com/react-native-maps/react-native-maps/blob/master/.github/workflows/androidBuild.yml)、[iosBuild.yml](https://github.com/react-native-maps/react-native-maps/blob/master/.github/workflows/iosBuild.yml))。エミュレーター、シミュレーター、実機の上でテストを走らせる手順は見当たらない (同)。PR では lint、型検査、Jest のテストを回す ([pullRequest.yml](https://github.com/react-native-maps/react-native-maps/blob/master/.github/workflows/pullRequest.yml))。一部の Android 端末で `doDestroy` が落ちる不具合の修正 (v1.26.18、2025-10-22) のような端末固有の修正がある ([Releases](https://github.com/react-native-maps/react-native-maps/releases))。GPU とメモリの上限は下の SDK の担当である (推測)。
- 操作の網羅: `MapView` の props で、ピンチでのズーム (`zoomEnabled`)、ダブルタップでのズーム (`zoomTapEnabled`)、回転 (`rotateEnabled`)、移動 (`scrollEnabled`)、傾き (`pitchEnabled`)、回転とズームの間に中心を固定する設定 (`scrollDuringRotateOrZoomEnabled`、Google Maps のみ) を切り替えられる ([mapview.md](https://github.com/react-native-maps/react-native-maps/blob/master/docs/mapview.md))。慣性やキーボードの扱いは下の SDK の挙動に従う (推測)。スクロールする親ビューとの両立の設定は未確認。
- エッジケースへの対応: `onMapReady` より前に `mapPadding` を設定したときに GoogleMap に触れて落ちる不具合の修正 (v1.29.6) や、null のオーバーレイを外すときの防御 (v1.29.1) のように、初期化と後始末の競合を直す修正が続いている ([Releases](https://github.com/react-native-maps/react-native-maps/releases))。地図をキャッシュした画像として表示する `cacheEnabled` と、読み込み中の表示 `loadingEnabled` がある ([mapview.md](https://github.com/react-native-maps/react-native-maps/blob/master/docs/mapview.md))。日付変更線は Issue の検索で「antimeridian」が 0 件で、扱いは未確認 (`repo:react-native-maps/react-native-maps is:issue antimeridian`、2026-11-12 検索)。オフライン、タイル読み込みの再試行は未確認。
- 継続的な保守: React Native の New Architecture (Fabric) に 1.21.0 で移り、Old Architecture をやめた (上の「対応プラットフォーム」)。その後も Fabric の上での iOS の Google Maps のマーカーとポリゴンの対応 (v1.29.0、2026-06-28) や、Fabric のレイアウトからマーカーの大きさを決める修正 (v1.29.9、2026-09-27) が続く ([Releases](https://github.com/react-native-maps/react-native-maps/releases))。リリースノートは semantic-release で `android:`、`ios:` の接頭辞を付けて書かれ、プラットフォームごとの修正を追える (同)。Issue のラベルにはプラットフォーム別のものが無い ([labels](https://github.com/react-native-maps/react-native-maps/labels))。

## 向いている場面

- iOS と Android のアプリで、Google マップや Apple マップの見た目と操作をそのまま使いたいとき。
- マーカー、図形、GeoJSON を重ねる程度で、ベース地図のスタイルを自前で作り込まないとき。
- iOS では Apple MapKit を選べば API キーなしで始められる (installation.md)。

## 向いていない場面

- 自前のベクトルタイル、スタイル JSON、PMTiles を使いたいとき (機能が無い)。
- Google Play 開発者サービスの無い Android 端末を対象に含むとき。
- Web やデスクトップでも同じコードで地図を出したいとき (Web は未実装)。
- Google の規約上、地図のオフライン保存や他社地図との併用が要る用途。

## 出典

- https://github.com/react-native-maps/react-native-maps
- https://github.com/react-native-maps/react-native-maps/blob/master/LICENSE
- https://github.com/react-native-maps/react-native-maps/tree/master/docs
- https://github.com/react-native-maps/react-native-maps/blob/master/docs/installation.md
- https://github.com/react-native-maps/react-native-maps#compatibility
- https://github.com/react-native-maps/react-native-maps#component-api
- https://github.com/react-native-maps/react-native-maps#using-a-custom-tile-overlay
- https://github.com/react-native-maps/react-native-maps#tile-overlay-using-local-tiles
- https://github.com/react-native-maps/react-native-maps#customizing-the-map-style-google-maps-only
- https://github.com/react-native-maps/react-native-maps/blob/master/android/build.gradle
- https://github.com/react-native-maps/react-native-maps/blob/master/react-native-maps.podspec
- https://github.com/react-native-maps/react-native-maps/blob/master/src/MapView.web.ts
- https://github.com/react-native-maps/react-native-maps/releases/tag/v1.21.0
- https://github.com/react-native-maps/react-native-maps/releases/tag/v1.29.0
- https://github.com/react-native-maps/react-native-maps/releases/tag/v1.29.11
- https://github.com/react-native-maps/react-native-maps/graphs/contributors
- https://www.npmjs.com/package/react-native-maps
- https://developers.google.com/maps/billing-and-pricing/pricing
- https://cloud.google.com/maps-platform/terms
- https://developer.apple.com/maps/
- https://github.com/maplibre/maplibre-react-native
- https://github.com/rnmapbox/maps

## 未確認のこと

- Apple MapKit (ネイティブ) の利用料と上限: Apple の Maps 開発者ページに料金や上限の記載が無く、確かめられなかった。
- 2.0.0 系 (npm の `beta` タグ) の内容と正式版の時期: リリースノートを追っていない。
- `UrlTile` や `mapType="none"` を使った構成が Google 規約 3.2.3(e) に抵触するか: 条文は確認したが、この構成に対する Google の公式な判断は見つからなかった。
- サードパーティの拡張 (クラスタリング等) の現状: 調べていない。
