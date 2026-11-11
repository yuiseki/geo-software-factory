# Urbanist Map

- URL: https://urbanistmap.org/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界の都市の建設中や計画中の開発プロジェクトを、利用者が登録して共有する地図 |
| 提供する価値 | どの街で何が建とうとしているかを、地図の上で探して追える |
| 想定する利用者 | 都市開発に関心がある人、建築や都市計画の愛好家 (いまはベルギーの投稿が多い) |
| 商用か非商用か | 非商用 (広告、寄付、有料プランは見えなかった。コードを GitHub で公開) |
| 推定の売上 | なし (非商用) |
| 運営 | 個人 (GitHub の個人アカウント Leni-Vienne) |
| 推定の運用費 | 推測: 月数百〜数千円。Cloudflare の配信、OpenFreeMap のタイル、投稿を受けるサーバー |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS |
| フレームワーク | Vue |
| 背景の地図とタイル | OpenFreeMap |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Cloudflare |

読み込んだタイルとスタイルの URL (一部):

- `https://tiles.openfreemap.org/natural_earth/ne2sr/{z}/{x}/{y}.png`
- `https://tiles.openfreemap.org/planet/20261101_080013_pt/{z}/{x}/{y}.pbf`
- `https://tiles.openfreemap.org/styles/liberty`
