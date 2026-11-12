# Auth0

対象: Okta の Auth0 (パブリッククラウドの管理型サービス)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | Okta, Inc. |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | 管理型サービス。専用環境の Private Cloud もある |
| ライセンス (OSS の場合) | サービス本体は OSS ではない。SDK は OSS (例: `@auth0/nextjs-auth0` 4.33.0 は MIT、npm で確認) |
| 料金ページ | https://auth0.com/pricing |
| ドキュメント | https://auth0.com/docs |

## 概要

Auth0 は認証と認可を API とホスト型のログイン画面で提供する管理型サービスである。B2C 向けと B2B 向けで料金表が分かれ、B2B 向けでは組織 (Organizations) と企業 SSO の接続数が増える。テナントを作るときに地域 (locality) を選び、日本 (JP) を選べる。

## 料金と無料枠

- 課金単位と無料枠: MAU。Free は 25,000 MAU まで 0 ドル。Free にはカスタムドメイン 1、パスワードレス、ソーシャル接続無制限、組織 5、企業接続 (Enterprise Connection) 1、セルフサービス SSO、SCIM が入る (https://auth0.com/pricing、2026-11-11)。
- 有料プランの最低額と、主な機能が入るプラン: Essentials は B2C 月 35 ドル、B2B 月 150 ドル。Professional は B2C 月 240 ドル、B2B 月 800 ドル。いずれも表示価格は 500 MAU のとき。Enterprise は見積もり (https://auth0.com/pricing、2026-11-11)。
- SSO (SAML) や組織機能の追加料金: B2B Essentials は企業接続 3、B2B Professional は 5 を含み、追加は 1 接続月 100 ドル (年 1,100 ドル)、合計 30 まで。組織は B2C の有料プランで 10、B2B の有料プランで無制限 (システムの上限あり)。B2C の有料プランでの企業接続は料金表で「Not available」とされる一方、追加機能の一覧に企業 SSO 接続があり、扱いは未確認 (https://auth0.com/pricing、2026-11-11)。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 対応 | パスワードレスは Free から (料金ページ) |
| ソーシャルログイン (Google、Apple、LINE など) | 対応 | ソーシャル接続は Free から無制限。LINE は Marketplace の統合として掲載がある (https://marketplace.auth0.com/integrations/line-social-connection、2026-11-11 にページの存在だけ確認、中身は未確認) |
| パスキー | 対応 | 全プラン (料金ページ、2026-11-11) |
| MFA | 対応 | プランごとの差は未確認 |
| SAML / OIDC による企業 SSO | 対応 | 接続数はプランで決まる (上記) |
| 組織・テナントと役割 (RBAC) | 対応 | Organizations (https://auth0.com/docs/manage-users/organizations) |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | JWT を発行する | アクセストークンを JWKS で検証できる (https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-key-sets)。PostgreSQL の RLS へ渡すには、JWT のクレームを DB に渡す層 (PostgREST など) が別に要る (推測) |
| 日本語の画面 | 未確認 | 日本語のドキュメント (https://auth0.com/docs/ja-jp/) はある。ログイン画面の日本語化は未確認 |
| データの保存地域 (日本リージョン) | JP を選べる | パブリッククラウドの locality に AU、CA、EU、JP、UK、US がある (https://auth0.com/docs/get-started/auth0-overview/create-tenants.md、2026-11-11)。作成後に地域を変えられるかは文書に記載がなく未確認 |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: Auth0 のアクセストークン (JWT) を、地図ライブラリのリクエストに付けてエッジ関数で検証する形になる。手段は [tile-access-control](../tile-access-control.md)。
- エッジ関数やサーバーレスで動くか: JWKS と標準の JWT ライブラリ (例: jose) で検証できるので、Web Crypto のある実行環境なら検証できる (推測)。各 SDK の対応ランタイムは未確認。

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: ISMAP クラウドサービスリストでの登録の有無は未確認 (ポータルの一覧が JavaScript で描かれ、取得できなかった)。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): API では書き出せず、サポートへの依頼で出せる。Free では依頼できず、日時の保証もない (https://auth0.com/docs/troubleshoot/customer-support/manage-subscriptions/export-data、2026-11-11)。
- 他の提供者からの取り込み: 一括取り込みで `custom_password_hash` を受ける。対応しないアルゴリズムの利用者は初回ログインでパスワードの再設定が要る (https://auth0.com/docs/manage-users/user-migration/bulk-user-imports、2026-11-11)。外部のユーザーストアからログイン時に移す自動移行もある (詳細は未確認)。

## ライセンス上の注意

- サービス本体は商用サービスで、利用条件は Okta の利用規約による。SDK は MIT なので、組み込み、改変、配布、SaaS のいずれでも著作権表示とライセンス文を残せばよい。

## 向いている場面

- B2B で、顧客の組織ごとに企業 SSO を付けたいとき。
- 管理型で、日本の地域にテナントを置きたいとき。
- 無料枠 25,000 MAU で始め、パスキーを最初から使いたいとき。

## 向いていない場面

- 企業接続が多い B2B で費用を抑えたいとき (1 接続月 100 ドルの追加)。
- パスワードのハッシュを自分で持ち出せることを条件にする案件 (書き出しはサポート経由)。

## 出典

- https://auth0.com/pricing : 無料枠、プラン価格、企業接続、組織、パスキー (2026-11-11)。
- https://auth0.com/docs/get-started/auth0-overview/create-tenants.md : パブリッククラウドの地域 (2026-11-11)。
- https://auth0.com/docs/troubleshoot/customer-support/manage-subscriptions/export-data : パスワードハッシュの書き出し条件 (2026-11-11)。
- https://auth0.com/docs/manage-users/user-migration/bulk-user-imports : 一括取り込み (2026-11-11)。
- https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-key-sets : JWKS (ページの存在を確認)。

## 未確認のこと

- ISMAP の登録の有無。
- テナントの地域を作成後に変えられるか。
- LINE 統合の提供者と条件。
- ログイン画面の日本語化の範囲。
- B2C の有料プランで企業 SSO 接続を追加できるか。
