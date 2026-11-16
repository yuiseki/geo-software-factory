# VersaTiles

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-16 |
| 運営主体 | VersaTiles プロジェクト (GitHub 組織 versatiles-org)。資金は GitHub Sponsors と Open Collective の寄付で、有償の運営会社は見当たらない。組織の consortium リポジトリは「コンソーシアムの設立」の呼びかけを置く (https://github.com/versatiles-org 、https://docs.versatiles.org/guides/use_tiles_versatiles_org) |
| 公式サイト | https://versatiles.org/ 、ドキュメント https://docs.versatiles.org/ |
| 料金ページ | なし。商用のホスティングは提供されていない (下の「料金」) |
| 利用規約・利用ポリシー | 利用規約の文書は見当たらない。公開デモサーバーの条件は https://docs.versatiles.org/guides/use_tiles_versatiles_org の「What to expect」に書かれている |

## 概要

OpenStreetMap から作った全球のベクトルタイルを、生成、変換、配信、描画まで一式のオープンソースで出す仕組みである。ドキュメントは「商用の供給元に代わる、パイプライン全体を自分で握れるセルフホスト」と位置づける (https://docs.versatiles.org/)。このスキル集では、セルフホスト前提の選択肢として扱う。

- 生成: Planetiler の Shortbread プロファイル (ベータ)。Docker イメージ `versatiles/versatiles-planetiler` で OSM の pbf から作る
- 保管の形式: `.versatiles` コンテナ。HTTP の byte range で読める単一ファイルで、PMTiles、COMTiles と同じ考え方。`.pmtiles`、`.mbtiles`、`.tar`、ディレクトリとの相互変換ができる
- 配信: `versatiles serve` (Rust 製の単一バイナリ。MIT)。TLS とキャッシュは含まれないので、nginx か CDN を前に置く
- 描画側の部品 (スタイル、フォント、MapLibre GL JS の一式): [versatiles-frontend](../../../geo-software-library/references/frameworks/versatiles-frontend.md) に分けて書いた

公開デモサーバー tiles.versatiles.org は無料で誰でも使えるが、無保証である。確かめられた範囲では、公式が「安定した地図が要るなら自前で立てる」と明言している (同上)。

## 地図データ

- データの出どころ: OpenStreetMap (ODbL)。Shortbread スキーマ (CC0) で構造化している。標高は Mapterhorn、陰影は Mapzen Jörð、土地被覆は ESA WorldCover、水深は GEBCO (OpenDEM 経由)、衛星と航空写真は各国の公開データ (https://docs.versatiles.org/basics/tilesets)
- 国内の詳しさ: OSM の日本国内データと、Shortbread スキーマの範囲に依存する。スキーマが持つ層が OpenMapTiles より少ないかどうかは未確認
- 全球の対応: あり。OSM のタイルは全球で z0〜14、約 62GB (同上)
- 更新頻度: 配布元は新しい版と日付つきの版 (例: `osm.20260608.versatiles`) を出し、版ごとに RSS がある。更新の間隔そのものは未確認 (同上)

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | 衛星 (WebP、512px、全球で z12 まで、欧州の国は国別にさらに深い)。標高は Terrarium 形式の WebP、z0〜12。衛星はアルファ、標高はベータ (https://docs.versatiles.org/basics/tilesets) |
| ベクトルタイル (形式、スキーマ) | あり | MVT。Shortbread スキーマ。`versatiles convert --tile-format mlt` で MLT にも変換できる。陰影、土地被覆、水深のベクトルタイルもある (アルファからベータ) |
| スタイルの編集・カスタマイズ | あり | `@versatiles/style` が 5 つのテーマ (colorful、natural、muted、gray、toner) と各ダーク版、衛星のスタイルを作る。ブラウザの編集 UI もある (frontend の reference を参照) |
| 衛星・航空写真 | 一部 | 上のとおり。z12 を超える高解像度は欧州の一部の国だけで、日本は未確認 |
| 地形・3D 建物 | 一部 | 標高タイルを `raster-dem` として使い、地形と陰影ができる。建物の 3D は未確認 |
| ジオコーディング / 逆ジオコーディング | 公開デモのみ | photon-stack リポジトリが geocode.versatiles.org の構成を公開している (Photon の Docker)。製品としての案内は未確認 |
| ルート検索 | なし | 該当する部品が見当たらない |
| オフライン利用 | あり | 地域ごとの切り出し (数百 MB) を `.versatiles`、`.pmtiles`、`.mbtiles` で配れる。ダウンロードサイトが bbox つきの変換コマンドを作る |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): 専用の SDK は無い。MapLibre GL JS、MapLibre Native (iOS、Android) のスタイル URL にそのまま渡せる (https://docs.versatiles.org/guides/what_about_mobile)。Svelte のコンポーネント `node-versatiles-svelte` と、MapLibre のスタイル編集プラグインがある。QGIS からも使える
- 公式以外のライブラリから使えるか: 使える。標準の `z/x/y` と TileJSON を話すので、Leaflet や OpenLayers でも読める (形式別の動作は未確認)
- 組み合わせの制約: なし。ただし配布元のスタイルとタイルのスキーマの版は合わせる (スタイル側の v8 で土地被覆の扱いが変わった記載がある)
- API キー・アカウントの要否: 不要

## 料金

- 課金単位: なし。商用ホスティングは無い
- 無料枠: 公開デモは無料で、地図の表示回数の上限は書かれていない。ただし IP ごとの流量制限があり、超えると 429 を返す (上限値は nginx の設定が公開)。高い流量なら前に CDN を置くよう求めている
- 自前ホストの費用: ソフトウェアは無料。実費はサーバーとディスクで、全球の OSM だけで約 62GB、衛星まで含めると 1.6TB 規模になる。国や地域の切り出しなら数百 MB から。月 10 万 / 100 万 / 1,000 万地図ロードの概算は、本リポジトリでは未計算 (geo-software-poc-measure で測る)
- 契約形態: 契約なし

## 利用規約上の制約

- 商用利用: ソフトウェアは MIT で可。タイルのデータは OSM の ODbL なので、帰属表示と、派生のデータベースを公開する場合の条件を満たす。商用の showcase が掲載されている (https://versatiles.org/showcases/)
- アクセス量の上限・公正利用の条件: 公開デモだけ、IP ごとの流量制限。自前ホストには無い
- キャッシュ・オフライン保存: 自前ホストなら制限なし。公開デモは ETag と 6 時間の Cache-Control を出し、CDN でのキャッシュを前提にしている
- 帰属表示の要件: OSM のタイルは `OpenStreetMap contributors` が必要。陰影は Mapzen の帰属を CC BY 4.0 で引き継ぐ。土地被覆は ESA WorldCover の帰属が必要。標高は Mapterhorn の帰属。衛星は元データごとに違うので、リポジトリの一覧で確かめる (https://docs.versatiles.org/basics/tilesets)
- 他社の地図との併用、データの持ち出しの制限: 併用を禁じる記述は無い。ダウンロードも切り出しも自由

## 安定性と運用

- SLA: なし。公開デモは「約年 1 時間の停止」と書かれているが、保証はしない (2026-11-16 確認)
- 運営の継続性: 資金は寄付。主要リポジトリは 2026-11-15 まで更新され、versatiles-rs は v5.12.0 (2026-11-13)、スタイルは v9.1.0 (2026-11-09) と、活発に動いている (GitHub、2026-11-16 確認)
- 障害情報の公開先: 専用のステータスページは未確認
- 公開デモの資産は破壊的な変更を含む更新が入る。固定したいなら frontend のリリースを自分の環境に置くよう案内されている

## 向いている場面

- 無料で、全球または国や地域の OSM ベクトルタイルを、完全に自前で配信したい。API キーも外部への通信も要らない構成にしたい
- 地図の生成から配信、スタイル、フォントまでを、MapLibre の標準的な構成で 1 つの系統に揃えたい
- 閉域網、オフライン、データの持ち出しの制限があり、外部のタイル供給元を使えない
- 標高、陰影、衛星、土地被覆を、1 つのサーバーでまとめて配りたい

## 向いていない場面

- SLA、契約書、サポート窓口が必要で、自前の運用を持てない (商用ホスティングは無い)
- 住宅地図レベルの詳しさや、国内の POI、住所の検索 API が要る (OSM に依存し、ルート検索は無い)
- 日本語の注記を最優先にしたい。Shortbread の言語の扱いは確かめられていない (下の「未確認のこと」)
- 日本の高解像度の航空写真が要る。確かめられた範囲では衛星の深いズームは欧州が中心

## 出典

- https://docs.versatiles.org/
- https://docs.versatiles.org/basics/tilesets
- https://docs.versatiles.org/basics/versatiles_server
- https://docs.versatiles.org/guides/use_tiles_versatiles_org
- https://docs.versatiles.org/guides/generate_tiles_from_osm
- https://docs.versatiles.org/guides/what_about_mobile
- https://github.com/versatiles-org/versatiles-rs (MIT、v5.12.0)
- https://github.com/versatiles-org/tiles.versatiles.org (公開デモの構成)
- https://github.com/versatiles-org/versatiles-style (MIT、v9.1.0)
- https://github.com/versatiles-org/versatiles-frontend (MIT、v3.17.2)
- https://shortbread-tiles.org/schema/1.1/
- 2026-11-16 に gh で取得した GitHub 組織の一覧、リリース、ライセンス

## 未確認のこと

- Shortbread スキーマでの日本語の注記: 言語の列として `name_ko` などが見つかったが、`name_ja` の有無と、日本の注記が既定で日本語になるかは確かめていない。`@versatiles/style` の `text.language` が `ja` を受けるかも未確認
- 日本国内の POI、建物、住所の網羅度。OpenFreeMap の OpenMapTiles スキーマとの差
- 自前ホスト 1 台のアクセス量の目安と、月ごとの実費
- 衛星タイルの日本の対応範囲と、元データごとの帰属表示
- OSM タイルの更新間隔
- 商用の保守やサポートを請け負う第三者がいるか
