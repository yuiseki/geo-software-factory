---
financial: non-commercial
organization: individual
---

# squidmaps

- URL: https://squidmaps.io/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: squidmaps、Chris Whong、Placemark、MapLibre、Protomaps、PMTiles、カスタムマップ作成、GeoJSON

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ブラウザ上で手軽にカスタム地図を作成・装飾・共有できる、Placemark 系譜の無料カスタムマップメーカー |
| 提供する価値 | GIS の専門知識がなくても、マーカー・線・ポリゴンの描画やデータ取り込みを行い、シンプルな URL や埋め込みで見栄えの良い地図をすぐ共有できる |
| 想定する利用者 | ジャーナリスト、都市計画・地域活動家、ブロガー、イベント主催者、軽量な地図を作りたい一般ユーザー |
| 商用か非商用か | 非商用・無料提供（現時点では無料で利用できる個人開発のホスト型 Web サービス。リポジトリは非公開） |
| 推定の売上 | 推測: 0 円〜少額（招待・ベータ段階から無料公開されており、明確な有料プランは前面に出ていない） |
| 運営 | 個人（Chris Whong） |
| 推定の運用費 | 推測: 月数千円〜数万円程度（Protomaps ベースのタイルや Cloudflare + Caddy による軽量ホスティングで運用費を抑えている） |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS（ランディング HTML 内に `maplibre` への参照を確認） |
| フレームワーク | Astro + React（HTML 内の `/_astro/` スクリプトおよび React コンポーネント構成を確認） |
| 背景の地図とタイル | Protomaps + OpenStreetMap（Placemark フォーク系譜として Protomaps ベースマップを採用） |
| 投稿やデータの保存先 | ホスト型バックエンド（作成した地図データの保存・共有用 API） |
| 配信 | Cloudflare + Caddy（応答ヘッダーで `server: cloudflare`、`via: 1.1 Caddy` を確認） |

メモ:

- 元の Placemark（オープンソース化されたブラウザ地図エディタ）をフォーク・発展させた事例であり、MapLibre + Protomaps によってタイル課金をほぼゼロに抑えつつ高機能な地図編集 UI を実現している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| ベースマップ | OpenStreetMap（Protomaps 経由） | https://squidmaps.io/ および作者解説 |
| ユーザー作成地物 | 利用者がブラウザ上で作成・インポートした GeoJSON 等 | サイト機能 |
