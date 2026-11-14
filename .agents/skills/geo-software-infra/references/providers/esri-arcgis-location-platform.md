# Esri ArcGIS Location Platform

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | Environmental Systems Research Institute, Inc. (Esri)。米国カリフォルニア州レッドランズに本社を置く非上場の民間企業 (https://www.esri.com/en-us/about/media-relations/fact-sheet) |
| 公式サイト | https://location.arcgis.com/ 、開発者向け文書 https://developers.arcgis.com/ |
| 料金ページ | https://location.arcgis.com/pricing/ |
| 利用規約・利用ポリシー | ArcGIS Location Platform Agreement https://www.esri.com/en-us/legal/requirements/arcgis-location-platform-agreement 、Master Agreement (E204、2026-08-14 版) https://www.esri.com/en-us/legal/terms/full-master-agreement 、Product-Specific Terms of Use (E300、2025-11-13 版) https://www.esri.com/content/dam/esrisites/en-us/media/legal/product-specific-terms-of-use/e300.pdf 、データの帰属と追加条件 https://www.esri.com/en-us/legal/terms/data-attributions (一覧は https://location.arcgis.com/help/terms-of-use/) |

## 概要

ArcGIS Location Platform は、Esri が開発者向けに出している PaaS で、ベースマップ、ジオコーディング、ルート検索、標高、Places などの位置情報サービスと、自前データのホスティングを従量課金で提供する (https://location.arcgis.com/help)。ベースマップは Basemap Styles service (v2) から Mapbox Style Specification v8 形式のスタイル JSON とベクトルタイルとして配信され、MapLibre GL JS などのオープンソースのライブラリからも使える (https://developers.arcgis.com/rest/basemap-styles/)。毎月の無料枠があり、ベースマップは月 200 万タイルまで無料である (https://location.arcgis.com/pricing/)。

## 地図データ

- データの出どころ (自社調査 / OSM / 公的データ / 他社からのライセンス): 2 系統ある。ArcGIS Basemap styles (`arcgis/*`) は Esri とパートナー (TomTom、Garmin、FAO、NOAA、USGS など) のデータに OpenStreetMap を組み合わせたもの。Open Basemap styles (`open/*`) は Overture Maps のデータ (OpenStreetMap、Microsoft、Esri Community Maps などを含む) から作られている (https://developers.arcgis.com/documentation/mapping-and-location-services/mapping/basemaps/)。ベクトルベースマップ World_Basemap_v2 の動的帰属データ (https://static.arcgis.com/attribution/Vector/World_Basemap_v2?f=json) を東京付近で引くと、全球共通の Esri、TomTom、Garmin、USGS などに加えて、日本の範囲にだけ「GeoTechnologies, Inc」(ズーム 10〜23) と「GSI」(国土地理院、ズーム 8〜23) が出る。日本の詳細な道路・建物などは GeoTechnologies (MapFan) のデータを使っていると読める。Open Basemap は Overture 由来なので、日本の範囲は OSM などのオープンデータに依存する。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): 未確認。上記のとおり ArcGIS Basemap styles の日本部分には GeoTechnologies と国土地理院のデータが入っているが、建物形状や番地の収録範囲を Esri は公表していない。Esri のブログでは日本向けのベースマップ更新で建物、公園、道路、鉄道、POI、水域を収録したと説明している (https://esri.com/arcgis-blog/products/arcgis-online/mapping/new-and-updated-basemap-content-for-asia-and-europe)。
- 全球の対応: 全球。ArcGIS Basemap styles は `language`、`worldview`、`places` のパラメータに対応し、Open Basemap styles も一部は `language` に対応する (https://developers.arcgis.com/rest/basemap-styles/)。
- 更新頻度: Open Basemap は Overture の月次リリースごとに更新すると Esri が説明している (https://www.esri.com/arcgis-blog/products/arcgis/announcements/arcgis-open-basemap-with-data-from-overture-maps-now-available)。ArcGIS Basemap styles の更新周期は未確認。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | Static Basemap Tiles service。512×512 px の PNG、ズーム 0〜22。URL は `https://static-map-tiles-api.arcgis.com/arcgis/rest/services/static-basemap-tiles-service/v1/arcgis/{style}/static/tile/{z}/{y}/{x}`。`arcgis/imagery` は対象外 (https://developers.arcgis.com/rest/static-basemap-tiles/) |
| ベクトルタイル (形式、スキーマ) | あり | Basemap Styles service v2 が Mapbox Style Spec v8 のスタイルと Esri ベクトルタイル (World_Basemap_v2 など、ズーム 0〜22 の indexedVector) を返す。スキーマは Esri 独自 (https://developers.arcgis.com/rest/basemap-styles/ 、https://basemaps.arcgis.com/arcgis/rest/services/World_Basemap_v2/VectorTileServer?f=json) |
| スタイルの編集・カスタマイズ | あり | ArcGIS Vector Tile Style Editor で作ったカスタムスタイルを `styles/items/{item_id}` で配信できる (https://developers.arcgis.com/rest/basemap-styles/)。規約上 Basemap Styles は Location Platform の Basemap Services 以外と組み合わせてはならない (E300 脚注 109) |
| 衛星・航空写真 | あり | `arcgis/imagery`、`arcgis/imagery/standard`、`arcgis/imagery/labels`、`open/hybrid` など。中身は World Imagery (../imagery/esri-world-imagery.md を参照) |
| 地形・3D 建物 | あり | 標高は Elevation service (点単位の課金)、陰影起伏は `arcgis/hillshade/*` や `arcgis/terrain` スタイル (https://location.arcgis.com/pricing/ 、https://developers.arcgis.com/rest/basemap-styles/)。3D 建物を MapLibre から使う手段は未確認 |
| ジオコーディング / 逆ジオコーディング | あり | 結果を保存しない検索は月 2 万件無料、保存する場合は無料枠なし (https://location.arcgis.com/pricing/)。日本の住所の精度は未確認 |
| ルート検索 | あり | ルートは月 2 万件、到達圏 (service areas) は月 5,000 件無料 (https://location.arcgis.com/pricing/)。車載システムと消費者向けリアルタイムナビを主目的とするアプリは不可 (E300 脚注 5、Master Agreement 3.3 d) |
| オフライン利用 | 制限つきであり | Esri Content Packages でベースマップを持ち出せるのは ArcGIS Maps SDKs for Native Apps、ArcGIS Desktop、ArcGIS Pro に限る (Master Agreement 3.2 c 1) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): ArcGIS Maps SDK for JavaScript、ArcGIS Maps SDKs for Native Apps (Kotlin、Swift など) (https://developers.arcgis.com/)。ネイティブ SDK は API キーだけでなく Runtime ライセンス文字列か対応する利用者認証が必要で、Lite ライセンスは Location Platform のアカウントに付く (https://location.arcgis.com/help/licensing-and-attribution/)。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 使える。Esri は Esri Leaflet、MapLibre GL JS、ArcGIS REST JS、OpenLayers、CesiumJS を名指しで挙げている (https://location.arcgis.com/help/licensing-and-attribution/)。MapLibre 向けには Esri 製プラグイン Esri/maplibre-arcgis (Apache-2.0、2026-11-10 時点の最新は 1.3.3) があり、ベースマップスタイルとセッショントークン (`BasemapSession`) に対応する (`gh api repos/Esri/maplibre-arcgis` で確認、https://github.com/Esri/maplibre-arcgis)。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): ライブラリの制約はないが、データ側の制約がある。Basemap Styles は Location Platform の Basemap Services とだけ使える (E300 脚注 109)。データは Esri が提供した製品とだけ使え (Master Agreement 3.2 a)、取得・保存・スクレイピングは原則不可 (同 3.2 c)。Esri の帰属表示は OSS ライブラリでも必要 (下記)。
- API キー・アカウントの要否: 必要。Location Platform のアカウントを作り、API キーなどのアクセストークンで認証する。収益を得るアプリは全リクエストに認証が必要 (E300 脚注 89、https://location.arcgis.com/help/licensing-and-attribution/)。

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): ベースマップはタイル単位 (返したタイル数で課金) か、セッション単位 (1 セッション最長 12 時間) のどちらか。その他はジオコード件数、ルート件数、標高の点数、Places のリクエスト数など (https://developers.arcgis.com/rest/basemap-styles/ 、https://location.arcgis.com/pricing/)。セッショントークンは 1 アプリ 1 端末ごとに使い、タイルの大量書き出しのような機械的な使い方は禁止 (E300 脚注 10)。
- 無料枠: 毎月、ベースマップ 200 万タイル (ベクトルと Static Basemap Tiles の合算)、またはセッション方式なら 1,000 セッション。ジオコーディング (非保存) 2 万件、ルート 2 万件、標高 5 万点、Places 検索 500 件など (2026-11-10 確認、https://location.arcgis.com/pricing/ 、https://developers.arcgis.com/rest/basemap-styles/)。無料枠は請求サイクルの始めに戻る。従量課金 (pay-as-you-go) は新規アカウントでは無効で、無効のまま無料枠を超えるとそのサービスは次のサイクルまで止まる (https://location.arcgis.com/help/billing/)。
- 従量単価 (主な API ごとに、通貨と確かめた日つき。問い合わせ制ならそう書き、金額を推測しない): 2026-11-10 確認、米ドル。ベースマップタイル 1,000 タイルあたり 0.15 USD、ベースマップセッション 1,000 セッションあたり 4.0 USD、ジオコーディング (非保存) 1,000 件あたり 0.5 USD、ジオコーディング (保存) 1,000 件あたり 4 USD、ルート 1,000 件あたり 0.5 USD、到達圏 1,000 件あたり 50 USD、Places の近傍・範囲検索 1,000 件あたり 8 USD、標高 1,000 点あたり 1 USD。技術サポートは別売りで年 2,500 USD (https://location.arcgis.com/pricing/ 、https://developers.arcgis.com/rest/basemap-styles/)。
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式と仮定を書く。単価が非公開なら「算出しない」): 仮定は「1 地図ロードあたりベクトルタイル 15 枚 (推測。画面サイズ、ズーム操作、スタイルが参照するソース数で大きく変わる)」と「1 地図ロード = 1 セッション」。タイル方式は (ロード数 × 15 − 2,000,000) ÷ 1,000 × 0.15 USD。10 万ロードは 150 万タイルで無料枠内なので 0 USD。100 万ロードは (15,000,000 − 2,000,000) ÷ 1,000 × 0.15 = 1,950 USD。1,000 万ロードは (150,000,000 − 2,000,000) ÷ 1,000 × 0.15 = 22,200 USD。セッション方式は (ロード数 − 1,000) ÷ 1,000 × 4 USD で、10 万ロードは 396 USD、100 万ロードは 3,996 USD、1,000 万ロードは 39,996 USD。1 ロードあたりのタイル数が 27 枚を超えるとセッション方式のほうが安くなる (4 ÷ 0.15 ≒ 26.7)。いずれも 2026-11-10 の公開単価で、ボリュームディスカウントは公開されていない。
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): セルフサーブ。無料で登録でき、従量課金を有効にするにはクレジットカードが必要。請求は月次で年次払いには切り替えられない。発注書 (PO) やバウチャー (前払い) は Esri の営業か各国の代理店を通す (https://location.arcgis.com/help/billing/)。

## 利用規約上の制約

- 商用利用: 可。収益を得るアプリも配布できるが、Location Platform で発行したトークンで全リクエストを認証する必要がある (E300 脚注 89、https://location.arcgis.com/help/licensing-and-attribution/)。本番運用に使えるサブスクリプションは組織内で 1 つ (E300 脚注 90)。
- アクセス量の上限・公正利用の条件: 公開された上限はない。従量課金を有効にした場合の支払上限機能は文書に記載がない (https://location.arcgis.com/help/billing/)。セッショントークンの機械的な利用は禁止 (E300 脚注 10)。
- キャッシュ・オフライン保存: データのスクレイピング、ダウンロード、保存は原則禁止。例外は Esri Content Packages による ArcGIS のネイティブ SDK・Desktop・Pro でのオフライン利用と、規約に沿って取得・保存したジオコード結果の社内利用 (Master Agreement 3.2 c)。ジオコード結果の保存には有料の「保存」課金が必要 (E300 脚注 66)。PDF や画像などの静的な地図表現は帰属表示つきで作成・報告書に使える (Master Agreement 3.2 b)。
- 帰属表示の要件: 「Powered by Esri」の表示と、ベースマップのデータ提供元の名前を地図上か地図下端の常に見える位置に表示する。OSS ライブラリやサードパーティ API で使う場合も必要で、ライブラリが自動で出さない場合は自分で表示する。外してはならない (https://developers.arcgis.com/documentation/esri-and-data-attribution 、https://location.arcgis.com/help/licensing-and-attribution/)。Esri の帰属データ API (https://static.arcgis.com/attribution/Vector/World_Basemap_v2?f=json) は表示範囲とズームに応じた提供元を返す。
- 他社の地図との併用、データの持ち出しの制限: Esri のデータを第三者向けに販売・提供するデータ集の作成・検証・補完に使ってはならない (Master Agreement 3.3 b)。Software と Online Services の外で AI/ML の学習に使ってはならない (同 3.3 h)。Esri の製品を競合する製品に組み込んではならない (同 B.1 i)。Basemap Styles は Location Platform の Basemap Services 以外と使えない (E300 脚注 109)。他社地図を同じ画面に重ねることの明示的な禁止は見つからなかった。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): 2 点ある。(1) Master Agreement B.1 k は、Esri の製品を GPL のようなオープンソースやオープンデータベースのライセンス条件に服させる形で使用・組み込み・改変・配布・結合することを禁じている。組み込みと配布では、Esri のデータを ODbL などのデータと混ぜて 1 つのデータベースとして再配布するような形は避ける必要がある。(2) Open Basemap の元データの Overture は Base、Buildings、Divisions、Transportation の各テーマが ODbL、Places は提供元ごとに CDLA Permissive 2.0 などで、OSM 由来の部分には ODbL の帰属が要る (https://docs.overturemaps.org/attribution/)。タイルを表示するだけ (改変なし、SaaS 上の表示) なら帰属表示で足りるが、タイルからデータを抽出して DB 化し配布・提供すると ODbL の継承条件 (派生 DB の ODbL での公開) と Esri 規約のデータ保存禁止の両方にかかる。SDK とプラグイン (Esri/maplibre-arcgis、Esri Leaflet) は Apache-2.0 でコピーレフトはない。

## 安定性と運用

- SLA: あり。ArcGIS Location Platform Service Level Agreement (G632a、2025-12-23 版) で月間稼働率 99.9% を約束する。対象は Basemap Services、Static Basemap Tiles、Geocoding、Routing、Elevation、Places など。99.89〜95% で月額の 10%、95% 未満で 20% をクレジットで返す。無料枠を超えて使っていないと対象外、クレジットの最低額は 100 USD (https://www.esri.com/content/dam/esrisites/en-us/media/legal/referenced-files/service-level-agmt-arcgis-platform.pdf)。
- 運営の継続性 (運営主体、資金源): Esri は 1969 年創業の非上場企業で、ArcGIS 製品群のライセンスとサブスクリプションが収益源 (https://www.esri.com/en-us/about/media-relations/fact-sheet)。Location Platform の売上規模は公表されていない。
- 障害情報の公開先: https://status.location.arcgis.com/ (https://location.arcgis.com/help/service-reliability-and-support/)。技術サポートは標準では付かず、年間サポートを営業経由で買う。

## 向いている場面

- MapLibre GL JS や Leaflet で、GeoTechnologies と国土地理院のデータを含む日本の詳細な背景地図を、セルフサーブの従量課金で使いたい場合。月 200 万タイルの無料枠が大きく、小中規模なら無料で収まる。
- 背景地図に加えてジオコーディング、ルート検索、標高、自前データのホスティングを同じアカウントと請求でまとめたい場合。
- 稼働率 99.9% の SLA が書面で必要な場合 (無料枠を超える有料利用が前提)。
- ArcGIS Online や ArcGIS Pro など既存の Esri 製品と組み合わせる組織。

## 向いていない場面

- タイルを自前のサーバーや CDN にキャッシュして配りたい、オフラインでブラウザアプリに持ち込みたい場合。規約上、オフラインは ArcGIS のネイティブ SDK・Desktop・Pro に限られる。
- 地図データを抽出して自前の DB を作る、AI/ML の学習データに使う場合。
- 帰属表示 (Powered by Esri と提供元) を出せない画面設計の場合。
- 月 1,000 万ロード級でタイル方式を使う場合。公開単価に段階割引がなく、概算は月 2 万 USD を超える。

## プライバシーとテレメトリ (2026-11-14 確認)

- **位置づけと越境移転**: Esri Products & Services Privacy Statement Supplement により、顧客がデータ管理者、Esri がデータ処理者 (Data Processor) として位置づけられ、EU-U.S. Data Privacy Framework (DPF)、SCC、DPA に対応している。
- **利用計測とストア開示**: Location Platform ダッシュボードで API キーごとのリクエスト数や地図ロード等の利用指標を計測する。ネイティブ SDK (Swift / .NET MAUI / Unreal / Qt 等) には Apple 向け Privacy Manifest が同梱されているが、エンドユーザー向けの位置テレメトリ自動収集やオプトアウトの詳細は利用する SDK 構成ごとに要確認 (未確認)。

## 出典

- https://location.arcgis.com/
- https://location.arcgis.com/help
- https://location.arcgis.com/pricing/
- https://location.arcgis.com/help/billing/
- https://location.arcgis.com/help/licensing-and-attribution/
- https://location.arcgis.com/help/terms-of-use/
- https://location.arcgis.com/help/service-reliability-and-support/
- https://status.location.arcgis.com/
- https://developers.arcgis.com/
- https://developers.arcgis.com/rest/basemap-styles/
- https://developers.arcgis.com/rest/static-basemap-tiles/
- https://developers.arcgis.com/documentation/mapping-and-location-services/mapping/basemaps/
- https://developers.arcgis.com/maplibre-gl-js/
- https://developers.arcgis.com/documentation/esri-and-data-attribution
- https://basemaps.arcgis.com/arcgis/rest/services/World_Basemap_v2/VectorTileServer?f=json
- https://static.arcgis.com/attribution/Vector/World_Basemap_v2?f=json
- https://github.com/Esri/maplibre-arcgis
- https://www.esri.com/en-us/legal/requirements/arcgis-location-platform-agreement
- https://www.esri.com/en-us/legal/terms/full-master-agreement
- https://www.esri.com/content/dam/esrisites/en-us/media/legal/ma-full/ma-full.pdf
- https://www.esri.com/content/dam/esrisites/en-us/media/legal/product-specific-terms-of-use/e300.pdf
- https://www.esri.com/en-us/legal/terms/data-attributions
- https://www.esri.com/content/dam/esrisites/en-us/media/legal/referenced-files/service-level-agmt-arcgis-platform.pdf
- https://www.esri.com/arcgis-blog/products/arcgis/announcements/arcgis-open-basemap-with-data-from-overture-maps-now-available
- https://esri.com/arcgis-blog/products/arcgis-online/mapping/new-and-updated-basemap-content-for-asia-and-europe
- https://www.esri.com/en-us/about/media-relations/fact-sheet
- https://docs.overturemaps.org/attribution/

## 未確認のこと

- 日本の建物形状、番地、POI、道路属性の収録範囲: Esri は国別の収録内容を公表しておらず、帰属データから GeoTechnologies と国土地理院が使われていることまでしか分からない。
- ArcGIS Basemap styles の更新周期: 公式文書に記載が見つからなかった。
- Open Basemap の提供開始日と月次更新の公式記述: esri.com のブログと support.esri.com は機械取得が 403 で拒否され、本文を直接読めなかった。検索結果の抜粋からは 2025-08-28 に提供開始と読めるが一次情報で確かめていない。
- 3D 建物を MapLibre から使う手段: 文書が見つからなかった。
- 日本の住所でのジオコーディング精度: 実測していない。
- 運営主体の資金源の詳細: Esri のファクトシート (esri.com) は機械取得が拒否され、検索結果の抜粋で非上場であることを確かめたにとどまる。
- 1 地図ロードあたりのタイル数 15 枚は推測で、実測していない。
