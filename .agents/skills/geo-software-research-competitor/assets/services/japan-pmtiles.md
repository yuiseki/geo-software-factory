# 自分のサーバーで日本地図を表示する｜Japan PMTiles

- URL: https://armd-01.sakura.ne.jp/tiles/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: PMTiles、自前の地図配信、セルフホスト、日本地図、ベクトルタイル、OSM、API キー不要

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 日本全体の OSM の地図を PMTiles 1 本 (1.6 GB) とスタイルで配り、自分のサーバーで地図を出す方法を示す開発者向けのサイト |
| 提供する価値 | API キーも回数課金もなしに、静的なファイルを置くだけで日本地図を表示できる |
| 想定する利用者 | 地図 API の費用や制約を避けたいウェブの開発者 |
| 商用か非商用か | 非商用 (広告、寄付は見えなかった) |
| 推定の売上 | なし (非商用) |
| 運営 | 個人 (作成・管理 K.Sakanoshita) |
| 推定の運用費 | 推測: 月数百〜数千円。さくらのレンタルサーバーで 1.6 GB のファイルを配る。ダウンロードが多いと転送量の上限にかかりうる |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | OpenStreetMap Japan のタイル、自前のタイル (サイトと同じドメイン) |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | nginx (配信先の事業者は不明) |

読み込んだタイルとスタイルの URL (一部):

- `https://armd-01.sakura.ne.jp/tiles/japan-20260806.pmtiles`
- `https://armd-01.sakura.ne.jp/tiles/style.css`
- `https://tile.openstreetmap.jp/styles/osm-bright/sprite.json`
- `https://tile.openstreetmap.jp/styles/osm-bright/sprite.png`

データの出どころ (地図の帰属表示と画面の最下部 500 字、2026-11-12):

- フッターに「作成・管理 K.Sakanoshita 地図データ © OpenStreetMap contributors」(初めの観測)
