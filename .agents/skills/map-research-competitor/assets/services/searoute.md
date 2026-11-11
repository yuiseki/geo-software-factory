# おでかけ航路マップ | 日本全国の旅客船・フェリー航路情報と時刻表リンク

- URL: https://searoute.info/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: フェリー、旅客船、航路、船、離島、時刻表

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 日本全国の旅客船とフェリーの航路を地図で探し、時刻表と運航会社のサイトへつなぐ地図 |
| 提供する価値 | どこからどこへ船で行けるかを、全国の航路を 1 枚で見て旅の計画に使える |
| 想定する利用者 | 船旅や離島への旅行を計画する人、フェリーの愛好家 |
| 商用か非商用か | 商用 (寄付。Amazon のほしいものリストで「運営の励み」を受け付ける)。広告と有料プランは見えなかった |
| 推定の売上 | 推測: 月数千円以下 (ほしいものリストの品物)。はてなブックマーク 1,123 件 (2026-11-12) |
| 運営 | 個人 (開発者 yy_kuso。コードと航路の PMTiles を GitHub で公開) |
| 推定の運用費 | 推測: 月 0〜数百円。Cloudflare の静的配信と自前の PMTiles、OpenStreetMap Japan のタイル (費用はかからない) |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | OpenStreetMap Japan のタイル、Protomaps (フォントとスプライト)、自前のタイル (サイトと同じドメイン) |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Cloudflare |

読み込んだタイルとスタイルの URL (一部):

- `https://pmtiles.searoute.info/searoute.pmtiles`
- `https://searoute.info/style/empty.json`
- `https://searoute.info/style/maptiler-basic-ja-custom.json`
- `https://searoute.info/style/sprite.json`
- `https://searoute.info/style/sprite.png`
- `https://tile.openstreetmap.jp/data/hoppo/{z}/{x}/{y}.pbf`
