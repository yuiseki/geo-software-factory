---
name: geo-software-protocol
description: 地図プロダクトで、データをやり取りする方式 (プロトコルと API の標準) を比較し選ぶ。リアルタイムの配信 (WebSocket、Server-Sent Events、MQTT、ポーリング、Webhook) と、地理空間の API の標準 (OGC API Features / Tiles / Maps / Processes / EDR、WMS / WMTS / WFS、STAC API、SensorThings API、NGSI-LD) を、届け方の保証、遅れ、ブラウザとエッジでの対応、途中のプロキシと CDN、地図ライブラリとの組み合わせ、規模と費用、実装のライセンスで比べる。「車両の位置をリアルタイムで地図に出したい」「センサーのデータを地図に」「WMS で配信してほしいと言われた」「OGC API とは」「都市 OS と連携したい」「衛星画像を検索させたい」と言われたら使う。
---

# geo-software-protocol

地図プロダクトのデータのやり取りを、流れ (集める、配る、渡す、受ける) ごとに、どの方式で行うかを決める。リアルタイムの手段と、地理空間の API の標準の 2 種類を扱い、足切り、軸ごとの評価、費用の順に比べて推奨を出す。比較の軸は [criteria](references/criteria.md) にあり、各方式の事実は下の表の reference にある。保存、計算、表現の置き場所は geo-software-arch で先に決め、この結果は geo-software-library (どのライブラリで描くか) の条件になる。

| reference | 読むとき | 中身 |
|---|---|---|
| [criteria](references/criteria.md) | 比較を始める前に、いつも | 比較の軸と、要件から軸の重みを決める方法 |
| [realtime/polling-webhook](references/realtime/polling-webhook.md) | リアルタイムの手段を比べるとき、いつも | ポーリング、条件付きリクエスト、Webhook、GTFS Realtime。ポーリングで足りるかの目安 |
| [realtime/websocket](references/realtime/websocket.md) | 利用者からも送るとき、秒単位で押し出すとき | WebSocket、Cloudflare Durable Objects、API Gateway の上限 |
| [realtime/sse](references/realtime/sse.md) | サーバーから押し出すだけでよいとき | Server-Sent Events、再接続、プロキシの溜め込み |
| [realtime/mqtt](references/realtime/mqtt.md) | 機器やセンサーからのデータを扱うとき | MQTT 5.0、QoS、retained、ブローカーとライセンス |
| [standards/ogc-api](references/standards/ogc-api.md) | OGC の新しい API 標準が求められるとき | OGC API (Features、Tiles、Maps、Processes、EDR) の部品ごとの状態と実装 |
| [standards/ogc-classic](references/standards/ogc-classic.md) | WMS、WMTS、WFS が求められるとき | WMS、WMTS、WFS の版と実装 |
| [standards/stac-api](references/standards/stac-api.md) | 衛星画像などの目録を検索させるとき | STAC と STAC API |
| [standards/sensorthings](references/standards/sensorthings.md) | センサーの観測値を扱うとき | OGC SensorThings API 1.1 と 2.0 |
| [standards/ngsi-ld](references/standards/ngsi-ld.md) | スマートシティの基盤と連携するとき | NGSI-LD、Orion-LD、Scorpio |

## 入力

比較の前に、次の要件をそろえる。プロダクト概要があればそこから読み、無ければ依頼から読み取る。

- やり取りの流れ: 機器からサーバーへ集める、地図の利用者へ配る、他の組織へ渡す、他の組織から受ける、のどれがあるか
- 許される遅れ: 変化してから地図に出るまで何秒まで許されるか (秒以下、数秒、数十秒、分)
- 向き: 利用者からも頻繁に送るか (編集、位置の共有)
- 規模: 同時に見る人数、送り手 (機器、車両) の数と送る頻度
- 相手が決めた標準: 発注者や連携先が API の形 (WMS、OGC API、NGSI など) を指定しているか、相手の道具 (QGIS、ArcGIS、都市 OS)
- 置き場所: geo-software-arch の結果 (静的ホスティングとエッジだけか、常駐のサーバーを置けるか)
- 対象端末: ブラウザ、ネイティブアプリ。画面を閉じている間も届ける必要があるか
- 配布形態: SaaS、受託で納品、パッケージ、OSS

やり取りの流れと許される遅れが分からないまま比較に入らない。足切りがこの 2 つで決まるので、分からなければ先に聞く。聞くときは選択肢で答えられる形にし (例: 「A 秒以下、B 数秒、C 数十秒以上、D それ以外」)、1 回に聞く数を絞る。要件が全体に曖昧なら、比較の前にプロダクトの価値から聞き直す (geo-software-product-grilling に当たる手順)。

## 進め方

