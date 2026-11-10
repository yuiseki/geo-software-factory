---
name: map-compare-protocol
description: 地図プロダクトで、データをやり取りする方式 (プロトコルと API の標準) を比較し選ぶ。リアルタイムの配信 (WebSocket、Server-Sent Events、MQTT、ポーリング、Webhook) と、地理空間の API の標準 (OGC API Features / Tiles / Processes、WMS / WMTS / WFS、STAC API、SensorThings API、NGSI-LD) を、通信の向き、ブラウザとエッジでの対応、地図ライブラリとの組み合わせ、規模と費用で比べる。「車両の位置をリアルタイムで地図に出したい」「センサーのデータを地図に」「WMS で配信してほしいと言われた」「OGC API とは」と言われたら使う。
---

# map-compare-protocol

地図プロダクトのデータのやり取りの方式を選ぶ。

> 骨組みの段階で、手順と reference はまだ書かれていない。このスキルを使うと決めたら、骨組みであることを答えに書き、reference の「[記入]」や空欄を事実として扱わない。判断は、書き上がったスキル (map-compare-arch、map-compare-infra、map-compare-library、map-compare-data、map-legal-check) と公式の文書で確かめられる範囲にとどめる。

後で書く。

| reference | 読むとき | 中身 |
|---|---|---|
| [criteria](references/criteria.md) | 比較を始める前に、いつも | 比較の軸 (後で書く) |
| [realtime/polling-webhook](references/realtime/polling-webhook.md) | リアルタイムの手段を比べるとき | ポーリングと Webhook |
| [realtime/websocket](references/realtime/websocket.md) | リアルタイムの手段を比べるとき | WebSocket |
| [realtime/sse](references/realtime/sse.md) | リアルタイムの手段を比べるとき | Server-Sent Events |
| [realtime/mqtt](references/realtime/mqtt.md) | 機器やセンサーからのデータを扱うとき | MQTT |
| [standards/ogc-api](references/standards/ogc-api.md) | OGC の新しい API 標準が求められるとき | OGC API (Features、Tiles、Maps、Processes) |
| [standards/ogc-classic](references/standards/ogc-classic.md) | WMS や WMTS が求められるとき | WMS、WMTS、WFS |
| [standards/stac-api](references/standards/stac-api.md) | 衛星画像などの目録を検索させるとき | STAC API |
| [standards/sensorthings](references/standards/sensorthings.md) | センサーの観測値を扱うとき | OGC SensorThings API |
| [standards/ngsi-ld](references/standards/ngsi-ld.md) | スマートシティの基盤と連携するとき | NGSI-LD |

後で書く:

- 入力 (要件のうち、このスキルの判断を左右するもの)
- 進め方
- 出力の形
- 注意
