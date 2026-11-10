---
name: compare-map-library
description: 地図プロダクトを実装するためのライブラリや SDK を、要件に応じて比較し技術選定する。Web (Leaflet, MapLibre GL JS, Mapbox GL JS, Google Maps JavaScript API, OpenLayers, CesiumJS, ArcGIS Maps SDK for JavaScript, deck.gl など)、ネイティブ (MapLibre Native, Mapbox Maps SDK, Google Maps SDK, Apple MapKit, Mapsui)、クロスプラットフォーム (react-native-maps, MapLibre React Native, flutter_map)、ゲームエンジン (Cesium for Unity / Unreal)、地図アプリの土台 (TerriaJS, Re:Earth Visualizer, kepler.gl)、複数 SDK の抽象化層 (MapConductor) を、対象端末、タイルの供給元との組み合わせ、ライセンス (コピーレフトを含む)、描画の能力、性能、保守体制、移行のしやすさで比べる。「地図ライブラリはどれがいい」「Leaflet と MapLibre どっち」「3D 地図を作りたい」「スマホアプリに地図を入れたい」「React Native や Flutter で地図」「地図 SDK を乗り換えたい」と言われたら使う。
---

# compare-map-library

地図プロダクトの要件から、地図を描くライブラリや SDK を選ぶ。Web のライブラリ、ネイティブ SDK、クロスプラットフォームのライブラリ、地図アプリの土台、複数 SDK の抽象化層を同じ軸で並べ、足切り、軸ごとの評価の順に比べて推奨を出す。比較の軸と、タイルの供給元との決め方は [criteria](references/criteria.md) にあり、各候補の事実は下の表の reference にある。

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
| [libraries/maptalks](references/libraries/maptalks.md) | Web で 2D と 3D を 1 つで扱いたいとき | maptalks.js |
| [libraries/openglobus](references/libraries/openglobus.md) | 地球儀型の 3D を CesiumJS 以外でも比べるとき | OpenGlobus |
| [libraries/navara](references/libraries/navara.md) | MapLibre 系で 3D を扱いたいとき | Navara |
| [libraries/globe-gl](references/libraries/globe-gl.md) | 全球のデータを地球儀で見せたいとき | globe.gl |
| [libraries/d3-geo](references/libraries/d3-geo.md) | タイルなしの主題図 (コロプレス図など) を描くとき | d3-geo |
| [libraries/arcgis-maps-sdk-js](references/libraries/arcgis-maps-sdk-js.md) | ArcGIS の資産がある案件、2D と 3D を同じ API で扱いたいとき | ArcGIS Maps SDK for JavaScript |
| [libraries/3d-tiles-renderer-js](references/libraries/3d-tiles-renderer-js.md) | three.js のアプリに 3D Tiles を載せたいとき | 3DTilesRendererJS |
| [frameworks/terriajs](references/frameworks/terriajs.md) | ライブラリから組まずに、地図アプリの土台を使うか検討するとき | TerriaJS |
| [frameworks/reearth-visualizer](references/frameworks/reearth-visualizer.md) | 同上。3D の Web GIS を組むとき | Re:Earth Visualizer |
| [frameworks/kepler-gl](references/frameworks/kepler-gl.md) | 同上。位置データの分析画面を作るとき | kepler.gl |
| [native/maplibre-native](references/native/maplibre-native.md) | ネイティブアプリで候補に入れるとき | MapLibre Native |
| [native/mapbox-maps-sdk](references/native/mapbox-maps-sdk.md) | ネイティブアプリで候補に入れるとき | Mapbox Maps SDK |
| [native/google-maps-sdk](references/native/google-maps-sdk.md) | ネイティブアプリで候補に入れるとき | Google Maps SDK for Android / iOS |
| [native/apple-mapkit](references/native/apple-mapkit.md) | iOS/macOS で候補に入れるとき | Apple MapKit |
| [native/cesium-native](references/native/cesium-native.md) | ゲームエンジン (Unreal, Unity) で 3D Tiles を扱うとき | Cesium Native |
| [native/mapsui](references/native/mapsui.md) | .NET のアプリに地図を入れるとき | Mapsui |
| [cross-platform/react-native-maps](references/cross-platform/react-native-maps.md) | React Native で OS 標準の地図を使うとき | react-native-maps |
| [cross-platform/maplibre-react-native](references/cross-platform/maplibre-react-native.md) | React Native で自前のタイルを使うとき | MapLibre React Native |
| [cross-platform/flutter-map](references/cross-platform/flutter-map.md) | Flutter で地図を使うとき | flutter_map |
| [niche](references/niche.md) | 上のどれも要件に合わないとき (屋内、完全オフライン、組み込み、非地理座標、印刷など) | 特定の要件でだけ候補になるもの |
| [multi-sdk/mapconductor](references/multi-sdk/mapconductor.md) | 複数の地図 SDK を併用・乗り換えしたいとき、複数プラットフォームで同じ書き方をしたいとき | MapConductor |

## 入力

比較の前に、次の要件をそろえる。プロダクト概要があればそこから読み、無ければ依頼から読み取る。

