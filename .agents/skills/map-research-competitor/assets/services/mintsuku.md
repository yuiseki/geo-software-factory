# みんなでつくる全国冠水道路マップ｜みんつく全国冠水マップ

- URL: https://mintsuku-kansuimap.com/
- 観測した日: 2026-11-11

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS 6.6.0 |
| フレームワーク | React |
| 背景の地図とタイル | Protomaps (フォントとスプライト)、自前のタイル (サイトと同じドメイン) |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Cloudflare |

読み込んだタイルとスタイルの URL (一部):

- `https://hazard-tiles.mintsuku-kansuimap.com/hazard-reports-20261110-193006.pmtiles`
- `https://tiles.mintsuku-kansuimap.com/japan-basemap-20260831/{z}/{x}/{y}.mvt`

メモ:

- 冠水の投稿を日付つきの PMTiles (`hazard-reports-YYYYMMDD-HHMMSS.pmtiles`) に焼いて配っていた。背景の地図も自前のベクトルタイル (2026-08-31 の版)
