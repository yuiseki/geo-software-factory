---
name: map-compare-auth
description: 地図プロダクトの認証と認可の仕組みを比較し選ぶ。管理型の認証サービス (Auth0、Clerk、Firebase Authentication、Supabase Auth、Amazon Cognito、WorkOS、Logto など) と OSS (Better Auth、Keycloak、Ory など) を、料金 (MAU)、機能 (SSO、パスキー、組織と役割)、DB の行単位アクセス制御との連携、エッジでの検証、日本リージョン、公共案件での利用、ロックインで比べる。タイルや地図データへのアクセス制御も扱う。「地図アプリに認証をつけたい」「どの認証サービスがいい」「自治体ごとにデータを出し分けたい」「タイルを限られた人だけに見せたい」と言われたら使う。
---

# map-compare-auth

地図プロダクトの利用者の認証 (誰か) と、データやタイルへの認可 (何を見てよいか) の仕組みを選ぶ。認証サービスを足切り、軸ごとの評価、規模ごとの費用の順に比べ、タイルやデータへのアクセス制御の手段と組み合わせて推奨を出す。比較の軸は [criteria](references/criteria.md) にあり、各提供者の事実は下の表の reference にある。正本の DB をどこに置くか、RLS を使うかの置き場所は map-compare-arch で決める。

| reference | 読むとき | 中身 |
|---|---|---|
| [criteria](references/criteria.md) | 比較を始める前に、いつも | 比較の軸と、要件から軸の重みを決める方法、費用の揃え方 |
| [providers/auth0](references/providers/auth0.md) | 候補に入れるとき | Auth0 |
| [providers/clerk](references/providers/clerk.md) | 候補に入れるとき | Clerk |
| [providers/firebase-auth](references/providers/firebase-auth.md) | 候補に入れるとき | Firebase Authentication と Identity Platform |
| [providers/supabase-auth](references/providers/supabase-auth.md) | 候補に入れるとき、PostGIS と RLS で地物を出し分けるとき | Supabase Auth |
| [providers/amazon-cognito](references/providers/amazon-cognito.md) | 候補に入れるとき、AWS で配信するとき | Amazon Cognito |
| [providers/workos](references/providers/workos.md) | 候補に入れるとき、企業 SSO が中心の B2B | WorkOS AuthKit |
| [providers/logto](references/providers/logto.md) | 候補に入れるとき | Logto (OSS と Cloud) |
| [providers/better-auth](references/providers/better-auth.md) | 候補に入れるとき、自分の DB に利用者を持ちたいとき | Better Auth |
| [providers/keycloak](references/providers/keycloak.md) | 候補に入れるとき、閉域網や既存の SAML 基盤があるとき | Keycloak |
| [providers/ory](references/providers/ory.md) | 候補に入れるとき | Ory (OSS と Ory Network) |
| [tile-access-control](references/tile-access-control.md) | タイルや地図データを限られた人だけに見せたいとき | 署名付き URL と Cookie、短命のトークン、Cloudflare Access、Referer の制限が弱い理由、MapLibre と PMTiles でのトークンの付け方 |
| [niche](references/niche.md) | 公共案件、自治体の職員が使う、マイナンバーカードや GビズID が話に出たとき | GビズID、公的個人認証、LGWAN |

関連する事実は他のスキルにある。RLS、PostgREST、署名付き URL の期限、Supabase の Free の休止は map-compare-arch の [source-of-truth](../map-compare-arch/references/capabilities/source-of-truth.md)、エッジ関数の制約と料金は [edge-functions](../map-compare-arch/references/edge/edge-functions.md)、位置情報と外国にある第三者への提供は map-legal-check の [location-privacy](../map-legal-check/references/location-privacy.md)。

## 入力

比較の前に、次の要件をそろえる。プロダクト概要があればそこから読み、無ければ依頼から読み取る。

- 利用者: 一般の利用者 (B2C)、顧客企業や自治体の職員 (B2B)、社内だけ
- 規模: 月に使う利用者数。B2B なら組織 (自治体、顧客企業) の数
- 制御する対象: 画面だけか、API、タイルや PMTiles、DB の行 (地物ごと) まで制御するか
- 出し分けの単位: 組織ごと、役割ごと、地域ごと、地物ごと
- 必須の認証方式: 企業 SSO (SAML)、パスキー、LINE などのソーシャルログイン、マイナンバーカード
- データの保存地域: 日本に置く必要があるか。位置情報や移動の記録を利用者に結びつけるか
- ネットワークと調達: 閉域網や LGWAN 接続系か、公共案件で ISMAP の登録が要るか、受託で納品するか
- map-compare-arch の結果: 正本の DB (PostgreSQL + PostGIS か、ファイルか)、エッジに置くか、配信の CDN

利用者、規模、制御する対象の 3 つが分からないまま比較に入らない。足切りと費用がこの 3 つで決まるので、分からなければ先に聞く。聞くときは選択肢で答えられる形にし、1 回に聞く数を絞る (例: 「A: 一般の利用者、B: 自治体や企業の職員、C: 社内だけ、D: それ以外」)。要件が全体に曖昧なら、比較の前にプロダクトの価値から聞き直す (map-product-grilling)。

## 進め方

