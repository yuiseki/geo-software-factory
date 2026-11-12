# STAC API

対象: SpatioTemporal Asset Catalog (STAC) の仕様と STAC API、静的カタログ

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 仕様と標準化団体、版 | STAC 1.1.0 (2024-09-11) と STAC API 1.0.0 (2023-04-25)。どちらも Radiant Earth の GitHub で作られ、OGC の Community Standard になった (STAC 1.1.0 は 25-004、STAC API 1.0.0 は 25-005) (https://github.com/radiantearth/stac-spec/releases 、 https://github.com/radiantearth/stac-api-spec 、 https://www.ogc.org/standards/stac/ 、2026-11-11) |

## 概要

STAC は、衛星画像、空中写真、点群などの「ファイル (asset) とその範囲と時刻」を JSON で記述する目録の形式である。Catalog、Collection、Item の 3 つの形を持ち、Item は GeoJSON の Feature として範囲と時刻と asset へのリンクを持つ。STAC API は、その目録を範囲、時刻、属性で検索する API で、OGC API - Features の骨格の上に `/search` を足した形をとる。JSON ファイルを置くだけの静的カタログでも使え、検索が要るときだけ API を立てる。

## 通信の形

- 向き: 利用者が取りに行く。
- 何を運ぶか: メタデータ (Item と Collection)。画像そのものは asset の URL (多くは COG) から別に読む。
- 下にある通信: HTTP。

## 対応状況

| 環境 | 対応 | 備考 | 出典 |
|---|---|---|---|
| ブラウザ | 対応 | JSON を読むだけ。STAC Browser (ISC、v5.2.0) でカタログを閲覧できる | `gh api repos/radiantearth/stac-browser/license` (2026-11-11) |
| ネイティブアプリ | ライブラリで対応 | Python は pystac-client。QGIS の対応の範囲は未確認 | 未確認 |
| エッジ関数・サーバーレス (接続の維持) | 対応 | 静的カタログはオブジェクトストレージと CDN に置ける。stac-server は AWS Lambda と API Gateway、OpenSearch で動くサーバーレスの構成をとる (README) | https://github.com/stac-utils/stac-server (2026-11-11) |
| 地図ライブラリ | 一部 | OpenLayers 向けに ol-stac (Apache-2.0) がある。MapLibre、Leaflet に公式の STAC 対応は無い。検索結果の Item は GeoJSON なので範囲は描け、画像は COG を読むライブラリや TiTiler (MIT) でタイルにして描く (推測) | `gh api repos/m-mohr/ol-stac` 、 `gh api repos/developmentseed/titiler/license` (2026-11-11) |

## 実装

| 実装 (OSS / 管理型サービス) | 版 | ライセンス・料金の単位 | 出典 |
|---|---|---|---|
| stac-fastapi | 7.1.1 (2026-11-02) | MIT。裏の DB は別の実装を選ぶ (stac-fastapi-pgstac は MIT、stac-fastapi-elasticsearch-opensearch は MIT) | `gh api repos/stac-utils/stac-fastapi/license` ほか (2026-11-11) |
| pgstac | v0.10.1 (2026-11-10) | MIT。PostgreSQL と PostGIS の上の STAC の格納と検索 | `gh api repos/stac-utils/pgstac/license` (2026-11-11) |
| stac-server | v5.0.2 (2026-07-31) | MIT | `gh api repos/stac-utils/stac-server/license` (2026-11-11) |
| STAC Browser | v5.2.0 | ISC | `gh api repos/radiantearth/stac-browser/license` (2026-11-11) |

## 国内の公共での利用

- JAXA の「JAXA Earth」のデータベースは、COG に変換したデータセットを STAC 1.0.0 の静的カタログで出している (https://data.earth.jaxa.jp/stac/cog/v1/catalog.json を 2026-11-11 に取得)。
- JAXA は CEOS WGISS-61 (2026-03) の発表で、G-Portal の OpenSearch を 2026 年度に STAC API に置き換える予定とし、stac-fastapi と Elasticsearch で作っていると述べた。発表の時点では正式なサービスではないとしている (https://ceos.org/document_management/Working_Groups/WGISS/Meetings/WGISS-61/4.5_Progress%20and%20opening%20of%20STAC%20API%20catalog%20at%20JAXA_Yousuke%20Ikehata_v1.pdf 。検索結果の要約で読み、PDF の本文は確かめていない)。

## 地図プロダクトでの使いどころ

- 衛星画像や空中写真の「この範囲、この期間の画像」を探させる画面。
- 自前の画像やラスタ (ドローンのオルソ、浸水の推定図) を、時刻と範囲で引ける目録にしたいとき。件数が少なければ静的カタログで足りる。
- 外部の STAC API (Overture のリリース一覧も STAC で出ている、geo-software-data の [overture-maps](../../../geo-software-data/references/sources/overture-maps.md)) を読んで、使うデータを選ぶとき。

## 規模と費用

- 静的カタログはファイルの置き場所の費用だけで済む。件数が増えて範囲や時刻の検索が要るなら API と DB (pgstac や OpenSearch) を常駐させる (推測)。
- 画像そのものの転送量は目録とは別にかかる。

## 落とし穴

- STAC の版 (1.0.0 と 1.1.0) と拡張の版が混ざる。読む側のライブラリが対応する版を確かめる。
- STAC API の適合クラス (Item Search、Filter、Sort など) は実装ごとに違う。`/conformance` で確かめる。
- asset の URL が署名付きや認証付きのことがある (商用の衛星画像など)。目録が読めても画像が読めるとは限らない。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- 仕様 (stac-api-spec は Apache-2.0) と、ここで挙げた実装 (MIT、ISC、Apache-2.0) にコピーレフトは無く、組み込み、改変、配布、SaaS 提供のどれも表示の保持で足りる。
- 目録が指す画像のライセンスは asset ごと、Collection の `license` ごとに違う。画像を使う前に確かめる。

## 出典

- https://github.com/radiantearth/stac-spec/releases : STAC 1.1.0。
- https://github.com/radiantearth/stac-api-spec : STAC API 1.0.0、Apache-2.0。
- https://www.ogc.org/standards/stac/ : OGC Community Standard (25-004、25-005)。
- `gh api repos/<owner>/<repo>/license` と releases (stac-utils/stac-fastapi、stac-utils/pgstac、stac-utils/stac-server、radiantearth/stac-browser、developmentseed/titiler、m-mohr/ol-stac) : ライセンスと版。
- https://data.earth.jaxa.jp/stac/cog/v1/catalog.json : JAXA Earth の STAC。

## 未確認のこと

- JAXA の G-Portal の STAC API が正式に公開されたか。
- Tellus など国内の他の衛星データ基盤の STAC 対応。
- QGIS の STAC 対応の版と範囲。
- stac-server を動かしたときの AWS の費用。
