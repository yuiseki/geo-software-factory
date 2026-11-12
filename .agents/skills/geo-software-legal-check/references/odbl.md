# ODbL の派生データベースと Produced Work

対象: ODbL 1.0 の条文、OSMF のコミュニティガイドライン (Substantial、Produced Work、Collective Database、Geocoding)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 根拠 (法令名と条、規約の版) | Open Database License (ODbL) v1.0 第 1 条 (定義)、第 4.2 条から第 4.7 条、第 9 条。OSMF Community Guidelines: Substantial (2014-06-06 OSMF 理事会承認、ページ最終編集 2018-02-27)、Produced Work (2014-06-06 承認、最終編集 2016-07-31)、Horizontal Map Layers (2014-06-06 承認、最終編集 2016-07-31)、Collective Database (2016-06-17 承認、最終編集 2016-07-31)、Geocoding (2017-08-24 承認、最終編集 2017-08-29)、Trivial Transformations (最終編集 2016-07-31。状態の記載が食い違う、下記)。帰属は OSMF Attribution Guidelines (2021-06-25 採択) |
| 所管・管理者 | ライセンス本文: Open Data Commons。OSM データのライセンサーとガイドライン: OpenStreetMap Foundation (OSMF) と License Working Group |

## 何を求める決まりか

目的: OSM のデータを誰でも使えるようにしつつ、データを足したり直したりしたデータベースを公開に使うなら同じ条件で共有させること (share-alike) と、データを使った成果物 (地図画像など) には出どころを示させることにある。地図画像のような成果物そのものには share-alike をかけない設計である。義務の種類はライセンス (契約) 上の表示と共有の義務で、事前の許可や承認ではない。

定義 (第 1 条):

- Derivative Database: Database に基づくデータベースで、Database 又は Contents の Substantial な部分の翻訳、翻案、配列、修正その他の変更を含む。Contents の全部又は Substantial な部分を新しいデータベースへ Extraction 又は Re-utilisation することを含む。
- Collective Database: Database を未変更のまま、それ自体独立したデータベースの集まりの一部として組み込んだもの。Collective Database は Derivative Database とみなさない。
- Produced Work: Database、Derivative Database、又は Collective Database の一部としての Database から、Contents の全部又は Substantial な部分を (検索その他の問い合わせで) 使った結果生じる著作物 (画像、映像、テキスト、音など)。
- Publicly: 自分以外の者、又は 50% 超の所有か活動を指揮する力 (独立コンサルタントとの契約等) で自分の支配下にある者以外の者に対して。
- Substantial: 量又は質、又はその組み合わせで相当なもの。非相当部分の反復的かつ系統的な Extraction や Re-utilisation は Substantial な部分の Extraction や Re-utilisation になりうる。
- Convey: 他者がデータベースの複製を作るか受け取れるようにすること。コンピュータネットワーク越しの利用者とのやり取りや、Produced Work を作って使うことで、データベースの複製が移転しないものは含まない。

義務:

- 第 4.2 条 (通知、表示): Database、Derivative Database、Collective Database の一部としての Database を Publicly Convey するときは、ODbL 又は第 4.4 条で認められたライセンスでのみ行い、ライセンスの写しか URI を同梱し、権利表示とライセンスへの言及を残す。
- 第 4.3 条 (Produced Work の表示): Produced Work を作って使うだけなら第 4.2 条の通知は不要。Produced Work を Publicly Use するときは、それに接する者がデータベース由来であることと ODbL で利用できることに気づくよう合理的に計算された通知を付ける。
- 第 4.4 条 (share-alike): Publicly Use する Derivative Database は、ODbL、同趣旨の後継版、又は互換ライセンスでのみ提供する (a)。Contents の全部又は Substantial な部分を新しいデータベースへ抽出・再利用すれば Derivative Database であり第 4.4 条に従う (b)。Derivative Database から作った Produced Work を Publicly Use すれば、その Derivative Database も Publicly Use されたことになる (c)。ODbL と両立しない権利の Contents を Derivative Database に加えてはならない (d、禁止)。
- 第 4.5 条 (share-alike の限界): Collective Database 全体を ODbL にする必要はないが、その中の Database には ODbL が及ぶ (a)。Produced Work を作ることは第 4.4 条の目的では Derivative Database を作ることにならない (b)。組織内での Derivative Database の利用は公開ではなく第 4.4 条の対象外 (c)。
- 第 4.6 条 (Derivative Database へのアクセス): Derivative Database、又は Derivative Database から作った Produced Work を Publicly Use するときは、受け手に、Derivative Database 全体か、Database との差分すべて (又は変更の方法、アルゴリズム等) を含むファイルを機械可読な形で提供すると申し出る。ネット配布なら無償、物理配布なら合理的な実費以下。
- 第 4.7 条 (技術的手段と追加条件): ライセンスの条件や権利を変えたり制限したりする条件や技術的手段 (DRM 等) を課してはならない。ただし制限のない複製を追加費用なしで並行して提供する場合は課してよい。

