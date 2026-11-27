---
financial: commercial
organization: corp-ent
first_seen: 2001-02-06
first_seen_by: wayback
---

# ぐるなび

- URL: https://www.gnavi.co.jp/ (店舗検索: https://r.gnavi.co.jp/)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ぐるなび、gnavi、楽天ぐるなび、飲食店検索、グルメ、レストラン予約、店舗マップ、Static Maps

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の飲食店の公式情報・メニュー・予約情報と店舗位置を地図付きで提供する老舗グルメ・飲食店情報サイト |
| 提供する価値 | 飲食店の詳細ページや地図ページでアクセス・周辺地図を素早く確認でき、楽天 ID 連携によるポイント付与付きのネット予約ができる |
| 想定する利用者 | 接待・会食・観光等で飲食店を探す一般消費者、および集客・DX 支援を受ける飲食店事業者 |
| 商用か非商用か | 商用 (利用者は無料。飲食店向けの月額ストック型販促支援サービス、ネット予約手数料、広告収入で運営) |
| 推定の売上 | 約 141 億 3,200 万円 (株式会社ぐるなび 2026 年 3 月期連結売上高。2025 年 3 月期は 134 億 5,800 万円) |
| 運営 | 企業 (株式会社ぐるなび、東証プライム上場) |
| 推定の運用費 | 未確認 (店舗情報・予約管理基盤、Google Maps API / Static Maps API 利用料、サーバー基盤の運用) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API および Google Maps Static API (`https://r.gnavi.co.jp/4ayj9vyu0000/map/` 等の店舗地図ページで `maps.googleapis.com/maps/api/js` と `maps.googleapis.com/maps/api/staticmap` の双方を確認) |
| フレームワーク | Next.js (`https://www.gnavi.co.jp/` および `https://r.gnavi.co.jp/` の店舗ページ HTML 内に `_next` を確認) |
| 背景の地図とタイル | Google Maps (Maps JavaScript API および Static Maps API) |
| 投稿やデータの保存先 | ぐるなび自社基盤 (加盟飲食店の店舗情報、メニュー、空席・予約データ) |
| 配信 | `Server: Apache` (`https://www.gnavi.co.jp/` の応答ヘッダーを確認) |

メモ:

- 店舗地図ページ (`/map/`) では初期表示用の静的地図画像 (`maps.googleapis.com/maps/api/staticmap`) の遅延読み込み記述と、インタラクティブ地図用の `maps.googleapis.com/maps/api/js` の両方が使われている。
- フロントエンドは Next.js (`_next`) ベースへ移行・構築されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 店舗地図 API・フレームワーク | Google Maps JavaScript API、Google Maps Static API、Next.js | `https://r.gnavi.co.jp/` の店舗地図ページ HTML 等 (2026-11-16 観測) |
| 連結売上高 | 株式会社ぐるなび 2026 年 3 月期決算 | ぐるなび IR 資料 |
