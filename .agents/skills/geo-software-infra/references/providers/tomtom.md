# TomTom Maps API

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | TomTom N.V. (オランダ、アムステルダム本拠の上場企業、ティッカー TOM2)。SDK のライセンス主体は TomTom Global Content B.V. (https://www.vfb.be/Media/Default/pdf/TOMTOM%20-%20Annual%20Report%202025.pdf 、https://stockanalysis.com/quote/ams/TOM2/transcripts/ 、npm パッケージ @tomtom-org/maps-sdk 1.0.0 の LICENSE.txt) |
| 公式サイト | https://docs.tomtom.com/ (旧 Developer Portal の developer.tomtom.com から移行。アカウント管理は https://my.tomtom.com/) |
| 料金ページ | https://docs.tomtom.com/pricing |
| 利用規約・利用ポリシー | https://docs.tomtom.com/legal/terms-and-conditions 、非推奨化の方針 https://docs.tomtom.com/deprecation-policy/overview |

## 概要

TomTom Maps API は、地図表示 (Map Display API のベクトルタイル・ラスタタイル)、ルート検索、ジオコーディング、Places 検索、交通情報などを REST で提供するサービスである (https://docs.tomtom.com/pricing)。現在の地図基盤は TomTom Orbis Maps で、Overture Maps、OpenStreetMap、TomTom 独自データを組み合わせている (https://docs.tomtom.com/tomtom-orbis-maps/documentation/introduction)。新規の API と機能は Orbis 上に作られ、旧世代の「TomTom Maps」系 API は支持は続くが一部が非推奨になっている (https://docs.tomtom.com/pricing)。Web 向けの新しい SDK (TomTom Maps SDK for JavaScript) は MapLibre GL JS の上に作られている (https://docs.tomtom.com/maps-sdk-js/)。

## 地図データ

- データの出どころ (自社調査 / OSM / 公的データ / 他社からのライセンス): Orbis Maps は Overture Maps の基盤データ、品質基準を満たす範囲で選択的に使う OpenStreetMap、TomTom 独自データ (住所点、制限速度、交通規制、速度プロファイル、交通標識)、提携先とセンサー由来の観測、顧客データ (BYOD) を組み合わせる。ODbL のオープンデータと TomTom の独自データが混在し、属性ごとにライセンス情報が付く (https://docs.tomtom.com/tomtom-orbis-maps/documentation/introduction)。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): 未確認。Orbis のジオコーディング API (v1、v2) と Search API の対応国一覧のアジア太平洋の表に日本が載っていない (2026-11-10 確認、https://docs.tomtom.com/geocoding-api/documentation/tomtom-orbis-maps/v2/product-information/market-coverage 、https://docs.tomtom.com/geocoding-api/documentation/tomtom-orbis-maps/v1/product-information/market-coverage 、https://docs.tomtom.com/search-api/documentation/tomtom-orbis-maps/product-information/market-coverage)。日本の住所検索は Orbis では提供されていないと読める。一方、Orbis の Routing API v2 は日本でルート計算とリアルタイム交通の両方に対応している (https://docs.tomtom.com/routing-api/documentation/tomtom-orbis-maps/v2/product-information/market-coverage)。背景地図の日本部分の詳しさ (建物、注記など) を示す公式資料は見つからなかった。
- 全球の対応: 235 以上の国と地域 (https://docs.tomtom.com/tomtom-orbis-maps/documentation/introduction)。
- 更新頻度: 「継続的に更新」とあるが周期は書かれていない (https://docs.tomtom.com/tomtom-orbis-maps/documentation/introduction)。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | Map Display API Raster Tiles (Orbis と旧 TomTom Maps の両方)。衛星と陰影起伏もラスタタイルの別エンドポイント (https://docs.tomtom.com/map-display-api/documentation/tomtom-orbis-maps/v2/product-information/introduction) |
| ベクトルタイル (形式、スキーマ) | あり | `https://api.tomtom.com/maps/orbis/display/vector/tile/{z}/{x}/{y}.pbf?apiVersion=2&key=...`。`application/vnd.mapbox-vector-tile` (MVT)、ズーム 0〜22、extent 4096。スキーマは TomTom 独自で、提供レイヤは `basic` のみ (https://docs.tomtom.com/map-display-api/documentation/tomtom-orbis-maps/v2/vector/tile) |
| スタイルの編集・カスタマイズ | あり | 既定スタイルは street-light、street-light_driving、street-dark、street-dark_driving、mono-light、mono-dark、street-satellite。Assets API が MapLibre Style Specification に沿ったスタイル、スプライト、フォントを返し、それを元にカスタマイズする (https://docs.tomtom.com/map-display-api/ 、https://developer.tomtom.com/assets-api/documentation/tomtom-orbis-maps/product-information/introduction) |
| 衛星・航空写真 | あり | Satellite Tile エンドポイント。画像の出どころと解像度は未確認 |
| 地形・3D 建物 | 一部あり | 陰影起伏 (Hillshade Tile) はある。3D 建物は Map Display API の文書に記載が見つからない (https://docs.tomtom.com/map-display-api/documentation/tomtom-orbis-maps/v2/product-information/introduction) |
| ジオコーディング / 逆ジオコーディング | あり (日本は対象外) | 各月 2 万件無料。Orbis 版の対応国一覧に日本がない (上記) |
| ルート検索 | あり | 月 2 万件無料。Orbis Routing API v2 は日本に対応 (上記) |
| オフライン利用 | なし (API 経由) | 規約 11.4 で、結果のキャッシュは Cache-Control の max-age の範囲でクライアント内に限られ、複数の利用者に配るためのキャッシュは認められない (https://docs.tomtom.com/legal/terms-and-conditions)。オフライン地図は Navigation SDK など別契約の製品の範囲で、未確認 |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): Web は TomTom Maps SDK for JavaScript (npm `@tomtom-org/maps-sdk`、2026-11-10 時点の最新は 1.0.0、依存に `maplibre-gl` ^6.15.0)。MapLibre GL JS の上に作られ、MapLibre の Map オブジェクトをそのまま操作できる (https://docs.tomtom.com/maps-sdk-js/ 、`npm view @tomtom-org/maps-sdk` で確認)。旧 SDK の `@tomtom-international/web-sdk-maps` (最新 6.25.0) は mapbox-gl 1.13.2 に依存している (`npm view` で確認)。Android は Navigation SDK などがある (https://docs.tomtom.com/pricing)。iOS 向けの地図 SDK の現状は未確認。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 技術的には使える。ベクトルタイルは MapLibre Style Specification 互換のレンダラーで使う前提で文書化され、CORS は全オリジンに開いている (https://docs.tomtom.com/map-display-api/documentation/tomtom-orbis-maps/v2/vector/tile)。ラスタタイルは XYZ 形式なので Leaflet や OpenLayers でも表示できる (推測。公式の手順書は確認していない)。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): SDK は TomTom の API と組み合わせて使う必要があり、同等の第三者 API と一緒に使ってはならない (API 規約 4.2、SDK ライセンス 1 条)。API 側には特定の SDK でしか表示してはならないという規定は見つからなかった。ただし規約 11.6.10 は、TomTom の製品を競合製品と並べて検証・比較・ベンチマークすることを書面の承認なしに禁じている (https://docs.tomtom.com/legal/terms-and-conditions)。
- API キー・アカウントの要否: 必要。MyTomTom (https://my.tomtom.com/) で登録して API キーを得る。無料枠の利用にクレジットカードは要らない (https://docs.tomtom.com/pricing)。

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): API ごとのリクエスト数。地図表示はタイル 1 枚が 1 リクエスト (https://docs.tomtom.com/pricing)。
- 無料枠: 毎月、API ごとに、Map Display ベクトルタイル (Orbis) 20 万、ラスタタイル 20 万、ラスタの非タイル (静的画像など) 2 万、Routing 2 万、Geocoding 2 万、Reverse Geocoding 2 万、Places Search Suggest 1 万、Places Search Details と Discover 各 5,000、旧 Search API 2,500 など (2026-11-10 確認、https://docs.tomtom.com/pricing 、https://docs.tomtom.com/pricing/price-announcement)。超えると 429 が返る (https://docs.tomtom.com/platform/documentation/status-and-support/faqs)。
- 従量単価 (主な API ごとに、通貨と確かめた日つき。問い合わせ制ならそう書き、金額を推測しない): 料金ページの計算機 (「Pricing details」) が表示する単価を、同ページが読み込む公開スクリプト (https://docs.tomtom.com/_astro/PricingCalculatorV2.sYFTf1he.js) から読んだ値。2026-11-10 確認、ユーロ、1,000 リクエストあたり。ベクトルタイルは 1,000 万まで 0.10 EUR、1,000 万〜5,000 万が 0.08 EUR、5,000 万〜1 億が 0.07 EUR、1 億超は Enterprise (個別見積もり)。ラスタタイルは同じ区切りで 0.25 / 0.20 / 0.16 EUR。Routing、Geocoding、Reverse Geocoding、ラスタの非タイルは 100 万まで 1.00 EUR、100 万〜500 万が 0.80 EUR、500 万〜1,000 万が 0.65 EUR、1,000 万超は Enterprise。EU は EUR、それ以外の地域は USD で請求する (https://docs.tomtom.com/platform/documentation/status-and-support/faqs)。USD の単価は計算機が為替係数で換算しており、固定の USD 単価は確かめていない。
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式と仮定を書く。単価が非公開なら「算出しない」): 仮定は「1 地図ロードあたりベクトルタイル 15 枚 (推測。画面サイズ、ズーム操作で変わる)」、「衛星やラスタは使わない」、「スタイル・スプライト・フォントの取得は課金対象に含めない (未確認)」。10 万ロードは 150 万タイルで、(1,500,000 − 200,000) ÷ 1,000 × 0.10 = 130 EUR。100 万ロードは 1,500 万タイルで、(10,000,000 − 200,000) ÷ 1,000 × 0.10 + (15,000,000 − 10,000,000) ÷ 1,000 × 0.08 = 980 + 400 = 1,380 EUR。1,000 万ロードは 1 億 5,000 万タイルで 1 億を超え Enterprise の個別見積もりになるため算出しない (参考までに 1 億タイルまでの部分は 980 + 3,200 + 3,500 = 7,680 EUR)。
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): 無料 (Freemium)、Pay As You Grow (前払いなしの従量課金、セルフサーブ)、Enterprise (個別見積もり) の 3 段階 (https://docs.tomtom.com/pricing)。Pay As You Grow はカードでのチャージ (top-up) と請求書のダウンロードに対応する。Pay As You Grow と Freemium は 1 ユーザーのみで、複数ユーザーは Enterprise 契約が必要 (https://docs.tomtom.com/platform/documentation/status-and-support/faqs)。

## 利用規約上の制約

以下の条番号は https://docs.tomtom.com/legal/terms-and-conditions のもの (2026-11-10 確認)。

- 商用利用: 可。Subscription Plan の範囲で「Permitted Solution」に使うライセンスが与えられる (2.1)。車載用途とナビゲーション機能は別の書面契約が必要 (2.1)。
- アクセス量の上限・公正利用の条件: QPS の上限は API ごとに 5〜50 (https://docs.tomtom.com/platform/documentation/status-and-support/faqs)。プランの上限を超えた場合や他の顧客の利用を妨げた場合は停止されうる (14.2.2、14.2.8)。無料枠の未使用分は月末で失効し繰り越さない (8.5)。
- キャッシュ・オフライン保存: 結果のキャッシュと保存は原則禁止。例外として、Cache-Control ヘッダがある結果をその max-age を超えない範囲でクライアントにキャッシュできる。複数のクライアントや利用者に配る目的のキャッシュは認められない (11.4)。ダウンロード型の地図データ (pbf など) は 90 日を超えて保持できない (11.6.12)。
- 帰属表示の要件: TomTom のロゴや著作権表示を自動で出す API ではそれを消したり隠したりしてはならず、それ以外の API では Copyright API を使って著作権表示とロゴを出す (17.3)。Map Display API には Copyrights エンドポイントがある (https://docs.tomtom.com/map-display-api/documentation/tomtom-orbis-maps/v2/product-information/introduction)。
- 他社の地図との併用、データの持ち出しの制限: 取得したデータから派生物、競合するデータベースやサービス、第三者データと組み合わせた二次データベースを作ってはならない (11.6.1)。製品を不要にするような ML/AI の処理にかけてはならず、公開の参照データセットに取り込む形で ML/AI に使ってはならない (11.6.3、11.6.4)。競合製品と並べた比較・ベンチマークは書面の承認が必要 (11.6.10)。SDK は同等の第三者 API と一緒に使えない (4.2)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): 2 点ある。(1) データの ODbL。Orbis のデータには ODbL のデータが含まれ、その部分には ODbL 以外の制限は適用されない (3.1.4)。利用者は求めに応じて TomTom から ODbL データを受け取れ、自社サービスの顧客から求められた場合も TomTom に請求できる (3.1.2)。一方で、TomTom の非 ODbL データを ODbL データなどと組み合わせて非 ODbL 部分が ODbL に服するようにしてはならず、ODbL データを第三者データと組み合わせて第三者データを ODbL に服させてもならない (3.1.5)。タイルを表示するだけ (SaaS で画面に出す) なら帰属表示で足りるが、データを抽出して DB を作り配布すると ODbL の継承条件と規約 11.6.1 の両方にかかる。(2) SDK は OSS ではない。`@tomtom-org/maps-sdk` と旧 `@tomtom-international/web-sdk-maps` の npm 上の license は「SEE LICENSE IN LICENSE.txt」で、中身は TomTom 独自の SDK ライセンス (2026-10 版) であり OSI 承認ライセンスではない。TomTom API と組み合わせて Web やモバイルのアプリを作る範囲でのみ使え、再配布・改変の権利は同ライセンスの条件に従う。内部で使う MapLibre GL JS は BSD-3-Clause でコピーレフトはない。

## 安定性と運用

- SLA: Pay As You Grow 向けの SLA は公開文書に見つからなかった。規約 20.1 は無停止・無誤りを保証しないとしている (https://docs.tomtom.com/legal/terms-and-conditions)。Enterprise 契約での SLA は個別契約で、内容は未確認。
- 運営の継続性 (運営主体、資金源): TomTom N.V. は上場企業で、事業は Location Technology (Automotive と Enterprise) と Consumer の 2 区分。2025 年の Location Technology の売上は 4 億 8,200 万 EUR (2025 年次報告書、https://www.vfb.be/Media/Default/pdf/TOMTOM%20-%20Annual%20Report%202025.pdf)。Overture Maps Foundation の共同設立者でもある (https://docs.tomtom.com/tomtom-orbis-maps/documentation/introduction)。
- 障害情報の公開先: https://tomtom.service-now.com/status (API ごとの状態と過去 5 日分の履歴、https://docs.tomtom.com/platform/documentation/status-and-support/api-status-page)。

## 向いている場面

- MapLibre GL JS ベースの SDK で、背景地図、ルート検索、リアルタイム交通情報を 1 社でまとめたい場合。日本でも Orbis のルート計算とリアルタイム交通は提供されている。
- 欧州・北米など、TomTom が住所点や道路属性を持つ地域を主な対象にするアプリ。
- 無料枠 (タイル月 20 万) を超えても前払いなしで段階的に単価が下がる従量課金を使いたい場合。

## 向いていない場面

- 日本の住所検索 (ジオコーディング) が必要な場合。Orbis のジオコーディングと Search の対応国一覧に日本がない。
- タイルを自前の CDN やサーバーでキャッシュして複数利用者に配りたい、オフラインで持ち込みたい場合。規約 11.4 で禁じられている。
- 地図サービスを並べて比較・ベンチマークし、その結果を公表したい場合。規約 11.6.10 で書面の承認が必要。
- 書面の SLA がセルフサーブ契約で必要な場合。

## 出典

- https://docs.tomtom.com/
- https://my.tomtom.com/
- https://docs.tomtom.com/pricing
- https://docs.tomtom.com/pricing/price-announcement
- https://docs.tomtom.com/_astro/PricingCalculatorV2.sYFTf1he.js
- https://docs.tomtom.com/legal/terms-and-conditions
- https://docs.tomtom.com/deprecation-policy/overview
- https://docs.tomtom.com/tomtom-orbis-maps/documentation/introduction
- https://docs.tomtom.com/map-display-api/
- https://docs.tomtom.com/map-display-api/documentation/tomtom-orbis-maps/v2/product-information/introduction
- https://docs.tomtom.com/map-display-api/documentation/tomtom-orbis-maps/v2/vector/tile
- https://developer.tomtom.com/assets-api/documentation/tomtom-orbis-maps/product-information/introduction
- https://docs.tomtom.com/geocoding-api/documentation/tomtom-orbis-maps/v2/product-information/market-coverage
- https://docs.tomtom.com/geocoding-api/documentation/tomtom-orbis-maps/v1/product-information/market-coverage
- https://docs.tomtom.com/search-api/documentation/tomtom-orbis-maps/product-information/market-coverage
- https://docs.tomtom.com/routing-api/documentation/tomtom-orbis-maps/v2/product-information/market-coverage
- https://docs.tomtom.com/maps-sdk-js/
- https://www.npmjs.com/package/@tomtom-org/maps-sdk
- https://www.npmjs.com/package/@tomtom-international/web-sdk-maps
- https://docs.tomtom.com/platform/documentation/status-and-support/faqs
- https://docs.tomtom.com/platform/documentation/status-and-support/api-status-page
- https://tomtom.service-now.com/status
- https://www.vfb.be/Media/Default/pdf/TOMTOM%20-%20Annual%20Report%202025.pdf
- https://stockanalysis.com/quote/ams/TOM2/transcripts/

## 未確認のこと

- 日本の背景地図の詳しさ (建物形状、注記、POI): Map Display API に国別の収録内容の資料が見つからなかった。Orbis の元データ構成から OSM と Overture に依存する部分が大きいと考えられるが推測。
- 従量単価の一次情報: 料金ページの本文には単価が表示されず、計算機のスクリプトに埋め込まれた値を読んだ。表示上の USD 単価は為替係数で換算されるため確かめていない。
- スタイル、スプライト、フォント (Assets API) のリクエストが課金されるか: 料金ページに記載がない。
- 衛星画像の出どころと解像度: 該当ページが 404 で読めなかった。
- 3D 建物の提供有無、iOS 向け地図 SDK の現状: 文書が見つからなかった。
- Enterprise 契約の SLA: 個別契約で公開されていない。
- 1 地図ロードあたりのタイル数 15 枚は推測で、実測していない。
- 運営主体の上場市場と事業区分: corporate.tomtom.com が機械取得を 403 で拒否したため、第三者サイトに置かれた 2025 年次報告書と株価サイトで確かめた。API 規約の契約主体の法人名は規約本文の抽出範囲で確かめていない。
