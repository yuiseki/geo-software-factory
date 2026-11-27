---
financial: commercial
organization: corp-ent
first_seen: 2007-10-25
first_seen_by: wayback
---

# 公文式 教室検索

- URL: https://www.kumon.ne.jp/enter/search/search.php
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、教室検索、学習塾、公文式、KUMON、くもん、幼児、小中高、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の公文式教室を地域・駅・現在地から検索し、対象教科や開室曜日を確認して見学・入会申込できる公式教室検索サイト |
| 提供する価値 | 子どもの通学圏内にある公文式教室を見つけ、対象教科・対象年齢・開室日時を比較して無料体験や資料請求へ進める |
| 想定する利用者 | 子どもや自身の学習のために通いやすい公文式教室を探している保護者および学習者 |
| 商用か非商用か | 商用 (教室見学・無料体験学習・入会申込の獲得のために提供。利用料は無料) |
| 推定の売上 | 推測: 教室検索単体の売上は 0 円。新規入会者の獲得と全国の教室運営を支える中核の集客基盤 |
| 運営 | 企業 (株式会社公文教育研究会) |
| 推定の運用費 | 推測: 月数十万円規模。Apache + CloudFront による配信費および MapFan / GeoTechnologies (©MAPPLE) 等の地図 API 利用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapFan / GeoTechnologies (©MAPPLE) (参考の事前調査による。一次 HTTP 取得の `search.php` および `classroom_map.php` では描画スクリプトを直接確認できず) |
| フレームワーク | PHP (`search.php`)、独自 JS (`/common_2019/js/lib/bundle.js`、`get_classroom_by_gps.js`、`search.js`) |
| 背景の地図とタイル | MapFan / GeoTechnologies (©MAPPLE) (参考の事前調査による。一次 HTTP 取得では詳細未確認) |
| 投稿やデータの保存先 | 自社教室検索基盤 (`www.kumon.ne.jp/enter/search/`) |
| 配信 | Apache + Amazon CloudFront (`server: Apache`、`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 観測では `search.php`、`map.php`、`classroom_map.php` を確認し、現在地検索用 JS (`get_classroom_by_gps.js`) 内で `/enter/search/classroom_map.php` への遷移を確認した
- 地図描画の具体的なタイル URL や API 呼び出しは動的遷移先のブラウザ実行で読み込まれるため、一次 HTTP 取得では未確認

データの出どころ (2026-11-17):

- 店舗データ: 株式会社公文教育研究会自社管理の教室情報
- 背景地図: MapFan / GeoTechnologies (©MAPPLE) (参考の事前調査による)
