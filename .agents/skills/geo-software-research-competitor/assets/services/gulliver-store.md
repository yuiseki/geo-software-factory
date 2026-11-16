# ガリバー (Gulliver) 店舗検索

- URL: https://221616.com/maps/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、中古車、買取、販売、ガリバー、IDOM、Gulliver、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のガリバー (IDOM) の中古車販売・買取店舗を現在地・エリア・条件から検索し、地図上に表示する公式店舗検索サイト |
| 提供する価値 | 近くのガリバー店舗や大型展示場 (WOW!TOWN 等) の場所・営業時間・取扱サービスを地図から確認し、来店予約や買取査定予約へ進める |
| 想定する利用者 | 中古車の購入・売却 (買取査定) を検討している一般消費者 |
| 商用か非商用か | 商用 (実店舗への来店予約・買取査定予約の送客基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。全国約 430〜490 拠点の中古車販売・買取事業の成約に貢献 |
| 運営 | 企業 (株式会社IDOM) |
| 推定の運用費 | 推測: 月数十万円。Google Maps Platform の利用料および Next.js サーバー・Cloudflare の運用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (Next.js の静的チャンク JS 内に `maps.googleapis` および `google.maps` の呼び出しを確認) |
| フレームワーク | Next.js (`__NEXT_DATA__`、`x-powered-by: Next.js`、`/maps/_next/static/...`) |
| 背景の地図とタイル | Google マップ (Google Maps Platform) |
| 投稿やデータの保存先 | 株式会社IDOM の店舗データベース (Next.js SSR / API 経由で配信) |
| 配信 | Cloudflare + Google (`server: cloudflare`、`CF-Ray: ...-NRT`、`via: 1.1 google`) |

メモ:

- 日本の中古車大手の店舗検索として、モダンな Next.js SPA/SSR 構成と Cloudflare CDN の組み合わせで配信されている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社IDOM 自社管理の店舗情報
- 背景地図: Google (Google Maps Platform)
