# 特定の要件でだけ候補になるライブラリ

確かめた日: 2026-11-10

比較表に毎回並べるほどではないが、特定の要件ではそれでしか実現できないもの。要件に当てはまるときだけ候補に加える。

日付は JST。「提供状況」の版と日付は GitHub / GitLab の最新リリース、npm、pub.dev で 2026-11-10 に確かめた。表中の「archived でない」は GitHub API の `archived: false` を確かめたもの。

| 名前 | 種別 | それでしか実現できないこと / 選ぶ事情 | 提供状況 | ライセンス・利用条件 (コピーレフトや商用禁止の注意を含む) | 料金の概略 | 出典 |
|---|---|---|---|---|---|---|
| Giro3D | Web 用 3D 地理空間可視化フレームワーク (JavaScript、three.js ベース) | 点群 (COPC、LAS/LAZ、Potree、3D Tiles の点群) や COG / GeoTIFF の標高・画像を、ブラウザでタイル変換せずに 2D/2.5D/3D で重ねて表示したいとき。 | 開発は GitLab。最新 v2.0.6 (2026-10-29)、最終活動 2026-11-10。npm `@giro3d/giro3d` 2.0.6。 | MIT (GitLab の LICENSE で確認)。組み込み、改変、配布、SaaS のいずれも著作権表示とライセンス文の同梱だけでよい。 | 無料 (OSS)。 | https://giro3d.org/ 、 https://giro3d.org/latest/examples/index.html 、 https://gitlab.com/giro3d/giro3d |
| iTowns | Web 用 3D 地理空間可視化フレームワーク (JavaScript) | 地球儀表示と投影座標系の平面表示を切り替えつつ、3D Tiles、点群 (Potree、EPT、COPC、LAS)、COG を Web で表示したいとき。フランス IGN のロゴが公式サイトに並ぶ。 | 最新 v2.46.0 (2025-10-07)、最終 push 2026-11-03、archived でない。 | CeCILL-B 1.0 と MIT のデュアル (LICENSE.md、npm の表記は `CECILL-B OR MIT`)。MIT を選べば組み込み、改変、配布、SaaS のいずれも著作権表示だけでよい。 | 無料 (OSS)。 | https://www.itowns-project.org/ 、 https://github.com/iTowns/itowns |
| Mappedin | 屋内地図の商用プラットフォーム (作成ツール + Web / iOS / Android / React Native の SDK) | 商業施設、空港、オフィスなどの屋内地図を作り、経路案内つきでアプリに組み込みたいとき。屋内地図を IMDF で書き出して Apple に申請する用途もある。 | 商用製品。npm `@mappedin/mappedin-js` 6.31.0 (2026-11-05)。SDK は公開リポジトリではなく npm で配布。 | 独自の SDK ライセンス (npm パッケージ同梱の LICENSE.txt)。OSS ではない。詳細は表の下の「ライセンス上の注意」。 | 建物の面積に応じたサブスクリプションで、金額は見積もり制 (2026-11-10 確認)。無料で地図作成を始められ、Free / Plus / Pro のプランがある。 | https://www.mappedin.com/pricing/ 、 https://developer.mappedin.com/ 、 https://www.npmjs.com/package/@mappedin/mappedin-js 、 https://www.mappedin.com/resources/blog/product-101-imdf-export |
| IMDF (Indoor Mapping Data Format) | 屋内地図のデータ形式 (GeoJSON ベースの仕様。ライブラリではない) | Apple Maps の屋内地図 (Indoor Maps Program) に施設を載せたい、または MapKit で屋内地図を扱いたいとき。空港、商業施設、駅向けの詳しい指針を含む。 | Apple の仕様 1.0.0 (Apple の掲載ページは 2021-10-19 更新)。OGC Community Standard 1.0.0 として 2021-02-02 承認。 | 仕様の利用は Apple の IMDF Terms of Use に従う。改変不可、社内共有とリンクは可、Apple への補償義務あり。OGC 版は royalty free, non-discriminatory で公開。 | 仕様は無料。Apple への掲載は Apple Business Register 経由 (費用は未確認)。 | https://register.apple.com/resources/imdf/ 、 https://docs.ogc.org/cs/20-094/index.html 、 https://docs.ogc.org/cs/20-094/License/index.html |
| Mapsforge / VTM | オフライン地図描画ライブラリ (Java)。Mapsforge は Android と Java デスクトップ、VTM は OpenGL 版で Android、iOS、デスクトップ、ブラウザ | 通信なしで動く端末で、独自の .map 形式 (OSM から生成) をベクタ描画したいとき。陰影起伏もオフラインで描ける。VTM は MVT や MBTiles も読める。 | Mapsforge 0.31.0 (2026-10-28)、VTM 0.31.0 (2026-10-28)。どちらも archived でない。 | LGPL-3.0 だが §4(d) と §4(e) の制約を免除する特例つき。詳細は表の下の「ライセンス上の注意」。 | 無料 (OSS)。地図ファイルは download.mapsforge.org で配布。 | https://github.com/mapsforge/mapsforge 、 https://github.com/mapsforge/vtm |
| MapLibre Native Qt | MapLibre Native の Qt バインディングと Qt Location プラグイン (C++ / QML) | Qt / QML で作るネイティブアプリ (デスクトップ、組み込み Linux など) に MapLibre のベクタ地図を入れたいとき。Linux、Windows、macOS、iOS、Android、WASM 向けのビルド設定がある。車載用途は推測 (下記)。 | 最新リリース v3.0.0 (2024-10-12)。main は 4.0 を開発中で、README に「API は安定版までに変わりうる」とある。最終 push 2026-11-10。Qt 6.5 以上。 | コアは BSD-2-Clause、QML バインディングは GPL-2.0 / GPL-3.0 / LGPL-3.0 から選択、例は MIT (README と LICENSES/)。GitHub の自動判定は空。詳細は表の下。 | 無料 (OSS)。Qt 自体のライセンス費用は別 (未確認)。 | https://github.com/maplibre/maplibre-native-qt 、 https://maplibre.org/maplibre-native-qt/docs/ |
| OpenSeadragon | 高解像度画像のズームビューア (JavaScript) | 地理座標を持たない巨大画像 (顕微鏡画像、美術品、古地図のスキャン) をタイル化してズーム表示したいとき。DZI、IIIF、Zoomify、TMS などに対応し、プラグインで GeoTIFF や OME-Zarr も扱える。 | 最新 v6.1.1 (2026-09-10)、archived でない。 | BSD-3-Clause。組み込み、改変、配布、SaaS のいずれも著作権表示だけでよい (名前を宣伝に使う場合は許可が要る)。 | 無料 (OSS)。 | https://openseadragon.github.io/ 、 https://github.com/openseadragon/openseadragon |
| (参考) forge3d | Python から地形と地図の作品を描くレンダラー (Rust、wgpu) | 地形を 3D にした地図を、印刷の解像度の PNG、PNG16、EXR で書き出したいとき。SVG と PDF の書き出しは Pro 機能。詳細は [python/forge3d](python/forge3d.md) | [python/forge3d](python/forge3d.md) を見る | 中核は Apache-2.0 OR MIT、一部は商用のライセンスキー | 中核は無料、Pro は価格非公開 | https://github.com/milos-agathon/forge3d |
| (参考) ezu | サーバー側の地図描画エンジン (純粋な Rust、CPU だけ) | GPU の無いサーバーで、ベクトルタイル (MVT、PMTiles) からタイルや印刷の 1 枚を描きたいとき。絵画風の描画。詳細は [server/ezu](server/ezu.md) | [server/ezu](server/ezu.md) を見る | MIT OR Apache-2.0 | 無料 (OSS) | https://github.com/reearth/ezu |
| Mapnik | サーバ側の地図描画ツールキット (C++、Python / Node.js バインディング) | サーバでラスタ画像や PDF / SVG / PostScript を描画したいとき (Cairo レンダラー使用時)。ブラウザに描画を任せられない印刷・バッチ出力向け。 | 最新 v4.3.2 (2026-09-23)、最終 push 2026-11-08、archived でない。 | LGPL-2.1 (COPYING)。コピーレフト。詳細は表の下。 | 無料 (OSS)。 | https://mapnik.org/ 、 https://github.com/mapnik/mapnik 、 https://github.com/mapnik/mapnik/wiki/OutputFormats |
| MapFish Print | サーバ側の地図印刷サービス (Java、JasperReports ベース) | 地図を含む帳票を PDF や画像 (PNG、JPEG、SVG、TIFF など) でサーバから出力したいとき。WAR (Tomcat など)、JAR、コマンドラインで動く。 | 最新 4.0.13 (2026-11-07)、archived でない。 | BSD-2-Clause (Camptocamp SA)。コピーレフトではない。組み込み、改変、配布、SaaS のいずれも著作権表示だけでよい。依存する JasperReports のライセンスは未確認。 | 無料 (OSS)。 | https://mapfish.github.io/mapfish-print-doc/ 、 https://mapfish.github.io/mapfish-print-doc/outputformats.html 、 https://github.com/mapfish/mapfish-print |
| react-map-gl | React ラッパー (MapLibre GL JS / Mapbox GL JS 向け) | React で MapLibre GL JS か Mapbox GL JS を宣言的に使いたいとき。v8 は `react-map-gl/maplibre` と `react-map-gl/mapbox` で描画エンジンを選ぶ。 | 最新 v8.1.3 (2026-09-03)、archived でない。 | MIT (LICENSE 本文で確認、GitHub の自動判定は NOASSERTION)。ただし `mapbox-gl` v2 以降は Mapbox TOS のもとでのみ使える独自ライセンス。 | ラッパーは無料。Mapbox GL JS を使う場合、Web の map loads は月 50,000 まで無料、超過分は 1,000 あたり 5.00 USD から (2026-11-10 確認)。 | https://visgl.github.io/react-map-gl/docs/get-started 、 https://github.com/visgl/react-map-gl 、 https://github.com/mapbox/mapbox-gl-js 、 https://www.mapbox.com/pricing |
| @vis.gl/react-google-maps | React ラッパー (Google Maps JavaScript API 向け) | React で Google Maps JavaScript API を使いたいとき。マーカー、InfoWindow、図形、3D 地図などをコンポーネントと hooks で扱える。 | 最新 v1.10.2 (2026-10-30)、archived でない。 | MIT。地図そのものは Google Maps Platform の規約と課金に従う。 | ラッパーは無料。Dynamic Maps は月 10,000 回まで無料、超過分 (10,001〜100,000) は 1,000 回あたり 7.00 USD (2026-11-10 確認)。 | https://visgl.github.io/react-google-maps/ 、 https://github.com/visgl/react-google-maps 、 https://developers.google.com/maps/billing-and-pricing/pricing |
| react-leaflet | React ラッパー (Leaflet 向け) | 既存の Leaflet 資産 (プラグイン、ラスタタイル) を React から使いたいとき。 | 最新 v5.0.0 (2024-12-14)、最終 push 2026-11-08、archived でない。 | Hippocratic License 2.1 (SPDX では OSI 非承認)。人権に関する条件と仲裁条項がある。詳細は表の下。 | 無料。 | https://react-leaflet.js.org 、 https://github.com/PaulLeCam/react-leaflet 、 https://spdx.org/licenses/Hippocratic-2.1.html |
| @rnmapbox/maps | React Native ラッパー (Mapbox Maps SDK for iOS / Android 向け) | React Native アプリで Mapbox のネイティブ地図 SDK を使いたいとき。Expo は config plugin で対応し、Expo Go では動かない。 | 最新 v10.3.17 (2026-11-04)、archived でない。既定は Mapbox Maps SDK 11 系。 | ラッパーは MIT。中身の Mapbox Maps SDK は Mapbox TOS のもとでのみ使える独自ライセンス (課金・計測部分の改変は不可、匿名化した位置・利用データを送信)。 | ラッパーは無料。Mapbox のモバイル SDK は月 25,000 MAU まで無料、25,001〜125,000 MAU は 1,000 MAU あたり 4.00 USD (2026-11-10 確認)。 | https://rnmapbox.github.io/docs/install 、 https://github.com/rnmapbox/maps 、 https://github.com/mapbox/mapbox-maps-ios 、 https://www.mapbox.com/pricing |
| MapLibre for Flutter | Flutter プラグイン。2 系統が並立: `maplibre_gl` (maplibre/flutter-maplibre-gl) と `maplibre` (josxha/flutter-maplibre) | Flutter で API キー不要の MapLibre 地図を使いたいとき。`maplibre_gl` は flutter-mapbox-gl の fork で Android、iOS、Web に対応。`maplibre` は FFI で呼び出す新しい実装で Android、iOS、macOS、Windows、Linux、Web に対応。 | `maplibre_gl` 0.28.0 (pub.dev 2026-11-03)。`maplibre` 0.3.7+1 (pub.dev 2026-10-30)、0.x 系。どちらも archived でない。 | どちらも BSD-3-Clause 相当 (LICENSE 本文で 3 条項を確認、GitHub の自動判定は NOASSERTION)。組み込み、改変、配布、SaaS のいずれも著作権表示だけでよい。 | 無料。タイルの費用は選んだ提供元による。 | https://github.com/maplibre/flutter-maplibre-gl 、 https://github.com/josxha/flutter-maplibre 、 https://pub.dev/packages/maplibre_gl 、 https://pub.dev/packages/maplibre |
| ECharts の地図 | グラフライブラリの地図機能 (geo コンポーネントと map シリーズ) | ダッシュボードの他のグラフと同じ見た目・操作で、GeoJSON や SVG を登録して塗り分け地図や散布図を描きたいとき。独自投影も渡せる。Baidu Maps 拡張 (bmap) もある。 | Apache ECharts 6.1.0 (2026-05-20)、archived でない。 | Apache-2.0。組み込み、改変、配布、SaaS のいずれも可。配布時はライセンス文と NOTICE を同梱する。 | 無料 (OSS)。 | https://echarts.apache.org/en/llms-documents/option-parts/option.geo.md 、 https://github.com/apache/echarts |
| Observable Plot の地図 | グラフライブラリの地図機能 (geo マークと投影) | 統計グラフと同じ文法で、GeoJSON / TopoJSON の主題図 (塗り分け図など) を d3-geo の投影で SVG に描きたいとき。レポートや記事の静的な図向け。 | @observablehq/plot 0.6.19 (2026-11-06)、archived でない。 | ISC。組み込み、改変、配布、SaaS のいずれも著作権表示だけでよい。 | 無料 (OSS)。 | https://observablehq.com/plot/marks/geo 、 https://github.com/observablehq/plot |

