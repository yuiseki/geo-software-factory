# Mapsui (.NET)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 5.1.0 (2026-05-27 JST)。5.2.0-beta.1 (2026-10-16 JST) が出ているが、GitHub Releases では prerelease の印が付いていないため `releases/latest` はこれを返す。NuGet の最新の安定版は 5.1.0 (https://github.com/Mapsui/Mapsui/releases/tag/5.1.0 、 https://www.nuget.org/packages/Mapsui) |
| リポジトリ | https://github.com/Mapsui/Mapsui |
| ドキュメント | https://mapsui.com/v5/ |
| ライセンス (LICENSE ファイルで確かめる) | MIT (Copyright (c) 2022 The Mapsui authors) (https://github.com/Mapsui/Mapsui/blob/main/LICENSE) |
| 運営主体・ガバナンス | GitHub の `Mapsui` Organization。GitHub Sponsors は pauldendulk 個人宛てで、Uno Platform などがスポンサーに並ぶ (https://github.com/Mapsui/Mapsui#sponsors-%EF%B8%8F) |

## 概要

.NET の主要な UI フレームワークで使える地図コンポーネント。SharpMap から派生し、ジオメトリに NetTopologySuite (NTS)、タイルの取得に BruTile、描画に SkiaSharp を使う (https://github.com/Mapsui/Mapsui#thanks-go-to)。OpenStreetMap などのタイル、WMS、WFS、WMTS、MBTiles を扱え、静的な地図画像の生成もできる (https://mapsui.com/v5/)。UI フレームワークごとに `Mapsui.Maui`、`Mapsui.Avalonia`、`Mapsui.Wpf` などの NuGet パッケージがあり、地図の中身のコードは共通にできる (https://github.com/Mapsui/Mapsui#ui-framework-nugets)。

## 対応プラットフォーム

| プラットフォーム | 対応 | 最低 OS 版・備考 |
|---|---|---|
| Android | 対応 | `Mapsui.Android` (.NET for Android、5.1.0 では net8.0-android と net9.0-android、`SupportedOSPlatformVersion` 21)、`Mapsui.Maui`、`Mapsui.Uno.WinUI`、Avalonia 経由 (https://github.com/Mapsui/Mapsui/blob/5.1.0/Mapsui.UI.Android/Mapsui.UI.Android.csproj) |
| iOS | 対応 | `Mapsui.iOS` (net9.0-ios)、`Mapsui.Uno.WinUI` (net9.0-ios、net9.0-maccatalyst)、`Mapsui.Maui`、Avalonia 経由。最低 iOS 版は未確認 (https://github.com/Mapsui/Mapsui/blob/5.1.0/Mapsui.UI.iOS/Mapsui.UI.iOS.csproj) |
| Web | 対応 | `Mapsui.Blazor` (SkiaSharp.Views.Blazor と WebAssembly 用ネイティブアセットを使う)。Avalonia と Uno Platform の WebAssembly 版もある (https://github.com/Mapsui/Mapsui/blob/5.1.0/Mapsui.UI.Blazor/Mapsui.UI.Blazor.csproj 、 https://mapsui.com/v5/) |
| デスクトップ (macOS / Windows / Linux) | 対応 | Windows は WPF (net8.0-windows、net9.0-windows)、WinUI 3、Windows Forms。macOS と Linux は Avalonia、Eto Forms、Uno Platform で使える (https://github.com/Mapsui/Mapsui#ui-framework-nugets) |

- フレームワークの版の要件: 5.1.0 のコア (`Mapsui`、`Mapsui.Rendering.Skia`、`Mapsui.Tiling`、`Mapsui.Nts`) は net8.0 と net9.0 を対象にする。`Mapsui.Maui` 5.1.0 の NuGet は net9.0 と net9.0-android の 2 つの対象しか持たない。Uno は 5.1.0 で .NET 8 の対象を外した。ドキュメントのクイックスタートは Blazor に .NET 8 以上、WPF と Eto に .NET 9 以上を求める。Avalonia 12 向けには別パッケージ `Mapsui.Avalonia12` がある (https://github.com/Mapsui/Mapsui/blob/5.1.0/Mapsui/Mapsui.csproj 、 https://www.nuget.org/packages/Mapsui.Maui/5.1.0 、 https://github.com/Mapsui/Mapsui/releases/tag/5.1.0 、 https://mapsui.com/v5/)

## 描画方式

- 自前で描画するか、OS や他の SDK のラッパーか: 自前で描画する。OS の地図 SDK を使わず、SkiaSharp (Skia の .NET バインディング) で全プラットフォーム共通に描く。各 UI フレームワーク向けパッケージは SkiaSharp のビュー (SKGLView など) を載せる薄い層 (https://github.com/Mapsui/Mapsui#thanks-go-to 、 https://mapsui.com/v5/)
- ラスタ / ベクトルタイル、2D / 3D: 2D。ラスタタイルが中心で、ベクトルタイルは実験的パッケージ `Mapsui.Experimental.VectorTiles` が VexTile を使って描く。5.1.0 のリリースノートに「VexTile VectorTiles で PNG の圧縮と展開を避ける改善」「vector tile as PNG の性能改善」とあり、ベクトルタイルを画像に変換してタイルとして表示する方式と読める (推測)。3D 表示は無い (https://mapsui.com/v5/experimental-packages/ 、 https://github.com/Mapsui/Mapsui/releases/tag/5.1.0)

## 対応するタイル・データ

- 表示できるタイル・地図データ: BruTile 経由の XYZ / TMS / WMTS などのタイル (OpenStreetMap を含む)、WMS、WFS、MBTiles (BruTile.MbTiles)、ArcGIS のサービス (`Mapsui.ArcGIS`)、NTS のジオメトリ、GeoJSON、GeoTIFF (サンプルあり)、Shapefile (サンプルあり)。ベクトルタイル (MVT) は実験的パッケージ (https://mapsui.com/v5/ 、 https://github.com/Mapsui/Mapsui/tree/main/docs/codesamples)
- 組み合わせの制約 (下にある SDK の規約・課金を引き継ぐか): 下に地図 SDK は無いので、規約と課金はタイルや WMS の提供元だけで決まる。OSM の公開タイルを使うなら OSM の利用方針と帰属表示に従う
- オフライン地図: MBTiles (SQLite に保存したタイル) で実現できる、とドキュメントが書く (https://mapsui.com/v5/)

## ライセンスと費用

- ライセンス: MIT。
- 下にある SDK の費用: 対象外 (下にある地図 SDK が無い)。費用はタイル配信の提供元か自前配信のインフラで決まる
- ライセンス上の注意: なし (コピーレフトの依存は見当たらない)。主な依存のライセンスは、SkiaSharp と HarfBuzzSharp が MIT、BruTile が Apache-2.0、Svg.Skia が MIT、Topten.RichTextKit が Apache-2.0、BitMiracle.LibTiff.NET が BSD 系、sqlite-net が MIT、SQLitePCLRaw が Apache-2.0、DotSpatial.Projections が MIT、NetTopologySuite.IO.VectorTiles が MIT、NetTopologySuite.IO.GeoJSON4STJ が BSD-3-Clause、VexTile.Renderers が MIT。NetTopologySuite 本体は BSD-3-Clause である。JTS から移植した部分は Eclipse Public License 1.0 と Eclipse Distribution License 1.0 (BSD 系) の選択制なので、EDL を選べば弱いコピーレフトの EPL の条件 (改変したソースの開示) を負わずに済む。Apache-2.0 の依存は配布時に NOTICE ファイルの扱いに注意する。配布時はこれらの著作権表示を含める (https://github.com/NetTopologySuite/NetTopologySuite/blob/develop/License.md 、 https://github.com/Mapsui/Mapsui/blob/main/Directory.Packages.props 、 https://github.com/BruTile/BruTile 、 https://github.com/memsom/VexTile.Renderers)

## エコシステム

- 主なプラグイン・拡張: 公式の追加パッケージとして `Mapsui.Nts` (NTS のジオメトリ)、`Mapsui.Tiling` (BruTile のタイル)、`Mapsui.ArcGIS`、`Mapsui.Extensions` (GeoTIFF、MBTiles、投影変換など)、実験的な `Mapsui.Experimental`、`Mapsui.Experimental.VectorTiles`、`Mapsui.Experimental.Rendering.Skia` (描画の書き直し) がある。実験的パッケージはパッチ版でも破壊的変更がありうる、とドキュメントが書く (https://github.com/Mapsui/Mapsui#core-nugets 、 https://mapsui.com/v5/experimental-packages/)
- 似た位置づけの他のライブラリとの違い: .NET MAUI 標準の `Microsoft.Maui.Controls.Maps` は OS の地図 (Android の Google Maps、iOS の Apple MapKit) を包むので、Windows や Linux では使えず、下の SDK の規約を引き継ぐ (推測)。Esri の ArcGIS Maps SDK for .NET は 3D や高度な GIS 機能を持つ商用 SDK。Mapsui は全 UI フレームワークで同じ描画を持ち、ライセンス費が無い代わりに 2D とラスタ中心である

## 開発の活発さ

- 直近 1 年のリリース数: 安定版 3 (5.0.1、5.0.2、5.1.0)、ベータ 10 (5.1.0-beta.2 から 5.1.0-beta.10、5.2.0-beta.1) (2025-11-10 から 2026-11-10 の GitHub Releases。ドキュメント凍結用のタグ `pages-v4-frozen-2026-07-26` は数えない)
- 最終コミット日: 2026-11-09 JST (main、WFS 2.0 の GetFeature フィルタの修正のマージ)
- 主なメンテナー (個人か組織か): Organization 管理だが、実質は pauldendulk 個人が中心。直近 1 年のコミットは pauldendulk が 438 件で、次の Copilot (15 件) 以下を大きく引き離す。累計では pauldendulk、inforithmics、charlenni が多い (https://github.com/Mapsui/Mapsui/graphs/contributors)

## 向いている場面

- .NET (MAUI、WPF、Avalonia、Uno、Blazor など) のアプリに、ライセンス費の無い 2D 地図を入れたいとき。
- Windows のデスクトップ業務アプリで WMS、WFS、WMTS、ArcGIS のサービスを重ねたいとき。
- 複数の UI フレームワークで地図のロジックを共有したいとき。
- 静的な地図画像をサーバー側で生成したいとき。

## 向いていない場面

- ベクトルタイルとスタイル JSON を本番で使いたいとき (実験的パッケージのみ)。
- 3D 地図、地形、建物の立体表示が要るとき。
- 主要な開発者 1 人への依存を避けたいとき。
- Google マップや Apple マップの見た目をそのまま使いたいとき。

## 出典

- https://github.com/Mapsui/Mapsui
- https://github.com/Mapsui/Mapsui/blob/main/LICENSE
- https://github.com/Mapsui/Mapsui#thanks-go-to
- https://github.com/Mapsui/Mapsui#ui-framework-nugets
- https://github.com/Mapsui/Mapsui#core-nugets
- https://github.com/Mapsui/Mapsui#sponsors-%EF%B8%8F
- https://github.com/Mapsui/Mapsui/releases/tag/5.1.0
- https://github.com/Mapsui/Mapsui/blob/5.1.0/Mapsui/Mapsui.csproj
- https://github.com/Mapsui/Mapsui/blob/5.1.0/Mapsui.UI.Android/Mapsui.UI.Android.csproj
- https://github.com/Mapsui/Mapsui/blob/5.1.0/Mapsui.UI.iOS/Mapsui.UI.iOS.csproj
- https://github.com/Mapsui/Mapsui/blob/5.1.0/Mapsui.UI.Blazor/Mapsui.UI.Blazor.csproj
- https://github.com/Mapsui/Mapsui/blob/main/Directory.Packages.props
- https://github.com/Mapsui/Mapsui/tree/main/docs/codesamples
- https://github.com/Mapsui/Mapsui/graphs/contributors
- https://mapsui.com/v5/
- https://mapsui.com/v5/experimental-packages/
- https://www.nuget.org/packages/Mapsui
- https://www.nuget.org/packages/Mapsui.Maui/5.1.0
- https://github.com/NetTopologySuite/NetTopologySuite/blob/develop/License.md
- https://github.com/BruTile/BruTile
- https://github.com/memsom/VexTile.Renderers

## 未確認のこと

- iOS の最低版: `Mapsui.iOS` の csproj に `SupportedOSPlatformVersion` が無く、.NET for iOS の既定値を確かめていない。
- `Mapsui.Maui` が iOS、Mac Catalyst、Windows でどう動くか: NuGet の対象が net9.0 と net9.0-android だけで、iOS などでは net9.0 のアセットと SkiaSharp の MAUI 実装で動くと思われるが、試していない (推測)。
- ベクトルタイルの描画方式: リリースノートの記述から画像化して表示すると読んだが、実装を読んで確かめていない。
- .NET MAUI 標準の地図コントロールや ArcGIS Maps SDK との比較: それぞれの公式ドキュメントを確かめていない。
- 依存ライセンスは 5.1.0 時点ではなく main ブランチの `Directory.Packages.props` で確かめた。
