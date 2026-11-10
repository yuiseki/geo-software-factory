# Google Maps Platform

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | Google LLC (Google Cloud の一部門として提供) |
| 公式サイト | https://mapsplatform.google.com/ |
| 料金ページ | https://developers.google.com/maps/billing-and-pricing/pricing (概要は https://mapsplatform.google.com/pricing/) |
| 利用規約・利用ポリシー | 利用規約 https://cloud.google.com/maps-platform/terms (Last modified 2026-08-26)、サービス固有規約 https://cloud.google.com/maps-platform/terms/maps-service-terms (Last modified 2026-10-28)、Map Tiles API のポリシー https://developers.google.com/maps/documentation/tile/policies |

## 概要

Google Maps Platform は Google マップの地図、ストリートビュー、場所検索、ジオコーディング、ルート検索を API と SDK で提供する従量課金サービスである ([料金ページ](https://developers.google.com/maps/billing-and-pricing/pricing))。Web では Maps JavaScript API の地図ロード (Dynamic Maps SKU) で課金し、Google の SDK を使わずに描画したい場合は Map Tiles API でタイルを直接取得してタイル単位で課金する ([Maps SKU details](https://developers.google.com/maps/billing-and-pricing/sku-details/maps))。2025-03-01 に月 200 ドルのクレジットが廃止され、SKU ごとの月間無料枠に置き換わった ([March 2025 changes](https://developers.google.com/maps/billing-and-pricing/march-2025))。

## 地図データ

- データの出どころ (自社調査 / OSM / 他社からのライセンス): 現在の日本の地図データの出どころは公式資料で未確認。日本の Google マップは 2019 年 3 月に地図が切り替わり、著作権表記から ZENRIN の表記がなくなったと報じられた ([ASCII 2019-03](https://ascii.jp/elem/000/001/831/1831886/))。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): 未確認。Map Tiles API の roadmap タイルは道路、建物、POI、行政界を含むと説明されている ([2D Tiles overview](https://developers.google.com/maps/documentation/tile/2d-tiles-overview))。ベクトルの生データ (地物ごとの属性) を取得するメソッドは自動車業界のパートナー向けに限られる ([Map Tiles API overview](https://developers.google.com/maps/documentation/tile/overview))。
- 全球の対応: 全球を対象とする。国・地域ごとの機能の対応状況は [Coverage](https://developers.google.com/maps/coverage) にある。請求先住所が欧州経済領域 (EEA) にある場合は 2025-07-08 から EEA 向け規約が適用され、Map Tiles API の一部コンテンツが返らなくなった ([Map Tiles API overview](https://developers.google.com/maps/documentation/tile/overview))。
- 更新頻度: 未確認。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | Map Tiles API の 2D Map Tiles。roadmap / satellite / terrain の画像タイル (PNG または JPEG) で、セッショントークンの取得が前提 ([2D Tiles overview](https://developers.google.com/maps/documentation/tile/2d-tiles-overview)、[Session tokens](https://developers.google.com/maps/documentation/tile/session_tokens)) |
| ベクトルタイル (形式、スキーマ) | 一般向けにはなし | Maps JavaScript API はベクトル描画に対応するが ([Vector maps](https://developers.google.com/maps/documentation/javascript/vector-map))、タイルの形式やスキーマは公開されていない。Map Tiles API のベクトルタイルのメソッドは自動車業界のパートナー向け ([Map Tiles API overview](https://developers.google.com/maps/documentation/tile/overview)) |
| スタイルの編集・カスタマイズ | あり | Maps JavaScript API ではクラウドベースのスタイル設定 (Map ID) ([Cloud customization](https://developers.google.com/maps/documentation/javascript/cloud-customization))。Map Tiles API では roadmap に限りセッション作成時の `styles` で JSON スタイルを指定できる ([Session tokens](https://developers.google.com/maps/documentation/tile/session_tokens)) |
| 衛星・航空写真 | あり | satellite タイル ([2D Tiles overview](https://developers.google.com/maps/documentation/tile/2d-tiles-overview))。Photorealistic 3D Tiles は衛星・航空写真を貼った 3D メッシュ ([3D Tiles](https://developers.google.com/maps/documentation/tile/3d-tiles)) |
| 地形・3D 建物 | あり | terrain タイル (等高線と自然地物) と Photorealistic 3D Tiles ([2D Tiles overview](https://developers.google.com/maps/documentation/tile/2d-tiles-overview)、[3D Tiles](https://developers.google.com/maps/documentation/tile/3d-tiles)) |
| ジオコーディング / 逆ジオコーディング | あり | Geocoding API ([Geocoding](https://developers.google.com/maps/documentation/geocoding/overview)) |
| ルート検索 | あり | Routes API ([Routes](https://developers.google.com/maps/documentation/routes)) |
| オフライン利用 | なし (Map Tiles API) | Map Tiles API はオフライン用途を含む可視化以外の用途に使えない ([Map Tiles API policies](https://developers.google.com/maps/documentation/tile/policies))。モバイル SDK に開発者向けのオフライン地図機能があるかは未確認 |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): Maps JavaScript API、Maps SDK for Android、Maps SDK for iOS ([Android](https://developers.google.com/maps/documentation/android-sdk/overview)、[iOS](https://developers.google.com/maps/documentation/ios-sdk/overview))。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): Map Tiles API を使えば使える。Map Tiles API のポリシーは「サードパーティのレンダラーで Google マップを表示する場合」のロゴ表示の決まりを定めており、他のレンダラーでの表示を前提にしている ([Map Tiles API policies](https://developers.google.com/maps/documentation/tile/policies))。3D Tiles は「任意の 3D Tiles レンダラー」にルートタイルセットの URL を渡して使う ([Map Tiles API overview](https://developers.google.com/maps/documentation/tile/overview))。ただし 2D Map Tiles はラスタ画像なので、ベクトルタイル前提のスタイル編集はできない。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): Google Maps Core Services を Google 以外の地図と一緒に、または近くで使ってはならない。例として、Places のコンテンツを Google 以外の地図に表示すること、ストリートビューと Google 以外の地図を同じ画面に表示すること、Google の地図から Google 以外の地図へリンクすることが挙がっている ([利用規約 3.2.3(e)](https://cloud.google.com/maps-platform/terms))。サードパーティのレンダラーを使うときは、Google ロゴにレンダラーのロゴを重ねず、十分な間隔を取る ([Map Tiles API policies](https://developers.google.com/maps/documentation/tile/policies))。
- API キー・アカウントの要否: 必要。請求先アカウントを紐づけた Google Cloud プロジェクトと API キーが要る ([Get API key](https://developers.google.com/maps/documentation/javascript/get-api-key))。

## 料金

価格は全て米ドル (料金ページに「All prices in USD」と明記)、2026-11-10 に [料金ページ](https://developers.google.com/maps/billing-and-pricing/pricing) で確かめた。

- 課金単位 (地図ロード、タイルリクエスト、MAU など): SKU ごとの課金対象イベント数。Dynamic Maps は Maps JavaScript API の地図ロードの成功 (Map ID の有無を問わない) と、Android / iOS / Navigation SDK での Map ID を使った地図ロードで発生する。Maps SDK (モバイル) は地図ロード単位で、パンやズーム、レイヤー切り替えでは追加の地図ロードは発生しない。2D Map Tiles は 2D タイルを返したリクエスト 1 件ごとで、セッショントークンとビューポート情報のリクエストは課金されない ([Maps SKU details](https://developers.google.com/maps/billing-and-pricing/sku-details/maps))。SKU は Essentials / Pro / Enterprise の 3 区分 ([March 2025 changes](https://developers.google.com/maps/billing-and-pricing/march-2025))。
- 無料枠: SKU ごとに月間無料枠がある。Dynamic Maps 10,000、Static Maps 10,000、2D Map Tiles 100,000、Street View Tiles 100,000、Photorealistic 3D Tiles 1,000、Geocoding 10,000、Autocomplete Requests (Places API New) 10,000、Compute Routes Essentials 10,000。Maps SDK (モバイル) は無料枠が「Unlimited」で単価の記載がない ([料金ページ](https://developers.google.com/maps/billing-and-pricing/pricing))。
- 従量単価 (主な API ごとに、通貨と確かめた日つき): 以下は 1,000 イベントあたり (USD、2026-11-10)。区分の境界は料金ページの列見出しと無料枠から読んだ。

| SKU (区分) | 単価 |
|---|---|
| Dynamic Maps (Essentials) | 10,001〜100,000: $7.00 / 100,001〜500,000: $5.60 / 500,001〜1,000,000: $4.20 / 1,000,001〜5,000,000: $2.10 / 5,000,001 以上: $0.53 |
| Static Maps (Essentials) | $2.00 / $1.60 / $1.20 / $0.60 / 5,000,001 以上: $0.15 (区分の境界は Dynamic Maps と同じ並び) |
| 2D Map Tiles (Essentials) | 100,001〜1,000,000: $0.60 / 1,000,001〜5,000,000: $0.48 / 5,000,001〜10,000,000: $0.36 / 10,000,001〜50,000,000: $0.18 / 50,000,001 以上: $0.045 |
| Street View Tiles (Essentials) | $2.00 / $1.60 / $1.20 / $0.60 / 50,000,001 以上: $0.20 |
| Photorealistic 3D Tiles (Enterprise) | $6.00 / $5.10 / $4.20 / $3.30 / 5,000,001 以上: $2.40 |
| Geocoding (Essentials) | 10,001〜100,000: $5.00 / 100,001〜500,000: $4.00 / 500,001〜1,000,000: $3.00 / 1,000,001〜5,000,000: $1.50 / 5,000,001 以上: $0.38 ([March 2025 changes](https://developers.google.com/maps/billing-and-pricing/march-2025)) |
| Autocomplete Requests (Essentials) | $2.83 / $2.27 / $1.70 / $0.85 / 5,000,001 以上: $0.21 |
| Compute Routes Essentials | $5.00 / $4.00 / $3.00 / $1.50 / 5,000,001 以上: $0.38 |

- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式も書く。単位の換算に仮定を置いたら仮定も書く): 2026-11-10 時点の従量単価による。
  - A. Maps JavaScript API を使う場合 (Dynamic Maps)
    - 月 10 万: (100,000 − 10,000) × $7.00 / 1,000 = 約 $630
    - 月 100 万: $630 + 400,000 × $5.60 / 1,000 + 500,000 × $4.20 / 1,000 = $630 + $2,240 + $2,100 = 約 $4,970
    - 月 1,000 万: $4,970 + 4,000,000 × $2.10 / 1,000 + 5,000,000 × $0.53 / 1,000 = $4,970 + $8,400 + $2,650 = 約 $16,020
  - B. MapLibre GL JS などで Map Tiles API の 2D Map Tiles を使う場合 (仮定: 1 地図ロードあたり平均 20 枚のタイルを取得する。実際の枚数は画面サイズ、タイルの大きさ、操作量で大きく変わる)
    - 月 10 万 = 200 万タイル: 900,000 × $0.60 / 1,000 + 1,000,000 × $0.48 / 1,000 = $540 + $480 = 約 $1,020
    - 月 100 万 = 2,000 万タイル: $540 + 4,000,000 × $0.48 / 1,000 + 5,000,000 × $0.36 / 1,000 + 10,000,000 × $0.18 / 1,000 = $540 + $1,920 + $1,800 + $1,800 = 約 $6,060
    - 月 1,000 万 = 2 億タイル: $6,060 + 30,000,000 × $0.18 / 1,000 + 150,000,000 × $0.045 / 1,000 = $6,060 + $5,400 + $6,750 = 約 $18,210
    - 2D タイルの既定のクォータはプロジェクトあたり 1 日 15,000 リクエスト、毎分 6,000 リクエストで ([Map Tiles API usage and billing](https://developers.google.com/maps/documentation/tile/usage-and-billing))、上記の規模ではクォータの引き上げが前提になる。
  - 定額のサブスクリプションを選ぶと、Starter 月 $100 (合算 50,000 コール、Dynamic Maps と Geocoding)、Essentials 月 $275 (合算 100,000 コール、2D Map Tiles を含む)、Pro 月 $1,200 (合算 250,000 コール) で、超過分は従量単価で課金される ([Subscriptions](https://developers.google.com/maps/billing-and-pricing/subscriptions))。
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): セルフサーブの従量課金が基本で、量に応じた割引は価格表に自動で組み込まれている。月 1,000 万イベント以上の有料 Core Services SKU がある顧客は、Google の裁量で追加の割引を受けられる場合がある ([March 2025 changes](https://developers.google.com/maps/billing-and-pricing/march-2025))。サブスクリプションは月額で、いつでも変更・解約できる ([Subscriptions](https://developers.google.com/maps/billing-and-pricing/subscriptions))。リセラー経由の契約もある ([利用規約 19.1](https://cloud.google.com/maps-platform/terms))。

## 利用規約上の制約

- 商用利用: 可。ただし高リスク用途、料金を逃れる目的の利用、児童向けサービス (COPPA の対象) などは禁止 ([利用規約 3.2.1](https://cloud.google.com/maps-platform/terms))。Google Maps Core Services を使って Google マップの代替品を作ること、リスティング・ディレクトリサービスや広告商品に使うことも禁止 ([利用規約 3.2.3(d)](https://cloud.google.com/maps-platform/terms))。
- アクセス量の上限・公正利用の条件: Maps JavaScript API の地図ロードはプロジェクトあたり毎分 30,000、IP あたり毎分 300 ([JS API usage and billing](https://developers.google.com/maps/documentation/javascript/usage-and-billing))。Map Tiles API の 2D タイルは前項のとおり 1 日 15,000 リクエストが既定 ([Map Tiles API usage and billing](https://developers.google.com/maps/documentation/tile/usage-and-billing))。
- キャッシュ・オフライン保存: Google Maps Content は、サービス固有規約が明示的に許す場合を除きキャッシュしてはならない ([利用規約 3.2.3(b)](https://cloud.google.com/maps-platform/terms))。事前取得、インデックス化、保存、再共有、再ホスト、タイルの一括ダウンロードも禁止 ([利用規約 3.2.3(a)](https://cloud.google.com/maps-platform/terms))。サービス固有規約は Geocoding API などの緯度経度を 30 日までキャッシュすることや place_id の保存を許すが、Map Tiles API にはキャッシュを許す個別の条項がない ([サービス固有規約](https://cloud.google.com/maps-platform/terms/maps-service-terms))。Map Tiles API のレスポンスの `Cache-Control` ヘッダ (max-age、stale-while-revalidate) は HTTP の規定どおりに守る必要がある ([Map Tiles API policies](https://developers.google.com/maps/documentation/tile/policies))。
- 帰属表示の要件: Google が提供する帰属表示 (ロゴ、著作権表示など) を改変・隠蔽・削除せずに表示する ([利用規約 3.2.2(b)](https://cloud.google.com/maps-platform/terms))。Map Tiles API では、できる限り Google Maps のロゴを表示し (狭い場合は「Google Maps」の文字)、表示中のタイルの帰属表示を集約して 1 行に並べる ([Map Tiles API policies](https://developers.google.com/maps/documentation/tile/policies))。
- 他社の地図との併用、データの持ち出しの制限: Google 以外の地図との併用は禁止 ([利用規約 3.2.3(e)](https://cloud.google.com/maps-platform/terms))。Google Maps Content を元にしたコンテンツの作成 (衛星画像からのトレース、標高値からの地形モデル作成、AI モデルの訓練・評価など) も禁止 ([利用規約 3.2.3(c)](https://cloud.google.com/maps-platform/terms))。自社データを重ねる場合は、どこが Google のデータでどこが自社データかを利用者が分かるようにし、帰属表示を重ねない ([Map Tiles API policies](https://developers.google.com/maps/documentation/tile/policies))。

## 安定性と運用

- SLA: 対象となる Core Services ごとに月間稼働率 99.9% 以上を目標とする。99.0% 以上 99.9% 未満で月額の 10%、95.0% 以上 99.0% 未満で 25%、95.0% 未満で 50% をクレジットする。クレジットは 30 日以内にサポートへ申請した場合に限る ([SLA](https://cloud.google.com/maps-platform/terms/sla)、Last modified 2025-01-27)。
- 運営の継続性 (運営主体、資金源): Google LLC が運営する。規約の重要な変更は通知から 30 日後に発効し、SLA に不利な変更は 90 日前までに通知する ([利用規約 1.3(b)](https://cloud.google.com/maps-platform/terms))。旧 Places API、Directions API、Distance Matrix API は Legacy 扱いで、廃止の 12 か月以上前に告知すると説明されている ([March 2025 changes](https://developers.google.com/maps/billing-and-pricing/march-2025))。
- 障害情報の公開先: https://status.cloud.google.com/maps-platform/

## 向いている場面

- Google の SDK で地図を描き、場所検索・ルート検索・ストリートビューを同じ画面で使いたい場合。
- モバイルアプリで Map ID を使わない地図表示 (Maps SDK の無料枠が Unlimited) を主に使う場合。
- 3D の街並み (Photorealistic 3D Tiles) を CesiumJS など 3D Tiles 対応のレンダラーで表示したい場合。

## 向いていない場面

- Google 以外の地図や Google 以外の POI データと同じ画面に並べたい場合。
- タイルを保存・オフライン配布したい場合や、地図から地物を抽出・トレースしたい場合。
- 他ライブラリでベクトルタイルを読み込み、スタイルを自由に組みたい場合 (一般向けの Map Tiles API はラスタのみ)。
- Web の地図ロードが多い場合。Dynamic Maps の無料枠は月 10,000 で、月 10 万ロードでも約 $630 かかる。

## 出典

- https://mapsplatform.google.com/
- https://mapsplatform.google.com/pricing/
- https://developers.google.com/maps/billing-and-pricing/pricing
- https://developers.google.com/maps/billing-and-pricing/march-2025
- https://developers.google.com/maps/billing-and-pricing/subscriptions
- https://developers.google.com/maps/billing-and-pricing/sku-details/maps
- https://cloud.google.com/maps-platform/terms
- https://cloud.google.com/maps-platform/terms/maps-service-terms
- https://cloud.google.com/maps-platform/terms/sla
- https://developers.google.com/maps/documentation/tile/overview
- https://developers.google.com/maps/documentation/tile/2d-tiles-overview
- https://developers.google.com/maps/documentation/tile/session_tokens
- https://developers.google.com/maps/documentation/tile/policies
- https://developers.google.com/maps/documentation/tile/usage-and-billing
- https://developers.google.com/maps/documentation/tile/3d-tiles
- https://developers.google.com/maps/documentation/javascript/usage-and-billing
- https://developers.google.com/maps/documentation/javascript/vector-map
- https://developers.google.com/maps/documentation/javascript/cloud-customization
- https://developers.google.com/maps/documentation/javascript/get-api-key
- https://developers.google.com/maps/documentation/android-sdk/overview
- https://developers.google.com/maps/documentation/ios-sdk/overview
- https://developers.google.com/maps/documentation/geocoding/overview
- https://developers.google.com/maps/documentation/routes
- https://developers.google.com/maps/coverage
- https://status.cloud.google.com/maps-platform/
- https://ascii.jp/elem/000/001/831/1831886/

## 未確認のこと

- 日本の地図データの現在の出どころと、建物・番地・道路属性の詳しさ、更新頻度。Google は出どころと更新周期を公式資料で示していない。2019 年の切り替えは報道で確かめたのみ。
- 料金表の Static Maps、Street View Tiles、Photorealistic 3D Tiles、Autocomplete、Compute Routes の中間区分の境界。料金ページは列見出しで示しており、本稿では単価の並びだけを書いた。
- Maps SDK (モバイル) の SKU が「Unlimited」である一方、Map ID を使うモバイルの地図ロードは Dynamic Maps の課金対象になる。どの使い方で課金が発生するかの細部は確かめきれていない。
- モバイル SDK の開発者向けオフライン地図機能の有無。公式資料で該当する記載を見つけられなかった。
- Map Tiles API の 2D タイルの 1 日 15,000 リクエストのクォータをどこまで引き上げられるか。公開資料に上限の記載がない。
