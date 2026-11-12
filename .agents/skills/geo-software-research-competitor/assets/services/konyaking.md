# こにゃーきんぐ

- URL: https://spotsharemap.github.io/sharewitheveryone/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 作業場所、カフェ作業、Web 会議、電源、Wi-Fi、通話できる場所、コワーキング

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 会話してよいか、電源や Wi-Fi があるかを、実際に使った人の声で確かめて選ぶ、作業と通話の場所の地図 |
| 提供する価値 | オンライン面接や Web 会議、打ち合わせができる場所を、駅や目的から探せる |
| 想定する利用者 | 外で Web 会議や作業をする会社員、就職活動の学生 |
| 商用か非商用か | 非商用 (広告、寄付、有料プランは見えなかった。OSM への貢献を呼びかける) |
| 推定の売上 | なし (非商用) |
| 運営 | 個人か有志 (GitHub の組織 spotsharemap。運営者の表示は見つからなかった) |
| 推定の運用費 | 推測: 月 0〜数百円。GitHub Pages の静的配信、OpenFreeMap のタイル、Firestore (無料枠の範囲と見られる) |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS 4.7.1、Leaflet |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | OpenFreeMap |
| 投稿やデータの保存先 | Firestore |
| 配信 | GitHub Pages |

読み込んだタイルとスタイルの URL (一部):

- `https://tiles.openfreemap.org/planet/20261101_080013_pt/{z}/{x}/{y}.pbf`
- `https://tiles.openfreemap.org/styles/positron`

メモ:

- 投稿の保存に Firestore を使っている

データの出どころ (地図の帰属表示と画面の最下部 500 字、2026-11-12):

- 地図の帰属表示: 「ver. 2026-11-08e ・ 地図データ © OpenStreetMap contributors（ODbL）・淡色の背景地図 国土地理院・シンプル地図 OpenFreeMap © OpenMapTiles・地名と施設 Overture Maps Foundation・Leaflet」 ／ 「地図データ © OpenStreetMap contributors（ODbL）・淡色の背景地図 国土地理院・シンプル地図 OpenFreeMap © OpenMapTiles・地名と施設 Overture Maps Foundation・Leaflet」
