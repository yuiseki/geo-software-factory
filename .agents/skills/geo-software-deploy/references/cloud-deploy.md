# 主要クラウド・PaaS へのデプロイ

対象: AWS、Google Cloud、Microsoft Azure、Vercel、Netlify、Render (Cloudflare Workers と D1 は [cloudflare-workers](cloudflare-workers.md) を参照)。昼に準備した CLI 認証と権限の範囲で、夜の自律実装を本番・プレビューへ出し、落ちたら即座に戻す手順をまとめる。

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |

## 一覧比較 (デプロイ・認証・ロールバック)

| 提供元 | 主な CLI / 構成ファイル | 昼に済ませる認証・環境変数 | プレビュー / 本番を汚さない出し方 | ロールバック (前の版へ戻す) | 注意点 |
|---|---|---|---|---|---|
| **AWS** (S3 + CloudFront / App Runner) | `aws` CLI、SAM / CDK / Terraform | `AWS_ACCESS_KEY_ID` 等、または GitHub OIDC ロール (`aws sts get-caller-identity` で確認) | S3 は別プレフィックスや別ステージ配信、App Runner は別サービスまたはイメージタグ固定 | App Runner は前のコンテナイメージタグ再配備。S3 は版付きプレフィックスのオリジンパスを戻し CloudFront キャッシュ無効化 | App Runner は待機課金あり ([cloud-containers](../../geo-software-arch/references/hosting/cloud-containers.md)) |
| **Google Cloud** (Cloud Run / GCS) | `gcloud` CLI | `gcloud auth login` またはサービスアカウント / WIF (`gcloud auth list` で確認) | `gcloud run deploy --no-traffic --tag preview` でトラフィック 0% のリビジョンを作成し URL で検証 | `gcloud run services update-traffic --to-revisions OLD=100` で即時トラフィック切り替え | `smoke.py` とシナリオ評価を `--no-traffic` URL に先に当ててから本番へ 100% 切替できる |
| **Microsoft Azure** (Static Web Apps / Container Apps) | `az` CLI、`swa` CLI | `az login` またはサービスプリンシパル、`AZURE_STATIC_WEB_APPS_API_TOKEN` | Static Web Apps は `--env preview` (Free 最大 3 環境)。Container Apps はリビジョンモードで 0% トラフィックリビジョン作成 | Container Apps は前リビジョンへトラフィック 100% を戻す。Static Web Apps は再デプロイで差し替え | Static Web Apps Free は単一環境 250 MB 上限、帯域 100 GB 超過不可 |
| **Vercel** | `vercel` CLI、`vercel.json` | `VERCEL_TOKEN`、`VERCEL_ORG_ID`、`VERCEL_PROJECT_ID` (`vercel whoami` で確認) | `vercel deploy` (引数なし) でプレビュー URL を発行。本番は `vercel deploy --prod` | `vercel rollback [<url-or-id>]` で即座に前のイミュータブルな本番配備へ切替 | Hobby プランは非商用限定。`.vercel.app` プレビュー URL の公開範囲に注意 |
| **Netlify** | `netlify` CLI、`netlify.toml` | `NETLIFY_AUTH_TOKEN`、`NETLIFY_SITE_ID` (`netlify status` で確認) | `netlify deploy` (引数なし) で Draft プレビュー URL を発行。本番は `netlify deploy --prod` | 各デプロイがイミュータブルなスナップショット。UI の Publish deploy または API で即時復元 | Free は月 300 クレジットを使い切ると全サイトが停止する |
| **Render** | `render` CLI、`render.yaml` (Blueprint) | `RENDER_API_KEY`、`render blueprints validate render.yaml` | Pull Request Preview / Preview Environments (有料プラン機能) または検証用別サービス | Dashboard の Deploys -> Rollback、または API `POST /v1/services/{serviceId}/rollback` (`deployId` 指定) | 永続ディスクと DB はサービスロールバックで戻らない。ロールバック時は自動デプロイが停止する |

## 夜のデプロイ共通の進め方

1. **デプロイ前関門**: どの提供元に出す場合も、先に [deploy_gate.py](../scripts/deploy_gate.py) (`check`) を通し、未コミットの変更が無いこと、評価報告 (`final.json`) の `version` が `HEAD` と一致し `ok: true` であること、重大な監査指摘や承認なしの破壊的 SQL が無いことを確かめる。
2. **プレビュー先行**: Google Cloud Run (`--no-traffic`)、Vercel (`vercel deploy`)、Netlify (`netlify deploy`) のように本番トラフィックを汚さずに検証 URL を作れる提供元では、まずプレビュー URL に対して `smoke.py` と `run_eval.py` を流してから本番へ切り替える。
3. **台帳への記録**: 本番へ出したら `deploy_gate.py record` にプラットフォーム側の版 ID (Cloud Run のリビジョン名、Vercel/Netlify のデプロイ URL や ID、Render の `deployId`、Cloudflare Workers の version ID) と `HEAD` コミットを対で記録する。
4. **拒まれたとき**: CLI の認証切れや権限エラー、自動許可の検査に拒まれた場合は、承認を待たずに作業ブランチへコミットし、プレビュー URL や手順コマンドを朝の報告の「止まったこと」に残す。

## 出典

- https://cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration (`gcloud run deploy --no-traffic` とトラフィック切替ロールバック)
- https://learn.microsoft.com/azure/static-web-apps/deploy-preview (Azure Static Web Apps のプレビュー環境)
- https://vercel.com/docs/deployments/instant-rollback (`vercel rollback`)
- https://docs.netlify.com/site-deploys/manage-deploys/#rollbacks (Netlify のイミュータブルデプロイとロールバック)
- https://render.com/docs/rollbacks (Render の Rollback と API、Blueprint の検証)
