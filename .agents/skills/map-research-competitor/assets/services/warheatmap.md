# WAR 3.0 - Live World War 3 Heat Map & Real-Time Conflict Tracker

- URL: https://warheatmap.app/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 戦争、紛争、ヒートマップ、OSINT、ウクライナ、中東

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 公開情報 (OSINT) から集めた世界の 6,000 件を超える紛争の出来事を、熱分布で示すリアルタイムの地図 |
| 提供する価値 | ウクライナ、イラン、中東などの戦況を 1 枚の地図で、ほぼ毎時に追える |
| 想定する利用者 | 国際情勢と戦況を追う一般の人 |
| 商用か非商用か | 非商用と見られる (広告と有料プランは見えなかった。寄付はウクライナの政府の基金へのリンクで、運営者の収入ではない) |
| 推定の売上 | なし (非商用と見られる) |
| 運営 | 個人と見られる (運営者の表示は見つからなかった) |
| 推定の運用費 | 推測: 月数千円。Cloudflare の配信、Supabase (無料か月 25 USD)、Esri のベースマップ |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS 4.7.1 |
| フレームワーク | React |
| 背景の地図とタイル | Esri (ArcGIS) のベースマップ |
| 投稿やデータの保存先 | Supabase |
| 配信 | Cloudflare |

読み込んだタイルとスタイルの URL (一部):

- `https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{x}/{y}`
- `https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{x}/{y}`
