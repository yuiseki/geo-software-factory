# Mapbox Maps SDK (Android / iOS)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (プラットフォームごと、リリース日) | Android: v11.34.2 (2026-11-06)。iOS: 11.34.2 (2026-11-06)。次版 11.35.0-rc.1 が 2026-11-04 に出ている ([Android Releases](https://github.com/mapbox/mapbox-maps-android/releases)、[iOS Releases](https://github.com/mapbox/mapbox-maps-ios/releases)、[Android ガイド](https://docs.mapbox.com/android/maps/guides/)) |
| リポジトリ | https://github.com/mapbox/mapbox-maps-android 、https://github.com/mapbox/mapbox-maps-ios (ソースは公開されているが OSS ライセンスではない) |
| ドキュメント | https://docs.mapbox.com/android/maps/guides/ 、https://docs.mapbox.com/ios/maps/guides/ |
| ライセンス | プロプライエタリ。Mapbox TOS のもとで、有効な Mapbox アカウントを持つ開発者が Mapbox 製品と一緒に使う場合に限り利用・改変を認める。アカウントが失効すると自動で終了する。課金・計測・データ収集に関わる部分の改変は認めない ([LICENSE.md](https://github.com/mapbox/mapbox-maps-android/blob/main/LICENSE.md)) |
| 運営主体 | Mapbox, Inc. |

## 概要

Mapbox Style Specification に従うスタイルを Mapbox Vector Tile に適用し、Android では OpenGL、iOS では Metal で描画するネイティブ地図 SDK である ([Android README](https://github.com/mapbox/mapbox-maps-android)、[iOS README](https://github.com/mapbox/mapbox-maps-ios))。Mapbox のアカウントと公開アクセストークンを前提とし、利用量は MAU で課金される ([インストール](https://docs.mapbox.com/android/maps/guides/install/)、[料金](https://www.mapbox.com/pricing))。v11 では Mapbox Standard スタイルと地球儀表示を既定で使える。

## 対応プラットフォーム

| プラットフォーム | 対応 | 最低 OS 版・備考 |
|---|---|---|
| Android | 対応 | Android SDK 21 以上でビルドする必要がある。Vulkan バックエンドを使う場合は Android 12 (API 31) 以上を推奨 ([Android ガイド](https://docs.mapbox.com/android/maps/guides/)) |
| iOS | 対応 | iOS 14 以上。Xcode 16 以上 (推奨 26.4)、Swift 5.9 以上 ([iOS ガイド](https://docs.mapbox.com/ios/maps/guides/))。Package.swift に visionOS 1.0 の宣言がある ([Package.swift](https://github.com/mapbox/mapbox-maps-ios/blob/main/Package.swift)) |
| デスクトップ (macOS / Windows / Linux) | 非対応 | Package.swift のコメントに「Maps SDK は macOS に対応しない」とある ([Package.swift](https://github.com/mapbox/mapbox-maps-ios/blob/main/Package.swift)) |
| ゲームエンジン (Unreal / Unity など) | 別製品 | Unity 向けに Mapbox Unity SDK のリポジトリがあり、2026-10-20 に更新がある ([mapbox-unity-sdk](https://github.com/mapbox/mapbox-unity-sdk))。Maps SDK v11 との関係と対応状況は未確認。Unreal 向けは未確認 |

- UI フレームワーク (Jetpack Compose / SwiftUI / Flutter / React Native) への対応 (公式か非公式か): Jetpack Compose は公式の拡張 `com.mapbox.extension:maps-compose` (16 KB ページサイズ対応版は `maps-compose-ndk27`) がある。一部の高度な機能は Compose API にまだ無い ([Compose ガイド](https://docs.mapbox.com/android/maps/guides/using-jetpack-compose/))。SwiftUI は公式に対応し、「完全にサポートする」としつつ全 API ではないと注記する (カスタムのカメラアニメーションは対応中) ([SwiftUI ガイド](https://docs.mapbox.com/ios/maps/guides/swiftui/))。Flutter は Mapbox 公式の [mapbox-maps-flutter](https://github.com/mapbox/mapbox-maps-flutter)。React Native はコミュニティの [rnmapbox/maps](https://github.com/rnmapbox/maps)。

## 描画方式

- グラフィックス API (OpenGL ES / Metal / Vulkan など): Android は OpenGL ES が既定で、Vulkan バックエンドが Public Preview (arm64-v8a が必要、OpenGL の完全な置き換えではない) ([Android ガイド](https://docs.mapbox.com/android/maps/guides/))。iOS は Metal ([iOS README](https://github.com/mapbox/mapbox-maps-ios))。
- 2D / 2.5D / 3D、地球儀: 投影法は Globe、Mercator、Albers (v11.32.0 以降)。Mapbox Standard スタイル (またはそれを import して投影を指定しないスタイル) では既定で地球儀表示になり、それ以外のスタイルでは Mercator になる ([Projections](https://docs.mapbox.com/android/maps/guides/projections/))。Standard スタイルには 3D オブジェクトの表示切り替えの設定がある ([Set a style](https://docs.mapbox.com/ios/maps/guides/styles/set-a-style/))。

## 対応するタイル・データ

- 表示できるタイル・地図データ: Mapbox Style Specification のスタイルと Mapbox Vector Tile Specification のベクタータイル ([Android README](https://github.com/mapbox/mapbox-maps-android))。Mapbox の Vector Tiles API / Raster Tiles API 以外のタイル URL をスタイルに書けるかは未確認。
- 組み合わせの制約 (特定のタイルでしか使えない等): SDK のライセンスが Mapbox アカウントと Mapbox 製品での利用を条件にしている ([LICENSE.md](https://github.com/mapbox/mapbox-maps-android/blob/main/LICENSE.md))。自前のタイルだけを表示する場合も、アカウントとアクセストークンが必要で、MAU 課金の対象になると読める (推測。規約上の扱いは未確認)。
- オフライン地図: スタイルパック (スタイル JSON、スプライト、フォント) とタイルリージョン (GeoJSON の範囲とズーム範囲) を TileStore にダウンロードする。タイルリージョンが使うタイルパックは累計 750 個まで。オフラインデータは自動更新されない。Mapbox のサーバーから落としたオフライン地図を開発者や利用者が再配布すること、アプリに同梱することは規約で認められない ([Offline concepts](https://docs.mapbox.com/android/maps/guides/offline/concepts/)、[Offline](https://docs.mapbox.com/android/maps/guides/offline/))。

## ライセンスと費用

- SDK 自体のライセンス: プロプライエタリ (上記)。SDK は匿名化した位置・利用データを Mapbox に送る ([LICENSE.md](https://github.com/mapbox/mapbox-maps-android/blob/main/LICENSE.md))。
- 従量課金 (MAU、地図ロードなど、単価と無料枠): Maps SDKs for Mobile は MAU 課金 (請求期間内にアプリで Mapbox のサービスを使ったユーザー数)。2026-11-10 に確かめた料金 (USD、1,000 MAU あたり): 25,000 MAU まで無料、25,001〜125,000 は $4.00、125,001〜250,000 は $3.20、250,001 以上は $2.40、1,250,000 以上は営業に問い合わせ ([料金](https://www.mapbox.com/pricing)、[料金ガイド](https://docs.mapbox.com/accounts/guides/pricing/))。ネイティブ Maps SDK でタイル要求数による課金になる版は無い。iOS v5.0.0 以降、Android v8.0.0 以降が「Maps SDKs for mobile MAUs」で、それより古い版は Legacy の扱い ([料金ガイド](https://docs.mapbox.com/accounts/guides/pricing/))。

## Web 版との関係

- 同じスタイル仕様・同じ API の Web 版: Mapbox GL JS (v3 系、最新 v3.34.2、2026-11-03) が同じ Mapbox Style Specification を使う ([mapbox-gl-js Releases](https://github.com/mapbox/mapbox-gl-js/releases))。API はプラットフォームごとに別。GL JS をハイブリッドアプリに組み込んだ場合はタイル要求数または Web の地図ロードで課金される ([料金ガイド](https://docs.mapbox.com/accounts/guides/pricing/))。

## 開発の活発さ

- 直近 1 年のリリース数: 2025-11-10 から 2026-11-10 の GitHub Releases で、Android は安定版 81 件 (RC を含めると 106 件)、iOS は安定版 82 件 (同 107 件)。複数のマイナー系列 (例: 11.30.x、11.33.x、11.34.x) に並行してパッチを出している ([Android Releases](https://github.com/mapbox/mapbox-maps-android/releases)、[iOS Releases](https://github.com/mapbox/mapbox-maps-ios/releases))。
- 最終コミット日: Android 2026-11-09、iOS 2026-11-09 (main ブランチ)。

## 向いている場面

- 地図データ、スタイル、3D 表示、地球儀、オフラインを 1 社からまとめて調達したい場合。
- Compose / SwiftUI / Flutter の公式ラッパーを使いたい場合。
- 利用者数が 25,000 MAU 以下に収まるアプリ。

## 向いていない場面

- 地図の提供元を自分で選びたい、自前タイルだけで運用したい場合 (SDK の利用が Mapbox アカウントに結びつく)。
- オフライン地図をアプリに同梱して配布したい場合 (規約で認められない)。
- 利用者数が多く、MAU 課金が負担になる場合。
- デスクトップ (macOS / Windows / Linux) のネイティブアプリ。

## 出典

- https://github.com/mapbox/mapbox-maps-android
- https://github.com/mapbox/mapbox-maps-android/releases
- https://github.com/mapbox/mapbox-maps-android/blob/main/LICENSE.md
- https://github.com/mapbox/mapbox-maps-ios
- https://github.com/mapbox/mapbox-maps-ios/releases
- https://github.com/mapbox/mapbox-maps-ios/blob/main/Package.swift
- https://docs.mapbox.com/android/maps/guides/
- https://docs.mapbox.com/android/maps/guides/install/
- https://docs.mapbox.com/android/maps/guides/using-jetpack-compose/
- https://docs.mapbox.com/android/maps/guides/projections/
- https://docs.mapbox.com/android/maps/guides/offline/
- https://docs.mapbox.com/android/maps/guides/offline/concepts/
- https://docs.mapbox.com/ios/maps/guides/
- https://docs.mapbox.com/ios/maps/guides/swiftui/
- https://docs.mapbox.com/ios/maps/guides/styles/set-a-style/
- https://docs.mapbox.com/accounts/guides/pricing/
- https://www.mapbox.com/pricing
- https://github.com/mapbox/mapbox-gl-js/releases
- https://github.com/mapbox/mapbox-maps-flutter
- https://github.com/rnmapbox/maps
- https://github.com/mapbox/mapbox-unity-sdk

## 未確認のこと

- Mapbox 以外のタイル (自前の MVT やラスタータイル) を表示した場合の規約上の扱いと課金。ライセンス文は Mapbox 製品での利用を条件にしているが、自前タイルだけの利用について明記した箇所を見つけられなかった。
- オフライン利用が MAU に数えられるか。料金ガイドとオフラインのページに記載がなかった。
- visionOS の正式対応。Package.swift に宣言はあるが、ガイドの要件は iOS のみを挙げている。
- Mapbox Unity SDK と Maps SDK v11 の関係、Unreal 向けの提供の有無。
- 料金ページの通貨表記。「$」のみで通貨名の明記がなく、USD と読んだ。
