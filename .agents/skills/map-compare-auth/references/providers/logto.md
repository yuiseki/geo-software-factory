# Logto

対象: Logto の OSS 版 (自前で運用) と Logto Cloud (管理型)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | Silverhand, Inc. (未確認。リポジトリは logto-io/logto) |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | 両方 |
| ライセンス (OSS の場合) | MPL-2.0 (`gh api repos/logto-io/logto/license`、LICENSE)。最新は v1.46.0 (2026-11-05)。SDK `@logto/node` 4.0.2 は MIT (npm) |
| 料金ページ | https://logto.io/pricing |
| ドキュメント | https://docs.logto.io |

## 概要

Logto は OIDC を基にした認証と認可の基盤で、OSS 版を PostgreSQL と Node.js で自前で運用するか、Logto Cloud を使う。Logto Cloud には日本 (Japan East) の地域がある。OSS 版には Cloud だけの機能があり、一部は自前運用向けの有料ライセンスで開く。

## 料金と無料枠

- 課金単位と無料枠: Free は 50,000 MAU まで、トークン 50K を含む (https://logto.io/pricing、2026-11-11)。
- 有料プランの最低額と、主な機能が入るプラン: Pro は月 24 ドルから。MAU とアプリ数は無制限で、トークン 50K を超えた分は 100 トークンごとに 0.08 ドル (同上)。トークンの数え方の詳細は未確認。
- SSO (SAML) や組織機能の追加料金: 企業 SSO は 1 コネクタ 48 ドル、組織は 48 ドルの追加 (いずれも Pro の追加。月額かは未確認)。Enterprise はデータの地域を指定できる (同上)。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 対応 | 詳細は未確認 |
| ソーシャルログイン (Google、Apple、LINE など) | 対応 | 公式の LINE コネクタがある (https://docs.logto.io/integrations/line、2026-11-11) |
| パスキー | 対応 | 第 1 要素のパスキーログインの文書がある (https://docs.logto.io/end-user-flows/sign-up-and-sign-in/passkey-sign-in、2026-11-11)。OSS 版で使えるかは文書に記載がなく未確認 |
| MFA | 対応 | WebAuthn の MFA (https://docs.logto.io/end-user-flows/mfa/webauthn、ページの存在を確認) |
| SAML / OIDC による企業 SSO | 対応 | Cloud では追加料金。OSS では IdP 起点の SSO が Cloud だけ (下記) |
| 組織・テナントと役割 (RBAC) | 対応 | 組織と RBAC (https://docs.logto.io/authorization/role-based-access-control) |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | JWT を発行する | OIDC のアクセストークン。RLS へは JWT のクレームを DB に渡す層が要る (推測) |
| 日本語の画面 | 未確認 | |
| データの保存地域 (日本リージョン) | Cloud で日本を選べる | 2025-04-22 に Japan (Japan East) を一般提供。他は Europe (Netherlands)、West US (Arizona)、Australia (Australia East)。地域はテナントを作るときに選ぶ (https://blog.logto.io/announcing-japan-region、2026-11-11) |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: アクセストークンをタイルのリクエストに付け、エッジで JWKS により検証する (推測)。手段は [tile-access-control](../tile-access-control.md)。
- エッジ関数やサーバーレスで動くか: OSS 版は PostgreSQL の要る常時動くサーバー (README の「Using Node.js (requires PostgreSQL)」)。トークンの検証だけならエッジでできる (推測)。

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: Logto Cloud の ISMAP 登録は未確認。OSS 版は動かす基盤で判断する (推測)。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): OSS 版は自分の PostgreSQL にあるので持ち出せる (推測)。Cloud からの書き出しは未確認。
- 他の提供者からの取り込み: 未確認。
- OSS 版で Cloud だけの機能: コンソールの複数テナント、共同編集者の招待、コンソールの MFA、Logto Protected App、組み込みのメール送信、Bring your UI、IdP 起点の SSO、SAML アプリ (OSS は 3 つまで)、Logto のロゴを隠す。このうち招待、コンソールの MFA の強制、Bring your UI、ロゴを隠す、SAML アプリ無制限は自前運用向けの有料ライセンスで開く (https://docs.logto.io/logto-oss、2026-11-11)。

## ライセンス上の注意

- MPL-2.0 はファイル単位の弱いコピーレフトである (条文から)。
- 改変せずに自前で運用する: 追加の義務は生じない (推測)。
- Logto のソースファイルを改変して配布する (ソフトウェアとして渡す、受託で納品する): 改変したファイルを MPL-2.0 のまま、ソースを入手できる形で渡す (第 3.1 条、3.2 条)。自社のコードを別のファイルに置けば、そのファイルは MPL-2.0 にしなくてよい (第 3.3 条の「Larger Work」)。
- 改変して SaaS として提供するだけ (配布しない): MPL-2.0 にはネットワーク越しの利用者へのソース提供の条項がないので、ソースの提供義務は生じない (推測。AGPL とは違う)。
- SDK は MIT で、アプリに組み込んでも著作権表示とライセンス文を残せばよい。

## 向いている場面

- 管理型でデータを日本に置き、LINE ログインと組織、RBAC が要るとき。
- 将来 OSS 版の自前運用に移れる余地を残したいとき。

## 向いていない場面

- OSS 版で、IdP 起点の SSO や SAML アプリを多数使いたいとき (Cloud か有料ライセンス)。
- トークン数の課金が読みにくい、タイルごとにトークンを発行する構成 (推測。数え方を確かめてから)。

## 出典

- https://github.com/logto-io/logto : LICENSE (MPL-2.0)、README、リリース v1.46.0。
- https://logto.io/pricing : Free と Pro、トークン、企業 SSO と組織の追加 (2026-11-11)。
- https://blog.logto.io/announcing-japan-region : 日本の地域 (2026-11-11)。
- https://docs.logto.io/logto-oss : OSS と Cloud の違い (2026-11-11)。
- https://docs.logto.io/integrations/line 、 https://docs.logto.io/end-user-flows/sign-up-and-sign-in/passkey-sign-in : LINE、パスキー (2026-11-11)。

## 未確認のこと

- 提供会社の正式名。
- 「トークン」の数え方 (どの発行が数えられるか)。
- 追加料金が月額か。
- OSS 版でのパスキーログイン。
- Cloud からの書き出し、他社からの取り込み。
- ISMAP の登録の有無、日本語の画面。
