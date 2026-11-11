# 浸水センサ表示システム（国土交通省）

- URL: https://c-sensor.river.go.jp/map/index?x=15028131.25709&y=4478521.57355&z=5.23368&r=0
- 観測した日: 2026-11-11

| 項目 | 観測したもの |
|---|---|
| 描画 | OpenLayers |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | 地理院タイル、自前のタイル (サイトと同じドメイン) |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | CloudFront 経由 (nginx/1.14.1) |

読み込んだタイルとスタイルの URL (一部):

- `https://c-sensor.river.go.jp/map/public/tile_data/prefs/{z}/{x}/{y}.mvt`
- `https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png`

メモ:

- 国土交通省の浸水センサの表示。都道府県の境界を自前のベクトルタイル (`.mvt`) で配っている
