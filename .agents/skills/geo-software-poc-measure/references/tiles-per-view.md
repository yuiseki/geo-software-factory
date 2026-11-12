# 1 回の地図表示あたりのタイル数と転送量の測り方

対象: 開発者ツールのネットワークタブ、HAR、Resource Timing API、Playwright のリクエストのイベント、地図ライブラリのイベントを使って、1 回の表示と典型的な操作で読まれるタイルの数と転送量を測る

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

実測は 2026-11-11 に行った。条件は下の「実測」の節に書く。

## 概要

タイルのリクエスト数で課金される経路では、月額は「月間の地図表示回数 × 1 回の表示あたりのタイル数 × 単価」で決まる ([criteria](../../geo-software-infra/references/criteria.md) の「費用の見積もり方」)。自前配信でも、リクエスト単価と転送単価にこの 2 つの値が掛かる ([self-hosting](../../geo-software-arch/references/self-hosting.md) の「費用の見積もり」)。この文書は、その「1 回の表示あたりのタイル数」と「1 回の表示あたりの転送量」を、仮置きではなく自分の画面で測る手順を書く。数えるのはブラウザがサーバーに届けたリクエストで、ブラウザのキャッシュから返ったものは除く。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| Chrome DevTools のネットワークパネル | 手で地図を開いて操作し、タイルの件数と転送量をその場で見る。フィルタ欄で URL やサイズで絞れる。「Disable cache」で初回の訪問を再現できる | 手作業なので条件をそろえて繰り返しにくい。下の帯の「transferred」はネットワーク上の大きさ、「resources」は展開後の大きさ | Chrome (版を問わない) | https://developer.chrome.com/docs/devtools/network/reference |
| HAR の書き出し | ネットワークパネルの記録を HAR ファイルに書き出し、後で集計する。既定では Cookie、Set-Cookie、Authorization を除いた「sanitized」で書き出す | 手で操作した 1 回分の記録になる | Chrome DevTools、Playwright の `recordHar` | https://developer.chrome.com/docs/devtools/network/reference 、https://playwright.dev/docs/api/class-browser |
| Playwright の `requestfinished` と `request.sizes()` | 同じビューポート、同じ地点、同じ操作を自動で繰り返し、件数と転送量を数える。`responseBodySize` は受け取った本体のエンコード後 (圧縮されたまま) の大きさ | ブラウザのキャッシュから返ったリクエストも `requestfinished` に出る (下の「落とし穴」) | Playwright 1.58.2 で実測 | https://playwright.dev/docs/api/class-request |
| Resource Timing API (`performance.getEntriesByType('resource')`) | ページの中で、読み込んだ資源の一覧と `transferSize` を取る | 別オリジンの資源は `Timing-Allow-Origin` が無いと `transferSize` が 0 になる。MapLibre GL JS のタイルはワーカーが取るので、メインスレッドの一覧に出ない (下の実測) | ブラウザの標準 API | https://developer.mozilla.org/en-US/docs/Web/API/PerformanceResourceTiming/transferSize |
| 地図ライブラリのイベント | 測り終わりの時点を決める。MapLibre GL JS の `idle` は「idle 状態に入る前に描いた最後のフレームの後」に発火し、`areTilesLoaded()` はビューポートのタイルがすべて読み込まれたかを返す。`dataloading` はスタイル、ソース、タイルの読み込みの始まりで発火する | ライブラリごとにイベントの名前と意味が違う | MapLibre GL JS 6.17.0 で実測 | https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapEventType/ 、https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/ |
| 配信側のログ | 本番に近い試験公開で、実際の利用者のタイル数を数える。自前配信なら CDN やストレージのリクエスト数がそのまま課金単位になる | 公開前の PoC では使えない。CDN のキャッシュに当たった分はストレージに届かない | Cloudflare R2、S3、CloudFront など (料金は [self-hosting](../../geo-software-arch/references/self-hosting.md)) | [self-hosting](../../geo-software-arch/references/self-hosting.md) |

## 判断を左右すること

