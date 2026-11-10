# 帰属表示の要件

対象: OpenStreetMap (OSMF のガイドライン)、商用の地図 API、地理院タイル、オープンデータ (CC BY、PDL、政府標準利用規約) の帰属表示の書き方と置き場所

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 根拠 (法令名と条、規約の版) | ODbL 1.0 第 4.2 条、第 4.3 条。OSMF Attribution Guidelines (2021-06-25 OSMF 理事会採択、ページの最終編集 2026-09-10)。CC BY 4.0 第 3 条 (a)、第 6 条。公共データ利用規約 (第 1.0 版) (PDL1.0、令和 6 年 7 月 5 日制定) 1.1、1.3、1.7。政府標準利用規約 (第 2.0 版) (平成 27 年 12 月 24 日 各府省 CIO 連絡会議決定) 1) ア、イ、3)。国土地理院コンテンツ利用規約 (令和 7 年 11 月 20 日改正)。測量法第 30 条第 4 項 (令和 8 年法律第 27 号改正反映版)。地理院タイル一覧と承認申請 Q&A Q1-12、Q1-15、Q1-19、Q5-2 |
| 所管・管理者 | OSM データ: OpenStreetMap Foundation (OSMF)。ODbL: Open Data Commons。CC BY: Creative Commons。PDL1.0: デジタル庁 (採用する国・地方公共団体等が各サイトで適用)。政府標準利用規約 2.0: 内閣官房 IT 総合戦略室 (当時) が作成したひな形を各府省が採用。地理院タイル: 国土地理院。商用の地図 API: 各提供元 |

## 何を求める決まりか

目的: データや地図の作り手を利用者に分かるようにし、利用者が元のデータとその利用条件にたどり着けるようにすることにある。国のオープンデータでは加えて、加工したものが国の作成物と誤認されないようにすることを求める。義務の種類はいずれも契約 (ライセンス) 上の表示義務で、事前の許可や承認ではない。測量法第 30 条第 4 項だけは法律上の表示義務である。

- ODbL 1.0 第 4.3 条: Produced Work (地図画像など) を Publicly Use するときは、それに接する者が、内容がデータベースから得られたことと ODbL で利用できることに気づくよう「reasonably calculated」な通知を付ける。例文として「Contains information from DATABASE NAME, which is made available here under the Open Database License (ODbL).」を示し、データベース名とライセンス名にはリンクを付け、リンクが使えなければ URI を平文で書く。
- ODbL 1.0 第 4.2 条: データベースそのもの (又は Derivative Database) を Publicly Convey するときは、ODbL の写しか URI を同梱し、著作権・データベース権の表示とライセンスへの言及を消さずに残す。ファイルの構造上入れられなければ、利用者が探しそうな場所 (関連ディレクトリ等) に置く。
- OSMF Attribution Guidelines: 第 4.3 条を満たす安全な方法として OSMF が示すもの。法的文言の代わりではなく、両者が食い違えば法的文言が優先すると明記している。
- CC BY 4.0 第 3 条 (a)(1): 共有するとき (改変した形を含む)、ライセンサーが提供していれば作成者の表示、著作権表示、ライセンスへの言及、無保証への言及、合理的に可能な範囲で素材への URI 又はリンクを保持し、改変したか示し、CC BY 4.0 で許諾されていることとその本文又は URI を示す。第 3 条 (a)(2) は媒体と文脈に応じた合理的な方法でよいとし、必要な情報を載せたページへの URI やリンクで足りる場合がある例を示す。
- PDL1.0 1.1: 利用時に出典を記載する。編集・加工した場合は出典とは別に、編集・加工を行ったこと及びその主体を記載する。加工した情報を国等が作成した未加工のもののように公表・利用してはならない (禁止)。1.7 で CC BY 4.0 と互換性があり、CC BY に従った利用も許諾する。
- 政府標準利用規約 (第 2.0 版) 1) ア、イ: 出典の記載と、編集・加工したことの記載を求め、国が作成したかのような態様での公表・利用を禁止する。PDL1.0 と違い「主体」の記載までは条文で求めていない。CC BY 4.0 と互換性がある旨を明記する。PDL1.0 の制定後も、以前の政府標準利用規約に従って利用している場合はその条件が続く (PDL1.0 1.7)。
- 国土地理院: 申請不要の場合でも出典を記載し、編集・加工した場合はその旨を別に記載する (Q&A Q1-15、コンテンツ利用規約)。測量法第 30 条第 4 項は、基本測量成果を使用して刊行物を刊行・ネット公開する者に、その旨の明示を法律上求める。承認を得た場合は承認番号と出所明示の文言の表示が必須 (Q&A Q5-2)。