1. [criteria](references/criteria.md) を読み、「要件から軸の重みを決める」の表で、当てる足切りの条件と重くする軸を決める。
2. 制御する対象を分ける。画面と API のログインは認証サービスで、タイルやファイルは [tile-access-control](references/tile-access-control.md) の手段で、地物ごとの出し分けは DB の RLS で行う。1 つの仕組みで全部を賄おうとしない。
3. 候補を集める。下の「最初の当たり」から要件に合うものを選び、表の「読むとき」に当てはまる reference を開く。公共案件や LGWAN、マイナンバーカードが話に出たら [niche](references/niche.md) を見る。
4. 足切りの条件で候補を外す。外した候補と理由を残す。
5. 残った候補を評価の軸で比べる。値は各 reference から写し、reference に「未確認」とあるものは未確認のまま書く。
6. 費用を見積もる。[criteria](references/criteria.md) の「費用の揃え方」に従い、MAU、MRU、aDAU、SSO の接続数を揃えて、規模ごとに並べる。
7. タイルやデータを制御するなら、選んだ認証サービスのトークンをどこで検証するか (CDN、エッジ関数、タイルサーバー) と、地図ライブラリへの付け方を決める。
8. 料金、無料枠、地域、規約の数字は、答える前に公式ページで確かめ直す。reference の確認日 (2026-11-11) から変わっていれば新しい値を使い、変わったことを書く。確かめ直せなければ、reference の確認日を添えて出す。
9. 「出力」の形で答え、プロダクト概要の「技術選定の結果」に認証の節を書き足す。前の段階の節は書き換えない。

## 最初の当たり

候補を集めるときの出発点。どれも足切りと評価の軸で確かめてから推奨する。

- 地物を PostGIS に置き、利用者や組織ごとに見える行を DB で強制したい: Supabase Auth (JWT をそのまま RLS で使える、東京リージョン)。Free は 1 週間使われないと止まる
- React や Next.js の試作を早く: Clerk (50,000 MRU 無料、LINE あり)。データは米国だけ
- 管理型でデータを日本に置きたい: Auth0 (JP)、Logto Cloud (Japan East)、Supabase (東京)、Cognito (リージョン)
- AWS で地図を配る: Amazon Cognito と CloudFront の署名付き Cookie
- 既に Firebase で作っている: Firebase Authentication (パスキーは標準の記載なし)
- 自治体や企業ごとの SAML の SSO が中心の B2B: WorkOS (100 万 MAU 無料、SSO は接続ごとの課金)、Auth0 の B2B プラン
- 閉域網、オンプレ、既存の SAML や AD と連携: Keycloak (Apache-2.0)
- 自分の DB に利用者を持ち、MAU の課金を避けたい: Better Auth (MIT、Cloudflare Workers で動く)
- 認証、OAuth、権限の判定を部品で組みたい: Ory (OSS は Apache-2.0、本番の自前運用には OEL を勧めている)
- 社内や少数の関係者だけにタイルを見せる: Cloudflare Access をタイルのホストの前に置く (50 人未満は無料)
- キーの流用による課金を抑えたいだけ: Referer の制限 (アクセス制御にはならない)

## 出力

答えは次の順に並べる。

1. 推奨: 認証サービスと、タイルやデータの制御の手段を、それぞれの理由とともに 1〜2 文ずつ。
2. 足切りで外した候補と理由。
3. 比較表: 行に評価の軸、列に候補。各セルに値と reference の根拠。
4. 費用表: 規模 (1,000、10,000、100,000、1,000,000 人) ごとの月額。SSO の接続数は別の行。課金単位の違い (MAU、MRU、aDAU) を注記する。
5. 制御の構成: どこで何を検証するか (認証サービス、CDN やエッジ、DB の RLS) と、地図ライブラリでのトークンの付け方 (MapLibre の `transformRequest`、PMTiles の `customHeaders`)。
6. 移行の備え: パスワードのハッシュを持ち出せるか、認可のロジックが提供者の独自機能に依存する箇所。
7. 確かめた日: 料金、地域、規約を確かめた日。
8. 未確認のこと: 結論を左右するのに確かめられなかったこと。確かめる手順 (公式ページ、手で 1 回試す) を添える。

## 注意

- Referer や Origin の制限をアクセス制御として推奨しない。curl などは任意の Referer を送れる ([tile-access-control](references/tile-access-control.md))。
- 取得を許した人はタイルやデータを保存できる。アクセス制御は持ち出しを防がない。データの利用条件は規約で縛る (map-legal-check)。
- 課金単位 (MAU、MRU、aDAU、トークン、SSO の接続) は提供者ごとに数え方が違う。同じ数として足し引きしない。
- 無料枠の条件 (Supabase の休止、Clerk の Hobby にパスキーなし、Cognito の古いプールの無料枠) を費用表の注記に書く。
- 位置情報や移動の記録を利用者に結びつけるなら、認証の提供者の所在地を書き、map-legal-check の [location-privacy](../map-legal-check/references/location-privacy.md) へ渡す。
- 自前運用の OSS を改変して納品するときは、ライセンスの条件 (Logto の MPL-2.0 など) を答えに書く。
- 規約やライセンスの解釈は、条文から読んだものと推測を分けて書く。法的な判断を断定しない。
