---
financial: commercial
organization: corp-ent
first_seen: 2024-03-23
first_seen_by: wayback
---

# エディオン 店舗・チラシ検索

- URL: https://search.edion.com/e_store/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、家電量販店、エディオン、EDION、100満ボルト、チラシ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のエディオンおよび 100満ボルト等のグループ店舗を地図・条件・エリアから検索できる公式店舗・チラシ検索サイト |
| 提供する価値 | 最寄り店舗の所在地、営業時間、デジタルチラシ、取扱サービスや最寄駅からのアクセスをまとめて確認できる |
| 想定する利用者 | 家電製品や携帯電話、リフォーム相談などでエディオン店舗へ来店する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客および公式通販・アプリ連携として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗売上への送客に貢献する集客基盤 |
| 運営 | 企業 (株式会社エディオン) |
| 推定の運用費 | 推測: 月数十万円。NAVITIME Location Cloud (法人向け店舗検索 SaaS) の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME Location Cloud (HTML 内に `navitime` の参照および `e_store/spot/detail?code={{:code}}` の JsRender テンプレート構造を確認) |
| フレームワーク | jQuery 3.7.1 (`jquery-3.7.1.min.js`)、JsRender 1.0pre35、Moment.js 2.30.1、jquery.inview 1.1.2、iframeResizer |
| 背景の地図とタイル | NAVITIME 地図タイル (NAVITIME Location Cloud の標準地図基盤) |
| 投稿やデータの保存先 | NAVITIME Location Cloud 上で店舗マスタを管理し、`search.edion.com/e_store/` で配信 |
| 配信 | Apache (`server: Apache`) |

メモ:

- 2026-11-17 の一次 HTTP 取得 (`https://search.edion.com/e_store/`) で HTTP/2 200 を確認した
- `iframeResizer.contentWindow.min.js` が組み込まれており、他ページへの埋め込みにも対応した構成になっている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社エディオン管理の店舗情報
- 背景地図・店舗検索基盤: 株式会社ナビタイムジャパン (NAVITIME Location Cloud)
