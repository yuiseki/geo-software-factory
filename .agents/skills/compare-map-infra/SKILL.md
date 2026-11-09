---
name: compare-map-infra
description: 地図プロダクトの要件に応じて、地図タイルサービス (tile.openstreetmap.org, tile.openstreetmap.jp, OpenFreeMap, Mapbox, Google Maps, Geolonia Maps, HERE, MapFan API など) を比較し技術選定する。個人利用か大規模な商用利用か、安定性や地図情報の詳しさがどこまで必要か、価格と機能と詳しさの釣り合いを軸に推奨を出す。「どの地図タイルを使うべき」「ベースマップの選定」「Google Maps の代わり」「地図 API の料金比較」と言われたら使う。
---

# compare-map-infra

> 骨組みの段階。以下の各節は後で書く。

| reference | 読むとき | 中身 |
|---|---|---|
| [criteria](references/criteria.md) | 比較を始める前に、いつも | 比較の軸と、要件から軸の重みを決める方法 |
| [providers/tile-openstreetmap-org](references/providers/tile-openstreetmap-org.md) | 候補に入れるとき | OSMF の公式タイル |
| [providers/tile-openstreetmap-jp](references/providers/tile-openstreetmap-jp.md) | 候補に入れるとき | OSMFJ のタイル |
| [providers/openfreemap](references/providers/openfreemap.md) | 候補に入れるとき | OpenFreeMap |
| [providers/mapbox](references/providers/mapbox.md) | 候補に入れるとき | Mapbox |
| [providers/google-maps](references/providers/google-maps.md) | 候補に入れるとき | Google Maps Platform |
| [providers/geolonia-maps](references/providers/geolonia-maps.md) | 候補に入れるとき | Geolonia Maps |
| [providers/here](references/providers/here.md) | 候補に入れるとき | HERE |
| [providers/mapfan-api](references/providers/mapfan-api.md) | 候補に入れるとき | MapFan API |

## 入力

後で書く: 必要な要件 (利用形態、規模、対象地域、詳しさ、端末、予算)。足りなければ grilling-map-product 相当の質問で先に聞く。

## 進め方

後で書く。候補:

1. 要件から足切り条件を決める (商用利用可否、利用規約、対象地域、ライブラリとの組み合わせ制約)
2. 残った候補を軸ごとに評価する
3. 規模ごとの費用を見積もる (無料枠を超える点を含めて)
4. 推奨を先に書き、続けて軸と候補ごとの評価を表で示す

## 大まかな指針

後で書く。たたき台:

- 個人で使うだけ、小規模、試作: OpenFreeMap で足りることが多い
- tile.openstreetmap.org / tile.openstreetmap.jp: 利用規約 (タイル利用ポリシー) で大量・商用のアクセスが制限される。本番の主たるタイル供給源にしない
- 大規模な商用利用、SLA、安定性、詳しい地図情報 (建物、住所、POI など) が必要: 商用サービスを検討する
- 商用サービスの中では、価格、機能 (ジオコーディング、ルート検索など)、地図情報の詳しさの釣り合いで選ぶ

## 出力

後で書く: 推奨、比較表、費用見積もり、確かめた日、未確認のこと。

## 注意

- 価格、無料枠、規約は頻繁に変わる。reference の数字は確かめた日つきで書き、答える前に公式ページで確かめ直す
- 利害関係の開示: このスキル集の作者は Geolonia Maps の提供元に関係している。Geolonia Maps を特別扱いしない
