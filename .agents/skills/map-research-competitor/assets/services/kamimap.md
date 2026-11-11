# 令和8年熊本地震関連情報 - 紙マップ

- URL: https://kamimap.com/map/2026-kumamoto-earthquake/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 災害、支援情報、給水所、避難所、紙の地図、印刷、Code for Japan

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 災害のとき、給水所、避難所、入浴施設、ガソリンスタンドなどの支援の情報を、A4 に印刷しやすい形で示す地図 |
| 提供する価値 | スマートフォンを持たない人にも、紙に印刷して支援の情報を届けられる |
| 想定する利用者 | 被災地の住民と、印刷して配る支援者や自治体 |
| 商用か非商用か | 非商用 (Code for Japan のオープンソースのプロジェクト) |
| 推定の売上 | なし (非商用) |
| 運営 | 団体 (一般社団法人 Code for Japan の有志) |
| 推定の運用費 | 0 円と見られる。GitHub Pages の静的配信と OpenStreetMap Japan のタイル。情報を集める人の時間が主 |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS、Mapbox GL JS |
| フレームワーク | Nuxt、Vue |
| 背景の地図とタイル | OpenStreetMap Japan のタイル |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | GitHub Pages |

読み込んだタイルとスタイルの URL (一部):

- `https://tile.openstreetmap.jp/data/planet/{z}/{x}/{y}.pbf`
- `https://tile.openstreetmap.jp/styles/maptiler-basic-ja/sprite.json`
- `https://tile.openstreetmap.jp/styles/maptiler-basic-ja/sprite.png`
- `https://tile.openstreetmap.jp/styles/maptiler-basic-ja/style.json`

データの出どころ (地図の帰属表示と画面の最下部 500 字、2026-11-12):

- 地図の帰属表示: 「© OpenMapTiles © OpenStreetMap contributors」
