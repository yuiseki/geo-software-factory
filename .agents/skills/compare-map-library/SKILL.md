---
name: compare-map-library
description: 地図プロダクトを実装するためのライブラリ/SDK を、地図プロダクトの要件に応じて比較し技術選定する。Web (Leaflet, MapLibre GL JS, Mapbox GL JS, Google Maps JavaScript API, CesiumJS, OpenLayers, deck.gl など)、ネイティブアプリ (MapLibre Native, Mapbox Maps SDK, Google Maps SDK for Android/iOS, Apple MapKit など)、複数 SDK の抽象化層 (MapConductor など) を扱う。描画方式 (ラスタ/ベクトル、2D/3D)、対象端末、組み合わせるタイルサービス、ライセンスと費用、データ量と性能を軸に推奨を出す。「地図ライブラリはどれがいい」「Leaflet と MapLibre どっち」「3D 地図を作りたい」「スマホアプリに地図を入れたい」「地図 SDK を乗り換えたい」と言われたら使う。
---

# compare-map-library

> 骨組みの段階。以下の各節は後で書く。

| reference | 読むとき | 中身 |
|---|---|---|
| [criteria](references/criteria.md) | 比較を始める前に、いつも | 比較の軸と、要件から軸の重みを決める方法 |
| [libraries/leaflet](references/libraries/leaflet.md) | Web で候補に入れるとき | Leaflet |
| [libraries/maplibre-gl-js](references/libraries/maplibre-gl-js.md) | Web で候補に入れるとき | MapLibre GL JS |
| [libraries/mapbox-gl-js](references/libraries/mapbox-gl-js.md) | Web で候補に入れるとき | Mapbox GL JS |
| [libraries/google-maps-js](references/libraries/google-maps-js.md) | Web で候補に入れるとき | Google Maps JavaScript API |
| [libraries/cesiumjs](references/libraries/cesiumjs.md) | Web で候補に入れるとき | CesiumJS |
| [libraries/openlayers](references/libraries/openlayers.md) | Web で候補に入れるとき | OpenLayers |
| [libraries/deck-gl](references/libraries/deck-gl.md) | Web で候補に入れるとき | deck.gl |
| [native/maplibre-native](references/native/maplibre-native.md) | ネイティブアプリで候補に入れるとき | MapLibre Native |
| [native/mapbox-maps-sdk](references/native/mapbox-maps-sdk.md) | ネイティブアプリで候補に入れるとき | Mapbox Maps SDK |
| [native/google-maps-sdk](references/native/google-maps-sdk.md) | ネイティブアプリで候補に入れるとき | Google Maps SDK for Android / iOS |
| [native/apple-mapkit](references/native/apple-mapkit.md) | iOS/macOS で候補に入れるとき | Apple MapKit |
| [multi-sdk/mapconductor](references/multi-sdk/mapconductor.md) | 複数の地図 SDK を併用・乗り換えしたいとき、複数プラットフォームで同じ書き方をしたいとき | MapConductor |

## 入力

後で書く: 必要な要件 (対象端末と UI フレームワーク、2D/3D、表示するデータの量と形式、使うタイルサービス、ライセンスの制約、将来の乗り換えの可能性)。タイルサービスが決まっていれば、その組み合わせ制約を先に当てる。

## 進め方

後で書く。候補:

1. 対象端末で分ける (Web / ネイティブ / 両方)
2. タイルサービスとの組み合わせ制約で足切りする (例: Google Maps のタイルは Google Maps の SDK で表示する)
3. 2D/3D、ベクトルタイルの要否、データ量で候補を絞る
4. ライセンス (OSS か商用か、利用料の有無) と費用を確かめる
5. 地図 SDK の乗り換えや併用が見込まれるなら、抽象化層 (MapConductor など) を挟むかを検討する
6. 推奨を先に書き、続けて軸と候補ごとの評価を表で示す

## 大まかな指針

後で書く。たたき台:

- ラスタタイルに少しのマーカーを置くだけ: Leaflet
- ベクトルタイル、スタイル編集、大量の地物: MapLibre GL JS
- 地球儀、3D Tiles、地形: CesiumJS
- 大量データの可視化レイヤー: deck.gl を他の地図ライブラリに重ねる
- Google Maps のタイルや Places を使う: Google Maps JavaScript API / Google Maps SDK
- Web とネイティブで同じスタイルを使いたい: MapLibre GL JS + MapLibre Native
- 地図 SDK を将来乗り換えうる、複数 SDK を併用する: 抽象化層を検討する

## 出力

後で書く: 推奨、比較表、確かめた日と版、未確認のこと。

## 注意

- ライブラリの版で API とライセンスが変わる (例: Mapbox GL JS v2 以降のライセンス変更)。reference には確かめた版を書く
- 性能の数字は、測った条件 (端末、データ件数、版) つきで書く