1. [criteria](references/criteria.md) を読み、やり取りを流れごとに分け、「要件から軸の重みを決める」の表で足切りの条件と重くする軸と最初の候補を決める。
2. 相手が決めた標準があれば、それを外せない条件として先に置く。相手の版 (WMS 1.1.1 か 1.3.0、NGSIv2 か NGSI-LD、SensorThings 1.1 か 2.0) を確かめる。
3. リアルタイムの手段は、まず [polling-webhook](references/realtime/polling-webhook.md) の「ポーリングで足りるかの目安」を当てる。足りないと説明できるときだけ、SSE、WebSocket、MQTT に進む。
4. 流れごとに `realtime/` と `standards/` の reference を開き、足切りの条件で候補を外す。外した候補と理由を残す。
5. 残った候補を評価の軸で比べる。値は各 reference から写し、「未確認」とあるものは未確認のまま書く。途中の経路 (プロキシ、CDN、企業のネットワーク) が結論を左右するなら、対象の経路で接続を張り続けて切れる時間を測ることを勧める (geo-software-poc-measure)。
6. 費用を見積もる。押し出しは同時接続数、接続時間、メッセージ数から、ポーリングは「表示している時間 / 間隔 x 利用者数」のリクエスト数と CDN のキャッシュの効き方から求める。仮定を書く。
7. 実装を選ぶときは、配布形態ごとにライセンスの条件を各 reference の「ライセンス上の注意」から写す。GPL、LGPL、AGPL、BSL のものは必ず書く。
8. 仕様の版、承認の段階、エッジの上限、料金、ライセンスは、答える前に公式の文書と GitHub の LICENSE で確かめ直す。reference の確認日 (2026-11-11) から変わっていれば新しい値を使い、変わったことを書く。
9. 「出力」の形で答える。決めたことはプロダクト概要の「技術選定の結果」に書き足す。

## 最初の当たり

候補を集めるときの出発点。どれも足切りと評価の軸で確かめてから推奨する。

- 公共交通、水位、気象など、数十秒から分ごとの更新: ポーリング + CDN。GTFS Realtime は取り直す前提のフィード
- 車両や配送の位置を秒単位で全員に見せる: SSE (HTTP/2 以上で配る)。開いた瞬間の最新は最初の全体の取得で描く
- 共同編集、位置の共有、位置情報ゲーム: WebSocket。エッジに置くなら Cloudflare Durable Objects の Hibernation API
- 機器、車載器、センサーから集める: MQTT のブローカー。利用者向けの配信はブローカーの後ろで SSE や WebSocket に変える案も並べる
- センサー網の観測値を標準の形で出す: SensorThings API (FROST-Server)。新しい値の購読は MQTT
- 公共案件で「WMS で」と言われた: WMS 1.3.0 と WMTS を GeoServer、MapServer、QGIS Server で出す。新しく作るなら OGC API - Features と Tiles を並べて出す
- PostGIS の表を標準の API で公開したい: pygeoapi (MIT) か ldproxy (MPL-2.0) の OGC API - Features
- 自治体の都市 OS と連携: 相手の NGSI の版に合わせる。NGSI-LD なら Scorpio (BSD-3-Clause) と Orion-LD (AGPL-3.0)
- 衛星画像や空中写真を範囲と時刻で探させる: STAC の静的カタログ。件数が多ければ stac-fastapi と pgstac
- 他のサービスの変化を受けて地図の成果物を作り直す: Webhook (署名と冪等キー) か、正本の DB の変更通知 (geo-software-arch の source-of-truth)

## 出力

答えは次の順に並べる。

1. 推奨: 流れごとの方式と、その理由を 1〜2 文ずつ。つなぎ目 (例: MQTT で集めて SSE で配る) があれば書く。
2. 足切りで外した候補と理由。
3. 比較表: 流れごとに、行に評価の軸、列に候補。各セルに値と reference の根拠。
4. 届け方の設計: 再接続、取りこぼしの取り直し、重複の除去、心拍の間隔、開いた瞬間に最新を描く方法。
5. 費用表: 規模ごとの月額と、仮定 (同時接続数、メッセージの頻度と大きさ、取り直しの間隔)。
6. 実装とライセンス: 選んだ実装の版とライセンス、配布形態ごとの条件。
7. 次に決めること: geo-software-library への条件 (例: 受け取ったメッセージを GeoJSON に組み直して描く、WMTS を読めるか)、geo-software-auth で決める接続の認証。
8. 確かめた日と、未確認のこと: 結論を左右するのに確かめられなかったこと。経路で切れる時間などを測る手順を添える。

## 注意

- 仕様の版と承認の段階、エッジの上限、料金は変わる。reference の値をそのまま最新として出さない。特に OGC API は部品ごとに承認の段階が違い、SensorThings API 2.0 は 2026-11-04 に公開されたばかりである。
- 「標準に対応」とだけ書かれた製品は、どの部品、どの適合クラスに対応しているかを `/conformance` や Capabilities で確かめる。
- 接続は切れる前提で設計する。どの方式でも、つなぎ直しと取り直しの方法を答えに書く。
- 押し出しの方式は、ポーリングで足りない理由を説明できるときだけ推奨する。
- ブラウザの `WebSocket` と `EventSource` は任意のヘッダーを付けられない。接続の認証は geo-software-auth で決める。
- 規約やライセンスの解釈は、条文から読んだものと推測を分けて書く。法的な判断を断定しない。
