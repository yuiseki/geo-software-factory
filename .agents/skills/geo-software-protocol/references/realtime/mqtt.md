# MQTT

対象: MQTT 5.0 と 3.1.1、ブラウザからの MQTT over WebSocket、主なブローカー (Mosquitto、EMQX、HiveMQ CE、AWS IoT Core)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 仕様と標準化団体、版 | OASIS MQTT Version 5.0 (OASIS Standard、2019-03-07)。3.1.1 も広く使われる (3.1.1 が ISO/IEC 20922 になったことは未確認)。WebSocket の上で動かす方法は 5.0 の 6 章 (https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html 、2026-11-11) |

## 概要

ブローカーを真ん中に置き、機器や利用者がトピック (`vehicles/123/position` など) に発行 (publish) し、別の誰かがトピックの絞り込み (`vehicles/+/position`) で購読する方式である。電池と回線の細い機器向けに作られ、配送の保証の段階 (QoS)、切れたあとも購読を保つセッション、最後の値を残す retained メッセージを仕様に持つ。ブラウザは TCP を直接張れないので、WebSocket の上の MQTT でつなぐ。

## 通信の形

- 向き: 双方向 (ブローカーを通した発行と購読)。
- 何を運ぶか: センサーの観測値、車両や機器の位置、コマンド。中身の形式は仕様が決めない (JSON、CBOR、Protocol Buffers など)。
- 下にある通信: TCP (多くは TLS 付き)。ブラウザからは WebSocket で、副プロトコル名は `mqtt` (仕様 6 章、[MQTT-6.0.0-3]、[MQTT-6.0.0-4])。

## 届け方の保証

- 配送: QoS 0 は最大 1 回、1 は最低 1 回、2 はちょうど 1 回 (geo-software-arch の [source-of-truth](../../../geo-software-arch/references/capabilities/source-of-truth.md) にも同じ記述)。
- 順序: 同じ送り手から同じ QoS で同じトピックに送られたものは、共有でない購読では順序どおりに届く (Ordered Topic、仕様 4.6 節)。送り手やトピックをまたぐ順序は保証されない。
- 再接続と取りこぼし: 5.0 ではセッションの有効期間 (Session Expiry Interval) を指定すると、切断後もブローカーが購読と未配送のメッセージ (QoS 1、2) を持つ。`0xFFFFFFFF` なら期限が無い (仕様 3.1.2.11.2)。メッセージに期限 (Message Expiry Interval) を付けると、期限までに配れなかったものは捨てられる (3.3.2.3.3)。
- 最新の値: retained メッセージを付けて発行すると、ブローカーはトピックごとに最後の 1 件を持ち、新しく購読した相手にすぐ送る。空のペイロードで消せる (3.3.1.3)。地図を開いた瞬間に各車両の最後の位置を描ける。
- 死活: Keep Alive の 1.5 倍の間に何も届かなければ、ブローカーは接続を閉じる (3.1.2.10)。

## 対応状況

| 環境 | 対応 | 備考 | 出典 |
|---|---|---|---|
| ブラウザ | WebSocket 経由で対応 | MQTT.js (v5.16.1、MIT) などがブラウザで WebSocket の上の MQTT を話す。ブローカー側で WebSocket の待ち受けを有効にする | `gh api repos/mqttjs/MQTT.js/license` 、 https://github.com/mqttjs/MQTT.js/releases (2026-11-11) |
| ネイティブアプリ | ライブラリで対応 | Eclipse Paho など (EPL-2.0 と EDL-1.0 の二重ライセンス)。バックグラウンドでは接続が保てない前提で設計し、通知は FCM や APNs に任せる (推測。[websocket](websocket.md) の Android の記述と同じ理由) | `gh api repos/eclipse-paho/paho.mqtt.python/license` (2026-11-11) |
| エッジ関数・サーバーレス (接続の維持) | ブローカーは置けない | ブローカーは常駐のサーバーか管理型サービスに置く (推測)。エッジやサーバーレスは、ブローカーから規則 (AWS IoT Core のルールなど) や Webhook で呼ばれる側にする | 推測 |
| 地図ライブラリ (MapLibre、OpenLayers、Leaflet、CesiumJS など) | 直接の対応は無い | 受け取ったメッセージから GeoJSON を組み直して描く (推測) | geo-software-library の各 reference |

## 実装

| 実装 (OSS / 管理型サービス) | 版 | ライセンス・料金の単位 | 出典 |
|---|---|---|---|
| Eclipse Mosquitto | v2.1.2 (タグ、2026-02-09) | EPL-2.0 OR BSD-3-Clause (EDL-1.0) | `gh api repos/eclipse-mosquitto/mosquitto/license` (2026-11-11) |
| EMQX | 6.3.2 (2026-10-16) | 5.9.0 以降は Business Source License 1.1 で OSI 非承認。追加の利用許諾は「単一ノードの本番利用。ただし第三者にホスト型や組み込み型で提供しない場合に限る」と、教育機関と非営利団体の営利でない本番利用。各版は公開から 4 年で Apache-2.0 に変わる | `gh api repos/emqx/emqx/license` (2026-11-11) |
| HiveMQ Community Edition | 2026.5 (2026-05-27) | Apache-2.0 | `gh api repos/hivemq/hivemq-community-edition/license` (2026-11-11) |
| NanoMQ | 未確認 | MIT | `gh api repos/nanomq/nanomq/license` (2026-11-11) |
| VerneMQ | 未確認 | Apache-2.0 | `gh api repos/vernemq/vernemq/license` (2026-11-11) |
| AWS IoT Core | (サービス) | 接続時間 (us-east-1 で 100 万分あたり 0.08 ドル) とメッセージ数 (5 KB 単位で数える。8 KB は 2 件)。ルールとアクションも 5 KB 単位。無料枠は AWS アカウント作成から 12 か月、月 225 万接続分と 50 万メッセージ | https://aws.amazon.com/iot-core/pricing/ (2026-11-11) |

