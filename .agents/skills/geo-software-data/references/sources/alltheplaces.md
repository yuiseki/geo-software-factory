# AllThePlaces

対象: AllThePlaces が各社の公式の店舗検索から集めたチェーン店の店舗データ

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 提供者 | AllThePlaces プロジェクト (有志の OSS。https://github.com/alltheplaces/alltheplaces) |
| 配布ページ | https://www.alltheplaces.xyz/ 、最新の収集の情報: https://data.alltheplaces.xyz/runs/latest.json |
| 利用規約・ライセンス | 収集したデータは CC0 1.0 (権利放棄)。収集プログラムは MIT (README の License の節) |

## 概要

AllThePlaces は、チェーン店や施設の運営者が自分のサイトで公開している店舗検索や店舗一覧から、店舗の位置と属性を集めるプログラム (spider) の集まりである。ブランドごとに 1 つの spider があり、毎週まとめて動かした結果をブランドごとの GeoJSON で配る。タグは OSM の書き方 (`shop=convenience`、`brand:wikidata` など) に合わせてある。Overture Maps の places の出所の 1 つでもある ([overture-maps](overture-maps.md))。

## 収録範囲と詳しさ

| 項目 | 値 | 出典 |
|---|---|---|
| 地域 | 全世界。spider があるブランドだけ。国ごとに別の spider のことがある (セブンイレブンは `seven_eleven_jp`、`seven_eleven_tw` など) | https://github.com/alltheplaces/alltheplaces/tree/master/locations/spiders |
| 詳しさ | 公式サイトの店舗情報をそのまま写すので、店名、支店名、住所、電話、営業時間、サービス (ATM、酒類など) が付くことが多い | `seven_eleven_jp` の出力 (2026-11-05 収集) |
| 時点と更新頻度 | おおむね毎週の収集。2026-10-31 開始の収集が 2026-11-07 に終わった。ブランドごとの収集時刻は出力の `spider:collection_time` にある | https://data.alltheplaces.xyz/runs/latest.json |
| 網羅性 | spider ごとに違う。サイトの API の上限で打ち切られることがある。`seven_eleven_jp` は全国でちょうど 6,000 件 (エラー 2 件) で、住所は北海道と東北・北関東に偏り、東京都は 0 件だった。公式の全国の店舗数は 21,956 店 (2026 年 10 月末) | 収集の統計 `stats/_results.json`、https://www.sej.co.jp/company/tenpo.html |

## 形式と取得方法

- 配布形式: ブランドごとの GeoJSON。全部まとめた zip、GeoParquet、PMTiles もある (`latest.json` の `output_url`、`parquet_url`、`pmtiles_url`)。
- 取得方法: `https://alltheplaces-data.openaddresses.io/runs/<run_id>/output/<spider>.geojson` (例: `runs/2026-10-31-13-32-34/output/seven_eleven_jp.geojson`)。`run_id` は `latest.json` で分かる。
- 座標参照系: GeoJSON なので WGS84 の経度・緯度。

## ライセンスと出典表示

- ライセンス: データは CC0 1.0。出典表示の義務はないが、出どころとして AllThePlaces と収集日を書くことを勧める。
- 元のデータとの関係: 元は各社のサイトの店舗情報である。各社のサイトの利用規約と、CC0 で配られたデータの関係は未確認。

## 向いている場面

- チェーン店の店舗を、公式サイトに近い属性つきで、ライセンスの負担なしに集めたいとき。ただし件数を公式の店舗数と突き合わせてから使う。
- OSM や Overture の店舗データの取りこぼしを確かめる比較の相手として。

## 向いていない場面

- 打ち切られている spider で、地域ごとの数を出すとき。件数がきりのいい数 (6,000 など) で止まっていたら、打ち切りを疑う。
- spider のないブランド、個人店。

## 出典

- https://github.com/alltheplaces/alltheplaces (README の License の節)
- https://www.alltheplaces.xyz/
- https://data.alltheplaces.xyz/runs/latest.json
- https://alltheplaces-data.openaddresses.io/runs/2026-10-31-13-32-34/stats/_results.json
- https://www.sej.co.jp/company/tenpo.html (セブン-イレブンの都道府県別店舗数。数字は地図の画像の中にある)

## 未確認のこと

- spider ごとの網羅率。プロジェクトとしての公表はない。
- 各社のサイトの利用規約と、CC0 での配布の関係。
