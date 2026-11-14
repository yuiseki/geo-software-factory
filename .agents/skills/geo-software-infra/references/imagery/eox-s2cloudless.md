# EOX Sentinel-2 cloudless

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | EOX IT Services GmbH (オーストリア)。製品名は現在「EOxCloudless」 (https://cloudless.eox.at/documentation/license) |
| 公式サイト | https://cloudless.eox.at/ (旧 https://s2maps.eu/ はここへ 301 リダイレクトする) |
| 料金ページ | https://cloudless.eox.at/pricing (金額は FAQ https://cloudless.eox.at/documentation/faq に記載) |
| 利用規約・ライセンス | ライセンス要約 https://cloudless.eox.at/documentation/license 、商用ライセンス本文 (EOX Commercial Attribution-RestrictedUse 1.2) https://cloudless.eox.at/license-legal/ |

## 概要

Copernicus Sentinel-2 の画像から雲を除いた全球の年次モザイクを、10 m 解像度のトゥルーカラー画像として提供する (https://cloudless.eox.at/documentation/product-list)。年版 (vintage) ごとに 1 枚の全球モザイクがあり、無料の WMTS / WMS エンドポイントで閲覧でき、商用利用やファイル納品は年版単位の有償ライセンスで買う (https://cloudless.eox.at/documentation/faq)。ライセンスは年版で異なり、2016 年版は CC BY 4.0、2018〜2025 年版は非商用の CC BY-NC-SA 4.0 である (https://cloudless.eox.at/pricing)。

## 画像の性質

- 元になる衛星・航空機とセンサー: ESA / Copernicus の Sentinel-2 (MSI)。製品は Sentinel-2 Level-2A 画像に基づく (https://cloudless.eox.at/documentation/product-list)。処理の入力には AWS 上の EarthSearch (Level-2A) と Copernicus Data Space の STAC カタログを使う (https://cloudless.eox.at/documentation/processing)。
- 地上解像度 (地域ごとに違えば国内と全球を分けて): 全球一律 10 m (国内も同じ) (https://cloudless.eox.at/documentation/product-list)。
- 撮影時期と更新頻度: 年 1 回の年版。WMTS には 2016〜2025 年の各年版のレイヤがある (`s2cloudless-2017` から `s2cloudless-2025`、および年なしの `s2cloudless` レイヤのタイトルが 2016 年版) (https://tiles.maps.eox.at/wmts/1.0.0/WMTSCapabilities.xml)。購入した年版の後継年版は含まれず、新しい年は別途購入する (https://cloudless.eox.at/documentation/faq)。
- 過去画像 (時系列) の有無と期間: 2016〜2025 年の年版を WMTS で切り替えて閲覧できる (https://tiles.maps.eox.at/wmts/1.0.0/WMTSCapabilities.xml)。日単位・月単位の時系列はない。
- 雲・季節の処理 (モザイクの作り方): 全球を地域に分け、地域ごとに期間を変えて「夏らしい」モザイクになるようシーンを集め、雲・影マスクと輝度閾値で画素を選ぶ。BRDF 補正 (HLS に倣った反射率の正規化) を行う (https://cloudless.eox.at/documentation/processing)。地域ごとの具体的な期間は公開されていない。
- 国内のカバー範囲: 全球モザイクなので日本全域を含む (https://cloudless.eox.at/documentation/product-list)。日本向けの撮影期間は未確認。

## 提供形式

- 形式 (XYZ / WMTS / COG / STAC など): 無料の WMTS (https://tiles.maps.eox.at/wmts/1.0.0/WMTSCapabilities.xml) と WMS (https://tiles.maps.eox.at/map?service=WMS&request=GetCapabilities)。WMTS は EPSG:3857 (GoogleMapsCompatible) と EPSG:4326 の TileMatrixSet を持ち、REST 形式 `https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2024_3857/default/GoogleMapsCompatible/{z}/{y}/{x}.jpg` で XYZ として使える (2026-11-10 に API キーなしで HTTP 200 を確認) (https://cloudless.eox.at/documentation/usage)。有償製品は Viewing Basic (タイル化 GeoTIFF、WMTS 風のピラミッド配置)、Viewing Ready (GeoPackage / SQLite キャッシュ、JPEG)、Exploitation Starter / Ready (タイル化 GeoTIFF、Ready は 12 bit 反射率を uint16 で格納) の 4 種 (https://cloudless.eox.at/documentation/product-list)。COG と STAC での提供は製品一覧に記載がない。MBTiles 変換は有償オプション (https://cloudless.eox.at/documentation/faq)。
- 最大ズーム: EPSG:3857 で 14、EPSG:4326 で 13 (https://cloudless.eox.at/documentation/product-list)。
- 対応ライブラリと API キーの要否: 標準の WMTS / WMS / XYZ なので OpenLayers、Leaflet、MapLibre GL JS、QGIS などで読める (公式ページは GeoPackage を QGIS / ArcGIS で開けるとだけ書く) (https://cloudless.eox.at/documentation/usage)。無料エンドポイントは API キー不要 (2026-11-10 に実リクエストで確認)。数値の利用上限は公開されておらず、急なトラフィックは自動で減速・一時遮断される (https://cloudless.eox.at/documentation/faq)。

## 料金

- 無料枠と課金単位: ライセンス条件を守る限り無料で WMTS / WMS を使える。ただし 2018 年版以降は非商用に限る。無料エンドポイントに稼働率の SLA はない (https://cloudless.eox.at/pricing 、https://cloudless.eox.at/documentation/faq)。課金単位は年版ごとの買い切り。
- 従量単価・契約形態 (問い合わせ制ならそう書き、金額を推測しない): FAQ 記載の価格 (EUR、VAT 別、2026-11-10 確認)。Viewing Ready 2025 年版が 6,000 EUR (永久ライセンス、一括払い)、Viewing Ready 2018〜2024 年版が年版ごとに 5,000 EUR、Exploitation Starter の国・地域単位の切り出しが 1,500 EUR から、MBTiles 変換が追加 1,000 EUR、専用ホスティングの WMTS / WMS エンドポイントが年 6,000 EUR (本番用 SLA 付き)。スタートアップ向けや試験導入向けの割引価格はない (https://cloudless.eox.at/documentation/faq)。季節別モザイク、色補正、一括納品などの個別注文は見積もり制 (https://cloudless.eox.at/pricing)。概算の例として、最新の 2025 年版を MBTiles にして自前ホストで商用利用する場合の初期費用は「Viewing Ready 2025 年版 6,000 EUR + MBTiles 変換 1,000 EUR = 7,000 EUR (VAT 別)」となる (仮定: 全球の Viewing Ready を 1 年版だけ購入し、変換オプションを 1 回使う。自前ホストの費用は含まない)。翌年以降に新しい年版へ更新するなら、その年版を別途購入する。

## 利用規約上の制約

- 商用利用: 2016 年版は CC BY 4.0 で商用利用できる (無料エンドポイントは SLA なし)。2018 年版以降の商用利用には有償の EOX Commercial Attribution-RestrictedUse 1.2 ライセンスが要る。収益化したプラットフォーム、代理店、B2B ポータルは非商用には当たらない。商用の本番アプリは 2018 年版以降の公開 WMS / WMTS エンドポイントを使えず、専用ホスティングかオフラインキャッシュが必要 (https://cloudless.eox.at/documentation/faq 、https://cloudless.eox.at/pricing)。2017 年版のライセンスは未確認。
- キャッシュ・ダウンロード・二次加工 (解析、学習データ) の可否: 商用ライセンスは全世界・永久で、Web、SaaS、モバイルアプリ、オフラインパック、自前ホストを含む。アプリ内キャッシュと利用者操作による地域オフラインパックは可だが、タイルは埋め込まれた状態に留め、エンドユーザーが生データとして取り出せてはならない。元モザイクを単体のデータセットやタイルサービスとして再販・再許諾・再配布することは不可 (https://cloudless.eox.at/documentation/faq)。商用ライセンスは「直接再配布」を有償・無償とも禁じ、再許諾は書面が必要、加工物 (Adapted Material) にも同じ条件が及ぶ (https://cloudless.eox.at/license-legal/ の 2(a)(2), 2(a)(3), 3(b)(1))。再投影・リサンプル・処理は可 (https://cloudless.eox.at/documentation/faq)。AI の学習データ化について、商用ライセンス本文と FAQ に明示の規定はない (未確認)。
- 帰属表示の要件: 「EOxCloudless https://cloudless.eox.at by EOX IT Services GmbH (Contains modified Copernicus Sentinel data "year")」を画像の表示場所で見える形で表示する。対話的な地図では地図 UI 内に表示する。2026 年 6 月から Data 製品と Viewing 製品で表記を統一した (https://cloudless.eox.at/documentation/license)。エクスポート、スクリーンショット、動画にも帰属表示を入れる (https://cloudless.eox.at/documentation/faq)。欧州委員会や ESA の推奨を示唆してはならない (https://cloudless.eox.at/documentation/license)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): 2018〜2025 年版の CC BY-NC-SA 4.0 は非商用条件と継承条件を持つ (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)。組み込み: 有償サービスや広告収益のあるサービス、受託開発の成果物など商業目的の製品には無料版を組み込めない。改変: 色調整、切り出し、合成などの加工物を共有するなら同じ CC BY-NC-SA 4.0 (または互換ライセンス) で出す必要があり、加工した旨の表示も要る。配布: 帰属表示とライセンスの明示が必要で、非商用に限る。SaaS 提供: CC 4.0 では公衆への利用可能化も「共有」に当たるので、地図配信サービスとして提供すれば上記の非商用・継承条件がかかる。商用 SaaS は有償ライセンスが必要。解析・学習データ化: NC 条件は使い道全体にかかるため、商業目的のモデル学習や解析は無料版では行えないと読むのが安全 (推測)。2016 年版の CC BY 4.0 は帰属表示だけが条件で継承条件はない (https://creativecommons.org/licenses/by/4.0/legalcode)。有償の商用ライセンスは独自ライセンスで、加工物にも同じ制限が及び、直接再配布は禁止 (https://cloudless.eox.at/license-legal/)。

## 向いている場面

- 非商用の研究、教育、NGO、個人の地図で、全球をそろった色調の衛星画像で覆いたい場面 (https://cloudless.eox.at/documentation/license)。
- 縮尺 1:50,000 程度より小さい広域表示の背景 (最大ズーム 14、10 m 解像度)。
- 商用でも、年版を買い切りで自前ホストし、継続費用をホスティング費だけにしたい場面。
- 2016 年版で足りるなら、CC BY 4.0 で商用でも無料で使える。

## 向いていない場面

- 建物や道路を判読する高ズーム表示 (10 m 解像度、ズーム 14 まで)。
- 災害対応など、直近の状況を見る必要がある用途 (年 1 回の年版)。
- 商用製品で公開の無料エンドポイントを直接使う構成 (2018 年版以降は不可、SLA なし)。
- 元画像をデータセットやタイルサービスとして顧客に再配布する用途 (商用ライセンスでも禁止)。

## プライバシーとテレメトリ (2026-11-14 確認)

- **アクセスログとテレメトリ**: EOX の公開 WMTS / WMS エンドポイントへ直接アクセスする場合は、通常の HTTP サーバーアクセスログ (IP アドレス・リクエスト URL 等) が配信側で記録されうる。独自 SDK による端末テレメトリは無い。自前でタイルを取得・再配信できる契約/ライセンス範囲であれば、エンドユーザーの接続を自前サーバーで完結できる。公開エンドポイントのログ保持期間は未確認。

## 出典

- https://cloudless.eox.at/
- https://cloudless.eox.at/preview
- https://cloudless.eox.at/pricing
- https://cloudless.eox.at/documentation/license
- https://cloudless.eox.at/documentation/faq
- https://cloudless.eox.at/documentation/product-list
- https://cloudless.eox.at/documentation/processing
- https://cloudless.eox.at/documentation/usage
- https://cloudless.eox.at/license-legal/
- https://tiles.maps.eox.at/wmts/1.0.0/WMTSCapabilities.xml
- https://tiles.maps.eox.at/map?service=WMS&request=GetCapabilities
- https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
- https://creativecommons.org/licenses/by/4.0/legalcode

## 未確認のこと

- 2017 年版のライセンス: WMTS にレイヤ (`s2cloudless-2017`) はあるが、料金ページとライセンス要約は 2016 年版と 2018〜2025 年版にしか触れていない。
- 日本を含む各地域の撮影期間: 処理説明は地域ごとに期間を変えるとだけ書き、具体的な期間を公開していない。
- 無料エンドポイントの数値の利用上限: FAQ は数値を公開していないと書く。
- AI の学習データ化の可否: 商用ライセンス本文と FAQ に規定がない。無料版の扱いは CC BY-NC-SA の一般解釈による推測。
- 2016 年版の商用ライセンス価格と Viewing Basic / Exploitation Ready の価格: FAQ に記載がなく、購入ページ (https://cloudless.eox.at/checkout) は取得時に金額を表示しなかった。
- 年版ごとの公開日: 公式ページに記載が見当たらなかった。
