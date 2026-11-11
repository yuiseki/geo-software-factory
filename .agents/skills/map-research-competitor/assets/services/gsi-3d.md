# 3次元地図可視化サイト

- URL: https://gsi-cyberjapan.github.io/gsi-3d-2025/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 国土地理院、3D 地図、地形、標高、点群、災害、空中写真

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 国土地理院の地図、空中写真、標高、点群、近年の災害の情報を、3 次元と地球儀の表示で重ねて見るサイト |
| 提供する価値 | 地形や災害の状況を立体で確かめ、計測、作図、共有ができる |
| 想定する利用者 | 防災や測量の担当者、地理を学ぶ人と教える人、地形に関心がある人 |
| 商用か非商用か | 非商用 (国の機関の公開) |
| 推定の売上 | なし (非商用) |
| 運営 | 公的機関 (国土地理院。GitHub の組織 gsi-cyberjapan) |
| 推定の運用費 | 推測: サイトは 0 円 (GitHub Pages)。地理院タイルの配信の費用は国の予算で、このサイトの分は分けられない |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS |
| フレームワーク | Next.js |
| 背景の地図とタイル | 地理院タイル |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | GitHub Pages |

読み込んだタイルとスタイルの URL (一部):

- `https://cyberjapandata.gsi.go.jp/3dmaps/buildings/{z}/{x}/{y}.pbf`
- `https://cyberjapandata.gsi.go.jp/xyz/dem1a_png/{z}/{x}/{y}.png`
- `https://cyberjapandata.gsi.go.jp/xyz/optimal_bvmap-v1/optimal_bvmap-v1.pmtiles`
- `https://raw.githubusercontent.com/gsi-cyberjapan/3dpc-3dtiles/refs/heads/main/public/styles/std.json`

データの出どころ (地図の帰属表示と画面の最下部 500 字、2026-11-12):

- 地図の帰属表示: 「国土地理院最適化ベクトルタイル(標準地図風スタイル) | MapLibre」
