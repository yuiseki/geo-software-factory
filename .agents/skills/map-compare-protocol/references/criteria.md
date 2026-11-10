# 比較の軸 (データのやり取りの方式)

地図プロダクトで、データを「どう届けるか」(リアルタイムの手段) と「どの API の形で出すか」(地理空間の API の標準) を同じ軸で並べるための手順。比較を始める前に読む。各方式の事実は `realtime/` と `standards/` にあり、この文書には軸と判定の手順だけを書く。例として挙げる事実は、各 reference に 2026-11-11 時点で書かれていたもの。

## 進め方

1. やり取りを、流れごとに分ける。例: 機器からサーバーへ (集める)、サーバーから地図の利用者へ (配る)、サーバーから他の組織へ (渡す)、他の組織からサーバーへ (受ける)。方式は流れごとに選ぶ。
2. 流れごとに、足切りの条件で候補を外す。
3. 残った候補を、評価の軸で比べる。軸の重みは「要件から軸の重みを決める」の表で決める。
4. 推奨を先に書き、続けて流れごとの方式と、つなぎ目 (例: MQTT で集めて SSE で配る) を示す。確かめられなかった項目は「未確認」のまま残す。

## 足切りの条件

| 条件 | 何を確かめるか | 外れる例 (各 reference の記述) |
|---|---|---|
| 相手が決めた標準 | 発注者や連携先が API の形を指定しているか | 「WMS で出してほしい」なら WMS を外せない ([ogc-classic](standards/ogc-classic.md))。相手の基盤が NGSIv2 なら NGSI-LD では通じない ([ngsi-ld](standards/ngsi-ld.md)) |
| 許される遅れ | 変化してから地図に出るまで、何秒まで許されるか | 数十秒以上で足りるなら、押し出しの方式は要らない ([polling-webhook](realtime/polling-webhook.md)) |
| 向き | 利用者からも頻繁に送るか | 利用者から送るものが多いなら、一方向の SSE だけでは足りない ([sse](realtime/sse.md)) |
| 置き場所 | 接続を保てる場所があるか | 静的ホスティングとサーバーレスだけなら、ブローカーや常駐の配信サーバーを置けない。Durable Objects のような接続を持てる場所を使うか、ポーリングにする ([websocket](realtime/websocket.md)、map-compare-arch の [edge-functions](../../map-compare-arch/references/edge/edge-functions.md)) |
| 対象端末とバックグラウンド | 画面を閉じている間も届ける必要があるか | アプリが裏に回ると接続は保てない前提にする。通知は FCM や APNs (Android は FCM を勧める、[websocket](realtime/websocket.md)) |
| ライセンス | 配布形態 (SaaS、受託納品、パッケージ) で実装を使えるか | EMQX 5.9.0 以降は BSL 1.1 で、第三者へのホスト型や組み込み型の提供を許諾から外す ([mqtt](realtime/mqtt.md))。Orion-LD は AGPL-3.0 ([ngsi-ld](standards/ngsi-ld.md))。GeoServer は GPL ([ogc-api](standards/ogc-api.md)) |
| 標準の承認の段階 | 使う部品が承認済みか | OGC API - Features の書き込み (Part 4) と Processes の Part 2 以降は草案 ([ogc-api](standards/ogc-api.md)) |

## 評価の軸

### 1. 届け方の保証

- 順序、取りこぼし、重複の扱い。WebSocket は再接続も取り直しも自分で作る。SSE は `Last-Event-ID` で取り直せる。MQTT は QoS とセッションと retained を持つ。Webhook は重複と順序の入れ替わりを前提に受ける (各 `realtime/`)。
- 地図では「最新の位置だけが要る」ことが多く、取りこぼしても次の値で上書きできる。そのときは保証の強さより、開いた瞬間に最新を描けるか (retained、最初の全体の取得) を重く見る (推測)。

### 2. 遅れと更新の頻度

- 押し出し (WebSocket、SSE、MQTT) は秒以下、ポーリングは間隔の分だけ遅れる。

### 3. 規模と費用

