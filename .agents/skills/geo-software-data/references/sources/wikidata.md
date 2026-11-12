# Wikidata

対象: Wikidata の項目 (名所、施設、行政区画などの ID、座標、画像、多言語の名前)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 提供者 | Wikimedia Foundation が運営する共同編集のデータベース |
| 配布ページ | https://www.wikidata.org/ 、Action API https://www.wikidata.org/w/api.php 、SPARQL https://query.wikidata.org/ |
| 利用規約・ライセンス | 構造化データ (main、Property、Lexeme、EntitySchema の名前空間) は CC0。それ以外の名前空間の文章は CC BY-SA 4.0 (https://www.wikidata.org/wiki/Wikidata:Licensing) |

## 概要

Wikidata は、事物ごとに ID (例: 通天閣は Q1148463) を持ち、性質ごとの値を並べた共同編集のデータベースである。地図に使うのは、座標 (P625)、Commons の画像 (P18)、多言語の名前と説明である。OSM の `wikidata=*` や Overture の `brand.wikidata` からも参照され、同じものを出どころをまたいで突き合わせる鍵になる。

## 収録範囲と詳しさ

| 項目 | 値 | 出典 |
|---|---|---|
| 名所の座標 | 2026-11-10 に大阪市の名所と施設 49 件を日本語の名前で引いたところ、40 件が座標つきの項目に当たった。残りの 9 件は、路線 (阪堺電気軌道、御堂筋線)、店 (551蓬莱、うさみ亭マツバヤ)、商店街、船着場、慰霊碑のほか、ラベルの表記が合わなかったもの (旧第四師団司令部庁舎) で、OSM の地物で補った | 実測 (SPARQL) |
| 画像 | P18 は Wikimedia Commons のファイル名を指す。座標つきの 40 件のうち 39 件に画像があった。作者とライセンスは Commons の API で別に引く。1 件は CC BY-SA 3.0 なのに作者が機械で読めず、使わなかった (geo-software-legal-check の attribution) | 実測 |
| 同名の取り違え | 日本語のラベルの完全一致でも、別のものに当たる。「造幣局」はロシアの造幣局の項目にも当たり、その画像が付いていた。「大阪水上バス」の項目の画像は船ではなく別の場所の写真だった。説明 (description) と、対象地域の範囲に座標が入るかで絞り、画像も目で確かめる | 実測 |

## 形式と取得方法

- 取得方法: 名前で探すなら Action API の `wbsearchentities`、ID から値を取るなら `wbgetentities`。多数の名前をまとめて引くなら SPARQL の `VALUES` で 1 回の問い合わせにすると、リクエスト数を減らせる。
- 回数の制限 (2026 年に導入、変更されうると明記): 識別できない匿名のアクセスは 1 分に 10 回、連絡先を含む User-Agent を付けた匿名のアクセスは 1 分に 200 回。同時接続は 3 以下。429 や 503 には `Retry-After` に従い、無ければ 5 秒以上か指数関数的に待つ (https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits)。
- User-Agent: 連絡先 (メールアドレスか URL) を含める。`curl` や `Python-urllib` のような汎用の値やブラウザの値を使わない (https://foundation.wikimedia.org/wiki/Policy:User-Agent_policy)。
- 実測 (2026-11-10): 連絡先の無い User-Agent で `wbsearchentities` を続けて呼ぶと、数件目から「You are making too many requests to the API.」が返った。SPARQL の窓口は障害の対応中に「1 req / min」に絞られていた。ビルドのたびに呼ばず、引いた結果を TSV などに固定して保存するのがよい。

## ライセンスと出典表示

- 構造化データは CC0 なので、出典表示の義務はない。出どころとして Wikidata と確かめた日を書くことを勧める。
- 画像 (P18) は Commons のファイルで、ファイルごとのライセンスに従う。Wikidata の CC0 は画像には及ばない。

## 地図プロダクトでの使いどころ

- 名所や施設の代表点を、ODbL の共有義務なしに持ちたいとき。
- 名所の写真を、作者とライセンスつきで添えたいとき (Commons を経由する)。
- OSM、Overture、自社のデータを、同じ ID で突き合わせたいとき。

## 向いていない場面

- 路線、店、商店街など、座標を持たない項目が多い種類。OSM の地物で補う。
- 網羅性が要る一覧 (ある地域の全施設など)。共同編集なので収録は偏る。

## 出典

- https://www.wikidata.org/wiki/Wikidata:Licensing
- https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits
- https://foundation.wikimedia.org/wiki/Policy:User-Agent_policy

## 未確認のこと

- 日本の名所全体での座標と画像の収録率。上の数字は大阪市の 49 件だけの実測で、選んだ名所に偏りがある。