- 課金の経路: 地図の表示回数で課金される経路 (Mapbox GL JS、Google の Maps JavaScript API、MapTiler SDK など) ではタイル数は月額に効かない。タイル数を測るのは、タイルのリクエスト数で課金される経路と自前配信のときだけでよい。経路の一覧は [criteria](../../geo-software-infra/references/criteria.md) の「課金単位と経路を先に決める」にある。
- タイルの大きさ (256 px か 512 px か): 同じ画面でも、512 px のタイルは 256 px のタイルの 4 分の 1 ほどの枚数で覆える。MapTiler は 512 px のラスタを 4 リクエスト、256 px のラスタを 1 リクエストと数える ([maptiler](../../geo-software-infra/references/providers/maptiler.md) の課金単位)。測った供給元とタイルの大きさが違う候補に、枚数をそのまま当てない。
- タイルの最大ズーム: 最大ズームより深く拡大すると、ブラウザは最大ズームのタイルを拡大して使い、新しいタイルをほとんど取らない (下の実測の z16)。最大ズームは供給元ごとに違う (OpenFreeMap の planet は z14、Protomaps の basemap は z15)。
- スタイルのソースの数: 1 つのスタイルが複数のソース (ベクトルタイルと陰影のラスタなど) を持つと、どちらもタイルのリクエストになる。下の実測の z5 では、ベクトルタイル 12 件のほかに陰影のラスタタイルが 28 件読まれた。
- 操作の量: 1 回の表示で終わる画面 (埋め込みの案内図) と、パンとズームを繰り返す画面 (店舗検索、業務の地図) では、1 回の表示あたりのタイル数が数倍違う。要件の「利用者と場面」から、測る操作の筋書きを決める。
- キャッシュ: 同じ利用者が同じ範囲を見直すと、ブラウザの HTTP キャッシュから返り、サーバーに届かない。初回の訪問 (キャッシュなし) で測った値は上限に近い。

## 手順

1. 課金の経路を決める ([criteria](../../geo-software-infra/references/criteria.md))。タイル数で課金されない経路なら、この手順は要らない。
2. 測る条件を決めて書く: ビューポート (例: スマートフォン 390 x 844、ノート PC 1366 x 768、デスクトップ 1920 x 1080)、地点と初期ズーム (利用者がいちばんよく開く場所)、スタイル、操作の筋書き (例: 右に 400 px、下に 300 px パン、1 段ズームイン、左に 400 px パン、2 段ズームアウト)。
3. まず手で 1 回通す。Chrome DevTools のネットワークパネルで「Disable cache」を入れ、フィルタ欄にタイルの URL の一部 (例: `.pbf`、`/tiles/`) を入れて、地図を開き、筋書きどおりに操作し、件数と転送量を読む。HAR を書き出して残す。
4. 自動で繰り返す。Playwright でビューポートごとに新しいブラウザコンテキスト (キャッシュなし) を作り、`page.on('requestfinished')` で URL と `request.sizes().responseBodySize` を集める。地図の `idle` と `areTilesLoaded()` を待ってから次の操作に移る。ヘッドレスの Chromium で WebGL が動くかを先に確かめる ([device-testing](device-testing.md) の「落とし穴」)。
5. タイルの URL の形 (`/{z}/{x}/{y}.pbf` など) でタイルとそれ以外 (スタイル、TileJSON、グリフ、スプライト) を分ける。課金がタイルだけなら、タイル以外は件数から外す (MapTiler は TileJSON、スタイル、フォントを数えない。MapFan のベクター地図 API は style、glyph、sprite を数えない。[maptiler](../../geo-software-infra/references/providers/maptiler.md)、[mapfan-api](../../geo-software-infra/references/providers/mapfan-api.md))。
6. ブラウザのキャッシュから返ったリクエストを除く。Playwright 1.58.2 では、キャッシュから返ったものは `responseBodySize` が負の値 (-998 など) になった (下の実測)。DevTools では Size の列に「(memory cache)」「(disk cache)」と出る。サーバーに届いたものだけを数える。
7. 同じ条件で 2 回以上測り、ばらつきを見る。初回の表示と、操作の筋書きを通した合計を分けて書く。
8. 結果を [criteria](../../geo-software-infra/references/criteria.md) の費用の計算に渡す。「月間の地図表示回数 × 1 回の表示あたりのタイル数」の後者に、初回の表示の値と筋書きを通した値の 2 つを当てて幅で示す。転送量は自前配信の転送単価に当てる。

Playwright で数える部分の骨組みは次のとおり (2026-11-11 に Playwright 1.58.2 で動かしたものを縮めた)。

