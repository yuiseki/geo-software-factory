# OpenGuessr

- URL: https://openguessr.com/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: OpenGuessr、PaulPlay、Paul Rhomberg、GeoGuessr代替、Google Street View、Leaflet、Svelte、Publift

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 登録不要・完全無料で無制限に遊べる、Google Street View ベースの GeoGuessr 代替ブラウザゲーム |
| 提供する価値 | GeoGuessr の有料化以降に「無料で制限なく遊びたい」ユーザーの受け皿となり、シングルプレイ・マルチプレイ・カスタムマップをブラウザですぐ遊べる |
| 想定する利用者 | 無料でストリートビュー地理ゲームを遊びたいプレイヤー、学校や職場の休憩時間に遊ぶユーザー、配信者 |
| 商用か非商用か | 商用（基本無料・Publift 経由の Web 広告と、任意の「Supporter」サブスクリプションで運営） |
| 推定の売上 | 推測: 年数千万円規模（数百万ユーザー規模のトラフィックと Publift 広告最適化による高 RPM 収益、サポーター課金を持つが具体額は非公開） |
| 運営 | 個人（PaulPlay Studio / Paul Rhomberg） |
| 推定の運用費 | 推測: 月数十万〜数百万円規模（Google Street View / Maps API 費とマルチプレイサーバー費がかかるが、広告最適化で回収） |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Street View（パノラマ表示）および Leaflet（推測用ミニマップ） |
| フレームワーク | Svelte（応答 HTML 内に `svelte` 関連記述を確認） |
| 背景の地図とタイル | Google Street View / Google Maps、OpenStreetMap・Carto 系タイル（ミニマップ用） |
| 投稿やデータの保存先 | 自前バックエンド（ユーザープロフィール、サポーター管理、マルチプレイ・カスタムマップ） |
| 配信 | Cloudflare（応答ヘッダーで `server: cloudflare`、`cf-ray` を確認。Turnstile、Publift 広告スクリプトを確認） |

メモ:

- 2023 年にプロトタイプから始まり、Svelte ベースの軽量 SPA と Publift による広告収益最適化によって、個人開発ながら Google Street View 系ゲームの API 負荷を商業的に持続させている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| ストリートビュー画像 | Google Maps Platform（Google Street View） | https://openguessr.com/ |
| 推測用地図タイル | OpenStreetMap / Carto 等 | サイト内ミニマップ表示 |
