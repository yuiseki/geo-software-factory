---
name: compare-map-infra
description: 地図プロダクトの要件に応じて、地図タイルの供給元 (tile.openstreetmap.org, tile.openstreetmap.jp, OpenFreeMap, Mapbox, Google Maps, Geolonia Maps, HERE, MapFan API などのサービス、または PMTiles や Planetiler による自前配信) を比較し技術選定する。個人利用か大規模な商用利用か、安定性や地図情報の詳しさがどこまで必要か、価格と機能と詳しさの釣り合い、自前で運用する負担を軸に推奨を出す。「どの地図タイルを使うべき」「ベースマップの選定」「Google Maps の代わり」「地図 API の料金比較」「タイルを自前で配信したい」と言われたら使う。
---

# compare-map-infra

> 骨組みの段階。以下の各節は後で書く。

| reference | 読むとき | 中身 |
|---|---|---|
| [criteria](references/criteria.md) | 比較を始める前に、いつも | 比較の軸と、要件から軸の重みを決める方法 |
| [self-hosting](references/self-hosting.md) | 自前配信を候補に入れるとき、商用サービスの費用が重いとき、外部通信が許されないとき | 自前でのタイル生成と配信の構成、費用、運用の負担 |
| [providers/tile-openstreetmap-org](references/providers/tile-openstreetmap-org.md) | 候補に入れるとき | OSMF の公式タイル |
| [providers/tile-openstreetmap-jp](references/providers/tile-openstreetmap-jp.md) | 候補に入れるとき | OSMFJ のタイル |
| [providers/openfreemap](references/providers/openfreemap.md) | 候補に入れるとき | OpenFreeMap |
| [providers/mapbox](references/providers/mapbox.md) | 候補に入れるとき | Mapbox |
| [providers/google-maps](references/providers/google-maps.md) | 候補に入れるとき | Google Maps Platform |
| [providers/geolonia-maps](references/providers/geolonia-maps.md) | 候補に入れるとき | Geolonia Maps |
| [providers/here](references/providers/here.md) | 候補に入れるとき | HERE |
| [providers/mapfan-api](references/providers/mapfan-api.md) | 候補に入れるとき | MapFan API |
| [providers/maptiler](references/providers/maptiler.md) | 候補に入れるとき | MapTiler Cloud |
| [providers/stadia-maps](references/providers/stadia-maps.md) | 候補に入れるとき | Stadia Maps (Stamen のスタイル) |
| [providers/esri-arcgis-location-platform](references/providers/esri-arcgis-location-platform.md) | 候補に入れるとき、ArcGIS の資産がある案件 | Esri ArcGIS Location Platform |
| [providers/tomtom](references/providers/tomtom.md) | 候補に入れるとき | TomTom Maps API |
| [providers/carto-basemaps](references/providers/carto-basemaps.md) | データ可視化の背景地図が要るとき | CARTO basemaps |
| [providers/gsi-tiles](references/providers/gsi-tiles.md) | 国内が対象のとき | 地理院タイル (国土地理院) |
| [providers/zenrin-maps-api](references/providers/zenrin-maps-api.md) | 国内で住宅地図レベルの詳しさが要るとき | ZENRIN Maps API |
| [regional/china](references/regional/china.md) | 中国本土が対象に入るとき | 法規制、GCJ-02 / BD-09、使えるサービス |
| [regional/korea](references/regional/korea.md) | 韓国が対象に入るとき | 法規制、使えるサービス |
| [imagery/esri-world-imagery](references/imagery/esri-world-imagery.md) | 衛星・航空写真が要るとき | Esri World Imagery |
| [imagery/eox-s2cloudless](references/imagery/eox-s2cloudless.md) | 衛星・航空写真が要るとき | EOX Sentinel-2 cloudless |
| [imagery/nasa-gibs](references/imagery/nasa-gibs.md) | 日次の全球画像や長期の時系列が要るとき | NASA GIBS |
| [3d/cesium-ion](references/3d/cesium-ion.md) | 3D の地形・建物が要るとき | Cesium ion |
| [3d/plateau](references/3d/plateau.md) | 国内の 3D 都市モデルが要るとき | PLATEAU |
| [niche](references/niche.md) | 上のどれも要件に合わないとき、特殊な主題・地域・画像が要るとき | 特定の要件でだけ候補になるもの |

## 入力

後で書く: 必要な要件 (利用形態、規模、対象地域、詳しさ、端末、予算、運用体制)。足りなければ grilling-map-product 相当の質問で先に聞く。

## 進め方

後で書く。候補:

1. 要件から足切り条件を決める (商用利用可否、利用規約、対象地域、ライブラリとの組み合わせ制約、外部通信の可否)
2. 残った候補を軸ごとに評価する。自前配信も 1 つの候補として同じ軸で並べる
3. 規模ごとの費用を見積もる (無料枠を超える点、自前配信との損益分岐を含めて)
4. 推奨を先に書き、続けて軸と候補ごとの評価を表で示す

## 大まかな指針

後で書く。たたき台:

- 個人で使うだけ、小規模、試作: OpenFreeMap で足りることが多い
- tile.openstreetmap.org / tile.openstreetmap.jp: 利用規約 (タイル利用ポリシー) で大量・商用のアクセスが制限される。本番の主たるタイル供給源にしない
- 大規模な商用利用、SLA、安定性、詳しい地図情報 (建物、住所、POI など) が必要: 商用サービスを検討する
- 商用サービスの中では、価格、機能 (ジオコーディング、ルート検索など)、地図情報の詳しさの釣り合いで選ぶ
- 表示回数が多い、外部通信が許されない、地図の中身を自分で決めたい: 自前配信 (PMTiles など) を検討する。ただし OSM 由来のデータの詳しさと、更新・監視の運用負担を引き受けることになる

## 出力

後で書く: 推奨、比較表、費用見積もり、確かめた日、未確認のこと。

## 注意

- 価格、無料枠、規約は頻繁に変わる。reference の数字は確かめた日つきで書き、答える前に公式ページで確かめ直す
- 利害関係の開示: このスキル集の作者は Geolonia Maps の提供元に関係している。Geolonia Maps を特別扱いしない
