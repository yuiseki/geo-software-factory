---
financial: commercial
organization: corp-smb
first_seen: 2023-01-03
first_seen_by: wayback
---

# ヴィ・ド・フランス 店舗検索

- URL: https://shop.viedefrance.co.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ベーカリーカフェ、パン屋、ヴィ・ド・フランス、VIE DE FRANCE、デリフランス、Canly、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ベーカリーカフェ「ヴィ・ド・フランス」および「デリフランス」などグループ各店舗を地域・ブランド・地図から検索できる公式店舗検索サイト |
| 提供する価値 | 都道府県・駅名・キーワード・地図から最寄りの店舗を探し、営業時間やイートイン席の有無、アクセス情報を確認できる |
| 想定する利用者 | ヴィ・ド・フランスやデリフランスへ来店したい一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗のパン・カフェ売上に貢献する集客・情報基盤 |
| 運営 | 企業 (株式会社ヴィ・ド・フランス / 山崎製パングループ。店舗情報・ストアロケーター基盤は株式会社カンリー / Canly を利用) |
| 推定の運用費 | 推測: 月十万〜数十万円。Canly のストアロケーター SaaS 利用料および地図 API 利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`shop.pronto.co.jp` と同一の Canly Next.js ストアロケーター基盤・共通チャンクを使用。`_app` バンドル内に Google Maps / Leaflet 関連モジュールを含む) |
| フレームワーク | Next.js (`x-powered-by: Next.js`、Canly ストアロケーター基盤、状態管理に Jotai) |
| 背景の地図とタイル | Google Maps (Canly 共通基盤。トップの一次取得では地図チャンク未読み込み、`/map` 等で読み込み) |
| 投稿やデータの保存先 | Canly API (`https://api.site.can-ly.com`)、画像は `https://meocloud-image.can-ly.com` |
| 配信 | Amazon CloudFront (`via: CloudFront`, `x-cache: Hit from cloudfront`) |

メモ:

- 総店舗数は約 210〜230 店舗 (ヴィ・ド・フランス、デリフランス等の複数ブランド合計)
- プロント (`shop.pronto.co.jp`) と同一の Canly 共通 Next.js チャンク (`383-a596eb3aa07a76d9.js` 等) が配信されている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社ヴィ・ド・フランス (Canly 経由で配信)
- 背景地図: Google Maps Platform