- 押し出しは同時接続数と接続時間とメッセージ数で、ポーリングはリクエスト数と転送量で決まる。全員が同じものを見るならポーリング + CDN が安くなりやすい (推測。[polling-webhook](realtime/polling-webhook.md))。
- エッジの課金の例: Durable Objects は受け取るメッセージを 20 件で 1 リクエストと数え、送るメッセージは課金しない ([websocket](realtime/websocket.md))。AWS IoT Core は接続時間と 5 KB 単位のメッセージ数 ([mqtt](realtime/mqtt.md))。

### 4. 途中の経路 (プロキシ、CDN、企業のネットワーク)

- 無通信の切断: Cloudflare は元のサーバーからの読み取りを 125 秒で打ち切る。nginx の `proxy_read_timeout` は既定 60 秒。SSE の仕様は 15 秒ほどごとのコメントを勧める ([sse](realtime/sse.md))。
- 溜め込み: nginx は既定で応答を溜める ([sse](realtime/sse.md))。
- 再起動での切断: Cloudflare はコードを出すときに WebSocket を切ることがある ([websocket](realtime/websocket.md))。

### 5. 地図ライブラリと相手の道具がそのまま読めるか

- WMS と WMTS は主要なライブラリと GIS が読む ([ogc-classic](standards/ogc-classic.md))。OGC API - Tiles と Maps は OpenLayers に専用のソースがある ([ogc-api](standards/ogc-api.md))。リアルタイムの手段はどのライブラリにも専用のソースが無く、受け取って GeoJSON を組み直す。
- 発注者や連携先が QGIS や ArcGIS で読むなら、相手の道具が読める標準を重く見る。

### 6. 標準としての成熟と公共での採用

- 承認の段階と版 (各 `standards/` のメタ情報)。国内の公共での例: J-SHIS の WMS 1.3.0 ([ogc-classic](standards/ogc-classic.md))、JAXA Earth の STAC 静的カタログ ([stac-api](standards/stac-api.md))。国内の公的機関の OGC API の公開例は見つけていない。

### 7. 実装のライセンスと運用の負担

- コピーレフトと OSI 非承認のもの (GPL、LGPL、AGPL、BSL) は、配布形態ごとの条件を各 reference の「ライセンス上の注意」から写す。
- 常駐させるもの (ブローカー、配信サーバー、OGC API のサーバー) の数だけ運用が増える。

## 要件から軸の重みを決める

| 要件 | 足切りに当てる条件 | 重くする軸 | 最初の候補 |
|---|---|---|---|
| 車両、船、機器の位置を秒単位で全員に見せる | 許される遅れ、置き場所 | 規模と費用、途中の経路 | SSE か WebSocket。機器から集める側は MQTT |
| 数十秒から数分ごとの更新で足りる (公共交通、水位、気象) | 許される遅れ | 規模と費用 | ポーリング + CDN |
| 共同編集、位置の共有、位置情報ゲーム | 向き | 届け方の保証 | WebSocket |
| センサー網の観測値を集めて出す | 相手が決めた標準 | 届け方の保証、標準としての成熟 | MQTT、SensorThings API |
| 公共案件、既存の GIS との連携 | 相手が決めた標準、ライセンス | 相手の道具がそのまま読めるか | WMS、WMTS、WFS。新しく作るなら OGC API - Features と Tiles を並べる |
| 自治体の都市 OS と連携する | 相手が決めた標準 | 標準としての成熟 | 相手の版の NGSI (NGSIv2 か NGSI-LD) |
| 衛星画像や空中写真を範囲と時刻で探させる | なし | 相手の道具がそのまま読めるか | STAC (静的カタログ、件数が多ければ STAC API) |
| 他のサービスの変化を受けて作り直す | なし | 届け方の保証 | Webhook (署名と冪等キー) |

## この文書で扱っていない方式

- WebTransport、WebRTC のデータチャネル: map-compare-arch の [network](../../map-compare-arch/references/browser/network.md) に WebTransport の記述がある。地図での採用例は未確認。
- GraphQL の Subscription、gRPC のストリーム: reference で調べていない。
- 正本の DB からの変更の取り出し (LISTEN/NOTIFY、change streams、CDC): map-compare-arch の [source-of-truth](../../map-compare-arch/references/capabilities/source-of-truth.md)。
- OGC API - Records、Coverages、Connected Systems、Moving Features: [ogc-api](standards/ogc-api.md) に承認の状態だけを書いた。
