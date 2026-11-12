# 日本苗字アトラス

- URL: https://www.myoji-atlas.com/
- 観測した日: 2026-11-12
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 苗字、名字、姓、分布、町丁目、ルーツ、家系

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の苗字の分布を、都道府県、旧市区町村 (2000 年)、大字町丁目の 3 つの単位で地図に示すサイト |
| 提供する価値 | 苗字がどこに集中し、どこで分散しているかを、町丁目の細かさまで見られる |
| 想定する利用者 | 苗字に関心がある人 (「苗字マニアによる苗字マニアのための」とサイトの説明)、地域の歴史を調べる人 |
| 商用か非商用か | 商用 (Google AdSense の広告と、Square での寄付) |
| 推定の売上 | 推測: 月数千〜数万円。2025-10-12 に公開 |
| 運営 | 個人 (管理人 すかわら) |
| 推定の運用費 | 推測: 月数百〜数千円。Cloudflare の後ろの Express のサーバー、自前の PMTiles (市区町村、町丁目)、地理院タイル。苗字の集計は手元で行う |

## 技術 (2026-11-12 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | 地理院タイル、自前のタイル (サイトと同じドメイン) |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Cloudflare |

読み込んだタイルとスタイルの URL (一部):

- `https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png`
- `https://www.myoji-atlas.com/tiles/muni-point.pmtiles`
- `https://www.myoji-atlas.com/tiles/muni.pmtiles`
- `https://www.myoji-atlas.com/tiles/neigh-point.pmtiles`
- `https://www.myoji-atlas.com/tiles/neigh.pmtiles`
- `https://www.myoji-atlas.com/tiles/pref-point.pmtiles`

メモ:

- 苗字は電話帳と住宅地図などから集計し、読みは市販の住所データから推計したとサイトの説明。境界は国土数値情報 (2000 年) と経済センサスの小地域

データの出どころ (地図の帰属表示と画面の最下部 500 字、2026-11-12):

- 地図の帰属表示: 「地理院タイル（淡色地図）」
