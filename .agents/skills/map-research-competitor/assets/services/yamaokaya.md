# 非公式 山岡家 Map

- URL: https://www.yama.dayjournal.dev/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ラーメン山岡家の 4 ブランドの店舗と新店舗を地図で見る、非公式の地図 |
| 提供する価値 | 山岡家の店と新しく開く店を、ブランドごとに地図で探せる |
| 想定する利用者 | 山岡家のファン、近くの店を探す人 |
| 商用か非商用か | 非商用 (非公式のファンの地図。広告、寄付は見えなかった) |
| 推定の売上 | なし (非商用) |
| 運営 | 個人 (dayjournal.dev、非公式と明記) |
| 推定の運用費 | 推測: 月 0〜数百円。S3 と CloudFront の静的配信、Amazon Location Service の地図 (無料枠の範囲と見られる) |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | Amazon Location Service |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Amazon S3 + CloudFront |

読み込んだタイルとスタイルの URL (一部):

- `https://maps.geo.ap-northeast-1.amazonaws.com/maps/v0/maps/YamaokayaMap/tiles/{z}/{x}/{y}`
