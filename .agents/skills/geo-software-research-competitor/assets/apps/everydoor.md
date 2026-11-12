# Every Door

- URL: https://every-door.app/
- 観測した日: 2026-11-12
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: OpenStreetMap、OSM の編集、店舗、POI、ベンチ、入口、マッピング

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 店やベンチ、街灯、建物の入口を、歩きながら確かめて OSM に足し直す編集アプリ |
| 提供する価値 | モールを歩いて、まだある店にチェックを付け、無い店を足すだけで、街の地図を新しく保てる |
| 想定する利用者 | OSM のマッパー、街の店の情報を新しくしたい人 |
| 商用か非商用か | 非商用と見られる (GPL-3.0 の OSS。広告、アプリ内課金は無い。寄付の受け付けは未確認) |
| 推定の売上 | なし (非商用と見られる) |
| 運営 | 個人 (作者 Ilya Zverev。App Store の販売元は AvatudKaart OÜ) |
| 推定の運用費 | 推測: 月数千円以下。編集は端末から OSM の API へ直接送る。紹介のサイトは GitHub Pages |

## 技術 (2026-11-12 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | iOS と Android のアプリ |
| 描画 | flutter_map と vector_map_tiles |
| フレームワーク | Flutter (Dart) |
| 背景の地図とタイル | 未確認 (ソースの設定で確かめられる) |
| 投稿やデータの保存先 | OpenStreetMap (利用者のアカウントで直接編集) |
| 配信 | App Store、Google Play |

ストアの表示 (2026-11-12):

- App Store: 販売元 AvatudKaart OU、無料、評価 2 件 (平均 5.0)、初出 2022-08-13、最新の更新 2025-10-24 (https://apps.apple.com/jp/app/id1621945342)
- Google Play: `info.zverev.ilya.every_door`、1万+ ダウンロード、開発元 Ilja Zverev、アプリ内購入 表示なし

メモ:

- ソースは `Zverik/every_door` (GitHub、GPL-3.0)。`pubspec.yaml` に flutter_map 8.2.0 と vector_map_tiles 9.0.0-beta.8、flutter_map_mbtiles (2026-11-12)
- アプリの中は端末で開いていない。描画などで「未確認」としたところは、端末でオープンソースのライセンスの一覧と通信を見て確かめる
