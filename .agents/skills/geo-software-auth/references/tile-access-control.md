# タイルと地図データへのアクセス制御

対象: タイルや PMTiles、GeoJSON を限られた人だけに見せる手段 (署名付き URL、署名付き Cookie、短命のトークン、エッジ関数での JWT 検証、Cloudflare Access、Referer の制限)。地図ライブラリでのリクエストへのトークンの付け方 (MapLibre の transformRequest、PMTiles の FetchSource)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

## 概要

地図は 1 回の表示で多数のタイルを取りに行くので、1 枚ずつ認可の重い処理を挟むと遅く高くなる。そこで、ログインの時点で短命の許可 (トークン、署名付き Cookie、署名付き URL) を発行し、タイルの前段 (CDN やエッジ関数) では署名と期限だけを確かめる形が基本になる。Referer や Origin の制限は、他のサイトに埋め込まれるのを減らすだけで、誰が取れるかの制御にはならない。どの手段でも、取得を許した人はタイルの中身をすべて保存できる。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| API キーと Referer (URL) の制限 | 他のサイトのブラウザからキーを流用されるのを減らす | Mapbox は URL 制限を「best-effort な緩和策」と書き、Referer のないリクエストは 403、モバイル SDK からのリクエストは対象外とする。Google はブラウザがクロスオリジンで Referer を削ることがあり、referrer-policy 次第で挙動が変わるとする。Referer はブラウザの JavaScript からは書き換えられない (forbidden request header) が、curl は `-e` で任意の Referer を送れる | 地図 API の各社。自前なら CDN のルールやエッジ関数で照合 | https://docs.mapbox.com/accounts/guides/tokens/ 、 https://developers.google.com/maps/api-security-best-practices 、 https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referer 、 https://curl.se/docs/manpage.html |
| 署名付き URL (オブジェクト単位) | 1 つのファイル (PMTiles 1 本、GeoJSON 1 本) を期限付きで許可する | URL を持つ人は誰でも使える。S3 と R2 は最長 7 日 (geo-software-arch の source-of-truth に記載)。z/x/y のタイル群に 1 枚ずつ署名するのは向かない (推測) | S3、R2、Cloud Storage、Supabase Storage (`createSignedUrl(path, expiresIn)`、秒) | [source-of-truth](../../geo-software-arch/references/capabilities/source-of-truth.md)、 https://cloud.google.com/storage/docs/access-control/signed-urls 、 https://supabase.com/docs/reference/javascript/storage-from-createsignedurl |
| 署名付き Cookie | 多数のファイル (タイル群) を URL を変えずに許可する | CloudFront は「複数の制限付きファイルを許可したいとき、今の URL を変えたくないとき」に Cookie を勧め、Cookie を扱えないクライアントには URL を勧める。`Expires`、`Policy`、`Signature`、`Key-Pair-Id`、`Hash-Algorithm` のクエリを持つ URL では使えない。両方あると署名付き URL が優先 | CloudFront | https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-choosing-signed-urls-cookies.html |
| 短命のトークン (JWT) をヘッダーに付けてエッジで検証 | 認証サービスの利用者ごとに許可し、組織や役割のクレームで出し分ける | 期限までは失効を見抜けない (Cognito の文書は、署名と期限の確認だけでは失効を検出できないので寿命を短くするよう書く)。公開鍵 (JWKS) のキャッシュと更新が要る | Cloudflare Workers (Web Crypto)、jose 6.2.17 (MIT)、aws-jwt-verify 5.2.1 (Apache-2.0)。各認証サービスの JWKS は providers/ の各 reference | https://developers.cloudflare.com/workers/runtime-apis/web-crypto/ 、 https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html |
| Cloudflare Access をタイルのホストの前に置く | 社内や限られた関係者だけに見せる。アプリ側で認証を作らずに済む | 1 人 1 席で数える。Free は 50 人未満のチーム向けで 0 ドル、従量は 1 人月 7 ドル。オリジンでは `Cf-Access-Jwt-Assertion` ヘッダーの JWT を、チームの certs と AUD タグで検証するよう勧めている (Cookie の `CF_Authorization` より推奨)。一般の利用者が多い B2C には向かない (推測) | Cloudflare Zero Trust | https://www.cloudflare.com/plans/sase-zero-trust.md 、 https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/validating-json/ |
| URL の HMAC トークンを WAF で検証 | 期限付きの URL を、オリジンのコードなしに CDN で検証する | `is_timed_hmac_valid_v0()` は Cloudflare の Pro、Business、Enterprise のみ | Cloudflare WAF のカスタムルール | https://developers.cloudflare.com/waf/custom-rules/use-cases/configure-token-authentication/ |
| DB の行単位アクセス制御 (RLS) で地物を絞って返す | 利用者や組織ごとに見える地物 (行) を DB で強制する | ファイルやタイルの中の行ごとには効かない。PostgreSQL では方針がないと既定で全行拒否 | PostgreSQL + PostGIS、PostgREST、Supabase | [source-of-truth](../../geo-software-arch/references/capabilities/source-of-truth.md) |