## 地図プロダクトでの使いどころ

- 機器やセンサー、車載器から位置や観測値を集める側。機器が MQTT を話すなら、そのまま受ける。
- 車両の最後の位置を retained で持たせ、地図を開いた利用者にすぐ描かせる。
- SensorThings API は MQTT での購読を仕様に持つ ([sensorthings](../standards/sensorthings.md))。NGSI-LD は購読の通知を MQTT で送る binding を持つ ([ngsi-ld](../standards/ngsi-ld.md))。
- ブラウザまで MQTT で届けるか、ブローカーの後ろで SSE や WebSocket に変えて配るかは選べる。利用者が多いなら、利用者向けは別の配信にして、ブローカーを機器だけに開く設計がある (推測)。

## 規模と費用

- 管理型サービスは接続している時間とメッセージ数で課金されることが多い (AWS IoT Core の例は上の表)。メッセージは 5 KB 単位なので、小さな位置を 1 件ずつ送るのと、まとめて送るので件数が変わる。
- 1 台の車両が 1 秒に 1 回送ると、1 か月で約 260 万メッセージになる (計算: 60 x 60 x 24 x 30)。

## 落とし穴

- トピックの設計で権限が決まる。利用者ごとに購読してよいトピックを絞る仕組み (ACL) はブローカーごとに違い、仕様は決めない (推測)。ブラウザに MQTT を開くと、絞り込みの誤りでほかの人の位置が漏れる。
- QoS 2 でも、アプリが受け取って処理し終えたことまでは保証しない。DB に書くなら、メッセージの ID で重複を消す (推測)。
- 共有の購読 (Shared Subscription) では、同じトピックのメッセージが複数の受け手に分かれ、順序の保証が外れる (仕様 4.6 節は Ordered Topic を共有でない購読に限る)。
- retained メッセージは消すまで残る。車両が引退したら空のペイロードで消さないと、地図に幽霊が残る。
- 有効期間の長いセッションは、つなぎに来ない機器の分までブローカーがメッセージを溜める。Message Expiry Interval を付ける。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- EMQX (5.9.0 以降、BSL 1.1、OSI 非承認): 条文では、単一ノードの本番利用は、第三者にホスト型や組み込み型で提供しない場合に限って許される。「ホスト型や組み込み型」は「サービスとして提供するか、第三者に提供する製品やソリューションに組み込む」と定義される。自社の SaaS の裏で動かす場合、受託で納品するシステムに入れる場合、複数ノードで動かす場合は、この許諾に当たらない可能性が高く、商用ライセンスが要りうる (推測)。各版は公開から 4 年で Apache-2.0 になる。古い 5.8 以前の扱いは未確認。
- Mosquitto と Paho (EPL-2.0、選択で BSD-3-Clause): BSD-3-Clause を選べば、組み込み、改変、配布、SaaS 提供のどれも著作権表示の保持で足りる。EPL-2.0 を選んで改変したものを配布するなら、改変したファイルのソースを EPL-2.0 で提供する (EPL-2.0 の条文の要約。SaaS 提供だけなら配布に当たらない、推測)。
- HiveMQ CE、VerneMQ、NanoMQ、MQTT.js は Apache-2.0 か MIT。

## 出典

- https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html : QoS、順序 (4.6)、retained (3.3.1.3)、セッションの有効期間 (3.1.2.11.2)、Keep Alive (3.1.2.10)、メッセージの期限 (3.3.2.3.3)、WebSocket (6 章)。
- `gh api repos/<owner>/<repo>/license` (eclipse-mosquitto/mosquitto、emqx/emqx、hivemq/hivemq-community-edition、nanomq/nanomq、vernemq/vernemq、mqttjs/MQTT.js、eclipse-paho/paho.mqtt.python) : ライセンス。EMQX は LICENSE の本文 (BSL 1.1 の Parameters)。
- 各リポジトリの releases とタグ : 版。
- https://aws.amazon.com/iot-core/pricing/ : AWS IoT Core の課金単位と無料枠。

## 未確認のこと

- 3.1.1 と ISO/IEC 20922 の関係。
- AWS IoT Core の us-east-1 のメッセージ単価 (料金ページの例はアイルランドで 100 万メッセージあたり 1 ドル)。
- HiveMQ Cloud、EMQX Cloud など管理型サービスの料金。
- EMQX 5.8 以前の版のライセンスと、BSL のもとでの SaaS の裏での利用の正式な解釈。
- 国内の公共で MQTT を公開の配信に使っている例。
