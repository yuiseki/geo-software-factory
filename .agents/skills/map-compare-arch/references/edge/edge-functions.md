# CDN のエッジ関数

対象: Cloudflare Workers (R2、KV、D1、Durable Objects を含む)、Fastly Compute、AWS Lambda@Edge と CloudFront Functions、Deno Deploy、Vercel、Netlify の Edge Functions

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |

## 候補ごとの制約

数字は 2026-11-10 時点の各社公式ドキュメントの既定値である。多くは申請で引き上げられる。

| 候補 | CPU 時間の上限 | メモリの上限 | 配れるコード・Wasm の大きさ | 置けるデータ (オブジェクトストレージ、KV、DB) | Range リクエスト | 料金の単位 | 出典 |
|---|---|---|---|---|---|---|---|
| Cloudflare Workers Free | 1 リクエストあたり 10 ms | 1 isolate あたり 128 MB (JS ヒープと Wasm の確保を含む) | 非圧縮 64 MiB。圧縮後の上限はない。静的アセットは 1 版あたり 20,000 ファイル、1 ファイル 25 MiB | R2 (無料枠 10 GB-月)、KV (値 25 MiB まで、1 日 1 GB 保存)、D1 (1 DB 500 MB、アカウント 5 GB)、Durable Objects (SQLite、アカウント 5 GB) | R2 の `get()` は `range` (offset、length、suffix) を受ける。Workers の静的アセットは Range を無視して 200 で全体を返す | 1 日 10 万リクエストまで無料 | [limits](https://developers.cloudflare.com/workers/platform/limits/)、[pricing](https://developers.cloudflare.com/workers/platform/pricing/)、[R2 API](https://developers.cloudflare.com/r2/api/workers/workers-api-reference/)、[静的アセットの制限](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/) |
| Cloudflare Workers Paid | 既定 30 秒、`limits.cpu_ms` で 5 分まで | 128 MB | 非圧縮 64 MiB。静的アセットは 1 版あたり 100,000 ファイル、1 ファイル 25 MiB | R2 (Standard 0.015 ドル/GB-月、下り転送無料)、KV (値 25 MiB、同じキーへの書き込みは毎秒 1 回)、D1 (1 DB 10 GB、アカウント 1 TB、1 クエリ 30 秒)、Durable Objects (SQLite で 1 オブジェクト 10 GB、キーと値の合計 8 MB) | Free と同じ | 月 5 ドル。1,000 万リクエストと 3,000 万 CPU ms を含み、超過は 100 万リクエストあたり 0.30 ドル、100 万 CPU ms あたり 0.02 ドル。R2 は Class A 100 万回 4.50 ドル、Class B 100 万回 0.36 ドル | 同上、[D1 limits](https://developers.cloudflare.com/d1/platform/limits/)、[DO limits](https://developers.cloudflare.com/durable-objects/platform/limits/)、[KV limits](https://developers.cloudflare.com/kv/platform/limits/) |
| Cloudflare Containers | インスタンス型で決まる (lite 1/16 vCPU から standard-4 の 4 vCPU まで) | 256 MiB から 12 GiB | イメージはインスタンスのディスクまで (2 GB から 20 GB)。アカウント合計 50 GB | コンテナ内のディスクは 2 GB から 20 GB | 中で動かすサーバー次第 | 制限ページには料金が載っていない (未確認) | [Containers limits](https://developers.cloudflare.com/containers/platform-details/limits/) |
| Fastly Compute | 1 リクエストあたり 50 ms、実行時間は 2 分 (試用は 60 秒) | ヒープ 128 MB、スタック 1 MB | コンパイル後のパッケージ 100 MB | KV Store (1 ファイル 25 MB、申請で 100 MB まで、5 ストア込み)、キャッシュは 1 オブジェクト 100 MB | 公式ページで確かめられなかった (未確認) | 無料枠は月 1,000 万リクエストと 1 億 vCPU ms。超過は 100 万リクエストあたり 0.50 ドルから、100 万 vCPU ms あたり 0.05 ドルから。Starter は月 500 ドル | [Compute resource limits](https://docs.fastly.com/products/compute-resource-limits)、[pricing](https://www.fastly.com/pricing) |
| AWS CloudFront Functions | 数値ではなく compute utilization (上限に対する割合) で示される | 2 MB | 10 KB (引き上げ不可) | CloudFront KeyValueStore (1 ストア 5 MB、値 1 KB、キー 512 B)。ネットワーク、ファイルシステム、リクエスト本文には触れない | 関数からは取りに行けない | 100 万回の呼び出しあたり 0.10 ドル、KVS 読み込み 100 万回 0.03 ドル。毎月 200 万回の呼び出しが無料 | [Quotas](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-limits.html)、[制約](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-function-restrictions.html)、[料金](https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/) |
| AWS Lambda@Edge | タイムアウト 30 秒 (Quotas ページの記載) | 「Lambda の上限と同じ」と書かれている | 圧縮 50 MB。レイヤー、コンテナイメージ、arm64、環境変数は使えない。us-east-1 で作る | 関数から S3、DynamoDB などリージョンのサービスへネットワークで取りに行ける。関数が生成するレスポンスは viewer イベントで 40 KB、origin イベントで 1 MB | S3 への Range 付き GetObject は関数のコード次第 (推測) | 100 万リクエストあたり 0.60 ドルと GB 秒あたり 0.00005001 ドル (1 ms 単位)。無料枠はない | [Quotas](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-limits.html)、[制約](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-at-edge-function-restrictions.html)、[料金](https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/) |
| Deno Deploy | 1 リクエストあたりの上限は公式ページに書かれていない。月の Active CPU 時間で課金 (Free 10 時間、Pro 50 時間) | 512 MB (制限ページ)。料金ページでは既定 768 MB の割り当てで課金し、Pro と Builder は引き上げられる、とあり記述が食い違う | デプロイ全体 (ソースと静的ファイル) で 1 GB | Deno KV (Free 1 GiB、Pro 5 GiB、Builder 10 GiB) | 未確認 | Free 0 ドル、Pro 月 20 ドル、Builder 月 200 ドル。リクエスト 100 万あたり 2 ドル、Active CPU 1 時間 0.10 ドル、メモリ時間 GiB 時 0.025 ドル、転送 GiB 0.20 ドル | [pricing and limits](https://docs.deno.com/deploy/pricing_and_limits/)、[pricing](https://deno.com/deploy/pricing) |
| Vercel Edge runtime | 25 秒以内にレスポンスを始め、ストリーミングは 300 秒まで | Edge 専用の数値は見つからなかった (Node.js の Vercel Functions は Hobby 2 GB、Pro 4 GB) | gzip 後で Hobby 1 MB、Pro 2 MB、Enterprise 4 MB。`WebAssembly.instantiate` は import 文で読み込んだ Wasm に限る | ファイルシステムは使えない。外部ストレージへ fetch する | fetch 先次第 | Active CPU 時間と割り当てメモリ時間で課金 | [Edge runtime](https://vercel.com/docs/functions/runtimes/edge)、[Functions limits](https://vercel.com/docs/functions/limitations) |
| Netlify Edge Functions | 1 リクエストあたり 50 ms (待ち時間は数えない)、レスポンスヘッダーは 40 秒以内 | 配備した Edge Functions 一式で 512 MB | 圧縮後 20 MB | 公式の制限ページには保存先の記載がない | fetch 先次第 | 呼び出し回数 (invocations)。キャッシュから返した分は数えない。プランごとの量は料金ページ | [limits](https://docs.netlify.com/build/edge-functions/limits/)、[usage and billing](https://docs.netlify.com/build/edge-functions/usage-and-billing/) |

## 地図プロダクトでの使いどころ

- 保存: タイルの本体はオブジェクトストレージに 1 本の PMTiles として置き、エッジ関数が Range 読みで切り出すのが基本形である。Cloudflare では R2 の `get()` が Range を受け、下り転送が無料である。KV は値 25 MiB、D1 は 1 DB 10 GB (Paid) が上限なので、タイル群そのものより索引やメタデータ、利用者ごとの設定に向く。CloudFront KeyValueStore は 1 ストア 5 MB なので API キーや許可オリジンの表を置く程度に限られる。
- 計算: (リクエスト時のタイル計算、検索、ルート検索が動くか)
  - PMTiles から z/x/y を引いて返す処理は Workers Free の 10 ms でも動く構成として公式手順がある (protomaps の Cloudflare 向け手順)。
  - リクエスト時のタイル生成 (GeoJSON や DB からの MVT 化) は、Workers Paid の CPU 30 秒から 5 分、メモリ 128 MB の範囲に入る小さな範囲なら動く (推測)。Fastly と Netlify は 50 ms なので重い生成は向かない (推測)。
  - DuckDB の Wasm は 30 MB を超える本体があり、Workers 向けに削った `@ducklings/workers` でも約 9.7 MB で Paid プランが前提と README に書かれている。メモリ 128 MB の中で大きな Parquet を扱うのは難しい (推測)。
  - SQLite は D1 と Durable Objects の SQLite として使える。D1 が SpatiaLite や R*Tree を有効にしているかは公式の制限ページに書かれていない (未確認)。
  - ルート検索 (OSRM や Valhalla) はグラフを常駐させるメモリが要るので、128 MB の isolate には収まらない (推測)。必要なら Cloudflare Containers (最大 12 GiB) か、リージョンのサーバーに置く。
- 表現: エッジ関数は描画しない。MVT、TileJSON、スタイル JSON、スプライトを返し、描画はブラウザやアプリの MapLibre が行う。認証 (API キーと Origin の照合) やスタイルの書き換えをエッジで済ませると、オリジンに届くリクエストを減らせる。

## 地図の実装例

- protomaps の PMTiles を Cloudflare Workers と R2 で配る構成。`protomaps/PMTiles` リポジトリの `serverless/cloudflare` にある Worker を使い、R2 バケットを `BUCKET` として束ね、`/NAME/z/x/y.mvt` と `/NAME.json` (TileJSON) を返す。既定の `Cache-Control` は `public, max-age=86400` で、キャッシュは独自ドメインのゾーンでしか効かない (`workers.dev` では効かない)。同じリポジトリに `serverless/aws` もある。
- go-pmtiles の `pmtiles serve` はバケットやローカルの PMTiles を z/x/y で配るサーバーで、エッジ関数を使わない場合の比較対象になる。

## 落とし穴

- Workers の静的アセット (Workers Assets) は Range を無視して 200 で全体を返す。PMTiles をアセットとして置くと Range 読みにならないので、R2 に置くか、`run_worker_first` で Worker を通して 206 を組み立てる。アセットは 1 ファイル 25 MiB までなので大きな PMTiles はそもそも置けない。
- protomaps の手順では、R2 は他のクラウドストレージより遅く「500ms or higher」と書かれている。キャッシュに当たらないタイルの体感速度を見積もる時に効く。
- R2 の Web 画面からのアップロードは 300 MB まで。大きなファイルは rclone などを使う。
- Cloudflare のキャッシュ全消去 (Purge Everything) はゾーン全体に効くので、タイル配信用にゾーンを分けることが protomaps の手順で勧められている。ただし Free プランでも URL、ホスト名、タグ、プレフィックスの単位で消せるので、消し方を絞ればゾーンを分けなくてもよい (https://developers.cloudflare.com/cache/how-to/purge-cache/、2026-11-10 確認)。
- Vercel は Edge runtime から Node.js への移行を勧めており、Next.js 16.3 以降では `runtime = 'edge'` が使えない。新規に Edge runtime を前提にしない。
- Vercel Edge runtime は実行時にバイト列から Wasm をコンパイルできない (import 文で読み込んだ Wasm だけ)。Wasm を R2 などから取ってくる構成はとれない。
- Lambda@Edge は viewer イベントで返せるレスポンスが 40 KB までで、タイル 1 枚を返すにも足りないことがある (推測)。origin イベントでも 1 MB までである。
- CloudFront Functions はリクエスト本文にもネットワークにも触れないので、タイルの中身を扱う処理は書けない。URL の書き換えや API キーの照合向けである。
- Workers の Free は CPU 10 ms、サブリクエスト 50 回までなので、1 リクエストで R2 を何度も読む処理 (PMTiles のディレクトリを複数段たどる場合など) は回数に注意する (推測)。

## 出典

- https://developers.cloudflare.com/workers/platform/limits/ (Workers の CPU、メモリ 128 MB、スクリプト 64 MiB、サブリクエスト、静的アセットの件数とファイルサイズ)
- https://developers.cloudflare.com/workers/platform/pricing/ (Workers、R2、KV、D1、Durable Objects の料金単位と無料枠)
- https://developers.cloudflare.com/r2/api/workers/workers-api-reference/ (R2 `get()` の `range` オプション)
- https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/ (静的アセットは Range 非対応で 200 を返す、アセットへのリクエストは無料)
- https://developers.cloudflare.com/kv/platform/limits/ (KV の値 25 MiB、キー 512 B、同じキーへの書き込み毎秒 1 回)
- https://developers.cloudflare.com/d1/platform/limits/ (D1 の DB サイズ、アカウント上限、クエリ 30 秒)
- https://developers.cloudflare.com/durable-objects/platform/limits/ (DO の SQLite 容量と CPU)
- https://developers.cloudflare.com/containers/platform-details/limits/ (Containers のインスタンス型とアカウント上限)
- https://docs.protomaps.com/deploy/cloudflare (PMTiles を Workers と R2 で配る手順、キャッシュ、R2 の遅延、300 MB のアップロード制限)
- https://github.com/protomaps/PMTiles (`serverless/cloudflare` と `serverless/aws` があることを GitHub API で確認)
- https://docs.fastly.com/products/compute-resource-limits (Fastly Compute のヒープ、CPU、実行時間、パッケージ、KV Store)
- https://www.fastly.com/pricing (Fastly Compute の無料枠と料金単位、プラン名)
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-limits.html (CloudFront Functions と Lambda@Edge と KeyValueStore の Quotas)
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-function-restrictions.html (CloudFront Functions の制約、compute utilization)
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-at-edge-function-restrictions.html (Lambda@Edge の制約、us-east-1、使えない機能)
- https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/ (CloudFront Functions、KVS、Lambda@Edge の単価)
- https://docs.deno.com/deploy/pricing_and_limits/ と https://deno.com/deploy/pricing (Deno Deploy のデプロイ 1 GB、メモリ、プランと料金)
- https://vercel.com/docs/functions/runtimes/edge と https://vercel.com/docs/functions/limitations (Vercel Edge runtime のコードサイズ、実行時間、Wasm の制約、Node.js 移行の推奨、課金単位)
- https://docs.netlify.com/build/edge-functions/limits/ と https://docs.netlify.com/build/edge-functions/usage-and-billing/ (Netlify Edge Functions の制限と課金単位)
- https://ducklings-api.pages.dev/_ducklings/workers/ (Workers 向け DuckDB Wasm が約 9.7 MB で Paid プラン前提。検索結果の要約で確認)

## 未確認のこと

- Fastly Compute でバックエンド (オブジェクトストレージ) に Range 付きで取りに行き、その一部を返す処理の公式な説明。
- CloudFront Functions の最大実行時間の具体的な数値 (公式は compute utilization の割合でしか示していない)。
- Lambda@Edge の viewer イベントでのメモリとタイムアウトの上限が、以前の 128 MB と 5 秒から変わったのか。現在の Quotas ページは「Lambda と同じ」「30 秒」とだけ書いている。
- Deno Deploy の 1 リクエストあたりの CPU 上限と、制限ページ (512 MB) と料金ページ (既定 768 MB) のメモリの食い違い。
- Vercel Edge runtime のメモリ上限の数値。
- Netlify Edge Functions のプランごとの invocations の量と単価。
- Cloudflare Containers の料金単位と、GA かベータか。
- D1 で SQLite の R*Tree、FTS5、SpatiaLite が使えるか。
- DuckDB Wasm を Workers で動かした時に、実際の Parquet や PMTiles に対して 128 MB に収まるかの実測。
