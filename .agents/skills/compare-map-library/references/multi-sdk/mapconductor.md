# MapConductor

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| GitHub org | https://github.com/MapConductor |
| ドキュメント | https://mapconductor.com/ (Android と共通の入口。iOS 版は https://docs-ios.mapconductor.com/) |
| 最新の安定版 (プラットフォームごと) | Android: Maven Central の `com.mapconductor:*` 1.3.1 (2026-08-16 公開)。iOS: Swift Package のタグで ios-sdk-core 1.3.2 (2026-10-23)、各プロバイダーは 1.3.1。React: npm の `@mapconductor/*` 0.3.0 から 0.3.1 (2026-10-29 から 10-30 公開)。どのリポジトリも GitHub Releases はほぼ使っておらず (org 全体で vectortile v0.1.0 の 1 件のみ)、版はタグとパッケージレジストリで確かめた |
| 運営主体 | 法人ではなく個人主導の OSS プロジェクト。公式サイトの Team ページは KATSUMATA Masashi を Lead Developer & Founder とし、ほか 4 名を挙げる。運営する会社名はサイトに書かれていない (https://mapconductor.com/team/)。android-sdk-core の LICENSE には「Copyright 2026 Masashi Katsumata」とある |

## 概要

MapConductor は、複数の地図 SDK を 1 つの共通 API で操作するための抽象化層である (https://github.com/MapConductor)。地図を描くのは下にある Google Maps、Mapbox、MapLibre、HERE、ArcGIS などの各 SDK で、MapConductor はその上に載り、マーカーや図形、カメラを SDK に依存しない形で書けるようにする。Android は Jetpack Compose、iOS は SwiftUI、Web は React の宣言的 API を提供し、地図 SDK ごとの差は「for-xxx」モジュールが吸収する (https://github.com/MapConductor/android-sdk)。

## 対応プラットフォーム

- Android (UI フレームワーク): Jetpack Compose。Maven Central で配布 (https://github.com/MapConductor/android-sdk)。
- iOS (UI フレームワーク): SwiftUI。Swift Package Manager で配布し、XCFramework を作るスクリプトもある (https://github.com/MapConductor/ios-sdk)。
- Web (React): React 18/19 と TypeScript。npm で配布。React Native 向けの入口 `@mapconductor/js-sdk-react/native` も同じパッケージにあり、旧 `reactnative-for-*` パッケージは統合済みとされている (https://github.com/MapConductor/react-sdk)。公式サイトのアーキテクチャ説明は React Native で使える地図 SDK を 4 種としている (https://mapconductor.com/architecture/)。

## 対応する地図 SDK とモジュールの成熟度

2026-11-10 に org の全 88 リポジトリを `gh repo list` で列挙し、各リポジトリのタグ、Maven Central、npm を確かめた。どのプロバイダーのリポジトリも最終コミットは 2026-11-09 前後で、ほぼ同時刻に同じ名前のブランチ (feat/polygon-tiling) がマージされている。各リポジトリのコミットの大半は 1 人による。

| 地図 SDK | Android | iOS | React | 備考 |
|---|---|---|---|---|
| Google Maps | android-for-googlemaps。Maven `for-googlemaps` 1.3.1 | ios-for-googlemaps。タグ 1.3.1 (計 10 タグ) | react-for-googlemaps。npm 0.3.1 | Android と iOS の README の対応表に載る |
| Mapbox | android-for-mapbox。Maven 1.3.1 | ios-for-mapbox。タグ 1.3.1 | react-for-mapbox。npm 0.3.1 | Android と iOS の README の対応表に載る |
| MapLibre | android-for-maplibre。Maven 1.3.1 | ios-for-maplibre。タグ 1.3.1 | react-for-maplibre。npm 0.3.1 | Android と iOS の README の対応表に載る。React 版は ESM のみで使う (README 記載) |
| HERE | android-for-here。Maven 1.3.1 | ios-for-here。タグ 1.3.1 | react-for-here。npm 0.3.0 | Android と iOS の README の対応表に載る |
| ArcGIS | android-for-arcgis。Maven 1.3.1 | ios-for-arcgis。タグ 1.3.1 | react-for-arcgis。npm 0.3.1 | Android は 2D と 3D の地図ビューがある |
| Apple MapKit | 対象外 (Apple のみ) | ios-for-mapkit。タグ 1.3.1 | react-for-mapkit。npm 0.3.1 (MapKit JS と推測) | iOS の README の対応表に載る |
| MapTiler | android-for-maptiler。Maven 1.3.1 | ios-for-maptiler。タグ 1.3.1 (計 2 タグ) | react-for-maptiler。npm 0.3.1 | Android と iOS の README の対応表には無い |
| TomTom | android-for-tomtom。Maven 1.3.1 | ios-for-tomtom。タグ 1.3.1 (計 2 タグ) | react-for-tomtom。npm 0.3.1 | README の対応表には無い |
| Longdo Map | android-for-longdo。Maven 1.3.1 | ios-for-longdo。タグ 1.3.1 (1 タグのみ) | react-for-longdo。npm 0.3.1 | README の対応表には無い |
| Mappls | android-for-mappls。Maven 1.3.1 | ios-for-mappls。タグなし | react-for-mappls。npm 0.3.1 | iOS は未リリース |
| Open Mobile Maps | android-for-openmobilemaps。Maven 1.3.1 | ios-for-openmobilemaps。タグなし | なし | iOS は未リリース |
| Leaflet | なし | なし | react-for-leaflet。npm 0.3.1 | Web のみ |
| OpenLayers | なし | なし | react-for-openlayers。npm 0.3.1 | Web のみ |
| Azure Maps | なし | なし | react-for-azuremaps。npm 0.3.1 | Web のみ |
| CesiumJS | なし | なし | react-for-cesium。npm 0.3.1 | Web のみ。LICENSE ファイルの扱いは「ライセンス」節 |
| deck.gl | なし | なし | react-for-deckgl。npm 0.3.1 (初回公開 2026-10-29) | Web のみ。タグなし |

ほかに、プロバイダーに依存しない拡張としてヒートマップ、マーカークラスタリング、GeoJSON、KML、アイコン集 (日本、米国、天気)、ベクトルタイル (vectortile、android-vectortile、ios-vectortile、react-vectortile) のリポジトリがある。WebView 内の JS 地図をネイティブ側から MapConductor API で操作する webview-sdk もある (https://github.com/MapConductor/webview-sdk)。

## 共通 API の範囲

- 共通化されているもの (カメラ、マーカー、ポリライン、ポリゴン、円、情報ウィンドウ、クラスタリングなど): Android の README は地図ビュー、カメラ状態、マーカー (カスタムアイコン)、Compose で書く情報バブル、メートル指定の円、ポリライン、ポリゴン、地上画像 (Ground Image)、ラスタータイルレイヤー、ヒートマップ、マーカークラスタリング、GeoJSON レイヤー、`GeoPoint` などの共通幾何型を挙げる。Google Maps、Mapbox、HERE、ArcGIS、MapLibre の 5 種で、ベクトルタイルレイヤー以外は全て対応済みとしている (https://github.com/MapConductor/android-sdk)。iOS の README も同じ項目を Google Maps、Mapbox、MapKit、ArcGIS、HERE、MapLibre の 6 種で対応済みとしている (https://github.com/MapConductor/ios-sdk)。React の README はマーカー、円、ポリライン、ポリゴン、GroundImage、RasterLayer、大量マーカー用の `<Markers>`、ヒートマップ、クラスタリング、カメラとイベントの API を挙げる (https://github.com/MapConductor/react-sdk)。
- 共通化されていないもの・SDK 固有機能の扱い: 公式サイトは「全ての地図 SDK の全機能を包むことは目指さない」と明言している。SDK 側に無い機能は、そのプロバイダーでは未実装のままにするか、コア側の代替で補う (例: ポリゴンの穴を単純な輪に分割する)。共通 API に無い機能は `getMapViewHolder()` で下の SDK の地図オブジェクトを取り出して使う。各ドライバーが対応する要素は Capable インターフェースで型に表れる (https://mapconductor.com/architecture/)。ベクトルタイルレイヤーは Android と iOS の README で「Planned」または未対応の扱いである。地図のスタイル指定 (`mapDesign`) はプロバイダーごとの値を使う (README のコード例)。

## アーキテクチャ

- 公式サイトは 6 層で説明している。UI フレームワーク、統一地図 API、ブリッジ (React Native のみ)、プラットフォーム差を吸収する層、ネイティブ SDK のドライバー、地図 SDK 本体の順で、プロバイダーを替えると下の 2 層だけが入れ替わる (https://mapconductor.com/architecture/)。
- オーバーレイごとに Controller と Renderer を分ける。Controller (コア側) は追加・更新・削除の振り分けと差分検知を担い、Renderer (各 SDK 側) は作成・更新・削除の 3 操作だけを SDK 固有に実装する (https://mapconductor.com/architecture/)。Android の `docs/architecture.md` は、これを「Bridge パターンによる SDK 抽象化 + Controller–Renderer パターンによるオーバーレイ管理」と要約し、State、Controller、Renderer、Entity、Manager (空間インデックスを含む) の役割を説明している (https://github.com/MapConductor/android-sdk/blob/develop/docs/architecture.md)。
- 状態は観測可能な State オブジェクトで持ち、React 版ではプロパティを直接書き換えると React のツリーを作り直さずに Renderer に反映される (https://github.com/MapConductor/react-sdk)。
- 各プラットフォームの SDK リポジトリ (android-sdk、ios-sdk、react-sdk) は、コアと各プロバイダーのリポジトリを git submodule で束ねる構成である。

## 何が楽になるか

- 同じオーバーレイのコード (マーカー、図形、クラスタリング、ヒートマップ) を、地図 SDK を替えても書き直さずに使える。README のコード例では、地図ビューの生成部分だけを差し替え、中身の `MapContent()` は共通にしている (https://github.com/MapConductor/android-sdk)。
- 地図 SDK の比較検討や、顧客や地域ごとに異なる SDK を使い分ける構成を、1 つのコードベースで作りやすい。
- ヒートマップやクラスタリングのように、SDK ごとに有無や API が違う機能を共通の部品として使える。

## 何が楽にならないか

- 下にある地図 SDK の料金、利用規約、API キーやアクセストークンの管理、タイルとスタイルの制約はそのまま残る。各 SDK の初期設定 (キー、Gradle や Info.plist の設定) もプロバイダーごとに要る (https://github.com/MapConductor/android-sdk)。
- 共通 API に無い機能は SDK 固有のコードを書くことになり、その部分は移植できない。
- 依存が 1 層増える。下の SDK の更新に MapConductor 側の追随が要り、MapConductor の対応を待つことがある。
- React 版は SSR で一部プロバイダーが読み込めない (Node の解決で失敗する) ことが README に表で示されており、クライアント側で遅延読み込みする必要がある (https://github.com/MapConductor/react-sdk)。
- README の対応表に載っているのは Android で 5 種、iOS で 6 種で、MapTiler、TomTom、Longdo、Mappls、Open Mobile Maps などは表に無い。これらの機能の揃い具合は README からは読み取れない。

## 開発の活発さ

- 主要リポジトリの最終コミット日、リリース数、コントリビュータ数: 最終コミットは android-sdk、ios-sdk、react-sdk とも 2026-11-09 (develop ブランチ)。GitHub Releases は使っておらず、版はタグとレジストリで出している。Android は Maven Central の core が 1.0.0 から 1.3.1 まで 12 版、iOS は ios-sdk-core に 12 タグ、npm の `@mapconductor/js-sdk-core` は 2026-07-22 の初回公開から 7 版。コントリビュータ (bot を除く) は org 全体で 5 アカウントで、2025-11-10 以降のコアリポジトリへのコミットは android-sdk-core 181 件中 179 件、ios-sdk-core 120 件中 120 件、js-sdk-core 106 件中 101 件が同じ 1 アカウント (wf9a5m75、表示名 Masashi Katsumata) による。リポジトリ作成は android-sdk が 2025-04、ios-sdk-core が 2026-01、js-sdk-core が 2026-07 で、全体に新しい。android-sdk の Star は 15 (確かめた日)。

## ライセンス

2026-11-10 に GitHub API のライセンス判定と、LICENSE ファイル・パッケージのメタデータで確かめた値。

| リポジトリ | 判定 |
|---|---|
| android-sdk, android-sdk-core, ios-sdk, ios-sdk-core | Apache-2.0 |
| react-sdk | MIT (LICENSE は「MIT License / Copyright (c) 2024 MapConductor」)。ただし npm で配る各パッケージの `package.json` は Apache-2.0 を宣言している |
| 地図 SDK ごとのモジュール (android-for-*, ios-for-*, react-for-*) | Apache-2.0 (react-for-cesium を除く) |
| react-for-cesium | GitHub の判定は NOASSERTION。LICENSE ファイルの中身が「Apache License 2.0」の 1 行だけで本文が無いためで、`package.json` は Apache-2.0 を宣言している |
| js-sdk-core, js-sdk-react | LICENSE ファイルなし。`package.json` は Apache-2.0 |
| android-marker-clustering, android-geojson-layer, android-kml, android-icons など一部の拡張 | LICENSE ファイルなし。Maven Central の POM は Apache License 2.0 を宣言している |

下にある地図 SDK のライセンスと料金は別にかかる。

## 執筆上の注意

他の候補と同じ粒度で書く。公開リポジトリから確かめられることだけを書く。

## 向いている場面

- 地図 SDK をまだ決めきれていない、または将来の乗り換えを見込んでいるモバイルアプリ (Compose や SwiftUI)。
- 顧客や地域ごとに異なる地図 SDK を使い分ける必要があるアプリ。
- 複数の SDK を同じオーバーレイで並べて比較検証したいとき。

## 向いていない場面

- 使う地図 SDK が 1 つに決まっており、乗り換えの予定も無いとき。抽象化層の分だけ依存と学習が増える。
- 下の SDK 固有の機能 (3D 表現、独自のスタイル機能など) を多用するとき。共通 API の外になる。
- ベクトルタイルレイヤーを共通 API で扱いたいとき。確かめた日の時点で README 上は計画段階である。
- 長期の保守体制を重視するとき。開発は 1 人のコミットが大半で、リポジトリも 2025 年以降に作られた新しいものである。
- Compose、SwiftUI、React 以外の UI (Android View、UIKit、Vue など) で使いたいとき。公開されているのはこの 3 種の宣言的 API である。

## 出典

- https://github.com/MapConductor
- https://github.com/MapConductor/.github/blob/main/profile/README.md
- https://github.com/MapConductor/android-sdk
- https://github.com/MapConductor/android-sdk/blob/develop/docs/architecture.md
- https://github.com/MapConductor/android-sdk/blob/develop/PUBLISHING.md
- https://github.com/MapConductor/android-sdk-core
- https://github.com/MapConductor/ios-sdk
- https://github.com/MapConductor/ios-sdk/blob/develop/docs/architecture.md
- https://github.com/MapConductor/ios-sdk-core
- https://github.com/MapConductor/react-sdk
- https://github.com/MapConductor/react-for-cesium
- https://github.com/MapConductor/webview-sdk
- https://mapconductor.com/
- https://mapconductor.com/architecture/
- https://mapconductor.com/team/
- https://docs-ios.mapconductor.com/
- https://repo1.maven.org/maven2/com/mapconductor/
- https://www.npmjs.com/org/mapconductor

## 未確認のこと

- MapTiler、TomTom、Longdo、Mappls、Open Mobile Maps、Leaflet、OpenLayers、Azure Maps、Cesium、deck.gl の各モジュールで、共通 API のどこまでが動くか: README の対応表に載っておらず、各リポジトリのコードまでは読んでいないため。
- react-for-mapkit が MapKit JS を使っているか: README と依存を確かめていないため (表では推測と明記)。
- 商用サポートや有償版の有無: 公式サイトに料金や商用提供の記載が無く、運営法人も書かれていないため。
- 実運用での採用例: 公式サイトとリポジトリに利用事例の記載が見つからなかったため。
