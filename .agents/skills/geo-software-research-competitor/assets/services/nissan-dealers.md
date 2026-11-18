---
financial: commercial
organization: corp-ent
---

# 日産 販売店(ディーラー)検索

- URL: https://www3.nissan.co.jp/dealers.html
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、ディーラー検索、販売店検索、日産、NISSAN、試乗、新車、中古車、EV充電、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の日産販売店 (ディーラー) を現在地・住所・販売会社・サービス条件から検索して地図上に表示する公式ディーラー検索サイト |
| 提供する価値 | 試乗予約、新車・中古車相談、EV 急速充電設備の有無、点検・整備対応など目的に合った日産販売店を地図と一覧から見つけられる |
| 想定する利用者 | 日産車の購入・試乗を検討している顧客、メンテナンスや EV 充電場所を探す日産車オーナー |
| 商用か非商用か | 商用 (全国の販売会社・店舗への来店・試乗・整備予約への送客基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 検索サイト単体の売上は 0 円。新車・中古車販売およびアフターサービス事業のリード獲得・送客に貢献 |
| 運営 | 企業 (日産自動車株式会社) |
| 推定の運用費 | 推測: 月数十万〜百万円規模。Google Maps Platform の利用料に加え、グローバル共通 Web 基盤 (AEM / CloudFront / API Gateway) の運用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (`dealers.html` 内の設定 JSON で `"mapProvider":"google"` を確認) |
| フレームワーク | Adobe Experience Manager (AEM) + 日産グローバル共通基盤 (`pace-omni-nav`、`nissan_modernisation`、`/content/nissan_prod/ja_JP/index/dealers/jcr:content.proxy.json`) |
| 背景の地図とタイル | Google マップ (Google Maps Platform) |
| 投稿やデータの保存先 | 日産自動車 API Gateway (`apigatewayEnabledServices` に `/v1/dealers`、`/v2/dealers` を確認) |
| 配信 | Amazon CloudFront (`via: 1.1 ...cloudfront.net (CloudFront)`、`x-amz-cf-pop: NRT12-P2`、AEM Dispatcher キャッシュ) |

メモ:

- グローバル展開される日産自動車の共通デジタル基盤 (`pace-omni-nav` / AEM) 上に構築されており、販売店データは `/v1/dealers` および `/v2/dealers` の API Gateway 経由で取得する設計になっている

データの出どころ (2026-11-17):

- 販売店データ: 日産自動車株式会社および全国の日産販売会社管理の拠点情報
- 背景地図: Google (Google Maps Platform)
