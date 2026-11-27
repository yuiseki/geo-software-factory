---
financial: commercial
organization: corp-smb
first_seen: 2009-09-05
first_seen_by: wayback
---

# MapTiler

- URL: https://www.maptiler.com
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: MapTiler、OpenMapTiles、ベクタタイル、スイス、セルフホスト、MapLibre、地理空間クラウド、航空写真

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | OpenStreetMap 等をベースにしたベクタ・ラスタタイル配信、マップデザインツール、オンプレミス向けタイルサーバーを提供するスイスの地図プラットフォーム |
| 提供する価値 | MapLibre と親和性の高いベクタタイル、70 言語以上対応の地図スタイル、衛星画像・地形データを手軽にクラウドまたは自社サーバーで配信できる |
| 想定する利用者 | 地図アプリ・Web サービスの開発者、自治体・企業、Google Maps や Mapbox からの移行を検討する組織 |
| 商用か非商用か | 商用 (非商用・検証向けの無料プランあり: クレジットカード不要。商用本番向けの Flex プランは月額 $30 から従量課金、大規模向けの Custom プランあり) |
| 推定の売上 | 推測: 年数億〜十数億円規模。世界中の開発者・企業に MapTiler Cloud と MapTiler Server (セルフホスト製品) を提供しているが、非上場のため公式売上は非公開 |
| 運営 | 企業 (MapTiler AG、スイス) |
| 推定の運用費 | 推測: 月数千万円規模。全世界のベクタタイル生成パイプライン、高解像度航空写真・衛星画像処理、グローバル CDN 配信を運用している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapTiler SDK / MapLibre GL JS 互換およびネイティブ Mobile SDK (Swift / Kotlin、BSD-3 ライセンスで OSS 公開。サイト HTML 内に `mapbox` の文字列も確認) |
| フレームワーク | Next.js + React (`/_next/static/chunks/` および `react` を HTML 内で確認) |
| 背景の地図とタイル | 自前の MapTiler Cloud タイル (OpenMapTiles ベースのベクタタイル、衛星画像、地形データ) |
| 投稿やデータの保存先 | MapTiler Cloud ストレージ (ユーザーがアップロードした GeoJSON や MBTiles 等をホスティング可能) |
| 配信 | Cloudflare (`server: cloudflare` を応答ヘッダーで確認) |

メモ:

- 一般消費者向けの地図アプリではなく、開発者向けのオープンソース SDK（iOS Swift / Android Kotlin 等）を提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| ベースマップ | OpenStreetMap (OSM) / OpenMapTiles プロジェクト | MapTiler 公式サイト |
| 衛星画像・標高・公的データ | 各国政府オープンデータ、商用衛星画像プロバイダ等 | MapTiler 公式サイト |
