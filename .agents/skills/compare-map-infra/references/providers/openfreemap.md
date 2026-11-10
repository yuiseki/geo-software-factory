# OpenFreeMap

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | 個人プロジェクト。作者は Zsolt Ero (GitHub: hyperknot)。規約の準拠法はハンガリー法 (https://openfreemap.org/ 、https://openfreemap.org/tos/) |
| 公式サイト | https://openfreemap.org/ |
| 料金ページ | なし (無料。寄付は GitHub Sponsors: https://github.com/sponsors/hyperknot) |
| 利用規約・利用ポリシー | https://openfreemap.org/tos/ 、プライバシーポリシー https://openfreemap.org/privacy/ |

## 概要

OpenStreetMap のデータから作った全球ベクトルタイルとスタイルを無料で配信するサービスである。公開インスタンスは地図の表示回数やリクエスト数に上限を設けず、登録、ユーザー DB、API キー、Cookie のいずれも無い (https://openfreemap.org/)。本番の構成一式が MIT ライセンスで公開されており、自前ホストもできる (https://github.com/hyperknot/openfreemap)。検索、ルート検索、ラスタタイル、衛星写真、独自データのホスティングは意図的に提供しない (同上)。

## 地図データ

- データの出どころ (自社調査 / OSM / 他社からのライセンス): OpenStreetMap。Planetiler で OpenMapTiles スキーマのタイルを生成し、Natural Earth と Wikidata も使う (https://github.com/hyperknot/openfreemap)
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): OSM の日本国内データと OpenMapTiles スキーマの範囲に依存する。スキーマは改変していない (https://openfreemap.org/)。既定スタイル Liberty の注記は `name:latin` と `name:nonlatin` を並べる式で、日本国内ではローマ字と日本語が併記される (https://tiles.openfreemap.org/styles/liberty を 2026-11-10 に取得して確認)。住所・番地の網羅度は未確認
- 全球の対応: あり (全球、z0〜14。https://tiles.openfreemap.org/planet を 2026-11-10 に取得して確認)
- 更新頻度: 週 1 回、全球のタイルを自動で再生成して差し替える (https://github.com/hyperknot/openfreemap)。2026-11-10 時点の最新版は `20261101_080013_pt` だった (実測)

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | なし | 「raster tile hosting」は提供しないと明記 (https://github.com/hyperknot/openfreemap) |
| ベクトルタイル (形式、スキーマ) | あり | MVT (pbf)、OpenMapTiles スキーマ (改変なし)、z0〜14。TileJSON は `https://tiles.openfreemap.org/planet` (https://openfreemap.org/ 、https://github.com/hyperknot/openfreemap) |
| スタイルの編集・カスタマイズ | あり | 既定スタイルは Positron、Bright、Liberty、Dark、Fiord、3D (https://openfreemap.org/)。Maputnik で編集できるが、編集したスタイル JSON は利用者が自分でホストする (https://openfreemap.org/quick_start/)。スタイルは https://github.com/hyperknot/openfreemap-styles で公開 |
| 衛星・航空写真 | なし | 提供しないと明記 (https://github.com/hyperknot/openfreemap) |
| 地形・3D 建物 | 一部 | 「3D」スタイルがある (https://openfreemap.org/)。標高の照会は提供しない (https://github.com/hyperknot/openfreemap)。Liberty は Natural Earth の陰影起伏ラスタ (`ne2_shaded`) を重ねている (2026-11-10 実測)。地形 (DEM) タイルは提供しない旨の記載はないが、配信もしていない (未確認) |
| ジオコーディング / 逆ジオコーディング | なし | 提供しないと明記 (https://github.com/hyperknot/openfreemap) |
| ルート検索 | なし | 提供しないと明記 (https://github.com/hyperknot/openfreemap) |
| オフライン利用 | 条件つきで可 | アプリ内のオフラインダウンロードは 1 回あたり 3,000 タイルまたは 50MB まで、並列 4 リクエストまで、アプリを識別できる User-Agent が必要。超える場合は info@openfreemap.org に連絡する (https://openfreemap.org/tos/)。全球データは毎週 Btrfs、MBTiles、PMTiles で配布される (https://github.com/hyperknot/openfreemap) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): なし。MapLibre の利用を前提とした案内になっている (https://openfreemap.org/quick_start/)
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 使える。MapLibre GL JS、Leaflet (MapLibre GL Leaflet 経由)、OpenLayers (ol-mapbox-style 経由)、モバイルは MapLibre Native が案内されている (https://openfreemap.org/quick_start/)
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): なし。Mapbox GL JS からは MapLibre GL JS への切り替えを勧めている (https://openfreemap.org/quick_start/)
- API キー・アカウントの要否: 不要 (https://openfreemap.org/)

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): 課金なし
- 無料枠: 全て無料。地図の表示回数とリクエスト数に上限はないとされる (https://openfreemap.org/)
- 従量単価 (主な API ごとに、通貨と確かめた日つき): なし (2026-11-10 確認)。将来 Pro プランを導入する可能性に触れているが、2026-11-10 時点では存在しない (https://openfreemap.org/)
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式も書く。単位の換算に仮定を置いたら仮定も書く): 料金はいずれも 0 円 (上限なしの公表に基づく。https://openfreemap.org/)。自前ホストの場合、作者は月 4.5 ユーロの Contabo Storage VPS を推奨例に挙げている (2026-11-10 確認、https://github.com/hyperknot/openfreemap/blob/main/docs/self_hosting.md)。ただし 1 台で 1,000 万ロードの転送量をさばけるかは未確認
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): 契約なし。寄付は任意で、月額の継続寄付を求めている (https://openfreemap.org/)

## 利用規約上の制約

- 商用利用: 可。公式サイトが商用利用を認めている (https://openfreemap.org/)。規約自体には商用利用の条項は無く、組織として使う場合は組織を拘束する権限を持つ者が同意する必要がある (https://openfreemap.org/tos/)
- アクセス量の上限・公正利用の条件: 表示とリクエストに上限は無い (https://openfreemap.org/)。規約はサービスの妨害と、オフラインダウンロードを除く自動的なデータ収集を禁じている (https://openfreemap.org/tos/)
- キャッシュ・オフライン保存: オフラインダウンロードは前述の上限内で可。それ以外のキャッシュについて規約に記述は無い (https://openfreemap.org/tos/)。大量に必要なら毎週配布される全球ファイルを使う手がある (https://github.com/hyperknot/openfreemap)
- 帰属表示の要件: 必要。MapLibre では自動で表示される。他のクライアントや印刷物、動画では OpenMapTiles と OpenStreetMap のクレジットを入れる。OpenFreeMap 自体の表記は任意 (https://openfreemap.org/)。TileJSON の attribution は「OpenFreeMap © OpenMapTiles Data from OpenStreetMap」(2026-11-10 実測)
- 他社の地図との併用、データの持ち出しの制限: 併用を禁じる記述は無い。データは OSM の ODbL、スタイルのデザインは CC BY 4.0 など各派生元のライセンスに従う (https://github.com/hyperknot/openfreemap/blob/main/LICENSE.md)

## 安定性と運用

- SLA: なし。「I don't offer SLA guarantees or personalized support」(https://openfreemap.org/)。規約上も無保証で、予告なく終了しうる (https://openfreemap.org/tos/)
- 運営の継続性 (運営主体、資金源): 作者個人が運営し、公開インスタンスの費用は寄付 (GitHub Sponsors) で賄う方針である (https://openfreemap.org/)。構成はクラウドを使わない専用サーバで、2026-11-10 時点の README では生成用 1 台と配信用 2 台 (ラウンドロビン DNS) である (https://github.com/hyperknot/openfreemap)。MapHub の本番ベースマップとして 2024-06 から使われている (同上)。規約は CDN として Cloudflare を使うと記載しており (https://openfreemap.org/tos/)、2026-11-10 の実測でも tiles.openfreemap.org の応答は `server: cloudflare` だった。README の「.org は Cloudflare を通さない」という記述とは食い違う。全球ファイルの配布 (btrfs.openfreemap.com) は Cloudflare R2 (https://github.com/hyperknot/openfreemap)
- 障害情報の公開先: 専用のステータスページは見つからなかった。変更は可能な場合 X と Bluesky で告知するとされる (https://openfreemap.org/tos/)。アカウントは https://x.com/OpenFreeMapOrg 、https://bsky.app/profile/hyperknot.com

## 向いている場面

- 予算をかけずに OpenMapTiles スキーマのベクトル地図を MapLibre で出したい Web サイトやアプリ。商用でも使える
- 公開インスタンスで試し、規模や可用性の要求が上がったら同じ構成で自前ホストに移る計画を立てたい場合。週次の全球ファイルと配信用スクリプトが公開されている
- MapLibre 系の既存スタイル (OSM Bright、Positron、Liberty) を出発点にスタイルを作りたい場合

## 向いていない場面

- SLA やサポート窓口、契約書が必要な案件
- ラスタタイルしか扱えない環境、衛星写真、ジオコーディング、ルート検索が必要な場合
- 日本語のみの注記が必要で、スタイルを自前で直してホストする手間をかけられない場合 (既定の Liberty はローマ字併記)
- 日次以上の頻度でのデータ更新が必要な場合 (更新は週 1 回)

## 出典

- https://openfreemap.org/
- https://openfreemap.org/quick_start/
- https://openfreemap.org/tos/
- https://openfreemap.org/privacy/
- https://github.com/hyperknot/openfreemap
- https://github.com/hyperknot/openfreemap/blob/main/docs/self_hosting.md
- https://github.com/hyperknot/openfreemap/blob/main/LICENSE.md
- https://github.com/hyperknot/openfreemap-styles
- https://github.com/sponsors/hyperknot
- https://tiles.openfreemap.org/planet
- https://tiles.openfreemap.org/styles/liberty
- https://x.com/OpenFreeMapOrg
- https://bsky.app/profile/hyperknot.com
- 2026-11-10 に tiles.openfreemap.org の TileJSON、スタイル、タイルへ送った HEAD/GET の実測

## 未確認のこと

- 公開インスタンスの運用費、寄付の総額、利用量の統計: 公式サイトと README に数値が無い
- 寄付が不足した場合の扱い: 規約は予告なく終了しうるとするだけで、具体的な方針は書かれていない
- 実際のレート制限の有無: 「上限なし」の公表のみで、遮断の基準は示されていない
- 自前ホスト 1 台で処理できるアクセス量: README にはループバックで 30Gbit のベンチマークがあるが、実運用の目安は示されていない
- 地形 (DEM) タイルと 3D スタイルの中身: 3D スタイルの存在のみ確認し、内容は確かめていない
- 日本国内の住所・番地や POI の網羅度: OSM のデータ量に依存し、本調査では計測していない
- tiles.openfreemap.org が Cloudflare を経由する範囲: README と実測が食い違っており、どちらが現行の方針かを示す文書が無い
