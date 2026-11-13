# 静的ホスティング

対象: GitHub Pages、Cloudflare Pages と Workers の静的アセット、Cloudflare R2、Vercel、Netlify、Render Static Sites、Fly.io、Amazon S3 + CloudFront、Google Cloud Storage + Cloud CDN、Azure Static Web Apps。地図アプリの HTML と JS、GeoJSON や大きな JSON、PMTiles や COG を、常駐するサーバーなしで配る置き場所として比べる

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

数字は 2026-11-11 に各社の公式文書で確かめた既定値である。Range への応答は、同じ日に各社のホストに置かれた公開ファイル (favicon など) へ `Range: bytes=0-99` を 1 回ずつ送って確かめた。料金は米ドル (USD) である。

## 概要

小さな地図アプリは、静的ホスティングに HTML、JS、データのファイルを置くだけで公開できる。2026-11-11 に公開の地図サービスを観察したところ、GitHub Pages、Cloudflare Pages、Vercel、Fly.io、S3 + CloudFront のどれもが使われていた。投稿の保存だけを Firebase Firestore や Supabase に任せる構成も多い ([source-of-truth](../capabilities/source-of-truth.md))。

地図で差が出るのは次の 4 点である。

- Range に 206 で答えるか。PMTiles と COG はブラウザから Range で一部だけを読むので、200 で全体を返す置き場所では直接読めない ([cloud-native-formats](../formats/cloud-native-formats.md))
- 1 ファイルとサイト全体の大きさの上限。全国や全球の PMTiles はここで外れる
- 無料枠を超えたときに、課金されるのか、止まるのか、遅くなるのか
- 大きな JSON や API の応答をエッジでキャッシュするか

## 比較表

