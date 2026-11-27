---
financial: non-commercial
organization: individual
first_seen: 2014-11-07
first_seen_by: wayback
---

# Global Fishing Watch

- URL: https://globalfishingwatch.org/
- ソース: https://github.com/GlobalFishingWatch (関連ツール・コンポーネントを公開)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Global Fishing Watch、GFW、漁業監視、AIS、船舶追跡、海洋保護、IUU漁業、MapLibre、非営利

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 衛星 AIS データと機械学習を用いて世界中の商業漁船の活動や海上インフラを可視化する海洋透明性プラットフォーム |
| 提供する価値 | 公海や排他的経済水域における漁獲活動・違法漁業 (IUU) の兆候・船舶の航跡を誰でも無料で地図上から調査・分析できる |
| 想定する利用者 | 海洋研究者、政府・水産庁などの監視機関、環境 NGO、報道機関、一般市民 |
| 商用か非商用か | 非商用 (米国の 501(c)(3) 非営利団体。マップ閲覧・研究データ・API は原則無料で公開) |
| 推定の売上 | 年間収入約 2,040 万米ドル (年次報告・公開財務情報による。Bloomberg Philanthropies や The Audacious Project などの助成金・寄付が財源で商業売上ではない) |
| 運営 | 非営利団体 (Global Fishing Watch, Inc.、米国登記の 501(c)(3) 国際 NGO。EIN: 81-5461345) |
| 推定の運用費 | 年間支出約 2,495 万米ドル (公開財務報告による。うち約 82% が衛星データ処理・機械学習解析・プラットフォーム開発等の直接事業費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (2026-11-16 のコーポレートトップページ観測では jQuery のみ検出。公式 GitHub / NPM では `@globalfishingwatch/maplibre-gl` 等 MapLibre GL 系の独自フォーク・コンポーネントを公開) |
| フレームワーク | WordPress / PHP 8.4.27 (トップページ応答ヘッダーの `x-powered-by: PHP/8.4.27` および `wp-includes` への参照を確認。マップアプリ本体は別ドメイン等で運用) |
| 背景の地図とタイル | MapLibre ベースのカスタム海洋・海底地形・EEZ 境界タイル等 (推測: 独自のタイル・時系列データ配信基盤を使用) |
| 投稿やデータの保存先 | Google Cloud 上のデータ基盤と推測 (応答ヘッダー `via: 1.1 google` を確認) |
| 配信 | Cloudflare + Google (`server: cloudflare`、`via: 1.1 google` を確認) |

メモ:

- モバイルアプリは提供しておらず、PC ブラウザ向けの高度な可視化マップと Python / R クライアント、REST API を提供している。
- Mapbox GL JS のライセンス変更後に MapLibre エコシステムへ移行し、多数の関連ライブラリを GitHub 上でオープンソース公開している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 船舶位置・航跡データ | 衛星・地上 AIS (自動船舶識別装置)、VMS (各国政府提供)、SAR 衛星画像 | 公式サイトおよび技術ドキュメント |
| 海域境界・保護区 | Flanders Marine Institute (Marine Regions)、WDPA 等 | 公式サイトのマップ凡例・データ説明 |
