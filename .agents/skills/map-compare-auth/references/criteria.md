# 比較の軸 (認証と認可)

地図プロダクトの利用者の認証と、データやタイルへの認可の仕組みを同じ軸で並べるための手順。比較を始める前に読む。各提供者の事実は `providers/` に、タイルとデータの制御は [tile-access-control](tile-access-control.md) に、国内や公共の手段は [niche](niche.md) にあり、この文書には軸と判定の手順だけを書く。例として挙げる事実は、各 reference に 2026-11-11 時点で書かれていたもの。

## 進め方

1. 要件を、認証 (誰か)、認可 (何を見てよいか)、制御する対象 (画面、API、タイル、DB の行) に分ける。
2. 足切りの条件で候補を外す。足切りは「点数を下げる」ではなく「候補から外す」。
3. 残った候補を、評価の軸で比べる。軸の重みは「要件から軸の重みを決める」の表で決める。
4. 費用は、課金単位を揃えて規模ごとに並べる (下の「費用の揃え方」)。
5. 推奨を先に書き、続けて軸ごとの評価を示す。確かめられなかった項目は「未確認」のまま残す。

## 足切りの条件

| 条件 | 何を確かめるか | 外れる例 (各 reference の記述) |
|---|---|---|
| データの保存地域 | 利用者のデータを日本に置く必要があるか | Clerk は地域を選べず米国 ([clerk](providers/clerk.md))。Firebase と WorkOS は保存地域を確かめられていない。Ory Network の日本は一般提供でない ([ory](providers/ory.md))。Neon Auth はデータベースと同じリージョンで、アジアは Singapore と Sydney だけ ([neon-auth](providers/neon-auth.md))。日本を選べるのは Auth0 (JP)、Supabase (東京)、Logto Cloud (Japan East)、Cognito (リージョンに作る) と、自前運用の OSS |
| 外部への通信 | 閉域網、LGWAN 接続系、オフラインか | 管理型のサービスは外れ、自前運用の OSS (Keycloak、Ory、Logto、Supabase Auth、Better Auth) に限られる ([niche](niche.md)) |
| 調達の条件 | ISMAP クラウドサービスリストへの登録が求められるか | AWS は ISMAP に登録 (Cognito の個別の掲載は未確認、[amazon-cognito](providers/amazon-cognito.md))。他の管理型サービスはいずれも未確認。自前運用の OSS は動かす基盤で判断する |
| 必須の認証方式 | 企業 SSO (SAML)、パスキー、LINE ログインが必須か | パスキーは Firebase に標準の記載なし、Supabase は実験的、Neon Auth は記載なし、Clerk は Pro 以上、Cognito は Essentials 以上。LINE は Firebase、Supabase、Neon Auth、Keycloak の標準にない (独自の OIDC で足す) |
| ライセンス | 自前運用するソフトウェアを改変して配布 (受託で納品) するか | Logto は MPL-2.0 で、改変したファイルは MPL-2.0 のままソースを渡す ([logto](providers/logto.md))。Keycloak、Ory、Supabase の OSS は Apache-2.0 か MIT |

## 評価の軸

### 1. 費用 (課金単位と無料枠)

- 課金単位が提供者ごとに違う: MAU (Auth0、Firebase、Supabase、Neon Auth、Cognito、Logto)、MRU (Clerk)、aDAU (Ory Network)、企業 SSO の接続数 (WorkOS、Auth0、Clerk)、トークン数 (Logto Cloud の Pro)、ソフトウェア代なし (Keycloak、Better Auth、各 OSS)。
- 無料枠の例: Auth0 25,000 MAU、Clerk 50,000 MRU、Firebase 50,000 MAU、Supabase 50,000 MAU、Neon Auth 60,000 MAU (認証は別料金なし、費用は Postgres の計算と保存)、Cognito Lite と Essentials 10,000 MAU、Logto 50,000 MAU、WorkOS 100 万 MAU。
- 無料枠の条件: Supabase の Free は 1 週間使われないと止まる ([source-of-truth](../../map-compare-arch/references/capabilities/source-of-truth.md))。Clerk の Hobby ではパスキーが使えない。

### 2. 機能 (認証方式)

- パスキー、MFA、ソーシャルログイン (国内向けなら LINE)、メールのリンクと OTP。
- 企業 SSO (SAML、OIDC): 自治体や企業の利用者が既存の ID で入るか。B2B では接続数がそのまま費用になる。

### 3. 認可のモデル

