---
financial: commercial
organization: corp-ent
---

# 白洋舎 店舗検索

- URL: https://map.hakuyosha.co.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、クリーニング、洗濯、白洋舎、白洋舍、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の白洋舍店舗・取次店をエリアや地図から検索し、営業時間や取扱サービスを確認できる公式店舗検索サイト |
| 提供する価値 | 最寄りの白洋舍店舗の場所や営業時間、集配サービス等への導線を地図付きで素早く確認できる |
| 想定する利用者 | 衣類や布団などのクリーニング持ち込み・受け取りのために白洋舍の店舗を探す一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客および宅配クリーニングサービスへの案内として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗でのクリーニング売上および集配・宅配サービスへの送客に貢献する集客基盤 |
| 運営 | 企業 (株式会社白洋舍) |
| 推定の運用費 | 推測: 月数万円。Canly (株式会社カンリー) の店舗管理 SaaS 利用料および CloudFront 配信費がかかる (Leaflet + OpenStreetMap 構成のため地図 API 従量費を抑えやすい) |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (HTML および JS バンドル内の `leaflet` 記述と参考の事前調査から確認) |
| フレームワーク | Next.js (`x-powered-by: Next.js`、`__NEXT_DATA__`) |
| 背景の地図とタイル | OpenStreetMap (参考の事前調査による。一次 HTTP 取得では Leaflet の利用を確認したが、タイル URL 自体は動的チャンク内での詳細未確認) |
| 投稿やデータの保存先 | Canly (株式会社カンリー) 店舗情報基盤 (`https://api.site.can-ly.com`、`https://meocloud-image.can-ly.com`) |
| 配信 | Amazon CloudFront (`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 観測では `x-powered-by: Next.js` と `via: ...cloudfront.net` を確認し、JS チャンク (`_app-7729e9b15c654c18.js`) 内に Canly の API (`https://api.site.can-ly.com`) が含まれていた
- 地図ライブラリに Leaflet、背景地図に OpenStreetMap を採用する SaaS 構成となっている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社白洋舍管理の店舗情報 (Canly 基盤経由で配信)
- 背景地図: OpenStreetMap (参考の事前調査による)
