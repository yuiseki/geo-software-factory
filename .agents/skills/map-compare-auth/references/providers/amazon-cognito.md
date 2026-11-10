# Amazon Cognito

対象: AWS の Amazon Cognito のユーザープール (機能プラン Lite、Essentials、Plus)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | Amazon Web Services |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | 管理型サービスのみ (リージョンごと) |
| ライセンス (OSS の場合) | サービス本体は OSS ではない。検証用の `aws-jwt-verify` 5.2.1 は Apache-2.0 (npm、`gh api`) |
| 料金ページ | https://aws.amazon.com/cognito/pricing/ |
| ドキュメント | https://docs.aws.amazon.com/cognito/latest/developerguide/ |

## 概要

Cognito はユーザープール (利用者の台帳と OIDC の発行者) を AWS のリージョンに作る管理型サービスである。ユーザープールごとに機能プラン (Lite、Essentials、Plus) を選び、新しいプールの既定は Essentials である。東京リージョンに置けるので、AWS で地図の配信 (CloudFront、S3) を組む案件と相性がよい。

## 料金と無料枠

- 課金単位と無料枠: MAU (直接ログインと、SAML/OIDC の連携で別々)。Lite と Essentials は直接ログイン 10,000 MAU が毎月無料で、AWS の 12 か月の無料期間が過ぎても切れない。Plus は無料枠なし。SAML/OIDC の連携は 50 MAU が無料。GovCloud では無料枠なし (https://aws.amazon.com/cognito/pricing/、2026-11-11)。
- 有料プランの単価: Lite は 1 MAU 0.0055 ドル (料金ページの例では 90,000 MAU を超えると 0.0046 ドル)、Essentials は 0.015 ドル、Plus は 0.020 ドル。SAML/OIDC の連携は 50 MAU を超えて 1 MAU 0.015 ドル (同上)。
- 古いプールの扱い: 2024-11-22 以前に作った Lite のプールは最初の 50,000 MAU が無料のままと料金ページにあり、同じページの 10,000 MAU の記述と食い違う。自分のプールにどちらが当たるかは確かめる (同上)。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 対応 | メールか SMS の OTP を第 1 要素にするパスワードレスは Essentials と Plus (https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sign-in-feature-plans.html、2026-11-11) |
| ソーシャルログイン (Google、Apple、LINE など) | 対応 | ソーシャル、SAML、OIDC は全プラン。LINE は OIDC の IdP として足す形になる (推測、未確認) |
| パスキー | Essentials と Plus | FIDO2 の認証器を第 1 要素にできる。Lite にはない (同上) |
| MFA | 対応 | 認証アプリと SMS は全プラン、メールの MFA は Essentials と Plus (同上) |
| SAML / OIDC による企業 SSO | 対応 | 連携 MAU で課金 |
| 組織・テナントと役割 (RBAC) | 一部 | ユーザーグループは全プラン。組織 (B2B のテナント) の機能は未確認 |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | JWT を発行する | RS256、JWKS は `https://cognito-idp.<Region>.amazonaws.com/<userPoolId>/.well-known/jwks.json`。`token_use` を確かめる。署名と期限の確認だけでは失効 (サインアウト、RevokeToken) を見抜けない (https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html、2026-11-11)。アクセストークンのクレームの変更は Essentials と Plus |
| 日本語の画面 | 未確認 | |
| データの保存地域 (日本リージョン) | 対応 | ユーザープールはリージョンに作る。東京 (ap-northeast-1) で使えるかは AWS のリージョン表で確かめていない (未確認、推測では使える) |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: CloudFront の署名付き URL か署名付き Cookie を、Cognito でログインした利用者だけに発行する形が組める (推測)。API Gateway の JWT オーソライザーに Cognito を指定できる (検証の文書の注記)。手段は [tile-access-control](../tile-access-control.md)。
- エッジ関数やサーバーレスで動くか: `aws-jwt-verify` で Lambda や Node.js で検証できる。CloudFront Functions はネットワークに触れないので、JWKS を取りに行けない ([edge-functions](../../../map-compare-arch/references/edge/edge-functions.md))。

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: AWS は ISMAP に登録されており、「AWS 全体が対象」と AWS は書いている。個別のサービスとリージョンはポータルと「Services in Scope」で確かめるよう案内している (https://aws.amazon.com/jp/compliance/ismap/、2026-11-11)。Cognito が一覧に載っているかはポータルで確かめていない (未確認)。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): パスワードを取り出せる形で持たないので書き出せない、と AWS のブログとフォーラムの回答にある (公式文書の条文では未確認)。プロフィールは ListUsers で出せる。
- 他の提供者からの取り込み: ログイン時に移すユーザー移行の Lambda トリガー (既存のパスワードのまま移れる) と、CSV の一括取り込みがある (https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-import-users.html、2026-11-11)。CSV でハッシュを取り込めるかは未確認。

## ライセンス上の注意

- サービス本体は AWS の規約による。`aws-jwt-verify` は Apache-2.0 で、組み込み、配布するなら NOTICE とライセンス文を残す。

## 向いている場面

- AWS (CloudFront、S3、API Gateway) で地図とデータを配る案件。
- データを日本のリージョンに置きたい、公共案件で ISMAP 登録のクラウドに寄せたいとき。
- 10,000 MAU 以下の小さな利用で、パスキーも使いたいとき (Essentials)。

## 向いていない場面

- 将来ほかの提供者へ、パスワードを保ったまま一度に移りたいとき (ハッシュを出せない)。
- 組織ごとの管理画面が要る B2B。

## 出典

- https://aws.amazon.com/cognito/pricing/ : プランごとの単価と無料枠、古いプールの扱い (2026-11-11)。
- https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sign-in-feature-plans.html : 機能とプランの表、既定は Essentials (2026-11-11)。
- https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html : JWT の検証、JWKS、失効 (2026-11-11)。
- https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-import-users.html : 取り込みの 2 つの方法 (2026-11-11)。
- https://aws.amazon.com/jp/compliance/ismap/ : ISMAP (2026-11-11)。

## 未確認のこと

- ISMAP のポータルで Cognito が対象に載っているか。
- 東京リージョンでの提供 (リージョン表)。
- CSV の一括取り込みでパスワードハッシュを受けるか。
- 古い Lite プールの無料枠 (50,000 か 10,000 か)。
- 日本語の画面、LINE の OIDC 連携の可否。
