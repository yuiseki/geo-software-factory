# WorkOS AuthKit

対象: WorkOS の AuthKit (User Management) と、企業 SSO、Directory Sync

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | WorkOS, Inc. |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | 管理型サービスのみ |
| ライセンス (OSS の場合) | サービス本体は OSS ではない。SDK は MIT (`@workos-inc/authkit-js` 0.20.5、`@workos-inc/node` 12.2.0、npm) |
| 料金ページ | https://workos.com/pricing |
| ドキュメント | https://workos.com/docs |

## 概要

WorkOS は企業向け (B2B) の SaaS に SSO と Directory Sync (SCIM) を付けることを主にした管理型サービスで、AuthKit は利用者管理とログイン画面を担う。利用者の数では 100 万 MAU まで無料で、課金の中心は企業 SSO の接続数である。

## 料金と無料枠

- 課金単位と無料枠: AuthKit は最初の 100 万 MAU が無料で、追加の 100 万 MAU ごとに月 2,500 ドル。本番環境だけ課金し、ステージングは無料 (https://workos.com/pricing、2026-11-11)。
- 有料プランの最低額と、主な機能が入るプラン: 月額の基本料はなく機能ごとの課金。カスタムドメインは月 99 ドル。Radar (ボットと不正の防止) は 1,000 回まで無料で、以降 5 万回ごとに月 100 ドル。監査ログは SIEM 接続 1 つ月 125 ドル、保持は 100 万件ごとに月 99 ドル (同上)。
- SSO (SAML) や組織機能の追加料金: SSO は 1 接続 1〜15 が 125 ドル、16〜30 が 100 ドル、31〜50 が 80 ドル、51〜100 が 65 ドル、101 以上は見積もり。Directory Sync も同じ単価 (同上。料金ページの表記に「/mo」が付くかは今回の抜き出しで確かめていない)。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 未確認 | |
| ソーシャルログイン (Google、Apple、LINE など) | 未確認 | LINE の対応は未確認 |
| パスキー | 対応 | AuthKit のパスキーの文書がある (https://workos.com/docs/authkit/passkeys、2026-11-11 にページの存在を確認) |
| MFA | 未確認 | |
| SAML / OIDC による企業 SSO | 対応 | 主たる機能。接続数で課金 |
| 組織・テナントと役割 (RBAC) | 対応 | 組織の単位で SSO と Directory Sync を付ける (詳細は未確認) |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | JWT を発行する | JWT テンプレートでクレームを変えられる (https://workos.com/docs/authkit/jwt-templates、ページの存在を確認)。RLS との連携は別の層が要る (推測) |
| 日本語の画面 | 未確認 | |
| データの保存地域 (日本リージョン) | 未確認 | セキュリティのページと API リファレンスに地域の記載がない (https://workos.com/security、 https://workos.com/docs/reference、2026-11-11) |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: AuthKit の JWT をタイルのリクエストに付けてエッジで検証する形になる (推測)。手段は [tile-access-control](../tile-access-control.md)。
- エッジ関数やサーバーレスで動くか: 未確認。

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: 未確認。SOC 2 Type 2 と GDPR、CCPA への準拠をうたっている (https://workos.com/security、2026-11-11)。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): 書き出しの手順は別の文書にあるとされ、ハッシュを含むかは未確認。
- 他の提供者からの取り込み: 作成時か Update User API でハッシュを取り込め、bcrypt、scrypt、firebase-scrypt、pbkdf2、argon2、ssha、ssha256 に対応する (https://workos.com/docs/migrate/other-services、2026-11-11)。

## ライセンス上の注意

- サービス本体は WorkOS の規約による。SDK は MIT で、著作権表示とライセンス文を残せばよい。

## 向いている場面

- 自治体や企業ごとに SAML の SSO や SCIM を付ける B2B の地図 SaaS。
- 利用者数は多いが、企業 SSO の接続は少ないとき (100 万 MAU まで無料)。

## 向いていない場面

- データの保存地域を日本と示す必要がある案件 (未確認のため)。
- SSO の接続が多数あり、1 接続ごとの課金が重いとき。

## 出典

- https://workos.com/pricing : AuthKit の無料枠、SSO と Directory Sync の単価、追加機能 (2026-11-11)。
- https://workos.com/security : SOC 2、GDPR (2026-11-11)。
- https://workos.com/docs/migrate/other-services : ハッシュの取り込み (2026-11-11)。
- https://workos.com/docs/authkit/passkeys 、 https://workos.com/docs/authkit/jwt-templates : ページの存在 (2026-11-11)。

## 未確認のこと

- データの保存地域と日本リージョンの有無。
- 対応するソーシャルログインと LINE。
- ユーザーの書き出しにハッシュが入るか。
- SSO の単価が月額か (料金ページの表記)。
- ISMAP の登録の有無。