```js
const recs = [];
page.on('requestfinished', async (req) => {
  const s = await req.sizes();
  recs.push({url: req.url(), bytes: s.responseBodySize});
});
await page.goto(url);
await page.waitForFunction(() => window.__idle && window.map.areTilesLoaded());
const tiles = recs.filter(r => /\/\d+\/\d+\/\d+\.pbf/.test(r.url));
const fromNetwork = tiles.filter(r => r.bytes > 0);
```

## 実測

2026-11-11 に、OpenFreeMap の Liberty スタイル (`https://tiles.openfreemap.org/styles/liberty`、planet `20261101_080013_pt`、ベクトルタイルは z14 まで) を MapLibre GL JS 6.17.0 で描き、Playwright 1.58.2 (Node 23.9.0) から HeadlessChrome 145.0.7632.6 で測った。WebGL は SwiftShader (`--use-angle=swiftshader`)。ケースごとに新しいブラウザコンテキストを作り、キャッシュなしで始めた。中心は東京駅付近 (139.7671, 35.6812)、z5 だけ日本の中央 (137.0, 37.0)。タイル数はサーバーに届いたものだけ、バイト数は `responseBodySize` (gzip のまま) である。OpenFreeMap は公開インスタンスに表示回数やリクエスト数の上限を設けていない ([openfreemap](../../geo-software-infra/references/providers/openfreemap.md))。

| ビューポート | DPR | ズーム | 操作 | タイル (件) | タイルの転送量 (B) | グリフ (件 / B) | スプライト (件 / B) |
|---|---|---|---|---|---|---|---|
| 390 x 844 | 1 | 14 | なし | 6 | 2,918,062 | 5 / 255,854 | 2 / 53,565 |
| 390 x 844 | 3 | 14 | なし | 6 | 2,917,718 | 5 / 255,845 | 2 / 123,173 |
| 1366 x 768 | 1 | 14 | なし | 12 | 4,962,461 | 5 / 255,848 | 2 / 53,558 |
| 1920 x 1080 | 1 | 14 | なし | 12 | 4,962,165 | 5 / 255,921 | 2 / 53,558 |
| 1366 x 768 | 1 | 10 | なし | 6 | 731,390 | 4 / 199,590 | 2 / 53,555 |
| 1366 x 768 | 1 | 16 | なし | 2 (リクエスト 12 件のうち 10 件はキャッシュ) | 856,180 | 5 / 255,834 | 2 / 53,581 |
| 1366 x 768 | 1 | 5 | なし | 12 (ほかに陰影のラスタ 28 件、2,124,606 B) | 1,365,045 | 8 / 435,081 | 2 / 53,552 |
| 1366 x 768 | 1 | 14 | パン 3 回、ズーム 2 回 | 23 (初回 12 + 操作で 11。リクエストは計 35 件で 12 件はキャッシュ) | 6,679,055 (初回 4,962,149 + 操作 1,716,906) | 6 / 281,011 | 2 / 53,569 |

このほか、どのケースでもスタイル JSON 1 件 (gzip で約 6.0 KB、展開して 43,311 B) と TileJSON 1 件 (約 2.2 KB) が読まれた。1366 x 768 の z14 を 3 回測り、タイルの件数は 3 回とも 12 件、転送量の差は 400 B 未満だった。

読み取れること:

- 初回の表示のタイル数は 6〜12 件で、criteria の仮置き (15 タイル) と self-hosting と一部の provider の reference の仮定 (20 タイル) より少なかった。512 px のタイルで z14 が最大ズームのスタイルでの値で、256 px のタイルや最大ズームの深いタイルでは増える (推測)。
- 操作の筋書きを通すと 23 件になり、初回のおよそ 2 倍だった。criteria の「15 タイルとその 2 倍の 30 タイル」の幅は、この条件では上側に寄った見積もりになる。
- DPR (端末の画素密度) を 3 にしてもタイル数は変わらず、スプライトが高解像度版になって大きくなった。
- 1920 x 1080 は 1366 x 768 と同じ 12 件だった。タイルの境目と画面の位置関係で枚数が決まり、画面の面積に比例しない。
- 東京駅付近の z14 のタイルは 1 枚 211,488〜769,950 B (gzip) で、平均は約 413 KB だった。self-hosting の仮定 (平均 50 KB) の 8 倍ほどある。同じ筋書きの z13 のタイルは 63,303〜185,061 B だった。都心の最大ズームのタイルは地物が多く、転送量は地点で大きく変わる。
- 同じ条件で、MapLibre GL JS 本体とワーカーの読み込みは手元のサーバーから非圧縮で計 1,182,820 B (CSS を含む) だった。gzip での大きさは [maplibre-gl-js](../../geo-software-library/references/libraries/maplibre-gl-js.md) にある。

