# Apple MapKit

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (プラットフォームごと、リリース日) | MapKit は OS と Xcode の SDK に同梱され、単独の版番号を持たない。Apple のリリースノート一覧には iOS & iPadOS 27.2 まで掲載され、27.3 はベータ ([iOS & iPadOS リリースノート](https://developer.apple.com/documentation/ios-ipados-release-notes))。各 OS 版のリリース日は未確認。MapKit JS の最新の主要版は MapKit JS 6 ([MapKit JS リリースノート](https://developer.apple.com/documentation/mapkitjs/mapkit-js-release-notes)) |
| リポジトリ | なし (非公開) |
| ドキュメント | https://developer.apple.com/documentation/mapkit 、https://developer.apple.com/documentation/mapkitjs |
| ライセンス | プロプライエタリ。Apple の OS SDK の一部 (利用条件は Apple Developer Program の契約による。条文は未確認) |
| 運営主体 | Apple |

## 概要

Apple Maps の地図と航空写真をアプリのビューに埋め込み、注釈やオーバーレイを重ね、Look Around、地点検索の補完、住所と座標の変換を行うフレームワークである ([MapKit](https://developer.apple.com/documentation/mapkit))。UIKit / AppKit 向けの `MKMapView` と SwiftUI 向けの `Map` がある ([MKMapView](https://developer.apple.com/documentation/mapkit/mkmapview)、[Map](https://developer.apple.com/documentation/mapkit/map))。Web 向けには別の JavaScript API である MapKit JS がある ([MapKit JS](https://developer.apple.com/documentation/mapkitjs))。

## 対応プラットフォーム

| プラットフォーム | 対応 | 最低 OS 版・備考 |
|---|---|---|
| Android | ネイティブは非対応 | MapKit JS は Web ページやアプリ (iOS、Android を含む) に地図を埋め込める ([MapKit JS](https://developer.apple.com/documentation/mapkitjs)) |
| iOS | 対応 | フレームワークは iOS 3.0 から。SwiftUI の `Map` は iOS 14.0 から、`MapStyle` を含む新しい API は iOS 17.0 から ([MapKit](https://developer.apple.com/documentation/mapkit)、[Map](https://developer.apple.com/documentation/mapkit/map)、[MapStyle](https://developer.apple.com/documentation/mapkit/mapstyle)) |
| デスクトップ (macOS / Windows / Linux) | macOS のみ | macOS 10.9 から、Mac Catalyst 13.0 から。Windows / Linux はネイティブ非対応で、MapKit JS を使う ([MapKit](https://developer.apple.com/documentation/mapkit)、[Apple Maps](https://developer.apple.com/maps/)) |
| ゲームエンジン (Unreal / Unity など) | 対象外 | Apple のプラットフォームのフレームワークとしてのみ提供される |

- UI フレームワーク (Jetpack Compose / SwiftUI / Flutter / React Native) への対応 (公式か非公式か): SwiftUI は公式で、`Map` ビューを iOS 14.0 / macOS 11.0 / tvOS 14.0 / watchOS 7.0 / visionOS から提供する。マーカー、注釈、オーバーレイを `Map` の中に書ける ([Map](https://developer.apple.com/documentation/mapkit/map))。Jetpack Compose は対象外 (Android 非対応)。Flutter / React Native の公式ラッパーは無い (Apple が提供していないことを確かめた範囲で。コミュニティ製は未確認)。他に tvOS 9.2、watchOS 2.0、visionOS 1.0 から MapKit を使える ([MapKit](https://developer.apple.com/documentation/mapkit))。

## 描画方式

- グラフィックス API (OpenGL ES / Metal / Vulkan など): 未確認。公式ドキュメントに記載がない。
- 2D / 2.5D / 3D、地球儀: `MKMapView` は 2D と 3D の表示を持つ標準地図、航空写真と地図を重ねたハイブリッド、航空写真の各構成を持つ ([MKMapView](https://developer.apple.com/documentation/mapkit/mkmapview))。SwiftUI では `MapStyle` (iOS 17.0 以降) で標準・航空写真・ハイブリッドを切り替える ([MapStyle](https://developer.apple.com/documentation/mapkit/mapstyle))。地球儀表示は未確認。

## 対応するタイル・データ

- 表示できるタイル・地図データ: 基盤の地図は Apple Maps。独自のビットマップのタイルを `MKTileOverlay` で重ねる、または基盤地図を完全に置き換えることができる。URL テンプレートで x、y、ズーム、スケールを指定する ([MKTileOverlay](https://developer.apple.com/documentation/mapkit/mktileoverlay))。GeoJSON は `MKGeoJSONDecoder` で MapKit の型に変換できる (iOS 13.0 以降) ([MKGeoJSONDecoder](https://developer.apple.com/documentation/mapkit/mkgeojsondecoder))。ベクタータイルを読む API の記載はない。
- 組み合わせの制約 (特定のタイルでしか使えない等): 独自タイルはラスターのみ。Apple Maps の地図を MapKit 以外のレンダラーで描く手段は公開されていない (MapKit JS と Apple Maps Server API を除く)。
- オフライン地図: 未確認。開発者向けにオフライン領域をダウンロードする API の記載を見つけられなかった。

## ライセンスと費用

- SDK 自体のライセンス: プロプライエタリ (OS SDK の一部)。
- 従量課金 (MAU、地図ロードなど、単価と無料枠): ネイティブの MapKit の料金や利用上限は公開ページで見つけられず未確認。MapKit JS は Apple Developer Program のメンバーシップごとに 1 日あたり地図表示 250,000 回、サービス呼び出し 25,000 回、スナップショット 25,000 件 (固有のリクエスト) までが無料。それ以上は Apple に問い合わせる形で、超過時の料金や挙動は書かれていない ([MapKit JS](https://developer.apple.com/maps/web/))。MapKit JS の利用には Maps トークンが必要 ([MapKit JS](https://developer.apple.com/documentation/mapkitjs))。

## Web 版との関係

- 同じスタイル仕様・同じ API の Web 版: MapKit JS が Web 版にあたる。ネイティブの MapKit と同様に注釈とオーバーレイを重ねられ、場所の詳細ビューと Look Around も提供する ([MapKit JS](https://developer.apple.com/documentation/mapkitjs))。API は JavaScript で、ネイティブの API とは別物。共通のスタイル仕様は公開されていない。

## 開発の活発さ

- 直近 1 年のリリース数: 対象外。OS の更新とともに提供されるため、MapKit 単独のリリースはない。
- 最終コミット日: 対象外 (ソース非公開)。

## 環境の違いと保守

- ブラウザ間の互換: ネイティブの MapKit は OS のフレームワークで、描画 API は文書に無く未確認 (上の「描画方式」)。Web 版の MapKit JS は、最新版の Safari (macOS のみ)、Edge、Chrome、Firefox を、モバイルでは Safari (iOS と iPadOS のみ)、Edge、Chrome、Firefox を推奨ブラウザとしている ([Understanding Browser Support](https://developer.apple.com/documentation/mapkitjs/browser-support))。どのブラウザで自動テストしているかは非公開で未確認。
- OS 間の互換: 対応する OS は iOS、iPadOS、macOS、Mac Catalyst、tvOS、watchOS、visionOS で、API ごとに使える最低版が文書にある (上の「対応プラットフォーム」、[MapKit](https://developer.apple.com/documentation/mapkit))。地図は OS に含まれるため、端末と OS の組み合わせの確かめは Apple が持つ。Android、Windows、Linux はネイティブ非対応で MapKit JS を使う。GPU とメモリの上限への対応の文書は未確認。
- 操作の網羅: `MKMapView` はフリックとピンチでの移動とズームを既定で有効にし、`isScrollEnabled`、`isZoomEnabled`、`isRotateEnabled`、`isPitchEnabled` で切り替え、`cameraZoomRange` でズームの範囲を絞れる ([MKMapView](https://developer.apple.com/documentation/mapkit/mkmapview))。SwiftUI の `Map` は `MapInteractionModes` の `pan`、`zoom`、`pitch`、`rotate`、`all` で許す操作を選ぶ ([MapInteractionModes](https://developer.apple.com/documentation/mapkit/mapinteractionmodes))。macOS のトラックパッドとキーボード、visionOS の視線と手の操作の細部は未確認。
- エッジケースへの対応: 日付変更線、浮動小数点の精度、バックグラウンド移行、タイル読み込みの再試行の扱いを説明した文書は見つからなかった (未確認)。開発者向けのオフライン領域の API は見つからない (上の「対応するタイル・データ」)。MapKit JS は v6 で、タイル画像と注釈の画像を含むすべての画像に CORS を求めるようになった ([Migrating from version 5 to version 6](https://developer.apple.com/documentation/mapkitjs/migrating-from-version-5-to-version-6))。
- 継続的な保守: OS の更新とともに Apple が追随するため、利用者側の作業は OS の新版で非推奨になった API の置き換えが中心になる (推測)。iOS 17 で `MapStyle` などの新しい SwiftUI の API が入った (上の「対応プラットフォーム」)。MapKit JS の CSP の文書、プラットフォーム固有の不具合の公開の一覧はどちらも未確認。

## 向いている場面

- iOS / macOS / watchOS / tvOS / visionOS だけを対象にするアプリで、SwiftUI で地図を書きたい場合。
- Apple Maps の地図、Look Around、検索をそのまま使いたい場合。
- 外部の SDK を追加せずに地図を出したい場合。

## 向いていない場面

- Android を同じネイティブ SDK で対象にする場合 (Android はネイティブ非対応)。
- 自前のベクタータイルやスタイルで地図を描きたい場合 (独自タイルはラスターのみ)。
- オフライン地図が必要な場合 (開発者向け API を確かめられなかった)。
- Web で大量に地図を表示する場合 (MapKit JS の無料枠を超えると個別に問い合わせが要る)。

## 出典

- https://developer.apple.com/maps/
- https://developer.apple.com/maps/web/
- https://developer.apple.com/documentation/mapkit
- https://developer.apple.com/documentation/mapkit/map
- https://developer.apple.com/documentation/mapkit/mapstyle
- https://developer.apple.com/documentation/mapkit/mkmapview
- https://developer.apple.com/documentation/mapkit/mktileoverlay
- https://developer.apple.com/documentation/mapkit/mkgeojsondecoder
- https://developer.apple.com/documentation/mapkitjs
- https://developer.apple.com/documentation/mapkitjs/mapkit-js-release-notes
- https://developer.apple.com/documentation/ios-ipados-release-notes

## 未確認のこと

- ネイティブ MapKit の料金と利用上限。公開ページに記載を見つけられなかった。
- MapKit の利用条件の条文 (Apple Developer Program License Agreement の該当箇所)。読んでいない。
- 描画に使うグラフィックス API。公式ドキュメントに記載がない。
- 地球儀表示、開発者向けのオフライン地図 API の有無。公式ドキュメントで記載を見つけられなかった。
- iOS 27 系の各版のリリース日。リリースノート一覧から日付を取れなかった。
- Flutter / React Native のコミュニティ製ラッパーの状況。調べていない。
