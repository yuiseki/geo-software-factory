---
financial: non-commercial
organization: individual
---

# kepler.gl

- URL: https://kepler.gl/
- ソース: https://github.com/keplergl/kepler.gl (MIT License、2026-11-16 確認)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: kepler.gl、Uber、Foursquare、deck.gl、MapLibre、大規模データ可視化、時空間データ、オープンソース GIS、WebGL

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 数百万点規模の位置情報や時空間データをブラウザ上で GPU 描画し、ノーコードで可視化・フィルタリングできるオープンソースの Web アプリ兼ライブラリ |
| 提供する価値 | CSV や GeoJSON ファイルをドラッグ＆ドロップするだけで、ポイント・アーク・ヒートマップ・H3 六角形グリッド・3D 押し出しなどの高度な地図可視化を即座に作れる |
| 想定する利用者 | データサイエンティスト、交通・モビリティ分析者、都市計画担当者、地図可視化を組み込みたいフロントエンド開発者 |
| 商用か非商用か | 非商用 OSS (MIT ライセンスで完全無料。Foursquare が保守を支援し、クラウド保存やチーム共有を加えた商用版として Foursquare Studio を別展開) |
| 推定の売上 | なし (kepler.gl 本体は OSS として無償提供) |
| 運営 | OSS コミュニティ・企業支援 (元は Uber が開発し、現在は Urban Computing Foundation および Foursquare がメンテナーとして関与) |
| 推定の運用費 | 推測: 月数千円から数万円程度 (kepler.gl 公式サイト自体は Netlify 上の静的フロントエンド配信で、計算処理はすべて利用者のブラウザ内で完結) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | deck.gl (WebGL/WebGPU) + MapLibre GL JS (v3.0 以降の標準ベースマップ。以前は Mapbox GL JS を利用) |
| フレームワーク | React + Redux (`/bundle.js` による SPA 構成) |
| 背景の地図とタイル | MapLibre / Mapbox 等のベースマップスタイルおよびカスタムタイル (利用者がスタイル URL やトークンを指定可能) |
| 投稿やデータの保存先 | ブラウザ内完結が基本 (データのアップロードはローカル処理。設定は JSON 書き出しや Dropbox 連携等で保存可能) |
| 配信 | Netlify (`server: Netlify`) |

メモ:

- v3.0 以降でベースマップの標準エンジンを Mapbox からオープンソースの MapLibre へ移行し、API トークン不要で完全な OSS スタックとして利用しやすくなった。
- React コンポーネントとして他の Web アプリに組み込む用途でも広く使われている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| ライセンス・開発経緯・技術構成 | GitHub (`keplergl/kepler.gl`)、Uber Engineering ブログ、Foursquare 公式発表 | GitHub リポジトリおよび公開技術記事 |
| 配信基盤情報 | `https://kepler.gl/` の HTTP 応答ヘッダー | 2026-11-16 の直接観測 |
