# OGC SensorThings API

対象: OGC SensorThings API (Part 1: Sensing 1.0、1.1、SensorThings API 2.0、Part 2: Tasking Core、拡張)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 仕様と標準化団体、版 | OGC。Part 1: Sensing 1.0 (15-078r6)、1.1 (18-088、2020-11-26 承認)。SensorThings API 2.0 (23-019、2026-09-14 承認、2026-11-04 公開)。Part 2: Tasking Core 1.0 (17-079r1)。拡張として STAplus 1.0 (22-022r1)、WebSub Asynchronous Messaging 1.0 (24-032r1) (https://www.ogc.org/standards/sensorthings/ 、 https://docs.ogc.org/is/23-019/23-019.html 、 https://docs.ogc.org/is/18-088/18-088.html 、2026-11-11) |

## 概要

センサーと観測値を、Thing (機器)、Location、Datastream (観測の系列)、Sensor、ObservedProperty、Observation (1 件の観測値)、FeatureOfInterest という決まった形で持つ API の標準である。OData に似た問い合わせ (`$filter`、`$expand`、`$select`) を HTTP で受け、同じ実体の変化を MQTT で購読できる。2.0 は 2026-11-04 に公開されたばかりで、MQTT の binding (11 章) と OGC API - Common の binding (12 章) を持つ。

## 通信の形

- 向き: HTTP では利用者が取りに行く。MQTT では、観測値の作成 (発行) と、実体の集合や 1 件の変化の購読ができる (1.1 の 14 章「SensorThings Sensing MQTT Extension」、2.0 の 11 章)。
- 何を運ぶか: 観測値、機器とその位置、観測の系列のメタデータ。
- 下にある通信: HTTP と MQTT。WebSub の拡張もある。

## 対応状況

| 環境 | 対応 | 備考 | 出典 |
|---|---|---|---|
| ブラウザ | 対応 | HTTP の JSON は `fetch` で読める。MQTT の購読は WebSocket の上の MQTT で行う ([mqtt](../realtime/mqtt.md))。ブラウザから MQTT を受けられるかはサーバーの設定による (推測) | 推測 |
| ネイティブアプリ | 対応 (HTTP と MQTT) | 専用の SDK は確かめていない | 未確認 |
| エッジ関数・サーバーレス (接続の維持) | HTTP の読み取りの前段だけ | MQTT のブローカーは常駐させる (推測) | 推測 |
| 地図ライブラリ | 直接の対応は無い | Location は GeoJSON の形を持つので、問い合わせの結果から GeoJSON を組み直して描く (推測)。地図ライブラリの公式の SensorThings 対応は見つけていない | 未確認 |

## 実装

| 実装 (OSS / 管理型サービス) | 版 | ライセンス・料金の単位 | 出典 |
|---|---|---|---|
| FROST-Server (Fraunhofer IOSB) | v2.8.2 (2026-10-25) | LGPL-3.0。公式の参照実装と自称。Part 1 の 1.0 と 1.1 を実装し、2.0 と 2.0 の拡張を README で「草案」として挙げる。MQTT の部品を別の成果物として配る | `gh api repos/FraunhoferIOSB/FROST-Server/license` 、 https://github.com/FraunhoferIOSB/FROST-Server (README、2026-11-11) |
| その他の実装 | 未確認 | OGC の製品データベースで探せる | https://www.ogc.org/standards/sensorthings/ |

## 地図プロダクトでの使いどころ

- 気象、水位、大気、騒音などのセンサー網の最新値を地図に出し、点をクリックすると時系列を出す画面。
- 複数の組織のセンサーを同じ形で集めたいとき。データの形が決まっているので、取り込む側を 1 つ書けば済む (推測)。
- 新しい値を MQTT で押し出してほしいとき。HTTP の問い合わせと購読が同じ形の実体を扱う。

## 規模と費用

- 観測値は件数が多くなる。FROST は PostgreSQL と PostGIS を使う (README の構成からの読み、詳細は未確認)。保存期間と集計の方針を先に決める (推測)。
- MQTT の購読は 1 つの Datastream ごとにトピックを持つので、地図に出す点の数だけ購読するとブローカーの負荷が増える。地図の範囲で絞った HTTP の取り直しと組み合わせる設計がある (推測)。

## 落とし穴

- 2.0 は公開されたばかりで、FROST の README はまだ「草案」と書いている (2026-11-11)。2.0 と 1.1 のどちらで作るかを、使う実装の対応で決める。
- 観測値の位置 (FeatureOfInterest) と機器の位置 (Location) が別の実体で、地図に出すときどちらを使うかを決める。
- `$expand` を深くすると応答が大きくなる。地図の一覧では最新の Observation だけを展開する (推測)。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- FROST-Server (LGPL-3.0): 自社のサーバーで動かしてネットワーク越しに使わせるだけなら、改変していてもソースの提供義務は生じない (LGPL にネットワーク越しの利用の条項は無い、条文からの読み)。FROST を改変して配布する (受託で納品する、パッケージに入れる) なら、改変した FROST のソースを LGPL-3.0 で出す。FROST をライブラリとして自社のアプリに組み込んで配布するなら、利用者が FROST の部分を差し替えられるようにし、LGPL の文を添える。自社のアプリ全体を LGPL にする必要は無い (条文からの読み。Java の war として同梱する場合の境界は推測)。
- 観測値のデータの利用条件は、センサーの持ち主ごとに違う。

## 出典

- https://www.ogc.org/standards/sensorthings/ : 文書の一覧と版。
- https://docs.ogc.org/is/23-019/23-019.html : 2.0 の承認日、公開日、MQTT の binding (11 章)、OGC API - Common の binding (12 章)。
- https://docs.ogc.org/is/18-088/18-088.html : 1.1 の承認日、MQTT の拡張 (14 章)。
- `gh api repos/FraunhoferIOSB/FROST-Server/license` 、 https://github.com/FraunhoferIOSB/FROST-Server : ライセンス、版、対応する版、MQTT の部品。

## 未確認のこと

- 国内の公的機関や自治体が SensorThings API を公開している例。
- FROST 以外の実装 (商用を含む) と、その 2.0 への対応。
- 地図ライブラリやデスクトップ GIS の SensorThings の読み込みの対応。
- FROST の DB の構成の詳細と、観測値の件数ごとの性能。
