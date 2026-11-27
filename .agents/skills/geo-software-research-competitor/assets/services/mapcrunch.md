---
financial: commercial
organization: individual
first_seen: 2010-09-29
first_seen_by: wayback
---

# MapCrunch

- URL: https://www.mapcrunch.com/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: MapCrunch、Nick Nicholaou、ランダムストリートビュー、Google Street View、仮想散歩、海外旅行気分

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ワンクリックで世界中のランダムな Google Street View 地点へジャンプして景色を楽しめる老舗のランダム街歩きサイト |
| 提供する価値 | ゲームの勝敗やスコアを競うのではなく、国や都市部フィルタ・ギャラリー機能を使って偶然の風景との出会い（セレンディピティ）を楽しめる |
| 想定する利用者 | 世界の景色をランダムに眺めたいユーザー、イラスト・小説の資料探し、暇つぶし・仮想旅行者 |
| 商用か非商用か | 商用（基本無料・Google AdSense 等の Web 広告を掲載して運用） |
| 推定の売上 | 推測: 年数十万〜数百万円規模（長年の被リンクと検索流入があるが、広告収入で API 費とサーバー費を賄う個人サイト規模） |
| 運営 | 個人（Nick Nicholaou） |
| 推定の運用費 | 推測: 月数万円〜十数万円程度（Google Maps / Street View API を呼び出すため、アクセス量に応じた API 課金が発生する） |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API v3 / Street View（HTML 内で `maps.google.com/maps/api/js?v=3.exp` の読み込みを確認） |
| フレームワーク | jQuery 1.12.4 + 素の JavaScript（HTML 内で `/js/jquery-1.12.4.min.js`、`/js/main.min.js` を確認） |
| 背景の地図とタイル | Google Maps / Google Street View |
| 投稿やデータの保存先 | サーバー側 DB / 静的座標リスト（お気に入り・ギャラリー投稿地点やランダム抽出ロジックを保持） |
| 配信 | Apache 2.4.67 (Debian)（応答ヘッダーで `server: Apache/2.4.67 (Debian)` を確認。AdSense、Plausible、Google Analytics を確認） |

メモ:

- GeoGuessr（2013 年）以前から存在する「ランダム Street View」系サイトの草分けであり、シンプルな UI と軽量な jQuery 構成のまま長年維持されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| ストリートビュー画像・地図 | Google Maps Platform（Google Street View） | https://www.mapcrunch.com/ |
| ギャラリー地点 | ユーザー投稿および運営キュレーション | サイト内ギャラリー |