| 候補 | Range (206) | 1 ファイルの上限 | サイト全体の上限 | 無料枠 | 無料枠を超えたとき | 無料プランの商用利用 | エッジのキャッシュ | 出典 |
|---|---|---|---|---|---|---|---|---|
| GitHub Pages | 206 を返す (2026-11-11 に maplibre.org と pmtiles.io の静的ファイルで確かめた。`accept-ranges: bytes`、`server: GitHub.com`) | 公式の Pages の制限には記載がない。リポジトリとしては 100 MiB を超えるファイルを GitHub が拒む (50 MiB で警告、ブラウザからの追加は 25 MiB) | 公開サイトは 1 GB まで。ソースのリポジトリは 1 GB を推奨 | 帯域は月 100 GB の soft limit。ビルドは 1 時間 10 回の soft limit (GitHub Actions の独自ワークフローには適用されない)。デプロイは 10 分でタイムアウト | 超えるとレート制限で HTTP 429 を返すことがある (公式の制限ページ)。課金はない | 「オンラインビジネスを動かす無料の Web ホスティング」としての利用は許されない。商取引や商用 SaaS を主目的とするサイト、パスワードやクレジットカード番号を扱うサイトも禁止 | Fastly (varnish) の前段がある。観察した `cache-control` は `max-age=600`、`access-control-allow-origin: *`。ヘッダーを設定する方法は公式文書に見つからなかった | [Pages の制限](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)、[大きなファイル](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) |
| Cloudflare Pages | 200 で全体を返す。公式文書は「現在は Range に 200 を返し、206 に対応する作業中」と書く | 25 MiB | Free は 20,000 ファイル、有料プランは 100,000 ファイル (プロジェクト設定で `PAGES_WRANGLER_MAJOR_VERSION=4` が要る) | ビルドは月 500 回 (Free)。静的アセットの帯域とリクエストの上限は制限のページに記載がない | 未確認 (静的アセットの帯域の上限が文書にない)。Pages Functions へのリクエストは Workers のプランの量に数える | 未確認 (制限のページに商用の制限の記載はない) | 配備したアセットは次の配備まで CDN にキャッシュされる。`Range` か `Authorization` 付きの要求はキャッシュの対象外 | [Pages の制限](https://developers.cloudflare.com/pages/platform/limits/)、[Serving Pages](https://developers.cloudflare.com/pages/platform/serving-pages/) |
| Cloudflare Workers の静的アセット | 200 で全体を返す (公式文書)。206 が要るパスは `run_worker_first` で Worker を通して自分で組み立てる | 25 MiB ([edge-functions](../edge/edge-functions.md)) | Free は 1 版 20,000 ファイル、Paid は 100,000 ファイル ([edge-functions](../edge/edge-functions.md)) | 静的アセットへのリクエストは無料で無制限 | 静的アセットは数えない。Worker を起動したリクエストだけが Workers の料金になる | 未確認 | Workers の静的アセットは CDN から返る (推測: 制限のページはキャッシュの上限を書いていない) | [静的アセットの料金と制限](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/) |
| Cloudflare R2 (公開バケット) | 206 を返す (2026-11-11 に Protomaps のサンプル PMTiles で確かめた。`cf-cache-status: DYNAMIC`) | 1 オブジェクト 5 TiB。1 回の PUT は 5 GiB、マルチパートで 4.995 TiB | 記載なし (保存量で課金) | 保存 10 GB-月、Class A 100 万回、Class B 1,000 万回 (Standard のみ)。下り転送は無料 | 保存は 0.015 ドル/GB-月。操作は単価で課金 ([edge-functions](../edge/edge-functions.md)) | 未確認 | `r2.dev` の URL はキャッシュが使えず、レート制限 (数百リクエスト/秒で 429、帯域も絞られる) があり本番向けでない。独自ドメインを付けると Cloudflare のキャッシュが使える。キャッシュは Free、Pro、Business で 1 ファイル 512 MB まで | [R2 料金](https://developers.cloudflare.com/r2/pricing/)、[R2 の制限](https://developers.cloudflare.com/r2/platform/limits/)、[公開バケット](https://developers.cloudflare.com/r2/buckets/public-buckets/)、[既定のキャッシュ](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/) |
| Vercel | 静的ファイルは 206 を返す (2026-11-11 に nextjs.org の favicon で確かめた。`x-vercel-cache: HIT`) | 未確認 (1 ファイルの上限の記載は見つからなかった)。CLI で上げるソースは Hobby 100 MB、Pro 1 GB まで | CLI の配備は 15,000 ファイルまで (`--archive=tgz` で回避できる) | Hobby は月に Fast Data Transfer 100 GB、Fast Origin Transfer 10 GB、CDN リクエスト 100 万回、関数の呼び出し 100 万回 | Hobby は超えると多くの場合 30 日待つまでその機能を使えない | Hobby は個人の非商用だけ (fair use guidelines) | 静的ファイルは配備の間ずっと自動でキャッシュされる。関数の応答は `s-maxage` などを付けたときだけ、リージョンごとにキャッシュされ、上限は 10 MB。`Authorization` 付きの要求、`set-cookie` 付きの応答、`Vary: Cookie` はキャッシュしない | [Limits](https://vercel.com/docs/limits)、[Hobby](https://vercel.com/docs/plans/hobby)、[CDN Cache](https://vercel.com/docs/caching/cdn-cache) |
| Netlify | 206 を返す (2026-11-11 に docs.netlify.com の静的ファイルで確かめた。`accept-ranges: bytes`) | 未確認 (公式文書に 1 ファイルの上限の記載が見つからなかった) | 未確認 | Free は月 300 クレジット。Web のリクエストは 1 万回で 2 クレジット、帯域は 1 GB で 20 クレジット (帯域だけなら約 15 GB) | Free はクレジットを使い切ると全サイトが止まり、訪問者には `Site not available` が出る。追加購入はできない | 未確認 (料金ページに記載がない) | 静的アセットはエッジにキャッシュされ、配備で自動的に無効化される。`max-age` を短くする指定は無視して最長 1 年新鮮とみなす | [料金](https://www.netlify.com/pricing/)、[クレジットの仕組み](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/)、[クレジットのプラン](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/)、[キャッシュ](https://docs.netlify.com/build/caching/caching-overview/) |
| Fly.io | アプリ次第。Fly のプロキシ越しに 206 が返ることは fly.io 自身の静的ファイルで確かめた (2026-11-11)。Next.js などのアプリが Range に答えるかは別に確かめる | アプリとボリューム次第 (未確認) | 同左 | 新規の組織には無料枠も月の無料量もない。試用として 7 日間か使い切るまでの 1 ドル分 | 従量課金。下り転送は北米と欧州 0.02 ドル/GB、アジア太平洋 0.04 ドル/GB。最小の shared-cpu-1x 256 MB は月 2.19 ドル (iad、ewr で 30 日) | 有料なので制限なし (推測) | 料金ページに CDN キャッシュの記載はない (未確認) | [料金](https://docs.fly.io/about/pricing) |
| Amazon S3 + CloudFront | S3 は Range に答え、CloudFront は要求された範囲をキャッシュして返す (2026-11-11 に a0.awsstatic.com で 206 と `Hit from cloudfront` を確かめた)。範囲が降順、重なり、不正のときは 200 で全体を返す。オリジンが `Transfer-Encoding: chunked` を返すと全体を返す | CloudFront がキャッシュする 1 応答は 50 GB まで。それより大きいオブジェクトも、50 GB 未満の Range に分ければ部分ごとにキャッシュされる | 配れるファイル数に上限なし | 従量課金なら常に無料の枠として月 1 TB の下り転送と 1,000 万リクエスト。定額プランの Free (0 ドル) は 100 万リクエストと 100 GB、S3 の保存のクレジット 5 GB。Free の定額プランは 1 アカウント 3 つまで | 従量課金は単価で課金。定額プランは超過料金がなく、超え続けると配信が調整される (遠いエッジから返す、性能を落とすなど) | 制限の記載なし (未確認) | 拡張子に関係なく、キャッシュポリシーで決める。代替ドメイン名は 1 配信あたり 100 | [Range GET](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RangeGETs.html)、[Quotas](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-limits.html)、[従量料金](https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/)、[定額プラン](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/flat-rate-pricing-plan.html)、[料金](https://aws.amazon.com/cloudfront/pricing/) |
| Google Cloud Storage + Cloud CDN | Cloud CDN と GCS オリジンは Range に 206 で答え、部分キャッシュ (cache fill) を行う (2026-11-13 公式文書確認) | 1 オブジェクト上限は GCS 側 5 TB (未確認箇所あり) | 配れるファイル数に上限なし | GCS の Always Free は 5 GiB 保存・特定リージョンからの下り 100 GB 等。**Cloud CDN 自体には永久無料枠がない** (新規 $300 トライアル枠のみ) | キャッシュ下り転送 (APAC 約 $0.09/GiB)、キャッシュ参照 ($0.0075/1万回)、GCS Class B 操作等の従量課金 | 制限なし (有料アカウント前提) | Cloud CDN がエッジでキャッシュ。Range ミス時は GCS から部分取得 | [Cloud CDN 概要と Range](https://cloud.google.com/cdn/docs/overview)、[Cloud CDN 料金](https://cloud.google.com/cdn/pricing) |
| Azure Static Web Apps (Free) | 未確認 (静的ファイルでの 206 応答可否は未計測) | 記載なし (単一環境合計 250 MB が実質上限) | Free は単一環境 250 MB、全環境計 500 MB、15,000 ファイル | Free は月 100 GB 帯域、カスタムドメイン 2 つ、ステージング環境 3 つ、マネージド Azure Functions 月 100 万回 | 超過トラフィック不可 (Standard プランへのアップグレードが必要) | 個人・非本番向け (Free に SLA なし) | グローバルエッジで配信 | [Azure Static Web Apps プラン](https://learn.microsoft.com/azure/static-web-apps/plans) |
| Render Static Sites | 未確認 (206 応答可否は未計測) | 未確認 | 未確認 | 静的サイトのホスティング自体は常に無料。Workspace Hobby で月 5 GB の下り転送込み | 帯域超過は $0.15/GB (Workspace Hobby) | 未確認 | グローバル CDN 配信、Git 連携で自動無効化 | [Render 料金](https://render.com/pricing) |

## 独自ドメイン

- GitHub Pages: apex と `www` のどちらか、または両方を設定できる。`www` を設定すると apex も自動で守ろうとする (確かめた日 2026-11-11、https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)。1 サイトに付けられる数は文書にない (未確認)
- Cloudflare Pages: 1 プロジェクトに Free 100、Pro 250、Business と Enterprise 500 (確かめた日 2026-11-11、https://developers.cloudflare.com/pages/platform/limits/)
- Vercel: 1 プロジェクトに Hobby 50、Pro は無制限 (確かめた日 2026-11-11、https://vercel.com/docs/plans/hobby)
- Netlify: Free でも独自ドメインと SSL を付けられる (確かめた日 2026-11-11、https://www.netlify.com/pricing/)
- CloudFront: 1 配信に代替ドメイン名 100 (引き上げ可)。定額プランは 1 配信に apex を 1 つまで (確かめた日 2026-11-11、https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-limits.html 、https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/flat-rate-pricing-plan.html)
- R2: 本番では独自ドメインを付ける。`r2.dev` は開発用である (確かめた日 2026-11-11、https://developers.cloudflare.com/r2/buckets/public-buckets/)

## PMTiles をどこに置くか

大きさの目安は、Protomaps の planet ビルドが z0〜15 で約 120 GB ([self-hosting](../self-hosting.md))。地域の PMTiles は対象範囲で切り出して測る (`pmtiles extract`)。

| PMTiles の大きさ | 置ける候補 | 外れる候補と理由 |
|---|---|---|
| 25 MiB 以下 (市区町村の主題データなど) | どれでも置ける。Range に 206 で答える GitHub Pages、Vercel、Netlify ならブラウザの pmtiles ライブラリがそのまま読める | Cloudflare Pages と Workers の静的アセットは 200 で全体を返すので、Range 読みにならず毎回ファイル全体を送る。ファイルが小さければ全体を読む形 (`fetch` で取り込む) でも済む (推測) |
| 25 MiB を超え 100 MiB 以下 | GitHub Pages (サイト 1 GB、帯域 100 GB/月 の soft limit の範囲で)、Vercel と Netlify (上限は未確認)、R2、S3 + CloudFront | Cloudflare Pages と Workers の静的アセット (25 MiB) |
| 100 MiB を超え 1 GB 程度 (都道府県から国の一部) | R2 (独自ドメイン)、S3 + CloudFront | GitHub Pages (1 ファイル 100 MiB、サイト 1 GB)。Vercel Hobby (アップロード 100 MB) |
| 1 GB 以上 (全国、全球) | R2 か S3 などのオブジェクトストレージ。z/x/y にしてタイル単位でキャッシュするなら前に Workers や Lambda を置く ([edge-functions](../edge/edge-functions.md)) | 静的ホスティングの全部。Cloudflare のキャッシュは Free から Business で 512 MB を超えるファイルをキャッシュしないので、R2 の大きな PMTiles を Range のまま配ると毎回 R2 から読む |

自前のタイルホストやアプリのサーバーから PMTiles を返す構成 (Fly.io の Next.js が自分で PMTiles を返す、自前のタイルホストを Cloudflare の後ろに置く) も観察された。このときは Range に 206 で答えるかと、前段の CDN が 206 をキャッシュするかを、実物に Range を 1 回送って確かめる。

## 落とし穴

- Cloudflare Pages と Workers の静的アセットは Range に 200 を返す。PMTiles をここに置くと、ブラウザの pmtiles ライブラリは最初の要求でファイル全体を受け取ってしまう。[edge-functions](../edge/edge-functions.md) の記述と同じである (2026-11-11 に公式文書で再確認した)。
- 大きな JSON は CDN でキャッシュされないことがある。Cloudflare は HTML と JSON を既定でキャッシュせず、キャッシュルールか Worker が要る ([既定のキャッシュ](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/))。Vercel は関数の応答を `s-maxage` などの指定があるときだけキャッシュし、上限は 10 MB である。2026-11-11 に観察した Vercel の地図アプリでは 8.7 MB の JSON API がエッジでキャッシュされていなかった。10 MB の上限の内側なので、キャッシュの指示ヘッダーが無いことが理由と考えられる (推測)。変わらないデータは配備時に静的ファイルとして書き出すと、どの候補でも自動でキャッシュされる。
- Vercel の CDN キャッシュはリージョンごとに分かれ、あまり読まれないものは追い出される。関数のリージョン (例: 東京) から遠い利用者は、キャッシュが外れるたびに関数まで往復する。
- 無料枠を超えたときの振る舞いが候補で違う。Netlify Free はサイトが止まり、Vercel Hobby は最長 30 日その機能が使えなくなり、GitHub Pages はレート制限 (429) がかかりうる。CloudFront の定額プランは止まらず配信が調整される。災害時のようにアクセスが急に増える地図では、止まる候補を避けるか、有料プランで上限と予算を決めておく。
- 無料プランの商用利用: Vercel Hobby は非商用だけ、GitHub Pages はオンラインビジネスの無料ホスティングとしての利用を禁じる。自治体や企業の地図、広告や決済のある地図は、有料プランか他の候補にする。Cloudflare、Netlify、AWS の無料枠の商用利用の条件は未確認である。
- GitHub Pages は Git のリポジトリに入れるので、大きなデータを差し替えるたびに履歴が膨らむ (推測)。データは別の置き場所に置き、アプリだけを Pages に置く分け方がある。
- S3 は HTTP/1.1 だけを話すので、多数の Range を並べるタイル読みでは CloudFront などを前に置く ([cloud-native-formats](../formats/cloud-native-formats.md))。
- `r2.dev` の URL は本番に使わない。キャッシュが効かず、レート制限で 429 を返す。
- Range と圧縮: 配信時に `Content-Encoding` をかけると範囲が圧縮後のバイトを指す。PMTiles は形式の中で圧縮し、配信時の圧縮をかけない ([cloud-native-formats](../formats/cloud-native-formats.md))。CloudFront の Range も圧縮後の大きさで数える。

## 出典

確かめた日はすべて 2026-11-11 である。

- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits (公開サイト 1 GB、帯域 100 GB/月 と 1 時間 10 ビルドの soft limit、10 分のタイムアウト、429、商用の禁止)
- https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github (50 MiB で警告、100 MiB で拒否、ブラウザは 25 MiB)
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages (apex と www)
- https://developers.cloudflare.com/pages/platform/limits/ (Pages のファイル数、25 MiB、ビルド回数、独自ドメイン数)
- https://developers.cloudflare.com/pages/platform/serving-pages/ (Pages は Range に 200、206 は作業中、配備までキャッシュ、ETag)
- https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/ (Workers の静的アセットは Range に 200、`run_worker_first`、アセットへのリクエストは無料で無制限)
- https://developers.cloudflare.com/cache/concepts/default-cache-behavior/ (キャッシュの 512 MB と 5 GB、HTML と JSON は既定でキャッシュしない)
- https://developers.cloudflare.com/r2/pricing/ 、 https://developers.cloudflare.com/r2/platform/limits/ 、 https://developers.cloudflare.com/r2/buckets/public-buckets/ (R2 の無料枠、オブジェクトの上限、`r2.dev` の制限)
- https://vercel.com/docs/limits (ソースのアップロード Hobby 100 MB、Pro 1 GB、CLI 配備 15,000 ファイル)
- https://vercel.com/docs/plans/hobby (Hobby の量、超えたら 30 日待つ、非商用、独自ドメイン 50)
- https://vercel.com/docs/caching/cdn-cache (静的ファイルの自動キャッシュ、関数の応答の条件と 10 MB、リージョンごとのキャッシュ)
- https://www.netlify.com/pricing/ 、 https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/ 、 https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/ (300 クレジット、単価、使い切るとサイトが止まる)
- https://docs.netlify.com/build/caching/caching-overview/ (静的アセットのキャッシュ、`Range` は `Netlify-Vary` に使えない)
- https://docs.fly.io/about/pricing (無料枠なし、1 ドルの試用、下り転送の単価、最小マシンの月額)
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RangeGETs.html (Range のキャッシュ、200 になる条件、50 GB と分割キャッシュ)
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-limits.html (キャッシュ 50 GB、ファイル数無制限、代替ドメイン名 100)
- https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/ (常に無料の枠 1 TB と 1,000 万リクエスト)
- https://aws.amazon.com/cloudfront/pricing/ 、 https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/flat-rate-pricing-plan.html (定額プラン、超過時の調整、Free は 1 アカウント 3 つ)
- Range の実測: 2026-11-11 に `curl -r 0-99` を 1 回ずつ送った。https://maplibre.org/favicon.ico と https://pmtiles.io/ (GitHub Pages、206)、https://nextjs.org/favicon.ico (Vercel、206)、https://docs.netlify.com/favicon.svg (Netlify、206)、https://r2-public.protomaps.com/protomaps-sample-datasets/cb_2018_us_zcta510_500k.pmtiles (R2、206)、https://a0.awsstatic.com/libra-css/images/site/fav/favicon.ico (S3 + CloudFront、206)、https://fly.io/static/images/favicon/favicon-32x32.png (Fly.io、206)

## 未確認のこと

- Cloudflare Pages と Workers の静的アセットの Range を実物で確かめていない。Pages のホストと分かる静的ファイル (`*.pages.dev`) に Range を送ったが、Functions を通る応答である可能性を外せなかった。公式文書の 200 をそのまま採った。
- Cloudflare Pages の静的アセットの帯域とリクエストの上限、超えたときの振る舞い。
- Cloudflare、Netlify、AWS の無料枠を商用に使う条件 (各社の利用規約は読んでいない)。
- Vercel と Netlify の 1 ファイルの上限、Netlify のサイト全体の上限。
- Netlify Free で止まったサイトがいつ戻るか (次の請求期間と推測されるが文書に書かれていない)。
- GitHub Pages の独自ドメインの数と、応答ヘッダー (`cache-control` など) を変える方法の有無。Git LFS のファイルを Pages が配るか。
- Fly.io に CDN キャッシュがあるか。Next.js の `public/` が Range に 206 で答えるか (ラズリマップが PMTiles を返していることから答えると推測される)。
- CloudFront の定額プランで、配信が調整されたときの具体的な速さ。
- 観察した各サービスが実際にどの設定で配っているか (外から見た応答ヘッダーで推し量っただけである)。
