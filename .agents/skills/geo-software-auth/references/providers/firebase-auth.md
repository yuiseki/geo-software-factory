# Firebase Authentication

対象: Google の Firebase Authentication と、その上位の Google Cloud Identity Platform

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | Google LLC |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | 管理型サービスのみ |
| ライセンス (OSS の場合) | サービス本体は OSS ではない。Web SDK `firebase` 13.2.0 は Apache-2.0 (npm)。firebase-js-sdk のリポジトリは Apache-2.0 で、同梱の protobuf だけ BSD-3-Clause (LICENSE ファイル) |
| 料金ページ | https://firebase.google.com/pricing 、 https://cloud.google.com/identity-platform/pricing |
| ドキュメント | https://firebase.google.com/docs/auth |

## 概要

Firebase Authentication は Firebase のプロジェクトに付く管理型の認証で、Identity Platform に上げると SAML と OIDC、マルチテナントなどが加わる。料金は Identity Platform の MAU 単価で決まり、メール、電話、匿名、ソーシャルの「Tier 1」は 50,000 MAU まで無料である。パスキーを標準の機能として使える旨の記載は公式文書に見つからなかった。

## 料金と無料枠

- 課金単位と無料枠: MAU。Spark (無料) も Blaze (従量) も 50,000 MAU まで無料 (https://firebase.google.com/pricing、2026-11-11)。Identity Platform の Tier 1 (メール、電話、匿名、ソーシャル) は 0〜50,000 が無料、50,000〜100,000 が 1 MAU 0.0055 ドル、100,000〜1,000,000 が 0.0046 ドル、1,000,000〜10,000,000 が 0.0032 ドル、それ以上が 0.0025 ドル (https://cloud.google.com/identity-platform/pricing?hl=en、2026-11-11)。
- 有料プランの最低額と、主な機能が入るプラン: 月額の最低額はなく、Blaze での従量課金。電話認証は Spark では使えず、Blaze で送った SMS ごとに課金 (https://firebase.google.com/pricing、2026-11-11)。
- SSO (SAML) や組織機能の追加料金: SAML と OIDC (Tier 2) は 1 プロジェクトあたり 50 MAU まで無料、それ以上は 1 MAU 0.015 ドル (https://cloud.google.com/identity-platform/pricing?hl=en、2026-11-11)。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 対応 | メールとパスワード、電話 (SMS)、匿名 (https://firebase.google.com/docs/auth、2026-11-11) |
| ソーシャルログイン (Google、Apple、LINE など) | 対応 | 標準は Google、Apple、Facebook、Twitter、GitHub。LINE は標準にない。Identity Platform の OIDC で足せるかは未確認 (推測では可能) |
| パスキー | 標準の機能としての記載なし | 公式の概要ページに記載がない。第三者の拡張 (Corbado など) はある (2026-11-11) |
| MFA | 未確認 | Identity Platform の機能として扱われる (詳細は未確認) |
| SAML / OIDC による企業 SSO | Identity Platform で対応 | SAML は Web のみ (https://firebase.google.com/docs/auth、2026-11-11) |
| 組織・テナントと役割 (RBAC) | 一部 | Identity Platform のマルチテナント。役割は独自のクレームで持たせる (推測) |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | ID トークン (JWT) を発行する | RS256、`aud` はプロジェクト ID、`iss` は `https://securetoken.google.com/<projectId>`、公開鍵は `https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com` (https://firebase.google.com/docs/auth/admin/verify-id-tokens、2026-11-11)。Firestore のセキュリティルールと結びつく。PostgreSQL の RLS には別の層が要る (推測) |
| 日本語の画面 | 未確認 | |
| データの保存地域 (日本リージョン) | 未確認 | Identity Platform のデータの置き場所を示す公式の記載を見つけられなかった |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: ID トークンをタイルのリクエストに付け、エッジ関数で上記の公開鍵と `aud`、`iss` を照合する。手段は [tile-access-control](../tile-access-control.md)。
- エッジ関数やサーバーレスで動くか: 第三者の JWT ライブラリで検証する手順が公式にあるので、Web Crypto のある環境で検証できる (推測)。公開鍵の更新は応答の `Cache-Control` の `max-age` に従う (公式文書)。

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: Google Cloud の ISMAP の範囲に Identity Platform や Firebase が入るかは未確認 (公式ページの本文を取得できなかった)。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): `firebase auth:export` はスクリプトのハッシュだけを出し、他のアルゴリズムの利用者は `passwordHash` と `salt` が空で出る (https://firebase.google.com/docs/cli/auth、2026-11-11)。既定の保存形式は Firebase 独自の改変 scrypt で、パラメータはコンソールで見られる。
- 他の提供者からの取り込み: 改変 scrypt、標準 scrypt、HMAC (MD5、SHA1、SHA256、SHA512)、MD5、SHA1、SHA256、SHA512、PBKDF_SHA1、PBKDF2_SHA256、BCRYPT を取り込める。Argon2 は Admin Java SDK のみ (https://firebase.google.com/docs/auth/admin/import-users、2026-11-11)。

## ライセンス上の注意

- サービス本体は Google の規約による。SDK は Apache-2.0 なので、組み込み、改変、配布、SaaS のいずれでも著作権表示、ライセンス文、NOTICE と改変の明示を残す。

## 向いている場面

- すでに Firebase (Firestore、Hosting) で作るアプリで、セキュリティルールと結びつけたいとき。
- 50,000 MAU まで無料で、利用者がそれより大きく伸びても単価が低いとき。

## 向いていない場面

- パスキーを標準の機能で使いたいとき。
- LINE ログインを標準で使いたいとき。
- データの置き場所を日本と示す必要がある案件 (未確認のため)。

## 出典

- https://firebase.google.com/pricing : Spark と Blaze の無料枠、電話認証 (2026-11-11)。
- https://cloud.google.com/identity-platform/pricing?hl=en : Tier 1 と Tier 2 の単価 (2026-11-11、ページの HTML から抜き出した)。
- https://firebase.google.com/docs/auth : 対応するログイン方法 (2026-11-11)。
- https://firebase.google.com/docs/auth/admin/verify-id-tokens : ID トークンの検証 (2026-11-11)。
- https://firebase.google.com/docs/auth/admin/import-users 、 https://firebase.google.com/docs/cli/auth : 取り込みと書き出し (2026-11-11)。

## 未確認のこと

- パスキーへの公式な対応予定。
- データの保存地域、日本リージョンの有無。
- ISMAP の範囲。
- LINE を OIDC で足せるか (LINE の OIDC 対応と Identity Platform の条件の突き合わせ)。
- MFA の課金。
