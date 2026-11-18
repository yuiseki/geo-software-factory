---
financial: commercial
organization: corp-ent
---

# キャンドゥ 店舗検索

- URL: https://shopinfo.cando-web.co.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、キャンドゥ、CanDo、100円ショップ、100均、Leaflet、カンリー、Canly、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の 100円ショップ「Can★Do (キャンドゥ)」の店舗をエリアや条件、地図から検索できる公式店舗検索サイト |
| 提供する価値 | 各店舗の住所、電話番号、営業時間、決済手段 (WAON POINT やキャッシュレス決済等)、アクセス方法、店舗からのお知らせを一目で確認できる |
| 想定する利用者 | 日用品や雑貨の購入で最寄りのキャンドゥ店舗や利用可能な決済方法を確認したい一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客のために株式会社キャンドゥが提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上および電子マネー・ポイント施策の案内による来店促進に貢献する集客基盤 |
| 運営 | 企業 (株式会社キャンドゥ) |
| 推定の運用費 | 推測: 月数万円〜十数万円。店舗情報管理・SEO 支援 SaaS「カンリー (Canly)」の店舗ページ基盤と CloudFront 配信を利用している |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (`__NEXT_DATA__` 内の設定値 `"mapMapSetting":"leaflet"` および `"mapClusterSetting":"use"` を確認。参考の事前調査では Google Maps と記載されていたが、2026-11-17 時点のページ設定は Leaflet となっている) |
| フレームワーク | Next.js (`x-powered-by: Next.js`、`__NEXT_DATA__`、`/map` や `/detail/[storeCode]` ルートを持つ) + カンリー (Canly) 店舗検索基盤 (`meocloud-image.can-ly.com`) |
| 背景の地図とタイル | 未確認 (2026-11-17 のトップページ HTML および初期 JS チャンクからはタイル供給元の URL を特定できず。動的ロードまたは `/map` ルート側で設定) |
| 投稿やデータの保存先 | カンリー (Canly) クラウド CMS (`meocloud-image.can-ly.com` で画像等を配信) |
| 配信 | Amazon CloudFront (`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 取得 (`https://shopinfo.cando-web.co.jp/`) では Next.js の SSR HTML (`__NEXT_DATA__`) 内に `"mapMapSetting":"leaflet"`、`mapClusterSetting: "use"` などの地図設定が含まれていることを確認した
- 店舗情報の画像アセットは `https://meocloud-image.can-ly.com/...` から配信されており、株式会社カンリー (Canly) の店舗検索 CMS 基盤で運用されている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社キャンドゥ自社管理の店舗情報 (カンリー店舗検索基盤経由)
- 背景地図: 未確認 (描画設定は Leaflet)
