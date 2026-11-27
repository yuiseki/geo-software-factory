---
financial: commercial
organization: individual
first_seen: none
first_seen_by: none
---

# 街レンズ

- URL: https://map.machilens.jp/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: 街レンズ、machilens、Atbase、病院検索、歯科検索、避難場所、Leaflet、OpenStreetMap、生活安心マップ、PRピン

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の病院・歯科医院・避難場所などの生活・防災施設を地図上から探せる個人開発ベースの生活安心マップ |
| 提供する価値 | 急病時や災害時に必要な近隣の医療機関や避難所を、軽快な地図 UI とクラスタ表示で素早く見つけられる |
| 想定する利用者 | 引っ越し先や外出先で病院・歯科・避難場所を探したい一般生活者、地域情報を発信したい医療機関・店舗 |
| 商用か非商用か | 商用（一般利用者向けは無料。医療機関や地域店舗向けの有料オプション「PRピン掲載」による広告・掲載料モデル） |
| 推定の売上 | 推測: 立ち上げ・成長段階（PR ピン掲載等のローカル広告モデルを展開しているが、売上規模は非公開） |
| 運営 | 個人法人（合同会社 Atbase。開発者 note にて個人開発で運用している旨を記載） |
| 推定の運用費 | 推測: 月数千円〜数万円程度（Cloudflare + Leaflet + OpenStreetMap の構成により、地図 API 課金を抑えて運用） |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet + Leaflet.markercluster（HTML 内で `leaflet@1.9.4/dist/leaflet.js` および `leaflet.markercluster@1.5.3` の読み込みを確認） |
| フレームワーク | 静的 / サーバーサイド生成 HTML + Leaflet（HTML 内に SPA フレームワークのチャンクは確認されず） |
| 背景の地図とタイル | OpenStreetMap |
| 投稿やデータの保存先 | 自前バックエンド / 静的施設データ（全国の病院・歯科・避難場所データを保持） |
| 配信 | Cloudflare（応答ヘッダーで `server: cloudflare`、`cf-ray` を確認。Google Analytics `G-1JL0PWJQ0C` を掲載） |

メモ:

- 合同会社 Atbase 名義でありながら個人開発で運用されており、OpenStreetMap + Leaflet による低コスト基盤と B2B の PR ピン掲載を組み合わせた日本国内のローカルマップ事例。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| ベースマップ | OpenStreetMap | https://map.machilens.jp/ |
| 病院・歯科・避難場所データ | 公開データ・独自整備データ等 | https://map.machilens.jp/ |
