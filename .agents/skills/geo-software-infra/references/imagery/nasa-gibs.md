# NASA GIBS

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | NASA。Earth Science Data and Information System (ESDIS) の一部として運用 (https://nasa-gibs.github.io/gibs-api-docs/) |
| 公式サイト | https://www.earthdata.nasa.gov/gibs 、API ドキュメント https://nasa-gibs.github.io/gibs-api-docs/ |
| 料金ページ | なし (無料の公開サービス。「free, open, and interoperable」と説明している) (https://www.earthdata.nasa.gov/gibs) |
| 利用規約・ライセンス | NASA Earth science のデータ利用方針 https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance (NASA 主導ミッションのデータは CC0) |

## 概要

NASA の地球観測衛星データを可視化した画像を、あらかじめ生成したタイルとして WMTS / WMS / TWMS で配信するサービス (https://nasa-gibs.github.io/gibs-api-docs/ 、https://nasa-gibs.github.io/gibs-api-docs/access-basics/)。可視化の数は 1,000 を超え (API ドキュメントは 1,200 超と書く)、多くは毎日更新され、観測から数時間で載る (https://www.earthdata.nasa.gov/gibs 、https://nasa-gibs.github.io/gibs-api-docs/available-visualizations/)。トゥルーカラー画像のほか、雲、エアロゾル、火災、海面水温、積雪などの物理量の可視化を含む。2026-11-10 時点の EPSG:3857 の WMTS GetCapabilities には 1,330 レイヤがある (https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/1.0.0/WMTSCapabilities.xml)。

## 画像の性質

- 元になる衛星・航空機とセンサー: Terra / Aqua の MODIS、Suomi NPP / NOAA-20 などの VIIRS、Landsat と Sentinel-2 を合わせた HLS、Sentinel-1 由来の OPERA、NISAR などのレイヤがある (https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/1.0.0/WMTSCapabilities.xml)。Suomi NPP は新しいデータの配信を止めており、代替製品への移行が告知されている (https://www.earthdata.nasa.gov/gibs)。
- 地上解像度 (地域ごとに違えば国内と全球を分けて): 全球一律で、国内も同じ。日次トゥルーカラーの MODIS / VIIRS Corrected Reflectance は 250 m 相当 (EPSG:3857 の TileMatrixSet が GoogleMapsCompatible_Level9)。HLS (L30 / S30) と Landsat WELD は 30 m 相当 (同 Level12)。NISAR と参照レイヤの一部は Level13 (https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/1.0.0/WMTSCapabilities.xml)。EPSG:3857 の 1,330 レイヤのうち 825 が Level6 (2 km 相当) で、多くは低解像度の物理量可視化である (同出典を集計)。
- 撮影時期と更新頻度: 多くのレイヤが毎日更新され、多くの製品は観測から 3〜5 時間で利用できる (https://www.earthdata.nasa.gov/gibs)。LANCE が作る準リアルタイム (NRT) 製品は観測から 3.5 時間以内に GIBS に載る (https://nasa-gibs.github.io/gibs-api-docs/available-visualizations/)。当日分は取得・処理が終わっていないため空タイルが返ることがある (https://nasa-gibs.github.io/gibs-api-docs/access-basics/)。
- 過去画像 (時系列) の有無と期間: あり。時刻は `YYYY-MM-DD` (サブ日次は `YYYY-MM-DDTHH:MI:SSZ`) で指定する (https://nasa-gibs.github.io/gibs-api-docs/access-basics/)。2026-11-10 時点の Capabilities では、MODIS_Terra_CorrectedReflectance_TrueColor が 2000-02-24 から当日まで日次、VIIRS_NOAA20 が 2018-01-05 から、HLS_L30 が 2013 年から、HLS_S30 が 2015 年から、Landsat WELD が 1983〜2001 年の年次・月次 (https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/1.0.0/WMTSCapabilities.xml)。製品によっては約 30 年分ある (https://www.earthdata.nasa.gov/gibs)。WMTS の GetCapabilities はレイヤごとに直近 100 期間しか列挙しないため、全期間は DescribeDomains で取る (https://nasa-gibs.github.io/gibs-api-docs/access-basics/)。
- 雲・季節の処理 (モザイクの作り方): 日次レイヤはその日の観測をそのまま並べたもので、雲は除去されず、軌道の間に欠損帯がある。複数の製品版がある場合は提供者と調整した「Best Available」のレイヤを `best` エンドポイントで返す (https://nasa-gibs.github.io/gibs-api-docs/access-advanced-topics/)。雲なしモザイクに当たるのは Landsat WELD の年次・月次合成など一部レイヤのみ (https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/1.0.0/WMTSCapabilities.xml)。
- 国内のカバー範囲: MODIS / VIIRS の日次レイヤは全球なので日本全域を含む。HLS など 30 m レイヤの日本での観測頻度は未確認。

## 提供形式

- 形式 (XYZ / WMTS / COG / STAC など): WMTS (REST と KVP) `https://gibs.earthdata.nasa.gov/wmts/epsg{code}/best/`、WMS 1.1.1 / 1.3.0 `https://gibs.earthdata.nasa.gov/wms/epsg{code}/best/wms.cgi?`、TWMS。`best` を `std` / `nrt` / `all` に変えると標準品質、準リアルタイム、全版を選べる。投影は EPSG:4326、EPSG:3857、極域の EPSG:3413 (北極、NSIDC 海氷極ステレオ) と EPSG:3031 (南極極ステレオ)。WMTS REST の URL を `{z}/{y}/{x}` のテンプレートにすれば XYZ として使える (例 `.../MODIS_Terra_CorrectedReflectance_TrueColor/default/2026-11-01/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg`) (https://nasa-gibs.github.io/gibs-api-docs/access-basics/)。EPSG:3857 ではベクタの可視化は WMTS で提供されない (https://nasa-gibs.github.io/gibs-api-docs/access-advanced-topics/)。COG と STAC での配信は GIBS のドキュメントに記載がない (元データは各 DAAC から別に取得する)。
- 最大ズーム: レイヤごとに違う。EPSG:3857 では最大 Level13、トゥルーカラー日次 (MODIS / VIIRS) は Level9、HLS は Level12 (https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/1.0.0/WMTSCapabilities.xml)。
- 対応ライブラリと API キーの要否: OpenLayers、Cesium、Mapbox GL、GDAL、Python からの利用例が公式ドキュメントにある (https://nasa-gibs.github.io/gibs-api-docs/map-library-usage/)。GIS アプリからの利用は別ページで案内している (https://nasa-gibs.github.io/gibs-api-docs/gis-usage/)。標準の WMTS / XYZ なので Leaflet や MapLibre GL JS でも読める。時刻をタイル URL に入れる必要があるので、日付切り替えはクライアント側でソース URL を差し替えて行う。API キーは不要 (2026-11-10 に WMTS タイルを認証なしで取得し HTTP 200 を確認)。並列取得には HTTP/1.1 のドメインシャーディングを使うよう案内している (https://nasa-gibs.github.io/gibs-api-docs/access-advanced-topics/)。

## 料金

- 無料枠と課金単位: 無料。課金はない (https://www.earthdata.nasa.gov/gibs)。
- 従量単価・契約形態 (問い合わせ制ならそう書き、金額を推測しない): なし。有償の SLA 契約や専用エンドポイントの提供は見当たらない (未確認)。

## 利用規約上の制約

- 商用利用: NASA 主導ミッションのデータは、利用制限やライセンスの表示がない限り CC0 で、利用に制限はない (https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance)。商用利用も CC0 の範囲で可。ただし NASA 以外のデータは提供元のライセンスに従い、NASA の素材を商用製品・サービスの推奨を示唆する形で使ってはならない (同出典)。
- キャッシュ・ダウンロード・二次加工 (解析、学習データ) の可否: CC0 のデータは複製、加工、解析、再配布に制限がない (https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance)。タイルのキャッシュや一括取得を禁じる規定、レート制限は公式ドキュメントに見当たらない (https://nasa-gibs.github.io/gibs-api-docs/access-advanced-topics/)。ただし GIBS の画像は可視化用の 8 bit RGB / カラーマップ画像であり、解析には元データ (各 DAAC の科学データ) を使うのが本来の形 (推測)。
- 帰属表示の要件: クライアントや発表で GIBS を使う場合、「We acknowledge the use of imagery provided by services from NASA's Global Imagery Browse Services (GIBS), part of NASA's Earth Science Data and Information System (ESDIS).」の記載を求めている (https://nasa-gibs.github.io/gibs-api-docs/)。データ利用方針も NASA を出典として示すよう求める (https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance)。地図上の帰属表示としては「NASA GIBS」と元の衛星・センサー名を出すのが妥当 (推測)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): NASA 主導ミッションのデータ (CC0) には継承条件も非商用条件もなく、組み込み、改変、配布、SaaS 提供、学習データ化のいずれにも義務はない (帰属は要請)。注意点は、GIBS のレイヤの中に NASA 以外の機関のデータや他機関の衛星データを使ったものがあり、それらは提供元のライセンスに従う点 (https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance)。どのレイヤが該当するかはレイヤごとに確かめる必要がある (未確認)。

## 向いている場面

- 日々の地球規模の変化 (台風、黄砂、林野火災の煙、積雪、海氷) を日付を切り替えながら見せる地図。
- 2000 年以降の日次の時系列をキー不要・無料で使いたい教育、報道、研究用途。
- 北極・南極を極ステレオ投影で表示したい用途 (EPSG:3413 / 3031)。
- 商用製品の背景や補助レイヤとして、ライセンス上の制約が少ない画像を使いたい場面 (CC0 のレイヤに限る)。

## 向いていない場面

- 都市や建物を判読する高解像度の背景地図 (日次トゥルーカラーは 250 m 相当、最大でも 30 m 相当)。
- 雲のない見栄えのよい背景地図 (日次レイヤは雲と欠損帯を含む)。
- 稼働率の保証が必要な商用サービスの唯一の画像源 (SLA の記載がない)。
- 反射率などの数値を使う解析 (配信されるのは可視化画像)。

## プライバシーとテレメトリ (2026-11-14 確認)

- **アクセスログ方針**: NASA Web Privacy Policy に従い、セキュリティ・サイト管理のために必要な期間に限り生ログ (IP アドレス等) が一時保存されるが、認可された法執行機関の調査を除き、個人の特定や利用習慣の追跡は行わないと明記している。独自 SDK による端末テレメトリは無い。

## 出典

- https://www.earthdata.nasa.gov/gibs
- https://nasa-gibs.github.io/gibs-api-docs/
- https://nasa-gibs.github.io/gibs-api-docs/access-basics/
- https://nasa-gibs.github.io/gibs-api-docs/access-advanced-topics/
- https://nasa-gibs.github.io/gibs-api-docs/available-visualizations/
- https://nasa-gibs.github.io/gibs-api-docs/map-library-usage/
- https://nasa-gibs.github.io/gibs-api-docs/gis-usage/
- https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/1.0.0/WMTSCapabilities.xml
- https://www.earthdata.nasa.gov/engage/open-data-services-software-policies
- https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance

## 未確認のこと

- SLA、稼働率、レート制限: GIBS のドキュメントと Earthdata の GIBS ページに記載がない。
- どのレイヤが NASA 以外のデータでライセンスが異なるか: レイヤ単位のライセンス表示を一覧で確かめる手段を見つけられなかった。
- HLS など 30 m レイヤの日本での観測頻度と欠損: レイヤごとの観測幾何を調べていない。
- GIS アプリ別ページ (gis-usage) と Python ページ (python-usage) の中身: ページの存在は API ドキュメントの目次で確認したが、記述は読んでいない。
- 有償の SLA や専用エンドポイントの提供有無: 公式ページに記載がなく、存在を確認できなかった。
