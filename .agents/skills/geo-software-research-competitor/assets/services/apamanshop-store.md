---
financial: commercial
organization: corp-ent
---

# アパマンショップ 店舗検索

- URL: https://www.apamanshop.com/shop/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、不動産仲介、賃貸、アパマンショップ、APAMAN、フランチャイズ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のアパマンショップ直営・加盟店舗を都道府県やエリア・キーワードから検索し、アクセスや取扱物件を確認できる公式店舗検索ページ |
| 提供する価値 | 最寄りのアパマンショップ店舗の所在地・営業時間・定休日・Google Maps 上の位置を確認でき、来店予約やオンライン接客・物件相談への導線になる |
| 想定する利用者 | 賃貸マンション・アパート等の部屋探しで実店舗への来店相談や内見予約を希望する一般顧客 |
| 商用か非商用か | 商用 (直営店およびフランチャイズ加盟店への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。親会社 APAMAN 株式会社の連結売上高は約 457 億円〜458 億円前後 (賃貸管理・FC・テクノロジー事業を含む) |
| 運営 | 企業 (APAMAN 株式会社 / アパマンショップネットワーク) |
| 推定の運用費 | 推測: 月数万〜数十万円。Web サーバー (Apache) 運用費に加え、店舗詳細ページ等で利用する Google Maps JavaScript API の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`maps.googleapis.com/maps/api/js` を店舗詳細ページ `/shop/33017002/` で確認。店舗検索トップ `/shop/` には地図埋め込みなし) |
| フレームワーク | jQuery 1.11.1 + jQuery UI (`shop_top.js` 等、HTML5 サーバー描画) |
| 背景の地図とタイル | Google Maps (店舗詳細ページで Google Maps JavaScript API 経由で読み込み) |
| 投稿やデータの保存先 | アパマンショップ自社店舗基盤 (店舗検索トップ・店舗詳細ともにサーバー側で HTML 生成) |
| 配信 | Apache (`server: Apache`) |

メモ:

- 店舗検索トップ (`https://www.apamanshop.com/shop/`) には地図は埋め込まれておらず、地域・店舗を選んで遷移する個別店舗ページ (例: `/shop/33017002/`) に Google Maps JavaScript API が埋め込まれている。

データの出どころ (2026-11-17):

- 店舗検索・技術構成: `https://www.apamanshop.com/shop/` および `https://www.apamanshop.com/shop/33017002/` の HTTP 応答ヘッダ・HTML/JS (2026-11-17 観測)
- 店舗データ: APAMAN 株式会社自社管理の店舗情報
- 背景地図: Google (Google Maps Platform)
- 運営・業績情報: APAMAN 株式会社 公開決算・会社情報
