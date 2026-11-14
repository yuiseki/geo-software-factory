# PLATEAU (3D 都市モデル)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | 国土交通省 都市局 (Project PLATEAU)。CityGML などのファイルは一般社団法人社会基盤情報流通推進協議会が運用する G空間情報センターで公開 (https://www.mlit.go.jp/plateau/open-data/) |
| 公式サイト | https://www.mlit.go.jp/plateau/ 、配信サービスのドキュメント https://docs.plateauview.mlit.go.jp |
| 料金ページ | なし (無償で提供。PLATEAU 配信サービスは「無償で利用可能」と説明 https://github.com/Project-PLATEAU/plateau-streaming-tutorial) |
| 利用規約・ライセンス | PLATEAU サイトポリシー https://www.mlit.go.jp/plateau/site-policy/ (公共データ利用規約 第 1.0 版、CC BY 4.0 互換)。G空間情報センターの各データセットのライセンス欄は「PLATEAU Site Policy『3. 著作権について』に拠る」 |

## 概要

国土交通省が主導して整備・公開する全国の都市の 3D 都市モデルで、建築物、道路、橋梁、植生、都市設備、土地利用、都市計画決定情報、災害リスク (洪水・津波・高潮・内水浸水想定区域、土砂災害警戒区域) などを CityGML で持つ (https://api.plateauview.mlit.go.jp/datacatalog/plateau-datasets を 2026-11-10 に取得して集計)。原本の CityGML と、変換済みの 3D Tiles、MVT などが G空間情報センターでオープンデータとして公開されている (https://www.mlit.go.jp/plateau/open-data/)。これとは別に、3D Tiles、MVT、地形、航空写真オルソを URL で直接読み込める「PLATEAU 配信サービス」を試験運用している (https://www.mlit.go.jp/plateau/learning/tpc06-1/)。

## データの性質

- 種類 (地形、建物、フォトリアル、点群、屋内): 建物 (LOD1〜LOD4)、地形、道路・徒歩道・鉄道などの交通、橋梁、地下街、地下埋設物、植生、水部、都市設備、土地利用、都市計画、災害リスク区域。CityGML 3.0 による屋内モデルも一部ある (https://docs.plateauview.mlit.go.jp/datasets/3d-tiles/)。フォトリアルの 3D メッシュは無いが、建物にテクスチャ付きのデータがある。航空写真オルソのタイルも配信している (https://docs.plateauview.mlit.go.jp/datasets/ortho/)。点群の配信は見当たらない。
- 形式 (3D Tiles 1.0 / 1.1, quantized-mesh, glTF, CityGML, MVT など): 原本は CityGML。標準製品仕様書の最新版は第 5.1 版で CityGML 2.0 ベース (i-UR 拡張)、CityGML 3.0 への移行は 2028 年度からの予定で、3.0 対応の仕様書は案の段階 (https://www.mlit.go.jp/plateau/libraries/handbooks/)。可視化用には 3D Tiles と MVT。3D Tiles は従来 1.0 で、2025 年度以降に整備された一部が 1.1 で配信されるとされる (https://docs.plateauview.mlit.go.jp/datasets/3d-tiles/)。ただし 2026-11-10 にデータカタログ API を取得した時点では、建築物モデル 1,065 件はすべて `format_version` 1.0 だった。地形は quantized-mesh (Cesium 向け) と Cesium ion 版 terraindb (https://docs.plateauview.mlit.go.jp/datasets/terrain/)。G空間情報センターでは都市・年度によって GeoJSON、Shapefile、FBX、OBJ、GeoPackage、ファイルジオデータベース、GeoTIFF も配布されている (G空間情報センターの CKAN API で各データセットのリソースを確認。例 https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku-3dtiles-2020)。
- 詳細度 (LOD) とテクスチャの有無: 2026-11-10 時点のデータカタログでの建築物モデルの 3D Tiles は LOD1 が 451 件 (テクスチャ付き 448)、LOD2 が 565 件 (テクスチャ付き 300)、LOD3 が 45 件、LOD4 が 4 件 (https://api.plateauview.mlit.go.jp/datacatalog/plateau-datasets の集計。件数はデータセット単位で都市数ではない)。テクスチャあり・なしを選んで取得できる (https://docs.plateauview.mlit.go.jp/datasets/3d-tiles/)。
- カバー範囲 (国内の都市数、全球): 国内のみ。2025 年度末時点で 329 都市で整備済み (https://www.mlit.go.jp/report/press/toshi03_hh_000223.html)。オープンデータページの掲載は 306 件 (2026-05-11 更新) (https://www.mlit.go.jp/plateau/open-data/)。地形 (PLATEAU-Terrain) は日本全国をカバーする (https://docs.plateauview.mlit.go.jp/datasets/terrain/)。
- 更新頻度: 都市ごとに整備年度があり、年度単位で新規整備や更新が加わる。データカタログでは `year` (整備年度) と `latest` 指定で最新年度に追従できる (https://docs.plateauview.mlit.go.jp/datasets/3d-tiles/)。都市ごとの更新周期は決まっていない (推測。公式の周期の記述は見つからない)。データカタログは G空間情報センターより先に更新されることがある (https://docs.plateauview.mlit.go.jp/datasets/citygml/)。

## 配信と対応ライブラリ

- 配信方法 (ホスティング、ダウンロード、自前変換): 3 通り。(1) G空間情報センターから CityGML や変換済みファイルを zip でダウンロード (https://www.mlit.go.jp/plateau/open-data/)。(2) PLATEAU 配信サービス (試験運用) から 3D Tiles の tileset.json、MVT の TileJSON、地形、オルソを URL で直接読み込む。配信 URL はデータカタログ API (REST `https://api.plateauview.mlit.go.jp/datacatalog/plateau-datasets`、GraphQL) で取得する。3D Tiles は建築物などの立体の地物、MVT は土地利用、道路、都市計画決定情報、土砂災害警戒区域などの平面の地物が中心 (2026-11-10 のカタログ集計) (https://docs.plateauview.mlit.go.jp/datasets/3d-tiles/)。CityGML API で範囲を指定した CityGML の取得もできる (https://docs.plateauview.mlit.go.jp/datasets/citygml/)。(3) CityGML を自前で変換する。PLATEAU GIS Converter (CityGML を 3D Tiles 1.1、MVT、GeoPackage などへ変換。MIT、最新 v0.1.19 は 2026-08-26) (https://github.com/MIERUNE/plateau-gis-converter 、国交省側の配布 https://github.com/Project-PLATEAU/PLATEAU-GIS-Converter は v0.1.14)、地形の CityGML を Terrain-RGB に変換する PLATEAU Mapbox Terrain Converter (MIT) (https://github.com/Project-PLATEAU-Admin/plateau-mb-terrain-converter)。
- 対応ライブラリ (CesiumJS, deck.gl, 3DTilesRendererJS, ゲームエンジンなど): 公式ドキュメントのサンプルは CesiumJS (3D Tiles) と、MVT 向けの cesium-mvt-imagery-provider。MVT の TileJSON は MapLibre GL JS や Mapbox GL JS から使える (https://docs.plateauview.mlit.go.jp/datasets/3d-tiles/)。オルソは XYZ と WMS で Leaflet のサンプルがある (https://docs.plateauview.mlit.go.jp/datasets/ortho/)。ゲームエンジン向けに PLATEAU SDK for Unity (v4.3.0、MIT) と PLATEAU SDK for Unreal (v3.2.2、MIT) がある (https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unity 、https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unreal)。3D Tiles は標準形式なので deck.gl や 3DTilesRendererJS でも読めると考えられる (推測。公式のサンプルは見つからない)。PLATEAU-Terrain の quantized-mesh は Cesium 向けで、MapLibre の raster-dem 向け Terrain-RGB の配信は未リリース (https://docs.plateauview.mlit.go.jp/datasets/terrain/)。
- API キー・アカウントの要否: データカタログ API と 3D Tiles・MVT の取得にはキーが要らない (2026-11-10 に `https://api.plateauview.mlit.go.jp/datacatalog/plateau-datasets` をキーなしで取得し HTTP 200 を確認)。地形の Cesium ion 版 terraindb を使う場合のみ、ドキュメントに掲載のアクセストークンとアセット ID が要る。`/terrain/` の quantized-mesh はトークン不要 (https://docs.plateauview.mlit.go.jp/datasets/terrain/)。G空間情報センターのダウンロードもアカウント不要 (推測。今回キーなしで API 検索できた)。

## 料金

- 無料枠と課金単位: 無料。課金は無い (https://github.com/Project-PLATEAU/plateau-streaming-tutorial)。
- 従量単価・契約形態 (問い合わせ制ならそう書き、金額を推測しない): なし (2026-11-10 時点)。契約も不要。

## 利用規約上の制約

- 商用利用、政府・公共案件での利用: 可能。サイトポリシーは公共データ利用規約 第 1.0 版 (PDL1.0) を適用し、CC BY 4.0 と互換、ODC-BY や ODbL での利用も妨げないとする (https://www.mlit.go.jp/plateau/site-policy/)。配信サービスのオルソのページは「CC BY 4.0 に従い、商用利用を含め自由に利用できる」と説明している (https://docs.plateauview.mlit.go.jp/datasets/ortho/)。ただし測量法に基づく公共測量の成果など、個別法令で利用が制限されるコンテンツがある (https://www.mlit.go.jp/plateau/site-policy/)。
- キャッシュ・ダウンロード・自前ホストの可否: 可能。CityGML や 3D Tiles はダウンロード用に公開されており、自前で変換・ホストできる (https://www.mlit.go.jp/plateau/open-data/)。配信サービスは ETag による HTTP キャッシュに対応する (https://docs.plateauview.mlit.go.jp/datasets/3d-tiles/)。
- 帰属表示の要件: 「出典：国土交通省 PLATEAU ウェブサイト (当該ページの URL)」のように記載する。加工した場合は加工した旨を別に記載し、国交省が作成したように見せてはならない (https://www.mlit.go.jp/plateau/site-policy/)。G空間情報センターの 3D 都市モデルの著作権は各地方公共団体に帰属する (同)。地形を表示する場合は「PLATEAU | Mapterhorn | 国土地理院」のいずれかの帰属表示が要り、Cesium ion 版の地形を使う場合は「地形データは、測量法に基づく国土地理院長承認 (使用) R3JHs 778 を得て使用」の記載が求められる (https://docs.plateauview.mlit.go.jp/datasets/terrain/)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): データには継承条件 (share-alike) が無い。組み込み、改変、配布、SaaS 提供のいずれも出典の表示 (改変時は加工の旨) で足りる (https://www.mlit.go.jp/plateau/site-policy/)。ツール側では、PLATEAU SDK for Unity / Unreal が同梱する libcitygml が LGPL 2.1 で、同梱物に Autodesk の FBX SDK も含まれる (各リポジトリの ThirdPartyNotices.md)。LGPL 2.1 部分は、SDK を組み込んだアプリを配布する際、利用者が libcitygml を差し替えて再リンクできるようにする (動的リンクにするか、オブジェクトファイルを提供する) ことと、ライセンス文と改変したライブラリのソースの提供が求められる。改変せずに使う場合も表示と再リンク可能性の確保は要る。SaaS としてサーバ側で動かすだけで配布しない場合は LGPL の義務は生じない。FBX SDK は Autodesk のライセンス条件に従う (詳細は未確認)。PLATEAU GIS Converter、PLATEAU Mapbox Terrain Converter は MIT、PLATEAU VIEW 5.0 は Apache-2.0 でコピーレフトではない (https://github.com/Project-PLATEAU/PLATEAU-VIEW-5.0)。

## 安定性と運用

- SLA・運用形態 (本運用か試験運用か): PLATEAU 配信サービスは試験運用で、提供期間やサービスレベルは保証されない。データ内容、API の URL 書式、レスポンスは予告なく変わることがある (https://docs.plateauview.mlit.go.jp/datasets/3d-tiles/ 、https://www.mlit.go.jp/plateau/learning/tpc06-1/)。旧配信 URL を年度内で終了した例がある (2023 年 4 月の告知、https://github.com/Project-PLATEAU/plateau-streaming-tutorial)。G空間情報センターのオープンデータは国の事業として 2021 年度から公開が続いている (https://www.mlit.go.jp/plateau/open-data/)。国交省は利用者がデータを用いて行う一切の行為について責任を負わない (https://www.mlit.go.jp/plateau/site-policy/)。

## 向いている場面

- 国内の都市を対象にした 3D の可視化、都市計画、防災 (浸水想定などの重ね合わせ)、景観・日照のシミュレーション。
- 建物の用途、高さ、構造などの属性を使う分析 (CityGML の属性を使う)。
- 商用を含めて無償で 3D 建物データを使い、自前でホストしたいとき (継承条件が無い)。
- Unity / Unreal でのデジタルツインやゲーム、XR コンテンツ。

## 向いていない場面

- 整備されていない都市や海外を含む用途 (全国の網羅ではない)。
- 配信サービスに SLA が要る本番システム (試験運用のため。自前ホストを前提にする)。
- フォトリアルな 3D メッシュが要る用途 (建物は LOD のモデルで、写真測量のメッシュではない)。
- MapLibre だけで地形と建物を完結させたい場合 (3D Tiles は MapLibre GL JS が標準では描画せず、Terrain-RGB の配信も未リリース。変換や別ライブラリが要る)。

## プライバシーとテレメトリ (2026-11-14 確認)

- **オープンデータの自前配信**: G空間情報センターや GitHub から 3D Tiles / CityGML をダウンロードして自前配信する場合、国土交通省や第三者へのエンドユーザー接続やテレメトリ送信は発生しない。
- **試験配信エンドポイント利用時**: 国交省の試験配信 URL やパートナー配信を直接参照する場合は、配信元サーバーに通常の HTTP アクセスログ (IP アドレス・リファラー等) が残る。公開配信サーバー側のログ保持方針は未確認。

## 出典

- https://www.mlit.go.jp/plateau/
- https://www.mlit.go.jp/plateau/site-policy/
- https://www.mlit.go.jp/plateau/open-data/
- https://www.mlit.go.jp/plateau/learning/tpc06-1/
- https://www.mlit.go.jp/plateau/libraries/handbooks/
- https://www.mlit.go.jp/report/press/toshi03_hh_000223.html
- https://docs.plateauview.mlit.go.jp
- https://docs.plateauview.mlit.go.jp/datasets/3d-tiles/
- https://docs.plateauview.mlit.go.jp/datasets/terrain/
- https://docs.plateauview.mlit.go.jp/datasets/ortho/
- https://docs.plateauview.mlit.go.jp/datasets/citygml/
- https://api.plateauview.mlit.go.jp/datacatalog/plateau-datasets
- https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku-3dtiles-2020
- https://github.com/Project-PLATEAU/plateau-streaming-tutorial
- https://github.com/MIERUNE/plateau-gis-converter
- https://github.com/Project-PLATEAU/PLATEAU-GIS-Converter
- https://github.com/Project-PLATEAU-Admin/plateau-mb-terrain-converter
- https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unity
- https://github.com/Project-PLATEAU/PLATEAU-SDK-for-Unreal
- https://github.com/Project-PLATEAU/PLATEAU-VIEW-5.0

## 未確認のこと

- 3D Tiles 1.1 で配信されているデータの有無: ドキュメントは 2025 年度以降の一部を 1.1 とするが、2026-11-10 のカタログの建築物モデルはすべて 1.0 だった。建築物以外の 1.1 の有無は集計していない。
- 配信サービスにリクエスト数の上限や利用規約が別にあるか: ドキュメントに記載が見つからなかった。
- 整備都市数の差 (329 と 306): 329 は 2025 年度末の整備数、306 はオープンデータページの掲載数 (2026-05-11) で、公開待ちの都市があると考えられるが確かめていない。データカタログの `city_code` は 307 種類あった (区を別コードにする例があるため都市数とは一致しない可能性がある)。
- 測量法の手続が要るコンテンツの範囲: サイトポリシーは公共測量成果などに制限があると書くが、どのデータセットが該当するかは示していない。
- FBX SDK の再配布条件: PLATEAU SDK に同梱される Autodesk FBX SDK のライセンス本文を読んでいない。
- 2027 年度末に 500 都市とする目標: 検索結果では見えたが、公式の報道発表ページの本文で確かめられなかったため本文に書いていない。
