# HERE

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | HERE Technologies (オランダに本拠を置く地図・位置情報サービス企業。2017 年のプレスリリースでの自己紹介は "the Netherlands-based global provider of mapping and location services") |
| 公式サイト | https://www.here.com/ |
| 料金ページ | https://www.here.com/get-started/pricing (料金表は JavaScript で描画され、データは https://pricing-calculator.here.com/api/contentfulData?widget=Pricing%20Widget から読み込まれる) |
| 利用規約・利用ポリシー | https://legal.here.com/en/terms/here-platform (2026-11-10 時点で HTTP 503 で読めず。本文は 2022-01-18 発効版 https://www.here.com/en-gb/terms/here-platform-terms-january-2022 で確認した) |

## 概要

HERE は地図表示 (ベクトルタイル、ラスタタイル、静止地図画像)、ジオコーディングと検索、ルート検索、交通情報などの位置情報 API を、従量課金の Base plan で提供する。Base plan では Web 向けの HERE Maps API for JavaScript とモバイル向けの HERE Explore SDK が使える (出典: 料金ページ)。料金ページには「表示価格は参考値で、最終的な価格は顧客と HERE の個別合意で決まる」と書かれている。オフライン地図を含む HERE Navigate SDK や MAU 課金は Base plan とは別の契約になる (出典: 料金ページ)。

## 地図データ

- データの出どころ (自社調査 / OSM / 他社からのライセンス): 自社の調査車両による走行調査を行っており、走行予定を https://www.here.com/drives で公開している。日本については、2017 年に Pioneer の子会社インクリメント・ピー (現ジオテクノロジーズ) と提携し、互いの SD 地図データを利用・再販できるようになったと発表している (出典: 2017-06-26 の HERE と Pioneer/Increment P のプレスリリース)。現在の日本の地図データがどこから来ているかを示す公式の記述は見つからなかった (未確認)。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): HERE Maps API for JavaScript では platform の region を `JP` にすると日本向けの地図になり、「日本固有の道路、ランドマーク、地名を現地の基準で収録する」と書かれている。日本向けスタイルと公共交通レイヤもある (出典: docs.here.com の Configure region-specific maps)。一方、HERE SDK のドキュメントには「既定では日本、中国、韓国など一部地域の地図データは限定的で、日本と韓国の完全な地図データには HERE の担当者への連絡が必要」とある (出典: HERE SDK の Maps and services)。建物形状、番地レベルの住所、道路属性の日本での収録度合いは公式資料で確かめられなかった (未確認)。
- 全球の対応: 全球を対象とする。Vector Tile API は Web メルカトルで全球のタイルを配信する (出典: Vector Tile API の API Reference)。
- 更新頻度: 未確認。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | Raster Tile API v3。トラック向け規制表示や logistics 系スタイルは Advanced Raster Tile として別単価 (出典: 料金ページ、Advanced raster tile のドキュメント) |
| ベクトルタイル (形式、スキーマ) | あり | Vector Tile API。Protobuf で Vector Tile Specification に従い、512px 表示に最適化、Web メルカトル。道路、建物、水域、POI を含む。HERE 独自のレイヤ構成で、MapLibre 用のスタイル URL は `.../styles/berlin/base/mapbox/tilezen` という形 (出典: Vector Tile API の概要、MapLibre ガイド)。レイヤ定義の一覧ページは確認できなかった |
| スタイルの編集・カスタマイズ | あり | Style Editor でスタイルを編集できる (出典: Vector Tile API の概要) |
| 衛星・航空写真 | あり | Raster Tile API に `satellite.day` スタイルがある。`logistics.satellite.day` は Advanced Raster Tile 扱い。通常の `satellite.day` がどちらの単価になるかは明記がない (出典: Raster Tile API のスタイル解説、Advanced raster tile) |
| 地形・3D 建物 | あり (3D 建物) | Maps API for JavaScript 3.2 (HARP エンジン) の feature に高さ情報つきの "building extruded" がある (出典: Features and modes)。地形の立体表示は確認できなかった |
| ジオコーディング / 逆ジオコーディング | あり | Geocoding & Search API。日本の住所の扱いを解説する公式チュートリアルがある |
| ルート検索 | あり | 自動車、自転車、歩行者、トラック、EV、公共交通、マトリクス、等時線など (出典: 料金ページ) |
| オフライン利用 | 契約による | オフライン地図は HERE Navigate SDK の機能で、Base plan ではなく MAU・アセット課金の契約に含まれる (出典: 料金ページ) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): Web は HERE Maps API for JavaScript (現行 3.2、描画エンジンは HARP のみ)。モバイルは HERE SDK (Explore / Navigate) (出典: 料金ページ、Maps API for JavaScript の移行ガイド)。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): Vector Tile API を MapLibre GL JS で使う公式ガイドがある (出典: MapLibre ガイド)。Vector Tile API の概要は「サードパーティのライブラリでも使える」としている。Leaflet、OpenLayers の公式ガイドは確認していない。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): 特定の SDK に限る条項は見つからなかった。ただし利用規約で HERE 以外のデータとの組み合わせに条件がある (下記「利用規約上の制約」)。
- API キー・アカウントの要否: HERE platform アカウントと API キーが必要。MapLibre の例ではスタイル URL に `apikey` を付ける (出典: MapLibre ガイド)。

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): トランザクション課金。地図タイルは 1 リクエスト = 1 トランザクション (出典: 料金ページ)。地図ロード単位の課金はない。
- 無料枠: Vector Tile、Raster Tile、Map Image、Geocode / Reverse Geocode、Routing (自動車・自転車・歩行者) はそれぞれ月 30,000 トランザクションまで無料。Discover / Search、Autosuggest、トラック・時刻考慮ルートなどは月 5,000、EV ルートなどは月 2,500 まで無料 (2026-11-10 確認、出典: 料金ページ)。
- 従量単価 (主な API ごとに、通貨と確かめた日つき): 1,000 トランザクションあたり、2026-11-10 確認。
  - Vector Tile: 30,001〜5,000,000 は USD 0.088 (EUR 0.070)、5,000,001〜10,000,000 は USD 0.070 (EUR 0.056)、10,000,001 以上は問い合わせ
  - Advanced Vector Tile: USD 0.239 / 0.191 (EUR 0.191 / 0.153)、同じ区分
  - Raster Tile: USD 0.120 / 0.095 (EUR 0.095 / 0.076)
  - Advanced Raster Tile: USD 0.239 / 0.191 (EUR 0.191 / 0.153)
  - Map Image: USD 0.88 / 0.70 (EUR 0.70 / 0.56)
  - Geocode / Reverse Geocode: USD 0.88 / 0.70 (EUR 0.70 / 0.56)
  - Discover / Search、Autosuggest: 5,001〜200,000 は USD 2.92、200,001〜1,000,000 は USD 2.33、それ以上は問い合わせ
  - Routing (自動車・自転車・歩行者、時刻考慮なし): USD 0.88 / 0.70。時刻考慮ルートは USD 2.92 / 2.33
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式も書く。単位の換算に仮定を置いたら仮定も書く): 仮定は (1) 1 地図ロードあたり Vector Tile を 15 リクエスト取得する、(2) ブラウザキャッシュによる削減は見込まない、(3) 料金表の区分は区分ごとに単価を当てる段階制として計算する、(4) USD 単価を使う。2026-11-10 の単価による。
  - 10 万ロード: 100,000 × 15 = 1,500,000 リクエスト。(1,500,000 − 30,000) ÷ 1,000 × 0.088 = 約 USD 129
  - 100 万ロード: 15,000,000 リクエスト。(5,000,000 − 30,000) ÷ 1,000 × 0.088 + 5,000,000 ÷ 1,000 × 0.070 = 437.36 + 350 = 約 USD 787、これに 10,000,001 リクエスト目以降の 5,000,000 リクエスト分 (問い合わせ価格) が加わる
  - 1,000 万ロード: 150,000,000 リクエスト。約 USD 787 に加えて 140,000,000 リクエスト分が問い合わせ価格になり、公開情報だけでは算出できない
  - 1 ロードあたりのタイル数を 2 倍にすると費用もおおむね 2 倍になる。実際のタイル数は画面サイズと操作量で大きく変わる
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): Base plan は platform.here.com でサインアップして使うセルフサーブの従量課金。月 1,000 万トランザクションを超える区分、MAU・アセット課金、Navigate SDK、有償サポートは問い合わせ (出典: 料金ページ)。

