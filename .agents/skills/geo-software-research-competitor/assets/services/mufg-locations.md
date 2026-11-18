---
financial: commercial
organization: corp-ent
---

# 三菱UFJ銀行 ATM・店舗のご案内

- URL: https://map.bk.mufg.jp/b/bk_mufg/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ATM検索、銀行、三菱UFJ銀行、MUFG、外貨両替、窓口、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の三菱UFJ銀行の店舗・ATM・相談窓口を現在地・駅・住所・利用条件から検索し、地図上に表示する公式店舗・ATM検索サイト |
| 提供する価値 | 近くの店舗や ATM の設置場所だけでなく、稼働時間・通帳記帳や硬貨取扱・テレビ窓口・外貨両替・バリアフリー対応などの条件を絞り込んで確認できる |
| 想定する利用者 | 三菱UFJ銀行の口座保有者、振込・両替・各種手続きのため窓口や ATM を探している一般利用者・法人担当者 |
| 商用か非商用か | 商用 (銀行利用者の利便性向上および店舗・ATM への案内基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 検索サイト単体の売上は 0 円。リテール・法人銀行業務の顧客接点維持および窓口相談への誘導に貢献 |
| 運営 | 企業 (株式会社三菱UFJ銀行) |
| 推定の運用費 | 推測: 月数十万〜百万円規模。ONE COMPATH (旧 Mapion) の法人向け店舗検索 ASP (`SpotSearch`) 利用料と配信費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet + ONE COMPATH (旧 Mapion) 店舗検索基盤 (`/f/bk_mufg/dist/js/base.js` 内に Leaflet、`lbs.mapion.co.jp/jslibs/JSPack.2.1.0.js` を確認) |
| フレームワーク | jQuery 3.6.0 (`jquery-3.6.0.min.js`)、ONE COMPATH `SpotSearch.js` (`common-ss2.0` / `ss5_5`) |
| 背景の地図とタイル | ONE COMPATH (Mapion) 地図タイル (`lbs.mapion.co.jp`) |
| 投稿やデータの保存先 | ONE COMPATH (旧 Mapion) のクラウド店舗検索基盤 (`SpotSearch.js` 経由の API) |
| 配信 | nginx (`server: nginx`) |

メモ:

- `/b/bk_mufg/` のパス構成や `/f/common-ss/common-ss2.0/js/client_js/SpotSearch.js`、`/f/js_libs/ss5_5/` は ONE COMPATH (旧 Mapion) の店舗検索 ASP の標準構成である

データの出どころ (2026-11-17):

- 店舗・ATM データ: 株式会社三菱UFJ銀行管理の拠点情報
- 背景地図・店舗検索基盤: 株式会社 ONE COMPATH (Mapion 地図)
