---
financial: commercial
organization: individual
---

# WorldGuessr

- URL: https://www.worldguessr.com/
- ソース: https://github.com/codergautam/worldguessr (PolyForm Noncommercial License)
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: WorldGuessr、codergautam、GeoGuessr代替、オープンソース、Google Street View、Leaflet、Next.js、ストリートビューゲーム

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 無料で遊べるオープンソース（非商用ライセンス）の GeoGuessr 風ストリートビュー位置当てゲーム |
| 提供する価値 | 課金や回数制限なしでシングルプレイ・マルチプレイ対戦・カスタムマップ作成を楽しめ、ソースコードも公開されている |
| 想定する利用者 | 無料で地理当てゲームを遊びたいプレイヤー、学校・学生、コードやロケーションデータ作成を学びたい開発者 |
| 商用か非商用か | 商用・広告併用（プレイヤー向け基本無料。Web/アプリ内の広告等による運営で、コード自体は PolyForm Noncommercial License で公開） |
| 推定の売上 | 推測: 年数百万円規模（月間多数のプレイヤーを抱え、広告収益等で API・サーバー費を賄うが具体額は非公開） |
| 運営 | 個人 / 個人法人（Gautam Anand / `codergautam`、Google Play 公開名義は CoderGautam LLC） |
| 推定の運用費 | 推測: 月数十万〜百万円規模（Google Street View / Maps の利用に加え、マルチプレイ用 Express サーバーと MongoDB を維持） |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API（Street View 表示）および Leaflet（推測用ミニマップ・マップ機能。GitHub の `package.json` で `@googlemaps/js-api-loader` と `leaflet` を確認） |
| フレームワーク | Next.js + React（HTML 内の `/_next/static/` チャンクおよび `package.json` の `next` を確認） |
| 背景の地図とタイル | Google Street View、OpenStreetMap 系データ・国境ポリゴン（`package.json` に `@osm_borders/maritime_10m` を確認） |
| 投稿やデータの保存先 | MongoDB + Express バックエンド（`package.json` の `mongoose`、`express`、Google OAuth 等を確認） |
| 配信 | Cloudflare（応答ヘッダーで `server: cloudflare`、`cf-ray` を確認） |

メモ:

- ウェブ版のほか iOS / Android の公式モバイルアプリも提供されており、アカウントや ELO レーティングが同期される。
- GitHub でコードが公開されているが、ライセンスは非商用限定（PolyForm Noncommercial）であり、商用フォークは禁止されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| パノラマ・地図表示 | Google Street View / Google Maps Platform | GitHub `package.json` および公式サイト |
| 領海・国境判定等 | OpenStreetMap 由来データ（`@osm_borders/maritime_10m` 等） | GitHub `package.json` |