## 地図プロダクトで当たる場面

| 場面 | 当たるか | 根拠 | 出典 |
|---|---|---|---|
| OSM から作ったラスタータイルや PNG、PDF、印刷地図を公開する | Produced Work。share-alike はかからないが、帰属表示 (第 4.3 条) が要る | 第 4.3 条、第 4.5 条 (b)。Produced Work Guideline は PNG、JPG、PDF、SVG とラスター画像、印刷物の地図を通常 Produced Work とする | https://opendatacommons.org/licenses/odbl/1-0/ 、 https://osmfoundation.org/wiki/Licence/Community_Guidelines/Produced_Work_-_Guideline |
| OSM の planet ダンプや抽出データ、元データを取り出すことを意図した出力を配布する | Produced Work ではなくデータベースとして扱われる。Publicly Convey なら第 4.2 条、加工していれば Derivative Database として第 4.4 条 | Produced Work Guideline は、元データの抽出を意図した出力はデータベースであり Produced Work ではないとし、planet ダンプのようなデータベースダンプを例に挙げる | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Produced_Work_-_Guideline |
| OSM に自社データを足したり、OSM のデータを修正したりして、そのデータから地図を公開する | 足した・直したデータベースは Derivative Database。そこから作った地図を公開すれば Derivative Database も Publicly Use されたことになり、share-alike と第 4.6 条の差分提供がかかる | 第 4.4 条 (a)(c)、第 4.6 条 | https://opendatacommons.org/licenses/odbl/1-0/ |
| OSM のベースマップの上に、OSM と関係のない自社データ (例: 鳥の渡りの経路) を別レイヤーで重ねる | 地物の種類 (Feature Type) ごとに全部が非 OSM なら、その種類には share-alike がかからない | Horizontal Map Layers Guideline。根拠として第 4.5 条 (b) を引く | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Horizontal_Map_Layers_-_Guideline |
| OSM の飲食店を全部除き、自社の飲食店レイヤーに置き換える | 同じ種類を全部非 OSM で置き換えるので share-alike はかからない (Guideline の例) | Horizontal Map Layers Guideline、Collective Database Guideline | 同上、 https://osmfoundation.org/wiki/Licence/Community_Guidelines/Collective_Database_Guideline_Guideline |
| 同じ種類の地物で OSM と自社データを混ぜる、OSM と比べて足りないものだけ足す (例: 「OSM にない墓地」レイヤー) | share-alike がかかる (別レイヤーでも) | Horizontal Map Layers Guideline | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Horizontal_Map_Layers_-_Guideline |
| OSM と非 OSM のデータを一つのデータベースに組み合わせる | 地域の区切り (regional cut) の中で、ある種類のデータが全部 OSM か全部非 OSM なら Collective Database。非 OSM データと OSM データの参照はデータベースのキー等でよい | Collective Database Guideline | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Collective_Database_Guideline_Guideline |
| 住所から緯度経度を求める (正引き) / 緯度経度から住所を求める (逆引き) ジオコーディングの結果を自社データと一緒に保存する | ジオコーダーの OSM データが未変更か Trivial な変更だけで、結果を集めて OSM の全部又は Substantial な部分を含む新しいデータベースを作らないなら、share-alike はかからない。名前、住所、緯度経度だけを含み、市規模以上の主要地物の大半を系統的に集めようとしていなければ Substantial な抽出ではない。ジオコーダーとそれを組み込むアプリは OpenStreetMap をクレジットする | Geocoding Guideline。同 Guideline は、ジオコーディング結果を Produced Work と宣言する案を ODbL の文言になじまないとして採らなかった | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Geocoding_-_Guideline |
| OSM から少数の地物を取り出して使う | 100 地物未満、又は人口 1,000 人までの地域の地物は Substantial ではない。100 地物超でも、非系統的で自分の質的な基準による一回限りの抽出なら Substantial ではない。同じ目的の小さな抽出の反復は一つの大きな抽出とみなす。ある地域の飲食店すべての抽出は系統的 | Substantial Guideline | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Substantial_-_Guideline |
| OSM データの形式変換 (JSON、MySQL 等)、座標系の変換、フィルタによる部分抽出、道路や面の単純化 | Trivial Transformation。他のデータ源が関わらなければ共有すべき情報を加えない。データの追加や修正は決して Trivial ではない | Trivial Transformations Guideline | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Trivial_Transformations_-_Guideline |
| OSM の Derivative Database を、受け手の権利を制限する条件や技術的手段 (DRM など) を付けて提供する | 第 4.7 条 (a) で禁止。制限のない複製を追加費用なしで並行提供する場合のみ可 (第 4.7 条 (b))。料金を取ること自体は禁止されていない (第 3.1 条は商用利用を含むとする)。ただし Publicly Use する場合は第 4.6 条の複製の提供が要る | 第 4.7 条 | https://opendatacommons.org/licenses/odbl/1-0/ |
| OSM を相当部分抽出した機械学習の学習データセット | Derivative Database。学習済みモデルはドキュメントで帰属。予測結果は ODbL の対象外とされる | Attribution Guidelines | https://osmfoundation.org/wiki/Licence/Attribution_Guidelines |

