---
name: map-compare-auth
description: 地図プロダクトの認証と認可の仕組みを比較し選ぶ。管理型の認証サービス (Auth0、Clerk、Firebase Authentication、Supabase Auth、Amazon Cognito、WorkOS、Logto など) と OSS (Better Auth、Keycloak、Ory など) を、料金 (MAU)、機能 (SSO、パスキー、組織と役割)、DB の行単位アクセス制御との連携、エッジでの検証、日本リージョン、公共案件での利用、ロックインで比べる。タイルや地図データへのアクセス制御も扱う。「地図アプリに認証をつけたい」「どの認証サービスがいい」「自治体ごとにデータを出し分けたい」「タイルを限られた人だけに見せたい」と言われたら使う。
---

# map-compare-auth

地図プロダクトの利用者の認証と、データやタイルへの認可の仕組みを選ぶ。

> 骨組みの段階で、手順と reference はまだ書かれていない。このスキルを使うと決めたら、骨組みであることを答えに書き、reference の「[記入]」や空欄を事実として扱わない。判断は、書き上がったスキル (map-compare-arch、map-compare-infra、map-compare-library、map-compare-data、map-legal-check) と公式の文書で確かめられる範囲にとどめる。

後で書く。

| reference | 読むとき | 中身 |
|---|---|---|
| [criteria](references/criteria.md) | 比較を始める前に、いつも | 比較の軸 (後で書く) |
| [providers/auth0](references/providers/auth0.md) | 候補に入れるとき | Auth0 |
| [providers/clerk](references/providers/clerk.md) | 候補に入れるとき | Clerk |
| [providers/firebase-auth](references/providers/firebase-auth.md) | 候補に入れるとき | Firebase Authentication |
| [providers/supabase-auth](references/providers/supabase-auth.md) | 候補に入れるとき | Supabase Auth |
| [providers/amazon-cognito](references/providers/amazon-cognito.md) | 候補に入れるとき | Amazon Cognito |
| [providers/workos](references/providers/workos.md) | 候補に入れるとき | WorkOS AuthKit |
| [providers/logto](references/providers/logto.md) | 候補に入れるとき | Logto |
| [providers/better-auth](references/providers/better-auth.md) | 候補に入れるとき | Better Auth |
| [providers/keycloak](references/providers/keycloak.md) | 候補に入れるとき | Keycloak |
| [providers/ory](references/providers/ory.md) | 候補に入れるとき | Ory |
| [tile-access-control](references/tile-access-control.md) | タイルや地図データを限られた人だけに見せたいとき | タイルとデータへのアクセス制御 |
| [niche](references/niche.md) | 上のどれも要件に合わないとき (公共、国内特有) | 国内や公共の案件で候補になるもの |

後で書く:

- 入力 (要件のうち、このスキルの判断を左右するもの)
- 進め方
- 出力の形
- 注意
