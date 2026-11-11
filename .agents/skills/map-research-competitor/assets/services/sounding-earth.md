# THE SOUNDING EARTH

- URL: https://musica-terra.com/interactive/the-sounding-earth/
- 観測した日: 2026-11-11

| 項目 | 観測したもの |
|---|---|
| 描画 | three.js |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | 使っていない (4K の地球の画像を three.js の球に貼り、文化圏を塗った画像を重ねる) |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | nginx (静的な配信) |

メモ:

- 地球儀を回して、地域と年代の音楽を聴く作品。地図ライブラリは使っていない
- データは `earth.json` 1 本 (1.7 MB)。文化圏、アルバム (Apple Music の ID つき)、場所、音楽の系譜の線とその出典を持つ
- 試聴の音源は、その場で iTunes Search API の lookup を呼んで `previewUrl` を取り、Web Audio でつないで流す。ジャケットの画像も Apple の配信元から取る