## 地図プロダクトで当たる場面

| 場面 | 当たるか | 根拠 | 出典 |
|---|---|---|---|
| OSM データから作ったタイルを使うインタラクティブ地図 (ウェブ、アプリ) | 当たる。地図の隅に「OpenStreetMap」(歴史的な「© OpenStreetMap contributors」も可) を表示し、openstreetmap.org/copyright へリンクする。右下が伝統的だが隅ならどこでもよい。操作しないと見えない形は不可。閉じた後、地図の操作後、又は 5 秒後に畳んだり消したりしてよいが、ライセンス情報はたどれるようにする | ODbL 第 4.3 条、Attribution Guidelines | https://osmfoundation.org/wiki/Licence/Attribution_Guidelines |
| OSM の静止画 (スクリーンショット、記事の図) | 当たる。基本はインタラクティブ地図と同じ。一つの文書で複数の画像なら一度の表示でよい。地物 100 未満、面積 10,000 m² 未満、小さなサムネイルやアイコンは除外 | Attribution Guidelines | https://osmfoundation.org/wiki/Licence/Attribution_Guidelines |
| 商用のベースマップの静止画 (記事、README) | 提供元ごとに違う。Geolonia Maps は帰属表示が写っていれば載せてよい (提供元への聞き取り、2026-11-10)。他の提供元は各 provider の reference と規約で確かめる | 提供元への聞き取り | map-compare-infra の providers/geolonia-maps.md |
| OSM の印刷物 (書籍、PDF、紙地図) | 当たる。地図の横、脚注、謝辞など、他の帰属表示が通常置かれる場所に置き、URL「openstreetmap.org/copyright」を印字する | Attribution Guidelines | 同上 |
| OSM を使うジオコーダーやルート検索、それを組み込むアプリ | 当たる。サービスとアプリで OpenStreetMap をクレジットする。個々の結果には表示は不要 (Derivative Database になる場合を除く) | Attribution Guidelines、Geocoding Guideline | https://osmfoundation.org/wiki/Licence/Attribution_Guidelines 、 https://osmfoundation.org/wiki/Licence/Community_Guidelines/Geocoding_-_Guideline |
| OSM 由来のデータベースや抽出ファイルの配布 | 当たる。帰属表示と ODbL 本文又はリンクを、readme やメタデータなど利用者が見る場所に置く | ODbL 第 4.2 条、Attribution Guidelines | https://opendatacommons.org/licenses/odbl/1-0/ |
| 機械学習モデルの学習に OSM を使う | 学習済みモデルはドキュメント (README、ダウンロードページ) で帰属表示。予測結果は ODbL の対象外とされる。OSM を相当部分抽出した学習用データセットは Derivative Database | Attribution Guidelines | https://osmfoundation.org/wiki/Licence/Attribution_Guidelines |
| 動画、ゲーム、グッズ | 当たる。動画はエンドクレジットか説明欄に URL を含めて。地図が主要な要素なら隅にも。第三者の地図が偶然映るだけなら追加不要だが、映っている帰属表示を消してはならない | Attribution Guidelines | 同上 |
| 地理院タイルをリアルタイムで読み込むウェブ地図・アプリ | 当たる。「国土地理院」又は「地理院タイル」等と書き、地理院タイル一覧ページ (https://maps.gsi.go.jp/development/ichiran.html) へリンクする。タイルによっては個別の出典 (例: 写真の「データソース：Landsat8画像（GSI,TSIC,GEO Grid/AIST）…」、GEBCO 等) を追加する | Q&A Q1-12、Q1-19、地理院タイル一覧の各タイルの備考 | https://www.gsi.go.jp/LAW/2930-qa.html 、 https://maps.gsi.go.jp/development/ichiran.html |
| 国土地理院の地図等を加工して載せる | 当たる。出典とは別に加工した旨を書く。例「地理院タイルに○○を追記して掲載」「地理院タイル （標高タイル（基盤地図情報数値標高モデル））を加工して作成」。国土地理院が作成したかのような態様は不可 | Q&A Q1-15、コンテンツ利用規約 | https://www.gsi.go.jp/LAW/2930-meizi.html 、 https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html |
| 測量法の承認を得た地図を公開する | 当たる。承認番号と出所明示の文言を、地図が表示されている間は常に見えるように、出力図にも印刷されるように表示 | 測量法第 30 条第 3 項、第 4 項、Q&A Q5-2 | https://laws.e-gov.go.jp/law/324AC0000000188 、 https://www.gsi.go.jp/LAW/2930-qa.html |
| CC BY 4.0 のデータ (自治体オープンデータ等) を地図に重ねる | 当たる。作成者等、著作権表示、ライセンスへの言及、無保証への言及、素材への URI、改変の有無、CC BY 4.0 の URI。媒体に応じた合理的な方法でよく、必要事項をまとめたページへのリンクで足りる場合がある | CC BY 4.0 第 3 条 (a)(1)、(a)(2) | https://creativecommons.org/licenses/by/4.0/legalcode.en |
| Wikimedia Commons の写真を載せる (名所の写真など) | 写真ごとのライセンスに従う。CC BY 系は、作者 (アップロードした人ではなく、ファイルの説明の「作者」)、ライセンス、ファイルの説明ページへのリンクを添える。パブリックドメインと CC0 は表示の義務はないが、出どころの表示を勧める。Commons の API の作者の欄が「No machine-readable author provided」のときは、ファイルの説明ページで作者を確かめてから載せ、確かめられなければ載せない (推測: リンクだけで足りるとは公式に書かれていない) | Commons の再利用の手引き、Credit line | https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia 、https://commons.wikimedia.org/wiki/Commons:Credit_line |
| PDL1.0 の国・自治体のデータを使う | 当たる。例「出典：「○○動向調査」（D庁）（当該ページのURL）、PDL1.0（規約原文ページのURL）」。加工時は例「「○○動向調査」（D庁）（当該ページのURL）をもとに○○株式会社作成」。提供元が「重要情報」で別の記載例を示していればそれに従う | PDL1.0 1.1 | https://www.digital.go.jp/resources/open_data/public_data_license_v1.0 |
| 政府標準利用規約 (第 2.0 版) のデータを使う | 当たる。例「出典：「○○動向調査」（A 省） （当該ページの URL）」、加工時は「…を加工して作成」。各府省が自サイトで示す記載例に従う | 政府標準利用規約 (第 2.0 版) 1) ア、イ | https://www.digital.go.jp/assets/contents/node/basic_page/field_ref_resources/f7fde41d-ffca-4b2a-9b25-94b8a701a037/a0f187e6/20220706_resources_data_betten_01.pdf |
| 商用の地図 API (タイル、検索、ルート) を使う | 当たる (一般的な形)。多くの提供元は利用規約で、提供元のロゴや著作権表示を地図上に残すこと、消したり隠したりしないこと、提供元が取得した第三者データの表示も残すことを求める。具体的な文言、置き場所、ロゴの要否は提供元ごとに違うので、各提供元の reference (map-compare-infra) を見る | 各提供元の規約 | 各提供元の reference (map-compare-infra) |

