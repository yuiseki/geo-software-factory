---
financial: public-service
organization: gov-central
---

# PLATEAU VIEW

- URL: https://plateauview.mlit.go.jp/ (ポータル: https://www.mlit.go.jp/plateau/)
- ソース: https://github.com/Project-PLATEAU/PLATEAU-VIEW-4.0 (ライセンス: 未確認、Re:Earth ベース)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: PLATEAU VIEW、PLATEAU、プラトー、国土交通省、3D都市モデル、CityGML、3D Tiles、CesiumJS、Re:Earth、オープンデータ

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 国土交通省が整備・オープンデータ化する日本全国の 3D 都市モデル (建物・道路・災害リスク等) をブラウザ上で 3D 表示・解析できる WebGIS |
| 提供する価値 | 専門の GIS や CAD ソフトがなくても、都市計画・防災・日照・景観シミュレーションなどに使える高精度な 3D 都市モデルをブラウザから即座に閲覧・検証できる |
| 想定する利用者 | 自治体・都市計画担当者、建築・不動産・防災関係者、ゲーム・VR・映像クリエイター、研究者、一般市民 |
| 商用か非商用か | 非商用 (国土交通省が主導する公共プロジェクトとして無料で提供。整備された 3D 都市モデルデータもオープンデータとして商用利用可能) |
| 推定の売上 | なし (国のプロジェクトによる無償提供。なお開発・構築は Eukarya 等への委託事業として実施) |
| 運営 | 公的機関 (国土交通省、開発: 株式会社 Eukarya 等) |
| 推定の運用費 | 推測: 年間数千万円〜数億円規模 (日本全国の巨大な 3D Tiles・地形・点群データの配信と Google Cloud 基盤の維持費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | CesiumJS 1.118.0 + Re:Earth (`https://plateauview.mlit.go.jp/` で `/cesium-1.118.0/Cesium.js` および Re:Earth 関連の記述を確認) |
| フレームワーク | React (ポータルサイト `www.mlit.go.jp/plateau/` は Next.js 1.3.0 / React で構築) |
| 背景の地図とタイル | 国土地理院の地理院タイル、衛星画像、PLATEAU 3D Tiles・MVT・地形データ |
| 投稿やデータの保存先 | Google Cloud / PLATEAU CMS (Re:Earth CMS) 等の配信基盤 |
| 配信 | Google Frontend (ビューア `plateauview.mlit.go.jp` は `server: Google Frontend`, `via: 1.1 google`。ポータル `www.mlit.go.jp/plateau/` は Amazon S3 + CloudFront) |

メモ:

- ウェブ版のみで、公式の iOS / Android アプリは提供されていない。
- バージョン 1.x は TerriaJS ベース、バージョン 2.0 以降は OSS の Re:Earth (CesiumJS 内包) ベースで構築されており、現在 5.0 が稼働している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 3D 都市モデル (建物・地形・災害リスク等) | 国土交通省 Project PLATEAU・各自治体 | https://www.mlit.go.jp/plateau/ |
