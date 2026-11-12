# MIERUNE (無料の地図タイルと、MIERUNE地図タイル)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 運営主体 | 株式会社MIERUNE (札幌市) (https://prtimes.jp/main/html/rd/p/000000014.000101350.html) |
| 公式サイト | 無料のタイル: https://github.com/MIERUNE/tiles (見本は https://mierune.github.io/tiles/)。有償の製品: https://maps.mierune.co.jp/ |
| 料金ページ | 無料のタイルには無い。有償の製品は https://maps.mierune.co.jp/ に価格がある |
| 利用規約・利用ポリシー | 無料のタイル: リポジトリの README の「利用条件」3 項目だけ (https://github.com/MIERUNE/tiles)。有償の製品: https://maps.mierune.co.jp/terms (2026-06-04 制定) |

## 概要

MIERUNE は 2 種類を出している。1 つは tile.mierune.co.jp で配る無料のラスタタイルで、「MIERUNE」(カラー) と「MIERUNE MONO」(モノクロ) の 2 つがある (https://github.com/MIERUNE/tiles)。もう 1 つは 2026-06-04 に販売を始めた有償の「MIERUNE地図タイル」で、データ、スタイル、アセットを一式で買い、自分のサーバーで配信する製品である (https://prtimes.jp/main/html/rd/p/000000014.000101350.html 、https://maps.mierune.co.jp/)。2026-11-11 の観察では、名字マップが tile.mierune.co.jp の mierune_mono を背景地図に使っていた。

## 地図データ

- データの出どころ (自社調査 / OSM / 公的データ / 他社からのライセンス): 無料のタイルは帰属表示が「MIERUNE Inc. © OpenMapTiles © OpenStreetMap contributors」で (https://github.com/MIERUNE/tiles)、OSM のデータを OpenMapTiles のスキーマで描いたものと読める (推測。生成の手順は公表されていない)。有償の製品は OSM を主な基盤とし、OpenMapTiles、Mapterhorn、地理院ベクトルタイル、国土数値情報 (鉄道、行政区域) を帰属表示に挙げる (https://maps.mierune.co.jp/ 、https://maps.mierune.co.jp/terms 別表1)
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): 無料のタイルは OSM の国内データに依存する (推測)。有償の製品は道路網、施設、都道府県と市区町村の境界、鉄道を含むとし、領土の表記を日本国政府の見解に合わせるとしている (https://prtimes.jp/main/html/rd/p/000000014.000101350.html 、https://maps.mierune.co.jp/)。住所・番地の網羅度は未確認
- 全球の対応: 無料のタイルは z0 から配信されている (2026-11-11 に `mierune_mono/0/0/0.png` が 200 を返した、実測)。有償の製品は全球版と日本版 (日本全土と周辺の海域) から選ぶ (https://maps.mierune.co.jp/)
- 更新頻度: 無料のタイルは公表されていない (未確認)。有償の製品は MIERUNE のデータの流れで月次に更新し、更新の提供は別契約のオプション (https://maps.mierune.co.jp/ 、https://maps.mierune.co.jp/terms 第3条)

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり (無料) | `https://tile.mierune.co.jp/mierune/{z}/{x}/{y}@2x.webp` と `https://tile.mierune.co.jp/mierune_mono/{z}/{x}/{y}@2x.webp` が 512px、`@2x` を外すと 256px。README の見本は maxzoom 18 (https://github.com/MIERUNE/tiles)。README は 2026-11-05 に PNG から WebP の URL へ書き換えられたが、2026-11-11 には `.png` の URL も 200 と `image/png` を返した (実測)。応答は `server: cloudflare`、`access-control-allow-origin: *`、`cache-control: max-age=86400` (実測)。有償の製品のラスタ形式は追加料金 (https://maps.mierune.co.jp/) |
| ベクトルタイル (形式、スキーマ) | 有償の製品のみ | 主な形式は PMTiles。MBTiles と XYZ は追加料金 (https://maps.mierune.co.jp/)。スキーマは未確認 |
| スタイルの編集・カスタマイズ | 有償の製品のみ | Streets、Gray、Dark の 3 つを MapLibre Style Spec の JSON で提供する (https://maps.mierune.co.jp/)。自分で使う分には編集できるが、編集したスタイルを第三者に渡すには事前の書面の許可が要る (https://maps.mierune.co.jp/terms 第2条4、5) |
| 衛星・航空写真 | なし | どちらにも記載が無い |
| 地形・3D 建物 | 未確認 | 有償の製品は Mapterhorn を帰属表示に挙げる (https://maps.mierune.co.jp/terms 別表1) ので標高を使っていると読める (推測) |
| ジオコーディング / 逆ジオコーディング | なし | 記載が無い |
| ルート検索 | なし | 記載が無い |
| オフライン利用 | 有償の製品は可 | 自分のサーバー (オンプレミス、AWS、GCP、Azure など) に置き、閉域網とオフラインで動かせる (https://prtimes.jp/main/html/rd/p/000000014.000101350.html)。無料のタイルのキャッシュと保存は、利用条件に記述が無い (未確認) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): なし
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 無料のタイルは XYZ のラスタなので、README が MapLibre GL JS、Leaflet、OpenLayers、deck.gl、CesiumJS、iTowns の見本を載せている (https://github.com/MIERUNE/tiles)。有償の製品のスタイルは MapLibre Style Spec (https://maps.mierune.co.jp/)
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): どちらにも記載が無い
- API キー・アカウントの要否: 無料のタイルは不要 (README の URL にキーが無く、2026-11-11 にキーなしで 200 が返った、実測)。有償の製品は契約が要る

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): 無料のタイルは課金なし。有償の製品は 1 システムあたりの一括払いで、表示回数やリクエスト数では課金しない (https://maps.mierune.co.jp/)
- 無料枠: 無料のタイルは「無料で利用できます」とあり、量の上限は書かれていない (https://github.com/MIERUNE/tiles)
- 従量単価 (主な API ごとに、通貨と確かめた日つき): 従量の単価は無い。有償の製品は税別で、全球版の基本価格が 60 万円、データ更新のオプションが 30 万円、日本版の基本価格が 30 万円、データ更新のオプションが 20 万円 (1 システム、2026-11-11、https://maps.mierune.co.jp/)。基本価格は一度の支払いで使用期限が無く、データ更新は 12 か月のオプション (https://prtimes.jp/main/html/rd/p/000000014.000101350.html)
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式も書く。単位の換算に仮定を置いたら仮定も書く): 無料のタイルはいずれも 0 円。有償の製品は表示回数によらず、初年度は日本版で 30 万円 (更新ありなら 50 万円)、全球版で 60 万円 (更新ありなら 90 万円)。どちらも税別で、自分のサーバーの配信費用が別にかかる (計算は上の価格から。配信費用は geo-software-arch の self-hosting で見積もる)
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): 有償の製品は契約で、規約は契約期間を開始月から 1 年、中途解約なし、満了の 2 か月前までに書面で申し出なければ 1 年ずつ自動で更新するとしている (https://maps.mierune.co.jp/terms 第4条)。一方で製品のページは基本価格を一度の支払いとし、ダウンロードしたデータは期限なく使えて、契約が終わると新しいダウンロードが止まるとする (https://maps.mierune.co.jp/terms 第13条4)。1 年ごとに更新される契約が基本価格とデータ更新のどちらを指すかは、ページから読み切れない (未確認)

## 利用規約上の制約

- 商用利用: 無料のタイルの利用条件は商用利用に触れていない (https://github.com/MIERUNE/tiles、未確認)。有償の製品の規約は「商用」という語を使わず、公開・非公開を問わず 1 システムで使え、Web、印刷物、出版物に追加料金なく組み込めるとする (https://maps.mierune.co.jp/terms 第2条1〜3)
- アクセス量の上限・公正利用の条件: 無料のタイルは上限の記載が無く、予告なく仕様を変えたりサーバーを止めたりすることがあるとする (https://github.com/MIERUNE/tiles)
- キャッシュ・オフライン保存: 無料のタイルは記載が無い (未確認)。有償の製品は自分の環境に置く前提
- 帰属表示の要件: 無料のタイルは「MIERUNE Inc. © OpenMapTiles © OpenStreetMap contributors」を表示する (https://github.com/MIERUNE/tiles)。有償の製品は「© OpenStreetMap contributors」「© OpenMapTiles」「© Mapterhorn」「出典：国土地理院ウェブサイト」(加工したら「を加工して作成」を足す)、「出典：国土数値情報（該当データ名）（国土交通省）」を表示する (https://maps.mierune.co.jp/terms 第7条2、別表1)
- 他社の地図との併用、データの持ち出しの制限: 有償の製品を不特定の第三者向けの地図配信の仕組みとして提供するには MIERUNE の明示の許可が要り、製品そのものを商品やサービスとして提供することは許されない。第2条の範囲を超える複製、改変、再配布は禁じられる (https://maps.mierune.co.jp/terms 第2条の2、第8条2)。無料のタイルは記載が無い
- データのライセンス: OSM 由来の部分は ODbL で、規約の別表1も OSM を ODbL として挙げる。製品全体を ODbL で許諾するとは書かれていない (https://maps.mierune.co.jp/terms)。ODbL の帰属表示以外の義務 (派生データベースの扱い) をどう満たすかは規約に書かれていない (未確認)

## 安定性と運用

- SLA: 無料のタイルは無い。予告なく仕様の変更やサーバーの停止がありうる (https://github.com/MIERUNE/tiles)。有償の製品は自分で配信するので、稼働は自分の運用で決まる
- 運営の継続性 (運営主体、資金源): 民間企業 (株式会社MIERUNE) が運営する。無料のタイルの資金源と継続の方針は公表されていない (未確認)
- 障害情報の公開先: 見当たらない (未確認)

## 向いている場面

- 国内向けの Web 地図で、主題データを目立たせる淡い背景 (MIERUNE MONO) を、キーなしで試作に使いたいとき
- 閉域網やオフラインで、日本の領土の表記に合わせたベクトルの背景地図を、表示回数の課金なしで持ちたいとき (有償の製品)
- MapLibre Style Spec のスタイルを自分の環境で配信し、印刷物や出版物にも追加料金なく使いたいとき (有償の製品)

## 向いていない場面

- SLA や窓口が要る本番の地図を、無料のタイルだけで賄うとき (停止がありうると明記されている)
- 無料のタイルでベクトルタイルや配色の作り込みが要るとき (ラスタのみ)
- 複数のサービスを 1 契約でまかないたいとき、地図を第三者に配信するサービスを作るとき (有償の製品は 1 システムごとで、第三者向けの配信には許可が要る)
- 衛星写真、ジオコーディング、ルート検索が要るとき

## 執筆上の注意

- 無料のタイルと有償の製品は規約が別で、有償の製品の規約が無料のタイルにかかるかは書かれていない。両者の条件を混ぜて書かない。

## 出典

- https://github.com/MIERUNE/tiles
- https://mierune.github.io/tiles/
- https://mierune.github.io/tiles/mono.html
- https://maps.mierune.co.jp/
- https://maps.mierune.co.jp/terms
- https://prtimes.jp/main/html/rd/p/000000014.000101350.html
- 2026-11-11 に tile.mierune.co.jp の `mierune` と `mierune_mono` へ送った HEAD の実測 (PNG と WebP、256px と 512px)

## 未確認のこと

- 無料のタイルで商用利用ができるか、キャッシュやオフライン保存ができるか: 利用条件が 3 項目だけで、触れていないため
- 無料のタイルのデータの更新頻度と生成の手順: 公表されていないため
- 無料のタイルの PNG の URL をいつまで配るか: README は 2026-11-05 に WebP へ書き換えられ、PNG についての記述が消えたため
- 有償の製品の規約 (第4条の 1 年の自動更新) と、製品ページの「一度の支払いで使用期限なし」との関係: どちらの文書も相手に触れていないため
- 有償の製品のベクトルタイルのスキーマ (OpenMapTiles か独自か) と、住所・番地や建物の網羅度: 製品ページで確かめられなかったため
- 2020 年に MapTiler と組んで出した MapTiler.jp との関係: 報道 (https://internet.watch.impress.co.jp/docs/column/chizu3/1232026.html) の検索結果の要約でしか見ておらず、本文を読んでいない。また、2026-11-11 に www.maptiler.jp は https://www.maptiler.com/ja/ へ転送された (実測)
