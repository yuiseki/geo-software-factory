---
financial: commercial
organization: corp-smb
---

# Park4Night

- URL: https://park4night.com
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Park4Night、AppMobilEdition、車中泊、キャンピングカー、バンライフ、RVパーク、欧州、Leaflet、MapLibre、MapTiler

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 欧州を中心に世界中のキャンピングカー・バンライフ向けの車中泊スポット、駐車場、キャンプ場、給排水設備を共有し地図上で探せるコミュニティアプリ |
| 提供する価値 | 数十万件規模の車中泊・休憩適地を、設備アイコン・利用者の最新コメント・衛星写真と合わせて地図上で素早く見つけられ、オフライン地図やルート沿い検索も行える |
| 想定する利用者 | キャンピングカー・バンコン・車中泊で旅をする個人・家族、および受け入れ施設を PR したいキャンプ場・農家・自治体 |
| 商用か非商用か | 商用 (フリーミアム。基本利用は無料で広告あり。個人向け park4night+ は年額約 €9.99、施設・事業者向け掲載プランは Bronze 年額 €100〜Platinum 年額 €3,000 で収益化) |
| 推定の売上 | 推測: 年商200万ユーロ以上 (フランスの登記・財務情報データベース等で純利益200万ユーロ超と報じられる高収益事業) |
| 運営 | 企業 (AppMobilEdition SAS、フランス・サン＝ペレ) |
| 推定の運用費 | 推測: 月数十万〜数百万円規模。MapTiler タイル API、数十万スポットと写真の配信、6〜9名規模の少人数チームでの運用 |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet + MapLibre (`https://cdn6.park4night.com/js/app.min.js` 内に `L.map`, `L.tileLayer` および `maplibre` の記述を確認) |
| フレームワーク | jQuery (`app.min.js` 内に `jquery` を確認) |
| 背景の地図とタイル | MapTiler (`https://api.maptiler.com/maps/streets-v2/style.json` を JS 内で確認。OpenStreetMap ベース) および Nominatim ジオコーディング (`https://nominatim.openstreetmap.org/search`) |
| 投稿やデータの保存先 | AppMobilEdition 自社基盤 (ユーザー投稿スポット・レビュー・写真、および提携施設データ) |
| 配信 | 独自 CDN (`cdn6.park4night.com`) 経由でアセット配信 |

メモ:

- `https://park4night.com/en` から読み込まれる `app.min.js` を直接解析し、Leaflet・MapLibre・MapTiler (`streets-v2`)・OpenStreetMap Nominatim の利用を確認した。
- ウェブ版のほか iOS / Android アプリも提供されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 車中泊スポット・駐車場・レビュー | コミュニティユーザーの投稿、提携施設 (geoSPOT 等) | Park4Night 公式サイト・アプリ |
| 背景地図・ジオコーディング | OpenStreetMap、MapTiler、Nominatim | `app.min.js` 内の URL |
