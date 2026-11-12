# Keycloak

対象: OSS の IAM サーバー Keycloak を自前で運用する場合

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | Keycloak プロジェクト (CNCF のプロジェクト。運営体制の詳細は未確認) |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | OSS を自前で運用。本家の管理型サービスはない (第三者のホスティングは調べていない) |
| ライセンス (OSS の場合) | Apache-2.0 (`gh api repos/keycloak/keycloak/license`、LICENSE.txt)。最新は 26.8.2 (2026-11-05)。JS アダプタ `keycloak-js` 26.2.5 も Apache-2.0 (npm) |
| 料金ページ | なし (OSS) |
| ドキュメント | https://www.keycloak.org/documentation |

## 概要

Keycloak は Java で動く IAM サーバーで、OIDC と SAML の IdP になり、外部の IdP (Google、企業の SAML) とも連携する。realm ごとに利用者、クライアント、役割を分け、組織 (Organizations) の機能もある。自治体や企業の既存の SAML 基盤と組み合わせる、閉域網に置く、といった要件に向く。

## 料金と無料枠

- 課金単位と無料枠: ソフトウェアの利用料はない。費用はサーバーと DB、運用の人手。
- 有料プランの最低額と、主な機能が入るプラン: 該当なし。商用のサポートは別の事業者が出している (未確認)。
- SSO (SAML) や組織機能の追加料金: なし。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 対応 | パスワード、パスキー、X.509 証明書 (サーバー管理ガイドの機能一覧) |
| ソーシャルログイン (Google、Apple、LINE など) | 対応 | 組み込みは Bitbucket、Facebook、GitHub、GitLab、Google、Instagram、LinkedIn、Microsoft、OpenShift 4、PayPal、Stack Overflow、Twitter。LINE と Apple は組み込みにない。一般の OIDC の IdP として足す形になる (推測) (https://www.keycloak.org/docs/latest/server_admin/index.html、2026-11-11) |
| パスキー | 対応 | 23.0.0 からプレビュー、26.4.0 で正式対応。WebAuthn Passwordless Policy で有効にする (https://www.keycloak.org/2025/09/passkeys-support-26-4、2026-11-11) |
| MFA | 対応 | OTP、WebAuthn (詳細は未確認) |
| SAML / OIDC による企業 SSO | 対応 | IdP としても、外部 IdP の仲介としても |
| 組織・テナントと役割 (RBAC) | 対応 | realm と役割、Organizations (ドメインで組織に振り分ける機能を含む、サーバー管理ガイド) |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | JWT を発行する | OIDC のアクセストークン。RLS へは PostgREST など JWT のクレームを DB に渡す層を使う (推測) |
| 日本語の画面 | 未確認 | |
| データの保存地域 (日本リージョン) | 自分で決める | 自前で運用する場所に置かれる |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: アクセストークンをタイルのリクエストに付け、エッジかタイルサーバーの前段で JWKS により検証する。手段は [tile-access-control](../tile-access-control.md)。
- エッジ関数やサーバーレスで動くか: Keycloak 本体は常時動くサーバーで、エッジでは動かない (推測)。トークンの検証だけならエッジでできる (推測)。

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: ソフトウェアなので ISMAP の対象ではない。動かす基盤の登録で判断する (推測)。閉域網や LGWAN の中に置ける (推測。LGWAN の条件は [niche](../niche.md))。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): DB は自分で持つので持ち出せる (推測)。パスワードのハッシュは argon2 (FIPS でない既定)、pbkdf2-sha512 (FIPS の既定)、pbkdf2-sha256、pbkdf2 (SHA1、非推奨) (サーバー管理ガイド、2026-11-11)。realm の書き出しの手順は未確認。
- 他の提供者からの取り込み: 未確認。他社のハッシュ形式を受けるには拡張 (SPI) が要る場合がある (推測)。

## ライセンス上の注意

- Apache-2.0。自前で運用 (SaaS として提供) する、改変する、配布する、のいずれでもソースの公開義務はない。配布するときはライセンス文と NOTICE を添え、改変したファイルに改変した旨を書く (Apache-2.0 の第 4 条)。特許の許諾があり、特許訴訟を起こすとその許諾が終わる (第 3 条)。

## 向いている場面

- 自治体や企業の既存の SAML や AD と連携する、公共や受託の案件。
- 閉域網、オンプレ、データを自分のサーバーに置くことが条件のとき。
- MAU の課金を避けたいとき。

## 向いていない場面

- 運用の人手がない小さなチーム (Java のサーバーと DB の更新、脆弱性の対応)。
- LINE や Apple のログインを組み込みの設定だけで付けたいとき。

## 出典

- https://github.com/keycloak/keycloak : LICENSE.txt (Apache-2.0)、リリース 26.8.2 (2026-11-05)。
- https://www.keycloak.org/docs/latest/server_admin/index.html : 組み込みのソーシャル IdP、Organizations、パスワードハッシュ (2026-11-11)。
- https://www.keycloak.org/2025/09/passkeys-support-26-4 : パスキーの正式対応 (2026-11-11)。

## 未確認のこと

- 日本語の画面の範囲。
- realm の書き出しにパスワードハッシュが入るか、他社のハッシュの取り込み。
- 商用サポートの提供者と費用。
- 必要なサーバーの大きさ (geo-software-poc-measure で測る)。
