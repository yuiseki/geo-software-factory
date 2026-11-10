# Geolonia Maps

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | 株式会社 Geolonia (2019 年 8 月設立) |
| 公式サイト | https://www.geolonia.com/maps/ |
| 料金ページ | https://www.geolonia.com/pricing/ |
| 利用規約・利用ポリシー | https://www.geolonia.com/terms/ (同社サービス共通の利用規約。地図データの出典は https://www.geolonia.com/credit/) |

## 概要

Geolonia Maps は、Geolonia が配信するベクトルタイル地図を Web サイトとアプリケーションに組み込むためのサービスとライブラリである (出典: ドキュメント)。描画は MapLibre GL JS を基にした maps-core の上に、HTML の属性だけで使う embed、JavaScript から操作する maps-suite、React 向けの maps-react の 3 つのライブラリを用意している。課金は地図の表示回数による従量制で、Free と Pro の 2 プランがある (出典: 料金ページ)。

## 地図データ

- データの出どころ (自社調査 / OSM / 他社からのライセンス): 標準スタイル `geolonia/basic-v2` は OpenStreetMap のデータを元にしている (出典: スタイル一覧)。著作権情報ページは、地図データソースとして OpenStreetMap (ODbL)、国土地理院の地理院地図 Vector と標高タイル、農林水産省の筆ポリゴンデータ、Natural Earth を挙げている (出典: 著作権情報)。`geolonia/gsi` と `geoloniamaps/smartcity-base` は国土地理院のベクトルタイルを使うスタイルである (出典: スタイル一覧)。自社による現地調査の記述はない。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): 標準スタイルの配信元 tiles.json が示すレイヤは building、poi、transportation、transportation_name、place、landuse、water、boundary、fudepoli (筆ポリゴン) などで、最大ズームは 14 (出典: `osm.v2.tiles.geolonia.com/tiles.json` の vector_layers)。建物の形と高さはベクトルタイルに含まれ、3D 建物表示に使われる (出典: 3D 表示のハウツー)。詳しさは OpenStreetMap と国土地理院データの収録状況に依存する。住所・番地レベルのデータを地図タイルに含むかは公式資料に記述がない (未確認)。
- 全球の対応: 全球。標準タイルの範囲は経度 −180〜180、緯度 ±85.05 (出典: tiles.json)。FAQ は海外エリアも OpenStreetMap を元に表示できるとしている。表示言語は日本語と英語 (出典: FAQ)。
- 更新頻度: 通常は月 1 回程度 (提供元への聞き取り、2026-11-10。公開文書に記述はない)。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | なし | 提供スタイルはすべてベクトルタイル。外部のラスタタイル (例: 地理院タイル) を利用者がソースとして追加することはできる (出典: 独自のデータソース追加のハウツー) |
| ベクトルタイル (形式、スキーマ) | あり | MVT (tiles.json の format は pbf、タイル URL は `.mvt`)。最大ズーム 14。レイヤ名は tiles.json の vector_layers で公開されている。スキーマ仕様書は見つからなかった |
| スタイルの編集・カスタマイズ | あり | スタイルは MapLibre Style Spec 準拠の JSON。公式スタイル 7 種 (標準、国土地理院ベース、暗色など) を論理名で切り替えられ、`https://cdn.geolonia.com/style/geolonia/basic-v2/ja.json` を元に自作スタイルを URL で指定できる (出典: 地図のスタイルとは、スタイル一覧) |
| 衛星・航空写真 | なし | 公式スタイルに航空写真・衛星画像はない |
| 地形・3D 建物 | あり | 3D 建物は標準スタイルに含まれる。地形は国土地理院の標高タイル (raster-dem) を使う (出典: 3D 表示のハウツー、basic-v2 スタイルの sources、FAQ) |
| ジオコーディング / 逆ジオコーディング | なし | 「Geolonia Maps 自体はジオコーダを持っていない」。住所正規化ライブラリ @geolonia/normalize-japanese-addresses と組み合わせる手順を案内している (出典: 住所検索のハウツー) |
| ルート検索 | なし | ドキュメントと製品ページにルート検索 API の記載はない |
| オフライン利用 | 要問い合わせ | 料金ページに「イントラネットでのご利用」は問い合わせとある。オフライン利用の公開仕様はない |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): Web 向けに embed、maps-suite、maps-react と、基盤の maps-core (いずれも JavaScript) (出典: ドキュメント)。FAQ は SDK を「JavaScript の SDK」としており、Android / iOS のネイティブ SDK の公開ドキュメントはない。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 技術的には使えるが、提供元は推奨せず、公式 SDK (embed、maps-suite、maps-react と基盤の maps-core) 以外からの利用はサポートの対象外である (提供元への聞き取り、2026-11-10。公開文書に記述はない)。公式 SDK の地図インスタンスは MapLibre GL JS の Map を継承しており、MapLibre GL JS の API をそのまま呼べる (出典: maps-core へのアクセスのハウツー、https://docs.geolonia.com/reference/)。公式 SDK は Geolonia のソースへのリクエストに API キー (`key`) と `sessionId` を付ける (出典: https://www.npmjs.com/package/@geolonia/maps-core)。公式 SDK を使わずに MapLibre GL JS 単体や Leaflet、OpenLayers から Geolonia のタイルを読む手順は公式資料にない。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): Geolonia のタイルは公式 SDK を通して使うのが推奨で、他のライブラリから使うのはサポート外 (提供元への聞き取り、2026-11-10)。公式 SDK は外部のスタイルやタイルも表示でき、MapLibre GL JS の API も使えるので、SDK を使うことで描画の機能が狭まることはない (出典: スタイル変更のハウツー https://docs.geolonia.com/howto/change-style/ 、独自のデータソース追加のハウツー)。利用規約に特定の SDK を指定する条項はない。外部スタイルを指定した場合は 3D 建物の切り替えなど一部の機能が効かない (出典: 3D 表示のハウツー)。
- API キー・アカウントの要否: 本番公開にはユーザー登録と API キーの発行、利用 URL の登録が必要。localhost、CodePen、GitHub Pages (`*.github.io`、独自ドメインは対象外)、Netlify、Vercel、Cloudflare Pages など許可された開発・プレビュー環境では、デモキー `YOUR-API-KEY` で登録なしに描画でき、表示回数の制限もない (出典: デモキーで無料で試せる環境、maps-dev ページ)。

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): 地図表示回数。地図がユーザーの端末の画面に表示された回数で、画面外にある地図は数えない。ページを再読み込みして再表示すると 2 回になる (出典: 料金ページ、FAQ)。タイルリクエスト数では課金しない。
- 無料枠: Free プランは月 20,000 回まで (月 20,000 回以上は Pro の利用を求めている)。Pro プランは月額料金に月 50,000 回分を含む。許可された開発環境での表示は課金対象外 (出典: 料金ページ、FAQ)。
- 従量単価 (主な API ごとに、通貨と確かめた日つき): Pro は月額 3,980 円 (税抜、税込 4,378 円)。50,001 回目からの 1 回あたり単価は次のとおり (日本円、税抜、2026-11-10 確認)。
  - 50,001〜100,000 回: 0.40 円
  - 100,001〜500,000 回: 0.30 円
  - 500,001〜1,000,000 回: 0.23 円
  - 1,000,001〜5,000,000 回: 0.12 円
  - 5,000,001 回以上: 0.06 円
  - 技術サポートは月 55,000 円 (税抜) のオプション
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式も書く。単位の換算に仮定を置いたら仮定も書く): 仮定は (1) 1 地図ロード = 地図表示回数 1 回、(2) 区分ごとに単価を当てる段階制で計算する。料金ページの計算例 (500,000 回で 143,980 円) は 100,000 回目まで 0.4 円、それ以降 0.3 円の段階制になっており、500,001 回目以降の区分も同じ方式と仮定した。税抜、2026-11-10 の単価による。
  - 10 万ロード: 3,980 + 0.40 × 50,000 = 23,980 円
  - 100 万ロード: 3,980 + 0.40 × 50,000 + 0.30 × 400,000 + 0.23 × 500,000 = 3,980 + 20,000 + 120,000 + 115,000 = 258,980 円
  - 1,000 万ロード: 258,980 + 0.12 × 4,000,000 + 0.06 × 5,000,000 = 258,980 + 480,000 + 300,000 = 1,038,980 円
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): Free と Pro はダッシュボードから申し込むセルフサーブで、Pro はクレジットカード払いの月額。請求書払い、イントラネット利用、開発代行などは問い合わせ (出典: 料金ページ、FAQ)。

