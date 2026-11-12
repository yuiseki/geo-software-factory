# Google Maps SDK for Android / iOS

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (プラットフォームごと、リリース日) | Android: 20.1.0 (2026-10-12) ([Android リリースノート](https://developers.google.com/maps/documentation/android-sdk/release-notes))。iOS: 11.3.0 (2026-11-02) ([iOS リリースノート](https://developers.google.com/maps/documentation/ios-sdk/release-notes)、[ios-maps-sdk](https://github.com/googlemaps/ios-maps-sdk/releases)) |
| リポジトリ | SDK 本体のソースは非公開のため「なし」。iOS のバイナリ配布用の Swift Package が https://github.com/googlemaps/ios-maps-sdk にある。補助ライブラリ (Compose、Utils) は公開されている |
| ドキュメント | https://developers.google.com/maps/documentation/android-sdk 、https://developers.google.com/maps/documentation/ios-sdk |
| ライセンス | プロプライエタリ。Google Maps Platform の利用規約とサービス別規約に従う ([規約](https://cloud.google.com/maps-platform/terms)、[サービス別規約](https://cloud.google.com/maps-platform/terms/maps-service-terms)) |
| 運営主体 | Google |

## 概要

Google の地図 (道路地図、航空写真、地形など) を Android / iOS アプリに表示し、マーカー、ポリライン、ポリゴン、タイルオーバーレイを重ねる SDK である。Google Cloud のプロジェクトと API キーを前提とし、地図データは Google のもので差し替えられない。スタイルは Cloud Console の Map ID に結びつけて管理できる ([Map ID](https://developers.google.com/maps/documentation/android-sdk/map-ids/mapid-over))。写実的な 3D 地図は別の SDK (Maps 3D SDK、プレビュー) で提供される ([3D Maps の告知](https://mapsplatform.google.com/resources/blog/introducing-3d-maps-on-mobile-build-immersive-experiences-for-android-and-ios/))。

## 対応プラットフォーム

| プラットフォーム | 対応 | 最低 OS 版・備考 |
|---|---|---|
| Android | 対応 | `minSdk` 23 以上、`compileSdk` 34 以上。端末に Google Play 開発者サービスが必要 ([設定](https://developers.google.com/maps/documentation/android-sdk/config)) |
| iOS | 対応 | iOS 17 以上 (11.x 系)。Xcode 26 でのビルドが必要 ([iOS リリースノート](https://developers.google.com/maps/documentation/ios-sdk/release-notes)、[Package.swift](https://github.com/googlemaps/ios-maps-sdk/blob/main/Package.swift)) |
| デスクトップ (macOS / Windows / Linux) | 非対応 | ネイティブ SDK は Android と iOS のみ。デスクトップでは Maps JavaScript API を使う形になる |
| ゲームエンジン (Unreal / Unity など) | 対象外 | 本 SDK としての提供はない。3D の地図データは Map Tiles API の Photorealistic 3D Tiles として別に提供される ([料金](https://developers.google.com/maps/billing-and-pricing/pricing)) |

- UI フレームワーク (Jetpack Compose / SwiftUI / Flutter / React Native) への対応 (公式か非公式か): Compose は googlemaps organization の [android-maps-compose](https://github.com/googlemaps/android-maps-compose) (v9.0.1、Apache-2.0、API 24 以上)。ただし「Google Maps Platform の Core Service ではない」と明記され、サポートと SLA の対象外。SwiftUI 用のビューは無く、SDK は UIKit ベースで `UIViewRepresentable` などで包む必要がある ([iOS の地図](https://developers.google.com/maps/documentation/ios-sdk/map))。Google はそのためのコードラボを出している ([SwiftUI コードラボ](https://developers.google.com/codelabs/maps-platform/maps-platform-ios-swiftui))。Flutter は Flutter チームの `google_maps_flutter` ([flutter/packages](https://github.com/flutter/packages/tree/main/packages/google_maps_flutter))。React Native はコミュニティの [react-native-maps](https://github.com/react-native-maps/react-native-maps)。

## 描画方式

- グラフィックス API (OpenGL ES / Metal / Vulkan など): 未確認。iOS では PanoramaView (ストリートビュー) を OpenGL から Metal に移す旨の記載がある ([iOS リリースノート](https://developers.google.com/maps/documentation/ios-sdk/release-notes))。Android は「最新のレンダラー」と「旧レンダラー」の区別があり、Cloud ベースのスタイル設定には最新のレンダラーが必要 ([Map ID](https://developers.google.com/maps/documentation/android-sdk/map-ids/mapid-over))。
- 2D / 2.5D / 3D、地球儀: Maps SDK は 2D の地図に傾き・回転を加えた表示。写実的な 3D 地図は Maps 3D SDK for Android / iOS (`Map3DView`) が担う。Android 版は実験的プレビューで、最新は v0.2.2 (2026-08-07)、同時に有効にできる `Map3DView` は 1 つ ([3D Maps の告知](https://mapsplatform.google.com/resources/blog/introducing-3d-maps-on-mobile-build-immersive-experiences-for-android-and-ios/)、[3D 地図の追加](https://developers.google.com/maps/documentation/maps-3d/android-sdk/add-a-3d-map))。地球儀表示は未確認。

## 対応するタイル・データ

- 表示できるタイル・地図データ: 基盤の地図は Google の地図のみ。独自データは `TileOverlay` で URL 指定のラスタータイル (256 dp、高解像度端末向けに 512 px を推奨) を重ねられる。ベクタータイルのオーバーレイの記載はない ([TileOverlay](https://developers.google.com/maps/documentation/android-sdk/tileoverlay))。GeoJSON、KML、クラスタリングは補助ライブラリ [android-maps-utils](https://github.com/googlemaps/android-maps-utils) で扱う。
- 組み合わせの制約 (特定のタイルでしか使えない等): この SDK の基盤地図は Google の地図に固定で、他社のタイルに替えることはできない (ラスタータイルを上に重ねることはできる)。逆に Google の地図を他のレンダラーで描く場合は、この SDK ではなく Map Tiles API (別 SKU) を使う ([料金](https://developers.google.com/maps/billing-and-pricing/pricing))。Map ID による Android のベクター地図は「JavaScript のみ」と記載されている ([Map ID](https://developers.google.com/maps/documentation/android-sdk/map-ids/mapid-over))。
- オフライン地図: 未確認。開発者向けにオフライン領域をダウンロードする API の記載を公式ドキュメントで見つけられなかった。サービス別規約は一部データ (経路の緯度経度など) の最大 30 日の一時キャッシュのみを認めている ([サービス別規約](https://cloud.google.com/maps-platform/terms/maps-service-terms))。

## ライセンスと費用

- SDK 自体のライセンス: プロプライエタリ (Google Maps Platform 規約)。Compose / Utils の補助ライブラリは Apache-2.0。
- 従量課金 (MAU、地図ロードなど、単価と無料枠): 2026-11-10 に確かめた料金表で、SKU「Maps SDK」(旧 Mobile Native Dynamic Maps と Mobile Native Static Maps を統合) は Essentials 区分で無料上限が「Unlimited」、単価の記載なし ([料金](https://developers.google.com/maps/billing-and-pricing/pricing)、[SKU 詳細](https://developers.google.com/maps/billing-and-pricing/sku-details))。Maps 3D SDK はプレビュー中は無料で、一般提供時に従量課金になる予定 ([3D Maps の告知](https://mapsplatform.google.com/resources/blog/introducing-3d-maps-on-mobile-build-immersive-experiences-for-android-and-ios/))。Places、Routes などを併用した場合はそれぞれの SKU で課金される。

## Web 版との関係

- 同じスタイル仕様・同じ API の Web 版: Maps JavaScript API が Web 版にあたる。API は別物で、Web の地図表示は SKU「Dynamic Maps」(USD、1,000 回あたり $7.00、月 10,000 回まで無料、2026-11-10 確認) で課金される ([料金](https://developers.google.com/maps/billing-and-pricing/pricing))。Map ID によるスタイル設定は Web とモバイルで共有できる ([Map ID](https://developers.google.com/maps/documentation/android-sdk/map-ids/mapid-over))。

## 開発の活発さ

- 直近 1 年のリリース数: Android はリリースノートで 2 件 (20.0.0: 2026-01-31、20.1.0: 2026-10-12) ([Android リリースノート](https://developers.google.com/maps/documentation/android-sdk/release-notes))。iOS は ios-maps-sdk の GitHub Releases で 13 件 (10.x から 11.3.0) ([ios-maps-sdk Releases](https://github.com/googlemaps/ios-maps-sdk/releases))。android-maps-compose は同期間に 18 件 (うち RC 3 件)。
- 最終コミット日: 本体は非公開のため対象外。ios-maps-sdk は 2026-11-02、android-maps-compose は 2026-11-09。

## 環境の違いと保守

- ブラウザ間の互換: ネイティブ SDK なので、代わりに描画 API を見る。Android と iOS の地図の描画 API は文書に無く未確認 (上の「描画方式」)。iOS では 9.4.0 (2025-03-24) でストリートビューの `PanoramaView` を OpenGL から Metal に移し始め、これでシミュレーターの描画の不具合も直ると書いている ([iOS リリースノート](https://developers.google.com/maps/documentation/ios-sdk/release-notes))。本体は非公開で、CI で確かめている描画 API と端末は未確認。Web の対象は無く、Web は Maps JavaScript API の担当である。
- OS 間の互換: 文書でうたう最低版は Android の `minSdk` 23 (Google Play 開発者サービスが必要) と iOS 17 である (上の「対応プラットフォーム」)。iOS は 10.0.0 (2025-05-19) で iOS 15、11.3.0 (2026-11-02) で iOS 16 の対応を凍結しており、おおむね年 1 版ずつ最低版を上げている ([iOS リリースノート](https://developers.google.com/maps/documentation/ios-sdk/release-notes))。Android では Android 12 (API 31) 以上で `StrictMode` の `detectIncorrectContextUse` が違反を出す既知の問題があり、回避策だけが示されている ([Android リリースノート](https://developers.google.com/maps/documentation/android-sdk/release-notes))。試験している端末、GPU、メモリの上限への対応は未確認。
- 操作の網羅: Android の文書は、ズーム (ダブルタップ、二本指タップでの縮小、ピンチ、ダブルタップ後のスライド)、移動、傾き (二本指の上下)、回転 (二本指のひねり) を挙げ、`UiSettings` でそれぞれ無効にできる。ライトモードでは地図はビットマップで、移動もズームもできない ([コントロールと操作](https://developers.google.com/maps/documentation/android-sdk/controls))。iOS も同様の操作の設定がある (https://developers.google.com/maps/documentation/ios-sdk/controls)。キーボード、マウス、ペン、スクロールする親ビューの中での扱いは文書に無く未確認。
- エッジケースへの対応: iOS の 10.4.0 (2025-10-02) で、端末の回転を含むフレームの大きさのアニメーション中に地図のレイヤーがずれる不具合を直し、10.2.0 (2025-08-12) で異常終了を数える MetricKit を入れた ([iOS リリースノート](https://developers.google.com/maps/documentation/ios-sdk/release-notes))。開発者向けのオフライン領域の API は見つからない (上の「対応するタイル・データ」)。日付変更線、バックグラウンド移行、描画コンテキストの喪失、タイル読み込みの再試行についての文書は未確認。
- 継続的な保守: Android の地図の描画器は Google Play 開発者サービスの側で更新される面があり、20.0.0 で `org.apache.http.legacy` を外した結果、旧レンダラーを読むアプリが `NoClassDefFoundError` で落ちうるが、Google Play 開発者サービス 25.50.34 以降は影響を受けないと書いている ([Android リリースノート](https://developers.google.com/maps/documentation/android-sdk/release-notes))。iOS は 10.8.0 (2026-01-27) から Xcode 26 でのビルドを必須にした ([iOS リリースノート](https://developers.google.com/maps/documentation/ios-sdk/release-notes))。本体の不具合の追跡の仕方とプラットフォーム別の件数は未確認。

## 向いている場面

- Google の地図データ、POI、ストリートビューを使いたい場合。
- 地図表示の利用料をかけずにモバイルで地図を出したい場合 (Maps SDK SKU の無料上限が Unlimited)。
- Android で Compose、Flutter の公式系ラッパーを使いたい場合。

## 向いていない場面

- 自前の地図データやベクタータイルを基盤地図にしたい場合。
- オフライン地図が必要な場合。
- Google Play 開発者サービスの無い Android 端末で動かす場合。
- SwiftUI だけで書きたい場合 (UIKit のラップが必要)。
- iOS 16 以下を対象に含める場合 (11.x 系は iOS 17 以上)。

## 出典

- https://developers.google.com/maps/documentation/android-sdk
- https://developers.google.com/maps/documentation/android-sdk/release-notes
- https://developers.google.com/maps/documentation/android-sdk/config
- https://developers.google.com/maps/documentation/android-sdk/tileoverlay
- https://developers.google.com/maps/documentation/android-sdk/map-ids/mapid-over
- https://developers.google.com/maps/documentation/ios-sdk
- https://developers.google.com/maps/documentation/ios-sdk/release-notes
- https://developers.google.com/maps/documentation/ios-sdk/map
- https://developers.google.com/codelabs/maps-platform/maps-platform-ios-swiftui
- https://developers.google.com/maps/documentation/maps-3d/android-sdk/add-a-3d-map
- https://mapsplatform.google.com/resources/blog/introducing-3d-maps-on-mobile-build-immersive-experiences-for-android-and-ios/
- https://developers.google.com/maps/billing-and-pricing/pricing
- https://developers.google.com/maps/billing-and-pricing/sku-details
- https://cloud.google.com/maps-platform/terms
- https://cloud.google.com/maps-platform/terms/maps-service-terms
- https://github.com/googlemaps/ios-maps-sdk
- https://github.com/googlemaps/ios-maps-sdk/releases
- https://github.com/googlemaps/ios-maps-sdk/blob/main/Package.swift
- https://github.com/googlemaps/android-maps-compose
- https://github.com/googlemaps/android-maps-utils
- https://github.com/flutter/packages/tree/main/packages/google_maps_flutter
- https://github.com/react-native-maps/react-native-maps

## 未確認のこと

- Android / iOS の地図描画に使うグラフィックス API。公式ドキュメントに記載がなかった。
- オフライン地図の可否。公式ドキュメントで API を見つけられず、規約の該当条文も特定しきれなかった。
- 地球儀表示の有無。
- Maps SDK SKU の課金対象となるイベントの定義。SKU 詳細ページに記載がなかった。
- Android の直近 1 年のリリース数。リリースノートのページは主要版の告知のみで、パッチ版を含む全件か確かめられなかった。
- Maps 3D SDK for iOS の版と状態。Android 版のみ確かめた。
