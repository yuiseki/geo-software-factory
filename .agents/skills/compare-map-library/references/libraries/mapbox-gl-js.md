# Mapbox GL JS (Mapbox SDK)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | v3.34.2 (2026-11-03、GitHub Releases の公開日時、JST)。npm の `next` タグは 3.35.0-rc.1 ([GitHub Releases](https://github.com/mapbox/mapbox-gl-js/releases)、[npm](https://www.npmjs.com/package/mapbox-gl)) |
| リポジトリ | https://github.com/mapbox/mapbox-gl-js (ソースは公開されているが OSS ライセンスではない) |
| ドキュメント | https://docs.mapbox.com/mapbox-gl-js/ |
| ライセンス (LICENSE ファイルで確かめる) | v2.0 以降は Mapbox 独自ライセンス (Mapbox Web SDK ライセンス。Mapbox TOS に従い、有効な Mapbox アカウントを持つ開発者が Mapbox 製品と組み合わせて使う場合に限り利用・改変を許す)。v1.13 以前は BSD-3-Clause ([LICENSE.txt](https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt))。npm の license 欄は `SEE LICENSE IN LICENSE.txt` |
| 運営主体・ガバナンス | Mapbox, Inc. が単独で開発・配布する。財団への移管やオープンガバナンスはない (LICENSE.txt の著作権表示は Mapbox, Inc.) |

## 概要

