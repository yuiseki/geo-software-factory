# Neon Auth

対象: Neon Auth (Neon の Postgres に付いた管理型の認証。文書での名前は Managed Better Auth)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-12 |
| 提供者 | Neon (料金ページは「from Databricks」と書く) |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | 管理型サービス。中身は OSS の Better Auth 1.7.12 を Neon が動かしたもの (https://neon.com/docs/auth/about、2026-11-12) |
| ライセンス (OSS の場合) | サービス本体は Neon の規約による。SDK の `@neon/auth` 0.8.2、旧名の `@neondatabase/auth` 0.7.0-beta と `@neondatabase/neon-js` 0.9.0-beta は Apache-2.0 (npm、2026-11-12)。中の Better Auth は MIT ([better-auth](better-auth.md)) |
| 料金ページ | https://neon.com/pricing |
| ドキュメント | https://neon.com/docs/auth/overview |

## 概要

Neon Auth は、Neon の Postgres のプロジェクトに付く管理型の認証である。利用者、セッション、OAuth の設定は、自分の Neon のデータベースの `neon_auth` スキーマに入る (https://neon.com/docs/auth/overview、2026-11-12)。中身は Better Auth で、Neon がサーバーを動かすので、Better Auth を自前で運用する手間は要らない。以前の Neon Auth は Stack Auth を使っており、旧版から移る手順が別にある (https://neon.com/docs/auth/about、2026-11-12)。認証だけを使うことはできず、Neon の Postgres のプロジェクトが前提になる。

## 料金と無料枠

- 課金単位と無料枠: MAU (請求の月に 1 回以上認証した利用者)。Free は 1 プロジェクト 60,000 MAU まで (https://neon.com/docs/auth/about、2026-11-12)。
- 有料プランの最低額と、主な機能が入るプラン: Launch と Scale は 1 プロジェクト 100 万 MAU まで。それを超えるときはコンソールのフォームで申し込む。認証は別料金を取らない (「Managed Better Auth, the Data API, and Realtime have no separate charge」、https://neon.com/pricing、2026-11-12)。費用は Postgres の計算と保存で、Launch は 1 CU 時間 0.106 ドル、Scale は 0.222 ドル、保存は 1 GB 月 0.35 ドル。Launch と Scale に月の最低額は無い (同上)。
- Free の条件: 計算は 1 プロジェクト月 100 CU 時間。5 分使われないと計算が止まり (Free では切れない)、次のリクエストで起きる。使われないことを理由にプロジェクトを止めることはしない。月の 100 CU 時間か転送 5 GB を使い切ると、次の請求の月まで止まる。保存は 1 プロジェクト 1 GB (https://neon.com/pricing、2026-11-12)。
- SSO (SAML) や組織機能の追加料金: SAML は文書に記載が無い。組織は追加料金の記載が無い。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 対応 | メールのリンク、メールの OTP、電話番号も対応 (https://neon.com/docs/auth/roadmap、2026-11-12)。共用の送信元は送る数が絞られ、本番では自分の SMTP を設定するよう求めている (https://neon.com/docs/auth/production-checklist) |
| ソーシャルログイン (Google、Apple、LINE など) | Google、GitHub、Vercel、Microsoft、Apple | Google は Neon の共用の資格情報で最初から使える。同意の画面には Neon の名前が出る。本番では自分の Google のクライアント ID とシークレットを入れる。他の 4 つは最初から自分の資格情報が要る (https://neon.com/docs/auth/guides/setup-oauth、2026-11-12)。LINE は記載が無い |
| パスキー | 記載なし | ロードマップにも無い |
| MFA | 未対応 | ロードマップで「Coming soon」 |
| SAML / OIDC による企業 SSO | 記載なし | |
| 組織・テナントと役割 (RBAC) | 一部 | Organization プラグインが「Partial」。JWT の `o` クレームに owner、admin、member の役割が入る (https://neon.com/docs/auth/guides/plugins/jwt、2026-11-12) |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | 対応 | ブラウザは HTTP only の Cookie を使い、生の JWT は `authClient.getSession()` で取れる。JWKS は `<認証の URL>/.well-known/jwks.json`、署名は EdDSA (Ed25519)、寿命は 15 分、独自のクレームは付けられない (同上)。Neon の Data API は JWT の `role` (`authenticated`) で DB のロールを切り替え、RLS の方針では `auth.user_id()` で `sub` を読む (https://neon.com/docs/data-api/access-control、2026-11-12) |
| 日本語の画面 | 未確認 | |
| データの保存地域 (日本リージョン) | 日本は無い | 認証はデータベースと同じリージョンに置かれる。AWS のリージョンだけで、Azure はまだ。アジアは Singapore (`aws-ap-southeast-1`) と Sydney (`aws-ap-southeast-2`) で、Tokyo は一覧に無い。Sydney では Managed Better Auth は使える (https://neon.com/docs/introduction/regions、2026-11-12) |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: 地物を Neon の PostGIS に置き、Data API と RLS で利用者ごとに出し分けられる。タイルの配信は、JWT を JWKS で検証する形になる。寿命が 15 分なので、地図ライブラリの `transformRequest` で毎回 `getSession()` から新しいトークンを付ける必要がある (推測)。手段は [tile-access-control](../tile-access-control.md)。
- エッジ関数やサーバーレスで動くか: JWKS と Ed25519 による検証は Web Crypto でできる (推測)。フロントエンドとバックエンドを別々のドメインに置く構成はまだ対応していない (「Standalone frontend + backend」が「Coming soon」、https://neon.com/docs/auth/roadmap、2026-11-12)。IP Allow や Private Networking を有効にしたプロジェクトでは使えない (https://neon.com/docs/auth/about)。
- 2026-03 の試作 (Cloudflare Workers と React Router 7 で Google ログインと PostGIS) で分かったこと。当時の版は `@neondatabase/neon-js` 0.2.0-beta で、今は名前と版が変わっている:
  - Workers では Next.js 向けの `@neondatabase/auth` が使えず、`@neondatabase/neon-js` を使った
  - 認証の部品は `window` に頼るので、SSR の中では import できず、ブラウザで動的に import した
  - 許可するオリジン (Trusted Origins) に末尾のスラッシュを付けると `403 Invalid origin` になった
  - 本番では「Allow Localhost」(既定で有効) を切るよう、本番の確認項目にある (https://neon.com/docs/auth/production-checklist)

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: 未確認。データは日本の外 (最も近いのは Singapore) に置かれるので、個人情報を外国にある第三者に渡す扱いになりうる (推測。条文は geo-software-legal-check の [location-privacy](../../../geo-software-legal-check/references/location-privacy.md) の第 28 条)。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): 利用者は自分のデータベースの `neon_auth` スキーマにあるので、SQL で読める (推測。ハッシュの列と形式は未確認)。中身が Better Auth なので、自前の Better Auth に移るのは他の管理型より近い (推測)。
- 他の提供者からの取り込み: 旧 Neon Auth (Stack Auth) からの移行手順がある (https://neon.com/docs/auth/migrate/from-legacy-auth、ページは開いていない)。他の提供者からは未確認。

## ライセンス上の注意

- サービスは Neon の規約による (規約本文は未確認)。SDK は Apache-2.0 なので、組み込みや配布では著作権表示とライセンス文を残し、改変したファイルには改変の旨を書く (Apache-2.0 の条文から)。

## 向いている場面

- 正本の DB を Neon の Postgres と PostGIS にし、利用者ごとの出し分けを RLS で DB に任せたいとき。
- Google ログインを、資格情報を作らずに試作で付けたいとき (共用の資格情報)。
- 認証に別料金を払わず、60,000 MAU まで無料で始めたいとき。

## 向いていない場面

- 正本の DB が Neon 以外 (D1、R2 のファイルなど) のとき。認証のためだけに Neon のプロジェクトを持つことになる。
- データを日本に置くことが条件の案件 (Tokyo のリージョンが無い)。
- MFA、パスキー、SAML が必須のとき。LINE ログインが要るとき。
- フロントエンドとバックエンドを別のドメインに置く構成。

## 出典

- https://neon.com/docs/auth/overview : `neon_auth` スキーマ (2026-11-12)。
- https://neon.com/docs/auth/about : Better Auth 1.7.12、MAU と各プランの上限、同じリージョン、AWS のみ、IP Allow と Private Networking (2026-11-12)。
- https://neon.com/pricing : 認証に別料金なし、計算と保存の単価、Free の条件 (2026-11-12)。
- https://neon.com/docs/auth/guides/setup-oauth : 対応するソーシャルログイン、Google の共用の資格情報、本番の設定、許可するオリジン (2026-11-12)。
- https://neon.com/docs/auth/roadmap : 一般提供、対応と未対応の機能 (2026-11-12)。
- https://neon.com/docs/auth/guides/plugins/jwt : JWKS、EdDSA、15 分、組織の役割のクレーム (2026-11-12)。
- https://neon.com/docs/data-api/access-control : `role` と `auth.user_id()` (2026-11-12)。
- https://neon.com/docs/introduction/regions : リージョンの一覧と Managed Better Auth の対応 (2026-11-12)。
- https://neon.com/docs/auth/production-checklist : SMTP、Allow Localhost、メールの確認 (2026-11-12)。

## 未確認のこと

- 一般提供になった日。
- パスキー、SAML の予定。
- `neon_auth` スキーマのパスワードのハッシュの形式と、書き出しの手順。
- 共用の Google の資格情報に、人数や回数の上限があるか。
- 日本語の画面、ISMAP の登録、規約本文。
