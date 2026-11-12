# ライセンスを混ぜたときの条件

対象: ODbL、CC BY、CC0、CDLA、PDL、政府標準利用規約のデータを、1 つの地図やデータベースに混ぜたときに何が求められるか (派生データベース、Produced Work、出典表示の並べ方)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |

## 概要

地図の主題データは、OSM や Overture (ODbL)、公的データ (PDL1.0、政府標準利用規約、CC BY 4.0)、企業や団体の提供データ (CDLA-Permissive-2.0、CC0、Apache-2.0) を組み合わせることが多い。条件が最も重いのは ODbL の share-alike で、混ぜ方によって自分のデータまで ODbL で出す義務が生じ得る。ここでは各ライセンスが混ぜたときに何を求めるか、OSMF がどの混ぜ方を共有義務の外と見ているか、出典表示をどう並べるかをまとめる。法的な判断は条文と公式ガイドラインに書かれた範囲にとどめ、それ以外は推測と書く。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| Produced Work (画像、印刷物、ラスタタイル) として出す | ODbL 4.3 により Produced Work は通知だけでよく、Produced Work 自体を ODbL にする義務はない | 元データの抽出を目的にした出力はデータベース扱い。派生データベースから作った Produced Work を公に使うなら、派生データベースか変更点の提供の申し出が要る (ODbL 4.6)。ベクトルタイルが Produced Work かは OSMF のガイドラインで確認できなかった | 特定のツールに依らない | https://opendatacommons.org/licenses/odbl/1-0/ 、https://osmfoundation.org/wiki/Licence/Community_Guidelines/Produced_Work_-_Guideline |
| 地物の種類ごとに出所を分ける (水平レイヤー) | 地物の種類 (Feature Type) のデータが全部 OSM 以外なら、その種類に ODbL の share-alike はかからない。例: OSM を背景にして鳥の渡りの経路を重ねる、OSM の飲食店を除いて自前の飲食店レイヤーを載せる | 同じ種類で OSM と他データを補い合うと、別レイヤーにしても共有義務がかかる。例: OSM にない墓地だけを集めたレイヤー、OSM と見比べて追加した飲食店 | 特定のツールに依らない | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Horizontal_Map_Layers_-_Guideline (2014-06-06 承認) |
| Collective Database として組む | 同じ地域の切り出しの中で、データの種類ごとに全部 OSM か全部 OSM 以外なら、共有義務は OSM 部分だけ。物理的に分ける必要はない。OSM 以外のデータが主要な地物の形状や属性を丸ごと置き換えるか、OSM にない形状や属性を足す場合も含む | OSM と他データが互いを参照しないことは、選べる条件の一つにすぎない (Guideline の条件は「または」でつながる)。キーでの結合 (本番の性能のための結合も) は参照とみなされるが、参照していても、データの種類ごとに全部 OSM か全部 OSM 以外なら Collective Database になる (Guideline の例では、OSM の飲食店にキーで結び付けた自社の電話番号に share-alike はかからない)。自社の店舗一覧と OSM を突き合わせて重複を消した統合データは対象外で、公に使うと share-alike がかかり得る | 特定のツールに依らない | https://osmfoundation.org/wiki/Licence/Community_Guidelines/Collective_Database_Guideline_Guideline (2016-06-17 承認)、ODbL 4.5 |
| ODbL を避けられる出所を選ぶ | Overture の places は OSM を含まず、主に CDLA-Permissive-2.0 で、共有時に規約本文を添えるだけでよい | Overture 自身が「places を OSM と結合すると結果に ODbL が要ることがある」と書いている。buildings、transportation、divisions、base は ODbL | Overture `2026-10-21.0` | https://docs.overturemaps.org/guides/places/ 、https://cdla.dev/permissive-2-0/ |
| 公的データは CC BY 4.0 として扱う | PDL1.0 と政府標準利用規約 (第 2.0 版) は CC BY 4.0 と互換で、CC BY に従った利用もできると明記している。CC BY 4.0 のデータと同じ条件でまとめられる | 各規約の出典表示と加工表示の条件は残る。第三者の権利を含むものは別途許諾が要る | 特定のツールに依らない | https://www.digital.go.jp/resources/open_data/public_data_license_v1.0 (1.7.3)、「政府標準利用規約（第 2.0 版）」の解説 (平成 27 年 12 月 24 日) |
| 出典表示をまとめて出す | 複数の出所の表示を地図の隅に並べる。OSMF は他の表示を OSM の表示と同時に、隣に出すことを認める | 他の表示が「OSM のデータが OSM 由来でない」と誤解させてはならない。OSM を使っていない範囲や地物では OSM 表示を出さないほうが望ましい (動的な切り替えは任意) | MapLibre GL JS などの地図ライブラリはソースごとの attribution を地図の隅に並べる機能を持つ (版は未確認) | https://osmfoundation.org/wiki/Licence/Attribution_Guidelines (2021-06-25 採択) |

