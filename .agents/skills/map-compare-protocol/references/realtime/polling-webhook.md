# ポーリングと Webhook

対象: 利用者からの定期的な取り直し (条件付きリクエストを含む)、サーバー間で変化を知らせる Webhook、GTFS Realtime のような取り直す前提のフィード

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 仕様と標準化団体、版 | ポーリングは HTTP そのもの (IETF RFC 9110 の条件付きリクエスト、RFC 9111 のキャッシュ)。Webhook に IETF の標準は無く、業界の取りまとめとして Standard Webhooks 1.0.0 (Apache-2.0) がある (https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md 、2026-11-11)。GTFS Realtime は HTTP GET で取り直すフィード (https://gtfs.org/documentation/realtime/reference/ 、2026-11-11) |

## 概要

ポーリングは、利用者が決まった間隔で同じ URL を取り直す方式で、特別な仕組みが要らず、CDN のキャッシュがそのまま効く。Webhook は、変化が起きたときにサーバーが相手のサーバーの URL へ HTTP の POST を送る方式で、ブラウザやアプリではなくサーバーどうしで使う。どちらも接続を張りっぱなしにしないので、エッジ関数、サーバーレス、静的ホスティングと相性がよい。

## 通信の形

- 向き: ポーリングは利用者が取りに行く。Webhook はサーバーから相手のサーバーへ押し出す。
- 何を運ぶか: ポーリングは地物の一覧や差分、GTFS Realtime の車両位置。Webhook はイベント (地物が変わった、報告が届いた)。
- 下にある通信: HTTP。

## 届け方の保証

- ポーリング: 取り直すたびに最新の全体を受け取るなら、取りこぼしは起きず、遅れが最大で取り直しの間隔になる。差分を取るなら、「この時刻 (や番号) より後」を問い合わせる。GTFS Realtime の `FULL_DATASET` は毎回の全体で前の情報を上書きする形で、`DIFFERENTIAL` は今のところ動作が未定義とされる (https://gtfs.org/documentation/realtime/reference/ 、2026-11-11)。
- 条件付きリクエスト: `ETag` と `If-None-Match`、`Last-Modified` と `If-Modified-Since` で、変わっていなければ 304 を返して本体を送らずに済む (RFC 9110 13 章。https://www.rfc-editor.org/rfc/rfc9110.html#name-conditional-requests)。
- Webhook: Standard Webhooks は、`webhook-id`、`webhook-timestamp`、`webhook-signature` のヘッダーと HMAC-SHA256 の署名 (ID、時刻、本文を `.` でつないで署名)、時刻の許容範囲による再送攻撃の防止、`webhook-id` を冪等キーにした重複の除去、数日にわたる指数的な待ちと揺らぎを入れた再試行 (例では約 75 時間)、15〜30 秒の待ち時間を勧める。順序の保証は扱っていない (Standard Webhooks の仕様、2026-11-11)。

## 対応状況

| 環境 | 対応 | 備考 | 出典 |
|---|---|---|---|
| ブラウザ | 対応 (`fetch` と `setInterval`) | バックグラウンドのタブでは、Chrome はタイマーを 1 秒に 1 回にまとめ、10 秒後からは予算で制限する。WebSocket を持たないタブは予算の制限の対象になる | https://developer.chrome.com/blog/background_tabs (2026-11-11) |
| ネイティブアプリ | 対応 | Android は、バックグラウンドでの変化の取り直しにポーリングでなく FCM の通知を使い、必要なときに WorkManager で取りに行くよう勧める | https://developer.android.com/develop/background-work/background-tasks (2026-11-11) |
| エッジ関数・サーバーレス (接続の維持) | 対応 (接続を保たない) | ポーリングの応答を CDN で短くキャッシュすれば、利用者が何人いても元のサーバーへの問い合わせは間隔ごとに 1 回に近づく (推測。キャッシュの一般的な性質)。Webhook の受け手は関数 1 つで書ける | [edge-functions](../../../map-compare-arch/references/edge/edge-functions.md) |
| 地図ライブラリ (MapLibre、OpenLayers、Leaflet、CesiumJS など) | 対応 (URL の再読み込み) | MapLibre は GeoJSON ソースの `setData` に URL を渡し直せば取り直す。OpenLayers は `VectorSource` の `refresh`。どれもライブラリの基本の API で済む (推測。各ライブラリの API の一般的な使い方) | map-compare-library の各 reference |

## 実装

| 実装 (OSS / 管理型サービス) | 版 | ライセンス・料金の単位 | 出典 |
|---|---|---|---|
| 静的ファイル + CDN | (各社) | オブジェクトストレージや静的ホスティングにファイルを書き直すだけで配れる。課金はリクエストと転送量 | map-compare-arch の [self-hosting](../../../map-compare-arch/references/self-hosting.md) |
| Standard Webhooks の参照ライブラリ | 1.0.0 (仕様) | Apache-2.0 | https://github.com/standard-webhooks/standard-webhooks (2026-11-11) |
| 正本の DB の変更通知 (PostgreSQL の LISTEN/NOTIFY、MongoDB の change streams、Debezium) | (各々) | Webhook や配信の起点にする | map-compare-arch の [source-of-truth](../../../map-compare-arch/references/capabilities/source-of-truth.md) |

## 地図プロダクトでの使いどころ

- 更新が数十秒から数分ごとで足りるもの: 公共交通の車両位置 (GTFS Realtime)、気象、河川の水位、避難所の開設状況。
- 利用者が多く、同じものを全員に見せるもの。CDN のキャッシュが効くので、押し出す方式より安く済むことが多い (推測)。
- ほかのサービスの変化 (決済、フォーム、外部の台帳) を受けて、地図の成果物を作り直すときの Webhook。

## ポーリングで足りるかの目安

- 許される遅れ (変化してから地図に出るまで) が取り直しの間隔より長いなら、ポーリングで足りる。
- 全員が同じものを見るなら、ポーリング + CDN が押し出しより有利になりやすい。利用者ごとに違うもの (自分の配達だけ) を秒単位で見せるなら、押し出しを考える (推測)。
- 利用者からも頻繁に送るなら WebSocket ([websocket](websocket.md))。サーバーから押し出すだけなら SSE ([sse](sse.md))。機器から集める側は MQTT ([mqtt](mqtt.md))。
- 1 人あたりのリクエスト数は「表示している時間 / 間隔」で見積もる。10 秒ごとで 1 時間見るなら 360 回 (計算)。

## 規模と費用

- 費用はリクエスト数と転送量で決まる。304 で本体を省けば転送量が減る。CDN でキャッシュできれば、元のサーバーへのリクエストは利用者の数に比例しない (推測)。
- Webhook は送る側の再試行が数日続きうるので、受け手が止まっている間の再送で一時的に負荷が上がる (Standard Webhooks の再試行の例からの推測)。

## 落とし穴

- 全員が同じ時刻に取り直すと山ができる。間隔に揺らぎを足す (推測)。
- キャッシュの時間を取り直しの間隔より長くすると、取り直しても古いものが返る。`Cache-Control: max-age` を間隔に合わせる。map-ops の運用にも関わる。
- Webhook は届かないことも、2 回届くことも、順番が入れ替わることもある前提で受ける。署名を検証し、`webhook-id` で重複を消し、時刻で古いイベントを捨てる。
- Webhook の受け手の URL は外から叩けるので、署名の検証を省くと誰でも地図を書き換えられる。
- GTFS Realtime はフィードの時刻 (`FeedHeader.timestamp`) を持つ。古いフィードを新しいものとして描かないよう、時刻を見て捨てる (仕様は古さのしきい値を決めていない)。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- 方式そのものにライセンスの条件は無い。Standard Webhooks の仕様とライブラリは Apache-2.0。
- 取り直すフィードの利用条件は配布元ごとに違う (公共交通のオープンデータの規約など)。map-compare-data と map-legal-check で確かめる。

## 出典

- https://www.rfc-editor.org/rfc/rfc9110.html#name-conditional-requests : 条件付きリクエストと 304。
- https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md : ヘッダー、署名、冪等キー、再試行、待ち時間、Apache-2.0、1.0.0。
- https://gtfs.org/documentation/realtime/reference/ : HTTP GET、Protocol Buffers、`FULL_DATASET` と `DIFFERENTIAL`、時刻。
- https://developer.chrome.com/blog/background_tabs : バックグラウンドのタブのタイマー。
- https://developer.android.com/develop/background-work/background-tasks : FCM と WorkManager の勧め。

## 未確認のこと

- 国内の公共交通の GTFS Realtime の更新間隔の実例 (配布元ごとに違う)。
- iOS のバックグラウンドでの取り直しの制約 (Apple の文書を読めていない)。
- 主要な Webhook の送り手 (GitHub、Stripe など) が Standard Webhooks にどこまで従っているか。
