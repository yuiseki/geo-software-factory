# 地図 API の規約で引っかかりやすい条項

対象: キャッシュと保存、他社の地図との併用、機械学習への利用、ベンチマークの公表、表示の改変の禁止。地図に載せる動画・音楽の API (YouTube、iTunes Search API) の要点。各提供元の事実は geo-software-infra の reference にあり、ここでは確かめる観点と条項の探し方をまとめる

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 (各提供元の条項は、下の表から辿る geo-software-infra の reference が 2026-11-10 に確かめた内容による。本稿では規約の原文を読み直していない) |
| 根拠 (法令名と条、規約の版) | 法令ではなく各提供元との契約 (利用規約、サービス固有規約、ポリシー)。主な版: Google Maps Platform 利用規約 (Last modified 2026-08-26)、同サービス固有規約 (Last modified 2026-10-28)、Mapbox Product Terms (2026-10-20 版)、Esri Master Agreement E204 (2026-08-14 版) と Product-Specific Terms E300 (2025-11-13 版)、HERE Platform Terms (2022-01-18 発効版。最新版は 2026-11-10 に読めず)、CARTO Basemap Terms (2026-09-29 最終更新)、Stadia Maps 利用規約 (2026-11-09 発効)、MapFan API 利用規約 (2025-04-21 改訂)、Cesium ion 利用規約 (2025-08-20 主な改定)。版が書かれていない規約 (TomTom、MapTiler、ZENRIN Maps API、OpenFreeMap、OSM のタイル利用ポリシー、国土地理院、PLATEAU、EOX、NASA) は reference の確かめた日を版の代わりにする |
| 所管・管理者 | 各提供元 (下の表の reference の「運営主体」) |

## 何を求める決まりか

地図 API の規約は、提供元がデータとサーバを守り、課金の対象を確保するための契約である。法令と違って行政の手続は無く、守るべき相手は提供元である。条項の種類は大きく次の 3 つに分かれる。

- 禁止: キャッシュ・保存の禁止、他社地図との併用の禁止、機械学習への利用の禁止、地図からの抽出・トレースの禁止、帰属表示の改変・削除の禁止など。
- 表示: ロゴや著作権表示を出す義務 (帰属表示)。
- 承認・別契約: 書面の承認があれば許される (TomTom のベンチマーク、MapTiler の一括ダウンロード)、別の契約やプランが要る (車載用途、オフライン、政府案件)。

条項の種類ごとに、参照した reference のうちどの提供元に該当する条項があるかを下にまとめる。「記載なし」は reference に条項が見当たらないと書かれているか、reference に記述が無いことを指し、条項が無いことの保証ではない。

### キャッシュと保存

