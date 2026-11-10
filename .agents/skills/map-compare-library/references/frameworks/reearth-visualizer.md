# Re:Earth Visualizer

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 正式版 1.0 は未リリース。最新は v1.0.0-beta.16.30 (2026-11-04、GitHub 上は prerelease 指定なし)。beta が付かない最後の版は v0.20.0 (2024-01-24) |
| リポジトリ | https://github.com/reearth/reearth-visualizer (旧名 reearth/reearth からリダイレクト) |
| ドキュメント | https://docs.reearth.io/ja/ (Visualizer の利用者向けページは「準備中」。プラグイン API は https://docs.reearth.io/ja/developer/plugin/api-reference/) |
| ライセンス (LICENSE ファイルで確かめる) | Apache-2.0 (LICENSE の本文で確認) |
| 運営主体 | 株式会社ユーカリヤ (Eukarya Inc.)。GitHub org reearth の説明欄とドキュメントサイトのフッター「© 2026 Eukarya Inc.」で確認 |

## 概要

Re:Earth Visualizer は、ブラウザ上の編集画面でデータを 3D/2D の地図に配置し、見た目の調整、ストーリーテリング、プラグインによる拡張を行って、URL で公開する WebGIS である (https://reearth.io/product/visualizer)。フロントエンドの React と、Go 製の GraphQL サーバー、MongoDB で構成され、セルフホストもできる (https://github.com/reearth/reearth-visualizer)。提供元はホスティング版を Re:Earth CMS や Re:Earth Flow と同じ料金体系で提供している。

## 下にある描画ライブラリ

- CesiumJS。README は描画エンジンとして Cesium を使うと書いている。`web/package.json` は cesium 1.145.0 に依存する (https://github.com/reearth/reearth-visualizer)。
- 地図エンジンへの依存は `@reearth/core` (https://github.com/reearth/core) で抽象化されている。README は「現在は Cesium を使っているが、将来は別のエンジンにも対応する計画がある」と書いており、確かめた日の時点で Cesium 以外の実装は確認できない。

## 最初から手に入るもの

- UI (レイヤー一覧、凡例、検索、時間スライダーなど): 編集画面 (レイヤー、条件付きスタイル、図形描画、カメラワーク)、ページ送り形式のストーリーテリング、ウィジェットとブロックの配置 (https://github.com/reearth/reearth-visualizer 、https://reearth.io/product/visualizer)。凡例や検索など個別の UI 部品の有無は、公式のプラグインや配置できるウィジェットに依存する。
- データの読み込み (対応形式、データカタログ): 製品ページは 3D Tiles、GeoJSON、CZML、Shapefile、CSV、KML、glTF、GLB、各種画像を挙げる (https://reearth.io/product/visualizer)。地形には Cesium ion のアセットを指定できる (https://docs.reearth.io/llms-full.txt)。データカタログ機能は Visualizer 単体には無く、PLATEAU VIEW では Re:Earth CMS 由来の CMS がその役を担っている (下の「実例」)。
- 共有・埋め込み: プロジェクトを公開し、配信 URL、埋め込み、カスタム URL で共有できる (https://github.com/reearth/reearth-visualizer)。ホスティング版のカスタムドメインは有料プランのみ (Starter 1 件、Business 3 件、Advanced 10 件) (https://reearth.io/pricing)。
- 開発せずに使えるか (ノーコード / 設定ファイル / コードが必要): 地図の作成と公開はノーコードでできる。機能の追加は JavaScript のプラグインで行う。プラグインのロジックは WebAssembly 側で動き、UI は iframe に描画される (https://docs.reearth.io/llms-full.txt)。

## 縛りになること

- カスタマイズの限界: 表示側の拡張はプラグイン API が提供する範囲に限られる。API の外の変更 (編集画面や描画エンジンそのもの) はソースのフォークになり、PLATEAU VIEW 5.0 もエディタ部分をリポジトリ内に丸ごと持っている (下の「実例」)。描画エンジンは Cesium のみである。
- 必要なサーバー・インフラ: セルフホストでは Go の API サーバー、MongoDB、オブジェクトストレージ (GCS。開発用は fake-gcs-server)、認可用の Cerbos、アカウント用 API、OpenID Connect の認証基盤が要る (https://github.com/reearth/reearth-visualizer の README と docker-compose.yml)。開発時の手順は Cesium ion のアクセストークンを求めている。ホスティング版を使えば自前のサーバーは不要。

## ライセンスと費用

- OSS 版のライセンス: Apache-2.0 (https://github.com/reearth/reearth-visualizer/blob/main/LICENSE)。Cesium ion を使う場合はその料金と規約が別にかかる。
- 提供元のホスティング版・有償版と料金: 2026-11-10 に https://reearth.io/pricing で確認した税込の日本円 (シート単位、閲覧者はシートに数えない)。

| プラン | 月払い | 年払い | 主な違い |
|---|---|---|---|
| Open & Public | 無料 | 無料 | 全プロジェクトがオープンデータとして公開される。非公開プロジェクトとカスタムドメインは使えない |
| Starter | ¥1,650 / シート / 月 | ¥19,800 / シート / 年 | 非公開プロジェクト可。CMS の非公開データ転送量 100GB、カスタムドメイン 1 件 |
| Business | ¥6,600 / シート / 月 | ¥66,000 / シート / 年 (月あたり ¥5,500) | 転送量 250GB、カスタムドメイン 3 件 |
| Advanced | ¥13,200 / シート / 月 | ¥132,000 / シート / 年 (月あたり ¥11,000) | 転送量 500GB、カスタムドメイン 10 件 |
| Enterprise | 個別見積もり | 個別見積もり | 各上限を個別に設定 |

有料プランのトライアルは無いとされている。非公開データの月間転送量の上限に達すると、その月は非公開データの追加アップロードや配信ができなくなる (https://reearth.io/pricing)。

## 実例

- PLATEAU VIEW 5.0 (国土交通省 Project PLATEAU、https://plateauview.mlit.go.jp/ 、ソースは https://github.com/Project-PLATEAU/PLATEAU-VIEW-5.0、Apache-2.0)。リポジトリは PLATEAU CMS、PLATEAU Editor、PLATEAU Flow、PLATEAU VIEW などで構成される。Editor の README は Re:Earth Visualizer の README とほぼ同じ内容で、Visualizer を取り込んだものと読める。ビューワーの機能は `extension` ディレクトリの「PLATEAU VIEW 3.0 extension for Re:Earth」(Re:Earth のプラグイン) として実装されている。CMS は Re:Earth CMS を元にしたと README に書かれ、`flow` は Re:Earth Flow である。つまり PLATEAU VIEW 5.0 は Re:Earth の各製品をフォークしてリポジトリ内に持ち、その上に PLATEAU 用のプラグインを載せた構成である。このリポジトリの最終コミットは 2026-03-24 で、上流の reearth-visualizer (2026-11-09) より古い。

## 開発の活発さ

- 直近 1 年のリリース数: 57 件 (2025-11-10 以降の GitHub Releases。v1.0.0-beta.* が 56 件、nightly が 1 件)。おおむね週 1 回のペースで beta を出している。
- 最終コミット日: 2026-11-09 (main)。

## 向いている場面

- 3D Tiles や CZML など 3D データを、開発者でない担当者が地図に並べてストーリー付きで公開したいとき。
- サーバー運用をせずに、ホスティング版で公開まで済ませたいとき。オープンデータとして公開してよいなら無料プランで足りる。
- PLATEAU のデータや PLATEAU VIEW の構成を土台にした案件。

## 向いていない場面

- 2D のベクトルタイル地図 (MapLibre GL JS 系のスタイル) を主役にしたいとき。描画エンジンは Cesium のみである。
- 安定版の API を前提に長く保守したいとき。確かめた日の時点で 1.0 正式版が出ておらず、beta が頻繁に更新されている。
- セルフホストを小さな構成で済ませたいとき。MongoDB、オブジェクトストレージ、認証基盤などが必要になる。
- 非公開データの転送量が月数百 GB を超える見込みがあるとき。ホスティング版は上限到達で配信が止まる。

## 出典

- https://github.com/reearth/reearth-visualizer
- https://github.com/reearth/reearth-visualizer/blob/main/LICENSE
- https://github.com/reearth/reearth-visualizer/blob/main/docker-compose.yml
- https://github.com/reearth/reearth-visualizer/releases
- https://github.com/reearth/core
- https://github.com/reearth
- https://reearth.io/product/visualizer
- https://reearth.io/pricing
- https://docs.reearth.io/ja/
- https://docs.reearth.io/ja/developer/plugin/api-reference/
- https://docs.reearth.io/llms-full.txt
- https://github.com/Project-PLATEAU/PLATEAU-VIEW-5.0
- https://plateauview.mlit.go.jp/

## 未確認のこと

- 凡例、住所検索、時間スライダーが Visualizer 単体の標準機能か、プラグインや PLATEAU 側の実装か: Visualizer の利用者向けドキュメントが「準備中」で、機能一覧を一次情報で確かめられなかったため。
- 2D 表示の実装 (Cesium の 2D モードか別実装か): 製品ページに「3Dまたは2D」とあるが、仕組みを説明した文書が見つからなかったため。
- PLATEAU VIEW 5.0 が取り込んだ Visualizer の版と、上流との差分の大きさ: リポジトリにサブモジュールや版の記録が無く、コードの比較までは行っていないため。
- https://plateauview.mlit.go.jp/ で確かめた日に動いているのが 5.0 系か: サイトの版表示を確かめていないため。
