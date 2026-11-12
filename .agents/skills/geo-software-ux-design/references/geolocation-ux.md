# 現在地の取得と表示

対象: 位置情報の許可を求める時機、精度の表示、追従、許可が無いときの代わり

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 確かめた版 | MapLibre GL JS 6.17.0 (`src/ui/control/geolocate_control.ts`)、Leaflet 1.9.4 (`map.locate()`)、W3C Geolocation (2026-11-05 版、geo-software-arch の device から)、Lighthouse の geolocation-on-start の文書 |

## 概要

現在地は、許可を求める時機を誤ると拒まれ、一度拒まれると取り直すのが難しい。取れても誤差があり、誤差の円をどう見せるかで信頼が変わる。現在地に寄せて拡大すると、近くの目的地が画面の外に出ることがある。ブラウザの API の事実 (仕様、対応ブラウザ、セキュアコンテキスト、iframe、WebView) は geo-software-arch の [device](../../geo-software-arch/references/browser/device.md) にあるので、ここでは画面の設計だけを書く。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| ボタンを押したときに許可を求める | 読み込み時の許可の画面で拒まれる | 押されるまで現在地が無い画面を作る | Lighthouse は読み込み時に `getCurrentPosition` か `watchPosition` を呼ぶページを指摘し、「利用者の操作のあとに求める」よう勧める。Chrome 144 からは `<geolocation>` 要素もある (Firefox、Safari は未対応) | https://developer.chrome.com/docs/lighthouse/best-practices/geolocation-on-start 、[device](../../geo-software-arch/references/browser/device.md) |
| 1 回だけ取る / 追従する | 電池と、地図が勝手に動くこと | 追従中に利用者が地図を動かしたら、追従を外す | MapLibre の GeolocateControl は `trackUserLocation` (既定 false) が false ならボタンを押したときに 1 回寄せ、true なら追従の切り替えになり、利用者がカメラを動かすと背景の状態 (点は動くがカメラは動かない) に移る。Leaflet の `map.locate()` は `watch` (既定 false)、`setView` (既定 false) | https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/control/geolocate_control.ts 、https://leafletjs.com/reference-1.9.4.html |
| 誤差の円 | 点がどれほど確かか | 円の意味 (信頼水準) を誤って説明しやすい | MapLibre の `showAccuracyCircle` (既定 true)。説明文は「95% の信頼水準」だが、W3C の仕様の `accuracy` は 68% (1 標準偏差) | 同上、[device](../../geo-software-arch/references/browser/device.md) |
| 現在地と目的地の両方が入る範囲に合わせる | 現在地に寄せると近くの目的地が画面の外に出る | 目的地の数が多いと縮尺が小さくなる | 位置が取れたら、現在地と近い数件 (または全件) の範囲で `fitBounds` する。MapLibre の GeolocateControl の寄せ方は `fitBoundsOptions` (既定 `maxZoom: 15`) | 実測 (下の「実測」)、同上 |
| 取れないときの代わり | 拒否、タイムアウト、精度が粗い | 代わりの入力を用意する手間 | 駅名や住所の検索 ([search-ux](search-ux.md))、地図を動かして中心を現在地とみなす、最後に選んだ地域を端末に覚える | (推測) |
| エラーの知らせ | 何が起きたか分からない | エラーの種類ごとに文言が要る | `GeolocationPositionError.code` は 1 (PERMISSION_DENIED)、2 (POSITION_UNAVAILABLE)、3 (TIMEOUT) | https://developer.mozilla.org/en-US/docs/Web/API/GeolocationPositionError/code |

## 判断を左右すること

- 誰に現在地を求めるか: 自分の記録や「近くを探す」のために使う本人だけにする。公開ページを閲覧するだけの人には求めない (下の「実測」)。
- 1 回で足りるか、追従が要るか: 追従なら電池、画面の点灯 (Screen Wake Lock)、バックグラウンドで取れないこと ([device](../../geo-software-arch/references/browser/device.md))。
- 位置をサーバーに送るか: 送るなら、個人情報か個人関連情報かの扱いが変わる (geo-software-legal-check の [location-privacy](../../geo-software-legal-check/references/location-privacy.md))。端末の中で距離を出すだけにできるなら、送らない設計を先に考える。
- 必要な精度: 「近くの店」なら数百 m で足りる。`enableHighAccuracy` はヒントにすぎず、遅くなり電力を使う ([device](../../geo-software-arch/references/browser/device.md))。

## 手順

