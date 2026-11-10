# 地図の提供元の障害時の切り替え

対象: 提供元の稼働状況の見方、別の提供元や自前のタイルへの切り替え、規約上の制約 (他社の地図との併用)、利用者への見せ方

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

## 概要

地図が出なくなる原因は、提供元の障害だけでなく、無料枠や上限の超過、キーの失効や制限の誤り、支払いの失敗、無料のサービスの一時停止 (Supabase Free は 1 週間使われないと止まる) がある。備えは、原因を早く見分けること、代わりのスタイルや自前のタイルへ切り替えられるようにしておくこと、地図が出ない間も主題データや一覧は見せることの 3 つである。切り替え先は規約で縛られ、Google のタイルは Google 以外の地図と併用できない。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| 提供元のステータスページを購読、機械で読む | 自分の不具合か提供元の障害かを早く分ける | 部分的な障害や地域の障害は載らないことがある (推測) | Google https://status.cloud.google.com/maps-platform/ (`incidents.json` あり)、Mapbox https://status.mapbox.com/ (`/api/v2/status.json` あり)、MapTiler https://status.maptiler.com/ 、Esri https://status.location.arcgis.com/ 、HERE https://status.here.com/status 、Stadia https://status.stadiamaps.com/ 、Cloudflare https://www.cloudflarestatus.com/ (`/api/v2/status.json` あり)。Geolonia Maps、OpenFreeMap、地理院タイルには専用のページが無い | 2026-11-11 に各 URL を取得して確認 |
| 自前の外形監視 | 自分の利用者から見て地図が出るかを測る | 監視の要求も課金の対象になる (推測) | 代表のタイル 1 枚とスタイル JSON を定期的に取得し、状態コードと応答時間を見る | 推測 |
| 予備のスタイルへ切り替える | 主の提供元が落ちても地図を出す | Google の地図は他社の地図と併用できず、Google 以外への切り替えは地図全体の差し替えになる。HERE は他社のデータとの組み合わせを原則禁じ、区別できる重ね合わせだけ認める | MapLibre GL JS の `setStyle` で、主のスタイルと予備のスタイル (OpenFreeMap、自前の PMTiles など) を切り替える。`error` イベントで失敗を受け取る | [providers/google-maps](../../map-compare-infra/references/providers/google-maps.md)、[providers/here](../../map-compare-infra/references/providers/here.md)、MapLibre の MapEventType |
| 自前の PMTiles を予備に持つ | 外部の提供元にも無料枠にも頼らない予備になる | データの更新と帰属表示を自分で持つ ([data-update](data-update.md)) | 対象地域だけを切り出した PMTiles を R2 などに置く | [self-hosting](../../map-compare-arch/references/self-hosting.md) |
| 端末のキャッシュ、オフラインの地図 | 通信や提供元が落ちても、見た範囲を出す | 多くの提供元はキャッシュを制限する。Google は原則禁止、Mapbox は同じ端末で 30 日まで (モバイルは SDK の上限まで)、Stadia はモバイルで端末あたり 100MB まで、HERE は日本の結果を 24 時間を超えて保存できない、MapTiler は端末内の一時キャッシュだけ、Esri はネイティブ SDK などの Content Packages だけ | 自前のタイルなら Service Worker やアプリのストレージに置ける | 各 provider の reference |
| 地図以外の表示を残す | 地図が出ない間も、店舗の一覧や住所、主題データを見せる | 画面の設計が要る (map-ux-design) | 地図の領域にメッセージを出し、一覧の表示は止めない | 推測 |

## 判断を左右すること

- 主の提供元の規約: Google を主にするなら、予備は Google の地図を使わない別の画面か、地図全体の差し替えになる。重ねて混ぜる予備は置けない。
- 予備に要る詳しさ: 障害の間だけなら、OSM 由来の汎用の地図 (OpenFreeMap、自前の PMTiles) で足りることが多い。住所や建物の詳しさが本質のサービスでは、予備では業務が回らないことを前提に、表示を止めて案内する方がよいこともある (推測)。
- 原因の見分け方: 提供元の障害 (ステータスページ、複数の利用者で同時に起きる)、上限の超過 (Google の OverQuotaMapError、Stadia の 429、Geolonia Free の地図上の表示、Workers Free の Error 1027)、キーの問題 (Google の RefererNotAllowedMapError、Mapbox や Stadia の 401 / 403、HERE の 401)、支払い (Google の BillingNotEnabledMapError、Mapbox のアカウントの無効化)。対処が違うので、エラーを記録する仕組みを先に置く。
- 自動で切り替えるか、人が切り替えるか: 自動にすると、一時的な失敗でも予備に移り、帰属表示や見た目が頻繁に変わる。失敗の回数や時間に閾値を置く (推測)。

