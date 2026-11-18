---
financial: commercial
organization: corp-ent
---

# エニタイムフィットネス 店舗一覧・店舗検索

- URL: https://www.anytimefitness.co.jp/list/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、エニタイムフィットネス、Anytime Fitness、24時間ジム、フィットネス、Fast Fitness Japan、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国 1,200 店舗以上のエニタイムフィットネスを都道府県やエリアから探し、店舗詳細や Google マップへの導線を確認できる公式店舗一覧ページ |
| 提供する価値 | 24 時間年中無休のマシン特化型ジムの店舗を地域ごとに探し、住所・アクセス・設備・Web 入会への導線をすばやく確認できる |
| 想定する利用者 | エニタイムフィットネスへの入会を検討している一般利用者、および全国相互利用のために訪問先の店舗を探す会員 |
| 商用か非商用か | 商用 (24 時間フィットネスジムの入会送客および相互利用会員の店舗案内として提供。検索ページの利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。株式会社Fast Fitness Japan (2025年3月期連結売上高 約180億円) の直営・FC 店舗の入会および利用継続に貢献 |
| 運営 | 企業 (株式会社Fast Fitness Japan) |
| 推定の運用費 | 推測: 月数万〜数十万円。Apache + Amazon CloudFront による Web 配信費が中心で、地図は Google マップへの外部リンクのため地図 API の従量課金は抑えられている |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 埋め込み地図なし (店舗詳細ページで Google マップの検索 URL `https://www.google.com/maps/search/?api=1&query=<lat>,<lng>` へ外部リンク) |
| フレームワーク | jQuery 3.6.0 (`jquery-3.6.0.min.js`、検索フォーム遷移は `/assets/js/list/listtop.js`) |
| 背景の地図とタイル | ページ内での背景地図タイル読み込みなし (リンク先の Google マップで表示) |
| 投稿やデータの保存先 | サーバー側で生成された HTML (`/list/`、`/kanto/tokyo/`、`/<store>/` 等) |
| 配信 | Apache + Amazon CloudFront (`server: Apache`、`via: ...cloudfront.net`、`x-cache: Hit from cloudfront`) |

メモ:

- `/list/` および都道府県別ページ (`/kanto/tokyo/`) には埋め込み地図はなく、各店舗ページ (例: `/nishitokyoyagisawa/`) には緯度経度付きの Google マップリンク (`maps/search/?api=1&query=...`) が置かれている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社Fast Fitness Japan 自社管理の店舗情報
- 背景地図: ページ内埋め込みなし (Google マップへの外部リンク)
