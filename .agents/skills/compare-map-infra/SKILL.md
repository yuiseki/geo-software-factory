---
name: compare-map-infra
description: 地図プロダクトの要件に応じて、ベースマップ、衛星・航空写真、3D データの供給元を比較し技術選定する。商用サービス (Google Maps, Mapbox, MapTiler, Esri, HERE, TomTom, Geolonia Maps, ZENRIN, MapFan など)、無償の公開タイル (OpenStreetMap, OpenFreeMap)、公的データ (地理院タイル, PLATEAU)、PMTiles などによる自前配信を、足切り (商用可否、公共案件、地域の法規制、ライブラリとの組み合わせ)、地図の詳しさ、安定性、ライセンス、移行のしやすさ、課金単位を揃えた費用で比べる。「どの地図タイルを使うべき」「ベースマップの選定」「Google Maps の代わり」「地図 API の料金比較」「衛星画像はどこから」「中国や韓国の地図」「タイルを自前で配信したい」と言われたら使う。
---

# compare-map-infra

地図プロダクトの要件から、ベースマップや衛星画像、3D データの供給元を選ぶ。商用サービス、無償の公開タイル、公的データ、自前配信を同じ軸で並べ、足切り、軸ごとの評価、規模ごとの費用の順に比べて推奨を出す。比較の軸と費用の見積もり方は [criteria](references/criteria.md) にあり、各供給元の事実は下の表の reference にある。

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

比較の前に、次の要件をそろえる。プロダクト概要があればそこから読み、無ければ依頼から読み取る。

- 利用形態: 個人、社内、商用 (営利組織か)、自治体・公共の案件か、受託で納品するか
- 規模: 月間の地図表示回数。分からなければ、利用者数と 1 人あたりの地図を開く回数から見積もる
- 対象地域: 国内だけか、全球か。中国本土や韓国が入るか
- 必要な地図の詳しさ: 住所・番地、建物、POI、日本語の注記、公的な正確さ
- 地図以外に要るもの: 衛星・航空写真、地形、3D、ジオコーディング、ルート検索
- 対象端末と、使う描画ライブラリ (決まっていれば)
- 外部通信の可否: 閉域網、オフライン
- 運用体制と予算、SLA の要否

利用形態、規模、対象地域の 3 つが分からないまま比較に入らない。足切りと費用がこの 3 つで決まるので、分からなければ先に聞く。聞くときは選択肢で答えられる形にし、1 回に聞く数を絞る。要件が全体に曖昧なら、比較の前にプロダクトの価値から聞き直す (grilling-map-product に当たる手順)。

## 進め方

1. [criteria](references/criteria.md) を読み、「要件から軸の重みを決める」の表で、当てる足切りの条件と重くする軸を決める。
2. 候補を集める。下の「最初の当たり」から要件に合うものを選び、表の「読むとき」に当てはまる reference を開く。自前配信も候補として同じ軸で並べる ([self-hosting](references/self-hosting.md))。要件に特殊な主題や地域が入っていれば [niche](references/niche.md) を見る。
3. 足切りの条件で候補を外す。外した候補と理由を残す。
4. 残った候補を評価の軸で比べる。値は各 reference から写し、reference に「未確認」とあるものは未確認のまま書く。
5. 費用を見積もる。[criteria](references/criteria.md) の「費用の見積もり方」に従い、候補ごとに使い方の経路と課金単位を決め、月間の地図表示回数を揃えて規模ごとに並べる。タイル数で課金される経路だけに、1 回の表示あたりのタイル数の換算を使う。
6. 料金、無料枠、規約の数字は、答える前に公式ページで確かめ直す。reference の確認日 (2026-11-10 など) から変わっていれば新しい値を使い、変わったことを書く。確かめ直せなければ、reference の確認日を添えて出す。
7. 「出力」の形で答える。

## 最初の当たり

候補を集めるときの出発点。どれも足切りと評価の軸で確かめてから推奨する。

- 個人や非商用の試作: OpenFreeMap (無料、キー不要、SLA なし)。tile.openstreetmap.org と tile.openstreetmap.jp は、本番の主たる供給元にしない
- 国内の公的な地図、防災、行政の図面との整合: 地理院タイル (無料、SLA なし)
- 国内で住宅地図レベルの詳しさ: ZENRIN Maps API (料金は見積もり制)
- 商用の汎用ベースマップ: Google Maps Platform、Mapbox、MapTiler Cloud、Esri、HERE、TomTom、Geolonia Maps などを、課金単位と使い方の経路を揃えて比べる
- ArcGIS の資産がある案件: Esri ArcGIS Location Platform
- データ可視化の背景地図: CARTO basemaps
- 表示回数が多い、閉域網、地図の中身を自分で決めたい: 自前配信。閉域網ならオンプレ版のある製品も候補 (MapTiler On-Prem)
- 中国本土、韓国が対象: [regional/china](references/regional/china.md)、[regional/korea](references/regional/korea.md) の手順で、その地域で使えるサービスに絞る
- 衛星・航空写真: `imagery/` の reference。商用か、解析や学習に使うかで使えるものが変わる
- 3D の地形と建物: 国内の都市なら PLATEAU、全球なら Cesium ion か Google Photorealistic 3D Tiles (Google の reference の節)。公共案件では Cesium ion の無料枠を使えない

## 出力

答えは次の順に並べる。

1. 推奨: 1 つ (条件で分かれるなら条件ごとに 1 つ) と、その理由を 2〜3 文。
2. 足切りで外した候補と理由。
3. 比較表: 行に評価の軸、列に残った候補。各セルに値と reference の根拠。
4. 費用表: 行に規模 (月 10 万、100 万、1,000 万回の地図表示)、列に候補。表の下に、候補ごとの使い方の経路、課金単位、計算式、仮定 (1 回の表示あたりのタイル数など) を書く。見積もり制の候補は「要見積もり」と書く。
5. 確かめた日: 料金と規約を公式ページで確かめた日。確かめ直せなかった項目は reference の確認日。
6. 未確認のこと: 結論を左右するのに確かめられなかったこと。国内の地図の詳しさが要件の中心なら、候補ごとに対象地域の画面を実際に見比べるよう勧める。

## 注意

- 料金、無料枠、規約は頻繁に変わる。reference の数字をそのまま最新として出さない。
- 課金単位が違う候補を、単価だけで並べない。月間の地図表示回数に揃えてから比べる。
- 規約の解釈は、条文から読んだものと推測を分けて書く。法的な判断を断定しない。
- 利害関係の開示: このスキル集の作者は Geolonia Maps の提供元に関係している。Geolonia Maps を特別扱いせず、候補に入れたときは開示を答えに添える。
