# Clerk

対象: Clerk (管理型の認証サービス)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | Clerk, Inc. |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | 管理型サービスのみ |
| ライセンス (OSS の場合) | サービス本体は OSS ではない。SDK のモノレポ clerk/javascript は MIT (`gh api repos/clerk/javascript/license`)、`@clerk/backend` 3.27.0 は MIT (npm) |
| 料金ページ | https://clerk.com/pricing |
| ドキュメント | https://clerk.com/docs |

## 概要

Clerk は React や Next.js 向けの UI 部品と SDK を中心にした管理型の認証サービスである。課金単位は MAU ではなく MRU (Monthly Retained Users) で、組織機能 (B2B) は MRO (Monthly Retained Organizations) で数える。データは米国のインフラに置かれ、地域を選べない。

## 料金と無料枠

- 課金単位と無料枠: MRU。Hobby (無料) は 1 アプリあたり 50,000 MRU、ダッシュボードの席は 3 まで (https://clerk.com/pricing、2026-11-11)。MRU の定義の細部は未確認。
- 有料プランの最低額と、主な機能が入るプラン: Pro は月 25 ドル (年払いで月 20 ドル)。50,000 MRU を超えた分は 50,001〜100,000 が 1 MRU 月 0.02 ドル、100,001〜1,000,000 が 0.018 ドルと段階で下がる。Business と Enterprise もある (Enterprise は見積もり) (https://clerk.com/pricing、2026-11-11)。
- SSO (SAML) や組織機能の追加料金: Pro と Business は 1 アプリあたり SSO 接続 1 を含み、追加は 2〜15 が 1 接続月 75 ドル、16〜100 が 60 ドル、101〜250 が 48 ドル。組織は 100 MRO と 1 組織 20 人までが含まれ、Enhanced の追加 (月 100 ドル、年払いで月 85 ドル) で人数無制限、100 MRO を超えた分は 101〜1,000 が 1 MRO 月 1 ドル (https://clerk.com/pricing、2026-11-11)。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 対応 | 詳細は未確認 |
| ソーシャルログイン (Google、Apple、LINE など) | 対応 | LINE の設定手順の文書がある (https://clerk.com/docs/guides/configure/auth-strategies/social-connections/line、2026-11-11) |
| パスキー | Pro 以上 | Hobby では使えない (https://clerk.com/pricing、2026-11-11) |
| MFA | 未確認 | プランの差は未確認 |
| SAML / OIDC による企業 SSO | 対応 | 接続数で課金 (上記) |
| 組織・テナントと役割 (RBAC) | 対応 | Organizations。MRO で課金 |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | JWT を発行する | セッショントークンを JWKS (`https://api.clerk.com/v1/jwks` か Frontend API の `/.well-known/jwks.json`) か公開鍵で検証でき、`azp` を許可するオリジンと照合するよう求めている (https://clerk.com/docs/guides/sessions/manual-jwt-verification、2026-11-11) |
| 日本語の画面 | 未確認 | |
| データの保存地域 (日本リージョン) | 選べない | 「地域のデータ所在地や地域の選択を提供しない」。米国のインフラ (Google Cloud と Cloudflare)、サブプロセッサーはすべて米国 (https://clerk.com/security.md、2026-11-11) |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: セッショントークンをタイルのリクエストに付け、エッジ関数で公開鍵を使って検証する。手段は [tile-access-control](../tile-access-control.md)。トークンの寿命が短い場合、地図ライブラリの `transformRequest` で毎回新しいトークンを付ける必要がある (推測。寿命の値は未確認)。
- エッジ関数やサーバーレスで動くか: 公開鍵による検証はネットワークを使わずにできると文書にある (上記)。対応ランタイムの一覧は未確認。

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: ISMAP の登録は未確認。SOC 2 Type 2 は 2022-05-06 から取得 (https://clerk.com/security.md)。データが米国に置かれるので、個人情報を外国にある第三者に渡す扱いになりうる (推測。条文は map-legal-check の [location-privacy](../../../map-legal-check/references/location-privacy.md) の第 28 条)。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): ダッシュボードの「Export users」で CSV を出せ、ハッシュ化したパスワードを含む (https://clerk.com/docs/guides/development/migrating/overview、2026-11-11)。
- 他の提供者からの取り込み: Backend API の `CreateUser` か OSS の移行ツールで、`password_hasher` を指定して取り込む。対応するハッシュの一覧は未確認 (同上)。

## ライセンス上の注意

- サービス本体は商用サービスで、利用条件は Clerk の規約による。SDK は MIT なので、組み込み、改変、配布、SaaS のいずれでも著作権表示とライセンス文を残せばよい。

## 向いている場面

- React や Next.js の試作で、UI 部品をそのまま使って早く認証を付けたいとき。
- 無料枠 50,000 MRU で始めたいとき (パスキーが要るなら Pro)。
- LINE ログインを管理型で付けたいとき。

## 向いていない場面

- データを日本に置くことが条件の案件 (地域を選べない)。
- 自治体や企業の SSO 接続が多い B2B (接続数で課金が増える)。

## 出典

- https://clerk.com/pricing : MRU、Pro の価格と超過料金、SSO 接続、組織の追加、パスキーのプラン (2026-11-11)。
- https://clerk.com/security.md : データ所在地を選べないこと、米国のインフラ、SOC 2 (2026-11-11)。
- https://clerk.com/docs/guides/sessions/manual-jwt-verification : JWKS、`azp` (2026-11-11)。
- https://clerk.com/docs/guides/development/migrating/overview : 書き出しと取り込み (2026-11-11)。
- https://clerk.com/docs/guides/configure/auth-strategies/social-connections/line : LINE (ページの存在を確認)。

## 未確認のこと

- MRU の正確な定義 (どの利用者が数えられるか)。
- セッショントークンの寿命。
- MFA のプランの差、日本語の画面。
- 取り込める `password_hasher` の一覧。
- ISMAP の登録の有無。
