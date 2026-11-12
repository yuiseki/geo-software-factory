# trainsworld

- URL: https://anita.garden/trainsworld/
- 観測した日: 2026-11-12
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 鉄道ゲーム、列車、路線を作る、交通シミュレーション、世界地図

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 実在の世界地図の上に線路と駅を敷いて列車を走らせる、無料のブラウザの鉄道建設ゲーム |
| 提供する価値 | 現実の人口と需要のデータで、何千もの駅の路線網を組み、乗客の経路選びまで遊べる |
| 想定する利用者 | 鉄道や都市交通のゲームが好きな人 |
| 商用か非商用か | 非商用 (無料のゲーム。広告、寄付、有料プランは見えなかった) |
| 推定の売上 | なし (非商用) |
| 運営 | 個人 (anita.garden の個人のサイト) |
| 推定の運用費 | 推測: 月 0〜数千円。GitHub Pages を Cloudflare の後ろから配り、OpenFreeMap のタイルと自前の PMTiles (data.anita.garden) |

## 技術 (2026-11-12 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | OpenFreeMap |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Cloudflare 経由の GitHub Pages |

読み込んだタイルとスタイルの URL (一部):

- `https://tiles.openfreemap.org/planet/20261101_080013_pt/{z}/{x}/{y}.pbf`
- `https://tiles.openfreemap.org/styles/positron`

データの出どころ (地図の帰属表示と画面の最下部 500 字、2026-11-12):

- 画面の最下部ほか: 「© EuroGeographics for the administrative boundaries」「© OpenMapTiles」(ページの HTML の中、初めの観測)
