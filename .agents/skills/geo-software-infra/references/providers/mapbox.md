# Mapbox

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | Mapbox, Inc. (米国の未上場企業)。日本では SoftBank との合弁会社 Mapbox Japan がある ([TechCrunch 2020-05-20](https://techcrunch.com/2020/05/20/mapbox-and-softbank-form-joint-venture-to-provide-mapping-tech-to-japanese-developers/)) |
| 公式サイト | https://www.mapbox.com/ |
| 料金ページ | https://www.mapbox.com/pricing |
| 利用規約・利用ポリシー | 利用規約 https://www.mapbox.com/legal/tos (Last updated 2024-03-31)、Product Terms https://www.mapbox.com/legal/product-terms (2026-10-20 版 PDF)。日本の顧客には別の Japan Product Terms が適用される |

## 概要

Mapbox は地図タイル (ベクトル・ラスタ)、スタイル編集ツール Mapbox Studio、Web 用の Mapbox GL JS とモバイル用 Maps SDK、ジオコーディング、ルート検索などを API と SDK で提供する商用サービスである ([料金ページ](https://www.mapbox.com/pricing))。Web は GL JS の地図ロード数、モバイルは月間アクティブユーザー (MAU) 数で課金し、GL JS 以外から API を直接呼ぶ場合はリクエスト数で課金する ([Product Terms 2.8.3](https://www.mapbox.com/legal/product-terms))。

## 地図データ

- データの出どころ (自社調査 / OSM / 他社からのライセンス): 基本は OpenStreetMap と Mapbox 独自データの組み合わせで、地域ごとにデータベンダーのデータを加える。日本は ZENRIN のデータを使う ([Mapbox Streets v8](https://docs.mapbox.com/data/tilesets/reference/mapbox-streets-v8/))。ただし帰属表示のページは「一部の顧客向けには日本で ZENRIN のデータを含む」と書いており、どの契約で ZENRIN データが配信されるかは公開資料から確定できない ([About Maps 日本語版](https://www.mapbox.com/ja/about/maps)、[About Maps](https://www.mapbox.com/about/maps))。交通情報は一部の顧客向けに JARTIC のデータを使う ([About Maps](https://www.mapbox.com/about/maps))。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): Streets v8 には日本向けの拡張があり、ZENRIN の建物種別コードから建物種別を割り当て、階数表記 (例: 5F-10F) から高さを推定する。道路の上下線分離 (`dual_carriageway`)、車線数 (`lane_count`)、交差点名 (`intersection`) は日本のみの属性である。日本の POI は `category_en` が常に null。番地ラベル (`housenum_label`) のレイヤーはあるが日本固有の説明はない ([Mapbox Streets v8](https://docs.mapbox.com/data/tilesets/reference/mapbox-streets-v8/))。国内の番地の網羅度は未確認。
- 全球の対応: 全球のタイルを提供する ([Mapbox Streets v8](https://docs.mapbox.com/data/tilesets/reference/mapbox-streets-v8/))。
- 更新頻度: Streets v8 は「新しい情報が入り次第、定期的に更新」とだけ書かれ、周期は示されていない ([Mapbox Streets v8](https://docs.mapbox.com/data/tilesets/reference/mapbox-streets-v8/))。日本専用の Mapbox Transit v2 は ZENRIN のデータ更新に合わせて約 3 か月ごとに更新される ([Mapbox Transit v2](https://docs.mapbox.com/data/tilesets/reference/mapbox-transit-v2/))。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | Static Tiles API (Studio スタイルをラスタ化) と Raster Tiles API (衛星画像などのラスタタイルセット) ([料金ページ](https://www.mapbox.com/pricing)) |
| ベクトルタイル (形式、スキーマ) | あり | Vector Tiles API。Mapbox Vector Tile 形式で、スキーマは Mapbox Streets v8 などの Mapbox 独自スキーマ ([Mapbox Streets v8](https://docs.mapbox.com/data/tilesets/reference/mapbox-streets-v8/)) |
| スタイルの編集・カスタマイズ | あり | Mapbox Studio で編集する。Studio で作ったスタイルは Studio 内か Mapbox Map (Mapbox の地図コンテンツを含む地図) でのみ使え、他の地図デザインツールや Mapbox 以外の地図には使えない ([Product Terms 2.11, 3.36](https://www.mapbox.com/legal/product-terms)) |
| 衛星・航空写真 | あり | Mapbox Satellite。Maxar、Vexcel Imaging、NASA、USGS などが出どころ ([About Maps](https://www.mapbox.com/about/maps)、[Mapbox Satellite](https://docs.mapbox.com/data/tilesets/reference/mapbox-satellite/)) |
| 地形・3D 建物 | あり | 標高タイル Mapbox Terrain-DEM v1 ([Terrain-DEM](https://docs.mapbox.com/data/tilesets/reference/mapbox-terrain-dem-v1/))。建物の高さ属性があり 3D 押し出しに使える ([Mapbox Streets v8](https://docs.mapbox.com/data/tilesets/reference/mapbox-streets-v8/)) |
| ジオコーディング / 逆ジオコーディング | あり | Geocoding API。結果を保存できない Temporary と保存できる Permanent の 2 種がある ([Geocoding API](https://docs.mapbox.com/api/search/geocoding/)、[Product Terms 2.7](https://www.mapbox.com/legal/product-terms)) |
| ルート検索 | あり | Directions API ほか ([Directions API](https://docs.mapbox.com/api/navigation/directions/)) |
| オフライン利用 | あり (モバイル SDK) | モバイル SDK の機能。タイルパックの累計は 750 個まで ([Android offline guide](https://docs.mapbox.com/android/maps/guides/offline/))。Web のキャッシュは同じ端末で 30 日まで ([Product Terms 2.8.1](https://www.mapbox.com/legal/product-terms)) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): Web は Mapbox GL JS ([GL JS guides](https://docs.mapbox.com/mapbox-gl-js/guides/))、モバイルは Maps SDK for Android / iOS ([iOS guides](https://docs.mapbox.com/ios/maps/guides/)、[Android offline guide](https://docs.mapbox.com/android/maps/guides/offline/))。GL JS v2.0 以降は Mapbox の契約に基づくライセンスで提供され、課金・計測のコードとその送信データを改変してはならない ([Product Terms 2.14](https://www.mapbox.com/legal/product-terms))。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): Web では使える。規約は Qualified Renderer (GL JS v1.0 以上) を使わない場合、地図ロード単価ではなく API リクエスト数で課金すると定めており、他ライブラリからの利用自体は禁じていない ([Product Terms 2.8.3, 3.57](https://www.mapbox.com/legal/product-terms))。料金ページも Static Tiles API のリクエストを「Mapbox.js、Leaflet などラスタのスリッピーマップを作る一連のリクエスト」と説明している ([料金ページ](https://www.mapbox.com/pricing))。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): モバイルアプリでは Mobile SDK を Mapbox サービスへの唯一のアクセス手段として使わなければならない ([Product Terms 2.9.1](https://www.mapbox.com/legal/product-terms))。このため MapLibre Native などからモバイルアプリで Mapbox のタイルを使うことは規約上できないと読める。地図コンテンツは Mapbox の API から直接取得し、プロキシや再配信をしてはならない ([Product Terms 1.9, 2.8.1](https://www.mapbox.com/legal/product-terms))。
- API キー・アカウントの要否: 必要。Mapbox アカウントとアクセストークンで API を呼ぶ ([Access tokens](https://docs.mapbox.com/accounts/guides/tokens/))。
- 提供元のエージェント向けスキル: [mapbox/mapbox-agent-skills](https://github.com/mapbox/mapbox-agent-skills) (MIT)。Web、iOS、Android、Flutter の実装、スタイル、検索、ナビゲーション、アクセストークンの守り方など 20 個のスキルがあり、Google Maps からの移行と MapLibre からの移行のスキルも含む。Claude Code などに `/plugin marketplace add mapbox/mapbox-agent-skills` で入れる (2026-11-11 確認)。

## 料金

価格は全て米ドル、2026-11-10 に [料金ページ](https://www.mapbox.com/pricing) で確かめた。ページは「$」表記のみで通貨コードを明記していない。

- 課金単位 (地図ロード、タイルリクエスト、MAU など): Web は Mapbox GL JS の地図ロード (GL JS の初期化ごと。`new mapboxgl.Map()` の呼び出しで数え、12 時間のタイムアウトがある)。1 地図ロードには Vector Tiles API と Raster Tiles API のリクエストが無制限に含まれる ([料金ページ](https://www.mapbox.com/pricing)、[Product Terms 3.44](https://www.mapbox.com/legal/product-terms))。Web にはユーザー数で課金する Map Seats もある。モバイル SDK は MAU (課金月の間にアプリ内で Mapbox サービスを使ったユーザー)。GL JS 以外から API を呼ぶ場合はタイルなどのリクエスト数。
- 無料枠: GL JS 地図ロード月 50,000、モバイル MAU 月 25,000、Static Tiles API 月 200,000 リクエスト、Vector Tiles API 月 200,000、Raster Tiles API 月 750,000、Static Images API 月 50,000、Temporary Geocoding API 月 100,000、Directions API 月 100,000。
- 従量単価 (主な API ごとに、通貨と確かめた日つき): 以下は 1,000 単位あたりの単価 (USD、2026-11-10)。

| API | 区分と単価 |
|---|---|
| Mapbox GL JS 地図ロード | 50,001〜100,000: $5.00 / 100,001〜200,000: $4.00 / 200,001〜1,000,000: $3.00 / 1,000,001〜5,000,000: $2.50 / 5,000,001 以上: 要問い合わせ |
| モバイル Maps SDK (MAU) | 25,001〜125,000: $4.00 / 125,001〜250,000: $3.20 / 250,001〜1,250,000: $2.40 / 1,250,000 超: 要問い合わせ |
| Static Tiles API | 200,001〜2,000,000: $0.50 / 2,000,001〜4,000,000: $0.40 / 4,000,001〜20,000,000: $0.30 / 20,000,000 超: 要問い合わせ |
| Vector Tiles API | 200,001〜2,000,000: $0.25 / 2,000,001〜4,000,000: $0.20 / 4,000,001〜20,000,000: $0.15 / 20,000,000 超: 要問い合わせ |
| Raster Tiles API | 750,001〜2,000,000: $0.25 / 2,000,001〜4,000,000: $0.20 / 4,000,001〜20,000,000: $0.15 / 20,000,000 超: 要問い合わせ |
| Static Images API | 50,001〜500,000: $1.00 / 500,001〜1,000,000: $0.80 / 1,000,001〜5,000,000: $0.60 |
| Temporary Geocoding API | 100,001〜500,000: $0.75 / 500,001〜1,000,000: $0.60 / 1,000,001〜5,000,000: $0.45 / 5,000,000 超: 要問い合わせ |
| Directions API | 100,001〜500,000: $2.00 / 500,001〜1,000,000: $1.60 / 1,000,001〜5,000,000: $1.20 / 5,000,000 超: 要問い合わせ |

- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式も書く。単位の換算に仮定を置いたら仮定も書く): 2026-11-10 時点の単価による。
  - A. Mapbox GL JS を使う場合 (地図ロード課金。タイル料金は含まれる)
    - 月 10 万: (100,000 − 50,000) × $5.00 / 1,000 = 約 $250
    - 月 100 万: 50,000 × $5.00 + 100,000 × $4.00 + 800,000 × $3.00 (各 / 1,000) = $250 + $400 + $2,400 = 約 $3,050
    - 月 1,000 万: 100 万までの $3,050 + 4,000,000 × $2.50 / 1,000 ($10,000) = $13,050 に、500 万超の 500 万ロード分 (要見積もり) が加わる。$2.50 が続くと仮定すると (推測) 約 $25,550
  - B. MapLibre GL JS など他ライブラリで Vector Tiles API を直接使う場合 (仮定: 1 地図ロードあたり平均 20 枚のベクトルタイルを取得する。実際の枚数は画面サイズと操作量で大きく変わる)
    - 月 10 万 = 200 万タイル: (2,000,000 − 200,000) × $0.25 / 1,000 = 約 $450
    - 月 100 万 = 2,000 万タイル: $450 + 2,000,000 × $0.20 / 1,000 + 16,000,000 × $0.15 / 1,000 = $450 + $400 + $2,400 = 約 $3,250
    - 月 1,000 万 = 2 億タイル: 2,000 万タイルを超える部分が要問い合わせのため算出できない。下限は約 $3,250
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): クレジットカード登録によるセルフサーブの従量課金で始められる。大量利用は営業との個別見積もりで、年間コミットによる追加割引がある ([料金ページ](https://www.mapbox.com/pricing))。

## 利用規約上の制約

- 商用利用: 可。ただし死傷や環境被害につながりうる用途、賭博など経済的損害のリスクが高い用途、複数アカウントで無料枠に収めるなど料金を不当に減らす行為は禁止 ([Product Terms 1.3](https://www.mapbox.com/legal/product-terms))。
- アクセス量の上限・公正利用の条件: 人間の操作に応じたクエリに限り、一括・自動クエリやスクレイピングは禁止 ([Product Terms 1.9](https://www.mapbox.com/legal/product-terms))。サービスに過負荷をかける利用は予告なく停止されうる ([Product Terms 1.8](https://www.mapbox.com/legal/product-terms))。地図コンテンツやサービスを使って機械学習・AI を訓練すること、Mapbox と競合するサービスの開発・ベンチマークに使うことも禁止 ([Product Terms 1.5](https://www.mapbox.com/legal/product-terms))。API ごとのレート制限の数値は本稿では確かめていない。
- キャッシュ・オフライン保存: 原則としてエクスポート、ダウンロード、キャッシュ、保存は禁止 ([Product Terms 1.9](https://www.mapbox.com/legal/product-terms))。例外として Mapping API の地図コンテンツはエンドユーザーの端末上で、リクエストした同じ端末に限り 30 日までキャッシュできる。モバイルでは SDK が定める上限までで、上限を回避・変更してはならない ([Product Terms 2.8.1](https://www.mapbox.com/legal/product-terms))。Temporary Geocoding の結果は保存・キャッシュできず、Permanent Geocoding の結果は条件付きで保存できる ([Product Terms 2.7.2, 2.7.3](https://www.mapbox.com/legal/product-terms))。
- 帰属表示の要件: Mapbox ロゴ、www.mapbox.com/about/maps へリンクする「© Mapbox」、www.openstreetmap.org/about へリンクする「© OpenStreetMap」が必須で、Mapbox Map では右下に「Improve this map」のリンクも要る ([Product Terms 1.4](https://www.mapbox.com/legal/product-terms))。日本で ZENRIN データを使う場合は「Japan Data provided by ZENRIN CO., LTD.」の表記がある ([About Maps](https://www.mapbox.com/about/maps))。
- 他社の地図との併用、データの持ち出しの制限: 地図からトレースや抽出をしてはならない (衛星画像のみの地図を非商用か OSM 向けにトレースする場合を除く) ([Product Terms 1.6](https://www.mapbox.com/legal/product-terms))。再配信、プロキシ配信、スクリーンショットでの代替は禁止 ([Product Terms 1.10, 2.8.1](https://www.mapbox.com/legal/product-terms))。Studio スタイルを Mapbox 以外の地図に使うことは禁止 ([Product Terms 2.11](https://www.mapbox.com/legal/product-terms))。印刷物での利用は、日本の地図データについては学校での教育用途か私的利用に限られる ([Product Terms 1.7.3](https://www.mapbox.com/legal/product-terms))。他社の地図を同じ画面に並べることを直接禁じる条項は、Product Terms には見当たらなかった。

## 安定性と運用

- SLA: 有効な発注書 (Order) を結んだ顧客に月間稼働率 99.9% を約束する。99.0% 以上 99.9% 未満で月額の 10%、99.0% 未満で 25% をクレジットする (最大 25%)。セルフサーブの従量課金のみの顧客への適用は書かれていない ([SLA](https://www.mapbox.com/legal/sla)、Last updated 2024-04-15)。
- 運営の継続性 (運営主体、資金源): Mapbox, Inc. はベンチャーキャピタルの出資を受けた未上場企業で、2017 年に SoftBank Vision Fund が主導するシリーズ C で 1 億 6,400 万ドルを調達した ([TechCrunch 2017-10-10](https://techcrunch.com/2017/10/10/mapbox-raises-164m-to-expand-its-location-platform-to-cars-vr-ar-and-asia/))。2020 年に SoftBank との合弁 Mapbox Japan を設立した ([TechCrunch 2020-05-20](https://techcrunch.com/2020/05/20/mapbox-and-softbank-form-joint-venture-to-provide-mapping-tech-to-japanese-developers/))。現在の財務状況は未確認。
- 障害情報の公開先: https://status.mapbox.com/

## 向いている場面

- Mapbox GL JS を使い、Web の地図ロードが月 5 万以下に収まる、または地図ロード単位の予算見積もりで足りる Web アプリ。
- 日本国内で ZENRIN 由来の道路属性 (車線数、交差点名など) や建物の高さを使いたい場合 (ZENRIN データが自分の契約で配信されるかは事前に確認が要る)。
- Studio でスタイルを作り込み、Web とモバイル SDK で同じスタイルを使いたい場合。

## 向いていない場面

- モバイルアプリで MapLibre Native など Mapbox 以外の描画エンジンを使いたい場合 (Mobile SDK 以外での利用が規約上できない)。
- タイルを自前のサーバやオフラインパッケージに保存・再配信したい場合。
- 地図データを使って機械学習モデルを訓練したい場合や、印刷物に日本の地図を商用で載せたい場合。
- 月 500 万地図ロードを超える規模で、価格表だけで予算を確定したい場合 (要見積もり)。

## 出典

- https://www.mapbox.com/
- https://www.mapbox.com/pricing
- https://www.mapbox.com/legal/tos
- https://www.mapbox.com/legal/product-terms
- https://cdn.prod.website-files.com/609ed46055e27a02ffc0749b/6ad79764a359d21b46049ea4_Mapbox%20Product%20Terms%20(October%2020%2C%202026).pdf
- https://www.mapbox.com/legal/sla
- https://www.mapbox.com/about/maps
- https://www.mapbox.com/ja/about/maps
- https://docs.mapbox.com/data/tilesets/reference/mapbox-streets-v8/
- https://docs.mapbox.com/data/tilesets/reference/mapbox-transit-v2/
- https://docs.mapbox.com/data/tilesets/reference/mapbox-terrain-dem-v1/
- https://docs.mapbox.com/data/tilesets/reference/mapbox-satellite/
- https://docs.mapbox.com/api/search/geocoding/
- https://docs.mapbox.com/api/navigation/directions/
- https://docs.mapbox.com/android/maps/guides/offline/
- https://docs.mapbox.com/ios/maps/guides/
- https://docs.mapbox.com/mapbox-gl-js/guides/
- https://docs.mapbox.com/accounts/guides/tokens/
- https://status.mapbox.com/
- https://techcrunch.com/2017/10/10/mapbox-raises-164m-to-expand-its-location-platform-to-cars-vr-ar-and-asia/
- https://techcrunch.com/2020/05/20/mapbox-and-softbank-form-joint-venture-to-provide-mapping-tech-to-japanese-developers/

## 未確認のこと

- 日本の ZENRIN データがどの契約・プランで配信されるか。Streets v8 の説明は ZENRIN を日本のベンダーとして挙げるが、帰属表示ページは「一部の顧客向け」と書いており、条件を示す公開資料が見つからなかった。
- 日本の顧客に適用される Japan Product Terms の内容。PDF の所在は確認したが本稿では読んでいない。
- 国内の住所・番地の網羅度と、Streets v8 の更新周期。公式資料に数値がない。
- セルフサーブ顧客への SLA の適用、各 API のレート制限の数値、Mapbox の現在の財務状況。公開資料で確かめられなかった。
- 500 万地図ロード超、2,000 万タイル超の単価。料金ページが要問い合わせとしている。
- モバイル MAU の $2.40 の区分の上端。料金ページの表は区分の見出し (250,001+、1,250,000+) と単価の数が合わず、グラフの目盛りから 250,001〜1,250,000 と読んだ。