- 対象端末: Web、Android、iOS、デスクトップ、ゲームエンジン、組み込み機器。モバイルならネイティブ (Compose、SwiftUI)、React Native、Flutter のどれで作るか
- 使うタイルや地図データの供給元 (決まっていれば)
- 描画に要るもの: ベクトルタイルと配色の作り込み、3D 建物、地形、地球儀、3D Tiles
- 表示するデータの量と形式: 地物の件数、GeoJSON、ベクトルタイル、点群など
- 配布形態: SaaS、アプリのストア配布、受託で納品、OSS として公開
- 開発体制と保守の期間、既存のアプリや社内の標準
- 将来の乗り換えや、複数の地図 SDK の併用の見込み
- 特殊な要件: 屋内、完全オフライン、印刷、地理座標を持たない画像

対象端末と配布形態が分からないまま比較に入らない。足切りがこの 2 つで決まるので、分からなければ先に聞く。聞くときは選択肢で答えられる形にし、1 回に聞く数を絞る。要件が全体に曖昧なら、比較の前にプロダクトの価値から聞き直す (grilling-map-product に当たる手順)。

## 進め方

1. [criteria](references/criteria.md) を読み、「要件から軸の重みを決める」の表で、当てる足切りの条件と重くする軸を決める。
2. タイルの供給元との関係を決める。[criteria](references/criteria.md) の「タイルの供給元との関係」の順に従う。供給元が決まっていなければ、compare-map-infra と並行して決める。
3. 候補を集める。下の「最初の当たり」から要件に合うものを選び、表の「読むとき」に当てはまる reference を開く。ライブラリから組まずに済むか (`frameworks/`) と、特殊な要件 ([niche](references/niche.md)) も確かめる。
4. 足切りの条件で候補を外す。ライセンスは本体だけでなく、主要な依存と推奨されるプラグインも見る。外した候補と理由を残す。
5. 残った候補を評価の軸で比べる。値は各 reference から写し、reference に「未確認」とあるものは未確認のまま書く。性能が結論を左右するなら、要件の件数で試作して測ることを勧める。
6. 版、ライセンス、課金は、答える前に公式ページやリポジトリで確かめ直す。reference の確認日から変わっていれば新しい値を使い、変わったことを書く。確かめ直せなければ、reference の確認日を添えて出す。
7. 「出力」の形で答える。

## 最初の当たり

候補を集めるときの出発点。どれも足切りと評価の軸で確かめてから推奨する。

- Web で少しのマーカーを置くだけ: Leaflet (安定版は 1.x、2.0 は移行中)
- Web でベクトルタイル、配色の作り込み、大量の地物: MapLibre GL JS
- Web で地球儀、3D Tiles、地形: CesiumJS。three.js のアプリに 3D Tiles を載せるなら 3DTilesRendererJS
- ArcGIS の資産がある案件: ArcGIS Maps SDK for JavaScript
- 大量データの可視化: deck.gl を地図ライブラリに重ねる
- パン・ズームしない主題図: d3-geo
- ネイティブアプリで自前のタイル: MapLibre Native。Google の地図なら Google Maps SDK、iOS だけなら Apple MapKit も候補
- React Native: OS 標準の地図なら react-native-maps (Web 非対応)、自前のタイルなら MapLibre React Native
- Flutter: flutter_map (オフライン用の推奨プラグインは GPL-3.0)
- .NET: Mapsui
- ゲームエンジンで 3D の都市や地形: Cesium for Unity / Unreal (Cesium Native の reference の節)
- Web とアプリで同じ見た目: MapLibre GL JS と MapLibre Native (同じスタイル仕様)
- 開発の手間を減らしたい GIS 画面: 地図アプリの土台 (TerriaJS、Re:Earth Visualizer、kepler.gl)
- 地図 SDK の乗り換えや併用: 抽象化層 (MapConductor)

## 出力

答えは次の順に並べる。

1. 推奨: 1 つ (条件で分かれるなら条件ごとに 1 つ) と、その理由を 2〜3 文。組み合わせるタイルの供給元も書く。
2. 足切りで外した候補と理由。
3. 比較表: 行に評価の軸、列に残った候補。各セルに値と reference の根拠。
4. ライセンスの注意: 推奨した候補と、その主要な依存・プラグインについて、要件の配布形態で求められること。
5. 確かめた日と版: 公式ページやリポジトリで確かめた日と、比べた版。確かめ直せなかった項目は reference の確認日。
6. 未確認のこと: 結論を左右するのに確かめられなかったこと。性能が結論を左右するなら、試作して測る手順を添える。

## 注意

- ライブラリの版で API とライセンスが変わる (Mapbox GL JS は v1 系と v2 以降でライセンスが違う)。比べた版を必ず書く。
- 性能の数字は、測った条件 (端末、データ件数、版) つきで書く。条件の無い数字で比べない。
- ライブラリの選択で、組み合わせるタイルの課金単位が変わることがある (Mapbox、MapTiler)。費用に効くときは compare-map-infra の費用の見積もりに戻す。
- 規約やライセンスの解釈は、条文から読んだものと推測を分けて書く。法的な判断を断定しない。