## 当たらない場面

- ODbL: Produced Work を作って使うだけで公開しない場合、第 4.2 条の通知は不要 (第 4.3 条前段)。「Publicly」は自分又は 50% 超の所有や指揮命令で支配下にある者以外を指す (第 1 条の定義) ので、組織内の利用は公開に当たらない。Attribution Guidelines も公開時の帰属を対象とし、内部利用は対象外とする。
- OSM の静止画で、地物 100 未満、面積 10,000 m² 未満、小さなサムネイルやアイコン (Attribution Guidelines)。
- OSM のジオコーディングやルート検索の個々の結果 (Derivative Database になる場合を除く) (Attribution Guidelines、Geocoding Guideline)。
- OSM を使った機械学習モデルの予測結果 (Attribution Guidelines)。
- PDL1.0、政府標準利用規約 (第 2.0 版): 数値データ、簡単な表・グラフ等は著作権の対象でないとして利用ルールの適用外で、自由に利用できる (PDL1.0 1. 前文、政府標準利用規約 2.0 解説)。著作権法上認められている引用などは制限しない (PDL1.0 1.7)。
- 国土地理院の地図記号は承認不要で自由に利用できる (Q&A Q1-22)。ただし出典の要否は書かれていない。

## 求められる手続き・表示

- 手続き (申請先、期間、費用): 帰属表示そのものに申請、期間、費用はない。測量法の承認が要る場合の手続は survey-act.md を見る。
- 表示の書き方 (公式の例):
  - OSM のウェブ地図: 「© OpenStreetMap」又は「OpenStreetMap」とし、openstreetmap.org/copyright へリンク。他の文言で OSM 由来でないかのような誤解を与えない。読みやすく理解できる文字にし、WCAG に従うことを推奨 (Attribution Guidelines)。
  - ODbL の例文: 「Contains information from DATABASE NAME, which is made available here under the Open Database License (ODbL).」(第 4.3 条 a)。
  - 地理院タイル: 「国土地理院」又は「地理院タイル」+ 地理院タイル一覧ページへのリンク。加工時「地理院タイルに○○を追記して掲載」。
  - 国土地理院の地図等: 「出典：国土地理院発行2.5万分1地形図」「電子地形図25000（国土地理院）を加工して作成」。ウェブやシステムでは地図の表示中は出典を見えるようにし、技術的に困難なら説明ページや取扱説明書でよい。印刷できるなら印刷物にも (出典の記載例ページ)。
  - PDL1.0: 「出典：D庁ウェブサイト（当該ページのURL）、PDL1.0（規約原文ページのURL）」。URL はリンクにしてもよい。
  - 政府標準利用規約 (第 2.0 版): 「出典：A 省ウェブサイト （当該ページの URL）」。
  - CC BY 4.0: 条文は特定の文言を指定しない。第 3 条 (a)(1) の要素を、媒体に応じた合理的な方法で示す。