## 利用規約上の制約

- 商用利用: 料金ページ、利用規約ともに商用利用を禁じる記述はない。
- アクセス量の上限・公正利用の条件: Free は月 20,000 回まで。FAQ は Pro プランについての回答で、利用上限に近づいたときの事前通知機能はなく、上限に達すると地図上にアップグレードが必要な旨のメッセージが表示されるとしている (出典: FAQ)。Pro の料金ページは 50,001 回目以降を従量課金とし、上限は書いていない。利用規約は、当社が適当でないと判断した場合に事前通知なく利用を制限できるとする (第 6 条)。
- キャッシュ・オフライン保存: 利用規約と料金ページにタイルのキャッシュ・保存に関する定めはない。
- 帰属表示の要件: 利用規約に定めはない。配信元の tiles.json は「© Geolonia」と「© OpenStreetMap」の表示を指定しており、OpenStreetMap のデータは ODbL で許諾されている (出典: tiles.json、著作権情報)。標高タイルには「© GSI Japan」の表示が付く (出典: basic-v2 スタイル)。
- 他社の地図との併用、データの持ち出しの制限: 利用規約に併用を制限する条項はない。外部のタイルソースを重ねる手順を公式ドキュメントが案内している (出典: 独自のデータソース追加のハウツー)。

