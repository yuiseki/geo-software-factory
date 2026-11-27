---
financial: commercial
organization: corp-ent
first_seen: 2001-04-04
first_seen_by: wayback
---

# 楽天トラベル

- URL: https://travel.rakuten.co.jp/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: 楽天トラベル、Rakuten Travel、宿予約、ホテル予約、エリアマップ、周辺地図、Google Maps、OTA、楽天グループ

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 国内外の宿泊予約、航空券や新幹線とのパッケージ、レンタカー、観光情報などを提供する国内大手オンライン旅行予約サイト |
| 提供する価値 | 宿泊施設や交通手段を楽天ポイント連携のもとで比較・予約でき、周辺地図や観光情報 (たびノート等) から立地を確認できる |
| 想定する利用者 | 国内旅行、海外旅行、出張で宿泊先や移動手段をまとめて手配したい楽天会員および一般旅行者 |
| 商用か非商用か | 商用 (宿泊・交通予約の送客手数料、広告掲載、各種パートナー連携による収益) |
| 推定の売上 | 未確認 (楽天トラベル単体の売上高・流通総額は非公開。楽天グループ全体の国内 EC 流通総額の一部として開示) |
| 運営 | 企業 (楽天グループ株式会社) |
| 推定の運用費 | 未確認 (大規模予約処理基盤、Google Maps Platform 等の地図 API 利用料、施設・口コミデータの維持管理費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | ウェブ、iOS と Android のアプリ |
| 描画 | Google Maps JavaScript API (`https://travel.rakuten.co.jp/HOTEL/14450/rtmap.html` の HTML 内に `<div id="mapBox">` および `https://maps.googleapis.com/maps/api/js` の読み込みを観測) |
| フレームワーク | 一部画面で Next.js 等を使用 (トップページ HTML 内に `Next` 関連記述を観測。宿泊施設個別地図ページ `rtmap.html` はサーバー生成 HTML 構成) |
| 背景の地図とタイル | Google Maps (Maps JavaScript API 経由で取得) |
| 投稿やデータの保存先 | 未確認 (楽天グループ自社インフラ・クラウド基盤上と推測されるが公開情報からは特定できず) |
| 配信 | Apache (`server: Apache` ヘッダーを観測) |

メモ:

- 宿泊施設ごとの地図ページ (`rtmap.html`) において、`maps.googleapis.com/maps/api/js` を直接読み込んで地図を描画していることを確認した。
- 観光情報メディア「たびノート」などでも Google Maps API が活用されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 地図ライブラリ・背景地図 | Google Maps JavaScript API | `https://travel.rakuten.co.jp/HOTEL/14450/rtmap.html` の HTML (2026-11-16 観測) |
| 宿泊施設・料金・口コミ情報 | 宿泊施設からの提供およびユーザー投稿 | 楽天トラベル公式サイト |
| 応答ヘッダー | `https://travel.rakuten.co.jp/` 等の HTTP 応答ヘッダー | 2026-11-16 観測 |
