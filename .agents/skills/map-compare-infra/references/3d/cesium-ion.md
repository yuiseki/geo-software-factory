# Cesium ion

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | Cesium GS, Inc. (米国)。2024-09-06 に Bentley Systems が買収を発表し、同社の傘下 (https://www.bentley.com/news/bentley-systems-acquires-3d-geospatial-company-cesium/) |
| 公式サイト | https://cesium.com/platform/cesium-ion/ |
| 料金ページ | https://cesium.com/platform/cesium-ion/pricing/ |
| 利用規約・ライセンス | 利用規約 https://cesium.com/legal/terms-of-service/ (主な改定 2025-08-20、軽微な改定 2025-08-27)、第三者データの条件 https://cesium.com/legal/third-party-terms/ 、Google データの条件 https://cesium.com/legal/terms-for-google/ 、コンテンツ利用と帰属のガイド https://cesium.com/learn/ion/content-usage-and-attribution-guide/ |

## 概要

3D 地理空間データのホスティング、3D Tiles への変換 (タイリング)、ストリーミング配信を行う SaaS で、Cesium が整備した全球の 3D コンテンツ (Cesium World Terrain、Cesium OSM Buildings など) と、Google Photorealistic 3D Tiles や Bing Maps 空中写真などのパートナーデータを同じアカウントから配信する (https://cesium.com/platform/cesium-ion/content/)。利用者が点群、写真測量メッシュ、CityGML、BIM/CAD などをアップロードして 3D Tiles に変換し配信することもできる (https://cesium.com/platform/cesium-ion/pricing/)。日本向けには国土交通省 PLATEAU を統合した Japan 3D Buildings と、国土地理院の基盤地図情報による Japan Regional Terrain がある (https://cesium.com/platform/cesium-ion/content/japan-3d-buildings/)。

## データの性質

- 種類 (地形、建物、フォトリアル、点群、屋内): 地形 (Cesium World Terrain、Cesium World Bathymetry、Japan Regional Terrain)、建物 (Cesium OSM Buildings、Japan 3D Buildings、Vexcel 3D Cities)、フォトリアル (Google Photorealistic 3D Tiles)、画像 (Sentinel-2 雲なし 10 m、Bing Maps 空中写真 最大 15 cm、Google Maps 2D Tiles)、月と火星 (https://cesium.com/platform/cesium-ion/content/)。点群や屋内 (BIM) は利用者のアップロードを変換して配信する (https://cesium.com/platform/cesium-ion/pricing/)。
- 形式 (3D Tiles 1.0 / 1.1, quantized-mesh, glTF, CityGML, MVT など): 地形は quantized-mesh 1.0 (水域マスクと頂点法線の拡張あり) (https://cesium.com/platform/cesium-ion/content/cesium-world-terrain/)。建物は 3D Tiles (https://cesium.com/platform/cesium-ion/content/cesium-osm-buildings/)。画像は WMTS 系 (https://cesium.com/platform/cesium-ion/content/)。各タイルセットが 3D Tiles 1.0 と 1.1 のどちらかは未確認。CesiumJS は Apache-2.0 (https://github.com/CesiumGS/cesium 、LICENSE.md を 2026-11-10 に確認、最新リリース 1.147 は 2026-11-02 公開)。
- 詳細度 (LOD) とテクスチャの有無: Cesium OSM Buildings は OpenStreetMap から作った建物で、建物ごとの属性 (名称、住所など) を持つ (https://cesium.com/platform/cesium-ion/content/cesium-osm-buildings/)。テクスチャと LOD の記載はない。Japan 3D Buildings はテクスチャ付きと無しの建物を含む (https://cesium.com/platform/cesium-ion/content/japan-3d-buildings/)。LOD の記載はない。Google Photorealistic 3D Tiles はテクスチャ付きのフォトリアルメッシュ (https://cesium.com/platform/cesium-ion/content/)。
- カバー範囲 (国内の都市数、全球): Cesium World Terrain は全球約 1,000 m、北緯・南緯 60 度の間は 30〜90 m、英国 1〜2 m、米国 1〜30 m など。日本は World Terrain の高解像度地域に挙がっていない (https://cesium.com/platform/cesium-ion/content/cesium-world-terrain/)。Cesium OSM Buildings は全球 3 億 5,000 万棟超 (https://cesium.com/platform/cesium-ion/content/cesium-osm-buildings/)。Japan 3D Buildings は 210 超の区市町村、約 2,300 万棟 (https://cesium.com/platform/cesium-ion/content/japan-3d-buildings/)。Google Photorealistic 3D Tiles は 49 か国の 2,500 超の都市 (https://cesium.com/platform/cesium-ion/content/)。Google のフォトリアルが日本のどの都市を含むかは未確認。
- 更新頻度: Cesium OSM Buildings は四半期ごと (https://cesium.com/platform/cesium-ion/content/cesium-osm-buildings/)。そのほかのコンテンツは「継続的に更新」とだけ書かれ、周期の記載はない (https://cesium.com/platform/cesium-ion/content/)。

## 配信と対応ライブラリ

- 配信方法 (ホスティング、ダウンロード、自前変換): Cesium ion の SaaS からのストリーミングが基本 (https://cesium.com/platform/cesium-ion/)。Cesium のコンテンツの一部範囲を切り出す Clips 機能があり、Clips を組み込んで価値を加えた成果物 (Value-Added Clips) は契約終了後も永久に利用・配布・販売できる (https://cesium.com/legal/terms-of-service/ の 1.6、1.22、2.3)。自社環境で動かす Cesium ion Self-Hosted (Kubernetes 上、エアギャップ構成可) がある (https://cesium.com/platform/cesium-ion/cesium-ion-self-hosted/)。Sentinel-2 画像は Self-Hosted でオフライン利用できる (https://cesium.com/platform/cesium-ion/content/)。オープンソースの 3D Tiles 変換ツールで自前変換し、別のホスティングで配信することも Cesium ion を使わない選択肢としてある。
- 対応ライブラリ (CesiumJS, deck.gl, 3DTilesRendererJS, ゲームエンジンなど): CesiumJS、Cesium for Unreal / Unity / Omniverse は Cesium ion のロゴと帰属表示を自動で出す。それ以外の 3D Tiles クライアントからも使えるが、ロゴと帰属表示を自前で出す必要がある (https://cesium.com/learn/ion/content-usage-and-attribution-guide/ 、https://cesium.com/platform/cesium-ion/content/cesium-osm-buildings/)。
- API キー・アカウントの要否: Cesium ion アカウントとアクセストークンが必要 (https://cesium.com/platform/cesium-ion/content/cesium-world-terrain/)。Cesium のデータを使い続けるにはアカウントが有効でなければならない (https://cesium.com/learn/ion/content-usage-and-attribution-guide/)。

## 料金

- 無料枠と課金単位: Community プラン (無料、個人) は保存 10 GB、ストリーミング 15 GB/月、Google Photorealistic のルートタイル 1,000/月、Global Imagery のセッション 1,000/月、ジオコーディング 50,000/月、Reality Modeling 20 ギガピクセル/月など (USD、2026-11-10 確認) (https://cesium.com/platform/cesium-ion/pricing/)。アプリ数とエンドユーザー数に上限はないが、使用量はアカウントの枠に収める (同出典)。
- 従量単価・契約形態 (問い合わせ制ならそう書き、金額を推測しない): Commercial は個人 149 USD/月、チーム 524 USD/月 (保存 100 GB、ストリーミング 150 GB/月、Google ルートタイル 5,000/月、5 人まで)。Premium は個人 499 USD/月、チーム 874 USD/月 (保存 500 GB、ストリーミング 500 GB/月、Google ルートタイル 10,000/月)。Custom は問い合わせ制 (https://cesium.com/platform/cesium-ion/pricing/、2026-11-10 確認)。月払いと年払いを選べるが年払いの金額は掲載されていない。超過時の料金は料金ページに記載がなく、利用規約は上限超過に追加料金がかかりうるとだけ書く (https://cesium.com/legal/terms-of-service/ の 4.1)。組織外に提供するソリューションへ組み込む場合は統合用の価格とライセンスがあり問い合わせ制 (https://cesium.com/platform/cesium-ion/pricing/)。Cesium ion Self-Hosted の価格は問い合わせ制 (https://cesium.com/platform/cesium-ion/cesium-ion-self-hosted/)。

## 利用規約上の制約

- 商用利用、政府・公共案件での利用: 無料の Community は個人・非商用、資金提供のない教育活動、商用・政府開発の評価目的に限る。年間総収入または調達額が 5 万 USD を超える会社、政府案件、資金提供を受けた教育研究、無料枠を超える利用には有償の商用ライセンスが必要 (https://cesium.com/platform/cesium-ion/pricing/)。つまり自治体案件は評価段階を除き無料枠を使えない。政府機関が発注者の場合、ライセンスは注文書に記載した機関・部署に限られる (https://cesium.com/legal/terms-of-service/ の 1.23)。利用規約はサービスを第三者がアクセスできない状態に保ち、第三者のためのサービスとして運用しないことを求める (同 2.2.1)。受託開発で発注者に Cesium ion を組み込んだシステムを納める場合は、料金ページの「組織外で使うソリューションへの組み込みは問い合わせ」に当たる (https://cesium.com/platform/cesium-ion/pricing/)。AI モデルの学習にサービスや出力を使うことは、明示の許可がない限り禁止 (https://cesium.com/legal/terms-of-service/ の 2.2.4(xiii))。
- キャッシュ・ダウンロード・自前ホストの可否: Cesium のデータ出力をオフラインや切断環境向けに複製・保存・再配布してはならない (Clips を除く)。キャッシュは、ほかのインターネット通信も対象にする性能目的の一般的なクライアント側・プロキシのキャッシュに限り可 (https://cesium.com/legal/terms-of-service/ の 2.2.2)。契約終了後は Cesium のデータ出力を表示・利用できない (同 2.2)。Bing のコンテンツのキャッシュは HTTP ヘッダの期間まで (https://cesium.com/legal/third-party-terms/)。Google のコンテンツは明示の許可がない限りキャッシュ不可、保存や再ホストのためのダウンロード不可、抽出・スクレイピング不可、Google 以外の地図と同じアプリで併用不可、緊急対応サービスなど高リスク用途に使用不可 (https://cesium.com/legal/terms-for-google/)。自前ホストは Cesium ion Self-Hosted (問い合わせ制) で可能。Self-Hosted と組み合わせる場合も Google Photorealistic 3D Tiles と Bing 空中写真は SaaS アカウントから使う (https://cesium.com/platform/cesium-ion/cesium-ion-self-hosted/)。利用者自身がアップロードしたデータから作ったタイルセットをダウンロードできるかは未確認。
- 帰属表示の要件: 「Cesium ion」ロゴをアプリのメイン画面に目立つ形で表示する (モバイル・没入型アプリはスプラッシュか About 画面でも可) (https://cesium.com/legal/terms-of-service/ の 2.2.3)。データの帰属表示を出し、静止画や動画では「Data attribution」のリンク文字だけでなく帰属の中身を見える形で入れる。Google のデータを含む場合は Google Maps ロゴを表示する (https://cesium.com/learn/ion/content-usage-and-attribution-guide/)。Cesium OSM Buildings は「© OpenStreetMap contributors」 (https://cesium.com/platform/cesium-ion/content/cesium-osm-buildings/)。Japan 3D Buildings は「3D City Model Data (Ministry of Land, Infrastructure and Transport) Created by Processing」 (https://cesium.com/platform/cesium-ion/content/japan-3d-buildings/)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): Cesium OSM Buildings は ODbL の OpenStreetMap データを含む (https://cesium.com/legal/third-party-terms/)。ODbL では、地図表示や画像などの生成物 (Produced Work) を公開するときは帰属表示が要る。OSM Buildings に自前のデータを混ぜて作った派生データベースを公開・配布する場合は、その派生データベースを ODbL で提供するか、作成方法とデータを入手可能にする必要がある (https://opendatacommons.org/licenses/odbl/1-0/ 、https://www.openstreetmap.org/copyright)。SaaS で 3D 表示として提供するだけなら生成物の公開に当たり、帰属表示が主な義務 (推測。ODbL 4.5、4.6 の一般解釈による)。ただし Cesium の利用規約はそもそも Cesium のデータ出力の複製・再配布を禁じるので、OSM Buildings をデータベースとして再配布することは Cesium 側の規約で止まる (https://cesium.com/legal/terms-of-service/ の 2.2.2)。Japan 3D Buildings と Japan Regional Terrain は PLATEAU のサイトポリシーに従う (https://cesium.com/legal/third-party-terms/)。PLATEAU のコンテンツは公共データ利用規約 (第 1.0 版) で CC BY 4.0 と互換で、加工したときは加工した旨を書き、国が作成したかのように見せてはならない (https://www.mlit.go.jp/plateau/site-policy/)。CesiumJS は Apache-2.0 でコピーレフトはない (https://github.com/CesiumGS/cesium)。

## 安定性と運用

- SLA・運用形態 (本運用か試験運用か): 本運用の商用 SaaS。ただし利用規約に稼働率の約束はなく、中断や誤りのない運用を保証しないと書く (https://cesium.com/legal/terms-of-service/ の 6.1)。無料プランへのサポート応答は保証されない (同 3)。Azure Maps 画像、Reality Modeling、BIM/CAD Tiler with Database API は Technology Preview で、Azure Maps 画像は本番利用しないよう書かれている (https://cesium.com/platform/cesium-ion/pricing/)。Custom 契約での SLA の有無は未確認。

## 向いている場面

- CesiumJS や Cesium for Unreal / Unity で、地形、建物、フォトリアル 3D をすぐにそろえて表示したい試作や評価 (評価目的なら無料枠も使える)。
- 点群、写真測量、BIM などの自社データを 3D Tiles に変換して配信したいが、変換基盤を自前で持ちたくない場面。
- Google Photorealistic 3D Tiles を Cesium の地形やデータと合わせて使いたい場面 (Google 以外の地図と併用しない構成に限る)。
- オフラインやエアギャップ環境が要件で、Self-Hosted の費用を負担できる場面。

## 向いていない場面

- 無料枠での自治体・政府案件 (評価段階を除き有償ライセンスが必要)。
- 取得したデータを自前サーバーにキャッシュ・再ホストして配る構成 (Clips と Self-Hosted を除き不可。Google データは不可)。
- 受託開発で発注者に納めるシステム (組織外への組み込みは個別の統合ライセンスが必要)。
- 日本の地形を高解像度で見せたい場合に Cesium World Terrain だけを使う構成 (日本は高解像度地域に挙がっていない。Japan Regional Terrain を使う)。
- 稼働率の契約上の保証が必要な用途 (標準の規約に SLA がない)。

## 出典

- https://cesium.com/platform/cesium-ion/
- https://cesium.com/platform/cesium-ion/pricing/
- https://cesium.com/platform/cesium-ion/content/
- https://cesium.com/platform/cesium-ion/content/cesium-world-terrain/
- https://cesium.com/platform/cesium-ion/content/cesium-osm-buildings/
- https://cesium.com/platform/cesium-ion/content/japan-3d-buildings/
- https://cesium.com/platform/cesium-ion/cesium-ion-self-hosted/
- https://cesium.com/legal/terms-of-service/
- https://cesium.com/legal/third-party-terms/
- https://cesium.com/legal/terms-for-google/
- https://cesium.com/learn/ion/content-usage-and-attribution-guide/
- https://github.com/CesiumGS/cesium
- https://www.bentley.com/news/bentley-systems-acquires-3d-geospatial-company-cesium/
- https://opendatacommons.org/licenses/odbl/1-0/
- https://www.openstreetmap.org/copyright
- https://www.mlit.go.jp/plateau/site-policy/

## 未確認のこと

- 各タイルセットの 3D Tiles の版 (1.0 か 1.1 か): コンテンツページに記載がない。
- Cesium OSM Buildings と Japan 3D Buildings の LOD: コンテンツページに記載がない。
- Google Photorealistic 3D Tiles の日本の対象都市: Cesium のページは国数と都市数だけを書く。
- 超過料金の単価と年払いの金額: 料金ページに記載がない。
- 利用者がアップロードしたデータから作ったタイルセットのダウンロード可否: 規約とガイドに直接の記載が見当たらなかった。
- Custom 契約と Self-Hosted の SLA と価格: 問い合わせ制で公開されていない。
- Cesium World Terrain の更新頻度と日本での実解像度: ページに記載がなく、日本が高解像度地域に含まれないことしか分からない。
- Clips を使えるプランと切り出せる対象: 利用規約は定義だけを書き、プラン別の扱いを書いていない。
