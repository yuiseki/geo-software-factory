---
financial: commercial
organization: corp-ent
---

# Naver Map (ネイバー地図)

- URL: https://map.naver.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Naver Map、네이버 지도、ネイバー地図、韓国地図、ベクタータイル、WebGL、Naver Labs、店舗予約

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | NAVER が韓国国内向けに提供する、高精度ベクター地図、ナビゲーション、ストリートビュー、店舗検索・予約が一体化した総合地図サービス |
| 提供する価値 | 韓国の建物・店舗情報、Naver 口コミ、予約・決済連携、3D デジタルツイン街並み、リアルタイム公共交通案内を 60fps の滑らかな操作感で利用できる |
| 想定する利用者 | 韓国国内の住民や旅行者、韓国の店舗や交通を調べたい訪韓外国人、Naver Cloud Platform 経由で地図 API を使う開発者 |
| 商用か非商用か | 商用 (一般利用は無料。ローカル店舗広告、Naver 予約・決済エコシステムへの送客、Naver Cloud Platform での法人向け Maps API 課金で収益化) |
| 推定の売上 | 未公表 (NAVER Corporation の決算では Search Platform や Commerce 等のセグメントに含まれ、Naver Map 単体の売上は公表されていない) |
| 運営 | 企業 (NAVER Corporation) |
| 推定の運用費 | 未確認 (Naver Labs による精密測量車両・航空撮影・デジタルツイン構築、膨大な POI と予約データの運用、自社配信基盤の維持費がかかる) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | WebGL ベースのベクタータイル描画 (法人・開発者向けの NAVER Map API v3 でも `gl` サブモジュールによる WebGL 描画を提供) |
| フレームワーク | モダン ES Modules 構成 (`https://map.naver.com/p/` の HTML で `type="module"` の `index-02a84c4.js` を確認。具体的なフレームワーク名は未確認) |
| 背景の地図とタイル | NAVER 自社地図データ、Naver Labs (P1 測量システム・ALIKE 技術) による航空写真・3D ポイントクラウド、韓国国内の地域 POI・公共交通データ |
| 投稿やデータの保存先 | NAVER アカウント (お気に入り場所、レビュー、予約履歴等の保存) |
| 配信 | NAVER 自社インフラ (`server: nfront`、`x-proxy-by: nautilus`、`maps-service.pstatic.net` からの静的配信を確認) |

メモ:

- 2026-11-16 に `https://map.naver.com/` を確認したところ、`https://map.naver.com/p/` へ `301` リダイレクトされ、`server: nfront`、`x-proxy-by: nautilus` を返していた。
- 韓国では地図データの国外持ち出し規制があるため、Google Maps よりも Naver Map や KakaoMap などの国内勢が標準的に使われている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 地図・ストリートビュー・3D 空間データ | NAVER Corporation および研究開発子会社 Naver Labs (P1・ALIKE) | Naver Labs・NAVER 公式技術発表 |
| 施設情報・口コミ・予約データ | NAVER ローカル検索データベース・ユーザー投稿・Naver Booking | NAVER 公式サービス案内 |