## 守らなかった場合

- ODbL: 違反すると許諾は通知なしに直ちに自動で終了する (第 9.1 条)。違反をやめれば 60 日目に恒久的に回復する等の回復規定がある (第 9.4 条)。
- CC BY 4.0: 違反すると権利は自動で終了する (第 6 条 (a))。違反を知ってから 30 日以内に是正すれば是正日に自動で回復する。ライセンサーが明示的に回復させることもできる (第 6 条 (b))。回復しても、ライセンサーの救済を求める権利には影響しない。
- PDL1.0、政府標準利用規約 (第 2.0 版): 違反時の措置を定めた条項は見当たらない。
- 測量法: 第 30 条第 4 項の明示義務違反に罰則を付ける条項は見当たらない (第 61 条から第 66 条を確認)。承認を受けずに複製・使用した場合の罰則は survey-act.md を見る。
- 商用の地図 API: 各提供元の規約による。

## 判断に迷う点

- OSM の帰属を地図の上から消してよいか: Attribution Guidelines は、閉じた後、地図の操作後、又は 5 秒後なら畳んだり消したりしてよいとするが、ライセンス情報にたどれることを条件とする。最初から操作しないと見えない形は不可。
- OSM と他のデータを混ぜた地図の帰属: Attribution Guidelines は、OSM データが一部の地域や地物だけにかかるなら、理想的にはその部分だけを帰属させるが、動的に切り替える必要はないとする。
- 複数のオープンデータを重ねたとき: PDL1.0 と政府標準利用規約 (第 2.0 版) はどちらも CC BY 4.0 との互換性を明記しているので、CC BY 4.0 の方法で表示する道もある。
- 国の利用規約で出典を書いても、測量法など個別法令の制約は外れない (PDL1.0 1.3、政府標準利用規約 2.0 解説 3) は測量法を例に挙げる)。

