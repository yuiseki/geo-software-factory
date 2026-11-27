---
financial: commercial
organization: corp-ent
first_seen: 2025-04-26
first_seen_by: wayback
---

# コスモ石油 サービスステーション検索

- URL: https://map.cosmo-energy.co.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ガソリンスタンド、SS検索、コスモ石油、コスモエネルギー、給油、洗車、カーリース、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のコスモ石油サービスステーション (SS) を現在地・エリア・サービス条件から検索して地図上に表示する公式店舗検索サイト |
| 提供する価値 | 近くのコスモ石油 SS の位置や営業時間、セルフ給油・洗車・車検・カーリース取扱などの条件を一覧と地図で素早く確認できる |
| 想定する利用者 | コスモ石油での給油や洗車・メンテナンスを希望するドライバー、コスモ・ザ・カードや法人カード利用者 |
| 商用か非商用か | 商用 (全国のコスモ石油 SS への送客基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 検索サイト単体の売上は 0 円。全国約 2,500 ヵ所の SS における燃料販売やカーケア・カーリース事業の売上に貢献 |
| 運営 | 企業 (コスモ石油マーケティング株式会社 / コスモエネルギーグループ) |
| 推定の運用費 | 推測: 月数十万円。GOGA Store Locator の SaaS 利用料および Google Maps Platform の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps + GOGA Store Locator (`/assets/main-BdyNgr0c.js` 内に `google.maps` および `Powered by GOGA` リンクを確認) |
| フレームワーク | Vue.js (Vite ビルドバンドル `/assets/main-BdyNgr0c.js` 内に Vue ランタイムを確認) |
| 背景の地図とタイル | Google マップ (Google Maps Platform) |
| 投稿やデータの保存先 | GOGA Store Locator 基盤 (株式会社ゴーガ提供のクラウド店舗検索システム) |
| 配信 | Google Frontend (`server: Google Frontend`、`via: 1.1 google`、`x-frame-options: DENY`) |

メモ:

- JS バンドル内に `https://www.goga.co.jp/services/storelocator/` への「Powered by GOGA」表記が含まれており、株式会社ゴーガの Store Locator 製品を採用していることが確認できる

データの出どころ (2026-11-17):

- SS データ: コスモ石油マーケティング株式会社管理の SS 情報
- 背景地図: Google (Google Maps Platform)
- 検索システム: 株式会社ゴーガ (GOGA Store Locator)
