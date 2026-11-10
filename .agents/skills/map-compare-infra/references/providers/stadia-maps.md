# Stadia Maps

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | Stadia Maps, Inc. (米デラウェア州法人、1690 Watertower Place Ste 100 #216, East Lansing, MI 48823, USA) |
| 公式サイト | https://stadiamaps.com/ |
| 料金ページ | https://stadiamaps.com/pricing/ |
| 利用規約・利用ポリシー | https://stadiamaps.com/terms-of-service/ (現行版は 2026-11-09 発効、前版は 2026-03-18 発効)、帰属表示 https://docs.stadiamaps.com/attribution/ |

## 概要

Stadia Maps は、OpenStreetMap ベースのベクトルタイルとラスタタイル、静的地図、衛星画像、ジオコーディング、ルート検索 (Valhalla ベース)、等時間圏、標高、タイムゾーンなどを API で提供するサービスである (https://stadiamaps.com/pricing/)。Stamen Design の Toner、Terrain、Watercolor の各スタイルは 2023-07-31 から Stadia Maps が配信している (https://maps.stamen.com/)。Free プランは非商用と評価目的に限られ、商用利用には月 20 USD からの有料プランが必要 (https://stadiamaps.com/pricing/ 、https://stadiamaps.com/terms-of-service/)。

## 地図データ

- データの出どころ (自社調査 / OSM / 公的データ / 他社からのライセンス): 地図は OpenStreetMap と OpenMapTiles 由来で、帰属表示は「© Stadia Maps © OpenMapTiles © OpenStreetMap」 (https://docs.stadiamaps.com/attribution/)。衛星画像は Airbus と PlanetObserver (Copernicus データを含む) からのライセンス (同)。ジオコーディングは OpenStreetMap、OpenAddresses、Who's On First、GeoNames、Foursquare Open Source Places を使う (https://docs.stadiamaps.com/geocoding-search-autocomplete/sources)。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): OSM の日本のデータに依存し、日本向けの独自データは公式ページに記載がない。日本の住所・番地の網羅性は未確認。
- 全球の対応: 全球。米国向けと EU 向け (tiles-eu.stadiamaps.com) のエンドポイントがある (https://docs.stadiamaps.com/vector/)。
- 更新頻度: 未確認 (ベクトルタイルのドキュメントに OSM データの更新頻度の記載がない、https://docs.stadiamaps.com/vector/)。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | 1 タイル = 1 クレジット (https://stadiamaps.com/pricing/) |
| ベクトルタイル (形式、スキーマ) | あり | MVT、OpenMapTiles 互換スキーマ、z0〜14 (以降はオーバーズーム)。1 タイル = 1 クレジット (https://docs.stadiamaps.com/vector/ 、https://stadiamaps.com/pricing/) |
| スタイルの編集・カスタマイズ | あり | 独自スタイル (Alidade Smooth / Smooth Dark / Bright / Satellite、Outdoors)、Stamen (Toner と派生、Terrain、Watercolor)、OSM Bright。OpenMapTiles 互換なので自作スタイルも使える (https://docs.stadiamaps.com/themes/ 、https://docs.stadiamaps.com/vector/) |
| 衛星・航空写真 | あり (Standard 以上) | 512px タイル 1 枚 = 4 クレジット (https://stadiamaps.com/pricing/) |
| 地形・3D 建物 | 一部 | Stamen Terrain スタイルと Elevation API (1 リクエスト 5 クレジット) がある (https://docs.stadiamaps.com/themes/ 、https://stadiamaps.com/pricing/)。3D 地形タイルと 3D 建物の提供は未確認 |
| ジオコーディング / 逆ジオコーディング | あり | 正・逆・構造化・一括とも 1 リクエスト 20 クレジット。オートコンプリート v2 は 1 クレジット。Free は基本 API のみ、Starter から標準ジオコーディング (https://stadiamaps.com/pricing/) |
| ルート検索 | あり | 標準ルート、地図マッチング、等時間圏は 20 クレジット、最適化ルート 40、行列 1 要素 10、交通考慮 60〜120 (https://stadiamaps.com/pricing/)。ナビゲーション SDK Ferrostar (BSD-3-Clause、0.59.0 が 2026-10-22 公開、https://github.com/stadiamaps/ferrostar) |
| オフライン利用 | 限定的 | モバイルアプリで端末あたり同時 100MB までのキャッシュは可 (規約 8 条)。それを超えるオフライン利用は Enterprise の個別契約か、Embedded tiles (要見積もり) (https://stadiamaps.com/terms-of-service/ 、https://stadiamaps.com/products/on-prem-embedded/) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): 地図描画の独自 SDK はなく、MapLibre GL JS、MapLibre Native、MapLibre React Native、Flutter MapLibre GL を推奨 (https://docs.stadiamaps.com/vector/)。API クライアントは TypeScript、Python、PHP、Kotlin、Swift 向けがあり、いずれも BSD-3-Clause (gh で確認: https://github.com/stadiamaps/stadiamaps-api-ts ほか)。ナビゲーションは Ferrostar (Android / iOS / Web / React Native)。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 使える。Leaflet (MapLibre GL Leaflet 経由)、OpenLayers (ol-mapbox-style 経由、描画差あり)、MVT を読めるレンダラー全般 (https://docs.stadiamaps.com/vector/)。ラスタタイルは Leaflet でもそのまま使える。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): 特定 SDK に限定する条項は見当たらない。データを競合する地図・ルート・交通サービスの改善に使うことは禁止 (規約 8 条、https://stadiamaps.com/terms-of-service/)。
- API キー・アカウントの要否: localhost / 127.0.0.1 からはキーなしで使えるが厳しいレート制限がある。本番の Web はドメイン認証 (Origin / Referer の検査) かキー、モバイル・サーバ・デスクトップは API キーが必要 (https://docs.stadiamaps.com/authentication/)。

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): クレジット。ベクトル・ラスタタイル 1 枚 = 1、衛星タイル 1 枚 = 4、静的地図 1 枚 = 20、キャッシュ可能な静的地図 1 枚 = 2,000、ジオコーディング 1 回 = 20 など (https://stadiamaps.com/pricing/)。地図ロード単位ではない。
- 無料枠: Free (0 USD) は月 200,000 クレジット、超過分の購入なし、標準ベースマップと基本 API のみ、商用不可。新規アカウントは 14 日間 Professional を試用できる (https://stadiamaps.com/pricing/、2026-11-10 確認)。
- 従量単価 (主な API ごとに、通貨と確かめた日つき。問い合わせ制ならそう書き、金額を推測しない): 価格は「$」表記で通貨コードの明記はない (米国企業のため USD と推測)。Starter 月 20 (月 1,000,000 クレジット、超過 1,000 クレジットあたり 0.03)、Standard 月 80 (7,500,000、超過 0.02)、Professional 月 250 (25,000,000、超過 0.015)。Enterprise は問い合わせ制 (https://stadiamaps.com/pricing/、2026-11-10 確認)。
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式と仮定を書く。単価が非公開なら「算出しない」): 仮定は 1 地図ロードあたりベクトルタイル 20 枚 (= 20 クレジット) で、ほかの API は使わない。月額 = プラン基本料 + max(0, ロード数 × 20 − 含有クレジット) / 1,000 × 超過単価 とし、最安のプランを選ぶ。10 万ロード (200 万クレジット) は Starter で 20 + 1,000 × 0.03 = 50 USD。100 万ロード (2,000 万クレジット) は Professional の含有枠内で 250 USD (Standard だと 80 + 12,500 × 0.02 = 330 USD)。1,000 万ロード (2 億クレジット) は Professional で 250 + 175,000 × 0.015 = 2,875 USD。1 ロードあたりのタイル数は画面サイズと操作量で大きく変わる (仮定)。Enterprise 契約の価格は非公開のため算出しない。
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): Free から Professional までは月額のセルフサーブ。Enterprise は年間の請求書払い、独自 SLA、オンプレミス、動画・印刷・オフライン向けの永続ライセンスを個別に定める要見積もり (https://stadiamaps.com/pricing/)。On-prem / Embedded も要見積もり (https://stadiamaps.com/products/on-prem-embedded/)。

## 利用規約上の制約

- 商用利用: Free は非商用か評価目的に限る (規約 13 条)。営利組織による利用は、収益を生むかどうかにかかわらず商用利用に当たる (規約 1 条) (https://stadiamaps.com/terms-of-service/)。Starter 以上は商用可 (https://stadiamaps.com/pricing/)。Stamen スタイルも全プランで使えるが、Free では同じく非商用に限られる (https://stadiamaps.com/stamen/ 、https://docs.stadiamaps.com/themes/)。
- アクセス量の上限・公正利用の条件: プランごとのクレジット上限。Free は超過分を購入できない (https://stadiamaps.com/pricing/)。キーなしの localhost 利用は厳しいレート制限 (https://docs.stadiamaps.com/authentication/)。
- キャッシュ・オフライン保存: 標準的なクライアント側キャッシュは可、ただし HTTP キャッシュヘッダーの期間を超えて保持しない。サーバ側キャッシュは禁止。モバイルアプリのオフライン用キャッシュは端末あたり同時 100MB まで。一括ダウンロードは禁止 (規約 8 条、https://stadiamaps.com/terms-of-service/)。キャッシュ可能な静的地図は有料契約中に限り保存できる (https://stadiamaps.com/pricing/)。
- 帰属表示の要件: 「© Stadia Maps © OpenMapTiles © OpenStreetMap」(リンク付きが望ましい)。Stamen スタイルは加えて「© Stamen Design」。Stamen Watercolor は OpenMapTiles の表示が不要。衛星は「© CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data)」 (https://docs.stadiamaps.com/attribution/)。帰属表示を隠すことは禁止 (規約 8 条)。
- 他社の地図との併用、データの持ち出しの制限: 他社地図との併用を禁じる条項は見当たらない。データを競合する地図・ルート・交通サービスの改善に使うことは禁止 (規約 8 条)。衛星画像の一括ダウンロードは禁止 (規約 30.1) (https://stadiamaps.com/terms-of-service/)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): クライアント SDK と Ferrostar は BSD-3-Clause で、組み込み・改変・配布では著作権表示とライセンス文の保持だけが求められ、SaaS 提供での追加義務はない (https://github.com/stadiamaps/ferrostar)。地図データは OSM 由来で ODbL が関わる。タイルの表示 (Produced Work) なら OSM の帰属表示で足りるが、タイルからデータを抽出した派生データベースを公開・配布すると ODbL の継承条件 (同ライセンスでの提供) が問題になる。ただし規約上、一括ダウンロードとサーバ側キャッシュが禁止されているので、そもそも大量のデータ抽出はできない (https://stadiamaps.com/terms-of-service/)。

## 安定性と運用

- SLA: セルフサーブのプランに SLA はなく、規約上サービスは現状有姿で提供される (規約 5 条、19 条、https://stadiamaps.com/terms-of-service/)。Enterprise では稼働率とサポートの保証を個別に定められる (https://stadiamaps.com/pricing/)。
- 運営の継続性 (運営主体、資金源): 2016 年創業、創業者は Luke Seelenbinder (CEO) と Ian Wagner。3 大陸に分散する小規模チーム (https://stadiamaps.com/about/)。資金源は未確認。
- 障害情報の公開先: https://status.stadiamaps.com/ (Maps、Routing、Geocoding などの部品ごとに表示)。

## 向いている場面

- Stamen Toner / Terrain / Watercolor の見た目をそのまま使いたい場合 (旧 maps.stamen.com の後継配信、https://maps.stamen.com/)。
- OpenMapTiles 互換のスキーマで、既存の OpenMapTiles 用スタイルを流用したい場合 (https://docs.stadiamaps.com/vector/)。
- 地図、ジオコーディング、ルート検索を 1 社で揃えたい小〜中規模の商用サービス (月 20 USD から公開単価で予算を立てられる)。
- Web でドメイン認証を使い、コードに API キーを埋め込みたくない場合 (https://docs.stadiamaps.com/authentication/)。

## 向いていない場面

- 営利組織が無料で使いたい場合 (収益の有無にかかわらず Free は使えない)。
- 日本の住所・建物・POI に OSM 以上の詳しさが要る場合 (日本向けの独自データの記載がない)。
- 公開 SLA が必要で、Enterprise 契約を結ばない場合。
- 100MB を超えるオフライン地図をアプリに持たせたい場合 (Enterprise か Embedded の個別契約になる)。

## 出典

- https://stadiamaps.com/
- https://stadiamaps.com/pricing/
- https://stadiamaps.com/terms-of-service/
- https://stadiamaps.com/stamen/
- https://stadiamaps.com/about/
- https://stadiamaps.com/products/on-prem-embedded/
- https://maps.stamen.com/
- https://docs.stadiamaps.com/themes/
- https://docs.stadiamaps.com/vector/
- https://docs.stadiamaps.com/authentication/
- https://docs.stadiamaps.com/attribution/
- https://docs.stadiamaps.com/geocoding-search-autocomplete/sources
- https://status.stadiamaps.com/
- https://github.com/stadiamaps/ferrostar
- https://github.com/stadiamaps/stadiamaps-api-ts

## 未確認のこと

- 料金の通貨コード: 料金ページは「$」表記のみで USD と明記されていない。本文では USD と推測して計算した。
- OSM データの更新頻度: ベクトルタイルのドキュメントに記載がない。
- 日本の住所・番地のジオコーディング精度と国内データの詳しさ: 公式ページに日本固有の記述がなく、実際に API を叩いて比べていない。
- ジオコーディングのデータソース一覧: docs.stadiamaps.com のジオコーディングのページは WebFetch で 403 となり、本文の 5 ソースは検索結果に表示された同ドキュメントの要約から取った。
- 3D 地形タイルと 3D 建物の提供: 料金ページとスタイル一覧に明記がない。
- プランごとのストレージ (temporary / persistent) の対応: 料金ページの表の構造が崩れて読み取れず、どのプランがどちらかを確定できなかった。
- 資金源: 会社紹介ページに出資・資金調達の記載がない。
