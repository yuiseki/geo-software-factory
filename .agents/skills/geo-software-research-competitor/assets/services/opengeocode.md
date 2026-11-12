# OpenGeocode: free, open-source, self-hosted geocoding

- URL: https://opengeocode.com/
- 観測した日: 2026-11-12
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: ジオコーディング、住所検索、逆ジオコーディング、セルフホスト、OSS、Rust

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | OSM と OpenAddresses から作った 1 ファイルで、住所の検索、逆ジオコーディング、補完、一括処理を自分のサーバーで動かすオープンソースのジオコーダ |
| 提供する価値 | 住所をネットの外に出さず、検索 1 回ごとの料金なしでジオコーディングできる (6.4 億件の住所) |
| 想定する利用者 | ジオコーディングを使う開発者と組織 |
| 商用か非商用か | 非商用 (MIT。料金は「$0. No tiers, no seats, no per-lookup fees」と明記) |
| 推定の売上 | なし (非商用) |
| 運営 | 団体 (OpenGeocode contributors。GitHub の組織 open-geocode-rs) |
| 推定の運用費 | 推測: 月数千円。紹介とデモのサイトは Cloudflare の配信。デモの検索は Cloudflare Worker と Tunnel の先の VM (open-geocode-live の説明) |

## 技術 (2026-11-12 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 地図ライブラリの名前は見つからなかった |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | 見つからなかった |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Cloudflare |

メモ:

- トップページを開いた。地図の画面そのもの (アプリ、デモ、ダウンロード版) は開いていない

データの出どころ (地図の帰属表示と画面の最下部 500 字、2026-11-12):

- 地図の帰属表示: 「© OpenFreeMap © OpenMapTiles © OpenStreetMap contributors」
