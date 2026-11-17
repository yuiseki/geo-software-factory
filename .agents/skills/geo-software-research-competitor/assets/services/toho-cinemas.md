# TOHOシネマズ 劇場検索・アクセス案内

- URL: https://www.tohotheater.jp/theater/find.html
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: 劇場検索、映画館、TOHOシネマズ、上映スケジュール、アクセス、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の TOHOシネマズ劇場をエリアや条件から検索し、各劇場の上映スケジュールやアクセス地図を確認できる公式劇場案内ページ |
| 提供する価値 | 近隣の TOHOシネマズ劇場の場所、IMAX や MX4D 等の設備対応状況、駐車場情報や最寄駅からの経路をまとめて確認できる |
| 想定する利用者 | 映画鑑賞を予定しており、上映館の場所やアクセス方法、上映時間を調べたい一般の映画ファン・来場者 |
| 商用か非商用か | 商用 (全国の TOHOシネマズ劇場への集客とオンラインチケット販売「vit」への送客のために提供。利用料は無料) |
| 推定の売上 | 推測: 劇場検索単体の売上は 0 円。映画鑑賞チケット販売や館内飲食・グッズ売上への送客に貢献 |
| 運営 | 企業 (TOHOシネマズ株式会社) |
| 推定の運用費 | 推測: 月数万〜数十万円。Web サーバーおよび劇場一覧 JSON 配信の運用費のみ (各劇場の地図は Google マップの無料 iframe 埋め込みを利用) |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps Embed (`iframe` による `https://www.google.com/maps/embed?pb=...` を各劇場のアクセスページ `/theater/<id>/access.html` に埋め込み) |
| フレームワーク | jQuery |
| 背景の地図とタイル | Google マップ (Embed iframe および `https://www.google.com/maps/place/...` リンク) |
| 投稿やデータの保存先 | 自社管理の劇場一覧 JSON (`/responsive/json/theater_list.json`) および各劇場ページ |
| 配信 | 未確認 (`HTTP/2 200` / Shift_JIS ページを確認したが、レスポンスヘッダに Web サーバーや CDN の製品名は出力されない) |

メモ:

- 劇場一覧 (`/theater/find.html`) では `/responsive/js/toHtml/theaterList.js` が `/responsive/json/theater_list.json` を読み込んで劇場リストを表示している
- 個別のアクセスページ (例: `/theater/076/access.html` TOHOシネマズ 新宿) では Google マップの埋め込み `iframe` と Google マップへの外部リンクを表示している

データの出どころ (2026-11-17):

- 劇場データ: TOHOシネマズ株式会社自社管理の劇場情報
- 背景地図: Google マップ (iframe 埋め込み)