## 利用規約上の制約

以下は 2022-01-18 発効版の HERE Platform Terms による。最新版の URL が 2026-11-10 時点で読めず、現行版との差分は未確認。

- 商用利用: 商用利用を前提とした規約である。ただし利用規約 6.4 に禁止事項がある。
- アクセス量の上限・公正利用の条件: 料金ページに「No daily transaction limits」とある。規約上の数値上限は見つからなかった。
- キャッシュ・オフライン保存: 6.4(f) で、Platform 外に Results をキャッシュ・保存できるのは 30 日まで (社内のテスト・評価、監査記録などの例外あり)。6.4(g) で、日本の HERE Content と Location Services の Results (Geocoding and Search を除く) は 24 時間を超えてキャッシュ・保存できない (一部のスマートフォン向けプランは 30 日)。キャッシュはキャッシュヘッダが許す範囲に限る (Exhibit 2 の 1.3)。
- 帰属表示の要件: 13.1 で HERE のマークと著作権表示を削除・隠蔽してはならない。6.4(i) で誤った帰属表示を禁じる。
- 他社の地図との併用、データの持ち出しの制限: 6.4(a) で HERE 以外のデータセットを HERE Content と組み合わせてエンドユーザーに提供することを原則禁じ、重ね合わせは HERE とそれ以外の出どころが区別できる場合に限り認める。6.4(e) で HERE Content をもとにした地理データベースや POI データベースの作成を禁じる。6.4(c) で HERE Content の改変を禁じる。

## 安定性と運用

