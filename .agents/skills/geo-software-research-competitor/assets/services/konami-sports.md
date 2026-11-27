---
financial: commercial
organization: corp-ent
first_seen: 2016-10-23
first_seen_by: wayback
---

# コナミスポーツクラブ 施設検索

- URL: https://www.konami.com/sportsclub/shisetsu/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、施設検索、コナミスポーツ、コナミスポーツクラブ、フィットネス、スポーツジム、スイミング、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | コナミスポーツクラブの直営・受託施設をエリアや提供プログラム・設備条件から検索できる公式施設検索ページ |
| 提供する価値 | 都道府県や子ども向けスクール・成人向けプログラムなどの条件で施設を絞り込み、検索結果の地図や各施設のアクセスページで場所を確認できる |
| 想定する利用者 | スポーツジムや子ども向けスイミング・体操・ダンススクールの入会を検討している利用者、および都度利用・他店舗利用する会員 |
| 商用か非商用か | 商用 (総合型スポーツクラブおよび受託施設の集客・体験予約・入会導線として提供。利用料は無料) |
| 推定の売上 | 推測: 施設検索単体の売上は 0 円。コナミスポーツ株式会社 (2026年3月期売上高 約495億円、約370〜380施設) の会員・スクール集客に貢献 |
| 運営 | 企業 (コナミスポーツ株式会社 / コナミグループ) |
| 推定の運用費 | 推測: 月数万〜数十万円。Apache による Web サーバー運用費に加え、検索結果ページでの Google Maps JavaScript API 利用料がかかる (個別施設のアクセスページは iframe 埋め込み) |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 検索結果ページ (`/sportsclub/shisetsu/result.html`) で Google Maps JavaScript API (`maps.googleapis.com/maps/api/js`) を読み込み、個別施設のアクセスページ (`/ksc/<code>/access.html`) では Google マップの iframe 埋め込み (`google.com/maps/embed?pb=...`) を使用 |
| フレームワーク | jQuery (`jquery.js`、検索 UI は `search_ui.js` と `search_run.js`) |
| 背景の地図とタイル | Google マップ (検索結果では Maps JavaScript API、個別施設アクセスでは Maps Embed iframe) |
| 投稿やデータの保存先 | 施設データ JSON API (`/sportsclub/api/facilities.php` から全施設データを取得) |
| 配信 | Apache (`server: Apache`) |

メモ:

- トップの `/sportsclub/shisetsu/` 自体には地図がなく、`/sportsclub/api/facilities.php` で施設マスタ JSON を取得して条件選択を行い、`/sportsclub/shisetsu/result.html` で Google Maps JavaScript API による地図表示、個別施設サイト (`information.konamisportsclub.jp/ksc/<code>/access.html`) で `google.com/maps/embed` を用いる構成になっている

データの出どころ (2026-11-17):

- 施設データ: コナミスポーツ株式会社自社管理の施設情報 (`/sportsclub/api/facilities.php`)
- 背景地図: Google (Google Maps Platform / Google マップ埋め込み)
