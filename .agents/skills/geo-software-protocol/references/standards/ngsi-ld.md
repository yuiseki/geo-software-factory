# NGSI-LD

対象: ETSI の NGSI-LD API (GS CIM 009) と、その実装 (FIWARE Orion-LD、Scorpio)。前の世代の NGSIv2 (FIWARE Orion) にも触れる

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 仕様と標準化団体、版 | ETSI の ISG CIM (Context Information Management) の Group Specification、ETSI GS CIM 009。最新は V1.9.1 (2025-07)。配布の一覧には V1.1.1 から V1.9.1 までがある (https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/ 、 https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.09.01_60/gs_CIM009v010901p.pdf 、2026-11-11) |

## 概要

都市や工場の「もの」(駐車場、バス停、センサー、建物) を、ID と型を持つ実体 (Entity) と、その属性 (Property)、位置 (GeoProperty)、他の実体への参照 (Relationship) として持ち、JSON-LD で読み書きする API である。属性の意味は JSON-LD の @context で語彙に結びつける。範囲や距離で絞る Geoquery (`georel=near;maxDistance==2000`、`within` など) を仕様に持ち、実装はこれを必ず持つ (`shall be supported`)。変化の購読 (Subscription) で、HTTP や MQTT に通知を送れる。

## 通信の形

- 向き: 利用者が取りに行く (問い合わせ) と、購読による通知 (サーバーから押し出す)。
- 何を運ぶか: 実体とその属性 (位置を含む)、属性の履歴 (temporal)。
- 下にある通信: HTTP の binding (仕様 6 章「API HTTP Binding」)。通知には MQTT の binding がある (目次の「API MQTT Notification Binding」)。

## 対応状況

| 環境 | 対応 | 備考 | 出典 |
|---|---|---|---|
| ブラウザ | 対応 (HTTP の JSON) | 通常の JSON (`application/json`) でも、JSON-LD でも受け取れる。購読の通知の送り先は URL か MQTT のブローカーなので、ブラウザに直接は届かない。間に SSE や WebSocket の配信を置く (推測) | GS CIM 009 V1.9.1 |
| ネイティブアプリ | 対応 (HTTP) | 同上 | 推測 |
| エッジ関数・サーバーレス (接続の維持) | 通知の受け手に向く | 購読の通知を受ける HTTP の端点は関数 1 つで書ける (推測)。ブローカー本体は常駐させる | 推測 |
| 地図ライブラリ | 直接の対応は無い | `Accept: application/geo+json` を送ると、実体を GeoJSON の Feature (一覧なら FeatureCollection) で返す形を仕様が持つ。それを GeoJSON ソースにすれば描ける (推測) | GS CIM 009 V1.9.1 |

## 実装

| 実装 (OSS / 管理型サービス) | 版 | ライセンス・料金の単位 | 出典 |
|---|---|---|---|
| FIWARE Orion-LD | 1.12.0 (2026-01-28) | AGPL-3.0。README は NGSI-LD 1.6.1 にほぼ準拠し、それより新しい版の一部の機能を持つとする。MongoDB を使い、履歴は TRoE で PostgreSQL に保存 | `gh api repos/FIWARE/context.Orion-LD/license` 、 https://github.com/FIWARE/context.Orion-LD (README、2026-11-11)。geo-software-arch の [source-of-truth](../../../geo-software-arch/references/capabilities/source-of-truth.md) |
| Scorpio (NEC Laboratories Europe、NEC Technologies India) | 6.0.1 (2026-01-19) | BSD-3-Clause。PostgreSQL (PostGIS) を使い、Kafka を使う構成と使わない構成がある。マイクロサービスに分けて伸ばせる | `gh api repos/ScorpioBroker/ScorpioBroker/license` 、 https://github.com/ScorpioBroker/ScorpioBroker (README、2026-11-11) |
| FIWARE Orion (NGSIv2) | 未確認 | AGPL-3.0。NGSI-LD ではなく前の世代の NGSIv2 | `gh api repos/telefonicaid/fiware-orion/license` (2026-11-11) |

