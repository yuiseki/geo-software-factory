# クラウド上のコンテナと PaaS

対象: Google Cloud Run、AWS App Runner、Microsoft Azure Container Apps、Cloudflare Containers、Render Web Services、Fly.io。エッジ関数 (メモリ 128 MB や短い CPU 上限) に収まらない地図サーバー (Martin、tileserver-gl、Valhalla、OSRM、Pelias、PostGIS 連携 API) をクラウドで動かす置き場所として比べる。

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-13 |

数字は 2026-11-13 時点で各社公式ドキュメントおよび料金案内から確認した既定値である。料金は米ドル (USD) である。

## いつエッジ関数ではなくコンテナ・PaaS を選ぶか

- ルート検索エンジン (OSRM、Valhalla) やジオコーダー (Pelias、Nominatim) のように、グラフや索引を数百 MB から数 GB のメモリに載せる必要がある ([near-user-servers](../edge/near-user-servers.md))。
- PostGIS と接続する動的タイルサーバー (Martin、tileserver-gl) や、GDAL / Tippecanoe / DuckDB などネイティブバイナリを動かす処理がある。
- リクエストごとに数秒から数分の処理時間がかかり、エッジ関数の CPU 上限に収まらない。

## 比較表

| 候補 | Scale-to-Zero (待機時 0 円か) | CPU / メモリの上限 | 無料枠 (月額など) | 待機時・超過時の課金 | マネージド Postgres / 永続ディスク | 出典 |
|---|---|---|---|---|---|---|
| Google Cloud Run | 可 (既定 `min-instances=0` で待機時は課金なし) | 1〜8 vCPU、128 MiB〜32 GiB | 月 200 万リクエスト、180,000 vCPU 秒、360,000 GiB 秒、北米からの下り 1 GB | リクエスト処理時間 (100 ms 単位) で従量課金。`min-instances > 0` にすると待機中も課金 | Cloud SQL (PostGIS 対応)。コンテナ内のディスクは揮発性 (GCS マウント等を使う) | [Cloud Run 料金](https://cloud.google.com/run/pricing) |
| AWS App Runner | **不可** (待機中もプロビジョニング済みインスタンスが常駐し、メモリ料金が発生。完全停止には一時停止操作が要る) | 0.25〜4 vCPU、0.5〜12 GB | 永久無料枠は記載なし | 待機中もメモリ単価 (GB 時間) が課金され、処理中だけ vCPU + メモリ単価が加算 | Amazon RDS / Aurora (PostGIS 対応)。ローカルディスクは揮発性 | [App Runner 料金](https://aws.amazon.com/apprunner/pricing/) |
| Azure Container Apps (Consumption) | 可 (既定 `minReplicas=0` で待機時は課金なし) | 構成により選択 (プラン上限は要確認: 未確認) | 月 200 万 HTTP リクエスト、180,000 vCPU 秒、360,000 GiB 秒 | 稼働中は秒単位課金 (Active / Idle の単価差あり) | Azure Database for PostgreSQL (PostGIS 拡張対応) | [Container Apps 料金](https://azure.microsoft.com/pricing/details/container-apps/) |
| Cloudflare Containers | 確認中 (未確認) | インスタンス型で 1/16〜4 vCPU、256 MiB〜12 GiB | 制限ページに料金・無料枠の記載なし (未確認) | 同上 (未確認) | コンテナ内ディスク 2〜20 GB (エフェメラル)。永続状態は D1 / R2 / Durable Objects に逃がす | [Containers limits](https://developers.cloudflare.com/containers/platform-details/limits/) |
| Render Web Services | 無料プランのみ 15 分無通信でスピンダウン (有料 Starter 以上は常時起動) | Free は 0.1 CPU / 512 MB RAM。Starter ($7/月) は 0.5 CPU / 512 MB。上位プランで拡張 | 静的サイトは無料。Web Services Free は月 750 インスタンス時間、Workspace Hobby は下り 5 GB/月 | Free のスピンダウン後は数秒のコールドスタート。Workspace 帯域超過は $0.15/GB | Render Postgres Free は 1 GB、**30 日で期限切れ削除** (本番不可)。Paid は $6〜/月、永続ディスク別売 | [Render 料金](https://render.com/pricing) |
| Fly.io | 構成可能 (auto_stop_machines) | マシン型による | 新規組織に永久無料枠なし (7 日間または $1 分の試用のみ) | 従量課金 (shared-cpu-1x 256 MB で約 $2.19/月、アジア太平洋の下り $0.04/GB) | Fly Volumes (永続ディスク)、Managed Postgres | [Fly.io 料金](https://docs.fly.io/about/pricing) |

## 地図プロダクトでの使いどころ

- **個人開発や検証・低トラフィックの動的地図 API**: コールドスタート (数秒) を許容できるなら Google Cloud Run か Azure Container Apps が待機費 0 円 (かつ月の無料枠あり) で収まりやすい。
- **自治体・エンタープライズの閉域・VPC 接続 (PostGIS / RDS 連携)**: AWS (App Runner / ECS Fargate + RDS)、Google Cloud (Cloud Run + Cloud SQL)、Azure (Container Apps + Azure Database for PostgreSQL) の中から、組織が既に契約しているクラウドとリージョン (東京 / 東日本など) に合わせる。
- **小規模な常駐 Docker + PostgreSQL を手軽に立てたい**: Render (Starter $7/月 + 有料 Postgres) や Fly.io は Git 連携や Dockerfile だけで立ち上げやすい。ただし Render の無料 Postgres は 30 日で消えるため、検証以外の正本には使わない。
- **エッジ配信と組み合わせる**: タイルや静的アセットは [static-hosting](static-hosting.md) や R2/S3 + CDN に逃がし、コンテナには「動的検索・ルート計算・PostGIS クエリ」だけを置くと転送費とメモリを抑えられる。

## 落とし穴

- **AWS App Runner は Scale-to-Zero しない**: 0 リクエストでもプロビジョニング済みメモリの課金が 24 時間続く。費用上限が厳しい案件で忘れると想定外の請求になる。
- **Render 無料枠の落とし穴**: Web Service Free は 15 分無通信で停止しコールドスタートが起きるうえ、**Render Postgres Free は 30 日で自動削除**される。また Workspace Hobby の転送枠は月 5 GB と小さいため、重い GeoJSON やタイルを Web Service から直接配るとすぐ超過する。
- **コンテナ内のローカルディスクは消える**: Cloud Run、App Runner、Container Apps、Render Free のローカルディスクは再起動・再デプロイで揮発する。PMTiles や検索索引を毎回起動時にダウンロードするとコールドスタートが伸びるため、小さいデータはイメージに焼き込むか、オブジェクトストレージ (GCS / S3 / R2) から Range で読む。

## 出典

- https://cloud.google.com/run/pricing (Cloud Run の無料枠、vCPU/メモリ上限、100 ms 単位の課金、Scale-to-Zero)
- https://aws.amazon.com/apprunner/pricing/ (App Runner の vCPU/メモリ組み合わせ、Provisioned と Active の課金)
- https://azure.microsoft.com/pricing/details/container-apps/ (Azure Container Apps Consumption の無料枠と Scale-to-Zero)
- https://developers.cloudflare.com/containers/platform-details/limits/ (Cloudflare Containers のインスタンス型とディスク上限)
- https://render.com/pricing (Render の Workspace 枠、Web Services Free/Starter、Render Postgres の 30 日期限)
- https://docs.fly.io/about/pricing (Fly.io の試用枠、マシンと下り転送単価)

## 未確認のこと

- AWS ECS Fargate、Google Cloud Run、Azure Container Apps の東京リージョンにおける最新単価の正確な比較表。
- Render Postgres の PostGIS 拡張の具体的な対応状況とバージョン (公式ドキュメントでの個別確認が必要)。
- Cloudflare Containers の正式リリース後の料金体系と無料枠。
