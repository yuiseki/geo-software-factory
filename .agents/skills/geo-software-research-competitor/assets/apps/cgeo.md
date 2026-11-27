---
financial: commercial
organization: individual
first_seen: 2011-07-11
first_seen_by: github
---

# c:geo

- URL: https://www.cgeo.org/
- ソース: https://github.com/cgeo/cgeo (Apache-2.0。2026-11-17 に確かめた)
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ジオキャッシング、Geocaching、OpenStreetMap、Mapsforge、オフライン地図、OSS、Android

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中のジオキャッシング (宝探し) に対応したコミュニティ開発のオープンソース Android クライアント |
| 提供する価値 | Geocaching.com 等のキャッシュ情報をライブ地図やオフライン地図 (Mapsforge) 上で検索・保存し、電波のない場所でもコンパスやナビゲーションで探索できる |
| 想定する利用者 | Android を使うジオキャッシング愛好家、オフラインでキャッシュ探索を行いたいユーザー |
| 商用か非商用か | 商用 (Apache-2.0 の OSS、広告なし・無料だが、公式サイトで PayPal による寄付を受け付けており Google Play でもアプリ内購入の表示あり) |
| 推定の売上 | 推測: 寄付ベース (金額非公開)。Google Play 500万+ ダウンロード |
| 運営 | 団体 (c:geo team、OSS コミュニティ) |
| 推定の運用費 | 推測: 月数千円以下。地図やキャッシュデータは外部サービスや端末内オフラインファイルから直接取得し、紹介サイトは GitHub Pages でホスト |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | Android のアプリ |
| 描画 | Mapsforge (`0.28.0`)、Mapsforge VTM (`0.28.0`)、Google Maps SDK (`play-services-maps:20.0.0`) (`main/build.gradle` で確認) |
| フレームワーク | Android ネイティブ (Java / Kotlin) |
| 背景の地図とタイル | OpenStreetMap 系のオフラインベクター地図 (Mapsforge `.map` 等)、Google マップ等 (外部連携で MAPS.ME、Organic Maps、Locus Maps にも対応) |
| 投稿やデータの保存先 | 端末内、および利用者が連携するジオキャッシングサービス (Geocaching.com 等) |
| 配信 | Google Play (GitHub Releases からも APK 配布) |

ストアの表示 (2026-11-17):

- Google Play: `cgeo.geocaching`、500万+ ダウンロード、開発元 c:geo team、アプリ内購入 あり
- App Store: 配信なし (Android のみ)

メモ:

- ソースは `cgeo/cgeo` (GitHub、Apache-2.0)。`main/build.gradle` に Mapsforge `0.28.0` と VTM `0.28.0`、Google Play Services Maps `20.0.0` の記載を確認 (2026-11-17)
- アプリの中は端末で開いていない。実際の通信先やライセンス一覧は端末で確かめる