## 国内の公共での利用

- デジタル田園都市国家構想の地域のデータ連携基盤で、データ社会推進協議会が連携の部品として FIWARE を勧めている、と AWS のブログが書いている (https://aws.amazon.com/jp/blogs/news/aws-and-fiware-to-buid-cityos-for-smartcity 、2026-11-11)。協議会の一次資料は確かめていない。
- 各自治体の基盤が NGSIv2 と NGSI-LD のどちらを使っているかは、確かめた範囲では分からなかった (未確認)。

## 地図プロダクトでの使いどころ

- 自治体の都市 OS やデータ連携基盤と連携する地図で、相手が NGSI の API を出しているとき。
- 駐車場の空き、バスの位置、設備の状態など、ID を持つ「もの」の最新の状態を位置で絞って出す地図。Geoquery で範囲を切れる。
- 変化の通知を受けて、地図の成果物 (GeoJSON、タイル) を作り直すとき。

## 規模と費用

- ブローカーは常駐のサーバーと DB (Orion-LD は MongoDB、Scorpio は PostgreSQL) が要る。費用はサーバーの台数と DB の大きさで決まる (推測)。
- 地図の利用者がブローカーに直接問い合わせると負荷が利用者の数に比例する。読み出しは成果物 (CDN に置いた GeoJSON) に分けると軽くなる (推測)。

## 落とし穴

- 実装が準拠する版が仕様の最新版と違う。Orion-LD は 1.6.1 にほぼ準拠、Scorpio の README は 1.2.2 の文書にリンクしている (どの版に準拠するかは未確認)。使う機能が実装にあるかを確かめる。
- @context の扱い: 属性名は @context で URI に展開される。読み手と書き手で @context が違うと、同じ名前の属性が別物として扱われる。
- NGSIv2 (Orion) と NGSI-LD は互換でない。相手の基盤がどちらかを先に確かめる。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- Orion-LD と Orion (AGPL-3.0): 改変した版をネットワーク越しに利用者に使わせる (SaaS) なら、その利用者に改変版のソースを提供する (AGPL-3.0 第 13 条)。配布 (受託で納品、パッケージに入れる) するなら、改変の有無にかかわらず GPL と同じくソースを提供する。README には権利者の説明として「バグ修正や機能追加のために改変したものは派生物に当たり、改変していない版を使う、または (リンクして) 集めるだけのソフトウェアは派生物に当たらない」とある (https://github.com/FIWARE/context.Orion-LD 、2026-11-11)。改変せずに API の向こうで使うだけなら、自社の地図アプリにソースの提供義務は及ばない (この説明からの推測)。
- Scorpio (BSD-3-Clause): 組み込み、改変、配布、SaaS 提供のどれも、著作権表示とライセンス文の保持で足りる。
- 仕様の文書は ETSI のもので、無料で読める。仕様の文書の利用条件は確かめていない。

## 出典

- https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/ : 版の一覧。
- https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.09.01_60/gs_CIM009v010901p.pdf : V1.9.1 (2025-07)、Geoquery、HTTP の binding、MQTT の通知の binding、`application/geo+json`。
- `gh api repos/<owner>/<repo>/license` と releases (FIWARE/context.Orion-LD、ScorpioBroker/ScorpioBroker、telefonicaid/fiware-orion) : ライセンスと版。
- https://github.com/FIWARE/context.Orion-LD 、 https://github.com/ScorpioBroker/ScorpioBroker : 準拠する版、DB、ライセンスの説明。
- https://aws.amazon.com/jp/blogs/news/aws-and-fiware-to-buid-cityos-for-smartcity : 国内の FIWARE の推奨 (二次資料)。

## 未確認のこと

- Scorpio が準拠する NGSI-LD の版。
- 国内の自治体の基盤ごとの NGSIv2 と NGSI-LD の使い分けと、データ社会推進協議会の一次資料。
- 管理型の NGSI-LD ブローカーのサービスと料金。
- FIWARE Orion (NGSIv2) の最新版。
