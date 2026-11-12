# Supabase Auth

対象: Supabase の認証 (Supabase Auth、旧 GoTrue) と、PostgreSQL の RLS との組み合わせ

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | Supabase, Inc. |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | 両方。管理型の Supabase と、OSS を自前で運用 |
| ライセンス (OSS の場合) | 認証サーバー supabase/auth は MIT (最新 v2.197.0、2026-09-09)。supabase/supabase のモノレポは Apache-2.0。`@supabase/supabase-js` 2.119.0 は MIT (`gh api`、npm で確認) |
| 料金ページ | https://supabase.com/pricing |
| ドキュメント | https://supabase.com/docs/guides/auth |

## 概要

Supabase Auth は Supabase のプロジェクトの PostgreSQL に利用者を `auth` スキーマとして持ち、発行する JWT をそのまま PostgreSQL の RLS で使える。地図の地物を PostGIS に置き、利用者や組織ごとに見える行を DB 側で決める構成に向く。RLS、PostgREST、Free の休止については geo-software-arch の [source-of-truth](../../../geo-software-arch/references/capabilities/source-of-truth.md) にあり、ここでは繰り返さない。

## 料金と無料枠

- 課金単位と無料枠: MAU。Free は 50,000 MAU、第三者の認証 (Third-party MAU) も 50,000 まで含む。Free のプロジェクトは 1 週間使われないと止まり、Free の組織で動かせるのは 2 プロジェクトまで (https://supabase.com/pricing、2026-11-11)。
- 有料プランの最低額と、主な機能が入るプラン: Pro は月 25 ドルから。100,000 MAU を含み、超過は 1 MAU 0.00325 ドル。有料プランは使われなくても止まらない (同上)。
- SSO (SAML) や組織機能の追加料金: SAML 2.0 は Pro 以上 (Team も) で、50 MAU を含み超過は 1 MAU 0.015 ドル。電話の MFA は最初のプロジェクトで月 75 ドル、追加のプロジェクトごとに月 10 ドル (https://supabase.com/pricing、 https://supabase.com/docs/guides/auth/enterprise-sso/auth-sso-saml、2026-11-11)。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 対応 | 詳細は未確認 |
| ソーシャルログイン (Google、Apple、LINE など) | 対応 | 標準は Apple、Azure、Bitbucket、Discord、Facebook、Figma、GitHub、GitLab、Google、Kakao、Keycloak、LinkedIn、Notion、Slack、Spotify、Twitter、Twitch、WorkOS、Zoom。LINE は標準にない。一覧にないものは Custom OAuth/OIDC Providers で足す (https://supabase.com/docs/guides/auth/social-login、2026-11-11) |
| パスキー | 実験的 | 2026-05-28 にベータとして公開。文書は「experimental、API は予告なく変わりうる」としている (https://supabase.com/docs/guides/auth/passkeys、2026-11-11) |
| MFA | 対応 | 電話の MFA は有料の追加 (上記)。他の方式の詳細は未確認 |
| SAML / OIDC による企業 SSO | Pro 以上 | SAML 2.0。CLI で IdP を管理する |
| 組織・テナントと役割 (RBAC) | 組み込みの組織機能は未確認 | 組織や役割は自分のテーブルと RLS で作る (推測) |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | 強い | RLS で `auth.uid()`、`auth.jwt()` を使える (source-of-truth 参照)。非対称の署名鍵 (RSA か楕円曲線) の公開鍵を `/auth/v1/.well-known/jwks.json` で公開する。旧来の HS256 の共有鍵は本番に勧めていない。JWKS はエッジで約 10 分キャッシュされる (https://supabase.com/docs/guides/auth/signing-keys、2026-11-11) |
| 日本語の画面 | 該当なし | ログイン画面はアプリ側で作る (推測) |
| データの保存地域 (日本リージョン) | 東京を選べる | 「Specific regions」に Northeast Asia (Tokyo) `ap-northeast-1` がある (https://supabase.com/docs/guides/platform/regions、2026-11-11) |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: 地物を PostGIS に置くなら、RLS で行を絞った結果を API (PostgREST、Edge Functions) から返す。タイルやファイルは Storage の署名付き URL (`createSignedUrl(path, expiresIn)`、秒単位) で期限付きに出せる (https://supabase.com/docs/reference/javascript/storage-from-createsignedurl、2026-11-11)。Storage は `storage.objects` の RLS がないとアップロードできない (https://supabase.com/docs/guides/storage/security/access-control)。手段の比較は [tile-access-control](../tile-access-control.md)。
- エッジ関数やサーバーレスで動くか: JWKS で検証できるので、Supabase 以外のエッジ (Cloudflare Workers など) でも検証できる (推測)。エッジ関数の制約は [edge-functions](../../../geo-software-arch/references/edge/edge-functions.md)。

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: ISMAP の登録は未確認。閉域網では OSS を自前で運用する案になる (推測)。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): 利用者は自分のプロジェクトの PostgreSQL の `auth` スキーマにあるので、DB のダンプで持ち出せる (推測。ハッシュの形式は未確認)。
- 他の提供者からの取り込み: 未確認。
- RLS のポリシーが `auth.uid()` などの Supabase の関数に依存すると、移行時に書き換えが要る (source-of-truth の記述)。

## ライセンス上の注意

- supabase/auth は MIT、モノレポは Apache-2.0。いずれもコピーレフトではないので、自前で運用、改変、配布、SaaS 提供しても、著作権表示とライセンス文 (Apache-2.0 では NOTICE と改変の明示も) を残せばよい。管理型の Supabase は同社の規約による。

## 向いている場面

- 地物を PostGIS に置き、利用者や自治体ごとに見える行を DB で強制したいとき。
- データを東京リージョンに置きたいとき。
- 将来 OSS で自前運用に移れる余地を残したいとき。

## 向いていない場面

- 使う時期が飛び飛びのサービスを Free で動かすとき (1 週間で止まる)。
- パスキーを本番の主たる手段にしたいとき (実験的)。
- 組み込みの組織と役割の管理画面が要る B2B。

## 出典

- https://supabase.com/pricing : MAU、超過単価、SAML、電話 MFA、Free の休止 (2026-11-11)。
- https://supabase.com/docs/guides/auth/social-login : ソーシャルの一覧と独自 OIDC (2026-11-11)。
- https://supabase.com/docs/guides/auth/passkeys : パスキーが実験的であること (2026-11-11)。
- https://supabase.com/docs/guides/auth/signing-keys : 非対称鍵、JWKS の場所とキャッシュ (2026-11-11)。
- https://supabase.com/docs/guides/platform/regions : 東京リージョン (2026-11-11)。
- https://supabase.com/docs/guides/auth/enterprise-sso/auth-sso-saml : SAML は Pro 以上 (2026-11-11)。

## 未確認のこと

- パスワードハッシュの形式と、他の提供者からハッシュごと取り込めるか。
- 組み込みの組織機能の有無。
- ISMAP の登録の有無。
- パスキーの正式提供の時期。
