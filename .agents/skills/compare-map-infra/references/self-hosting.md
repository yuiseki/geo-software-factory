# 自前でのタイル配信 (self-hosting)

> 後で書く。各項目に確かめた日、ツールの版、出典を添える。確かめていない項目は「未確認」と書く。

確かめた日: 未確認

## いつ候補に入れるか

後で書く。候補:

- 表示回数が多く、商用サービスの従量課金が重い
- 外部サービスへの通信が許されない (閉域、オフライン、データ主権)
- 地図の中身 (表示する地物、スタイル、更新タイミング) を自分で決めたい
- 自前のデータをベースマップに混ぜたい

## 構成の型

後で書く。候補:

- 静的ファイル 1 本 (PMTiles) をオブジェクトストレージ + CDN で配信する
- MBTiles/PostGIS からタイルサーバーで配信する (Martin, tileserver-gl など)
- 事前生成した z/x/y のタイル群を静的に置く

## タイルの生成

後で書く。候補: Planetiler, tilemaker, OpenMapTiles, Protomaps basemaps。入力 (OSM の planet/抽出、自前データ)、出力スキーマ (OpenMapTiles, Shortbread, Protomaps)、必要な計算資源と時間。

## 配信

後で書く。候補: PMTiles + S3/R2 + CDN、Martin、tileserver-gl、ラスタ化が要る場合。

## タイル形式

後で書く: MVT と、その後継として MapLibre が策定中の MLT (MapLibre Tile, https://github.com/maplibre/maplibre-tile-spec)。対応するライブラリと生成ツールの状況。

## 地形タイル

後で書く: 標高タイルを自前で持つか、公開の地形タイルを使うか。候補: Mapterhorn (https://github.com/mapterhorn/mapterhorn, BSD-3-Clause)。

## スタイル・フォント・スプライト

後で書く: タイル以外に自前で用意するもの。

## タイル以外を自前で持つ: ジオコーディング

後で書く: 住所・地名検索を商用 API に頼らず持つ場合。候補: Pelias (https://github.com/pelias/pelias, MIT), Photon (https://github.com/komoot/photon, Apache-2.0)。日本の住所をどこまで引けるかは未確認。

## 費用の見積もり

後で書く: 生成の計算資源、保存容量、転送量。商用サービスとの損益分岐の求め方。

## 運用の負担

後で書く: データ更新の頻度と手順、監視、帰属表示 (ODbL)、障害時の責任。

## 向いている場面 / 向いていない場面

後で書く。