- 組織 (テナント) と役割: 自治体ごと、顧客企業ごとにデータを分けるか。Auth0 Organizations、Clerk Organizations、Keycloak Organizations、Logto の組織と RBAC、Better Auth の Organization プラグイン。Ory の自前運用では B2B の組織が OEL 版だけ。
- DB の行単位アクセス制御 (RLS) との結びつき: Supabase は JWT を RLS の `auth.uid()`、`auth.jwt()` でそのまま使える。Neon Auth は Data API で `auth.user_id()` を使う。他は PostgREST など JWT のクレームを DB に渡す層が要る。
- タイルやファイルの制御: [tile-access-control](tile-access-control.md) の手段と組み合わせられるか (JWKS で公開鍵を取れるか、短命のトークンか)。

### 4. エッジとの相性

- JWKS で公開鍵を取り、Web Crypto のある環境で検証できるか。Clerk、Supabase、Neon Auth、Cognito、Firebase は JWKS か公開鍵の場所を文書化している。
- 認証の処理そのものをエッジで動かせるか: Better Auth は Cloudflare Workers の例がある。Keycloak、Ory、Logto の OSS は常時動くサーバー (推測)。
- エッジ関数の制約は [edge-functions](../../map-compare-arch/references/edge/edge-functions.md)。CloudFront Functions は JWKS を取りに行けない。

### 5. 運用の負担

- 管理型: 更新、鍵の管理、可用性は提供者が持つ。障害時に自分では直せない。
- 自前運用: サーバー、DB、脆弱性の対応を自分で持つ。Ory は OSS 版を「評価と試作向け」とし、本番の自前運用に OEL を勧めている ([ory](providers/ory.md))。

### 6. ロックインと移行

- パスワードのハッシュを持ち出せるか: Cognito は出せない。Auth0 はサポート経由で、Free では不可。Firebase の書き出しはスクリプトのハッシュだけ。Clerk はダッシュボードの CSV に入る。自前運用の OSS、Supabase、Neon Auth は自分の DB にある。
- 取り込めるか: WorkOS と Firebase はハッシュの形式の一覧を出している。Cognito と Auth0 はログイン時に移す仕組みを持つ。
- 認可のロジックが提供者の独自機能 (Supabase の `auth.uid()`、独自のクレーム) に依存するほど、移るときの書き換えが増える (推測)。

### 7. 個人情報と所在地

- 位置情報や移動の記録を利用者に結びつけるなら、認証の提供者に渡る情報と、その所在地 (外国にある第三者への提供) を確かめる ([location-privacy](../../map-legal-check/references/location-privacy.md))。

## 要件から軸の重みを決める

| 要件 | 足切りに当てる条件 | 重くする軸 |
|---|---|---|
| 個人や小さな試作、無料で始めたい | なし | 費用 (無料枠と休止の条件)、運用の負担 |
| 一般の利用者向け (B2C) で利用者が多い | 必須の認証方式 | 費用 (MAU の単価)、機能 (ソーシャル、パスキー) |
| 自治体や企業ごとにデータを出し分ける B2B | 必須の認証方式 (企業 SSO) | 認可のモデル (組織と役割)、費用 (SSO の接続数) |
| 地物ごとに見える範囲を変える (同じ地域の中で) | なし | 認可のモデル (RLS との結びつき) |
| タイルや PMTiles を限られた人だけに見せる | なし | エッジとの相性、[tile-access-control](tile-access-control.md) |
| 公共案件、自治体の職員が使う | 調達の条件、外部への通信、データの保存地域 | 運用の負担、[niche](niche.md) |
| 受託で納品し、相手の環境で動かす | ライセンス、外部への通信 | 運用の負担、ロックインと移行 |
| 位置情報や移動の記録を扱う | データの保存地域 | 個人情報と所在地 |
| 将来、提供者を乗り換える可能性がある | なし | ロックインと移行 |

## 費用の揃え方

1. 月間の利用者数を見積もる。分からなければ、登録者数と月に 1 回以上使う割合から出す。
2. 提供者ごとの課金単位に直す。MRU (Clerk) と aDAU (Ory) は MAU と数え方が違うので、各 reference の定義を見て、MAU と同じ値として扱わない。aDAU は日ごとの平均なので、MAU より小さくなる (推測)。
3. 企業 SSO が要るなら、接続数 (自治体や顧客企業の数) を別の行に置く。
4. 1,000、10,000、100,000、1,000,000 の 4 段で並べ、無料枠を超える段を示す。
5. 自前運用の OSS は、サーバーと DB の費用と、運用の人手を別に書く。人手の見積もりは推測と明記する。

## この文書で扱っていない仕組み

- Microsoft Entra ID (External ID を含む)、Okta Workforce、国内の業務向け IDaaS: reference で調べていない。
- 地図 API の提供者 (Mapbox、Google など) の API キーの管理: map-ops で扱う予定。
