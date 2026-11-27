---
financial: public-service
organization: gov-central
first_seen: 2014-04-22
first_seen_by: github
---

# NASA Worldview

- URL: https://worldview.earthdata.nasa.gov
- ソース: https://github.com/nasa-gibs/worldview (NASA-1.3 / NASA Open Source Agreement v1.3)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: NASA Worldview、GIBS、衛星画像、地球観測、MODIS、VIIRS、山火事、気象、OpenLayers、NASA

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | NASA の地球観測衛星が毎日撮影する高解像度の全球画像や環境レイヤーを、過去から数時間前まで遡って閲覧・アニメーション再生できる Web アプリ |
| 提供する価値 | 1,000 以上の衛星観測レイヤー (山火事の熱点、大気汚染、台風、海氷、植生など) をログイン不要・無料で重ね合わせ、時間軸スライダーで変化を比較して画像や GIF として書き出せる |
| 想定する利用者 | 気象・環境研究者、防災・山火事監視担当者、報道機関、教育関係者、地球観測に関心のある一般利用者 |
| 商用か非商用か | 非商用・公共サービス (米国連邦政府機関 NASA EOSDIS による完全無料提供。データとソフトウェアはオープン公開) |
| 推定の売上 | なし (米国政府予算による公的運用) |
| 運営 | 政府機関 (NASA EOSDIS / Earth Science Data and Information System、米国) |
| 推定の運用費 | 推測: 月数千万円〜億円規模 (GIBS によるペタバイト級の日次衛星タイル生成・保持および CloudFront での世界配信) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | OpenLayers (`nasa-gibs/worldview` において WMTS/WMS タイル描画および極座標投影処理に採用) |
| フレームワーク | React 等のコンポーネントベース JavaScript バンドル (`build/wv.js` を確認) |
| 背景の地図とタイル | NASA GIBS (Global Imagery Browse Services) の WMTS/WMS 衛星画像タイルおよび Blue Marble / 境界・地名オーバーレイ |
| 投稿やデータの保存先 | 保存先なし (表示レイヤーや日付・座標の状態は URL パラメータで共有) |
| 配信 | Amazon CloudFront (`via: CloudFront`、`server: ServerTokens ProductOnly` を応答ヘッダーで確認) |

メモ:

- 専用の iOS / Android アプリは提供されていない (Web ブラウザ専用、モバイルブラウザ対応)。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 衛星画像・地球観測データ | NASA (MODIS, VIIRS, GPM 等)、NOAA、ESA、JAXA 等 (GIBS 経由) | 公式サイト・GIBS ドキュメント |