## 判断を左右すること

- 誰に見せるか: 社内や少数の関係者なら Cloudflare Access のような前段の認証で足りる。一般の利用者ごとに出し分けるなら、認証サービスのトークンをエッジで検証する。
- 何の単位で出し分けるか: 地域や組織ごとにタイルのファイルを分けられるなら、ファイル単位の署名付き URL や Cookie で済む。同じ範囲の中で行ごとに出し分けるなら、RLS で絞ってから返すか、利用者ごとにタイルを作る (推測。後者はキャッシュが効かない)。
- 失効の速さ: 退職や契約終了で即座に止める必要があるなら、トークンの寿命を短くし、更新の仕組みを用意する。
- クライアント: Cookie はブラウザでは扱いやすいが、ネイティブアプリや独自の HTTP クライアントでは CloudFront も署名付き URL を勧めている。
- 費用: タイル 1 枚ごとにエッジ関数が動くと、リクエスト数で課金が増える ([edge-functions](../../geo-software-arch/references/edge/edge-functions.md) の料金)。

## 手順

1. 見せる相手と、出し分けの単位 (ファイル、地域、行) を決める。
2. 上の表から手段を選ぶ。Referer の制限だけで済ませるのは、見られても困らないデータで、キーの流用による課金だけを抑えたい場合に限る。
3. 地図ライブラリにトークンを付ける。MapLibre GL JS (6.17.0、npm) では `transformRequest` (`(url, resourceType) => RequestParameters`) で、対象の URL のときだけ `headers` に `Authorization` を足すか、`credentials: 'include'` で Cookie を送る。RequestParameters は `url`、`headers`、`credentials` (`same-origin` か `include`)、`referrerPolicy` などを持つ (https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/RequestTransformFunction/ 、 https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/RequestParameters/)。
4. PMTiles (pmtiles 4.5.0、npm) では `FetchSource` の第 2 引数に `customHeaders` (Headers)、第 3 引数に `credentials` を渡し、`setHeaders()` で差し替えられる (https://github.com/protomaps/PMTiles/blob/main/js/src/index.ts)。公式の MapLibre の手順 (`addProtocol("pmtiles", protocol.tile)`) には認証の記載がない (https://docs.protomaps.com/pmtiles/maplibre)。`pmtiles://` のリクエストに `transformRequest` が効くかは未確認なので、ヘッダーは FetchSource で付ける。
5. 前段 (エッジ関数、CDN) で、署名、`exp`、`iss`、`aud` (サービスごとに `azp` や `token_use`) を確かめる。公開鍵は JWKS から取り、`kid` で選び、キャッシュする。
6. 許可したあとのタイルをキャッシュするなら、トークンをキャッシュのキーに入れない (推測。入れると利用者ごとにキャッシュが割れる)。共有のキャッシュに載せる応答と、利用者ごとの応答 (`Cache-Control: private`) を分ける (推測)。
7. 期限切れのときの更新を確かめる。地図を開いたまま期限が来ても、次のタイルの取得で新しいトークンが付くようにする (推測)。

## 落とし穴

- Referer の制限を「アクセス制御」と呼ばない。curl などは任意の Referer を送れる。ブラウザも referrer-policy 次第で Referer を削り、正規の利用者が弾かれることがある (Google の文書)。
- 署名付き URL や URL のトークンは持参人トークンで、URL が漏れれば誰でも使える。URL のクエリに入れたトークンはアクセスログに残る (推測)。
- JWT は期限まで有効なので、ログアウトしても取得できる時間が残る。
- 許可した人はタイルを保存できる。持ち出しを防ぐ仕組みではない。データの利用条件は規約で縛る (geo-software-legal-check)。
- Supabase の JWKS はエッジで約 10 分、クライアントライブラリでさらに約 10 分キャッシュされるので、鍵の切り替えの直後は古い鍵で検証されうる (https://supabase.com/docs/guides/auth/signing-keys)。
- CloudFront Functions はネットワークに触れないので JWKS を取りに行けない ([edge-functions](../../geo-software-arch/references/edge/edge-functions.md))。
- 位置情報を含むデータ (利用者の軌跡など) は、アクセス制御とは別に個人情報としての扱いがかかる ([location-privacy](../../geo-software-legal-check/references/location-privacy.md))。

## ライセンス上の注意

- maplibre-gl と pmtiles の JS 実装は BSD-3-Clause (npm)。PMTiles の仕様は public domain か CC0 (リポジトリの LICENSE)。組み込み、配布するときは著作権表示とライセンス文を残し、作者の名前を宣伝に使わない。
- jose は MIT、aws-jwt-verify は Apache-2.0。いずれもコピーレフトではなく、SaaS でもソースの公開義務はない。
- Cloudflare Access、WAF、CloudFront は各社の規約による。

## 出典

- https://docs.mapbox.com/accounts/guides/tokens/ : URL 制限は best-effort、Referer のないリクエスト、モバイル SDK (2026-11-11)。
- https://developers.google.com/maps/api-security-best-practices : Referer の削除と referrer-policy、プラットフォームごとの制限 (2026-11-11)。
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referer : forbidden request header (2026-11-11)。
- https://curl.se/docs/manpage.html : `-e`、`--referer` (ページの存在を確認)。
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-choosing-signed-urls-cookies.html : 署名付き URL と Cookie の使い分け (2026-11-11)。
- https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/validating-json/ : Access の JWT の検証 (2026-11-11)。
- https://www.cloudflare.com/plans/sase-zero-trust.md : Zero Trust の Free と従量の料金 (2026-11-11)。
- https://developers.cloudflare.com/waf/custom-rules/use-cases/configure-token-authentication/ : HMAC トークン、Pro 以上 (2026-11-11)。
- https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/RequestTransformFunction/ 、 https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/RequestParameters/ : transformRequest (2026-11-11)。
- https://github.com/protomaps/PMTiles : FetchSource の customHeaders と credentials、LICENSE (2026-11-11)。

## 未確認のこと

- MapLibre の `transformRequest` が `addProtocol` で登録した `pmtiles://` のリクエストに効くか。
- 署名付き GET URL に Range ヘッダーを付けた部分取得が、S3 と R2 でそのまま通るか (PMTiles に要る)。手で 1 回試してから構成を決める。
- 署名付き Cookie をクロスオリジンのタイルのホストで使うときの、Cookie の属性 (SameSite、ドメイン) の条件。
- Cloudflare Zero Trust の Free の機能制限 (ログの保持など) の公式の値。
