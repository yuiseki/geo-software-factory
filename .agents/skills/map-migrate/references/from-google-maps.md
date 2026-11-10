# Google Maps Platform からの移行

対象: Google Maps JavaScript API、Places、Geocoding、Directions からの移行

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 根拠の版 | Google Maps Platform 利用規約 (Last modified 2026-08-26)、同サービス固有規約 (Last modified 2026-10-28)。ライブラリの版は map-compare-library の reference (2026-11-10 確認) による |

## 移行元の特徴

Google Maps JavaScript API は、地図の描画、データ (地図、航空写真、ストリートビュー、Places)、規約、課金が 1 つに束ねられている。本体は非公開で Google のサーバーから読み込み、見た目はマップ ID に紐づくクラウドのスタイルで決める ([google-maps-js](../../map-compare-library/references/libraries/google-maps-js.md))。MapLibre / Mapbox のスタイル仕様は読めない。課金は地図の読み込みと API ごとの SKU で数える ([google-maps](../../map-compare-infra/references/providers/google-maps.md))。

移行を縛るのは技術より規約である。Google Maps Core Services を Google 以外の地図と一緒に、または近くで使ってはならず、例として Places のコンテンツを Google 以外の地図に表示することが挙がっている (利用規約 3.2.3(e)、https://cloud.google.com/maps-platform/terms)。サービス固有規約も、Geocoding API (6.2)、Directions API (4.2)、Places API (14.2) などのコンテンツを Google 以外の地図と組み合わせることを個別に禁じている (https://cloud.google.com/maps-platform/terms/maps-service-terms)。このため、地図だけを先に乗り換えて検索やルート検索を Google のまま残す段階は、規約上とれない。

## 移行先の候補と API の対応

座標の順に注意する。Google は `{ lat, lng }`、MapLibre GL JS は `[lng, lat]` (`LngLat`)、Leaflet は `[lat, lng]`、OpenLayers は既定で EPSG:3857 の `[x, y]` で、経緯度を渡すには `fromLonLat()` で変換するか `useGeographic()` を呼ぶ。取り違えると地物が海の上に出る。

| 移行元の機能・API | 移行先 (ライブラリ・サービス) | 違いと注意 | 出典 |
|---|---|---|---|
| `google.maps.Map` (マップ ID、クラウドのスタイル) | MapLibre GL JS の `Map`、OpenLayers の `Map`、Leaflet の `Map` | MapLibre はスタイル文書 (JSON) を `style` に渡す。Google のクラウドのスタイルや JSON スタイル配列を MapLibre Style に変える公式の道具は見つからなかった (未確認)。見た目は作り直す前提で見積もる | https://maplibre.org/maplibre-gl-js/docs/, [google-maps-js](../../map-compare-library/references/libraries/google-maps-js.md) |
| `google.maps.Marker` (2024-02 に非推奨)、`AdvancedMarkerElement` | MapLibre の `Marker` (DOM 要素)、Leaflet の `Marker`、OpenLayers は `Overlay` か点の地物 | 数百件を超えるなら DOM のマーカーをやめ、GeoJSON ソースと `symbol` / `circle` レイヤーで描くほうが軽い (推測。MapLibre の大きなデータの手引きによる) | https://maplibre.org/maplibre-gl-js/docs/API/classes/Marker/, https://developers.google.com/maps/documentation/javascript/advanced-markers/migration |
| `MarkerClusterer` (@googlemaps/markerclusterer) | MapLibre の GeoJSON ソースの `cluster: true`、Leaflet.markercluster | MapLibre はワーカーでクラスタを作る。クラスタの見た目はレイヤーの式で書く | https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/ |
| `InfoWindow` | MapLibre の `Popup`、Leaflet の `bindPopup()`、OpenLayers の `Overlay` | 地物をクリックして出すなら、MapLibre では `click` イベントで `queryRenderedFeatures` かイベントの `features` から属性を取って `Popup` を開く | https://maplibre.org/maplibre-gl-js/docs/API/classes/Popup/, https://maplibre.org/maplibre-gl-js/docs/examples/display-a-popup-on-click/, https://openlayers.org/en/latest/apidoc/module-ol_Overlay-Overlay.html |
| `Polyline`、`Polygon`、`Circle` | GeoJSON ソースと `line` / `fill` レイヤー (MapLibre)、Leaflet の `Polyline` / `Polygon` / `Circle` | MapLibre に円の図形は無いので、円を多角形にして GeoJSON で渡す (推測。turf の `circle` などで作る) | https://maplibre.org/maplibre-gl-js/docs/ |
| `Data` レイヤー (GeoJSON) | MapLibre の `geojson` ソース、Leaflet の `GeoJSON`、OpenLayers の `VectorSource` | Google の `setStyle` の関数は、MapLibre ではデータ駆動の式 (`["get", "属性"]`) に書き換える | [maplibre-gl-js](../../map-compare-library/references/libraries/maplibre-gl-js.md) |
| Heatmap レイヤー、Drawing ライブラリ (2026-05 に使えなくなった)、KmlLayer | MapLibre の `heatmap` レイヤー、描画は Terra Draw、KML は GeoJSON に変換してから読む | KML の変換は @tmcw/togeojson などの外部の道具 (未確認。版とライセンスは採用時に確かめる) | https://maplibre.org/maplibre-gl-js/docs/examples/create-a-heatmap-layer/, https://maplibre.org/maplibre-gl-js/docs/plugins/ |
| ストリートビュー | 代わりになる無償のものは無い。Mapillary などの街路画像サービスは別の規約で選ぶ (未確認) | Google の地図を外すとストリートビューも同じ画面に置けない (利用規約 3.2.3(e) の例 (ii)) | https://cloud.google.com/maps-platform/terms |
| Geocoding API、Places API (検索、オートコンプリート、詳細) | map-compare-arch の [search](../../map-compare-arch/references/capabilities/search.md) で選ぶ。MapLibre の UI は maplibre-gl-geocoder にジオコーダを渡して組む | 日本の住所や POI の網羅度は供給元で大きく違うので、移行前に代表的な検索語で結果を並べて比べる | https://github.com/maplibre/maplibre-gl-geocoder |
| Directions API、Routes API | map-compare-arch の [routing](../../map-compare-arch/references/capabilities/routing.md) で選ぶ | 所要時間、渋滞の反映、経路の形が変わる。利用者に見える差なので、比較の項目に入れる | |
| google.maps に近い書き方を残したい | Geolonia Maps SDK の maps-suite (`Map`、`Marker`、`InfoWindow`、`MarkerClusterer`、`Polyline`、`Data`、`Geocoder` などのクラスを持つ) | 候補の 1 つで、MapLibre GL JS の上に作られている。maps-suite のクラスが Google のクラスとどこまで同じ振る舞いをするかは確かめていない (未確認)。Geolonia のタイルは SDK を通して使うのが推奨で、他のライブラリからはサポート外 | [geolonia-maps (library)](../../map-compare-library/references/libraries/geolonia-maps.md), [geolonia-maps (provider)](../../map-compare-infra/references/providers/geolonia-maps.md) |

## 規約上の注意

- 移行元のデータ (キャッシュ、ジオコーディングの結果、プレイス ID) を移行後も使えるか: 条文から読める範囲では使えない。Geocoding API の緯度経度は 30 日までの一時キャッシュ (6.3.1) と、要求した利用者本人の画面の機能を支えるためだけの無期限キャッシュ (6.3.2、利用者ごとに分け、追加の呼び出しの代わりにしない) が許されるが、どちらも Google 以外の地図との併用禁止 (6.2) の下にある。Places API の緯度経度は 30 日まで (14.3)。place_id は保存してよいが (Google ID の保存の条項)、Google の API に渡す以外の使い道は無い。契約を終えたらサービスから得たコンテンツを削除する (利用規約 10.6(c))。このため、Google のジオコーディングで作った座標の列を新しい地図に載せる案は規約に反すると読める (推測。法的な判断ではない)。自社の住所データから、移行先のジオコーダで座標を付け直す。
- 移行中に移行元と移行先を併用してよいか: 同じ画面で Google の地図と他社の地図を並べる、Google の検索結果を他社の地図に出す、Google の地図から他社の地図へリンクする、のいずれも利用規約 3.2.3(e) の例に当たる。画面や利用者の単位で丸ごと切り替える (ある画面は Google だけ、別の画面は移行先だけ) なら当たらないと読めるが、「near a non-Google Map」の範囲は条文からは決まらない (未確認)。
- 例外: Places UI Kit は Google 以外の地図と一緒に使ってよいと定められ、3.2.3(e) より優先する (サービス固有規約 15.1)。ただし帰属表示の改変禁止と、キャッシュと書き出しの禁止は残る (15.3、15.4)。検索だけ Google に残したいときの選択肢になりうるが、費用と画面の制約は確かめていない (未確認)。

## 費用の変化

- Google は地図の読み込みと、検索、ジオコーディング、ルート検索の SKU ごとの従量課金である。移行先は課金単位が違う (タイルのリクエスト、地図の表示回数、MAU、自前配信の転送量) ので、map-compare-infra の [criteria](../../map-compare-infra/references/criteria.md) の「費用の見積もり方」で、月の地図表示回数と検索回数をそろえて並べる。単価は [google-maps](../../map-compare-infra/references/providers/google-maps.md) と移行先の provider の reference から写し、答える前に料金ページで確かめ直す。
- 地図だけ移すと安くなっても、検索とルート検索の代わりのサービスの費用が別にかかる。地図以外の費用を見積もりから落とさない。

## 移行の手順

1. コードから `google.maps.*` の使用箇所を全部洗い出し、上の表の行ごとに数える (`grep -rn "google\.maps\." src` など)。Places、Geocoding、Directions の呼び出しと、保存している place_id と座標の列も数える。
2. 保存しているデータを、自社のもの (住所、施設名) と Google 由来のもの (座標、place_id、営業時間などの Places のコンテンツ) に分ける。Google 由来のものは移行先で使わない前提で、付け直しの手順と費用を見積もる。
3. 検索とルート検索の移行先を map-compare-arch で決める。地図と同時に切り替える必要があるので、地図より後回しにしない。
4. 移行先のライブラリで、地図、マーカー、情報窓、検索の最小の画面を作り、代表的な画面と並べて比べる ([migration-plan](migration-plan.md) の「手順」)。
5. 画面か利用者の単位で丸ごと切り替える。同じ画面で混ぜない。
6. Google の API キーを止める前に、Google 由来のキャッシュと保存データを消したことを確かめる。

## 既にある移行の道具

- Geolonia の Agent Skills (MIT) が、Google Maps JavaScript API から maps-suite へ移す手順と `google.maps.*` と `geolonia.maps.*` の対応表を持つ ([geolonia-maps (library)](../../map-compare-library/references/libraries/geolonia-maps.md) の「主なプラグイン・拡張」、https://docs.geolonia.com/explanation/agent-skills/)。
- Google Maps JavaScript API から MapLibre GL JS や OpenLayers へ移す公式の移行ガイドは、MapLibre と OpenLayers の文書には見つからなかった (未確認)。
- React で書かれていれば、react-map-gl の `react-map-gl/maplibre` が宣言的な書き方を保てる (https://visgl.github.io/react-map-gl/docs/get-started)。

## 落とし穴

- 座標の順 (上記)。テストに経緯度の順を確かめる例を入れる。
- 地図の色、文字の大きさ、POI の出方は、移行先のスタイルと地図データで変わる。利用者からは「地図の質が落ちた」に見えるので、変わることを先に伝え、比べる画面を決めておく。
- Google の地図の上に重ねていた自社データの見た目 (アイコンの大きさ、線の太さ) は、ズームの段階が違うと別物に見える。ズームごとに並べて比べる。
- 帰属表示が変わる。Google のロゴを外し、移行先の帰属表示 (OpenStreetMap など) を出す ([attribution](../../map-legal-check/references/attribution.md))。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- MapLibre GL JS は BSD 3-Clause、Leaflet は BSD 2-Clause で、再配布の際に著作権表示が要る。react-leaflet は OSI 非承認の Hippocratic License 2.1 である ([leaflet](../../map-compare-library/references/libraries/leaflet.md))。
- 移行先の地図データが OpenStreetMap 由来なら ODbL の帰属表示が要り、地図から抽出したデータを配ると継承条件がかかる ([odbl](../../map-legal-check/references/odbl.md))。
- 自前でジオコーダを動かすなら、Nominatim は GPL-3.0 で、改変して機器ごと納品すると配布になる ([near-user-servers](../../map-compare-arch/references/edge/near-user-servers.md))。

## 出典

- https://cloud.google.com/maps-platform/terms (2026-11-11 確認。3.2.3(e) No Use With Non-Google Maps、10.6 Effects of Termination)
- https://cloud.google.com/maps-platform/terms/maps-service-terms (2026-11-11 確認。4.2、4.3 Directions、6.2、6.3 Geocoding、14.2、14.3 Places、15 Places UI Kit、Google ID 値のキャッシュ)
- https://developers.google.com/maps/documentation/javascript/advanced-markers/migration (Marker から AdvancedMarkerElement への移行。ページの存在を確認)
- https://maplibre.org/maplibre-gl-js/docs/API/classes/Marker/、https://maplibre.org/maplibre-gl-js/docs/API/classes/Popup/ (MapLibre の対応するクラス)
- https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/、https://maplibre.org/maplibre-gl-js/docs/examples/create-a-heatmap-layer/
- https://github.com/maplibre/maplibre-gl-geocoder
- https://visgl.github.io/react-map-gl/docs/get-started (`react-map-gl/maplibre` の import)

## 未確認のこと

- Google のクラウドのスタイルや JSON スタイル配列を MapLibre Style に変える道具の有無。
- 利用規約 3.2.3(e) の「near a non-Google Map」がどこまでを指すか (同じページの別のタブ、同じアプリの別の画面)。
- maps-suite のクラスと Google のクラスの振る舞いの一致の程度。
- Places UI Kit を他社の地図と組み合わせたときの費用と画面の制約。