ベクトルタイルとスタイル定義をブラウザ側で組み合わせて描画する、クライアントサイドの地図ライブラリである ([公式ガイド](https://docs.mapbox.com/mapbox-gl-js/guides/))。v3 では Mapbox Standard スタイル、3D ライティング、建物の影などを扱えるようになった ([CHANGELOG 3.0.0](https://github.com/mapbox/mapbox-gl-js/blob/main/CHANGELOG.md))。v2.0.0 (2020-12) で BSD-3-Clause から Mapbox 独自ライセンスへ移り、地図の初期化ごとに課金される方式になった。v1 系の BSD 版は MapLibre GL JS のフォーク元である。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): WebGL。v3.0.0 で WebGL 1 対応をやめ、WebGL 2 が必須になった ([CHANGELOG 3.0.0](https://github.com/mapbox/mapbox-gl-js/blob/main/CHANGELOG.md))。WebGPU への言及は公式ガイドに見当たらない
- 2D / 2.5D (傾き・回転) / 3D: 2D、傾き・回転、3D 地形、建物の押し出し、glTF モデルに対応する。v2.0.0 で最大ピッチが 60° から 85° に上がり、3D 地形と空 (sky) レイヤー、Free Camera API が入った ([CHANGELOG 2.0.0](https://github.com/mapbox/mapbox-gl-js/blob/main/CHANGELOG.md))
- 地球儀表示: 対応。`projection: 'globe'` で地球儀になり、v12 系のスタイルでは globe が既定 ([Projections ガイド](https://docs.mapbox.com/mapbox-gl-js/guides/projections/))
- 対応する投影法: globe、mercator (既定)、equalEarth、naturalEarth、winkelTripel、albers、lambertConformalConic、equirectangular。投影法の切り替えは v2.6 で入った。3D 地形、Free Camera API、霧 (fog)、`CustomLayerInterface` は globe と mercator でしか動かない ([Projections ガイド](https://docs.mapbox.com/mapbox-gl-js/guides/projections/))

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | `raster` ソースに `tiles` (URL テンプレート) か TileJSON の `url` を渡す。`scheme` で xyz / tms を選べる ([Sources](https://docs.mapbox.com/style-spec/reference/sources/)) |
| ベクトルタイル (MVT / PMTiles / MLT) | MVT は対応、PMTiles と MLT は未確認 | `vector` ソースは Mapbox Vector Tile 仕様に従うタイルを読む。スタイル仕様のソース一覧に PMTiles と MLT の記述はない ([Sources](https://docs.mapbox.com/style-spec/reference/sources/)) |
| スタイル仕様 (MapLibre/Mapbox Style 等) | Mapbox Style Specification | v3 の Standard スタイルや import など Mapbox 独自の拡張があり、MapLibre Style Spec とは差がある (差分の網羅は未確認) |
| GeoJSON | 対応 | `geojson` ソース。インラインか URL。クラスタリングあり ([Sources](https://docs.mapbox.com/style-spec/reference/sources/)) |
| 3D Tiles / glTF | glTF は対応、3D Tiles は未確認 | `model` ソースで glTF モデルを置ける。`tiles` を使うには `batched-model` ソースが要る。OGC 3D Tiles の読み込みはスタイル仕様のソース一覧にない ([Sources](https://docs.mapbox.com/style-spec/reference/sources/)) |
| 地形 (標高タイル) | 対応 | `raster-dem` ソース。`encoding` は `mapbox` (既定) と `terrarium`。ドキュメントは Mapbox Terrain-DEM を前提に書かれている ([Sources](https://docs.mapbox.com/style-spec/reference/sources/)) |
| WMS / WMTS | WMS は条件つきで対応、WMTS は未確認 | EPSG:3857 に対応する WMS なら `raster` ソースの `tiles` URL に `{bbox-epsg-3857}` を入れて使える ([Sources](https://docs.mapbox.com/style-spec/reference/sources/))。WMTS は XYZ 形式の URL で引ける場合に `raster` ソースとして使える (推測) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: v2 以降は、ライブラリそのものが「Mapbox 製品と組み合わせて使う場合に限り」許諾されている ([LICENSE.txt](https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt))。自前タイルや他社タイルを表示するだけの用途でも、Mapbox アカウントと課金 (地図の初期化ごとのマップロード) から外れることはできない。課金・計測・データ収集に関わる部分のコードを改変することも許されていない (同 LICENSE.txt)。他社タイルサービス側の規約による制限は、各サービスの規約による
- API キー・アカウントの要否: 必須。アクセストークンが地図を Mapbox アカウントに結びつける ([公式ガイド](https://docs.mapbox.com/mapbox-gl-js/guides/))。アカウントが失効するとライセンスも自動的に終わる ([LICENSE.txt](https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt))

## ライセンスと費用

- ライセンス: v2.0 以降は Mapbox TOS と Mapbox Product Terms に従う独自ライセンス (オープンソースではない)。SDK は匿名化した位置情報と利用データを Mapbox に送る ([LICENSE.txt](https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt))
- 利用料 (無料 / 従量 / 有料の機能): Web はマップロード課金。`Map` オブジェクトの初期化 1 回が 1 マップロードで、その後のズーム・パン・スタイル切り替えは追加課金されない。1 セッションは最長 12 時間 ([Web の課金ガイド](https://docs.mapbox.com/mapbox-gl-js/guides/pricing/))。月 50,000 回まで無料、50,001〜100,000 回は 1,000 回あたり 5.00 ドル、100,001〜200,000 回は 4.00 ドル、200,001〜1,000,000 回は 3.00 ドル、1,000,001〜5,000,000 回は 2.50 ドル、それ以上は営業に問い合わせ。マップロードには Vector Tiles API と Raster Tiles API のリクエストが無制限に含まれる ([料金ページ](https://www.mapbox.com/pricing)、2026-11-10 確認。料金ページは「$」表記で通貨コードを明示していないため、米ドルとみなしたのは推測)。Geocoding や Directions などのプラグインが呼ぶ API は別に課金される ([Plugins](https://docs.mapbox.com/mapbox-gl-js/plugins/))
- 版によるライセンスの変化: v1.13 以前は BSD-3-Clause。v2.0.0 (2020-12-08) で独自ライセンスへ移り、「この版に上げると Mapbox TOS に同意したことになる」と CHANGELOG に明記された ([CHANGELOG 2.0.0](https://github.com/mapbox/mapbox-gl-js/blob/main/CHANGELOG.md))。課金の数え方も変わり、v1 は「Map の初期化と Mapbox がホストするタイルの要求」の組で 1 マップロード、v2 以降は初期化だけで 1 マップロードになる ([Web の課金ガイド](https://docs.mapbox.com/mapbox-gl-js/guides/pricing/))。BSD 版の最終は v1.13.3 (2023-01-19) で、npm の `old` タグに残っている ([npm](https://www.npmjs.com/package/mapbox-gl))。BSD 版 v1 をフォークしたのが MapLibre GL JS である

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): v3.34.2 で 520,474 バイト (約 508 KiB)、v1.13.3 で 195,402 バイト ([bundlephobia mapbox-gl@3.34.2](https://bundlephobia.com/package/mapbox-gl@3.34.2)、[bundlephobia mapbox-gl@1.13.3](https://bundlephobia.com/package/mapbox-gl@1.13.3))
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 上限の数値は公式に示されていない。大きな GeoJSON のガイドは「50 万点を超える」データで追加の工夫を検討するよう書き、座標を小数 6 桁までに丸める、`maxzoom` を下げる、クラスタリング、サーバー側でのタイル化を勧める ([Working with large GeoJSON sources](https://docs.mapbox.com/help/troubleshooting/working-with-large-geojson-data/))
- 低性能端末・モバイルブラウザでの注意: v3 は WebGL 2 必須なので、WebGL 2 を使えない環境では動かない ([CHANGELOG 3.0.0](https://github.com/mapbox/mapbox-gl-js/blob/main/CHANGELOG.md))。GeoJSON を複数ソースに分けてもモバイルブラウザではあまり速くならないと公式ガイドが書いている ([Working with large GeoJSON sources](https://docs.mapbox.com/help/troubleshooting/working-with-large-geojson-data/))

## エコシステム

- 主なプラグイン・拡張: mapbox-gl-geocoder、mapbox-gl-draw、mapbox-gl-directions、mapbox-gl-compare、mapbox-gl-language、mapbox-gl-traffic、mapbox-gl-sync-move など ([Plugins](https://docs.mapbox.com/mapbox-gl-js/plugins/))。deck.gl は `MapboxOverlay` で重ねられ、interleaved 描画は mapbox-gl v2.13 以降で使える ([deck.gl Using with Mapbox](https://deck.gl/docs/developer-guide/base-maps/using-with-mapbox))
- React / Vue などのラッパー: 公式の雛形生成ツール create-mapbox-web-app が Vanilla JS、React、Angular、Vue、Svelte に対応する。Angular 向け ngx-mapbox-gl、Ember 向け ember-mapbox-gl が公式ページに載っている ([Plugins](https://docs.mapbox.com/mapbox-gl-js/plugins/))。React 向けには vis.gl の react-map-gl 8.1.3 が `react-map-gl/mapbox` で Mapbox GL JS に対応する ([npm react-map-gl](https://www.npmjs.com/package/react-map-gl))
- TypeScript の型: 同梱 (`dist/mapbox-gl.d.ts`)。v3.5.0 で Flow から TypeScript に移り、コミュニティの `@types/mapbox-gl` は外すよう案内された ([CHANGELOG](https://github.com/mapbox/mapbox-gl-js/blob/main/CHANGELOG.md))
- ネイティブ版・兄弟プロジェクト: Mapbox Maps SDK for iOS / Android。React Native 向けに rnmapbox/maps がある ([Plugins](https://docs.mapbox.com/mapbox-gl-js/plugins/))。v1 の BSD 版から MapLibre GL JS が分岐している
- 日本語の情報 (公式翻訳、国内コミュニティ): docs.mapbox.com に日本語版のガイドと API リファレンスがあるが、本文の多くは英語のまま ([日本語ガイド](https://docs.mapbox.com/mapbox-gl-js/ja/guides/)、[日本語 API](https://docs.mapbox.com/mapbox-gl-js/ja/api/))。国内コミュニティは未確認

## 開発の活発さ

- 直近 1 年のリリース数: 24 (2025-11-10〜2026-11-10 に GitHub Releases で公開された、プレリリースを除く版の数。`gh api repos/mapbox/mapbox-gl-js/releases` で数えた)。ほぼ 2 週間ごとにマイナー版が出ている
- 最終コミット日: 2026-11-09 (main ブランチ、JST)
- 近年の大きな破壊的変更: v3.0.0 (2023-11-29) で WebGL 1 対応をやめた。v3.5.0 で TypeScript へ移り `@types/mapbox-gl` と非互換になった。v3.21.0 で `mapbox-gl-unminified.js` を削除、v3.25.0 で ESM 入口を名前付きエクスポートに変え `mapboxgl.accessToken` を `Map` の `accessToken` オプションに置き換え、v3.33.0 で `setRTLTextPlugin` を削除した ([CHANGELOG](https://github.com/mapbox/mapbox-gl-js/blob/main/CHANGELOG.md))。マイナー版でも破壊的変更が入る

## 向いている場面

- Mapbox のスタイル、タイル、Geocoding、Directions などをまとめて使い、地図データの整備を Mapbox に任せたい場合
- Standard スタイル、3D ライティング、多数の投影法など、MapLibre にない Mapbox 独自の機能が要件にある場合
- 月 5 万マップロード以下に収まる小規模な Web アプリ

## 向いていない場面

- 自前のタイルや他社のタイルだけを表示したい場合 (v2 以降はそれでも Mapbox アカウントとマップロード課金が要る)。この用途なら BSD 版から分岐した MapLibre GL JS が候補になる
- ライブラリに OSS ライセンスを求める場合、ソースを改変して再配布したい場合
- WebGL 2 を使えない古い端末を対象に含める場合
- マップロード数が大きく、課金額を読みにくいサービス

## 出典

- https://github.com/mapbox/mapbox-gl-js/releases
- https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt
- https://github.com/mapbox/mapbox-gl-js/blob/main/CHANGELOG.md
- https://www.npmjs.com/package/mapbox-gl
- https://docs.mapbox.com/mapbox-gl-js/guides/
- https://docs.mapbox.com/mapbox-gl-js/guides/projections/
- https://docs.mapbox.com/mapbox-gl-js/guides/pricing/
- https://docs.mapbox.com/mapbox-gl-js/plugins/
- https://docs.mapbox.com/style-spec/reference/sources/
- https://docs.mapbox.com/help/troubleshooting/working-with-large-geojson-data/
- https://docs.mapbox.com/mapbox-gl-js/ja/guides/
- https://docs.mapbox.com/mapbox-gl-js/ja/api/
- https://www.mapbox.com/pricing
- https://bundlephobia.com/package/mapbox-gl@3.34.2
- https://bundlephobia.com/package/mapbox-gl@1.13.3
- https://www.npmjs.com/package/react-map-gl
- https://deck.gl/docs/developer-guide/base-maps/using-with-mapbox

## 未確認のこと

- PMTiles と MLT への対応: スタイル仕様のソース一覧と公式ガイドに記述がなく、対応の有無を確かめられなかった
- OGC 3D Tiles の読み込み: ソース一覧に該当する型がなく、`batched-model` との関係も公式文書から読み取れなかった
- WMTS: 公式文書に記述がない
- Mapbox Style Spec と MapLibre Style Spec の差分の網羅: 今回の調査範囲外
- 料金の通貨: 料金ページは「$」表記のみで通貨コードを書いていない
- Mapbox Product Terms の Web SDK に関する条項: 規約本文は PDF で配布されており、今回は読めなかった。上の制約は LICENSE.txt の文言に基づく
- 国内コミュニティ: 公開されている活動を確かめられなかった