## 当たらない場面

- 組織内だけでの Derivative Database の利用は公開ではなく、share-alike (第 4.4 条) の対象外 (第 4.5 条 (c))。「Publicly」の定義上、50% 超の所有等で支配下にある者への提供も公開に当たらない (第 1 条)。
- Produced Work を作って使うだけで公開しないなら第 4.2 条の通知は不要 (第 4.3 条)。
- Produced Work を作ることは、第 4.4 条の目的では Derivative Database を作ることにならない (第 4.5 条 (b))。
- Collective Database 全体を ODbL にする必要はない (第 4.5 条 (a))。
- ネットワーク越しの利用者とのやり取りや、Produced Work を作って使うことで、データベースの複製が移転しないものは Convey に当たらない (第 1 条 Convey の定義)。
- Substantial でない抽出 (Substantial Guideline の基準内) は、Derivative Database の定義 (Substantial な部分の抽出) に当たらない。
- Geocoding Guideline の条件を満たすジオコーディング結果の保存。

## 求められる手続き・表示

- 手続き (申請先、期間、費用): ODbL の利用に申請や費用はない。Derivative Database を公開に使う場合は、Derivative Database 全体か差分ファイルを機械可読な形で、ネット配布なら無償で提供すると受け手に申し出る (第 4.6 条)。
- 表示の書き方 (公式の例): ODbL の例文「Contains information from DATABASE NAME, which is made available here under the Open Database License (ODbL).」で、DATABASE NAME はデータベース名とその URI へのリンク、「Open Database License」はライセンス本文へのリンク。リンクが使えなければ URI を平文で添える (第 4.3 条 a)。OSM では「OpenStreetMap」(又は「© OpenStreetMap contributors」) を openstreetmap.org/copyright へリンクする形を OSMF が示している。置き場所の詳細は attribution.md を見る。

