---
financial: commercial
organization: individual
first_seen: 2014-08-01
first_seen_by: wayback
---

# Light Pollution Map

- URL: https://www.lightpollutionmap.info/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Light Pollution Map、光害マップ、夜空の明るさ、天体観測、星空スポット、VIIRS、Black Marble、Bortle Scale

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | NASA の夜間光衛星データや夜空の明るさモデルを重ねて、世界中の光害の度合いと星空観測適地を探せるインタラクティブ地図 |
| 提供する価値 | VIIRS 夜間光や World Atlas 2015 の輝度データ、雲量・オーロラ予報、SQM 実測値を切り替えて、光害の少ない天体観測地を簡単に特定できる |
| 想定する利用者 | 天体写真家、アマチュア天文家、星空観光者、光害研究者 |
| 商用か非商用か | 商用・個人運営 (Web 版は広告付きで無料。iOS / Android / Huawei アプリは買い切り約 €5 で広告なし・オフライン対応) |
| 推定の売上 | 推測: 年数百万円規模 (Web 広告収益と約 €5 の有料アプリ販売による個人開発プロジェクトの規模) |
| 運営 | 個人運営 (Jurij Stare 氏による単独開発・運営) |
| 推定の運用費 | 推測: 月数万円〜十数万円規模 (Ubuntu 上の Apache サーバーと NASA 等の公開衛星タイル・SQM データのホスティング) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (2026-11-16 の HTML 観測では `jquery-3.7.1.min.js`、`jquery-ui.min.js`、`assets/index-CrNFzVzd.js` 等を検出) |
| フレームワーク | jQuery / jQuery UI + Vite バンドル風の独自 JS (`./assets/index-*.js` と `assets/lib/jquery-3.7.1.min.js` を確認) |
| 背景の地図とタイル | Microsoft Bing Maps (道路・ハイブリッド) および OpenStreetMap 等をベースとし、NASA VIIRS Black Marble や World Atlas 2015 等のオーバーレイを重ねる構成 |
| 投稿やデータの保存先 | 自前サーバー上のデータベース (ユーザー投稿の SQM / SQC 夜空明るさ測定値や天文台情報を保存) |
| 配信 | Apache/2.4.58 on Ubuntu (`server: Apache/2.4.58 (Ubuntu)` を応答ヘッダーで確認) |

メモ:

- ウェブ版のほか iOS / Android / Huawei AppGallery 向けの有料アプリを提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 夜間光・光害データ | NASA Black Marble (VIIRS)、World Atlas of Artificial Night Sky Brightness (2015) | 公式サイトのレイヤー説明・meta description |
| 実測夜空輝度 (SQM/SQC) | ユーザーからの投稿データ | 公式サイトの説明 |
| 背景地図 | Microsoft Bing Maps、OpenStreetMap | 公式サイトの凡例・利用情報 |