1. 現在地が要る機能と、要る人を決める。閲覧するだけの人の画面では、現在地のボタンを出さないか、押したときだけ求める。
2. 許可を求める前に、何に使うかを 1 行で示す (例: 「近い順に並べるために使います。位置は送信しません」)。送らないなら送らないと書く。
3. ボタンを押したら取る。押す前の画面は、地域の既定の範囲か、最後に見た範囲で見せる。
4. 取れたら、目的に合わせて表示範囲を決める。「近くを探す」なら現在地と近い数件が入る範囲、ナビなら現在地中心。
5. 誤差の円を出し、誤差が大きいとき (例: 数 km) は「おおよその位置」と示す (推測)。誤差の円の意味を説明するなら、仕様の 68% に合わせる。
6. 拒否、タイムアウト、取れないときは、エラーの種類ごとに文言を出し、駅名や住所の検索に誘導する。拒否されたあとの取り直しは、ブラウザの設定から許可し直すしかないことを示す (推測)。
7. 一覧の距離と地図の点を同じ位置から出す (MapLibre で使ったときは、同じ `watchPosition` から出すと食い違わなかった、[device](../../geo-software-arch/references/browser/device.md))。

## 実測

- MapLibre の GeolocateControl で現在地に寄せたら、510 m 先の最寄りの目的地が画面の外に出た。現在地と目的地を含む範囲に `fitBounds` すると両方が入った (2026-11-11 実測、上野の銭湯を探す画面)。
- 公開ページの閲覧者に現在地を求めないほうがよい。旅の名所のチェックリスト (本人が使う) では現在地つきの一覧が Must だったが、他人が見る公開ページでは求めないことにした (2026-11-10、[unlock-your-trip](../../../../examples/unlock-your-trip/README.md))。

## 落とし穴

- 読み込み時に許可の画面を出すと、何に使うか分からないまま拒まれる (Lighthouse の指摘の対象)。
- MapLibre の GeolocateControl の既定の `timeout` は 6000 ms (6 秒) で、Leaflet の `map.locate()` は 10000 ms。仕様の既定値 (事実上無限) とは違い、屋内や起動直後の GPS では足りないことがある (推測)。
- MapLibre の GeolocateControl は、位置の可否の判定に Permissions API を使い、iOS 16 では例外になるので `navigator.geolocation` の有無で判定し直している ([device](../../geo-software-arch/references/browser/device.md))。自前で書くときも Permissions API の結果だけで決めない。
- 現在地を中心に表示すると、外部のタイル配信元に、おおよその現在地が伝わる (推測、[location-privacy](../../geo-software-legal-check/references/location-privacy.md))。
- ヘッドレスのブラウザで位置を与えて試すと、GeolocateControl が待ち状態のまま点を出さなかったことがある (2026-11-10、原因は未確認、[device](../../geo-software-arch/references/browser/device.md))。実機でも確かめる。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- ライセンスの論点は無い。MapLibre GL JS (BSD 3-Clause) と Leaflet (BSD-2-Clause) の現在地の機能は本体の一部である。位置の扱いは法令の論点で、geo-software-legal-check の [location-privacy](../../geo-software-legal-check/references/location-privacy.md) で確かめる。

## 出典

- https://github.com/maplibre/maplibre-gl-js/blob/v6.17.0/src/ui/control/geolocate_control.ts (既定値 `enableHighAccuracy: false`、`maximumAge: 0`、`timeout: 6000`、`fitBoundsOptions.maxZoom: 15`、`trackUserLocation: false`、`showAccuracyCircle: true`、`showUserLocation: true`、`zoomToUserAccuracy: true`、背景の状態と誤差の円の説明文。2026-11-11)
- https://leafletjs.com/reference-1.9.4.html (`locate()` の `setView`、`maxZoom`、`watch`、`timeout` 10000、`maximumAge` 0、`enableHighAccuracy` false。2026-11-11)
- https://developer.chrome.com/docs/lighthouse/best-practices/geolocation-on-start (読み込み時の許可要求の指摘と勧め。2026-11-11)
- https://developer.mozilla.org/en-US/docs/Web/API/GeolocationPositionError/code (エラーの種類。2026-11-11)
- geo-software-arch の [device](../../geo-software-arch/references/browser/device.md) (仕様、対応ブラウザ、`accuracy` の信頼水準、`<geolocation>` 要素)

## 未確認のこと

- Lighthouse の現行版にこの指摘 (geolocation-on-start) が残っているか。文書はあるが、リリースの変更履歴は見ていない。
- 拒否したあとに、各ブラウザで許可の画面をもう一度出せるか (iOS の Safari、Android の Chrome)。
- iOS で「正確な位置情報」を切ったときの `accuracy` の値 ([device](../../geo-software-arch/references/browser/device.md) でも未確認)。
