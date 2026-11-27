---
financial: commercial
organization: corp-ent
first_seen: 2008-06-18
first_seen_by: wayback
---

# ベルク 店舗情報・チラシ

- URL: https://www.belc.jp/shop
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、スーパー、食品スーパー、ベルク、Belc、クルベ、埼玉県、北関東、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 埼玉県を中心に関東圏で展開する食品スーパー「ベルク」の店舗を地域・設備条件から検索し、チラシや地図を確認できる公式店舗情報サイト |
| 提供する価値 | 都道府県や店舗名、サービス設備から近くのベルクを探し、店舗詳細ページでデジタルチラシ (DELISH KITCHEN 連携) や Google マップの埋め込み地図を確認できる |
| 想定する利用者 | ベルク各店舗への来店を予定している一般客、特売チラシや店舗設備を調べたい買い物客 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗情報サイト単体の売上は 0 円。連結営業収益 約 4,234 億円 (2026 年 2 月期) の実店舗送客に貢献 |
| 運営 | 企業 (株式会社ベルク) |
| 推定の運用費 | 推測: 月数万〜十数万円。Drupal CMS と nginx + Varnish の運用費に加え、Google Maps API (周辺検索用キー設定を確認) の利用料がかかる可能性がある |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | トップ (`/shop`) には埋め込み地図なし。個別店舗ページ (`/shop/0076` 等) 内に Google マップの `iframe` (`https://www.google.com/maps/embed?pb=...`) を埋め込み。HTML 内に `google_map_api_key` および `google_map_api_key_geo` の設定値も確認 |
| フレームワーク | Drupal (`/sites/default/files/js/...`, `/modules/contrib/...`)、jQuery 3.1.1 / 3.6.0、Google カスタム検索 (`cse.google.com`) |
| 背景の地図とタイル | Google マップ (`maps/embed?pb=` および Google Maps API キー設定) |
| 投稿やデータの保存先 | Drupal CMS 上で店舗情報を管理。チラシウィジェットは DELISH KITCHEN (`chirashi.delishkitchen.tv`) を `iframe` 埋め込み |
| 配信 | nginx + Varnish キャッシュ (`server: nginx`, `via: varnish`, `x-cache: HIT, HIT`) |

メモ:

- 店舗数は 151 店舗 (ベルクおよびディスカウント型のクルベ含む、2026 年夏時点)
- Google マップへの外部リンク (`https://goo.gl/maps/...`) も店舗詳細ページに併設されている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社ベルク
- 埋め込み地図: Google マップ / Google Maps Platform
- チラシウィジェット: DELISH KITCHEN
