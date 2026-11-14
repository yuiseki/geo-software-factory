# tile.openstreetmap.jp (OpenStreetMap Foundation Japan)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | 一般社団法人オープンストリートマップ・ファウンデーション・ジャパン (OSMFJ)。英国の OpenStreetMap Foundation とは別の法人である (https://www.osmf.jp/) |
| 公式サイト | https://tile.openstreetmap.jp/ (サーバの情報は https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver に集約されている) |
| 料金ページ | なし (無料) |
| 利用規約・利用ポリシー | 未確認。本サービス専用の利用規約ページは見つからなかった。関連: https://openstreetmap.jp/node/29/ (openstreetmap.jp サイトのライセンスとプライバシーポリシー) |

## 概要

OSMFJ が日本の OSM コミュニティ向けに運用するタイルサーバである (https://www.osmf.jp/ 、https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver)。TileServer GL で構成され、OpenMapTiles スキーマの全球ベクトルタイルと、日本語ラベルのスタイル (osm-bright-ja、maptiler-basic-ja など) をサーバ側で描画したラスタタイルを配信する (https://tile.openstreetmap.jp/)。API キーや登録は要らない (2026-11-10 実測)。料金や利用条件を定めた文書は公開されていない。

## 地図データ

- データの出どころ (自社調査 / OSM / 他社からのライセンス): OpenStreetMap。全球データは OpenMapTiles スキーマ v3.16.0 (https://tile.openstreetmap.jp/data/planet.json)。これとは別に竹島と北方領土の補正用ベクトルタイル (takeshima、hoppo) を重ねており、Wiki では対応を進めている途中とされている (https://tile.openstreetmap.jp/ 、https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver)
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): OSM の日本国内データと OpenMapTiles スキーマの範囲に依存する。注記は `name:ja` などの多言語名を持ち、日本語スタイルが用意されている (https://tile.openstreetmap.jp/data/planet.json)。住所・番地の網羅度は未確認
- 全球の対応: あり。第 2 世代サーバは全球 (Planet) のベクトルタイルとラスタタイルを扱う。第 1 世代 (2012〜2020) は日本のラスタタイルが中心だった (https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver)
- 更新頻度: 週 1 回、全球データを入れ替える。日次更新はサーバのスペック上現実的でないとされている (https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver)。2026-11-10 に取得したタイルと planet.pmtiles の Last-Modified は 2026-11-06 だった (実測)

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | `https://tile.openstreetmap.jp/{z}/{x}/{y}.png` のほか、`/styles/{osm-bright-ja,osm-bright-en,maptiler-basic-ja,maptiler-basic-en,maptiler-toner-ja,maptiler-toner-en}/{z}/{x}/{y}.png`。ベクトルタイルをサーバ側で描画したもの (https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver) |
| ベクトルタイル (形式、スキーマ) | あり | MVT (pbf)、OpenMapTiles スキーマ v3.16.0、z0〜14。TileJSON は `https://tile.openstreetmap.jp/data/planet.json` (2026-11-10 実測)。全球 PMTiles `https://tile.openstreetmap.jp/static/planet.pmtiles` (約 85GB、実測) も置かれている (https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver) |
| スタイルの編集・カスタマイズ | あり (利用者側で) | style.json が公開されているので、取得して書き換え、自分でホストできる。例: `https://tile.openstreetmap.jp/styles/osm-bright-ja/style.json` (https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver) |
| 衛星・航空写真 | 未確認 | トップページのスタイルとデータの一覧には無い (https://tile.openstreetmap.jp/) |
| 地形・3D 建物 | 未確認 | OpenMapTiles スキーマの building レイヤーは含まれるが、3D 表示のスタイルや地形データは一覧に無い (https://tile.openstreetmap.jp/) |
| ジオコーディング / 逆ジオコーディング | なし | |
| ルート検索 | なし | |
| オフライン利用 | 未確認 | 可否を定めた文書が無い。planet.pmtiles や MBTiles のファイルは公開されている (https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): なし
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 使える。ベクトルは style.json と TileJSON を MapLibre GL JS などで読み込み、ラスタは XYZ を Leaflet などで読み込む。WMTS の定義 (`/styles/{id}/wmts.xml`) も提供されている (https://tile.openstreetmap.jp/)
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): 定めた文書は見つからなかった。応答は `access-control-allow-origin: *` を返す (2026-11-10 実測)
- API キー・アカウントの要否: 不要 (2026-11-10 実測)

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): 課金なし
- 無料枠: 全て無料。ただし量の保証を示した文書は無い
- 従量単価 (主な API ごとに、通貨と確かめた日つき): なし (2026-11-10 確認)
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式も書く。単位の換算に仮定を置いたら仮定も書く): 料金はいずれも 0 円。どの規模まで受け入れられるかは公表されていない。2015 年のメーリングリストでは OSMFJ 関係者がアクセスのレートリミットを入れていると述べている (https://lists.openstreetmap.org/pipermail/talk-ja/2015-May/008924.html)。現行の制限値は未確認
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): 契約なし。有償プランもない

## 利用規約上の制約

- 商用利用: 未確認。本サービスについて可否を定めた文書が見つからなかった
- アクセス量の上限・公正利用の条件: 未確認。2015 年時点ではレートリミットがあるとの発言がある (https://lists.openstreetmap.org/pipermail/talk-ja/2015-May/008924.html)。現在は Varnish のキャッシュの後ろに複数のバックエンドを並べた構成である (https://github.com/osmfj/tileserver-gl-site)
- キャッシュ・オフライン保存: 未確認。2015 年のメーリングリストでは、キャッシュサーバを介した利用は内部確認の結果差し支えないとの返信があったとされるが、第 1 世代サーバ当時の発言で正式な規約ではない (https://lists.openstreetmap.org/pipermail/talk-ja/2015-May/008925.html)
- 帰属表示の要件: Wiki ではラスタタイルを CC-BY とし、「©OpenStreetMap Contributors」の表記を求めている (https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver)。TileJSON の attribution は「© OpenMapTiles © OpenStreetMap contributors」(https://tile.openstreetmap.jp/data/planet.json)。なお openstreetmap.jp サイトのライセンスページは地図画像とタイルを CC BY-SA 2.0 としており、表記が一致しない (https://openstreetmap.jp/node/29/)
- 他社の地図との併用、データの持ち出しの制限: 定めた文書は見つからなかった。データ自体は OSM の ODbL に従う (https://www.openstreetmap.org/copyright)

## 安定性と運用

- SLA: なし。SLA を示す記述は見つからなかった (https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver)
- 運営の継続性 (運営主体、資金源): OSMFJ は 2010 年設立の一般社団法人で、正会員と賛助会員の会費、寄付、企業スポンサーで運営される。サーバ基盤はさくらインターネットなどの支援を受けている (https://www.osmf.jp/)。第 2 世代サーバ (2019〜) はさくらのクラウド上にある (https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver)。運用の設定は GitHub で公開されている (https://github.com/osmfj/tileserver-gl-site)
- 障害情報の公開先: 未確認。専用のステータスページは見つからなかった。問い合わせ窓口は info@osmf.jp と Google フォーム (https://www.osmf.jp/ 、https://openstreetmap.jp/)

## 向いている場面

- 日本語ラベルの OSM 地図を、API キーなしで手早く試作やデモ、コミュニティ活動に使いたい場合
- OpenMapTiles スキーマのベクトルタイルと日本語スタイルの組み合わせを評価したい場合や、style.json を出発点に自前のスタイルを作りたい場合

## 向いていない場面

- 商用サービスや大量アクセスが見込まれるサービスの基盤地図。利用条件、許容量、SLA のいずれも公表されていない
- 利用条件の文書化を求められる案件 (自治体や企業の調達など)
- 毎日の更新が必要な場合 (更新は週 1 回)

## プライバシーとテレメトリ (2026-11-14 確認)

- **アクセスログとテレメトリ**: ボランティア運営の HTTP タイルサーバーであるため、接続元の IP アドレスやユーザーエージェント等の一般的なアクセスログが記録されうるが、独自のクライアント SDK による端末識別子・位置テレメトリの収集は無い。アクセスログの保持期間・匿名化方針の公開文書は未確認。

## 出典

- https://tile.openstreetmap.jp/
- https://tile.openstreetmap.jp/data/planet.json
- https://tile.openstreetmap.jp/styles/osm-bright-ja/style.json
- https://wiki.openstreetmap.org/wiki/Japan/OSMFJ_Tileserver
- https://www.osmf.jp/
- https://openstreetmap.jp/
- https://openstreetmap.jp/node/29/
- https://github.com/osmfj/tileserver-gl-site
- https://lists.openstreetmap.org/pipermail/talk-ja/2015-May/008924.html
- https://lists.openstreetmap.org/pipermail/talk-ja/2015-May/008925.html
- https://www.openstreetmap.org/copyright
- 2026-11-10 に tile.openstreetmap.jp の各エンドポイントへ送った HEAD/GET の実測 (応答ヘッダ、TileJSON、style.json)

## 未確認のこと

- 利用規約、商用利用の可否、アクセス量の上限: 本サービス専用の文書が OSMFJ のサイト、openstreetmap.jp、OSM Wiki のいずれにも見つからなかった。osmf.jp の「Terms of Use」リンクは中身の無いアンカーだった
- オフライン保存とキャッシュの可否: 2015 年のメーリングリストの発言以外に根拠が無く、現行のサーバに当てはまるかは分からない
- ライセンス表記の食い違い (Wiki の CC-BY と openstreetmap.jp の CC BY-SA 2.0): どちらが本サーバに適用されるかを示す文書が無い
- 障害情報の公開先: ステータスページや告知先が見つからなかった
- 衛星写真、地形、3D 建物: トップページの一覧に無いことだけを確かめた
- 日本国内の住所・番地や POI の網羅度: OSM のデータ量に依存し、本調査では計測していない
