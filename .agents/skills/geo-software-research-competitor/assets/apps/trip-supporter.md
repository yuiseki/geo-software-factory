---
financial: commercial
organization: individual
first_seen: 2026-08-28
first_seen_by: store
---

# Trip Supporter

- URL: https://chicchi.work/tripsupporter/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: グループ旅行、旅程共有、現在地共有、割り勘、精算、Mapbox、Expo、React Native

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | グループ旅行のスケジュール・チャット・現在地マップ共有・立て替え精算を 1 つのスペースにまとめる個人開発アプリ |
| 提供する価値 | 旅行ごとにメンバーを招待し、別行動中の現在地確認や集合場所ピン共有、日程管理、割り勘精算までを幹事の負担を減らしながら完結できる |
| 想定する利用者 | 友人や家族とグループ旅行をする人、幹事や会計のやり取りを一元化したい人 |
| 商用か非商用か | 商用 (無料ダウンロード、リアルタイム位置共有等に使うチケットのアプリ内課金と Google AdMob 広告あり) |
| 推定の売上 | 推測: 初期段階。App Store の評価 1 件、2026年8月リリース |
| 運営 | 個人 (ちっち / DAICHI NEMOTO) |
| 推定の運用費 | 推測: 月数千円〜数万円。Firebase (Firestore / Realtime Database / Cloud Functions)、Mapbox の地図利用料 |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | iOS のアプリ |
| 描画 | Mapbox (開発者の技術記事・サイトで言及) |
| フレームワーク | React Native / Expo (TypeScript) (開発者の技術記事等で確認) |
| 背景の地図とタイル | Mapbox |
| 投稿やデータの保存先 | Firebase / Google Cloud (Firestore、Realtime Database、Cloud Functions) |
| 配信 | App Store |

ストアの表示 (2026-11-17):

- App Store: 販売元 DAICHI NEMOTO、無料 (アプリ内課金・広告あり)、評価 1 件 (平均 5.0)、初出 2026-08-28、最新の更新 2026-10-29 (https://apps.apple.com/jp/app/id6787812825)
- Google Play: 配信なし (2026-11-17 時点)

メモ:

- 開発者の技術ブログ・Zenn/Qiita 記事等で React Native (Expo)、Firebase、Mapbox、RevenueCat、AdMob の構成が公開されている
- アプリの中は端末で開いていない。実際の通信先や詳細なライセンスは端末で確かめる