## 落とし穴

- キャッシュから返ったリクエストを数えてしまう: 最大ズームより深いズーム (上の z16) や、見た範囲に戻る操作では、同じ URL のリクエストが何度も出るが、2 回目からはブラウザのキャッシュから返る。Playwright の `requestfinished` は両方を出すので、件数をそのまま数えると 12 件のところを、実際にサーバーに届いたのは 2 件だった。課金されるのはサーバーに届いた分だけと考えられる (推測。各社の文書で「キャッシュから返ったリクエストは数えない」とは確かめていない)。
- Resource Timing にタイルが出ない: MapLibre GL JS 6.17.0 では、メインスレッドの `performance.getEntriesByType('resource')` にスタイル、スプライト、グリフ、TileJSON は出たが、タイルは 1 件も出なかった (2026-11-11 実測)。タイルはワーカーが取っているためと考えられる (推測)。加えて、OpenFreeMap の応答には `Timing-Allow-Origin` が無く、別オリジンの資源の `transferSize` は 0 になる。ページの中で数えるなら、ワーカーの中で測るか、ライブラリのリクエストの差し替え口 (MapLibre の `transformRequest` など) で数える。
- 測り終わりを早まる: `load` イベントは最初の描画の時点で、その後もタイルの読み込みは続く。`idle` と `areTilesLoaded()` を待つ。
- 平均のタイルの大きさを他の地点に当てる: 上のとおり、都心の z14 と z13 で数倍違う。利用者がよく開く地点で測る。
- 単位の違い: 課金の単位は「タイル 1 枚」とは限らない。MapTiler は 512 px のラスタを 4 と数え、Azure Maps と MapFan のベクター地図 API は 15 タイルで 1 と数える ([criteria](../../geo-software-infra/references/criteria.md)、[mapfan-api](../../geo-software-infra/references/providers/mapfan-api.md))。

## ライセンス上の注意

- Playwright は Apache-2.0、MapLibre GL JS は BSD-3-Clause で、測る道具として使う分には義務は生じない。測るために表示したタイルの地図データ (OSM 由来なら ODbL) の帰属表示は、PoC の画面でも消さない。帰属表示の扱いは geo-software-legal-check で確かめる。
- 公開のタイル配信を負荷試験に使わない。同じ範囲を何百回も読むような試験は、自前の配信か、試験を許す契約のある供給元で行う。tile.openstreetmap.org はアクセスをいつでも止めうると明記している ([tile-openstreetmap-org](../../geo-software-infra/references/providers/tile-openstreetmap-org.md))。

## 出典

- https://developer.chrome.com/docs/devtools/network/reference (Disable cache、フィルタ、HAR の sanitized 書き出し、transferred と resources の違い。2026-11-11 確認)
- https://playwright.dev/docs/api/class-request (`request.sizes()` の `responseBodySize` がエンコード後の大きさであること、`request.timing()`。2026-11-11 確認)
- https://playwright.dev/docs/api/class-browser (`recordHar`、`deviceScaleFactor`、`isMobile`。2026-11-11 確認)
- https://developer.mozilla.org/en-US/docs/Web/API/PerformanceResourceTiming/transferSize (`transferSize` はエンコード後の本体 + 300、キャッシュと `Timing-Allow-Origin` 無しで 0。2026-11-11 確認)
- https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapEventType/ (`idle`、`load`、`dataloading` の説明。2026-11-11 確認)
- https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/ (`areTilesLoaded()`。2026-11-11 確認)
- https://tiles.openfreemap.org/styles/liberty (2026-11-11 の実測で使ったスタイル)

## 未確認のこと

- 各社がブラウザのキャッシュから返ったリクエストや、304 で返したリクエストを課金に数えるか。
- 256 px のラスタタイル、z15 以上を持つベクトルタイル、他のライブラリ (Leaflet、OpenLayers) での枚数。上の実測は MapLibre GL JS と 512 px のベクトルタイルだけである。
- 実機 (iOS Safari、Android Chrome) で同じ筋書きを通したときの枚数。画面の大きさが同じなら同じになると考えられる (推測)。
- MapLibre GL JS がタイルをワーカーで取るために Resource Timing に出ない、という説明が正しいか (ワーカーの中の `performance` で確かめていない)。
