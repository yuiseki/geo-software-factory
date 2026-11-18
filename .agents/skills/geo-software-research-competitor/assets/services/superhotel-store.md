---
financial: commercial
organization: corp-ent
---

# スーパーホテル 店舗・ホテル検索

- URL: https://www.superhotel.co.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ホテル検索、スーパーホテル、ビジネスホテル、NAVITIME、ゼンリン、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 国内外 180 店舗以上のスーパーホテルをトップページ内のインタラクティブ地図やエリア検索から探し、宿泊予約できる公式サイト |
| 提供する価値 | トップページに埋め込まれた地図から地域ごとのスーパーホテルの位置と詳細を直感的に確認し、そのまま最安値保証の宿泊予約へ進める |
| 想定する利用者 | ビジネス出張や旅行でスーパーホテルの店舗立地を比較して宿泊予約したい一般利用者 |
| 商用か非商用か | 商用 (公式サイト経由の直接予約送客として提供。検索機能の利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。株式会社スーパーホテル (2026年3月期売上高 約621億円、182店舗) の宿泊予約売上に貢献 |
| 運営 | 企業 (株式会社スーパーホテル。地図検索機能は株式会社ナビタイムジャパンの NAVITIME Location Cloud を採用) |
| 推定の運用費 | 推測: 月数十万円。Cloudflare による配信費に加え、NAVITIME Location Cloud (法人向け店舗案内・地図 ASP) およびゼンリン地図データの利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | トップページ内に `<iframe src="https://pkg.navitime.co.jp/superhotel-map/map">` を埋め込み (リサイズ連携に `iframeResizer.min.js`)、iframe 内で NAVITIME 地図スクリプト (`/superhotel-map/api/map/tilemap`) を描画 |
| フレームワーク | jQuery 3.7.1 + Bootstrap 3.2.0 + JsRender (`pkg.navitime.co.jp/superhotel-map/` 側) |
| 背景の地図とタイル | ゼンリン地図データ + NAVITIME 配信 (`tilemap` スクリプト内に `© NAVITIME JAPAN. All Rights Reserved. 地図 ©ゼンリン` の表記を確認) |
| 投稿やデータの保存先 | NAVITIME Location Cloud 基盤 (`pkg.navitime.co.jp/superhotel-map/`) |
| 配信 | Cloudflare (`server: cloudflare`、`cf-ray: ...-NRT`) |

メモ:

- 公式サイトのトップページ (`https://www.superhotel.co.jp/`) 自体に `pkg.navitime.co.jp/superhotel-map/map` の iframe が組み込まれており、外部地図検索ページへ遷移せずともトップ上で日本全国のホテル地図を操作できる

データの出どころ (2026-11-17):

- ホテルデータ: 株式会社スーパーホテル管理のホテル情報
- 店舗検索システム・地図配信: 株式会社ナビタイムジャパン (NAVITIME Location Cloud)
- 背景地図: 株式会社ゼンリン