## 出典

- https://osmfoundation.org/wiki/Licence/Attribution_Guidelines (採択日、最終編集日、インタラクティブ地図・静止画・印刷・動画・ゲーム・データベース・ジオコーディング・機械学習の帰属、法的文言が優先する旨)
- https://opendatacommons.org/licenses/odbl/1-0/ (ODbL 1.0 の第 1 条の定義、第 4.2 条、第 4.3 条、第 9 条の原文)
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Geocoding_-_Guideline (ジオコーダーとアプリのクレジット義務)
- https://creativecommons.org/licenses/by/4.0/legalcode.en (CC BY 4.0 第 3 条、第 6 条の原文)
- https://www.digital.go.jp/resources/open_data/public_data_license_v1.0 (PDL1.0 本文。1.1 出典、1.2 第三者の権利、1.3 個別法令、1.7 制定日と CC BY 互換)
- https://www.digital.go.jp/assets/contents/node/basic_page/field_ref_resources/f7fde41d-ffca-4b2a-9b25-94b8a701a037/a0f187e6/20220706_resources_data_betten_01.pdf (「政府標準利用規約（第 2.0 版）」の解説、平成 27 年 12 月 24 日。出典の記載例、加工の記載、個別法令の例として測量法、CC BY 4.0 との互換)
- https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html (国土地理院コンテンツ利用規約、令和 7 年 11 月 20 日改正。PDL1.0 適用、出典と加工の記載例)
- https://www.gsi.go.jp/LAW/2930-meizi.html (国土地理院の出典の記載例と置き場所)
- https://www.gsi.go.jp/LAW/2930-qa.html (Q1-12、Q1-15、Q1-19、Q1-22、Q5-2)
- https://maps.gsi.go.jp/development/ichiran.html (地理院タイルの利用と出典、タイルごとの個別出典の例、他機関のタイルは各機関の規約が適用される場合がある旨)
- https://laws.e-gov.go.jp/law/324AC0000000188 (測量法第 30 条第 3 項、第 4 項、罰則)

## 未確認のこと

- OSMF Attribution Guidelines の 2021-06-25 採択以後の改訂内容 (ページは 2026-09-10 に編集されているが、どの記述が変わったかは履歴を見ていない)。
- 地理院タイル一覧ページは長く、後半 (約 9 万字) の各タイルの個別出典を全部は読んでいない。使うタイルごとに備考を確かめる必要がある。
- PDL1.0 の各府省・自治体の「重要情報」で示される個別の記載例。提供元ごとに確かめる。
- 政府標準利用規約 (第 2.0 版) の規約本文そのもの (各府省の採用ページ) は読んでおらず、内閣官房の解説資料に引用された条文で確認した。
- 商用の地図 API 各社の帰属要件の具体的な内容 (このファイルでは調べていない。map-compare-infra の各提供元 reference に委ねる)。
- 帰属表示を畳む UI (MapLibre の compact attribution 等) が Attribution Guidelines の「5 秒後に畳んでよい」等の条件を満たすかは、実装ごとの挙動を確かめていない。