| 提供元 | 条項の要点 | 条項 | reference |
|---|---|---|---|
| Google Maps Platform | サービス固有規約が明示的に許す場合を除きキャッシュ禁止。事前取得、保存、再ホスト、一括ダウンロードも禁止。Geocoding の緯度経度は 30 日まで可、Map Tiles API にキャッシュを許す条項は無い | 利用規約 3.2.3(a)(b)、サービス固有規約、Map Tiles API policies | [google-maps.md](../../geo-software-infra/references/providers/google-maps.md) (https://cloud.google.com/maps-platform/terms) |
| Mapbox | 原則禁止。Mapping API の地図コンテンツはリクエストした端末に限り 30 日まで可 | Product Terms 1.9、2.8.1 | [mapbox.md](../../geo-software-infra/references/providers/mapbox.md) (https://www.mapbox.com/legal/product-terms) |
| HERE | Platform 外のキャッシュは 30 日まで。日本の HERE Content は 24 時間まで | 6.4(f)(g) (2022 年版) | [here.md](../../geo-software-infra/references/providers/here.md) (https://www.here.com/en-gb/terms/here-platform-terms-january-2022) |
| TomTom | 原則禁止。Cache-Control の max-age の範囲でクライアント内に限り可、複数の利用者に配るキャッシュは不可 | 11.4、11.6.12 | [tomtom.md](../../geo-software-infra/references/providers/tomtom.md) (https://docs.tomtom.com/legal/terms-and-conditions) |
| Esri | スクレイピング、ダウンロード、保存は原則禁止。ジオコード結果の保存は有料 | Master Agreement 3.2 c、E300 脚注 66 | [esri-arcgis-location-platform.md](../../geo-software-infra/references/providers/esri-arcgis-location-platform.md) (https://www.esri.com/en-us/legal/terms/full-master-agreement) |
| CARTO | 端末での 30 日超のキャッシュ、サーバ側のキャッシュ、一括ダウンロードは禁止 | 9.c | [carto-basemaps.md](../../geo-software-infra/references/providers/carto-basemaps.md) (https://carto.com/legal/basemap-terms/) |
| MapTiler | エンドユーザーの一時キャッシュは可、サーバ側キャッシュは禁止 | Cloud 特別規約 5.7、7.2 | [maptiler.md](../../geo-software-infra/references/providers/maptiler.md) (https://www.maptiler.com/cloud/terms/) |
| Stadia Maps | クライアント側は HTTP ヘッダの期間まで可、サーバ側キャッシュと一括ダウンロードは禁止 | 8 条 | [stadia-maps.md](../../geo-software-infra/references/providers/stadia-maps.md) (https://stadiamaps.com/terms-of-service/) |
| MapFan API | 複製は禁止。複製オプション契約中に限り社内ネットワーク内で可 | 第 4 条第 2 項・第 8 項 | [mapfan-api.md](../../geo-software-infra/references/providers/mapfan-api.md) (https://api-auth.mapfan.com/terms/mfapi_terms.pdf) |
| ZENRIN Maps API | 端末に保存できるのは ZID と「保存可能データ」に限る。地図データの複製は禁止 | 利用条件第 7 条、地図使用規約 | [zenrin-maps-api.md](../../geo-software-infra/references/providers/zenrin-maps-api.md) (https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html) |
| tile.openstreetmap.org | キャッシュヘッダに従う。オフライン保存と先読みは禁止 | Tile Usage Policy | [tile-openstreetmap-org.md](../../geo-software-infra/references/providers/tile-openstreetmap-org.md) (https://operations.osmfoundation.org/policies/tiles/) |
| Cesium ion | 一般的なクライアント側・プロキシのキャッシュに限り可。Google のコンテンツは原則キャッシュ不可 | 利用規約 2.2.2、Google データの条件 | [cesium-ion.md](../../geo-software-infra/references/3d/cesium-ion.md) (https://cesium.com/legal/terms-of-service/) |
| 国土地理院タイル | キャッシュの明文の規定は見当たらない。基本測量成果の複製・加工は測量法第 29 条・第 30 条の承認申請が要る場合がある | 測量法、コンテンツ利用規約 | [gsi-tiles.md](../../geo-software-infra/references/providers/gsi-tiles.md) (https://www.gsi.go.jp/LAW/2930-index.html) |

### 他社の地図との併用、スタイルや SDK の組み合わせ

| 提供元 | 条項の要点 | 条項 | reference |
|---|---|---|---|
| Google Maps Platform | Google Maps Core Services を Google 以外の地図と一緒に、又は近くで使ってはならない | 利用規約 3.2.3(e) | [google-maps.md](../../geo-software-infra/references/providers/google-maps.md) |
| HERE | HERE 以外のデータを HERE Content と組み合わせて提供することを原則禁止。出どころが区別できる重ね合わせは可 | 6.4(a) (2022 年版) | [here.md](../../geo-software-infra/references/providers/here.md) |
| TomTom | SDK は同等の第三者 API と一緒に使えない。第三者データと組み合わせた二次データベースの作成は禁止 | 4.2、11.6.1 | [tomtom.md](../../geo-software-infra/references/providers/tomtom.md) |
| Mapbox | Studio スタイルを Mapbox 以外の地図に使うことは禁止。他社地図を同じ画面に並べることを直接禁じる条項は見当たらない | Product Terms 2.11 | [mapbox.md](../../geo-software-infra/references/providers/mapbox.md) |
| Esri | Basemap Styles は Location Platform の Basemap Services 以外と使えない。他社地図の重ね合わせの明示的な禁止は見つからない | E300 脚注 109 | [esri-arcgis-location-platform.md](../../geo-software-infra/references/providers/esri-arcgis-location-platform.md) |
| Cesium ion | Google のコンテンツは Google 以外の地図と同じアプリで併用不可 | Google データの条件 | [cesium-ion.md](../../geo-software-infra/references/3d/cesium-ion.md) (https://cesium.com/legal/terms-for-google/) |
| CARTO、MapTiler、Stadia Maps、MapFan API、ZENRIN Maps API、OpenFreeMap、国土地理院、tile.openstreetmap.org、Geolonia Maps | 併用を禁じる条項は reference の調べた範囲で見当たらない | - | 各 reference |

### 機械学習・解析への利用、データの抽出

| 提供元 | 条項の要点 | 条項 | reference |
|---|---|---|---|
| Google Maps Platform | Google Maps Content を元にしたコンテンツの作成 (衛星画像のトレース、AI モデルの訓練・評価など) を禁止 | 利用規約 3.2.3(c) | [google-maps.md](../../geo-software-infra/references/providers/google-maps.md) |
| Mapbox | 地図コンテンツやサービスで機械学習・AI を訓練することを禁止。トレース・抽出も禁止 | Product Terms 1.5、1.6 | [mapbox.md](../../geo-software-infra/references/providers/mapbox.md) |
| Esri | Software と Online Services の外で AI/ML の学習に使うことを禁止。画像サービスの深層学習などの機械的な大量利用も禁止 | Master Agreement 3.3 h、E300 脚注 96 | [esri-arcgis-location-platform.md](../../geo-software-infra/references/providers/esri-arcgis-location-platform.md)、[esri-world-imagery.md](../../geo-software-infra/references/imagery/esri-world-imagery.md) |
| TomTom | 製品を不要にするような ML/AI の処理と、公開の参照データセットに取り込む形の ML/AI 利用を禁止 | 11.6.3、11.6.4 | [tomtom.md](../../geo-software-infra/references/providers/tomtom.md) |
| ZENRIN Maps API | AI モデルや機械学習への利用、生成 AI の成果物作成への利用、他の地図の精度向上への利用を禁止 | 利用条件第 8 条 | [zenrin-maps-api.md](../../geo-software-infra/references/providers/zenrin-maps-api.md) |
| Cesium ion | 明示の許可がない限り AI モデルの学習への利用を禁止 | 利用規約 2.2.4(xiii) | [cesium-ion.md](../../geo-software-infra/references/3d/cesium-ion.md) |
| HERE | HERE Content をもとにした地理データベースや POI データベースの作成を禁止 (機械学習の明示的な条項は reference に記載なし) | 6.4(e) (2022 年版) | [here.md](../../geo-software-infra/references/providers/here.md) |
| MapTiler | 派生ベクトルデータセットの作成は非商用か OSM 向けに限り可 | 一般規約 4.3 | [maptiler.md](../../geo-software-infra/references/providers/maptiler.md) (https://www.maptiler.com/terms/) |
| EOX (EOxCloudless) | AI の学習データ化について、商用ライセンス本文と FAQ に明示の規定はない (reference で未確認) | - | [eox-s2cloudless.md](../../geo-software-infra/references/imagery/eox-s2cloudless.md) |
| NASA GIBS、PLATEAU | NASA 主導ミッションのデータは CC0、PLATEAU は公共データ利用規約 第 1.0 版で、解析・加工を禁じる条項は reference に見当たらない | - | [nasa-gibs.md](../../geo-software-infra/references/imagery/nasa-gibs.md)、[plateau.md](../../geo-software-infra/references/3d/plateau.md) |

### ベンチマーク・比較の公表

| 提供元 | 条項の要点 | 条項 | reference |
|---|---|---|---|
| TomTom | 競合製品と並べた比較・ベンチマークは書面の承認が必要 | 11.6.10 | [tomtom.md](../../geo-software-infra/references/providers/tomtom.md) |
| Mapbox | Mapbox と競合するサービスの開発・ベンチマークに使うことを禁止 | Product Terms 1.5 | [mapbox.md](../../geo-software-infra/references/providers/mapbox.md) |
| その他の提供元 | reference に記載なし (条項の有無は未確認) | - | 各 reference |

### 表示 (帰属表示、ロゴ) の改変

| 提供元 | 条項の要点 | 条項 | reference |
|---|---|---|---|
| Google Maps Platform | 帰属表示を改変・隠蔽・削除せずに表示。Map Tiles API では Google Maps のロゴと集約した帰属表示を出し、他のレンダラーのロゴを重ねない | 利用規約 3.2.2(b)、Map Tiles API policies | [google-maps.md](../../geo-software-infra/references/providers/google-maps.md) |
| Mapbox | Mapbox ロゴ、© Mapbox、© OpenStreetMap、Improve this map が必須 | Product Terms 1.4 | [mapbox.md](../../geo-software-infra/references/providers/mapbox.md) |
| HERE | マークと著作権表示の削除・隠蔽を禁止、HERE Content の改変を禁止 | 13.1、6.4(c)(i) (2022 年版) | [here.md](../../geo-software-infra/references/providers/here.md) |
| TomTom | 自動で出るロゴや著作権表示を消したり隠したりしない。それ以外は Copyright API で表示 | 17.3 | [tomtom.md](../../geo-software-infra/references/providers/tomtom.md) |
| Esri | 「Powered by Esri」とデータ提供元を常に見える位置に表示 | Esri の帰属表示の文書 | [esri-arcgis-location-platform.md](../../geo-software-infra/references/providers/esri-arcgis-location-platform.md) |
| MapTiler | 帰属表示が必要。製品識別や権利表示の改変・削除は禁止 | Cloud 特別規約 5.4、7.5 | [maptiler.md](../../geo-software-infra/references/providers/maptiler.md) |
| Stadia Maps、CARTO、tile.openstreetmap.org | 帰属表示を隠すことの禁止、又は目立つ形での表示 | Stadia 8 条、CARTO 13 条、Tile Usage Policy | 各 reference |
| Cesium ion | Cesium ion ロゴをメイン画面に目立つ形で表示 | 利用規約 2.2.3 | [cesium-ion.md](../../geo-software-infra/references/3d/cesium-ion.md) |
| 国土地理院、PLATEAU | 加工した場合はその旨を記載し、国が作成したように見せてはならない | 国土地理院コンテンツ利用規約、PLATEAU サイトポリシー | [gsi-tiles.md](../../geo-software-infra/references/providers/gsi-tiles.md)、[plateau.md](../../geo-software-infra/references/3d/plateau.md) |
| MapFan API | 「地図閲覧利用規約」と著作権表記『© GeoTechnologies, Inc.』を表示 | 第 4 条第 1 項 | [mapfan-api.md](../../geo-software-infra/references/providers/mapfan-api.md) |
| ZENRIN Maps API | 著作権表示の義務の条文は見当たらないが、ユーザーに「地図使用規約」を掲載して同意を得る義務がある | 利用条件第 8 条 | [zenrin-maps-api.md](../../geo-software-infra/references/providers/zenrin-maps-api.md) |

### オフライン利用

| 提供元 | 条項の要点 | reference |
|---|---|---|
| Google Maps Platform (Map Tiles API) | オフライン用途を含む可視化以外の用途に使えない | [google-maps.md](../../geo-software-infra/references/providers/google-maps.md) |
| tile.openstreetmap.org | オフライン利用は不可 | [tile-openstreetmap-org.md](../../geo-software-infra/references/providers/tile-openstreetmap-org.md) |
| Mapbox | モバイル SDK のオフライン機能 (タイルパック 750 個まで) | [mapbox.md](../../geo-software-infra/references/providers/mapbox.md) |
| Esri | Esri Content Packages による ArcGIS のネイティブ SDK・Desktop・Pro に限る | [esri-arcgis-location-platform.md](../../geo-software-infra/references/providers/esri-arcgis-location-platform.md) |
| Stadia Maps | モバイルで端末あたり同時 100MB まで | [stadia-maps.md](../../geo-software-infra/references/providers/stadia-maps.md) |
| OpenFreeMap | アプリ内のオフラインダウンロードは 1 回 3,000 タイルか 50MB まで | [openfreemap.md](../../geo-software-infra/references/providers/openfreemap.md) |
| MapTiler | Cloud は不可、On-Prem 製品で可 | [maptiler.md](../../geo-software-infra/references/providers/maptiler.md) |
| HERE、TomTom | 別契約の SDK の範囲 | [here.md](../../geo-software-infra/references/providers/here.md)、[tomtom.md](../../geo-software-infra/references/providers/tomtom.md) |
| Cesium ion | データ出力をオフライン向けに複製・保存・再配布してはならない (Clips を除く)。Self-Hosted 製品あり | [cesium-ion.md](../../geo-software-infra/references/3d/cesium-ion.md) |

### 政府・公共案件での利用

| 提供元 | 条項の要点 | reference |
|---|---|---|
| Cesium ion | 無料の Community は政府開発の評価目的に限る。政府案件は有償の商用ライセンスが必要。政府機関が発注者の場合、ライセンスは注文書に記載した機関・部署に限る | [cesium-ion.md](../../geo-software-infra/references/3d/cesium-ion.md) (利用規約 1.23、https://cesium.com/platform/cesium-ion/pricing/) |
| その他の提供元 | 政府利用に特化した条項は reference に記載なし (条項の有無は未確認) | 各 reference |

### 地図に載せる動画・音楽の API (地図 API 以外)

地図の上に動画の埋め込みや音楽の試聴を並べるサービスでは、地図 API とは別の規約がかかる。条項の詳細は個別の reference に置く (2026-11-11 確認)。

| 提供元 | 条項の要点 | 条項 | reference |
|---|---|---|---|
| YouTube (埋め込みプレーヤー、Data API) | 埋め込みも YouTube API Services に含まれる。プレーヤーは 200 × 200px 以上、自動再生は 1 画面に同時に 1 つ、プレーヤーの上に要素を重ねない。動画の保存・キャッシュは書面の承認なしに禁止。認可なしの API Data の保存は 30 日まで、API Data から新しい指標を作らない、スクレイピングの禁止。帰属を隠さない | RMF、Policies III.E.1、III.E.4、III.E.6、III.F.2、III.I | [youtube-embed](youtube-embed.md) (https://developers.google.com/youtube/terms/developer-policies) |
| Apple (iTunes Search API) | 試聴とアートワークは元の内容の宣伝に限る。購入ページへ直接リンクするバッジの近くに置き、試聴には「provided courtesy of iTunes」。試聴はストリーミングだけで、ダウンロード・保存・キャッシュ禁止。独立の娯楽の価値のために使わない。1 分に約 20 回 | Search API の文書「Legal」(i) から (vi)、「Notes」 | [itunes-search-api](itunes-search-api.md) (https://performance-partners.apple.com/search-api) |

## 地図プロダクトで当たる場面

| 場面 | 当たるか | 根拠 | 出典 |
|---|---|---|---|
| タイルを自社サーバや CDN でキャッシュ・プロキシして配る | 多くの商用 API で禁止に当たる (Google、Mapbox、TomTom、CARTO、MapTiler、Stadia Maps、Esri)。キャッシュヘッダの範囲でのクライアント側キャッシュのみ許す提供元が多い | 上の「キャッシュと保存」の各条項 | 各 reference |
| Google の地図と、Google 以外の POI や地図を同じ画面に出す | Google 利用規約 3.2.3(e) に当たる | 同条 | [google-maps.md](../../geo-software-infra/references/providers/google-maps.md) |
| 衛星画像や地図から建物や道路をトレースしてデータを作る、地図を AI の学習データにする | Google、Mapbox、Esri、TomTom、ZENRIN、Cesium ion で禁止に当たる | 上の「機械学習・解析への利用」の各条項 | 各 reference |
| 複数の地図 API の速度や品質を比べた記事やスライドを公開する | TomTom は書面の承認が必要。Mapbox は競合サービスのためのベンチマークを禁止 | TomTom 11.6.10、Mapbox Product Terms 1.5 | 各 reference |
| ロゴや帰属表示を消す、小さくする、UI の裏に隠す | 多くの提供元で禁止に当たる | 上の「表示の改変」の各条項 | 各 reference |
| 自治体の受託案件で 3D 都市モデルを Cesium ion で配信する | 無料枠は使えず、有償の商用ライセンスが必要 | Cesium ion 料金ページ、利用規約 1.23 | [cesium-ion.md](../../geo-software-infra/references/3d/cesium-ion.md) |

## 当たらない場面

- Google のサービス固有規約は、Geocoding API などの緯度経度を 30 日までキャッシュすることと place_id の保存を許している。Geocoding API の緯度経度と住所は、利用者向けの機能のためだけに、利用者ごとに分けて保存するなら期限なしでもよい (6.3.2)。Places UI Kit は Google 以外の地図とも使える (15.1) (2026-10-28 版、2026-11-11 確認。[google-maps.md](../../geo-software-infra/references/providers/google-maps.md))。
- Mapbox の Mapping API の地図コンテンツは、リクエストした同じ端末に限り 30 日までキャッシュできる (Product Terms 2.8.1、[mapbox.md](../../geo-software-infra/references/providers/mapbox.md))。
- Esri は帰属表示つきの PDF や画像などの静的な地図表現を作成し報告書に使うことを認めている (Master Agreement 3.2 b、[esri-arcgis-location-platform.md](../../geo-software-infra/references/providers/esri-arcgis-location-platform.md))。
- 国土地理院のタイルをリアルタイムに読み込むウェブサイトやアプリは、営利・非営利を問わず出典の明示のみで申請不要 (国土地理院 Q&A Q1-12、[gsi-tiles.md](../../geo-software-infra/references/providers/gsi-tiles.md))。
- PLATEAU のデータはダウンロード、自前の変換・ホストが可能で、出典の表示 (加工時はその旨) で足りる ([plateau.md](../../geo-software-infra/references/3d/plateau.md))。
- NASA 主導ミッションのデータ (CC0) は複製、加工、解析、再配布に制限がない ([nasa-gibs.md](../../geo-software-infra/references/imagery/nasa-gibs.md))。

## 求められる手続き・表示

- 手続き (申請先、期間、費用): 規約上の承認や別契約が要る条項は、提供元の営業窓口か書面の合意で手当てする。例: TomTom のベンチマーク (書面の承認)、MapTiler の一括ダウンロード (書面の合意、Cloud 特別規約 6.3)、Cesium ion の政府案件 (有償ライセンス)、MapFan API の複製 (複製オプション契約)。国土地理院の基本測量成果の複製・加工は、規約ではなく測量法の承認申請で、「地図の利用手続ナビ」(https://service.gsi.go.jp/onestop/navi/index/) で要否を判断する。
- 条項の探し方: 規約の目次で次の見出しを探す。英語の規約は「Restrictions」「Prohibited uses」「Acceptable use」「License grant」「Attribution」「Caching」の節に集まっていることが多い (推測。reference で確かめた Google、Mapbox、TomTom の規約の構成からの一般化)。検索語は、キャッシュ・保存は cache、store、prefetch、bulk download、offline、proxy、保存、複製。併用は non-Google map、third-party map、combine、in conjunction with、併用。機械学習は machine learning、train、artificial intelligence、derive、trace、extract、学習、抽出。ベンチマークは benchmark、compare、competitive、比較。表示は attribution、logo、obscure、remove、帰属、著作権表示。政府利用は government、public sector、agency、政府。サービス全体の規約に加えて、サービス固有規約や API ごとのポリシー (Google の Map Tiles API policies、Mapbox の Product Terms、Esri の E300) を必ず開く。日本向けに別の規約がある場合がある (Mapbox の Japan Product Terms、HERE の日本の Content のキャッシュ制限)。
- 確かめること: (1) 規約の版と発効日、(2) 条項が全サービス共通か API ごとか、(3) 禁止か承認制か別契約か、(4) 許される範囲の数値 (日数、容量、タイル数)、(5) 契約終了後のデータの削除義務、(6) 自社の配布形態 (SaaS、受託納品、オフライン) で当たる条項。
- 表示の書き方 (公式の例): 帰属表示の文言は提供元ごとに異なるので、各 reference の「帰属表示の要件」に書かれた公式の例に従う (例: Mapbox は © Mapbox と © OpenStreetMap にリンクを付ける、Esri は「Powered by Esri」とデータ提供元)。

## 守らなかった場合

- 規約上の措置として reference に記載があるもの: 過負荷をかける利用は予告なく停止されうる (Mapbox Product Terms 1.8)。プランの上限超過や他の顧客の利用を妨げた場合は停止されうる (TomTom 14.2.2、14.2.8)。一括ダウンロードなどポリシーに反する利用は予告なく遮断され、繰り返すとネットワーク単位の長期遮断もありうる (tile.openstreetmap.org Tile Usage Policy)。サーバに負荷をかける通信は予告なく遮断される場合がある (地理院地図の利用規約)。過大な負荷のリクエストは遮断されうる (MapFan API 第 11 条第 5 項)。当社が適当でないと判断した場合に事前通知なく利用を制限できる (Geolonia 利用規約第 6 条)。契約終了時は地図コンテンツとバックアップを削除する義務がある (MapTiler 一般規約 12.5)。契約終了後は Cesium のデータ出力を表示・利用できない (Cesium ion 利用規約 2.2)。
- 損害賠償や契約解除の条項は本稿では確かめていない。

## 判断に迷う点

- 規約に書かれていないことが許されるとは限らない。たとえば国土地理院タイルはキャッシュの明文の規定が無いが、基本測量成果の複製・加工には測量法の手続が要る場合がある ([gsi-tiles.md](../../geo-software-infra/references/providers/gsi-tiles.md))。
- 同じ提供元でも、規約の版の取り違えに注意が要る。HERE は最新版の URL が 2026-11-10 に読めず、2022 年版で確かめている ([here.md](../../geo-software-infra/references/providers/here.md))。
- データのライセンス (ODbL、CC BY など) と提供元の規約は別の層で、両方を満たす必要がある。OSM 由来のタイルからデータを抽出すると ODbL の継承条件がかかるが、多くの提供元は規約で抽出自体を禁じている (各 reference の「ライセンス上の注意」)。

## 出典

- [../../geo-software-infra/references/providers/google-maps.md](../../geo-software-infra/references/providers/google-maps.md) : https://cloud.google.com/maps-platform/terms 、https://cloud.google.com/maps-platform/terms/maps-service-terms 、https://developers.google.com/maps/documentation/tile/policies
- [../../geo-software-infra/references/providers/mapbox.md](../../geo-software-infra/references/providers/mapbox.md) : https://www.mapbox.com/legal/product-terms
- [../../geo-software-infra/references/providers/here.md](../../geo-software-infra/references/providers/here.md) : https://www.here.com/en-gb/terms/here-platform-terms-january-2022
- [../../geo-software-infra/references/providers/tomtom.md](../../geo-software-infra/references/providers/tomtom.md) : https://docs.tomtom.com/legal/terms-and-conditions
- [../../geo-software-infra/references/providers/esri-arcgis-location-platform.md](../../geo-software-infra/references/providers/esri-arcgis-location-platform.md) : https://www.esri.com/en-us/legal/terms/full-master-agreement 、https://www.esri.com/content/dam/esrisites/en-us/media/legal/product-specific-terms-of-use/e300.pdf
- [../../geo-software-infra/references/providers/carto-basemaps.md](../../geo-software-infra/references/providers/carto-basemaps.md) : https://carto.com/legal/basemap-terms/
- [../../geo-software-infra/references/providers/maptiler.md](../../geo-software-infra/references/providers/maptiler.md) : https://www.maptiler.com/cloud/terms/ 、https://www.maptiler.com/terms/
- [../../geo-software-infra/references/providers/stadia-maps.md](../../geo-software-infra/references/providers/stadia-maps.md) : https://stadiamaps.com/terms-of-service/
- [../../geo-software-infra/references/providers/mapfan-api.md](../../geo-software-infra/references/providers/mapfan-api.md) : https://api-auth.mapfan.com/terms/mfapi_terms.pdf
- [../../geo-software-infra/references/providers/zenrin-maps-api.md](../../geo-software-infra/references/providers/zenrin-maps-api.md) : https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html 、https://developers.zmaps-api.com/document/Terms_of_Use_for_Map.html
- [../../geo-software-infra/references/providers/openfreemap.md](../../geo-software-infra/references/providers/openfreemap.md) : https://openfreemap.org/tos/
- [../../geo-software-infra/references/providers/tile-openstreetmap-org.md](../../geo-software-infra/references/providers/tile-openstreetmap-org.md) : https://operations.osmfoundation.org/policies/tiles/
- [../../geo-software-infra/references/providers/tile-openstreetmap-jp.md](../../geo-software-infra/references/providers/tile-openstreetmap-jp.md) : 専用の利用規約は未確認
- [../../geo-software-infra/references/providers/gsi-tiles.md](../../geo-software-infra/references/providers/gsi-tiles.md) : https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html 、https://maps.gsi.go.jp/help/termsofuse.html 、https://www.gsi.go.jp/LAW/2930-qa.html
- [../../geo-software-infra/references/providers/geolonia-maps.md](../../geo-software-infra/references/providers/geolonia-maps.md) : https://www.geolonia.com/terms/
- [../../geo-software-infra/references/imagery/eox-s2cloudless.md](../../geo-software-infra/references/imagery/eox-s2cloudless.md) : https://cloudless.eox.at/license-legal/
- [../../geo-software-infra/references/imagery/esri-world-imagery.md](../../geo-software-infra/references/imagery/esri-world-imagery.md) : https://www.esri.com/en-us/legal/terms/full-master-agreement
- [../../geo-software-infra/references/imagery/nasa-gibs.md](../../geo-software-infra/references/imagery/nasa-gibs.md) : https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance
- [../../geo-software-infra/references/3d/cesium-ion.md](../../geo-software-infra/references/3d/cesium-ion.md) : https://cesium.com/legal/terms-of-service/ 、https://cesium.com/legal/terms-for-google/
- [../../geo-software-infra/references/3d/plateau.md](../../geo-software-infra/references/3d/plateau.md) : https://www.mlit.go.jp/plateau/site-policy/

## 未確認のこと

- ベンチマークの公表と政府利用の条項は、TomTom、Mapbox、Cesium ion 以外の提供元について reference に記載が無く、条項の有無を確かめていない。
- 機械学習への利用について、CARTO、MapTiler、Stadia Maps、MapFan API、OpenFreeMap、EOX の規約に明示の条項があるか。
- HERE の現行版の規約 (https://legal.here.com/en/terms/here-platform) と 2022 年版の差分。
- 各規約の損害賠償、契約解除、準拠法の条項。
- 規約の英語版と日本語版が両方ある提供元で、どちらが優先するか。
- OSMFJ のタイル (tile.openstreetmap.jp) の利用条件。専用の規約が見つかっていない。
