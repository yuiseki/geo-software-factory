# Better Auth

対象: TypeScript の認証ライブラリ Better Auth (自分のアプリと DB に組み込む OSS) と、同社の有料の管理基盤

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | Better Auth (better-auth/better-auth のメンテナー) |
| 形態 (管理型サービス / OSS を自前で運用 / 両方) | OSS のライブラリを自分のサーバーで動かす。ダッシュボードや監査ログは有料の管理基盤として別に売られている |
| ライセンス (OSS の場合) | MIT (`gh api repos/better-auth/better-auth/license` は MIT、LICENSE.md)。npm の `better-auth` 1.7.20 も MIT |
| 料金ページ | https://www.better-auth.com/pricing (管理基盤の料金。ライブラリは無料) |
| ドキュメント | https://www.better-auth.com/docs |

## 概要

Better Auth は特定のフレームワークに依存しない TypeScript の認証ライブラリで、利用者とセッションを自分の DB (SQLite、PostgreSQL、MySQL、各 ORM) に持つ。パスキー、組織、2 要素認証などはプラグインで足す。認証のサービス会社にデータを預けないので、データの置き場所は自分の DB の置き場所で決まる。

## 料金と無料枠

- 課金単位と無料枠: ライブラリは無料 (「The Better Auth framework is free and open source」、https://www.better-auth.com/pricing、2026-11-11)。MAU の課金はない。
- 有料プランの最低額と、主な機能が入るプラン: 管理基盤は Starter 0 ドル (席 1、監査ログ月 10,000 件で保持 1 日、セキュリティ検知月 1,000 件)、Pro 月 20 ドル (席無制限、監査ログ月 20,000 件で以降 1 件 0.0001 ドル、保持 7 日、検知月 10,000 件で以降 1 件 0.001 ドル、メール 1 通 0.001 ドル、SMS 1 通 0.09 ドル)、Enterprise は見積もり。カスタムのダッシュボードドメインとログの転送は各月 25 ドル (同上)。
- SSO (SAML) や組織機能の追加料金: 管理基盤の Pro にセルフサービスの SSO と Directory Sync が各 1 接続含まれ、追加は 1 接続月 50 ドル (同上)。ライブラリだけで SAML を扱えるかは未確認。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| メールとパスワード、メールのリンク・OTP | 対応 | 詳細は未確認 |
| ソーシャルログイン (Google、Apple、LINE など) | 対応 | LINE の文書がある (https://www.better-auth.com/docs/authentication/line、2026-11-11 にページの存在を確認) |
| パスキー | プラグイン | `@better-auth/passkey` (https://www.better-auth.com/docs/plugins/passkey、2026-11-11)。成熟度の記載はない |
| MFA | プラグイン | 2FA (README) |
| SAML / OIDC による企業 SSO | 未確認 | 管理基盤のセルフサービス SSO は上記 |
| 組織・テナントと役割 (RBAC) | プラグイン | Organization プラグイン (https://www.better-auth.com/docs/plugins/organization) |
| JWT の発行と、DB の行単位アクセス制御 (RLS) との連携 | 未確認 | 既定はセッション (Cookie) 方式 (推測)。JWT を出すプラグインの有無と、RLS への渡し方は未確認 |
| 日本語の画面 | 該当なし | 画面はアプリ側で作る (推測) |
| データの保存地域 (日本リージョン) | 自分で決める | 利用者のデータは自分の DB に置く |

## 地図プロダクトとの組み合わせ

- タイルや地図 API への認可: 地図と同じオリジンでセッション Cookie を使い、タイルを返すサーバーやエッジでセッションを確かめる形が組みやすい (推測)。別オリジンのタイルには、MapLibre の `credentials: 'include'` か短命のトークンが要る。手段は [tile-access-control](../tile-access-control.md)。
- エッジ関数やサーバーレスで動くか: Cloudflare Workers の例が文書にあり、AsyncLocalStorage のために `nodejs_compat` か `nodejs_als` のフラグが要る。D1 への言及はない (https://www.better-auth.com/docs/installation、2026-11-11)。

## 公共案件での利用

- ISMAP などの登録、政府・自治体の利用条件: ライブラリなので ISMAP の対象ではない。動かす基盤 (IaaS) の登録で判断することになる (推測)。

## ロックインと移行

- ユーザーの書き出し (パスワードのハッシュを含むか): 利用者のテーブルは自分の DB にあるので、そのまま持ち出せる。ハッシュの形式は未確認。
- 他の提供者からの取り込み: 未確認。

## ライセンス上の注意

- MIT。組み込み、改変、配布、SaaS のいずれでも、著作権表示とライセンス文を残せばよい。コピーレフトではないので、自社のコードを公開する義務は生じない (MIT の条文から)。
- 管理基盤 (有料) を使う場合は、そのサービスの規約による (規約本文は未確認)。

## 向いている場面

- 地図アプリを TypeScript で書き、利用者のデータを自分の DB (PostGIS と同じ DB など) に置きたいとき。
- MAU の課金を避けたいとき、閉域網やオンプレで動かしたいとき。
- Cloudflare Workers で、地図の API と認証を同じところに置きたいとき。

## 向いていない場面

- 認証の運用 (脆弱性の対応、鍵の管理、メール送信) を自分で持ちたくないとき。
- SAML の企業 SSO を多数の自治体や企業に付ける B2B (ライブラリだけでの対応が未確認)。

## 出典

- https://github.com/better-auth/better-auth : LICENSE (MIT)、README (2026-11-11)。
- https://www.better-auth.com/pricing : 管理基盤の料金 (2026-11-11)。
- https://www.better-auth.com/docs/installation : DB とアダプタ、Workers (2026-11-11)。
- https://www.better-auth.com/docs/plugins/passkey : パスキーのプラグイン (2026-11-11)。

## 未確認のこと

- ライブラリ単体での SAML 対応。
- JWT の発行と、PostgreSQL の RLS への渡し方。
- パスワードハッシュの形式と、他の提供者からの取り込み。
- 管理基盤の規約とデータの置き場所。
