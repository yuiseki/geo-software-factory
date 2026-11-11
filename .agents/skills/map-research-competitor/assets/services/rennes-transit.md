# Rennes Transit Map - Visualisation temps réel du réseau STAR

- URL: https://nahelou.github.io/rennes-transit-map/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | フランスのレンヌの公共交通 STAR のバスの位置と地下鉄を、リアルタイムに 3 次元のアニメーションで示す地図 |
| 提供する価値 | 街のバスと地下鉄が今どこを走り、どれだけ遅れているかを動く地図で見られる |
| 想定する利用者 | レンヌの住民と公共交通の利用者、交通のオープンデータに関心がある人 |
| 商用か非商用か | 非商用 (広告、寄付は見えなかった) |
| 推定の売上 | なし (非商用) |
| 運営 | 個人 (GitHub の個人アカウント nahelou) |
| 推定の運用費 | 0 円と見られる。GitHub Pages の静的配信と、フランス政府 (data.gouv.fr) のタイル、STAR のオープンデータ |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | data.gouv.fr の OpenMapTiles |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | GitHub Pages |

読み込んだタイルとスタイルの URL (一部):

- `https://openmaptiles.data.gouv.fr/data/planet-vector/{z}/{x}/{y}.pbf`
