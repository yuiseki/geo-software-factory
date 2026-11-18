---
financial: commercial
organization: corp-ent
---

# Domino's（Pinpoint Delivery / 店舗検索）

- URL: https://www.dominos.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Domino's、ドミノ・ピザ、Pinpoint Delivery、ピンドロップ配達、Google Maps Platform、店舗検索、配達エリア、出店計画、インドネシア

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 地図上にピンを落とすだけで住所のない公園やビーチ等にもピザを届けられる「Pinpoint Delivery」や、配達状況のリアルタイム追跡を提供する大手ピザチェーンの注文基盤 |
| 提供する価値 | 従来の番地・住所入力に頼らず地図上の任意地点を指定して配達を依頼でき、また各地域の店舗検索・配達可能エリア判定・配達追跡をシームレスに利用できる |
| 想定する利用者 | 自宅だけでなく公園・ビーチ・イベント会場など屋外へピザを注文したい一般消費者、および最寄り店舗から配達・持ち帰りを注文したいユーザー |
| 商用か非商用か | 商用 (Web・アプリからのピザ等のフード注文およびフランチャイズ・直営店舗売上により収益化) |
| 推定の売上 | Domino's Pizza, Inc. 全体の 2024 年通期売上は 47.1 億ドル (全世界システム小売売上は 191 億ドル超) |
| 運営 | 企業 (Domino's Pizza, Inc.、米国上場企業、各国マスターフランチャイジー含む) |
| 推定の運用費 | 推測: 月数千万円〜数億円規模 (グローバルなオンライン注文基盤、店舗検索、Google Maps Platform 等の位置情報・配達追跡 API 運用) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (`https://www.dominos.com/` は `/en/pages/international/` へリダイレクトし HTTP 200 を返却。静的 HTML 上では `has_gmaps: false` で、米国注文画面やアプリ内の Pinpoint Delivery 等の描画手段は直接観測できていない) |
| フレームワーク | Express 等 (`x-powered-by: Express` ヘッダーを確認) |
| 背景の地図とタイル | Google Maps Platform (米国 Pinpoint Delivery や Domino's Indonesia の公開事例にて、Google Maps Platform / Geocoding API / Places API 等の利用が公表されている) |
| 投稿やデータの保存先 | Domino's 自社基盤 (店舗マスタ、配達ゾーン、注文・配達トラッキングデータ) |
| 配信 | `Server: Apache`、`x-powered-by: Express` (`https://www.dominos.com/` の応答ヘッダーを確認) |

メモ:

- 日本等からのアクセスでは `https://www.dominos.com/en/pages/international/` にリダイレクトされる。
- 米国の **Pinpoint Delivery** は Google Maps Platform を活用し、住所のない場所（公園、ビーチ、道路脇など）でも地図上にピンを立てて注文・配達を受け取れる機能として展開されている。
- **Domino's Indonesia** の事例でも、住所表記が曖昧または未整備な新興住宅地が多い環境で「30分配達」を実現するため、Google Maps Platform（Geocoding API、Places API、ピンドロップ位置特定）を導入し、さらに実走行時間や交通パターンに基づく配達ゾーン設計と、人口動態・履歴データを用いた機械学習による新規出店計画（ロケーションインテリジェンス）にも地図データを活用している。
- ウェブ版のほか、iOS / Android 向けの公式モバイルアプリを提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 店舗・メニュー・注文・配達状況 | Domino's 自社および各地域フランチャイズシステム | Domino's 公式サイトおよび IR 資料 |
| 地図・住所変換・ピンドロップ位置情報 | Google Maps Platform | Domino's 発表および Google Maps Platform 公式事例 (Domino's Indonesia 等) |