## 安定性と運用

- SLA: 公開されている SLA はない。利用規約は、保守や障害時に事前通知なくサービスを停止・中断でき、それによる損害に責任を負わないとする (第 5 条)。消費者契約でない場合、損害について一切責任を負わないとし、消費者契約で過失による賠償をする場合も損害が発生した月に受領した利用料が上限 (第 7 条)。サービス内容を通知なく変更・中止できる (第 8 条)。
- 運営の継続性 (運営主体、資金源): 株式会社 Geolonia。2019 年 8 月設立、2022 年 10 月に第三者割当増資を行い、資本金は 67,022 千円 (2022 年 11 月現在) (出典: 会社概要)。
- 障害情報の公開先: 未確認。公開されたステータスページは見つからなかった。

## 向いている場面

- 日本語の地図を表示回数ベースの公開単価で使いたい場合。月 10 万〜1,000 万回の費用を料金ページだけで計算できる。
- MapLibre GL JS の API やスタイル仕様をそのまま使い、スタイルを自由に変えたい場合。
- 外部のタイルや GeoJSON を重ねる地図を作る場合。利用規約に併用の制限がない。
- 手元の GeoJSON をコロプレス図やヒートマップで素早く可視化したい場合。公式 SDK の embed なら HTML の属性だけで描ける (https://docs.geolonia.com/howto/choropleth/ , https://docs.geolonia.com/howto/heatmap/)。提供元も推している機能である (提供元への聞き取り、2026-11-10)。
- 開発中やプロトタイプを、登録なしに localhost や GitHub Pages などで動かしたい場合。

## 向いていない場面

- ジオコーディングやルート検索を同じ提供元の API でそろえたい場合。どちらも提供していない。
- 航空写真が必要な場合。
- Android / iOS のネイティブアプリに組み込む場合。公開されているのは JavaScript のライブラリだけである。ネイティブアプリに近いものを作るなら、提供元が公開している PWA の地図アプリのテンプレート Geolonia PWAマップ (MIT、https://github.com/geoloniamaps/pwamap) がある。提供元によれば利用は定着している (提供元への聞き取り、2026-11-10)。
- 稼働率の保証や障害情報の公開を契約上の条件にしたい場合。公開 SLA とステータスページがない。

## 出典

- https://www.geolonia.com/maps/
- https://www.geolonia.com/pricing/
- https://www.geolonia.com/terms/
- https://www.geolonia.com/credit/
- https://www.geolonia.com/products/faq/
- https://www.geolonia.com/maps-dev/
- https://www.geolonia.com/company/
- https://docs.geolonia.com/
- https://docs.geolonia.com/tutorials/
- https://docs.geolonia.com/explanation/map-style/
- https://docs.geolonia.com/explanation/styles/
- https://docs.geolonia.com/explanation/free-referers/
- https://docs.geolonia.com/howto/3d/
- https://docs.geolonia.com/howto/address-search/
- https://docs.geolonia.com/howto/custom-source/
- https://docs.geolonia.com/howto/maps-core-access/
- https://cdn.geolonia.com/style/geolonia/basic-v2/ja.json
- https://osm.v2.tiles.geolonia.com/tiles.json?key=YOUR-API-KEY

## 未確認のこと

- 住所・番地レベルのデータを地図タイルに含むか。tiles.json のレイヤ名からは判断できない。
- 公式 SDK 以外 (MapLibre GL JS 単体、Leaflet、OpenLayers、MapLibre Native) からの利用の扱いを書いた公式文書。提供元への聞き取りでは、技術的には使えるがサポート外である。ただし、ドキュメント、FAQ、利用規約に該当する文言は見つからなかった。公式 SDK を使わずに使う公式の手順もない。tiles.json が返すタイル URL には Origin に結び付いたトークンが付く。
- ベクトルタイルのスキーマ仕様書。レイヤ名は tiles.json で見えるが、属性の定義を説明するページが見つからなかった。
- 障害情報の公開先。ステータスページが見つからなかった。
- 料金表の 500,001 回目以降が段階制か。料金ページの計算例は 500,000 回までしか示していない。
- Free プランで月 20,000 回を超えた場合の挙動。料金ページは「Pro をご利用ください」とだけ書く。FAQ のメッセージ表示は Pro プランの質問への回答である。

## 執筆上の注意

作者の利害関係があるため、他の provider と同じ項目・同じ粒度で書く。公開情報だけを書く。