## ライセンス上の注意

本節は LICENSE 本文の要約であり、法的な判断ではない。製品に組み込む前に原文を確かめる。

- Mappedin: npm パッケージ同梱の「Software Developer Toolkit License Agreement」が基本の許諾で、範囲は評価・開発・デモ目的に限られる。商用のアプリを作った時点で、その時点の商用ライセンス (ロイヤルティの支払いを含む) に同意したものとみなされる。ただし Mappedin の製品・サービスで SDK が無償提供または追加購入済みの場合は、この商用利用の制限が適用されない。改変 (リバースエンジニアリング、逆コンパイル) は禁止。配布は自社アプリに組み込む場合だけ認められ、アプリ側に SDK を大きく超える機能が必要。SDK 単体や SDK をそのままホストしたサービスとして他者に提供すること、Mappedin と競合する製品の開発に使うことは禁止。SDK をコピーレフトのライセンスに巻き込む改変・配布も禁止。
- IMDF: 仕様書は改変できず、社外への再掲載も禁止される。IMDF 形式のデータを作って自社製品で使うことの可否は Terms of Use に明記がない (未確認)。Apple は条件をいつでも変更でき、使い続けると同意したとみなされる。
- Mapsforge / VTM: LGPL-3.0 だが、§4(d) と §4(e) (利用者が再リンクできる手段を用意する義務、インストール情報の提供義務) を免除している。README は「アプリをオープンソースにせずに Android アプリへ組み込める」と書いている。ライブラリ本体を改変して配布する場合は、改変部分を LGPL-3.0 で公開する義務が残る。SaaS として提供するだけなら、LGPL は配布を伴わないため公開義務は生じない。VTM は SGI Free Software License B 2.0 の tessellate など、第三者コードを含む。
- MapLibre Native Qt: コア (BSD-2-Clause) だけを C++ から使うなら著作権表示だけでよい。QML バインディングを使う場合は GPL-2.0 / GPL-3.0 / LGPL-3.0 から選ぶ。非公開のアプリに組み込むなら LGPL-3.0 を選び、動的リンクなど利用者がライブラリを差し替えられる形で配布し、バインディングを改変した場合はその部分を公開する。GPL を選ぶとアプリ全体を GPL で公開する義務が生じる。Qt 自体のライセンス (商用または LGPL/GPL) は別に確かめる必要がある (未確認)。
- Mapnik: LGPL-2.1。サーバ内で使うだけ (SaaS) なら配布にあたらないため公開義務はない。Mapnik を組み込んだソフトウェアを配布する場合は、Mapnik 部分のソースの提供と、利用者が Mapnik を差し替えて再リンクできるようにすることが求められる。Mapnik 本体を改変して配布する場合は改変部分も LGPL-2.1 で公開する。
- react-leaflet: Hippocratic License 2.1 は、国連の世界人権宣言などの人権原則に沿った利用を条件にし、人権法に反する用途での利用を禁じる。紛争はハーグ規則による仲裁 (書類は原則公開) で扱われ、参加を拒むとライセンスが失効する。改変版には改変した旨の表示が必要。SPDX の一覧で OSI 非承認であり、「OSI 承認ライセンスのみ」とする社内規定や調達条件に合わない可能性がある。依存する Leaflet 本体のライセンスは別 (本ファイルでは未確認)。
- react-map-gl / @rnmapbox/maps: ラッパーは MIT だが、Mapbox 側の SDK (mapbox-gl v2 以降、Mapbox Maps SDK for iOS / Android) は有効な Mapbox アカウントと Mapbox TOS が前提の独自ライセンス。Mapbox の製品と組み合わせる場合に限り使える。MapLibre GL JS と組み合わせる react-map-gl はこの制約を受けない。
- iTowns: CeCILL-B はフランス法準拠の BSD 型ライセンスで SPDX では OSI 非承認。MIT とのデュアルなので、MIT を選べばこの点は問題にならない。

