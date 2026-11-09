# MapConductor

> 後で書く。各項目に確かめた日、版、出典を添える。確かめていない項目は「未確認」と書く。

確かめた日: 未確認
出典: https://github.com/MapConductor

## 概要

複数の地図 SDK を共通の API で扱うための抽象化ライブラリ。地図を描くのは下にある各地図 SDK で、MapConductor はその上に載る層。詳細は後で書く。

## 対応プラットフォームと下にある地図 SDK

後で書く。GitHub org に android-sdk / ios-sdk / react-sdk と、地図 SDK ごとのモジュール (`<platform>-for-<sdk>`: Google Maps, MapLibre, Mapbox, HERE, MapKit, ArcGIS, TomTom, MapTiler, Leaflet, OpenLayers, Cesium, deck.gl など) がある (2026-11-10 にリポジトリ名で確認。各モジュールの成熟度は未確認)。

## ライセンス

2026-11-10 に GitHub API のライセンス判定で確かめた値。

| リポジトリ | 判定 |
|---|---|
| android-sdk, android-sdk-core, ios-sdk, ios-sdk-core | Apache-2.0 |
| react-sdk | MIT |
| 地図 SDK ごとのモジュール (react-for-maplibre など、確かめたもの) | Apache-2.0 |
| react-for-cesium | NOASSERTION (LICENSE の実体は未確認) |

下にある地図 SDK のライセンスと料金は別にかかる。

## 何が楽になるか

後で書く: 地図 SDK の乗り換え、複数 SDK の併用、マーカー・図形などのオーバーレイの共通化。

## 何が楽にならないか

後で書く: 下にある SDK の料金・規約・タイル制約は残る。共通 API に無い SDK 固有機能の扱い。

## 向いている場面 / 向いていない場面

後で書く。

## 執筆上の注意

他の候補と同じ粒度で書く。公開リポジトリから確かめられることだけを書く。