## 手順

1. 使っている提供元と自前の配信ごとに、ステータスページ (上の表) を購読する。機械で読める形 (`status.json`、`incidents.json`) があればチームの通知に流す。
2. 自前の外形監視で、代表のタイル 1 枚とスタイル JSON を数分おきに取り、状態コードと応答時間を記録する。
3. 地図のクライアントで、スタイルの読み込みとタイルの取得の失敗を受け取り、エラーの名前と状態コードを記録する (MapLibre GL JS は `error` イベント、Google の Maps JavaScript API はエラーの名前がコンソールに出る)。
4. 予備のスタイルを用意し、規約上の併用の制約を確かめる。予備の帰属表示も予備のデータに合わせて用意する。
5. 切り替えの条件 (例: スタイル JSON の取得が数回続けて失敗、タイルの失敗が一定の割合を超える) と、戻す条件を決める。
6. 地図が出ないときの画面 (メッセージ、一覧の表示) を作り、主の提供元を止めた状態で一度試す。
7. 無料のサービスの一時停止 (Supabase Free など) に頼る部分があれば、止まらない構成か、定期的に起こす仕組みを選ぶ ([source-of-truth](../../map-compare-arch/references/capabilities/source-of-truth.md))。

## 落とし穴

- Google の地図から他社の地図への切り替えは、同じ画面で重ねて使えない。予備を重ねる設計は規約違反になる ([providers/google-maps](../../map-compare-infra/references/providers/google-maps.md) の利用規約 3.2.3(e))。
- 予備の地図の帰属表示を、主の地図の表示のまま残さない。切り替えたら表示も切り替える。
- Workers Free の上限超過は、fail mode が open だと Worker を通らずにオリジンへ素通しになり、障害に見えないまま振る舞いが変わる。
- Geolonia Maps と OpenFreeMap と地理院タイルには専用のステータスページが無い。OpenFreeMap は変更を X と Bluesky で告知するとされ、地理院タイルは国土地理院のお知らせでメンテナンスを告知する。自前の外形監視が要る。
- SLA の無い提供元 (OpenFreeMap、地理院タイル、Geolonia Maps、MapTiler の Free と Flex) は、障害の補償も復旧の目安も無い。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- 予備に OSM 由来のタイルを使うなら、主の提供元と同じく ODbL の帰属表示が要る。OpenMapTiles スキーマなら「© OpenMapTiles」も要る ([self-hosting](../../map-compare-arch/references/self-hosting.md))。
- 主の提供元のタイルをキャッシュして予備にするのは、多くの規約で禁じられる (上の表の「端末のキャッシュ」の行)。予備は別の出どころのデータで作る。

## 出典

- https://status.cloud.google.com/maps-platform/ と https://status.cloud.google.com/maps-platform/incidents.json (2026-11-11 に取得、HTML と JSON を返した)
- https://status.mapbox.com/api/v2/status.json (2026-11-11 に取得、JSON を返した)
- https://status.maptiler.com/ 、https://status.location.arcgis.com/ 、https://status.here.com/status 、https://status.stadiamaps.com/ (2026-11-11 に取得、HTML を返した。Stadia の `/api/v2/status.json` は 404)
- https://www.cloudflarestatus.com/api/v2/status.json (2026-11-11 に取得、JSON を返した)
- https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapEventType/ (`error` イベント。2026-11-11)
- https://developers.google.com/maps/documentation/javascript/error-messages (エラーの名前。2026-11-11)
- https://developers.cloudflare.com/workers/platform/limits/ (Error 1027 と fail open / closed。2026-11-11)
- キャッシュの規約と SLA、ステータスページの有無は map-compare-infra の各 provider の reference (2026-11-10 確認) から写した。

## 未確認のこと

- MapLibre GL JS の `error` イベントが、タイルの失敗のときに source の ID や状態コードをどこまで含むか (型の説明ページに ErrorEvent の中身が書かれていない)。
- 各ステータスページが、地域 (日本) 単位や API 単位の部分的な障害をどこまで載せるか。
- Geolonia Maps の障害情報の公開先。
