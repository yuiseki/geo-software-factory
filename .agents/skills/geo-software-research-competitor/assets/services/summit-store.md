---
financial: commercial
organization: corp-ent
first_seen: 2020-08-09
first_seen_by: wayback
---

# サミット 店舗検索・チラシ情報

- URL: https://www.summitstore.co.jp/store/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、スーパー、食品スーパー、サミット、サミットストア、住友商事、チラシ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 首都圏の食品スーパー「サミットストア」の店舗を都県別・店舗名から検索し、チラシや営業時間を確認できる公式店舗情報サイト |
| 提供する価値 | 東京・神奈川・埼玉・千葉のサミット店舗を一覧から探し、店舗ごとの営業時間やチラシ、サービス設備を確認できる |
| 想定する利用者 | サミットストアへの来店を予定している一般客、近隣店舗のチラシや営業時間を調べたい買い物客 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。営業収益 約 3,748 億円 (2026 年 3 月期) の実店舗送客に貢献 |
| 運営 | 企業 (サミット株式会社 / 住友商事グループ) |
| 推定の運用費 | 推測: 月数万円。Amazon S3 + CloudFront による静的 SPA ホスティングと WordPress API サーバーの運用費が中心 |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (トップ `/store/` および店舗詳細 `/store/tokyo/post/?id=215` の一次取得は Nuxt.js SPA のシェル HTML とエントリ JS `DtCURSw9.js` のみで、JS 内に Google Maps 等の直接記述は確認されず。実際の店舗データ取得後の描画は未確認) |
| フレームワーク | Nuxt.js (`/_nuxt/DtCURSw9.js`、Vue.js ベースの SPA) |
| 背景の地図とタイル | 未確認 (ビルド済み主要 JS チャンクからは外部地図 API の URL は確認されず) |
| 投稿やデータの保存先 | ヘッドレス WordPress の REST API (`public.wpApiUrl`、画像パスに `wp-content/uploads/` を参照) |
| 配信 | Amazon S3 + Amazon CloudFront (`server: AmazonS3`, `via: CloudFront`, `x-cache: Hit from cloudfront`) |

メモ:

- 店舗数は 137 店舗 (2026 年 3 月期末時点)
- S3 + CloudFront 上に Nuxt.js の静的 SPA をホストし、WordPress REST API から店舗データを取得するモダンなヘッドレス CMS 構成を採用している

データの出どころ (2026-11-17):

- 店舗データ: サミット株式会社