## 判断を左右すること

- 出すものがデータベースか Produced Work か。画像や印刷物は Produced Work。ダンプや、元データの抽出を目的にした出力はデータベース。ベクトルタイルや API の応答がどちらかは公式ガイドラインで確認できなかった (未確認)。
- 公に使うか (Publicly Use)。ODbL の share-alike と提供の申し出は公に使うときにかかる。内部利用だけなら出典表示のガイドラインも対象外としている。
- 地物の種類ごとに出所が 1 つか。同じ種類 (例: 飲食店、建物) で OSM と他データを突き合わせる、補う、重複を消すと共有義務が他データにも及ぶ。
- 混ぜる相手のライセンスが ODbL の派生データベースに入れられるか。CDLA-Permissive-2.0 は OSMF が互換と書いている。CC BY 系は OSM 本体への取り込みには明示の許諾が要るとしている。自前の派生データベースを ODbL で出すときに CC BY 4.0 のデータを含められるかは公式の記述を確認できなかった (未確認)。
- 公的データの規約が PDL1.0 か政府標準利用規約か CC BY 4.0 か、と第三者の権利の有無 (ロゴや登記所備付地図データのような別規約)。

## 手順

1. 使うデータを出所ごとに一覧にし、ライセンス、版、取得日、出典表示の公式の文例を書く。
2. 出すものを決める: 画像・印刷物 (Produced Work)、ベクトルタイル、API、ダウンロード用データ。後の 3 つはデータベース扱いになり得る。
3. 地物の種類ごとに出所を 1 つに決める。ODbL のデータとそれ以外を同じ種類で突き合わせる設計なら、統合結果を ODbL で出す前提にするか、設計を変える。
4. ODbL の派生データベースを公に使うなら、派生データベース全体か変更点を機械可読で提供する場所を用意する (ODbL 4.6)。
5. CDLA-Permissive-2.0 のデータを共有するなら規約本文を添える。PDL1.0 と政府標準利用規約のデータは出典と、加工したなら加工した旨と主体を書く。
6. 地図の隅の出典表示を、使っている全出所について並べる。OSM の表示は「OpenStreetMap」と ODbL の明示 (copyright ページへのリンク) にする。
7. 判断に迷う組み合わせは OSMF や各データの提供者に確かめ、記録を残す。

## 落とし穴

- 自社の POI と OSM の POI を「重複を消して 1 つにまとめる」と、OSMF のガイドラインの対象外となり、自社データにも share-alike がかかり得る。
- 「別レイヤーにしたから大丈夫」は成り立たない。同じ種類の地物を補い合えばレイヤーが分かれていても共有義務がかかる。
- キーで結合しているだけでも「参照」とみなされる。ただし、参照しないことは Collective Database の条件の一つにすぎない。参照していても、ある種類のデータが同じ地域の切り出しの中で全部 OSM か全部 OSM 以外なら Collective Database として扱える。
- Overture を使えば ODbL を避けられるとは限らない。places 以外の主要テーマは ODbL。
- CC BY 4.0 は技術的保護手段 (DRM) を課して配布することを禁じており、OSMF はこれを ODbL の配布条件と衝突するとして許諾を求めている。DRM のかかるアプリ配布に CC BY 4.0 のデータを含めるときは同じ論点があり得る (推測)。
- 加工した公的データを「国が作った未加工のデータ」に見えるように出すことは PDL1.0 で禁止されている。
- Overture の公開リリースは 60 日で消える。出典表示に版と取得日を書くなら、元のファイルも保存しておかないと後で確かめられない。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- ODbL 1.0: 組み込み (自分のデータベースに取り込む) では、派生データベースか Collective Database かで変わる。改変したデータベースを公に使うなら ODbL (または後継・互換) で出す (4.4)。派生データベースか、それから作った Produced Work を公に使うなら、派生データベースか変更点の提供を申し出る (4.6)。Produced Work を公に使うときはデータベース由来である旨の通知が要る (4.3)。権利を制限する追加の条件や技術的手段は、制限のない版も提供しない限り課せない (4.7)。SaaS で地図画像だけを返す場合は Produced Work の扱いになる (推測、ODbL の定義と OSMF の Produced Work ガイドラインからの読み)。
- CC BY 4.0: 出典 (作者、著作権表示、ライセンス表示、免責表示、URI) の保持と、改変したことの表示が要る。DRM などの技術的保護手段で受け手の権利を制限してはならない (第 2a5B 節)。継承 (share-alike) 条件はない。
- CC0 1.0: 権利の放棄で、出典表示の義務はない。OSMF は CC0 は一般に互換だが、提供者が持たない第三者の権利までは放棄されないと注意している。
- CDLA-Permissive-2.0: データを共有するときは規約本文を添える (2.1 節)。分析結果 (Results) の利用や共有には制約がない (3.1 節)。出典表示の義務は本文にない。OSMF は互換としている。
- Apache-2.0 (Overture places の Foursquare 分): Overture は著作権表示と NOTICE.txt を示している。データへの Apache-2.0 の適用の細部は本調査では読んでいない。
- PDL1.0 (2024-07-05 制定): 複製、公衆送信、翻案、商用利用を認める。出典表示、加工時の加工表示と主体の表示が条件。CC BY 4.0 と互換で CC BY に従う利用も許す (1.7.3)。デジタル庁は、政府標準利用規約や CC BY 4.0 を適用していたサイトにも PDL1.0 の利用を案内している。
- 政府標準利用規約 (第 2.0 版、平成 27 年 12 月 24 日): CC BY 4.0 と互換で、CC BY に従った利用もできると明記している。以前の版で利用している場合はその条件が続く。
- ODbL と CC BY 4.0、PDL1.0、政府標準利用規約の互換性: 公的機関の公式な説明は見つからなかった。東京都の 2022 年の資料は CC ライセンスについて ODbL と互換性がない点を弱点に挙げている (検索結果の要約で見ただけで、本文は読んでいない)。

