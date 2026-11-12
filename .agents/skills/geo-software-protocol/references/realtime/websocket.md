# WebSocket

対象: WebSocket (RFC 6455、ブラウザの `WebSocket` API)、HTTP/2 と HTTP/3 の上の WebSocket、エッジと管理型サービスでの WebSocket の上限

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 仕様と標準化団体、版 | プロトコルは IETF の RFC 6455 (2011-12)。HTTP/2 の上で動かす方法は RFC 8441 (2018-09、拡張 CONNECT と `:protocol` 疑似ヘッダー)。ブラウザの API は WHATWG の WebSockets Standard。ストリームで読み書きする `WebSocketStream` は標準になっておらず、MDN は Experimental かつ Non-standard としている (https://developer.mozilla.org/en-US/docs/Web/API/WebSocketStream 、2026-11-11) |

## 概要

1 本の TCP (または HTTP/2 のストリーム) の上で、サーバーと利用者の両方からいつでもメッセージを送れる双方向の通信である。HTTP の Upgrade で始まり、その後は HTTP のリクエストとレスポンスの形をとらない。1 本の接続の中では順序が保たれるが、切れたあとの再接続、取りこぼしの再送、購読の再開は仕様に無く、アプリかライブラリ (Socket.IO など) が持つ。

## 通信の形

- 向き: 双方向。
- 何を運ぶか: イベント (車両やユーザーの位置、地物の追加や変更の通知)。地物そのものを JSON や Protocol Buffers で送ることもある。タイルを WebSocket で送る使い方は一般的でない (推測)。
- 下にある通信: TCP の上の HTTP/1.1 Upgrade (RFC 6455)。HTTP/2 では拡張 CONNECT (RFC 8441)。

## 届け方の保証

- 順序: 1 本の接続の中では TCP の順序が保たれる。接続をまたぐ順序は保証されない。
- 配送: 送ったメッセージが相手のアプリに届いたかの確認は無い。切断の間に送られたものは失われるので、再接続のときに「最後に受け取った番号」を送って差分を取り直す仕組みを自分で作る (推測。一般的な設計)。
- 再接続: ブラウザの `WebSocket` は自動で再接続しない。SSE の `EventSource` との大きな違いである ([sse](sse.md))。
- 背圧: 標準の `WebSocket` には背圧の仕組みが無く、`bufferedAmount` を見るだけである。`WebSocketStream` は Streams の背圧を使えるが、標準化されていない (MDN、上記)。

## 対応状況

| 環境 | 対応 | 備考 | 出典 |
|---|---|---|---|
| ブラウザ | 対応 (主要ブラウザ) | バックグラウンドのタブでは、Chrome は WebSocket を持つタブを予算によるタイマー制限から外す (タイマーの 1 秒 1 回の制限は残る)。bfcache は、Chrome (149 以降) と Safari では開いた WebSocket があっても妨げられないが、他のブラウザでは妨げられる。web.dev は `pagehide` で接続を閉じ、`pageshow` でつなぎ直すことを勧める | https://developer.chrome.com/blog/background_tabs 、 https://web.dev/articles/bfcache (2026-11-11) |
| ネイティブアプリ | 対応 (OS の標準 API とライブラリ) | 前面にいる間だけ使える前提で設計する。Android は、バックグラウンドでは非同期の作業が止まりうるとし、変化の通知にはポーリングでなく FCM を使うよう勧める。iOS のバックグラウンドでの接続の扱いは Apple の文書を読めておらず未確認 | https://developer.android.com/develop/background-work/background-tasks (2026-11-11) |
| エッジ関数・サーバーレス (接続の維持) | 条件付き | Cloudflare Workers は受け取るメッセージを 1 件 32 MiB までとし、ランタイムの更新の猶予が尽きると接続を切る。複数の接続をまとめる用途 (部屋、地図の共有画面) には Durable Objects を勧める。Durable Objects は Hibernation API (`ctx.acceptWebSocket`) を使うと、待っている間の Duration 課金がかからず、コードの更新でも接続が保たれうる。AWS API Gateway の WebSocket API は 1 接続 2 時間まで、無通信 10 分で切断、フレーム 32 KB、メッセージ 128 KB | https://developers.cloudflare.com/workers/runtime-apis/websockets/ 、 https://developers.cloudflare.com/durable-objects/best-practices/websockets/ 、 https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-execution-service-websocket-limits-table.html (2026-11-11) |
| 地図ライブラリ (MapLibre、OpenLayers、Leaflet、CesiumJS など) | 直接の対応は無い | どのライブラリもソースの型として WebSocket を持たない。受け取ったメッセージから GeoJSON を組み直して `setData` (MapLibre) や `VectorSource` への追加 (OpenLayers) で描く (推測。各ライブラリの API の一般的な使い方) | geo-software-library の各 reference |

## 実装

| 実装 (OSS / 管理型サービス) | 版 | ライセンス・料金の単位 | 出典 |
|---|---|---|---|
| ws (Node.js) | 未確認 | MIT | `gh api repos/websockets/ws/license` (2026-11-11) |
| Socket.IO | 4.8.4 (2026-09-25) | MIT。再接続、部屋、確認応答 (ack) を持つ独自のプロトコルで、素の WebSocket の相手とは通じない | `gh api repos/socketio/socket.io/license` 、 https://github.com/socketio/socket.io/releases (2026-11-11) |
| Centrifugo | v6.10.3 (2026-11-08) | Apache-2.0。WebSocket、SSE などをまとめる配信サーバー | `gh api repos/centrifugal/centrifugo/license` (2026-11-11) |
| Cloudflare Durable Objects | (サービス) | 接続を張るのに 1 リクエスト。受け取るメッセージは 20 件で 1 リクエストとして数え、送るメッセージとプロトコルの ping は課金しない。Paid は月 100 万リクエストを含み、超過は 100 万あたり 0.15 ドル。Duration は月 40 万 GB 秒を含み、超過は 100 万 GB 秒あたり 12.50 ドル。Free は 1 日 10 万リクエストと 1 万 3,000 GB 秒 | https://developers.cloudflare.com/durable-objects/platform/pricing/ (2026-11-11) |
| AWS API Gateway WebSocket API | (サービス) | 接続の時間とメッセージ数で課金 (単価は未確認)。新しい接続は既定で毎秒 500 (地域ごと、引き上げ可) | https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-execution-service-websocket-limits-table.html (2026-11-11) |

## 地図プロダクトでの使いどころ

- 利用者からも頻繁に送る双方向の地図: 共同編集のカーソル、位置の共有、位置情報ゲーム。
- 1 秒に何回も変わる位置 (配車、配送の車両) を、多くの利用者に同時に押し出すとき。利用者から送るものが無ければ SSE で足りることが多い ([sse](sse.md))。
- MQTT のブローカーをブラウザから直接使うとき (MQTT over WebSocket、[mqtt](mqtt.md))。

## 規模と費用

- 同時接続数は、エッジでは「接続を張った回数」と「受け取るメッセージ数」で課金されることが多い。Cloudflare は接続を張るリクエストだけを HTTP のリクエストとして数え、帯域は Cloudflare から利用者へ送った分で数える (https://developers.cloudflare.com/network/websockets/ 、2026-11-11)。
- Durable Objects の公式の手引きは、小さなメッセージを 50〜100 ms ごとか 50〜100 件ごとにまとめて送ることを勧める (https://developers.cloudflare.com/durable-objects/best-practices/websockets/ 、2026-11-11)。地図の車両位置なら、1 秒ごとに全車両の差分を 1 通にまとめる設計が合う (推測)。
- Durable Object 1 つで何本の接続を持てるかは、公式の文書が「数千」としか書いておらず、正確な上限は未確認。

## 落とし穴

- 切れることを前提にする。Cloudflare は、ネットワークに新しいコードを出すときにサーバーを再起動し、WebSocket を切ることがあると書いている。無通信の接続も一定時間で閉じる (時間は非公開、Enterprise は相談で変更可) ので、ping と pong の心拍を送る (https://developers.cloudflare.com/network/websockets/ 、2026-11-11)。
- 再接続の嵐: 配信側の再起動で全員が同時につなぎ直す。指数的な待ちと揺らぎ (jitter) を入れる (推測。一般的な設計)。
- ロードバランサーの後ろに複数の配信サーバーを置くなら、同じ相手に戻すセッションアフィニティか、サーバー間でメッセージを配る仕組み (Redis の Pub/Sub、MQTT のブローカー、Durable Objects) が要る。Cloudflare の文書も、負荷分散する元のサーバーにはセッションアフィニティを勧める (同上)。
- 自前の nginx などの逆プロキシは、Upgrade を通す設定と、読み取りの待ち時間 (`proxy_read_timeout` は既定 60 秒) の延長が要る (https://nginx.org/en/docs/http/ngx_http_proxy_module.html 、2026-11-11)。
- Durable Objects の Hibernation API でも、アラーム、`setTimeout`、外へ張った WebSocket があると眠れず、Duration の課金が続く (https://developers.cloudflare.com/durable-objects/best-practices/websockets/ 、2026-11-11)。
- 認証: ブラウザの `WebSocket` は任意のヘッダーを付けられないので、Cookie、URL の短命なトークン、接続直後の最初のメッセージのどれかで認証する (推測。API の形からの判断)。トークンを URL に載せるとアクセスログに残る。認証の方式は geo-software-auth で決める。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- ここで挙げた実装 (ws、Socket.IO、Centrifugo) は MIT か Apache-2.0 で、組み込み、改変、配布、SaaS 提供のどれでも、著作権表示とライセンス文の保持 (Apache-2.0 は NOTICE と変更の表示も) で足りる。
- 運ぶデータの継承条件は別に効く。OSM 由来の地物を配信するなら ODbL の条件がかかる (geo-software-data の license-mixing)。

## 出典

- https://www.rfc-editor.org/rfc/rfc8441.html : HTTP/2 の上の WebSocket (2018-09)。
- https://developer.mozilla.org/en-US/docs/Web/API/WebSocketStream : Experimental、Non-standard、背圧。
- https://developer.chrome.com/blog/background_tabs : バックグラウンドのタブのタイマー制限と WebSocket の扱い。
- https://web.dev/articles/bfcache : bfcache と開いた WebSocket。
- https://developers.cloudflare.com/network/websockets/ : 全プランで対応、無通信での切断、再起動での切断、課金の数え方、セッションアフィニティ。
- https://developers.cloudflare.com/workers/runtime-apis/websockets/ : 32 MiB、ランタイム更新での切断、Durable Objects の推奨。
- https://developers.cloudflare.com/durable-objects/best-practices/websockets/ : Hibernation API、課金、自動の pong、メッセージをまとめる勧め。
- https://developers.cloudflare.com/durable-objects/platform/pricing/ : メッセージの 20:1 の数え方と単価。
- https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-execution-service-websocket-limits-table.html : API Gateway の上限。
- https://developer.android.com/develop/background-work/background-tasks : Android のバックグラウンドと FCM の勧め。
- https://nginx.org/en/docs/http/ngx_http_proxy_module.html : `proxy_read_timeout` の既定。

## 未確認のこと

- iOS アプリがバックグラウンドに回ったときの WebSocket の扱いを、Apple の文書で確かめていない。
- Cloudflare の無通信での切断までの秒数 (公式は数値を出していない)。
- Durable Object 1 つあたりの接続数の上限。
- AWS API Gateway WebSocket API の接続時間とメッセージの単価。
- `WebSocketStream` のブラウザごとの対応版。
- ws の最新版。
