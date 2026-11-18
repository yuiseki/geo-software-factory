---
financial: commercial
organization: corp-ent
---

# コジマ 店舗一覧

- URL: https://www.kojima.net/shop/shoplist/index.html
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、家電量販店、コジマ、コジマ×ビックカメラ、KOJIMA、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のコジマおよびコジマ×ビックカメラ店舗を地方別ページから探し、住所や営業時間、Google マップへのリンクを確認できる公式店舗一覧 |
| 提供する価値 | 地方・都道府県ごとの一覧ページで最寄り店舗の基本情報と Google マップへの外部リンクを軽量なページ構成で確認できる |
| 想定する利用者 | 家電や日用品の購入でコジマ×ビックカメラ店舗へ来店する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客および公式通販サイト「コジマネット」との連携として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗一覧単体の売上は 0 円。実店舗売上および EC 送客に貢献する集客基盤 |
| 運営 | 企業 (株式会社コジマ / ビックカメラグループ) |
| 推定の運用費 | 推測: 月数万円。埋め込み地図 API を使わず静的 HTML と CloudFront で配信しているため運用費は低い |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 埋め込み地図なし (地方別ページ `kitakanto.html` 等で `https://www.google.co.jp/maps/place/...` への外部リンクを掲載) |
| フレームワーク | jQuery 2.2.4 (`ajax.googleapis.com`)、Shift_JIS エンコーディングの静的・サーバー生成 HTML |
| 背景の地図とタイル | なし (自社ページ内への地図埋め込みは確認できず、Google マップの外部リンクへ遷移する形式) |
| 投稿やデータの保存先 | 自社管理の地方別 HTML (`www.kojima.net/shop/shoplist/<地方>.html`) |
| 配信 | Apache + Amazon CloudFront (`server: Apache`、`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 取得 (`https://www.kojima.net/shop/shoplist/index.html` および `kitakanto.html`) で HTTP/2 200 を確認した
- グループ親会社のビックカメラ店舗一覧 (`biccamera.com/bc/i/shop/shoplist/index.jsp`) への導線も併設されている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社コジマ自社管理の店舗情報
- 背景地図: なし (Google マップへの外部リンクのみ)
