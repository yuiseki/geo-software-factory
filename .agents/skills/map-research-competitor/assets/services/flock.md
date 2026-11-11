# Flock camera map: Find the Flock cameras watching you | Proton

- URL: https://proton.me/flock-camera-map
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 米国の Flock 社のナンバー読み取りカメラの位置を、郵便番号で探せる地図 |
| 提供する価値 | 自分の近くで誰が車を記録しているかを知る権利に応える |
| 想定する利用者 | 米国の住民、プライバシーを気にする人 |
| 商用か非商用か | 商用 (企業の宣伝。地図は無料。Proton の有料プランのサイトの中にあり、本業への集客と見られる) |
| 推定の売上 | 地図そのものの売上は無い。Proton 全体の売上は未確認 |
| 運営 | 企業 (Proton AG、スイス) |
| 推定の運用費 | 推測: 月数千円以下 (地図の分だけ)。OpenFreeMap のタイルと、カメラの位置のデータの配信 |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS |
| フレームワーク | Astro、React |
| 背景の地図とタイル | OpenFreeMap |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | 不明 (応答ヘッダーに手がかりが無い) |

読み込んだタイルとスタイルの URL (一部):

- `https://tiles.openfreemap.org/planet/20261101_080013_pt/{z}/{x}/{y}.pbf`
- `https://tiles.openfreemap.org/styles/positron`
