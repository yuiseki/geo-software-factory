---
financial: commercial
organization: corp-ent
first_seen: 2010-08-29
first_seen_by: wayback
---

# ホンダ 四輪販売店検索

- URL: https://shopsearch.honda.co.jp/auto/search/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、ディーラー検索、販売店検索、ホンダ、Honda Cars、試乗、新車、中古車、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の Honda 四輪販売店 (Honda Cars 等) を地域・条件から検索し、位置や取扱サービスを地図上に表示する公式販売店検索サイト |
| 提供する価値 | 最寄りの Honda 販売店の位置、営業時間、試乗車・展示車や福祉車両取扱、車検・点検対応の有無を確認し、来店や問い合わせにつなげられる |
| 想定する利用者 | Honda 車の購入・試乗を検討している顧客、点検・車検などの整備を希望する Honda 車オーナー |
| 商用か非商用か | 商用 (全国の Honda 販売店への来店・試乗・整備予約への送客基盤として提供。利用料は無料) |
| 推定の売上 | 推測: 検索サイト単体の売上は 0 円。全国の四輪販売店における車両販売・メンテナンス事業の送客に貢献 |
| 運営 | 企業 (本田技研工業株式会社) |
| 推定の運用費 | 推測: 月数十万円。ゼンリンデータコム (いつもNAVI API) の法人利用料および Amazon CloudFront 配信費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | ゼンリンデータコム いつもNAVI API (`https://api.its-mo.com/v3/loader?api=zdcmap.js,usercontrol.js,userwidget.js`) |
| フレームワーク | jQuery 1.4.2 / jQuery UI (`jquery-1.4.2.js`、`ui.core.js`、`ui.dialog.js`)、独自スクリプト (`/js/map.js`、`/js/common/dealer_info.js`) |
| 背景の地図とタイル | ゼンリン地図 (株式会社ゼンリンデータコム `api.its-mo.com`) |
| 投稿やデータの保存先 | 本田技研工業の販売店データベース (サーバー側描画および `/js/common/dealer_info.js` 経由) |
| 配信 | Amazon CloudFront (`via: 1.1 ...cloudfront.net (CloudFront)`、`x-amz-cf-pop: NRT20-P9`) |

メモ:

- 自動車メーカーの店舗検索の中で、Google Maps ではなく国内のゼンリンデータコム (`api.its-mo.com/v3/loader`) を採用している事例である

データの出どころ (2026-11-17):

- 販売店データ: 本田技研工業株式会社管理の販売店情報
- 背景地図: 株式会社ゼンリンデータコム (いつもNAVI API / ゼンリン地図)
