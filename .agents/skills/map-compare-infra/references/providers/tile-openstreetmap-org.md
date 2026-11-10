# tile.openstreetmap.org (OpenStreetMap Foundation)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | OpenStreetMap Foundation (OSMF)。運用は OSMF の Operations Working Group が担う |
| 公式サイト | https://www.openstreetmap.org/ |
| 料金ページ | なし (無料) |
| 利用規約・利用ポリシー | Tile Usage Policy: https://operations.osmfoundation.org/policies/tiles/ 、OSMF Terms of Use: https://osmfoundation.org/wiki/Terms_of_Use |

## 概要

openstreetmap.org のトップページに表示される「Standard」レイヤー (OpenStreetMap Carto スタイル) のラスタタイルを配信するサーバ群である。タイル URL は `https://tile.openstreetmap.org/{z}/{x}/{y}.png` で、API キーも登録も要らない (https://operations.osmfoundation.org/policies/tiles/)。ただし寄付とスポンサーで賄われる容量の限られた資源であり、OSM の編集者と閲覧者のためのものという位置づけで、Tile Usage Policy が利用者に多くの条件を課している (同上)。第三者のサービスの基盤として使うことは想定されておらず、ポリシー自体が代替手段 (他の配信事業者、自前ホスト) を案内している (同上)。

## 地図データ

- データの出どころ (自社調査 / OSM / 他社からのライセンス): OpenStreetMap のデータそのもの。ライセンスは ODbL (https://www.openstreetmap.org/copyright)
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): OSM の日本国内データの充実度に依存する。スタイルは OSM Carto で、注記は各オブジェクトの `name=*` の値をそのまま描くため、日本国内は日本語で表示される (https://wiki.openstreetmap.org/wiki/Standard_tile_layer)。住所・番地の網羅度は未確認
- 全球の対応: あり (全球のラスタタイル)
- 更新頻度: 未確認。2026-11-10 に取得したタイルの応答ヘッダは `cache-control: max-age=90119, stale-while-revalidate=604800` であり、CDN 上では 1 日程度キャッシュされる (実測)

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | PNG、256px。z19 までは取得でき z20 は 400 を返した (2026-11-10 実測)。HTTP は禁止で HTTPS のみ (https://operations.osmfoundation.org/policies/tiles/) |
| ベクトルタイル (形式、スキーマ) | なし (本サービスとしては) | 別ホストの vector.openstreetmap.org があり、別のポリシーが適用される (https://operations.osmfoundation.org/policies/tiles/)。本ファイルの対象外 |
| スタイルの編集・カスタマイズ | なし | 配信されるのは OSM Carto で描画済みの画像のみ |
| 衛星・航空写真 | なし | |
| 地形・3D 建物 | なし | |
| ジオコーディング / 逆ジオコーディング | なし (本サービスとしては) | OSMF は別サービス (Nominatim) を別ポリシーで運営しているが本ファイルの対象外 |
| ルート検索 | なし | |
| オフライン利用 | 不可 | 「Offline use is not permitted on tile.openstreetmap.org」。地域の一括保存や先読みは禁止 (https://operations.osmfoundation.org/policies/tiles/) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): なし。XYZ ラスタタイルを直接参照する
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 使える。XYZ ラスタタイルを扱えるライブラリなら表示できる。ブラウザは既定の設定のままでキャッシュの要件を満たすとポリシーに書かれている (https://operations.osmfoundation.org/policies/tiles/)
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): SDK の指定はない。ただしアプリや SDK は自分を識別できる固有で安定した User-Agent を送る必要があり、`okhttp`、`python-requests`、`curl` などの汎用の既定値は遮断される。Web では有効な Referer を送り、制限的な Referrer-Policy で消してはならない (https://operations.osmfoundation.org/policies/tiles/)
- API キー・アカウントの要否: 不要

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): 課金なし
- 無料枠: 全て無料。ただし量の保証はなく、サービスに負荷をかける利用は予告なく遮断されうる (https://operations.osmfoundation.org/policies/tiles/)
- 従量単価 (主な API ごとに、通貨と確かめた日つき): なし (2026-11-10 確認)
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式も書く。単位の換算に仮定を置いたら仮定も書く): 料金はいずれも 0 円。ただし数値の上限が公表されていない一方で「heavy or inappropriate use harms others」とされ遮断の対象になりうるため、月 100 万ロード以上を本サービスに載せられるかは料金ではなくポリシー上の許容で決まり、その許容量は公表されていない (https://operations.osmfoundation.org/policies/tiles/)
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): 契約なし。有償プランもない

## 利用規約上の制約

- 商用利用: ポリシーは商用利用を明示的に禁じていないが、「Commercial services, or those that seek donations, should be especially aware that access may be withdrawn at any point」と警告している (https://operations.osmfoundation.org/policies/tiles/)
- アクセス量の上限・公正利用の条件: 数値の上限は公表されていない。一括ダウンロード (表示中でないタイルの先回り取得、.zip や .mbtiles へのアーカイブ、z14 以上の広域走査、ヘッドレスボット) は禁止。違反や負荷を与える利用は予告なく遮断され、繰り返すとネットワーク単位の長期遮断もありうる (https://operations.osmfoundation.org/policies/tiles/)
- キャッシュ・オフライン保存: サーバの `Cache-Control`、`Expires`、`ETag` に従う。ヘッダを読めないキャッシュは各タイルを最低 7 日保持する。`Cache-Control: no-cache` などでキャッシュを迂回してはならない。キャッシュ用プロキシは推奨されず、使うなら連絡のつく User-Agent が必要。オフライン保存と先読みは禁止 (https://operations.osmfoundation.org/policies/tiles/)
- 帰属表示の要件: 「© OpenStreetMap contributors」などの OSM の帰属表示を地図上 (通常は右下) に明示する。UI の下やトグルの奥、画面外に隠してはならない (https://operations.osmfoundation.org/policies/tiles/ 、https://www.openstreetmap.org/copyright)
- 他社の地図との併用、データの持ち出しの制限: 他の地図との併用を禁じる記述はない。タイル画像の一括保存は前述のとおり禁止。データは ODbL で別途入手できる (https://www.openstreetmap.org/copyright)

## 安定性と運用

- SLA: なし。「best-effort」で「there is no SLA or guarantee」と明記 (https://operations.osmfoundation.org/policies/tiles/)
- 運営の継続性 (運営主体、資金源): 非営利の OSMF が運営し、サーバ群は寄付とスポンサーで賄われる (https://operations.osmfoundation.org/policies/tiles/)。タイルサーバは欧州、米国、台湾などの複数拠点にあり、各拠点のホスティング提供者が公開されている (https://hardware.openstreetmap.org/)。ポリシーは随時変更されうる (https://operations.osmfoundation.org/policies/tiles/)
- 障害情報の公開先: OpenStreetMap Server Status https://uptime.openstreetmap.org/ (https://operations.osmfoundation.org/)

## 向いている場面

- OSM の編集や閲覧に関連する小規模な Web ページ、個人や研究の試作で、OSM 標準の見た目のラスタ地図をすぐ出したい場合
- ブラウザから通常の対話的な閲覧に限って使い、帰属表示と Referer の要件を守れる場合

## 向いていない場面

- 観測 (2026-11-11): はてなブックマークで集めた地図サービス 60 件のうち 6 件 (個人や小さなチームのもので、Leaflet と組み合わせたものが多い) が、このタイルを本番の地図に直接使っていた。上の利用ポリシーは大量の利用や主たる供給元としての利用を想定しておらず、利用が増えたときに止められうる。試作から公開に進むときに、OpenFreeMap などへ移すかを決める

- 商用サービスや大量アクセスが見込まれるサービスの基盤地図。予告なく遮断されうるうえ SLA がない
- オフライン地図、地域の事前ダウンロード、タイルのアーカイブ作成
- 汎用 HTTP クライアントのままのネイティブアプリやサーバ側バッチ
- ベクトルタイルやスタイルの変更が必要な場合

## 出典

- https://operations.osmfoundation.org/policies/tiles/
- https://operations.osmfoundation.org/
- https://osmfoundation.org/wiki/Terms_of_Use
- https://www.openstreetmap.org/
- https://www.openstreetmap.org/copyright
- https://wiki.openstreetmap.org/wiki/Standard_tile_layer
- https://hardware.openstreetmap.org/
- https://uptime.openstreetmap.org/
- 2026-11-10 に `https://tile.openstreetmap.org/{z}/{x}/{y}.png` へ HEAD/GET を送った実測 (応答ヘッダ、最大ズーム)

## 未確認のこと

- 編集がタイルに反映されるまでの時間: 公式ページに明記された記述を見つけられなかった。応答ヘッダのキャッシュ期間だけを実測した
- 遮断の基準となる具体的なリクエスト数: ポリシーは数値を示していない
- 日本国内の住所・番地や POI の網羅度: OSM のデータ量に依存し、本調査では計測していない
- OSMF Terms of Use の本文: URL のみ記載し、タイルに固有の追加条件があるかは読んでいない
- CDN 事業者名: 応答ヘッダに CDN のキャッシュ痕跡 (`x-cache: HIT`、`x-served-by: cache-nrt-...`) はあるが、事業者名を公式ページで確認できなかった
