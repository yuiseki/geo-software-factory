# TerriaJS

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | terriajs 8.13.0 (npm 公開 2026-09-11)。TerriaMap は v0.4.8 (GitHub Release 2026-09-11) |
| リポジトリ | https://github.com/TerriaJS/terriajs (TerriaMap は同リポジトリの `apps/terriamap`。旧 https://github.com/TerriaJS/terriamap にも変更が反映される) |
| ドキュメント | https://docs.terria.io/ |
| ライセンス (LICENSE ファイルで確かめる) | Apache-2.0 (`LICENSE.md` の本文で確認) |
| 運営主体 | Terria Pty Ltd。公式サイトは CSIRO で開発され Terria Pty Ltd に譲渡されたと説明している (https://terria.com/) |

## 概要

TerriaJS は Web で 2D/3D の地理空間データを閲覧する「データカタログ型」の地図サイトを作るためのライブラリで、TerriaMap はそれを使った完成済みの Web サイトの雛形である (https://github.com/TerriaJS/terriajs)。数万件のレイヤーを持つカタログを扱え、ブラウザ側の JavaScript がほぼ全てを担うため静的サイトとしても配置できる、と README は説明している。オーストラリア政府系の National Map や Digital Earth Australia Map の基盤として使われている。

## 下にある描画ライブラリ

- 3D は CesiumJS (TerriaJS 用のフォーク `terriajs-cesium`)、2D は Leaflet を使い、Cesium が動かない環境では Leaflet に切り替わる (https://github.com/TerriaJS/terriajs)。
- `packages/terriajs/package.json` の依存には `terriajs-cesium`、`leaflet`、`protomaps-leaflet`、`@maplibre/maplibre-gl-style-spec` が入っている (https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/package.json)。MapLibre GL JS 本体は依存に無い。

## 最初から手に入るもの

- UI (レイヤー一覧、凡例、検索、時間スライダーなど): 入れ子のデータカタログ、レイヤーの重ね合わせ、時間次元を持つデータの時間コントロール (アニメーション再生とスライダー)、ドラッグ&ドロップでのファイル表示、UI の多言語化 (日本語訳あり) を README が挙げている (https://github.com/TerriaJS/terriajs)。検索プロバイダーの設定方法もドキュメントにある (https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/doc/customizing/search-providers.md)。
- データの読み込み (対応形式、データカタログ): ファイルは GeoJSON、KML、CSV (点と地域コードによる塗り分け)、GPX、GeoRSS、CZML、zip した Shapefile。サービスは WMS、WFS、WMTS、Esri MapServer / FeatureServer、Bing Maps、Carto、Cesium ion、OSM 形式のラスタータイル、Mapbox、SDMX、3D Tiles、GTFS、SOS。CSW、CKAN、Socrata、OpenDataSoft などからレイヤー群をまとめて取り込める (https://github.com/TerriaJS/terriajs)。地域コードによる塗り分けはオーストラリアの統計地域 (ASGS) などを内蔵している。
- 共有・埋め込み: 現在の地図の状態を URL で共有できる (https://github.com/TerriaJS/terriajs)。共有データを短い URL で保存するには terriajs-server の設定が要り、無い場合は JSON を URL に直接埋め込むため URL が非常に長くなる (https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/doc/deploying/deploying-terriamap.md)。iframe やポップアップからの制御、URL パラメータでの制御の手順がある (https://docs.terria.io/deploying/controlling-in-an-iframe-or-popup/ 、https://docs.terria.io/deploying/controlling-with-url-parameters/)。
- 開発せずに使えるか (ノーコード / 設定ファイル / コードが必要): 設定ファイルで足りる範囲が広い。公式 Docker イメージ `ghcr.io/terriajs/terriamap` に `config.json`、カタログ JSON、`serverconfig.json` をマウントすれば再ビルドなしで動かせる。それ以上の変更は clone してビルドする (https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/doc/getting-started.md)。

## 縛りになること

- カスタマイズの限界: 見た目の変更は `config.json`、SASS 変数、`UserInterface.jsx` でのメニューやボタンの追加が案内されている。v8 では `global.scss` で任意の CSS を上書きする方法が使えなくなっており、代替は Issue で議論中とされている (https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/doc/customizing/skinning.md)。UI の大きな作り替えには TerriaJS 本体の React コンポーネントに手を入れることになる (推測)。
- 必要なサーバー・インフラ: 静的ホスティングでも動くが、CORS 非対応のデータサーバーへのプロキシ、共有 URL の保存、SPA ルーティングには Node.js 製の terriajs-server が要る。Node.js 22 以上が必要で、本番は Docker か Kubernetes を推奨している (https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/doc/deploying/deploying-terriamap.md)。

## ライセンスと費用

- OSS 版のライセンス: Apache-2.0 (https://github.com/TerriaJS/terriajs/blob/main/LICENSE.md)。3D 表示で Cesium ion のアセットを使う場合はその利用条件が別にかかる。
- 提供元のホスティング版・有償版と料金: Terria Pty Ltd がホスティング版 (app.terria.io へのログイン導線あり) を提供している。料金ページに金額は無く、展開する地図やデジタルツインの数、接続するデータソース、サポート段階で決まる見積もり制で、ユーザー数 (シート) では課金しないと書かれている。支払いは月次クレジットカードか年次請求書、オーストラリア政府向けには BuyICT パネル経由がある (https://terria.com/pricing、2026-11-10 確認)。

## 実例

- National Map: https://nationalmap.gov.au
- NSW Spatial Digital Twin: https://nsw.digitaltwin.terria.io
- Digital Earth Australia Map: https://maps.dea.ga.gov.au
- Digital Earth Africa Map: https://maps.digitalearth.africa
- GeoGLAM RAPP: https://map.geo-rapp.org/
- Data61 以外の利用例として AURIN Map (http://map.aurin.org.au/)、GeoPlatform Mapping (https://terriamap.geoplatform.gov/) などを README が挙げている (https://github.com/TerriaJS/terriajs)。

## 開発の活発さ

- 直近 1 年のリリース数: terriajs は GitHub Releases を使っておらず、npm に 2025-11-10 以降 9 件公開 (8.11.1 から 8.13.0、うち 1 件は alpha)。TerriaMap は GitHub Releases に同期間 5 件 (v0.4.4 から v0.4.8)。
- 最終コミット日: 2026-11-09 (TerriaJS/terriajs の main)。TerriaMap は 2026-06-15 に terriajs リポジトリへ統合すると告知されている (https://github.com/TerriaJS/terriamap)。

## 向いている場面

- 多数の公開データセット (WMS や CKAN など) を 1 つのカタログにまとめ、利用者が自由に重ねて見るポータルを作りたいとき。
- 2D と 3D (3D Tiles を含む) を同じ画面で扱いたいとき。
- 設定ファイル中心で、大きな開発をせずにデータポータルを立ち上げたいとき。

## 向いていない場面

- 独自の UI や業務フローを持つアプリを作りたいとき。UI は TerriaJS の構成が前提で、作り替えの自由度は低い。
- MapLibre GL JS のベクトルタイルスタイルを主役にした地図を作りたいとき。2D 描画は Leaflet である。
- 地域コードによる塗り分けなど、オーストラリア向けの内蔵機能をそのまま日本で使いたいとき。日本の境界データは自分で用意する必要がある (推測)。

## 出典

- https://github.com/TerriaJS/terriajs
- https://github.com/TerriaJS/terriajs/blob/main/LICENSE.md
- https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/package.json
- https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/doc/getting-started.md
- https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/doc/customizing/skinning.md
- https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/doc/customizing/search-providers.md
- https://github.com/TerriaJS/terriajs/blob/main/packages/terriajs/doc/deploying/deploying-terriamap.md
- https://github.com/TerriaJS/terriamap
- https://github.com/TerriaJS/terriamap/releases
- https://www.npmjs.com/package/terriajs
- https://docs.terria.io/
- https://docs.terria.io/deploying/controlling-in-an-iframe-or-popup/
- https://docs.terria.io/deploying/controlling-with-url-parameters/
- https://terria.com/
- https://terria.com/pricing

## 未確認のこと

- ホスティング版の具体的な金額: 料金ページが見積もり制で金額を公開していないため。
- ホスティング版の機能範囲 (OSS 版との差): 公式サイトに比較表が無く、ログインしないと確かめられないため。
- 実例に挙げたサイトが確かめた日に TerriaJS の最新系で動いているか: 各サイトの版を個別に調べていないため。
