---
financial: commercial
organization: corp-ent
first_seen: 2013-04-03
first_seen_by: wayback
---

# ダイワロイネットホテルズ ホテル一覧

- URL: https://www.daiwaroynet.jp/hotelist/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ホテル検索、ダイワロイネットホテル、Daiwa Roynet、大和ハウス、ビジネスホテル、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 国内外約 80 施設のダイワロイネットホテルズをエリアや条件から一覧検索し、各ホテルの詳細・アクセス地図を確認できる公式ホテル一覧ページ |
| 提供する価値 | 駅近の都市型ホテルを中心に各地域の施設を比較し、予約導線や Google マップでの周辺位置・道案内を確認できる |
| 想定する利用者 | 出張や観光で主要駅近くのビジネス・都市型ホテルを探している宿泊客 |
| 商用か非商用か | 商用 (公式予約システムへの宿泊予約送客として提供。検索・閲覧は無料) |
| 推定の売上 | 推測: ホテル一覧単体の売上は 0 円。ダイワロイネットホテルズ (ホテル事業売上高目安 約842億円、約78〜81施設) の宿泊予約売上に貢献 |
| 運営 | 企業 (ダイワロイネットホテルズ株式会社 / 大和ハウスリアルティマネジメント株式会社 / 大和ハウスグループ) |
| 推定の運用費 | 推測: 月数万〜数十万円。Apache による Web サーバー運用費と予約連携 SDK (tripla) の費用が中心で、地図は Google マップへの外部リンクおよび iframe 埋め込みのため地図 API の従量課金は発生しない |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 一覧ページ (`/hotelist/`) では Google マイマップ (`google.com/maps/d/viewer?mid=...`) や Google マップ地点 (`google.com/maps/place/...`) への外部リンクを掲載し、個別ホテルページ (例: `/ginza/`) では Google マップの iframe 埋め込み (`https://www.google.com/maps/embed?pb=...`) を使用 |
| フレームワーク | jQuery 3.4.1 (`jquery-3.4.1.min.js`、`hotelist.min.js`、`flatpickr.min.js`、予約導線に `tripla.min.js`) |
| 背景の地図とタイル | Google マップ (Maps Embed iframe および Google マップ / マイマップへの外部リンク) |
| 投稿やデータの保存先 | サーバー側で生成された HTML (`/hotelist/`、`/<hotel>/` 等)、予約は `reserve.daiwaroynet.jp` へ連携 |
| 配信 | Apache (`Server: Apache`) |

メモ:

- `/hotelist/` ページ自体には動的地図ウィジェットはなく、エリアごとの施設一覧と予約ボタン・Google マップリンクを提供し、各ホテルページ内で `google.com/maps/embed` を表示する構成になっている

データの出どころ (2026-11-17):

- ホテルデータ: ダイワロイネットホテルズ株式会社管理のホテル情報
- 背景地図: Google (Google マップ埋め込み / Google マップリンク)