## 出典

- https://opendatacommons.org/licenses/odbl/1-0/ : Collective Database、Derivative Database、Produced Work の定義と 4.3〜4.7。
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Collective_Database_Guideline_Guideline : 2016-06-17 承認、独立なデータベースの条件、参照の扱い、例。
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Horizontal_Map_Layers_-_Guideline : 2014-06-06 承認、地物の種類ごとの判断、共有が要る例と要らない例。
- https://osmfoundation.org/wiki/Licence/Community_Guidelines/Produced_Work_-_Guideline : 2014-06-06 承認、Produced Work の範囲、抽出目的の出力はデータベース。
- https://osmfoundation.org/wiki/Licence/Attribution_Guidelines : 2021-06-25 採択、OSM の表示の書き方、他の表示との並べ方。
- https://osmfoundation.org/wiki/Licence/Licence_Compatibility : CC0、CC BY 系、CDLA Permissive 2.0 の扱い。
- https://blog.openstreetmap.org/2017/03/17/use-of-cc-by-data/ : CC BY 4.0 に明示の許諾を求める理由 (出典表示の方法と DRM の禁止)。
- https://cdla.dev/permissive-2-0/ : CDLA-Permissive-2.0 の 2.1 節と 3.1 節。
- https://creativecommons.org/licenses/by/4.0/legalcode.ja : CC BY 4.0 の表示の条件と第 2a5B 節 (条文の項番は OSMF の記事からも確認した)。
- https://www.digital.go.jp/resources/open_data/public_data_license_v1.0 : PDL1.0 の許諾範囲、出典と加工の表示、CC BY 4.0 との互換、制定日。
- https://www.digital.go.jp/resources/open_data : PDL1.0 の利用の案内、政府標準利用規約 (第 2.0 版) を参考として掲載。
- https://www.digital.go.jp/assets/contents/node/basic_page/field_ref_resources/f7fde41d-ffca-4b2a-9b25-94b8a701a037/a0f187e6/20220706_resources_data_betten_01.pdf : 「政府標準利用規約（第 2.0 版）」の解説。CC BY 4.0 との互換の条文と理由。
- https://docs.overturemaps.org/attribution/ と https://docs.overturemaps.org/guides/places/ : Overture のテーマごとのライセンスと、places と OSM を結合したときの注意。

## 未確認のこと

- ベクトルタイルや API の応答が ODbL の Produced Work か Derivative Database か。OSMF の公式ガイドラインでの明記は見つからなかった。
- ODbL の派生データベースに CC BY 4.0、PDL1.0、政府標準利用規約のデータを含めて ODbL で出せるか (再ライセンスの可否)。公的機関と OSMF のどちらの公式見解も確認できなかった。
- OSMF の PDL Japan の扱い (Licence Compatibility のページから「PDL Japan and variants」へのリンクがあるが、本調査では該当ページを開けなかった)。
- MapLibre GL JS などで複数の出典表示を並べる機能の具体的な版と挙動。
- CC BY 4.0 の表示を ODbL の OSM 表示と同じ場所にまとめる書き方について、Creative Commons 側の公式の文例。
- 東京都の 2022 年資料の該当箇所の原文。
