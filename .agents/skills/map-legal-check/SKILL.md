---
name: map-legal-check
description: 地図プロダクトを公開する前に、法令と規約と権利の確認をする。帰属表示、ODbL の派生データベース、測量法による地図の複製・使用の承認 (地理院地図、基盤地図情報)、位置情報と個人情報、電気通信事業法の外部送信規律、地図 API の規約 (キャッシュ、併用、機械学習への利用)、地図に載せる YouTube の埋め込みと iTunes の試聴の規約、中国・韓国の規制を、条文と公式の案内で確かめる。「地図を公開して大丈夫か」「帰属表示はどう書く」「地理院の地図を使うのに申請は要るか」「位置情報を集めたい」と言われたら使う。
---

# map-legal-check

地図プロダクトを公開する前に、法令、規約、権利の確認をする。プロダクトの使い方から当たる決まりを洗い出し、決まりごとに「何を求めるか」「当たるか」「何をすればよいか」を、条文と公式の案内で確かめて並べる。法的な判断は断定せず、公式の記述が無いところは推測と書き、専門家に確かめるべき点として残す。

| reference | 読むとき | 中身 |
|---|---|---|
| [survey-act](references/survey-act.md) | 国土地理院の地図や基盤地図情報を使うとき | 測量法による複製・使用の承認 |
| [attribution](references/attribution.md) | どの地図でも、公開の前に | 帰属表示の要件 |
| [odbl](references/odbl.md) | OSM 由来のデータを加工・配布するとき | ODbL の派生データベースと Produced Work |
| [location-privacy](references/location-privacy.md) | 利用者の位置情報を集めるとき | 位置情報と個人情報 |
| [external-transmission](references/external-transmission.md) | 地図 SDK や解析ツールが利用者の情報を外部に送るとき | 電気通信事業法の外部送信規律 |
| [api-terms](references/api-terms.md) | 商用の地図 API を使うとき | 地図 API の規約で引っかかりやすい条項 |
| [youtube-embed](references/youtube-embed.md) | 地図に YouTube の動画やライブ配信を埋め込む、配信の状態や視聴者数を取るとき | YouTube API Services の規約 (埋め込み、保存、帰属、割当て) |
| [itunes-search-api](references/itunes-search-api.md) | 地図に iTunes Search API の試聴やアートワークを出すとき | Promo Content の条件、バッジ、帰属 |
| [map-compare-infra の regional/china](../map-compare-infra/references/regional/china.md) | 中国本土が対象に入るとき | 中国の地図の規制 |
| [map-compare-infra の regional/korea](../map-compare-infra/references/regional/korea.md) | 韓国が対象に入るとき | 韓国の地図データの規制 |

## 入力

確認の前に、プロダクトの使い方をそろえる。プロダクト概要と、技術選定の結果 (map-compare-arch、map-compare-infra、map-compare-library、map-compare-data) があればそこから読み、無ければ依頼から読み取る。

- 使う地図とデータ: ベースマップの供給元、主題データの出どころ (国土地理院のもの、OSM 由来、国や自治体のオープンデータ、商用 API)
- 使い方: その場で読み込むだけか、自社のサーバーに複製して配るか、加工するか (陰影図を作る、注記を直す、自社のデータを足す)、端末にキャッシュするか、解析や機械学習に使うか
- 公開の形: 不特定多数に公開するか、社内だけか。Web、アプリ、印刷物
- 利用者の情報: 位置情報を集めるか、保存するか、第三者 (海外の事業者を含む) に送るか。地図 SDK や解析ツールが外部に送る情報
- 事業の形: 電気通信事業に当たる役務か (オンライン地図サービスなど)、受託で納品するか
- 対象地域: 中国本土、韓国を含むか

使う地図とデータ、使い方、利用者の情報の 3 つが分からないまま確認に入らない。当たる決まりがこの 3 つで決まるので、分からなければ先に聞く。聞くときは選択肢で答えられる形にし、1 回に聞く数を絞る。

