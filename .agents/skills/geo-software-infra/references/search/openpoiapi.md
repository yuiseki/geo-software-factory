# OpenPOI API

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 (JST) |
| 提供者 (運営主体) | 未確認。利用規約は「本サービスの運営者 (以下「運営者」)」とだけ書き、法人名や個人名を示していない。運営者の特定は窓口 (security@openpoiapi.com) への問い合わせに委ねている (https://docs.openpoiapi.com/legal.html) |
| サイト / ドキュメント | https://openpoiapi.com/ (紹介ページ、デモ)、https://docs.openpoiapi.com/ (API 仕様書、よくある質問、出典、既知の制約) |
| API の仕様 (OpenAPI など) | https://api.openpoiapi.com/openapi.json (OpenAPI 3.1.0、info.version 1.0.0、paths は /v1/search と /v1/suggest)。info.license は「MIT (API) / 元データは提供元ごとに異なるライセンス」 |
| 利用規約 | https://docs.openpoiapi.com/legal.html (利用規約、プライバシーポリシー、サポート窓口を1ページにまとめたもの。最終更新日 2026-10-03) |
| 稼働状況の公開 | https://docs.openpoiapi.com/status.html 。閲覧したブラウザから主要エンドポイント (/、/v1/search、/v1/suggest、/openapi.json、/mcp) に直接アクセスして「いま」の応答だけを表示する。履歴や過去の障害記録は残さない |

## 概要

日本全国の POI (施設) をキーワードと位置で検索する読み取り専用の HTTP API である。Overture Maps の Places、自治体と厚生労働省の食品営業許可・届出オープンデータ (Japan Food Facilities)、国土数値情報の駅 (N02)、学校 (P29)、市町村役場等及び公的集会施設 (P05) を名寄せして配信し、件数は「300万件以上」と公称する。2026-11-10 に GET / が返した facility_count は 3,170,822 だった (ドキュメントの例は 2026-10-31 時点で 3,208,280)。各レコードに licenses と attributions が付き、検索結果を自分のデータベースに保存してよいと明記している (https://docs.openpoiapi.com/)。

## データの出どころと更新

| 出どころ | 件数 | ライセンスと出典表示の条件 | 更新頻度 | 出典 |
|---|---|---|---|---|
| Overture Maps Places (Meta、Microsoft、PinMeTo、Krick、RenderSEO、DAC、BrightQuery 提供分) | 未公表 (ソース別の件数は出ていない) | CDLA-Permissive-2.0。データを共有 (再配布) するときは協定の全文を一緒に提供する (2.1条)。計算による分析の成果物 (Results) には制限も義務も課さない (3.1条)。Overture は「Overture Maps Foundation, overturemaps.org」の表示を求める | Overture のリリース単位で取り込む。現在は 2026-09-23.1 に固定で、毎週は更新しない | https://openpoiapi.com/attribution.html 、https://docs.overturemaps.org/attribution/ 、https://cdla.dev/permissive-2-0/ |
| Foursquare OS Places (Overture Maps Places に含まれる分) | 未公表 | Apache-2.0。再配布時はライセンスの写しを渡し、変更した旨を示し、NOTICE.txt の内容を保持する (4条)。Foursquare は API の形で配る場合に NOTICE.txt の内容を開発者向けドキュメントに目立つ形で載せるよう求める。OpenPOI API はドキュメントに全文と自らの変更 (名寄せ、座標の統合) の通知を載せている | Overture と同じ | https://openpoiapi.com/attribution.html 、https://opensource.foursquare.com/places-notice-txt/ |
| Overture Maps Places (AllThePlaces 提供分) | 未公表 | CC0-1.0 (表示義務なし) | Overture と同じ | https://openpoiapi.com/attribution.html 、https://docs.overturemaps.org/attribution/ |
| Japan Food Facilities (自治体と厚生労働省の食品営業許可・届出オープンデータ) | 未公表。ソース数は OpenPOI 側が 81、JFF の出典ページが 80 と書いており一致しない | ソースごとに CC BY 2.0 / 2.1 JP / 3.0 / 4.0 (OpenPOI の集計で 76)、公共データ利用規約 PDL1.0 (4)、CC0 1.0 (1)。CC BY 系と PDL1.0 は出典の明示と、加工した旨の表示を求める。JFF は「加工して作成」を含む表示文をそのまま載せるよう求め、提供元が推奨しているかのような表示を禁じる。緯度経度は JFF が住所からジオコーディングした参考値 | 毎週、日曜 19:00 UTC (月曜 4:00 JST) に再構築 | https://openpoiapi.com/attribution.html 、https://gl20percentclub.github.io/japan-food-facilities/attribution.html |
| 国土数値情報 鉄道データ (N02、2025年度版) | 駅 9,046件 | 2020年度版以降は「オープンデータ (CC_BY_4.0)」。国土数値情報ダウンロードサイトの規約は出典の記載と、加工した場合はその旨の記載を求め、国が作成したかのような公表を禁じる | 上流は年1回 (2026年4月に2025年度版へ更新)。OpenPOI 側の取り込み周期は未公表 | https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-2025.html 、https://nlftp.mlit.go.jp/ksj/other/agreement.html |
| 国土数値情報 学校データ (P29、2023年度版) | 56,807件 | 2023年度版と2021年度版は「オープンデータ (CC_BY_4.0)」。2013年度版は非商用なので版に注意。出典表示の条件は N02 と同じ | 上流は2年ごとの更新実績 (2022年6月、2024年6月)。OpenPOI 側の取り込み周期は未公表 | https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P29-2023.html |
| 国土数値情報 市町村役場等及び公的集会施設 (P05、2022年版) | 79,532件 | 「オープンデータ (CC_BY_4.0)」。出典表示の条件は N02 と同じ | 上流は2023年に2022年版へ更新、その前は2011年。OpenPOI 側の取り込み周期は未公表 | https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P05-2022.html |
| 令和2年国勢調査 小地域 (町丁・字等別) 境界データ (駅の住所の付与と座標検査に使用。POI そのものではない) | 該当なし | e-Stat の利用規約は政府標準利用規約 (第2.0版) 準拠で CC BY 4.0 と互換。出典の記載と、加工した場合はその旨の記載を求める。ただし e-Stat は統計地理情報システムに別の利用ルールがあるとしており、その個別ルールは確かめていない | 国勢調査の周期 (5年) | https://openpoiapi.com/attribution.html 、https://www.e-stat.go.jp/terms-of-use |
| OpenPOI Manual Overrides (運営者による現地実測の追加と差し替え) | 未公表 | CC0-1.0 | 未公表 | https://openpoiapi.com/attribution.html |

出典ページは、ほかに住所正規化と検査の参照データとして郵便番号データ (日本郵便)、geolonia/japanese-addresses (CC BY 4.0)、アドレス・ベース・レジストリ (PDL1.0)、登記所備付地図データ、街区レベル位置参照情報を挙げている (https://openpoiapi.com/attribution.html)。Overture の公式の帰属ページは Places の提供元に Birdeye、Uberall、OpenTravel Alliance も挙げているが、OpenPOI の出典ページの列挙には含まれていない (https://docs.overturemaps.org/attribution/)。

## 機能

| 機能 | 対応 | 備考 |
|---|---|---|
| キーワード検索 (店名、カナ、住所) | あり | GET /v1/search の q。施設名、カナ、都道府県、市区町村、住所を横断する。スペース区切りの複数語は OR。ひらがなとカタカナは同じ結果だが、半角カナと全角カナでは結果が変わる |
| 位置での絞り込み (半径、矩形、近い順) | あり | bbox (minLng,minLat,maxLng,maxLat)、center (lng,lat) と radius (既定 50,000 m)。優先は bbox、次に center+radius。近い順に並ぶのは center を指定したときだけ。名前が入力と完全一致する施設は範囲外からも最大20件返る (2026-11-10 に center 新宿付近 radius 1,000 m で「駅」を引くと川崎市の店舗も返った)。limit は 1〜200 |
| 入力補完 | あり | GET /v1/suggest。複数語は AND、全角半角、大文字小文字、ひらがなカタカナの違いを吸収し、重複除去と並び替えを済ませて返す。bbox 内で0件なら全国に広げる。limit は 1〜20。fields=minimal で licenses と attributions を応答直下に1回だけ載せる軽量形式になる。カテゴリ、ブランド、地名の語彙 (vocabulary) とゴーストテキスト用の completion も返す |
| カテゴリでの検索 | 一部 | カテゴリを指定する専用のパラメータは無い。応答の category は restaurant、cafe、convenience_store、medical、station など17値。/v1/suggest の vocabulary がカテゴリ語彙と再検索用の query を返す。category が unknown のレコードが1割程度あり、カテゴリでの絞り込みにはまだ使えない場合があると公式が書いている |
| 住所のジオコーディング、逆ジオコーディング | なし | 住所を座標に変える、座標から住所を引くエンドポイントは仕様に無い。住所文字列での施設検索はできる |
| MCP | あり | POST https://api.openpoiapi.com/mcp (Streamable HTTP、ステートレス、JSON-RPC 2.0)。ツールは search_facilities と dataset_info の2つ。セッション ID と SSE ストリームは提供しない |
| 一括の取得 (データのダウンロード) | なし | ダンプやファイルでの配布はドキュメントに無い。取得は検索 API 経由だけである |

## 料金と利用の上限

- 料金と課金単位: 現時点では登録不要、無償。有料プランや課金単位は公開されていない。今後、レート制限の導入や API キーによる利用登録を求めるなど提供形態を変える場合があるとしている (https://docs.openpoiapi.com/legal.html)
- API キーの要否: 不要。発行もしていない。CORS は全オリジン許可 (https://docs.openpoiapi.com/)
- レート制限、公正利用の条件: 利用者ごとの制限は無い。API 全体で定常 200 req/s、バースト 600 req/s を超えると 429 を返す。429 は API Gateway が生成し、CORS ヘッダが付かないのでブラウザでは CORS エラーに見える。規約は不正利用や過度な負荷のアクセスを検知、防止する目的でアクセス記録を取るとしている (https://docs.openpoiapi.com/ 、https://docs.openpoiapi.com/legal.html)
- SLA: 無い。仕様は予告なく変更、追加、廃止されることがあり、サービスの全部または一部を予告なく停止、終了することがあると規約に書かれている。問い合わせ対応もベストエフォートで、対応時間と回答期限の保証 (SLA) は無いと明記している (https://docs.openpoiapi.com/legal.html)

## 利用規約上の制約

- 商用利用: 目的を問わず利用でき、商用も可。ただしデータ側のライセンス義務は免除されない (https://docs.openpoiapi.com/legal.html)
- 結果の保存、キャッシュ、再配布: 保存してよいと明記している。条件は licenses と attributions を配列のまま一緒に保存すること。公式の整理では、保存だけなら追加の義務は無く、画面に出すときは出典表示、第三者に渡す (再配布する) ときはライセンスごとの再配布条件 (CDLA は協定の全文か参照先、Apache-2.0 はライセンスの写しと NOTICE、CC BY は出典とライセンスへのリンクと変更の有無)、加工して公開するときはさらに加工したことと加工の主体を記載する。OpenPOI API 自身は取得したデータに追加の制限を課していないとし、その理由に CC BY 4.0 第2条a項5号B (下流への追加制限の禁止) を挙げる。公式は、PDL1.0 と CC BY 2.1 JP は義務の起点が「利用する際」で保存が含まれるかは原文から断定できない、Apache-2.0 も保存だけが対象かは断定できない、と注記し、法的助言ではないとしている (https://docs.openpoiapi.com/ の「検索結果を保存する場合」)。SaaS として保存した結果を利用者に表示、配信する場合は、上記の「画面に出す」と「第三者に渡す」の両方に当たると考えるのが安全である (推測)。CC BY と PDL1.0 由来の行は加工の旨の表示が必要になり、CDLA と Apache-2.0 由来の行を API やファイルで渡すなら協定とライセンスの本文、NOTICE の提供が加わる。どの元ライセンスも継承 (share-alike) を求めないので、自社データと混ぜた成果物を同じライセンスで公開する義務は生じない (各ライセンス原文から読んだもの。ODbL のデータは含まれない)
- 出典表示の要件 (レコードごとの licenses と attributions の扱い): 画面には「OpenPOI API」を出典として記載し、https://openpoiapi.com/attribution.html へリンクする。リンクを置けない媒体では「出典: OpenPOI API (https://openpoiapi.com/attribution.html)」の形でよい。licenses と attributions はレコードに適用されるライセンスをプログラムで判定するための参考情報で、画面への表示は求めていない。複数ソースを名寄せしたレコードでは両配列が和集合になる (2026-11-10 の /v1/suggest でも fields=minimal の応答直下に licenses と attributions が載ることを確かめた) (https://docs.openpoiapi.com/)
- 他社の地図との併用: 規約に併用の制限は書かれていない。紹介ページのデモは地理院タイルを背景に使っている (https://openpoiapi.com/)

## 品質の限界

- category が unknown のレコードが1割程度ある (2026-10-18 時点の公式の実測)。大半は JFF 由来で、許可の種類がカテゴリに読み替えられていない (https://docs.openpoiapi.com/ の「既知の制約」。以下同じ)
- 位置がずれたレコードがある。Overture の座標をそのまま使うため、観光地、駅、公園などの名前を持つレコードで数 km から数百 km ずれる例がある。JFF 由来は住所からの位置で、同じ建物の店舗は同じ座標になる
- 閉業、閉鎖した施設が残ることがある。既知の制約は「鮮度を示す値は現在レスポンスに含まれない」と書くが、同じページのスキーマには source_updated_at (原典の更新日、充足 75.6%) があり、2026-11-10 の /v1/search の応答にもこのフィールドがあった (JFF 由来の行では空文字)。記述が食い違っている
- 東京スカイツリーのような観光名所、ランドマーク自体は収録対象外
- /v1/search の複数語は OR で、center が無いと関連度順にも距離順にもならない。無関係な結果が先頭に来ることがある
- 網羅性は元データ次第で、実在する施設が無いことがある
- JFF には個人事業主の氏名が施設名として載っている場合があり、運営者は個人名と判定した行を配信しないが、機械判定なので漏れうると規約に書いている (https://docs.openpoiapi.com/legal.html)
- website、postcode、socials、brand などの付加項目は Overture 由来の行にしか値が無い。充足率は website 43.4%、postcode 63.4%、brand 6.5%、name_en 1.9% (https://docs.openpoiapi.com/ のスキーマ説明)

## 置き場所の判断との関係

外部の API に任せる型だが、結果を保存できるので、正本や検索索引を自分の側に持つ構成 (geo-software-arch の search と source-of-truth) にも移れる。

- 自分の側に持ち出す手段と条件: 一括ダウンロードは無いので、/v1/search の bbox 検索などで取得して保存することになる。1回の上限は200件で、API 全体の上限 (定常 200 req/s) を共有するため、全件の複製は時間がかかり、他の利用者への負荷にもなる (推測)。保存するときは licenses と attributions を配列のまま残し、表示と再配布の際に上記の出典表示と再配布条件を満たす。配信側の名寄せや個人名の除外は更新のたびに変わりうるので、保存した複製はその時点の版として扱い、更新方法を自分で決める必要がある (推測)
- 元データ (Overture Maps、国土数値情報など) から同じものを自前で作る場合との違い: 元データはそれぞれ公開されており、ライセンス上は自前で統合できる。OpenPOI API を使うと、JFF のソース間の正規化とジオコーディング、Overture との名寄せ、個人名の除外、駅への住所付与、カナと表記ゆれの吸収、入力補完の並び替えを自分で作らずに済む。一方で、取り込む Overture のリリース (現在は 2026-09-23.1 に固定)、名寄せの規則、カテゴリの語彙は運営者が決めるので、更新の速さや統合の規則を自分で選べない。自前で作れば鮮度や対象範囲を選べるが、名寄せと個人名の除外の手間とリスクを自分で負う (推測)

## 向いている場面

- 日本国内の店舗や施設の検索ボックスと入力補完を、API キーや契約なしで試作したいとき
- 取得した POI を自社のデータベースに保存して、地図の上に重ねたり分析したりしたいとき (保存を禁じる商用の場所検索 API の代わりとして)
- AI エージェントから MCP 経由で国内の施設を引きたいとき
- 背景地図の提供元を問わずに使える検索がほしいとき (規約に併用の制限が無い)

## 向いていない場面

- SLA、サポート期限、提供の継続性が必要な本番サービス。予告なく変更、停止しうると規約に書かれ、運営主体も公表されていない
- 観光名所、ランドマーク、住所そのものの検索、逆ジオコーディング
- 閉業の反映や位置の正確さが重要な用途 (ナビゲーション、来店の誘導など)
- 一定以上の高負荷を自分のサービスから直接かける構成 (全体で 200 req/s を他の利用者と共有する)
- 日本国外の POI

## 出典

- https://openpoiapi.com/ : 紹介ページ。300万件以上、保存可、商用可、MCP 対応、デモの背景が地理院タイルであることを確かめた
- https://docs.openpoiapi.com/ : エンドポイントとパラメータ、スキーマ、MCP、レート上限 (200/600 req/s)、よくある質問、出典表示、「検索結果を保存する場合」、Foursquare NOTICE、既知の制約、各データの件数と更新頻度を確かめた (ページ内の実例の取得日は 2026-10-31)
- https://docs.openpoiapi.com/legal.html : 運営者の表記、無償で登録不要、仕様変更と停止の可能性、商用可、プライバシーポリシー、個人名の扱い、サポート窓口と SLA が無いことを確かめた (最終更新日 2026-10-03)
- https://docs.openpoiapi.com/status.html : 稼働状況ページがブラウザからの即時確認だけで履歴を持たないことを確かめた
- https://openpoiapi.com/attribution.html : ソースごとのライセンスと表示文、参照データ、Foursquare NOTICE の扱いを確かめた
- https://api.openpoiapi.com/openapi.json : OpenAPI 3.1.0、version 1.0.0、paths、info.license を確かめた
- https://api.openpoiapi.com/ 、/v1/search、/v1/suggest : 2026-11-10 15:51 JST ごろに各1回呼び、facility_count、licenses と attributions の形、source_updated_at などの項目、fields=minimal の応答、範囲外の完全一致が返ることを確かめた
- https://docs.overturemaps.org/attribution/ : Places テーマの提供元ごとのライセンス (CDLA Permissive 2.0、Foursquare は Apache 2.0、AllThePlaces は CC0 1.0) を確かめた
- https://cdla.dev/permissive-2-0/ : CDLA-Permissive-2.0 の共有条件 (2.1条) と Results への無制限 (3.1条) を確かめた
- https://opensource.foursquare.com/places-notice-txt/ : OpenPOI のドキュメントが転記する NOTICE の取得元 (転記内容を OpenPOI 側のページで確かめた。原ページは直接は開いていない)
- https://gl20percentclub.github.io/japan-food-facilities/attribution.html : JFF のソース数 (80)、ライセンス別の内訳、表示文の要件を確かめた
- https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-2025.html 、https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P29-2023.html 、https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P05-2022.html : 各データの使用許諾条件と更新履歴を確かめた
- https://nlftp.mlit.go.jp/ksj/other/agreement.html : 国土数値情報ダウンロードサイトの出典記載と加工時の記載の要件を確かめた (2026-03-23 施行)
- https://www.e-stat.go.jp/terms-of-use : e-Stat の利用ルールが政府標準利用規約 (第2.0版) 準拠で CC BY 4.0 と互換であること、出典と加工の記載の要件を確かめた

## 未確認のこと

- 運営主体 (法人か個人か、名称、所在地)。規約とドキュメントのどこにも書かれていない
- 将来の有料化やレート制限、API キー登録の時期と条件
- ソースごとの件数の内訳 (Overture、JFF の件数)、名寄せ後に複数ソースを持つレコードの割合
- JFF のソース数が OpenPOI 側 (81) と JFF の出典ページ (80) で違う理由
- Overture の帰属ページにある Birdeye、Uberall、OpenTravel Alliance 由来のレコードが OpenPOI に含まれるか、含まれる場合の attributions の表記
- e-Stat の統計地理情報システム (境界データ) に適用される個別の利用ルールの文面
- 国土数値情報 (N02、P29、P05) と国勢調査境界データを OpenPOI 側がどの周期で取り込み直すか
- アクセス記録の保存期間、/mcp の呼び出しも同じレート上限に含まれるか
- 「鮮度を示す値はレスポンスに含まれない」という既知の制約の記述と、source_updated_at フィールドの存在のどちらが現状を表すか
