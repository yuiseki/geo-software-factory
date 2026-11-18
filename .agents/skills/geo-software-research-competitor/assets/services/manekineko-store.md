---
financial: commercial
organization: corp-ent
---

# カラオケまねきねこ 店舗一覧・店舗検索

- URL: https://www.karaokemanekineko.jp/locations/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、カラオケまねきねこ、まねきねこ、カラオケ、コシダカ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のカラオケまねきねこ店舗をエリアや設備条件から検索し、各店舗の料金表やアクセス地図を確認できる公式店舗一覧ページ |
| 提供する価値 | 持ち込み可否や営業時間、部屋タイプ、料金体系を店舗ごとに確認でき、Google マップの埋め込み地図と経路案内リンクから迷わず来店できる |
| 想定する利用者 | ヒトカラやグループ利用で手頃な料金のカラオケ店舗を探している学生・一般客 |
| 商用か非商用か | 商用 (カラオケまねきねこ各店舗への来店集客およびアプリ予約誘導のために提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。全国店舗の室料・ドリンク売上に貢献 |
| 運営 | 企業 (株式会社コシダカ / 株式会社コシダカホールディングス) |
| 推定の運用費 | 推測: 月数万〜数十万円。WordPress + nginx + Amazon CloudFront による配信費が中心で、地図は Google マップの無料 iframe 埋め込みを利用しているため地図 API 課金は抑えられている |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps Embed (`iframe` による `https://www.google.com/maps?output=embed&...` を各店舗詳細ページに埋め込み) + Google マップ経路案内リンク (`https://www.google.com/maps/dir/?api=1&...`) |
| フレームワーク | WordPress (`/wp-content/themes/omaneki-web/`) + jQuery + GSAP |
| 背景の地図とタイル | Google マップ (Embed iframe) |
| 投稿やデータの保存先 | WordPress (自社管理の店舗投稿データ、`/locations/<pref>/<city>/<store>/`) |
| 配信 | nginx + Amazon CloudFront (`server: nginx`、`via: ...cloudfront.net`) |

メモ:

- `/locations/` で店舗検索・一覧を提供し、個別店舗ページ (例: `/locations/gunma/maebashi/aqeru-maebashi-store/`) 内に Google マップの埋め込み `iframe` と経路案内リンクを表示している
- フォームスパム対策として Cloudflare Turnstile も導入されている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社コシダカ自社管理の店舗情報
- 背景地図: Google マップ (iframe 埋め込み)
