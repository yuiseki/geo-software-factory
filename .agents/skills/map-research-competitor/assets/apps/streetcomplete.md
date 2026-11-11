# StreetComplete

- URL: https://streetcomplete.app/
- 観測した日: 2026-11-12
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: OpenStreetMap、OSM の編集、クエスト、地図の改善、貢献、マッピング

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 近くの OSM の地図の抜けを「クエスト」として地図に出し、現地で簡単な質問に答えると OSM が直る編集アプリ |
| 提供する価値 | OSM の知識が無くても、歩きながら答えるだけで地図をよくできる |
| 想定する利用者 | OSM に貢献したい一般の人、散歩をする人 |
| 商用か非商用か | 商用 (寄付。作者への GitHub Sponsors、Liberapay、Patreon。Liberapay の表示で週 54.64 EUR、支援者 108 人、2026-11-12) |
| 推定の売上 | 推測: 年数百万円 (寄付の合計。Liberapay だけで年約 2,800 EUR。ほかの経路と助成の額は未確認) |
| 運営 | 個人 (作者 Tobias Zwick (westnordost)。GitHub の組織 streetcomplete) |
| 推定の運用費 | 推測: 月数千円。編集は利用者の端末から OSM の API へ直接送るので、サーバーはほとんど要らない |

## 技術 (2026-11-12 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | iOS と Android のアプリ (iOS 版は 2026-11-04 に App Store に出た) |
| 描画 | MapLibre (maplibre-compose 0.20.0) |
| フレームワーク | Kotlin |
| 背景の地図とタイル | 未確認 (ソースの設定で確かめられる) |
| 投稿やデータの保存先 | OpenStreetMap (利用者のアカウントで直接編集) |
| 配信 | Google Play、App Store |

ストアの表示 (2026-11-12):

- App Store: 販売元 Tobias Zwick、無料、評価 0 件、初出 2026-11-04、最新の更新 2026-11-05 (https://apps.apple.com/jp/app/id6808344816)
- Google Play: `de.westnordost.streetcomplete`、10万+ ダウンロード、開発元 westnordost、アプリ内購入 表示なし

メモ:

- ソースは `streetcomplete/StreetComplete` (GitHub、GPL-3.0、スター約 5,100)。`gradle/libs.versions.toml` に maplibre-compose 0.20.0 (2026-11-12)
- アプリの中は端末で開いていない。描画などで「未確認」としたところは、端末でオープンソースのライセンスの一覧と通信を見て確かめる