## 進め方

1. 入力から、当たりうる決まりを洗い出す。下の表の「当たる兆し」に 1 つでも当てはまれば、その reference を開く。

   | 当たる兆し | 開く reference |
   |---|---|
   | 地理院タイル、地理院地図、基盤地図情報を使う。とくに複製して配る、加工する、オフライン用に保存する | [survey-act](references/survey-act.md) |
   | 地図を公開する (どの地図でも) | [attribution](references/attribution.md) |
   | OSM や、OSM を含むデータ (Overture の一部のテーマなど) を加工する、自社のデータと混ぜる、配る | [odbl](references/odbl.md)、map-compare-data の license-mixing |
   | 利用者の位置情報を取得、保存、分析、第三者に提供する。海外の事業者のクラウドや API に送る | [location-privacy](references/location-privacy.md) |
   | Web やアプリで、地図 SDK、タイル API、解析ツールが利用者の端末の情報を外部に送る | [external-transmission](references/external-transmission.md) |
   | 商用の地図 API を使う。とくにキャッシュ、他社の地図との併用、解析や機械学習、オフライン、政府案件 | [api-terms](references/api-terms.md) と map-compare-infra の各提供元の reference |
   | 地図の上に YouTube の動画やライブ配信を埋め込む、YouTube Data API を使う | [youtube-embed](references/youtube-embed.md) |
   | 地図の上で iTunes Search API の試聴を鳴らす、アートワークを出す | [itunes-search-api](references/itunes-search-api.md) |
   | 対象地域に中国本土、韓国が入る | map-compare-infra の regional/china、regional/korea |

2. 決まりごとに、reference の「何を求める決まりか」を先に読み、その決まりが何を守ろうとしているかを書く。続けて、当たるかどうかを、reference の「地図プロダクトで当たる場面」と「当たらない場面」に照らして判断する。
3. 義務の種類 (許可、承認、届出、同意、通知、公表、表示、禁止) を区別して、何をすればよいかを書く。手続 (申請先、期間、費用) と、表示の文面 (出典、帰属、加工の表示) は、公式の例を写す。
4. 公式の記述 (条文、ガイドライン、Q&A) で判断できないものは、推測と明記し、「専門家や所管に確かめること」として残す。他社がどうしているかは根拠にしない。
5. 条文、ガイドライン、規約は、答える前に公式のページで確かめ直す。reference の確認日 (2026-11-10 など) から改正や改定があれば新しいものを使い、変わったことを書く。
6. 「出力」の形で答える。

## 出力

答えは次の順に並べる。

1. 結論: 公開の前にしなければならないことの一覧 (手続、表示、同意の取り方、設定の変更)。急ぐもの (公開前に要る手続) を先に。
2. 決まりごとの表: 行に決まり、列に「何を求めるか」「当たるか」「根拠 (条文の番号、公式の資料)」「すること」。
3. 表示の文面: 地図に置く出典と帰属、加工の表示、利用者への通知・公表の項目を、そのまま使える形で。
4. 当たらないと判断したものと、その根拠。
5. 専門家や所管に確かめること: 公式の記述で判断できなかった点。
6. 確かめた日: 条文と公式の資料を確かめた日と、その版 (改正日、改定日)。

## 注意

- 法的な判断を断定しない。条文や公式の資料から読んだことと、推測を分けて書く。
- 条文は番号つきで引く。ガイドラインや Q&A は、名前、版、項目の番号を書く。
- 他社の事例や業界の慣行を根拠にしない。
- 義務の種類を混ぜない (例: 「公表」と「本人の知り得る状態に置く」は違う、委託でも外国にある第三者への提供の規律は外れない)。
- 公共案件や受託開発では、発注者の規程 (情報セキュリティの規程、クラウドの利用条件) も別にかかることがある。reference では調べていないので、発注者に確かめるよう書く。
