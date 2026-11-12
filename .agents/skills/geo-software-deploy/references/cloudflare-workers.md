# Cloudflare Workers と D1 に出す

静的ファイルと API を 1 つの Worker で配り、D1 に保存する構成で、実際に出したときの手順と挙動。挙動は 2026-11-12 に wrangler 4 系で見たもの。版で変わることがある。

## 手順

```sh
npm test && npm run build                                   # テスト、型検査、ビルド
npx wrangler d1 migrations apply <DB 名> --remote           # 追加だけのマイグレーション
npx wrangler deploy                                         # 版の ID が出る
curl -s https://<本番のホスト>/api/<確かめる API>            # 本番で確かめる
```

- マイグレーションは、手元 (`--local`) で当ててテストを通してから、本番 (`--remote`) に当てる。
- 本番の D1 への API の呼び出しは、一時的に失敗することがあった。追加だけのマイグレーションや読み出しは、少し待って再試行してよい。消す、書き換える操作は再試行の前に状態を確かめる。
- 本番に流さずに版だけを作るときは、版のアップロード (`wrangler versions upload`) を使い、本番の割り当ては変えない (https://developers.cloudflare.com/workers/configuration/versions-and-deployments/)。

## 静的ファイルと API を 1 つの Worker で配る

- `assets` の `not_found_handling` を `single-page-application` にすると、画面の URL (`/japan/kansai/osaka/` など) をそのまま開ける。
- `run_worker_first` に API の道 (`/api/*`) を書くと、その道だけ Worker の処理が先に動く。

## 独自ドメイン

- `routes` に `custom_domain: true` で独自ドメインを割り当てると、それまでの `*.workers.dev` の URL が既定で無効になった。ホーム画面に入れた PWA や、共有済みのリンクが開けなくなる。残すなら `workers_dev: true` を明示する。
- 認証のプロバイダーに許可するオリジン (Clerk の authorized parties など) に、新しいドメインを足す。足し忘れると、新しいドメインでだけログインが通らない。
- デプロイの直後の数秒は、古い版や 404 が返ることがあった。少し待って確かめ直す。

## 手元の開発サーバー

- `wrangler dev` は、ビルドで静的ファイルが作り直されると、それを配らなくなることがあった。ビルドのたびに立て直す。
- 立て直すときは、自分が起動したプロセスの番号で止める。

## 鍵

- Clerk の Publishable Key のように、画面に配る前提の値は `vars` に書いてよい。
- 秘密の値は `wrangler secret put` で設定し、設定ファイルにもリポジトリにも書かない。トークンの検証を公開の検証鍵 (JWKS) で行えば、秘密の鍵自体が要らないことがある。