## 環境の違いと保守

- ブラウザ間の互換: Web 用のものでは、iTowns が機能テストを puppeteer (Chrome) で回している (https://github.com/iTowns/itowns/blob/master/package.json 、https://github.com/iTowns/itowns/blob/master/test/hooks_functional.js)。MapLibre Native Qt は WASM のビルドを CI に持つ (https://github.com/maplibre/maplibre-native-qt/tree/main/.github/workflows)。React のラッパー (react-map-gl、@vis.gl/react-google-maps、react-leaflet) のブラウザ間の互換は下の地図ライブラリに従う (推測)。Mappedin のような商用のプラットフォームでは提供元が持ち、対応ブラウザの記述は未確認。他の製品の対応ブラウザと CI のブラウザは未確認。
- OS 間の互換: MapLibre Native Qt は CI に Android、iOS、Linux、macOS、Windows、WASM のワークフローを持つ (https://github.com/maplibre/maplibre-native-qt/tree/main/.github/workflows)。@rnmapbox/maps は Android と iOS の CI を持ち、iOS はシミュレーターで回す (https://github.com/rnmapbox/maps/blob/main/.github/workflows/ios-actions.yml)。Mapsforge / VTM、MapLibre for Flutter などの試験の範囲は未確認。
- 操作の網羅: React と React Native と Flutter のラッパーは、下の地図ライブラリや SDK の操作をそのまま引き継ぐ (推測)。OpenSeadragon、ECharts、Observable Plot は地図専用の操作ではなく、それぞれの画像ビューアやグラフの操作になる (推測)。個別の確かめは未確認。
- エッジケースへの対応: 日付変更線、描画コンテキストの喪失、タイル読み込みの再試行の扱いは製品ごとに調べておらず未確認。Mapsforge / VTM は通信なしでの描画そのものが目的である (上の表)。
- 継続的な保守: @rnmapbox/maps は CI の入力で React Native の New Architecture の有効、無効を切り替えてビルドする (https://github.com/rnmapbox/maps/blob/main/.github/workflows/android-actions.yml 、https://github.com/rnmapbox/maps/blob/main/.github/workflows/ios-actions.yml)。それ以外の製品の OS とフレームワークの新版への追随、CSP の文書は未確認。

## 出典

- https://giro3d.org/
- https://giro3d.org/latest/examples/index.html
- https://gitlab.com/giro3d/giro3d
- https://gitlab.com/giro3d/giro3d/-/raw/main/LICENSE
- https://www.npmjs.com/package/@giro3d/giro3d
- https://www.itowns-project.org/
- https://github.com/iTowns/itowns
- https://github.com/iTowns/itowns/blob/master/LICENSE.md
- https://www.mappedin.com/pricing/
- https://developer.mappedin.com/
- https://www.npmjs.com/package/@mappedin/mappedin-js
- https://www.mappedin.com/resources/blog/product-101-imdf-export
- https://register.apple.com/resources/imdf/
- https://docs.ogc.org/cs/20-094/index.html
- https://docs.ogc.org/cs/20-094/License/index.html
- https://github.com/mapsforge/mapsforge
- https://github.com/mapsforge/vtm
- https://github.com/maplibre/maplibre-native-qt
- https://github.com/maplibre/maplibre-native-qt/blob/main/docs/Building.md
- https://maplibre.org/maplibre-native-qt/docs/
- https://openseadragon.github.io/
- https://github.com/openseadragon/openseadragon
- https://mapnik.org/
- https://github.com/mapnik/mapnik
- https://github.com/mapnik/mapnik/wiki/OutputFormats
- https://mapfish.github.io/mapfish-print-doc/
- https://mapfish.github.io/mapfish-print-doc/outputformats.html
- https://github.com/mapfish/mapfish-print
- https://visgl.github.io/react-map-gl/docs/get-started
- https://github.com/visgl/react-map-gl
- https://github.com/mapbox/mapbox-gl-js
- https://visgl.github.io/react-google-maps/
- https://github.com/visgl/react-google-maps
- https://developers.google.com/maps/billing-and-pricing/pricing
- https://react-leaflet.js.org
- https://github.com/PaulLeCam/react-leaflet
- https://spdx.org/licenses/Hippocratic-2.1.html
- https://spdx.org/licenses/licenses.json
- https://rnmapbox.github.io/docs/install
- https://github.com/rnmapbox/maps
- https://github.com/mapbox/mapbox-maps-ios
- https://www.mapbox.com/pricing
- https://github.com/maplibre/flutter-maplibre-gl
- https://github.com/josxha/flutter-maplibre
- https://pub.dev/packages/maplibre_gl
- https://pub.dev/packages/maplibre
- https://echarts.apache.org/en/llms-documents/option-parts/option.geo.md
- https://github.com/apache/echarts
- https://observablehq.com/plot/marks/geo
- https://github.com/observablehq/plot

## 未確認のこと

- MapLibre Native Qt の車載での採用: Automotive Grade Linux 向けのレイヤーにレシピがあるという検索結果は得たが、layers.openembedded.org が 403 を返し原文を読めなかった。表では「推測」とした。
- Qt 自体のライセンス費用・条件: Qt の商用 / LGPL の区分は本ファイルの対象外として確かめていない。
- Mappedin の金額: 料金ページは見積もり制で金額を載せていない。SDK を商用で使う場合にどのプランが必要かもページに記載がなく、営業への問い合わせが必要。
- Mappedin の商用ライセンス本文: 同梱の LICENSE.txt は評価用の許諾で、商用時に適用される「その時点の商用ライセンス」の本文は公開されていない。
- IMDF の Terms of Use がデータ作成・製品での利用をどう扱うか: 条文に明記がない。Apple Business Register への掲載費用も公式ページに記載が見当たらなかった。
- MapFish Print が依存する JasperReports Library のライセンス: 今回は MapFish Print 本体の LICENSE だけを確かめた。
- react-leaflet が依存する Leaflet 本体のライセンス: 本ファイルの範囲外として確かめていない。
- Observable Plot がパン・ズームや背景タイルを持たないこと: geo マークと投影の文書にそれらの記述が見当たらないことを確かめただけで、無いことを明記した文書は見ていない。表では「静的な図向け」とだけ書いた。
- josxha/flutter-maplibre の位置づけ: LICENSE に「Copyright (c) 2026 MapLibre contributors」とあるが、MapLibre org への移管の有無は確かめていない (maplibre/flutter-maplibre は 2026-11-10 時点で存在しない)。
