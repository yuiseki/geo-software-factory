# ビバホーム・ムサシ 店舗検索

- URL: https://store.musashi.vivahome.com/vivamusashi/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ホームセンター、ビバホーム、スーパービバホーム、ムサシ、アークランズ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のビバホーム・スーパービバホーム・ホームセンタームサシの店舗を地域や地図から検索できる公式店舗検索サイト |
| 提供する価値 | アークランズ系列の大型ホームセンターの所在地、営業時間、資材館の営業状況やアクセス情報を横断して確認できる |
| 想定する利用者 | 日用品や建築資材・DIY 用品の購入で最寄りのビバホームまたはムサシへ来店する一般客および業者 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。グループ店舗への来店送客に貢献する集客基盤 |
| 運営 | 企業 (アークランズ株式会社) |
| 推定の運用費 | 推測: 月数十万円。NAVITIME Location Cloud (法人向け店舗検索 SaaS) の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME Location Cloud (HTML 内に `navitime` の参照および `spot/detail?code={{:code}}` の JsRender テンプレート構造を確認) |
| フレームワーク | jQuery 3.7.1 (`jquery-3.7.1.min.js`)、jquery.inview 1.1.2、jquery-cookie 1.4.1、JsRender、iframeResizer |
| 背景の地図とタイル | NAVITIME 地図タイル (NAVITIME Location Cloud の標準地図基盤) |
| 投稿やデータの保存先 | NAVITIME Location Cloud 上で店舗マスタを管理し、`store.musashi.vivahome.com/vivamusashi/` で配信 |
| 配信 | Apache (`server: Apache`) |

メモ:

- 2026-11-17 の一次 HTTP 取得 (`https://store.musashi.vivahome.com/vivamusashi/`) で HTTP/2 200 を確認した
- `https://musashi.vivahome.com/import-parts/script.js` を読み込み、本体サイト側のヘッダ・パーツと連携している

データの出どころ (2026-11-17):

- 店舗データ: アークランズ株式会社管理の店舗情報
- 背景地図・店舗検索基盤: 株式会社ナビタイムジャパン (NAVITIME Location Cloud)
