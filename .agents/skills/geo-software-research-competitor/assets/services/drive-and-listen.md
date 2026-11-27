---
financial: commercial
organization: individual
first_seen: 2022-02-27
first_seen_by: wayback
---

# Drive & Listen

- URL: https://driveandlisten.app/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: Drive & Listen、Erkam Şeker、ドライブ動画、現地ラジオ、仮想ドライブ、バーチャル旅行、作業用BGM

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中の都市のドライブ車載映像と現地のリアルタイムラジオ放送・環境音を組み合わせて聴きながら仮想ドライブできる Web アプリ |
| 提供する価値 | 地図の操作ではなく「都市を選んで車窓映像と現地ラジオを同時に流す」ことで、コロナ禍以降の仮想旅行や作業用環境としての没入感を提供する |
| 想定する利用者 | 作業用 BGM や環境映像を求める人、海外の街並みや現地のラジオを楽しみたい旅行好き |
| 商用か非商用か | 商用・個人運営（基本無料・Google AdSense 等の Web 広告と寄付リンクで運営） |
| 推定の売上 | 推測: 年数十万〜数百万円規模（SNS で世界的にバイラルした個人サイトで、AdSense 等による運営維持） |
| 運営 | 個人（Erkam Şeker。2020 年にミュンヘン在住の大学院生・エンジニアとして個人制作） |
| 推定の運用費 | 推測: 月数千円〜数万円程度（映像は YouTube 埋め込み、音声は各ラジオ局のストリームを参照し、地図タイル配信を持たないため低コスト） |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 地図描画なし（都市選択 UI + YouTube 映像プレイヤー + 音声ストリーミングプレイヤー） |
| フレームワーク | React（Create React App 系の `/static/js/16.aa6f7117.chunk.js` と `/static/js/main.d06efca6.chunk.js` を確認） |
| 背景の地図とタイル | なし（都市名・緯度経度ではなく都市リストからドライブ映像とラジオ局を紐づける設計） |
| 投稿やデータの保存先 | 静的リスト / キュレーションデータ（都市ごとの YouTube 動画 ID とラジオストリーム URL） |
| 配信 | Cloudflare（応答ヘッダーで `server: cloudflare`、`x-cache: HIT`、`cf-ray` を確認。AdSense と Google Analytics を掲載） |

メモ:

- 以前は `driveandlisten.herokuapp.com` で公開されていたが、現在は独自ドメイン `https://driveandlisten.app/` で稼働している。
- 地図タイルを使わずに「場所の体験（映像＋音）」だけを届ける、地図サービスの境界例。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| ドライブ映像 | YouTube 上の各都市ドライブ動画 | https://driveandlisten.app/ |
| 現地ラジオ音声 | 世界各地のインターネットラジオ局ストリーム | https://driveandlisten.app/ |
