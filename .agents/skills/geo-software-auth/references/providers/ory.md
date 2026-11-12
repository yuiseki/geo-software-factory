# Ory

対象: Ory の OSS (Kratos、Hydra、Keto、Oathkeeper、Polis) と、管理型の Ory Network

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | Ory Corp |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | 両方。自前運用には OSS 版と、有料の Ory Enterprise License (OEL) 版がある |
| ライセンス (OSS の場合) | Kratos、Hydra、Keto、Oathkeeper、Polis はいずれも Apache-2.0 (`gh api repos/ory/<repo>/license`)。Kratos と Hydra の最新は v26.2.0 (2026-03-20)。`@ory/client` 1.22.66 は Apache-2.0 (npm) |
| 料金ページ | https://www.ory.com/pricing |
| ドキュメント | https://www.ory.com/docs |

## 概要

Ory は認証 (Kratos)、OAuth 2.0 と OIDC の発行 (Hydra)、権限の判定 (Keto)、プロキシでの認可 (Oathkeeper)、企業 SSO (Polis) を別々の部品として出している。部品を組み合わせる自由度は高いが、自前運用では組み立てと運用の手間が大きい (推測)。管理型の Ory Network は MAU ではなく aDAU (1 日の利用者数の月平均) で課金する。

## 料金と無料枠

- 課金単位と無料枠: aDAU、M2M トークン、権限の判定回数。Developer は無料だが本番環境 0、開発環境 2、メンバー 1 (https://www.ory.com/pricing、2026-11-11)。
- 有料プランの最低額と、主な機能が入るプラン: Production は年 770 ドル (月 21 ドルの利用分を含む)、aDAU 1 人月 0.14 ドル、M2M トークン 1 つ月 0.007 ドル、権限の判定 1 回 0.000090 ドル。Growth は年 9,350 ドル (月 255 ドル分を含む)、aDAU 0.12 ドル。Enterprise は見積もりで 99.99% の SLA (同上)。
- SSO (SAML) や組織機能の追加料金: 料金ページでは確かめていない (未確認)。自前運用では Kratos の B2B の組織とマルチテナントが OEL 版だけ (https://www.ory.com/docs/self-hosted/oel、2026-11-11)。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 対応 | 詳細は未確認 |
| ソーシャルログイン (Google、Apple、LINE など) | 対応 | LINE の対応は未確認 |
| パスキー | 対応 | Kratos は WebAuthn のパスキーでのパスワードレスに対応し、自前運用の設定例がある (https://www.ory.com/docs/kratos/passwordless/passkeys、2026-11-11) |
| MFA | 対応 | 詳細は未確認 |
| SAML / OIDC による企業 SSO | 対応 | Polis (Apache-2.0)。OSS 版に含まれるかは OEL のページに書かれていない (未確認) |
| 組織・テナントと役割 (RBAC) | 一部 | 権限は Keto (関係ベース)。Kratos の B2B 組織は自前運用では OEL 版だけ |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | 対応 | Hydra が OIDC のトークンを出す。RLS への渡し方は未確認 |
| 日本語の画面 | 未確認 | |
| データの保存地域 (日本リージョン) | 日本はあるが一般提供ではない | 2024-10-11 に日本のデータ地域を発表、コンソールからは選べず本番利用は Ory に連絡 (https://changelog.ory.com/announcements/japan-data-region、2026-11-11)。地域の選択は Production と Growth から (料金ページ) |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: Oathkeeper をタイルサーバーの前に置き、セッションやトークンを確かめてから通す構成が取れる (推測)。エッジでの検証は [tile-access-control](../tile-access-control.md)。
- エッジ関数やサーバーレスで動くか: OSS の各部品は Go の常時動くサーバー (推測)。

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: Ory Network の ISMAP 登録は未確認。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): 未確認。
- 他の提供者からの取り込み: 未確認。
- 自前運用の OSS 版は「評価と試作向け」と料金ページに書かれ、本番の自前運用には OEL を勧めている。OSS 版に CVE の修正を保証する Continuous Security License も別売り (https://www.ory.com/pricing、 https://www.ory.com/docs/self-hosted/oel、2026-11-11)。

## ライセンス上の注意

- OSS 版は Apache-2.0。自前で運用、改変、配布、SaaS 提供のいずれでもソースの公開義務はなく、配布するときはライセンス文と NOTICE、改変の明示を残す。
- OEL は商用ライセンスで、条件は契約による (本文は未確認)。B2B の組織、マルチテナント、ダウンタイムのない更新などは OEL 版のビルドにだけある。

## 向いている場面

- 認証、OAuth の発行、細かい権限の判定を部品ごとに組み合わせたいとき。
- 管理型で、利用の山が大きく平均が小さいサービス (aDAU は日ごとの平均で山をならす)。

## 向いていない場面

- 自前運用で B2B の組織機能が要り、OEL を買わないとき。
- データを日本に置くことを管理型で確実に満たしたいとき (日本の地域は一般提供でない)。
- 小さなチームで部品を組み立てて運用する余力がないとき。

## 出典

- https://www.ory.com/pricing : プラン、aDAU の単価、OSS と OEL (2026-11-11)。
- https://www.ory.com/docs/self-hosted/oel : OEL だけの機能 (2026-11-11)。
- https://www.ory.com/docs/kratos/passwordless/passkeys : パスキー (2026-11-11)。
- https://changelog.ory.com/announcements/japan-data-region : 日本のデータ地域 (2026-11-11)。
- https://github.com/ory/kratos ほか : LICENSE (Apache-2.0)、リリース。

## 未確認のこと

- 企業 SSO (Polis) の Ory Network での料金と、OSS 版での扱い。
- LINE の対応。
- ユーザーの書き出しと取り込み。
- ISMAP の登録の有無、日本語の画面。