## 守らなかった場合

- 違反すると許諾は通知なしに直ちに自動で終了する (第 9.1 条)。違反者から正しく受け取った者の許諾は、その者が遵守していれば終了しない。第 1 条、第 2 条、第 7 条から第 10 条は終了後も存続する。
- 違反をやめると、違反をやめてから 60 日目までは暫定的に回復し、ライセンサーから合理的な通知がなければ 60 日目に恒久的に回復する。ライセンサーから初めて違反の通知を受け、所定の期間内に是正した場合にも恒久的に回復する (第 9.4 条)。
- 違反がなければライセンサーは権利を終了させない (第 9.2 条)。

## 判断に迷う点

- Produced Work か データベースか: Produced Work Guideline は、元データの抽出を意図しているかで分ける。意図した出力はデータベース。
- 別レイヤーにすれば share-alike を避けられるか: Horizontal Map Layers Guideline は、レイヤーの分け方ではなく地物の種類で判断する。同じ種類で OSM と非 OSM を混ぜれば別レイヤーでも share-alike がかかる。OSM と比較して作ったレイヤーも share-alike がかかる。
- ジオコーディング結果の大量保存: 結果を集めて OSM の Substantial な部分を含むデータベースにすると Derivative Database になりうる (Geocoding Guideline)。
- ガイドラインの効力: Community Guidelines の目次ページは、ガイドラインは方針を指図するものではなく、ライセンサーの見解として利用者や裁判官に重みを持ちうるが、最終判断は裁判所がすると書く。Attribution Guidelines も法的文言の代わりではなく、食い違えば法的文言が優先するとする。ガイドラインに沿っても法的な結論は保証されない。

## 出典

- https://opendatacommons.org/licenses/odbl/1-0/ (ODbL 1.0 原文。第 1 条の定義、第 4.2 条から第 4.7 条、第 9 条を取得して確認)
- https://osmfoundation.org/wiki/Licence/Community_Guidelines (ガイドラインの目次と効力についての記述。最終編集 2022-11-21)
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Substantial_-_Guideline (100 地物、人口 1,000 人、反復・系統的抽出の基準。2014-06-06 承認)
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Produced_Work_-_Guideline (抽出を意図するかの基準、通常 Produced Work とされる形式。2014-06-06 承認)
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Collective_Database_Guideline_Guideline (regional cut ごとに種類単位で全部 OSM か全部非 OSM なら Collective Database。2016-06-17 承認)
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Horizontal_Map_Layers_-_Guideline (Feature Type 単位の判断と例。2014-06-06 承認)
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Geocoding_-_Guideline (正引き・逆引き、結果の保存、クレジット。2017-08-24 承認)
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Trivial_Transformations_-_Guideline (形式変換、座標変換、フィルタ、単純化の例)
- https://osmfoundation.org/wiki/Licence/Attribution_Guidelines (機械学習と帰属の扱い。2021-06-25 採択)

## 未確認のこと

- ベクトルタイル (MVT、PMTiles 等) が Produced Work かデータベースか。Produced Work Guideline はベクトルタイルに触れていない。元データの抽出を意図するかの基準では判断が分かれうる (推測)。OSMF の公式の見解を見つけられなかった。
- Trivial Transformations Guideline の状態: 目次ページは承認済み (endorsed) の一覧に載せるが、ガイドラインのページ自体は「at the proposal stage」と書く。どちらが現状かは確かめられなかった。
- Regional Cuts Guideline (目次では承認済み) の本文は読んでいない。Collective Database Guideline の「regional cut」の範囲はこれに依る。
- OSMF のガイドラインのうち、目次に載らない「new and evolving guidelines」の一覧と状態は確かめていない。
- 第 4.4 条 (a)(iii) の互換ライセンスについて、OSMF が代理人として互換を認めたライセンスがあるか (第 4.4 条 (e)) は調べていない。
- ODbL の条文の日本語訳は公式のものを確認していない。このファイルの訳は英語原文からの要約である。
