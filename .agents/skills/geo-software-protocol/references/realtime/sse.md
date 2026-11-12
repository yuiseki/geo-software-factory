# Server-Sent Events

対象: Server-Sent Events (`text/event-stream` と、ブラウザの `EventSource`)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 仕様と標準化団体、版 | WHATWG HTML Living Standard の 9.2 節 (Server-sent events)。版番号は無く、随時更新される (https://html.spec.whatwg.org/multipage/server-sent-events.html 、2026-11-11) |

## 概要

普通の HTTP のレスポンスを閉じずに流し続け、サーバーから利用者へイベントを押し出す方式である。ブラウザの `EventSource` が切断時の再接続と、最後に受け取ったイベント ID の送り直しを受け持つ。向きはサーバーから利用者への一方だけで、利用者から送るものは普通の HTTP のリクエストで送る。

## 通信の形

- 向き: サーバーから押し出す (一方向)。
- 何を運ぶか: イベント (車両位置、警報、地物の変更の通知)。中身は UTF-8 のテキストだけで、バイナリは送れない。
- 下にある通信: HTTP/1.1、HTTP/2、HTTP/3 のレスポンス。

## 届け方の保証

- 順序: 1 本のレスポンスの中で順序が保たれる。
- 配送: 確認応答は無い。サーバーが各イベントに `id:` を付けると、ブラウザは再接続のときに `Last-Event-ID` ヘッダーで最後の ID を送るので、サーバーはその後のイベントを送り直せる (仕様 9.2.4)。送り直すには、サーバー側で過去のイベントを持っておく必要がある。
- 再接続: 切れたら自動で再接続する。待ち時間の初期値は実装が決め、仕様は「数秒程度」とする。サーバーは `retry:` でミリ秒を指定できる。HTTP 204 を返すと再接続をやめさせられる。200 以外か `Content-Type` が `text/event-stream` でないと失敗として扱い、再接続しない (仕様 9.2.1〜9.2.3)。

## 対応状況

| 環境 | 対応 | 備考 | 出典 |
|---|---|---|---|
| ブラウザ | 対応 (主要ブラウザの `EventSource`) | HTTP/2 を使わないと、ブラウザとドメインの組ごとに同時接続が 6 本に限られ、タブを 6 つ開くと 7 つ目がつながらない。Chrome と Firefox はこの制限を直さないとしている。HTTP/2 では同時ストリーム数を交渉で決め、既定は 100。`EventSource` のコンストラクタは `withCredentials` しか取らず、任意のヘッダー (Authorization など) を付けられない | https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events (2026-11-11) |
| ネイティブアプリ | ライブラリで対応 | OS の標準 API に `EventSource` 相当は無く、HTTP のストリームを読むライブラリを使う (推測)。バックグラウンドの扱いは WebSocket と同じく、前面にいる間だけ使える前提で設計する ([websocket](websocket.md)) | 未確認 |
| エッジ関数・サーバーレス (接続の維持) | 条件付き | レスポンスを流し続けられる環境なら動く。Cloudflare の元のサーバーとの間の読み取りの待ち時間 (Proxy Read Timeout) は 125 秒で、超えると 524 になる (Enterprise だけ変更可)。Vercel Edge runtime はストリーミングが 300 秒まで ([edge-functions](../../../geo-software-arch/references/edge/edge-functions.md)) | https://developers.cloudflare.com/fundamentals/reference/connection-limits/ (2026-11-11) |
| 地図ライブラリ (MapLibre、OpenLayers、Leaflet、CesiumJS など) | 直接の対応は無い | 受け取ったイベントから GeoJSON を組み直して描く。WebSocket と同じ (推測) | geo-software-library の各 reference |

## 実装

| 実装 (OSS / 管理型サービス) | 版 | ライセンス・料金の単位 | 出典 |
|---|---|---|---|
| 各言語の Web フレームワーク | (各々) | 特別なサーバーは要らない。`text/event-stream` のレスポンスを書き続けるだけで実装できる | 仕様 9.2.5 |
| @microsoft/fetch-event-source (Azure/fetch-event-source) | 未確認 | MIT。`fetch` で SSE を読み、任意のヘッダーや POST を使えるようにするブラウザのライブラリ | `gh api repos/Azure/fetch-event-source/license` (2026-11-11) |
| Centrifugo | v6.10.3 (2026-11-08) | Apache-2.0。SSE と WebSocket の両方で配る | `gh api repos/centrifugal/centrifugo/license` (2026-11-11) |

## 地図プロダクトでの使いどころ

- 車両、船、災害の通報など、サーバーから押し出すだけでよいリアルタイムの地図。利用者からの操作は普通の API で送る。
- 再接続と取りこぼしの取り直しを、ブラウザの標準の仕組み (`Last-Event-ID`) に任せたいとき。
- 既存の HTTP の配信 (CDN、認証の Cookie、ログ) にそのまま載せたいとき。

## 規模と費用

- 1 人 1 本の HTTP のレスポンスを開きっぱなしにするので、配信サーバーは同時接続数に比例してメモリとファイル記述子を使う (推測)。サーバーレスで秒数課金なら、接続している時間そのものが費用になる (推測)。
- Cloudflare Durable Objects の Hibernation のような「待つ間は課金しない」仕組みは WebSocket 向けで、SSE には同じものが無い (推測。確かめた文書は WebSocket だけを扱っていた)。

## 落とし穴

- 途中のプロキシが溜め込む: nginx は既定で `proxy_buffering on` で、レスポンスを溜めてから送る。`X-Accel-Buffering: no` を返すか設定で切る。読み取りの待ち時間 `proxy_read_timeout` は既定 60 秒 (https://nginx.org/en/docs/http/ngx_http_proxy_module.html 、2026-11-11)。圧縮をかけるミドルウェアも溜め込むことがある (推測)。
- 無通信で切られる: 仕様は、古いプロキシが無通信の接続を落とすので、15 秒ほどごとに `:` で始まるコメント行を送ることを勧める (9.2.7)。Cloudflare の 125 秒、nginx の 60 秒より短い間隔で送る。
- HTTP/1.1 のままだと 6 本の制限で、複数のタブやソースを開くと止まる。HTTP/2 以上で配る。
- 認証: `EventSource` はヘッダーを付けられないので、Cookie か URL のトークンを使う。ヘッダーが要るなら fetch で読むライブラリに替える。
- テキストだけなので、座標の多い差分は JSON が大きくなる。まとめて送るか、変わった車両だけを送る (推測)。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- 仕様に従うだけなら、ライセンスの条件は生じない。ここで挙げたライブラリは MIT か Apache-2.0。
- 運ぶデータの継承条件 (ODbL など) は別に効く。

## 出典

- https://html.spec.whatwg.org/multipage/server-sent-events.html : 再接続、`Last-Event-ID`、204 で止める、200 以外で失敗、15 秒ごとのコメント、UTF-8 のみ。
- https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events : 6 本の制限、HTTP/2 の既定 100、`retry`、コメント行、`withCredentials`。
- https://developers.cloudflare.com/fundamentals/reference/connection-limits/ : Proxy Read Timeout 125 秒、524。
- https://nginx.org/en/docs/http/ngx_http_proxy_module.html : `proxy_buffering`、`X-Accel-Buffering`、`proxy_read_timeout`。

## 未確認のこと

- iOS と Android のネイティブアプリで SSE を読む標準的なライブラリと、バックグラウンドでの扱い。
- `EventSource` と bfcache の関係 (web.dev の bfcache の記事は EventSource に触れていない)。
- fetch-event-source の最新版と保守の状況。
- Cloudflare 経由で SSE を流したときに、エッジが応答を溜め込むかどうか (公式の記述を見つけていない)。
