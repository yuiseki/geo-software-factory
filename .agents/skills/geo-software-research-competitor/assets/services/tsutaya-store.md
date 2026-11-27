---
financial: commercial
organization: corp-ent
first_seen: 2021-06-12
first_seen_by: wayback
---

# TSUTAYA／蔦屋書店 店舗一覧

- URL: https://store.tsite.jp/portal/storelist/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、TSUTAYA、蔦屋書店、書店、レンタル、T-SITE、営業時間、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の蔦屋書店・T-SITE・TSUTAYA 各店の店舗一覧を地域別にまとめ、各店の詳細ページへ案内するポータルページ |
| 提供する価値 | 地域の蔦屋書店や TSUTAYA を一覧から探し、各店舗の営業時間、アクセス、イベント情報ページへ素早く移動できる |
| 想定する利用者 | 書籍や雑貨の購入、カフェ利用、DVD/CD レンタルやイベント参加のために店舗を探す一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客のためにカルチュア・コンビニエンス・クラブ株式会社が提供。利用料は無料) |
| 推定の売上 | 推測: 店舗一覧単体の売上は 0 円。全国の TSUTAYA・蔦屋書店の集客に貢献する案内基盤 |
| 運営 | 企業 (カルチュア・コンビニエンス・クラブ株式会社) |
| 推定の運用費 | 推測: 月数万円〜十数万円。一覧ページ自体は埋め込み地図を持たず Cloudflare 配信費のみだが、一部の店舗個別アクセスページでは Google Maps API を利用している |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 一覧ページ (`/portal/storelist/`) は埋め込み地図なし (HTML リスト)。個別店舗ページの一部 (例: 代官山 蔦屋書店 `/daikanyama/access/`) では Google Maps JavaScript API と iframe 埋め込みを併用 |
| フレームワーク | jQuery (`jquery-3.4.1.min.js`) |
| 背景の地図とタイル | 一覧ページは埋め込み地図なし (一部個別店舗ページでは Google Maps を利用) |
| 投稿やデータの保存先 | 自社管理の店舗データベース (API 詳細は未確認) |
| 配信 | Cloudflare (`server: cloudflare`、`cf-ray` ヘッダ) |

メモ:

- 2026-11-17 の一次 HTTP 取得で `https://store.tsite.jp/portal/storelist/` はステータス 200 を返し、一覧ページ内には地図ライブラリや埋め込み iframe がないことを確認した
- ポータルからリンクされている `store-tsutaya.tsite.jp/store/detail` は、2026-11-17 の一次 HTTP 取得時点では `SORRY_HTML` (`noindex,nofollow`) を返した
- 一方の蔦屋書店個別ページ (`https://store.tsite.jp/daikanyama/access/`) では `maps.google.com/maps/api/js` および `https://www.google.com/maps/embed` の利用を確認した

データの出どころ (2026-11-17):

- 店舗データ: カルチュア・コンビニエンス・クラブ株式会社自社管理の店舗情報
- 背景地図: 一覧ページは埋め込みなし (個別店舗ページの一部で Google Maps を利用)
