# ノーコードの地図作成サービス (Google マイマップ、ArcGIS Online のアプリ、uMap、Felt)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 対象 | Google マイマップ (My Maps)、ArcGIS Online のアプリ (ArcGIS StoryMaps、ArcGIS Experience Builder、ArcGIS Web AppBuilder)、uMap (最新の安定版 3.8.1、2026-08-19。4.0.0a0 が 2026-10-29 に出ている、https://github.com/umap-project/umap/releases)、Felt |
| 種類 | ブラウザの画面で地図を作り、URL か iframe で配る。ライブラリでも、自前でビルドする土台 (TerriaJS など) でもない |
| ライセンス | Google マイマップ、ArcGIS Online、Felt は商用のサービスで、ソースは公開されていない。uMap は AGPL-3.0-or-later (https://github.com/umap-project/umap/blob/master/LICENSE) |
| 運営主体 | Google、Esri、uMap はコミュニティと寄付で開発し公開インスタンスは各国の OpenStreetMap の団体が運営する (https://umap-project.org/)、Felt は Felt 社 |

## 概要

点や線を手で描く、表計算のファイルを読み込む、といった作業をブラウザの画面だけで済ませ、できた地図を URL や iframe で Web サイトに埋め込むサービスである。2026-11-11 に公開の地図サイトをヘッドレスブラウザで観察したところ、withfs ニュースマップは Blogger に Google マイマップを埋め込み、JAXA 防災インタフェースは ArcGIS Online のアプリ (Web AppBuilder、Map Journal) を使い、気温のページは WordPress に Google Maps を埋め込んでいた。ライブラリから組む前に、この種のサービスで要件が足りるかを確かめる。

## Google マイマップ

- できること: Google の地図の上に点、線、図形を描き、レイヤーに分けて配色する。CSV、TSV、KML、KMZ、GPX、XLSX、Google スプレッドシートと、Google ドライブや Google フォトの写真を読み込める (https://support.google.com/mymaps/answer/3024836?hl=en)。
- 上限: 1 つの地図のレイヤーは最大 10 (https://support.google.com/mymaps/answer/3024933?hl=en)。1 つのレイヤーに線、図形、地点が 2,000 まで、地図全体で 10,000 まで、点の総数は 50,000 まで (https://support.google.com/mymaps/answer/3024837?hl=en)。読み込みは、展開後の KML/KMZ が 5 MB まで、ほかの形式が 40 MB まで、2,000 行を超えるファイルは読み込まない、写真は一度に 100 枚まで (https://support.google.com/mymaps/answer/3024836?hl=en)。
- 埋め込み: 地図を公開にしてから、メニューの「Embed on my site」で iframe のコードを得る (https://support.google.com/mymaps/answer/3109452?hl=en)。
- ベースマップ: Google の地図に限られ、他社のタイルには替えられない (推測。ヘルプの手順に他社のタイルを選ぶ項目が無い)。
- 規約と商用利用: Google は、Google の地図を Web サイトに埋め込むだけなら許可は要らないとし、点、線、ラベルの書き込みを認め、マイマップをその道具として挙げている。帰属表示は例外なく必須で、収益を生む用途や組み込んだ商用利用には Google Maps Platform を使うよう案内している (https://about.google/brand-resource-center/products-and-services/geo-guidelines/)。営利の Web サイトにマイマップを埋め込むことがこの案内のどちらに当たるかは、ページに書かれていない (未確認)。
- 費用: マイマップの料金ページは見当たらなかった (未確認)。個人の Google アカウントで作れることは手順から読める (推測)。

## ArcGIS Online のアプリ (StoryMaps、Experience Builder、Web AppBuilder)

- できること: ArcGIS Online の Web マップを材料に、ArcGIS StoryMaps で地図つきの読み物を、ArcGIS Experience Builder で地図アプリの画面をノーコードで組む。ArcGIS Maps SDK for JavaScript で書く場合は [arcgis-maps-sdk-js](../libraries/arcgis-maps-sdk-js.md) を見る。
- Web AppBuilder の廃止: ArcGIS Online では、2026 年第 1 四半期に新規作成ができなくなり、2026 年第 4 四半期に既存のアプリの更新ができなくなり、2027 年第 2 四半期に既存のアプリが動かなくなる。移行先は Experience Builder (https://doc.arcgis.com/en/web-appbuilder/latest/create-apps/wab-retirement.htm)。2026-11-11 は更新ができる最後の四半期に当たる。
- 旧版の Esri Story Maps (Map Journal、Cascade など): テンプレートは 2026-02 に ArcGIS Online から廃止された。廃止された項目は、所有者が代わりの項目を設定していればそこへ転送される (https://doc.esri.com/en/arcgis-storymaps/latest/get-started/transition-from-classic.html)。2026-11-11 の観察で JAXA 防災インタフェースに Map Journal が見えたことと、この記述との関係は確かめていない (未確認)。 JAXA のアプリは ArcGIS Online ではなく JAXA 自身の ArcGIS のポータル (daichi-bousai.dpif.jaxa.jp/portal/) から配られていた (2026-11-11 観測)。自前で運用する ArcGIS Enterprise では、ArcGIS Online の廃止の予定がそのまま及ばない可能性がある (推測)。
- ライセンスと費用: ArcGIS Online はユーザータイプ (Creator、Professional、Professional Plus、Mobile Worker、Contributor、Viewer) ごとに契約し、クレジットが Creator と Professional 系は 500、Mobile Worker と Contributor は 250、Viewer は 0 付く。料金はページに無く、営業への問い合わせになる (https://www.esri.com/en-us/arcgis/products/arcgis-online/buy)。地図とアプリを作って共有できると書かれているのは Creator 以上である (同)。クレジットは解析、ルート検索、ジオコーディングなどで減り、公開したアプリが組織の有料のコンテンツを使えば費用は組織が負う (https://doc.esri.com/en/arcgis-online/latest/reference/faq.html)。StoryMaps は、有料のサービスやデータを使う地図を載せると閲覧回数に応じてクレジットを使う (https://doc.esri.com/en/arcgis-storymaps/latest/reference/faq.html)。
- 無料のアカウント: 公開アカウントは個人の非商用に限られ、保存容量は 2 GB で、ホストレイヤーの公開と Map Viewer での解析ができない (https://doc.esri.com/en/arcgis-online/latest/reference/faq.html)。
- 縛り: 作った画面は ArcGIS Online の上で動き、廃止の予定に従って移行を迫られる (Web AppBuilder、旧版 Story Maps の例)。長く公開しつづける地図では、製品の寿命を見込む。

## uMap

- できること: OpenStreetMap などのタイルの上に点、線、面を描き、ファイルや外部の URL からデータを読み込み、Web サイトに埋め込む (https://docs.umap-project.org/en/stable/)。地図ごとにデータのライセンスを選ぶ欄があり、既定は「No licence set」(https://github.com/umap-project/umap/blob/master/umap/models.py)。
- 公開インスタンス: 公式サイトは、OpenStreetMap Germany、OpenStreetMap Switzerland、OpenStreetMap France の各サーバーで動く uMap DE、uMap CH、uMap FR を挙げる。どれも匿名での利用ができ、リアルタイムの共同編集は DE だけが有効 (https://umap-project.org/)。各インスタンスの利用規約、容量の上限、商用利用の可否は、公式サイトと利用者向けの文書に見当たらなかった (未確認)。uMap のメーリングリストでは、ソフトウェアのライセンスはインスタンスの利用条件ではなく、共有のインスタンスは負荷の小さいサイト向けで、負荷の大きいサイトは自前で立てるべきだという議論がある (2017 年、https://lists.openstreetmap.org/pipermail/umap/2017-March/000199.html)。公式の方針ではない。
- 自前で立てる: Python と Django で書かれ、PostGIS を有効にした PostgreSQL が要る。Docker イメージもある (https://github.com/umap-project/umap/blob/master/docs/install.md)。
- ライセンス上の注意: AGPL-3.0-or-later なので、改変した uMap をネットワーク越しに利用者へ使わせるなら、その利用者に改変後のソースを提供する義務が生じる (AGPL-3.0 第 13 条、https://www.gnu.org/licenses/agpl-3.0.html)。改変せずに立てるだけなら、配布元のソースを示せば足りる (推測)。地図に載せるデータが OSM 由来なら ODbL の条件が別にかかる。背景のタイルは各供給元の規約に従う (map-compare-infra の各 reference)。
- 費用: ソフトウェアと公開インスタンスは無料。開発は OpenCollective と LiberaPay の寄付とスポンサーで賄う (https://umap-project.org/)。

## Felt

- 料金 (米ドル、2026-11-11、https://felt.com/pricing): Free は $0 で 3 席、閲覧者 25 人、月 10k 回の地図表示。Team は月払い $249 (年払いなら月 $199) で 3 席、閲覧者 25 人、月 25k 回、処理 5 GB/月。Business は月払い $749 (年払いなら月 $599) で 5 席、閲覧者 100 人、月 100k 回、処理 25 GB/月。Enterprise は年払いで月 $1,250 から、10 席、閲覧者無制限、月 250k 回、処理 100 GB/月。席の追加は月払い $59、年払いなら月 $49。保存容量は月の処理量の 4 倍。地図表示や処理が足りなくなると、超過料金は取らずに止める (公開の訪問者には上限超過のページが出る)。$5/月で 1 GB の処理、1,000 回の地図表示などを足せる。
- 埋め込み: Free には無く、Team 以上で使える。公開の地図はログインなしで見られ、非公開の地図は閲覧者に Felt の無料アカウントが要り、閲覧者の人数に数える (https://felt.com/pricing)。自分のアプリを作る場合や、販売する製品に Felt の地図を埋め込む場合は Platform アドオン (月払い $1,250、年払いなら月 $1,000、有料プランに足す、最初の 3 か月は無料) が要り、顧客にアカウントや席は要らない (同)。iframe は共有メニューの Embed から得る (https://help.felt.com/sharing-and-collaboration/embedding)。JavaScript SDK `@feltmaps/js-sdk` で埋め込んだ地図を操作でき、非公開の地図はサーバー側で REST API から短命の埋め込みトークンを発行して見せる (https://developers.felt.com/js-sdk/getting-started 、https://developers.felt.com/js-sdk/embed-options)。
- データ: アップロードは Team 以上で、CSV、Excel、GeoJSON、GeoPackage、Shapefile、.gdb、KML/KMZ、GeoTIFF などを読める。REST API は Business 以上 (https://felt.com/pricing)。
- 縛り: 席、閲覧者、地図表示回数の上限が契約で決まる。上限を超える表示回数は 1,000 回ごとに $5/月で足す (https://felt.com/pricing)。月 100 万回を Business (100k 込み) で賄うと、足りない 90 万回分で $4,500/月が加わる計算になる (900,000 / 1,000 x $5。上の料金表からの計算で、見積もりは取っていない)。

## ノーコードで足りるとき、作るとき

ノーコードで足りるのは、次をすべて満たすときである。地物が数千件以内で、手で更新できる頻度である (Google マイマップは 1 レイヤー 2,000、地図全体 10,000 の上限)。画面と操作がサービスの既定の範囲で足りる。表示回数が、無料の範囲か契約の上限に収まる (Felt の Free は月 10k 回)。ベースマップをサービスの用意したものから選べばよい。地図がサービスの寿命 (廃止や仕様の変更) に付き合ってよい。

ライブラリから作る (または TerriaJS などの土台を使う) のは、次のどれかに当たるときである。地物が多い、またはデータを自動で更新する。独自の画面、検索、操作が要る。特定のベースマップ (地理院タイル、自前の PMTiles など) を使う。表示回数が多く、席や表示回数の課金では費用が合わない。長く同じ URL で公開しつづけ、製品の廃止に左右されたくない。営利のサイトで Google の地図を使い、Google Maps Platform の契約が要るかどうかを避けたい。

迷うときは、まずノーコードで試作して要件 (件数、画面、更新の手間) を確かめ、足りないところが出てからライブラリに移る (推測。移行の手間はデータを KML や GeoJSON で書き出せるかで決まる)。

## 向いている場面

- 自治体、報道、個人のブログで、地点を数十から数千件載せた地図を早く出したいとき。
- 開発者がいない部署が、自分で地図を更新しつづけるとき。
- ArcGIS の契約がある組織で、地図つきの報告や読み物を出すとき (StoryMaps)。
- OSM のタイルの上で、AGPL のソフトウェアを自前で立てられる組織 (uMap)。

## 向いていない場面

- 地物が数万件を超える、または自動で更新する地図。
- 画面と操作を作り込みたいプロダクト。
- 販売する製品に地図を組み込むとき (Felt は Platform アドオンが要り、Google は Maps Platform を案内している)。
- 長く同じ形で公開しつづけたい地図で、製品の廃止に付き合えないとき (Web AppBuilder は 2027 年第 2 四半期に動かなくなる)。

## 環境の違いと保守

- ブラウザ間の互換: ホスティング型のサービスでは、ブラウザ間の互換は提供元が引き受け、利用者が確かめられるのは対応ブラウザのページだけである。Google マイマップは Chrome、Firefox、Safari でよく動くと書く (https://support.google.com/maps/answer/80785?hl=en)。ArcGIS Online は Chrome 154 以降、Edge 154 以降、Firefox 159 以降と 153 ESR、Safari 26 以降を挙げ、WebGL の使える 64 ビットのブラウザだけを対象とし、Scene Viewer などは別の要件に従う (https://doc.esri.com/en/arcgis-online/latest/reference/browsers.html)。uMap は CI で Playwright の統合テストを Chromium (headless shell) だけで回している (https://github.com/umap-project/umap/blob/master/justfile 、https://github.com/umap-project/umap/blob/master/.github/workflows/test-docs.yml)。Felt の対応ブラウザのページは見つからなかった (未確認)。
- OS 間の互換: Google マイマップのヘルプは、パソコン、Android、iPhone と iPad の版に分かれている (https://support.google.com/maps/answer/80785?hl=en)。ArcGIS Online の対応ブラウザのページはモバイルのブラウザに触れていない (https://doc.esri.com/en/arcgis-online/latest/reference/browsers.html)。uMap の CI は ubuntu-latest だけである (https://github.com/umap-project/umap/blob/master/.github/workflows/test-docs.yml)。各サービスが試験している OS と端末は未確認。
- 操作の網羅: 地図の操作は各サービスの下の地図ライブラリ (Google の地図、ArcGIS Maps SDK for JavaScript、uMap は Leaflet) に従う (推測)。埋め込んだ地図でページのスクロールと両立させる設定がどのサービスにあるかは未確認。
- エッジケースへの対応: 各サービスとも、日付変更線、描画コンテキストの喪失、タイル読み込みの再試行、オフラインについての文書は見つからなかった (未確認)。ArcGIS Online はローカルストレージを有効にしないと正しく動かないと書く (https://doc.esri.com/en/arcgis-online/latest/reference/browsers.html)。
- 継続的な保守: ホスティング型ではブラウザと OS の変化への追随は提供元が行う。ArcGIS Online は対応ブラウザの版を引き上げ続けており、最新版の使用を勧めている (https://doc.esri.com/en/arcgis-online/latest/reference/browsers.html)。一方で、製品そのものの廃止 (Web AppBuilder、旧版 Story Maps) に合わせた移行は利用者の作業になる (上の「ArcGIS Online のアプリ」)。uMap を自前で立てる場合は、追随の作業は運用者が持つ (推測)。

## 出典

- https://support.google.com/mymaps/answer/3024836?hl=en
- https://support.google.com/mymaps/answer/3024933?hl=en
- https://support.google.com/mymaps/answer/3024837?hl=en
- https://support.google.com/mymaps/answer/3109452?hl=en
- https://about.google/brand-resource-center/products-and-services/geo-guidelines/
- https://doc.arcgis.com/en/web-appbuilder/latest/create-apps/wab-retirement.htm
- https://doc.esri.com/en/arcgis-storymaps/latest/get-started/transition-from-classic.html
- https://doc.esri.com/en/arcgis-storymaps/latest/reference/faq.html
- https://doc.esri.com/en/arcgis-online/latest/reference/faq.html
- https://www.esri.com/en-us/arcgis/products/arcgis-online/buy
- https://umap-project.org/
- https://docs.umap-project.org/en/stable/
- https://github.com/umap-project/umap/blob/master/LICENSE
- https://github.com/umap-project/umap/blob/master/docs/install.md
- https://github.com/umap-project/umap/blob/master/umap/models.py
- https://github.com/umap-project/umap/releases
- https://lists.openstreetmap.org/pipermail/umap/2017-March/000199.html
- https://www.gnu.org/licenses/agpl-3.0.html
- https://felt.com/pricing
- https://help.felt.com/sharing-and-collaboration/embedding
- https://developers.felt.com/js-sdk/getting-started
- https://developers.felt.com/js-sdk/embed-options
- 2026-11-11 に公開の地図サイト (withfs ニュースマップ、JAXA 防災インタフェース、気温のページ) をヘッドレスブラウザで観察した結果

## 未確認のこと

- 営利の Web サイトに Google マイマップを埋め込むことが、Google の案内の「埋め込むだけなら許可不要」と「収益を生む用途は Google Maps Platform」のどちらに当たるか: ページに書かれていないため。
- Google マイマップの料金と、Google Workspace の契約で上限や規約が変わるか: 料金ページが見当たらなかったため。
- ArcGIS Online の各ユーザータイプの価格と、Experience Builder や StoryMaps を作るのに要る最小のユーザータイプ: 購入ページに価格が無く、作成の可否が明記されていないため。
- ArcGIS Online の有料の契約で、公開アプリを営利の目的に使ってよい範囲: FAQ に有料契約の商用利用の記述が無いため。
- 旧版の Esri Story Maps (Map Journal) が 2026-02 の廃止後にどう表示されるか: 文書は転送の設定を説明するだけで、転送の無い項目の扱いを書いていないため。観察で見えた Map Journal が ArcGIS Enterprise の上か、別の仕組みかも確かめていない。
- uMap の公開インスタンス (DE、CH、FR) の利用規約、容量の上限、商用利用の可否: 公式サイトと文書に見当たらず、公開の OpenStreetMap のサーバーは呼ばない方針のため各インスタンスのページを確かめていない。
- Felt で選べるベースマップと、その供給元: 料金ページと SDK の文書の範囲では確かめていない。
