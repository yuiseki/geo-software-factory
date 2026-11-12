# Google Maps JavaScript API (Google Maps SDK)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | ウィークリーチャネル 3.66 (最新のリリースノートは 3.66.13d、2026-11-04)。クォータリーチャネルは 3.65。四半期版は 2 月・5 月・8 月・11 月の中旬に出て、2026 年 11 月中旬にウィークリーが 3.67 に上がる予定 ([バージョン](https://developers.google.com/maps/documentation/javascript/versions)、[リリースノート](https://developers.google.com/maps/documentation/javascript/releases)) |
| リポジトリ | なし (本体は非公開。Google のサーバーからスクリプトとして読み込む) |
| ドキュメント | https://developers.google.com/maps/documentation/javascript |
| ライセンス (LICENSE ファイルで確かめる) | 対象外 (LICENSE ファイルを持つ配布物ではない)。Google Maps Platform 利用規約に基づくプロプライエタリなサービス ([利用規約](https://cloud.google.com/maps-platform/terms)) |
| 運営主体・ガバナンス | Google が単独で開発・運用する |

## 概要

Google の地図、航空写真、ストリートビューを Web ページに埋め込み、マーカー、図形、GeoJSON などを重ねるための JavaScript API である。2D の `Map` に加え、`maps3d` ライブラリの `Map3DElement` (`<gmp-map-3d>`) でフォトリアリスティックな 3D 地図を表示できる ([3D Maps](https://developers.google.com/maps/documentation/javascript/3d-maps-overview))。ベクターマップ、Advanced Markers、データ駆動スタイルなど主な新機能はマップ ID の設定を前提にしている。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): ラスターマップはサーバーで描いた画像タイルを並べる。ベクターマップはタイルをクライアント側で WebGL で描く ([ベクターマップ](https://developers.google.com/maps/documentation/javascript/vector-map))。WebGPU はリリースノートに言及がない ([リリースノート](https://developers.google.com/maps/documentation/javascript/releases))
- 2D / 2.5D (傾き・回転) / 3D: ベクターマップで傾き (tilt) と回転 (heading) を扱える。傾きの上限はズーム 10 以下で 30°、ズーム 15.5 以上で 67.5° ([ベクターマップ](https://developers.google.com/maps/documentation/javascript/vector-map))。3D は `Map3DElement` で、フォトリアリスティックな建物メッシュは一部の都市圏だけにあり、他の地域は 3D 地形に 2D の画像を貼る表示になる ([3D Maps](https://developers.google.com/maps/documentation/javascript/3d-maps-overview))。3D Maps はベータチャネル (3.60.10、2025-04-24) を経て、3.62.11d (2025-10-23) でウィークリーチャネルに入った ([リリースノート](https://developers.google.com/maps/documentation/javascript/releases))
- 地球儀表示: 未確認。2D の `Map` はメルカトル図法を使う ([座標](https://developers.google.com/maps/documentation/javascript/coordinates))。3D Maps の公式概要とリリースノートに地球儀表示の記述はない
- 対応する投影法: メルカトル図法 ([座標](https://developers.google.com/maps/documentation/javascript/coordinates))。独自地図タイプでは `Projection` インターフェースを実装して別の投影法 (例: ガル・ピーターズ) を使えるが、投影法は直交座標系 (rectilinear) である前提 ([地図タイプ](https://developers.google.com/maps/documentation/javascript/maptypes))

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | `ImageMapType` に `getTileUrl` と `tileSize` を渡し、ベース地図か `overlayMapTypes` の重ねる層として表示する ([地図タイプ](https://developers.google.com/maps/documentation/javascript/maptypes))。Google の地図の上に自前のラスタを重ねる使い方になる |
| ベクトルタイル (MVT / PMTiles / MLT) | 非対応 | 任意の MVT / PMTiles / MLT を読む API は公式ドキュメントに見当たらない。代わりにデータセット (GeoJSON / CSV / KML をアップロード) のデータ駆動スタイルがあり、ベクターマップとマップ ID が必須 ([データセットのデータ駆動スタイル](https://developers.google.com/maps/documentation/javascript/dds-datasets/overview)) |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 非対応 | 地図の見た目はクラウドベースのマップスタイル (マップ ID に紐づく) で設定する。MapLibre / Mapbox Style Spec は読めない。旧来のクラウドスタイルは 2025-03-25 に自動移行された ([非推奨一覧](https://developers.google.com/maps/deprecations)) |
| GeoJSON | 対応 | Data レイヤーの `loadGeoJson()` (URL) と `addGeoJson()` (オブジェクト) ([Data レイヤー](https://developers.google.com/maps/documentation/javascript/datalayer)) |
| 3D Tiles / glTF | glTF は対応、3D Tiles は API 内では非対応 | 3D Maps の `Model3DElement` が glTF (PBR の基本プロパティのみ、拡張なし) を置ける ([3D Maps のモデル](https://developers.google.com/maps/documentation/javascript/3d/models))。Google の Photorealistic 3D Tiles は Map Tiles API で別に提供され、deck.gl などの外部ライブラリで読む ([料金](https://developers.google.com/maps/billing-and-pricing/pricing)、[deck.gl Tile3DLayer](https://deck.gl/docs/api-reference/geo-layers/tile-3d-layer)) |
| 地形 (標高タイル) | 自前データは非対応 | 3D Maps は Google の 3D 地形を表示する ([3D Maps](https://developers.google.com/maps/documentation/javascript/3d-maps-overview))。利用者の標高タイルを読み込む API は見当たらない |
| WMS / WMTS | 組み込みはなし | 公式ドキュメントに WMS / WMTS の記述はない。`ImageMapType` の `getTileUrl` でタイル座標から要求 URL を組み立てれば表示できる (推測) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: Google Maps Platform 利用規約 3.2.3(e)「No Use With Non-Google Maps」で、Google Maps Core Services を Google 以外の地図と一緒に、または近くで使うことを禁じている。例として、Places の内容を Google 以外の地図に表示する、ストリートビューと Google 以外の地図を同じ画面に出す、Google の地図を Google 以外の地図にリンクする、が挙がっている ([利用規約](https://cloud.google.com/maps-platform/terms)、2026-08-26 改定版)。Google の地図の上に自前のラスタやデータを重ねることは `ImageMapType` などの公式機能で想定されている
- API キー・アカウントの要否: Google Maps Platform の API キーが必須 ([3D Maps](https://developers.google.com/maps/documentation/javascript/3d-maps-overview))。Advanced Markers、ベクターマップの WebGL Overlay View、データ駆動スタイルにはマップ ID も要る (デモ用の `DEMO_MAP_ID` あり) ([Advanced Markers](https://developers.google.com/maps/documentation/javascript/advanced-markers/overview)、[WebGL Overlay View](https://developers.google.com/maps/documentation/javascript/webgl/webgl-overlay-view))

## ライセンスと費用

- ライセンス: Google Maps Platform 利用規約に基づくプロプライエタリなサービス ([利用規約](https://cloud.google.com/maps-platform/terms))
- 利用料 (無料 / 従量 / 有料の機能): 地図の読み込み (map load) が Dynamic Maps SKU として課金される ([使用量と課金](https://developers.google.com/maps/documentation/javascript/usage-and-billing))。2026-11-10 確認の単価 (米ドル、1,000 回あたりの最初の有料段): Dynamic Maps は月 10,000 回まで無料で 7.00 ドル、Dynamic Street View は月 5,000 回まで無料で 14.00 ドル、Immersive Maps は月 5,000 回まで無料で 7.00 ドル、Static Maps は月 10,000 回まで無料で 2.00 ドル。Map Tiles API は 2D タイルが月 100,000 回まで無料で 0.60 ドル、Photorealistic 3D Tiles が月 1,000 回まで無料で 6.00 ドル ([料金](https://developers.google.com/maps/billing-and-pricing/pricing))。Places ライブラリなどは別料金 ([使用量と課金](https://developers.google.com/maps/documentation/javascript/usage-and-billing))。Immersive Maps SKU が 3D Maps (`Map3DElement`) に当たるかは未確認
- 版によるライセンスの変化: なし (版によって規約が変わる仕組みではない)。ただし機能の廃止は続いている。`google.maps.Marker` は 2024-02 (v3.56) に非推奨となり、廃止日は未定 (廃止の 12 か月前までに告知)。Heatmap レイヤーと Drawing ライブラリは 2026-05 に使えなくなり、KmlLayer も使えなくなった ([非推奨一覧](https://developers.google.com/maps/deprecations))

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 対象外 (npm パッケージではなく、Google のサーバーから実行時に読み込むため)。読み込み補助の `@googlemaps/js-api-loader` は npm にある (2.1.3) ([npm](https://www.npmjs.com/package/@googlemaps/js-api-loader))
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 未確認。Data レイヤーと Advanced Markers の公式ページに件数の目安はない ([Data レイヤー](https://developers.google.com/maps/documentation/javascript/datalayer)、[Advanced Markers](https://developers.google.com/maps/documentation/javascript/advanced-markers/overview))。割り当て (課金とは別) は 1 プロジェクトあたり毎分 30,000 マップロード、1 IP あたり毎分 300 ([使用量と課金](https://developers.google.com/maps/documentation/javascript/usage-and-billing))
- 低性能端末・モバイルブラウザでの注意: ベクターマップは WebGL に依存する ([ベクターマップ](https://developers.google.com/maps/documentation/javascript/vector-map))。deck.gl の文書によれば、ベクターマップを使えない端末ではラスターマップに切り替わることがある ([deck.gl GoogleMapsOverlay](https://deck.gl/docs/api-reference/google-maps/google-maps-overlay))。フラクショナルズーム (ベクターでは既定で有効) では `zoom_changed` が頻繁に発火するので、処理を間引くよう公式が勧めている ([ベクターマップ](https://developers.google.com/maps/documentation/javascript/vector-map))

## エコシステム

- 主なプラグイン・拡張: deck.gl の `GoogleMapsOverlay` (ベクターマップでは WebGL2 コンテキストを共有して interleaved 描画、ラスターでは別キャンバスを重ねる) ([deck.gl GoogleMapsOverlay](https://deck.gl/docs/api-reference/google-maps/google-maps-overlay))。WebGL Overlay View で Three.js などの描画を重ねられる ([WebGL Overlay View](https://developers.google.com/maps/documentation/javascript/webgl/webgl-overlay-view))。廃止された Heatmap の代替に deck.gl の HeatmapLayer、Drawing ライブラリの代替に Terra Draw が案内されている ([非推奨一覧](https://developers.google.com/maps/deprecations))
- React / Vue などのラッパー: React 向けに vis.gl の `@vis.gl/react-google-maps` (1.10.2、MIT) ([npm](https://www.npmjs.com/package/@vis.gl/react-google-maps))。Vue 向けの公式ラッパーは未確認
- TypeScript の型: `@types/google.maps` (DefinitelyTyped、3.66.10) ([npm](https://www.npmjs.com/package/@types/google.maps))
- ネイティブ版・兄弟プロジェクト: Maps SDK for Android / iOS、Map Tiles API (2D タイル、Photorealistic 3D Tiles を外部レンダラに供給) ([料金](https://developers.google.com/maps/billing-and-pricing/pricing))
- 日本語の情報 (公式翻訳、国内コミュニティ): ドキュメントは `?hl=ja` で日本語版が出るが、HTML の言語属性は `ja-x-mtfrom-en` で、英語からの機械翻訳である ([日本語版の概要](https://developers.google.com/maps/documentation/javascript/overview?hl=ja))。国内コミュニティは未確認

## 開発の活発さ

- 直近 1 年のリリース数: リリースノートの日付エントリが 38 件 (2025-11-10〜2026-11-10。[リリースノートのフィード](https://developers.google.com/static/maps/documentation/javascript/feeds/releases.xml) で数えた。1 日に複数の版が出ることもあり、版の数とは一致しない)
- 最終コミット日: 対象外 (ソースが非公開)。最新のリリースノートは 2026-11-04 ([リリースノート](https://developers.google.com/maps/documentation/javascript/releases))
- 近年の大きな破壊的変更: Heatmap レイヤー (2025-05 非推奨、2026-05 廃止)、Drawing ライブラリ (2025-08 非推奨、2026-05 廃止)、45° 航空写真 (v3.65 で終了)、KmlLayer (2026-04 非推奨、使用不可に) ([非推奨一覧](https://developers.google.com/maps/deprecations))。DirectionsService / DirectionsRenderer / DistanceMatrixService は 2026-02-25 に非推奨 (3.64.2b) ([リリースノート](https://developers.google.com/maps/documentation/javascript/releases))

## 環境の違いと保守

- ブラウザ間の互換: 文書でうたう対応は、Windows の Microsoft Edge の現行版 (IE モードを除く)、Windows と macOS と Linux の Firefox と Chrome の最新 2 つのメジャー安定版、macOS の Safari の最新 2 つのメジャー安定版である (https://developers.google.com/maps/documentation/javascript/browsersupport)。本体は非公開で、Google がどのブラウザで自動テストしているかは未確認。
- OS 間の互換: 文書でうたうモバイルの対応は、Android 4.1 以上の Chrome の現行版、Android 4.4 以上の Chrome WebView、iOS の現行と一つ前のメジャー版の Mobile Safari と WKWebView、Chrome for iOS の現行版である (https://developers.google.com/maps/documentation/javascript/browsersupport)。ベクター地図は WebGL で GPU を使って描くと説明されるが (https://developers.google.com/maps/documentation/javascript/vector-map)、WebGL が使えない端末での挙動、GPU とドライバの違い、メモリ上限への対応を述べた文書は未確認。
- 操作の網羅: `gestureHandling` に `cooperative` (ページを普通にスクロールでき、地図は二本指かズームボタンで動かす)、`greedy` (すべてのタッチとスクロールに反応する)、`none` (操作を止める)、`auto` (iframe の中なら `cooperative`、それ以外は `greedy`) がある (https://developers.google.com/maps/documentation/javascript/interaction)。ベクター地図では、傾きと回転を有効にすると Shift を押したドラッグと Shift と矢印キーで傾きと方位を変えられる (https://developers.google.com/maps/documentation/javascript/vector-map)。慣性とペン入力の扱いを述べた文書は未確認。
- エッジケースへの対応: 本体が非公開で、日付変更線、精度、WebGL のコンテキスト喪失、タイルの読み込み失敗への対応は、利用者が設定する対象としては文書に見当たらない (未確認)。地図画像もライブラリも Google が配るので、これらは Google 側が引き受ける作り (推測)。
- 継続的な保守: CSP の文書があり、nonce を使う strict CSP を勧め、`script` と `style` の両方の要素に nonce を付けるよう求める。例示のポリシーには `worker-src blob:` と `'unsafe-eval'` が入っているが、要る理由は書かれていない (https://developers.google.com/maps/documentation/javascript/content-security-policy)。対応ブラウザは「最新 2 つのメジャー版」のように相対的に決めてあり、ブラウザの更新に合わせて自動的に動く方針である (https://developers.google.com/maps/documentation/javascript/browsersupport)。ブラウザ固有の不具合の変更履歴と、不具合の追跡の分類は未確認。

## 向いている場面

- Google の地図データ、航空写真、ストリートビュー、Places を使いたい場合
- 店舗検索やルート表示など、Google のサービスと組み合わせる用途
- 都市部のフォトリアリスティック 3D 表示が要る場合

## 向いていない場面

- 自前のベクトルタイルや独自のスタイル定義 (MapLibre / Mapbox Style) で地図を描きたい場合
- Google 以外の地図や地図データと同じ画面で組み合わせたい場合 (利用規約 3.2.3(e))
- オフライン、閉域網、オンプレミスでの運用
- 地図の投影法をメルカトル以外にしたい場合 (独自地図タイプの直交座標系の投影に限られる)
- 機能の廃止に追随する保守体制を用意できない場合

## 出典

- https://developers.google.com/maps/documentation/javascript
- https://developers.google.com/maps/documentation/javascript/versions
- https://developers.google.com/maps/documentation/javascript/releases
- https://developers.google.com/static/maps/documentation/javascript/feeds/releases.xml
- https://developers.google.com/maps/deprecations
- https://developers.google.com/maps/documentation/javascript/vector-map
- https://developers.google.com/maps/documentation/javascript/advanced-markers/overview
- https://developers.google.com/maps/documentation/javascript/3d-maps-overview
- https://developers.google.com/maps/documentation/javascript/3d/models
- https://developers.google.com/maps/documentation/javascript/coordinates
- https://developers.google.com/maps/documentation/javascript/maptypes
- https://developers.google.com/maps/documentation/javascript/datalayer
- https://developers.google.com/maps/documentation/javascript/dds-datasets/overview
- https://developers.google.com/maps/documentation/javascript/webgl/webgl-overlay-view
- https://developers.google.com/maps/documentation/javascript/usage-and-billing
- https://developers.google.com/maps/billing-and-pricing/pricing
- https://developers.google.com/maps/documentation/javascript/overview?hl=ja
- https://cloud.google.com/maps-platform/terms
- https://www.npmjs.com/package/@googlemaps/js-api-loader
- https://www.npmjs.com/package/@vis.gl/react-google-maps
- https://www.npmjs.com/package/@types/google.maps
- https://deck.gl/docs/api-reference/google-maps/google-maps-overlay
- https://deck.gl/docs/api-reference/geo-layers/tile-3d-layer

## 未確認のこと

- 地球儀表示: 2D の `Map` と 3D Maps のどちらについても、公式ドキュメントとリリースノートに地球儀表示の記述が見つからなかった
- Immersive Maps SKU と 3D Maps (`Map3DElement`) の対応関係: 料金ページに SKU の説明がなく、3D Maps のページも SKU 名を挙げていない
- 3D Maps の提供段階 (GA かどうか): リリースノートは「ウィークリーチャネルで利用可能」と書くだけで GA と明記していない
- 扱える地物・マーカー数の目安: 公式の記述がない
- Map Tiles API を Google 以外のレンダラで使う場合の条件: 利用規約 3.2.3(e) との関係を Map Tiles API 固有の規約で確かめていない
- Vue 向けラッパーと国内コミュニティ: 公式の案内が見つからなかった
- Advanced Markers が別途課金されるか: 公式ページに記述がない