- SLA: HERE Service Level Agreement があり、HERE は「商業的に合理的な努力」で約束を果たすとしている。サービスクレジット、報告、インシデント管理の条項は、サポートパッケージの購入や個別契約で明示的に付与された企業顧客にだけ適用される。Vector Tile や Maps API の稼働率の数値は公開ページに見当たらなかった (出典: HERE Service Level Agreement)。
- 運営の継続性 (運営主体、資金源): 運営は HERE Technologies。公式サイトは 50 以上の拠点、52 か国の従業員を挙げている (出典: here.com/about)。株主構成は公式サイトで確かめられなかった (未確認)。
- 障害情報の公開先: https://status.here.com/status (API 単位の稼働状況、過去の実績、計画メンテナンスを公開。アカウントなしで閲覧可) (出典: HERE system status のドキュメント)。

## 向いている場面

- 日本と海外の両方を 1 社の地図とルート検索、ジオコーディングでそろえたい場合。
- トラック規制、EV、交通情報などの物流・移動系の API を地図と同じ契約で使いたい場合。
- 月数百万タイルまでの規模で、公開単価で費用を見積もりたい場合。

## 向いていない場面

- 日本国内の詳細な地図データを確実に使いたい場合。日本の完全なデータは SDK では担当者経由とされ、日本の Results は 24 時間を超えてキャッシュできない。
- OSM などの他のデータと自由に混ぜて地図を作りたい場合。規約 6.4(a) の組み合わせ条件がある。
- 月 1,000 万リクエストを超える規模を公開単価だけで見積もりたい場合。

## プライバシーとテレメトリ (2026-11-14 確認)

- **HERE SDK のテレメトリと測位改善**: HERE SDK で交通情報やネットワーク測位 (Wi-Fi / 基地局測位) 等を利用する場合、サービス改善のために匿名化された診断・テレメトリ情報 (タイムスタンプ、端末モデル、周辺の Wi-Fi / 基地局信号特性等) が処理される場合がある (HERE SDK Privacy Supplement)。
- **オプトアウト**: アプリ内設定でのテレメトリのオプトイン/オプトアウトに加え、HERE は Wi-Fi アクセスポイントの MAC アドレスを測位データベースから除外する専用のオプトアウト窓口 (HERE Wi-Fi Opt-Out) を用意している。HTTP タイル API 単体利用時のアクセスログ保持期間は未確認。

## 出典

- https://www.here.com/
- https://www.here.com/get-started/pricing
- https://pricing-calculator.here.com/api/contentfulData?widget=Pricing%20Widget
- https://www.here.com/en-gb/terms/here-platform-terms-january-2022
- https://legal.here.com/en/terms/here-platform
- https://docs.here.com/map-rendering/docs/introduction-vector-tile-api
- https://docs.here.com/map-rendering/reference/here-vector-tile-api-api-reference
- https://docs.here.com/map-rendering/docs/maplibre
- https://docs.here.com/map-rendering/docs/advanced-raster-tile
- https://docs.here.com/map-rendering/docs/styles-raster-tile-api
- https://docs.here.com/maps-api-for-js/docs/map-region-specifics
- https://docs.here.com/maps-api-for-js/docs/get-started-japan
- https://docs.here.com/maps-api-for-js/docs/features-modes
- https://docs.here.com/maps-api-for-js/docs/migration-guide
- https://docs.here.com/here-sdk/docs/ios-customization-catalogs
- https://docs.here.com/policies/docs/here-service-level-agreement
- https://docs.here.com/system-status/docs/concept-1
- https://www.here.com/about
- https://www.here.com/drives
- https://assets.here.com/x7rx8ayph7ee/ca7d3091-2a7a-4956-af8d-ae4b656c77e6/b74afffc6a13ba741f7b11e5e07d02c1/260617_HERE_and_Pioneer_Increment_P_form_partnership_to_enable_global_map_solutions.pdf

## 未確認のこと

- 現行の HERE Platform Terms の本文。legal.here.com が 2026-11-10 に HTTP 503 を返したため、2022-01-18 発効版で代用した。条項番号や内容が変わっている可能性がある。
- 日本の地図データの現在の調達元。公式に確認できたのは 2017 年のインクリメント・ピーとの提携発表だけである。
- Vector Tile API と Maps API for JavaScript で、追加契約なしに日本の詳細データがどこまで出るか。HERE SDK は「既定では限定的」とするが、Vector Tile API と Maps API for JavaScript には同様の記述が見つからなかった。
- 日本での建物形状、番地レベルの住所、道路属性の収録度合い。公式資料に記述が見つからなかった。
- 地図データの更新頻度。公式資料に記述が見つからなかった。
- `satellite.day` の課金区分 (Raster Tile か Advanced Raster Tile か)。Advanced の一覧に載っていないが、明記もない。
- Vector Tile API のレイヤ定義の一覧。公式ページを特定できなかった。
- Maps API for JavaScript での地形の立体表示の有無。
- 1 地図ロードあたりのタイルリクエスト数。概算は 15 リクエストと仮定した。
- 料金表の区分が段階制か、総量で単価が決まる方式か。料金ページに明記がなく、段階制と仮定した。
- 株主構成と資金源。公式サイトに記述が見つからなかった。
