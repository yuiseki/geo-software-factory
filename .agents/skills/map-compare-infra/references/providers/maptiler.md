# MapTiler Cloud

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | MapTiler AG (スイス、Zugerstrasse 22, 6314 Unterägeri。本社と主たるオフィスは Zug、開発チームの一部はチェコ Brno) |
| 公式サイト | https://www.maptiler.com/ |
| 料金ページ | https://www.maptiler.com/cloud/pricing/ |
| 利用規約・利用ポリシー | 一般規約 https://www.maptiler.com/terms/ 、MapTiler Cloud の特別規約 https://www.maptiler.com/cloud/terms/ 、On-Prem (Server と Data) の規約 https://www.maptiler.com/terms/server-data/ |

## 概要

MapTiler Cloud は、ベクトルタイルとラスタタイルの地図スタイル配信、自前データのホスティングと変換、ジオコーディング、標高、座標変換、静的地図、気象データなどを API で提供するクラウドサービスである (https://docs.maptiler.com/cloud/api/)。地図表示には自社の MapTiler SDK (MapLibre GL JS ベース、BSD-3-Clause) を使う方法と、MapLibre GL JS や Leaflet などの他のライブラリからタイルを直接取得する方法がある (https://www.maptiler.com/cloud/pricing/)。同じ地図を自社サーバやオフライン環境で配信する製品として MapTiler Server と MapTiler Data (On-Prem) がある (https://www.maptiler.com/server/)。

## 地図データ

- データの出どころ (自社調査 / OSM / 公的データ / 他社からのライセンス): 全球のベースとなる MapTiler Planet は OpenStreetMap が主で、低ズームに Natural Earth、高ズームの水域ポリゴンに OpenStreetMapData を使う (https://docs.maptiler.com/schema/planet/)。2025-10 から新世代スタイル (Streets v4 など) は MapTiler Planet v4 で配信されているが、v4 のデータソースの内訳は公開ページに書かれていない (https://www.maptiler.com/news/2025/10/new-generation-of-maptiler-maps/)。日本向けには国土地理院 (GSI) のベクトルタイルを収めたタイルセット「JP GSI」があり、出典表示は「© GSI」「© MapTiler」「© OpenStreetMap contributors」である (https://docs.maptiler.com/schema/jp-gsi/)。2026-05-20 公開の日本地図スタイル (ID `jp-gsi-standard`) は GSI データと MapTiler Planet v4 を組み合わせたもの (https://www.maptiler.com/news/2026/05/a-new-map-of-japan/)。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): JP GSI タイルセットには建物 (BldA、z14〜17)、道路縁 (RdEdg、z17)、行政区域、注記などのレイヤがあり、多くのレイヤは z4〜17 で提供される (https://docs.maptiler.com/schema/jp-gsi/)。`jp-gsi-standard` は日本の地図記号、命名、縦書き注記に対応すると説明されている (https://www.maptiler.com/news/2026/05/a-new-map-of-japan/)。住所・番地の網羅性と、ジオコーディングの日本の住所への対応度は未確認。
- 全球の対応: 全球 (MapTiler Planet) (https://docs.maptiler.com/schema/planet/)。
- 更新頻度: 公開ドキュメントに頻度の記載はなく、ビューアで最終更新日を確かめる形式 (https://docs.maptiler.com/schema/planet/ 、https://docs.maptiler.com/schema/jp-gsi/)。料金ページの機能表には「Regular updates」の行がある (https://www.maptiler.com/cloud/pricing/)。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | Free でも XYZ ラスタを利用可。WMTS は Flex 以上 (https://www.maptiler.com/cloud/pricing/) |
| ベクトルタイル (形式、スキーマ) | あり | MVT。MapTiler Planet のスキーマ (https://docs.maptiler.com/schema/planet/)。OpenMapTiles スキーマとの互換の程度は未確認。日本は JP GSI スキーマ (https://docs.maptiler.com/schema/jp-gsi/) |
| スタイルの編集・カスタマイズ | あり | Map Designer で編集。カスタムスタイル数の上限は Free 5、Flex 1,000、Custom 1,000 超 (https://www.maptiler.com/cloud/pricing/)。`jp-gsi-standard` も Map Designer で編集できる (https://www.maptiler.com/news/2026/05/a-new-map-of-japan/) |
| 衛星・航空写真 | あり | プリセットの Satellite スタイルがある (https://www.maptiler.com/cloud/pricing/)。On-Prem 向けに日本を含む高解像度航空写真の提供がある (https://www.maptiler.com/server/) |
| 地形・3D 建物 | あり | 3D 地形 (Map Session では傾き 65 度まで)、3D セッション枠が別にある (https://www.maptiler.com/cloud/pricing/) |
| ジオコーディング / 逆ジオコーディング | あり | Geocoding API (正逆とも) (https://docs.maptiler.com/cloud/api/) |
| ルート検索 | なし | API 一覧にルート検索・経路案内の API はない (https://docs.maptiler.com/cloud/api/) |
| オフライン利用 | Cloud はなし、On-Prem はあり | Cloud はサーバ側キャッシュ禁止、端末内の一時キャッシュのみ可 (https://www.maptiler.com/cloud/terms/)。MapTiler Server はオフライン・閉域網で動作し、`jp-gsi-standard` も On-Prem で利用できる (https://www.maptiler.com/server/ 、https://www.maptiler.com/news/2026/05/a-new-map-of-japan/) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): Web は MapTiler SDK JS (BSD-3-Clause、v4.2.1 が 2026-11-06 公開)、Android は maptiler-sdk-kotlin (BSD-3-Clause、2.5.0)、iOS は maptiler-sdk-swift (BSD-3-Clause、2.4.0) (gh で確認: https://github.com/maptiler/maptiler-sdk-js 、https://github.com/maptiler/maptiler-sdk-kotlin 、https://github.com/maptiler/maptiler-sdk-swift)。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 使える。他のライブラリからの利用は Map Session ではなくタイル API リクエストとして課金され、他のライブラリ利用自体に追加料金はない (https://www.maptiler.com/cloud/pricing/)。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): 特定 SDK に限定する条項は見当たらない。ただし課金単位が変わる (MapTiler SDK なら Map Session、他ライブラリならリクエスト数) (https://www.maptiler.com/cloud/pricing/)。
- API キー・アカウントの要否: アカウントと API キーが必要。API キー数の上限は Free 1、Flex 1,000 (https://www.maptiler.com/cloud/pricing/)。キーなしでの `api.maptiler.com/maps/jp-gsi-standard/style.json` 取得は HTTP 403 を返した (2026-11-10 に curl で確認)。

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): MapTiler SDK を使う場合は Map Session (地図を初期化したページ・アプリの読み込み 1 回。その後の操作は無制限)。他のライブラリを使う場合は API リクエスト (ベクトルタイル 1 枚 = 1、512px ラスタ = 4、256px ラスタ = 1、静的地図 1 枚 = 15、ジオコーディング 1 回 = 1。TileJSON、スタイル JSON、フォントは無料) (https://www.maptiler.com/cloud/pricing/)。
- 無料枠: Free プラン (0 USD) で月 5,000 Map Session、1,000 Search Session、2,000 3D Session、100,000 API リクエスト、ストレージ 5 GB (1 ファイル)。超過すると翌月まで停止する (https://www.maptiler.com/cloud/pricing/、2026-11-10 確認)。
- 従量単価 (主な API ごとに、通貨と確かめた日つき。問い合わせ制ならそう書き、金額を推測しない): Flex は月 30 USD (月 25,000 Map Session、3,000 Search Session、10,000 3D Session、500,000 API リクエストを含む)。超過単価は Map Session 2.50 USD / 1,000、Search Session 2.50 USD / 1,000、3D Session 6.00 USD / 1,000、API リクエスト 0.15 USD / 1,000。Custom は問い合わせ制 (いずれも税抜、2026-11-10 確認、https://www.maptiler.com/cloud/pricing/)。
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式と仮定を書く。単価が非公開なら「算出しない」): Flex プランの公開単価で計算する (2026-11-10 時点、USD、税抜)。(A) MapTiler SDK を使い 1 地図ロード = 1 Map Session とする場合、月額 = 30 + (ロード数 − 25,000) / 1,000 × 2.50。10 万ロードで 217.50 USD、100 万ロードで 2,467.50 USD、1,000 万ロードで 24,967.50 USD。(B) MapLibre GL JS などから直接タイルを取得し、1 ロードあたりベクトルタイル 20 枚 (= 20 リクエスト) と仮定する場合、月額 = 30 + (ロード数 × 20 − 500,000) / 1,000 × 0.15。10 万ロードで 255 USD、100 万ロードで 2,955 USD、1,000 万ロードで 29,955 USD。1 ロードあたりのタイル数は画面サイズと操作量で大きく変わる (仮定)。1,000 万ロード規模は Custom (年間契約、ボリューム割引) の対象になるが、Custom の金額は非公開のため算出しない。
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): Free と Flex はセルフサーブ (Flex はカードか PayPal、超過分は月末に自動請求、支出上限を設定可)。Custom は年間コミットの前払い契約で請求書払い、要見積もり (https://www.maptiler.com/cloud/pricing/)。On-Prem (MapTiler Server / Data) も価格非公開で要見積もり (https://www.maptiler.com/server/)。

## 利用規約上の制約

- 商用利用: Free は非商用と、商用製品の研究開発に限る (Cloud 特別規約 1.2、https://www.maptiler.com/cloud/terms/)。料金ページでも Free は「testing, PoC, prototyping, personal, or non-commercial use」向けで、機能表の Commercial use は Flex と Custom にチェックがある (https://www.maptiler.com/cloud/pricing/)。再販できるのは Custom のみ。動画・ゲームへの書き出しの商用利用は問い合わせ (同)。`jp-gsi-standard` を使えるプランは公開ページに記載がなく未確認。
- アクセス量の上限・公正利用の条件: プランごとの上限は料金ページの値。Free は超過で停止、Flex は従量課金、Custom はソフトリミットで大幅超過時に担当者から連絡 (https://www.maptiler.com/cloud/pricing/)。書面の合意なしにタイルの一括・過剰ダウンロードは禁止 (Cloud 特別規約 6.3、https://www.maptiler.com/cloud/terms/)。
- キャッシュ・オフライン保存: 結果をエンドユーザー個人の一時キャッシュに保存するのは可 (5.7)。サーバ側キャッシュや一時保存からの地図コンテンツの保存・再配布は禁止 (7.2) (https://www.maptiler.com/cloud/terms/)。契約終了時は地図コンテンツとバックアップを削除する義務がある (一般規約 12.5、https://www.maptiler.com/terms/)。オフライン利用は On-Prem で行う (https://www.maptiler.com/server/)。
- 帰属表示の要件: 書面で別に合意しない限り、地図表示中は MapTiler の帰属表示が必要 (Cloud 特別規約 5.4、https://www.maptiler.com/cloud/terms/)。OSM 由来データなら「© OpenStreetMap」を表示 (一般規約 6.2、https://www.maptiler.com/terms/)。Free は地図上の MapTiler ロゴも必要で、Flex と Custom はロゴ不要 (3D Session のみロゴ必須) (https://www.maptiler.com/cloud/pricing/)。JP GSI を使う場合は「© GSI」「© MapTiler」「© OpenStreetMap contributors」 (https://docs.maptiler.com/schema/jp-gsi/)。
- 他社の地図との併用、データの持ち出しの制限: 他社地図との併用を禁じる条項は Cloud 特別規約に見当たらない (https://www.maptiler.com/cloud/terms/)。製品識別や権利表示の改変・削除は禁止 (7.5、同)。派生ベクトルデータセットの作成は非商用目的か OpenStreetMap 向けに限り許可 (一般規約 4.3、https://www.maptiler.com/terms/)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): SDK はいずれも BSD-3-Clause で、組み込み・改変・配布では著作権表示とライセンス文の保持だけが求められ、SaaS 提供での追加義務はない (https://github.com/maptiler/maptiler-sdk-js)。地図データの多くは OSM 由来で ODbL が関わる。タイルを表示するだけ (Produced Work) なら「© OpenStreetMap」の表示で足りる。タイルからベクトルデータを抽出して派生データベースを作り公開・配布する場合は ODbL の継承条件 (同じライセンスでの提供) が問題になるが、MapTiler の規約自体が派生データの作成を非商用か OSM 向けに限っているため、商用でのデータ抽出はそもそも認められない (https://www.maptiler.com/terms/)。

## 安定性と運用

- SLA: Free と Flex はベストエフォート (Cloud 特別規約 8.1)。Custom は 99.9% SLA、サービスクレジット付きの個別 SLA を合意できる (8.3) (https://www.maptiler.com/cloud/terms/ 、https://www.maptiler.com/cloud/pricing/)。
- 運営の継続性 (運営主体、資金源): 運営は MapTiler AG (スイス法準拠) (https://www.maptiler.com/terms/)。創業者 Petr Pridal が率いるチームで、本社はスイス Zug (https://www.maptiler.com/company/)。資金源は未確認。
- 障害情報の公開先: https://status.maptiler.com/ (StatusCake の公開レポート)。

## 向いている場面

- 日本の地図記号や縦書き注記を含む国土地理院データ由来のスタイル (`jp-gsi-standard`) を、自社でタイル生成せずにベクトルタイルで使いたい場合 (https://www.maptiler.com/news/2026/05/a-new-map-of-japan/)。
- 同じスタイルを Cloud とオフライン・閉域網 (On-Prem) の両方で使いたい場合 (https://www.maptiler.com/server/)。
- MapLibre GL JS 系のスタックで、地図表示、ジオコーディング、標高、静的地図を 1 社で揃えたい小〜中規模の商用サービス (Flex の公開単価で予算を立てられる)。

## 向いていない場面

- 無料で商用サービスを出したい場合 (Free は非商用と研究開発のみ)。
- ルート検索が必要な場合 (API がない)。
- 月数百万ロード以上で、他ライブラリから直接タイルを取得する構成 (Flex の従量では高額になり、Custom は価格非公開)。
- タイルからデータを抽出して自社データベースに取り込みたい場合 (規約で制限)。

## 出典

- https://www.maptiler.com/
- https://www.maptiler.com/cloud/pricing/
- https://www.maptiler.com/cloud/terms/
- https://www.maptiler.com/terms/
- https://www.maptiler.com/terms/server-data/
- https://www.maptiler.com/company/
- https://www.maptiler.com/server/
- https://docs.maptiler.com/cloud/api/
- https://docs.maptiler.com/schema/planet/
- https://docs.maptiler.com/schema/jp-gsi/
- https://www.maptiler.com/news/2026/05/a-new-map-of-japan/
- https://www.maptiler.com/news/2026/05/may-updates-interactive-3d-models-and-a-new-map-of-japan/
- https://www.maptiler.com/news/2025/10/new-generation-of-maptiler-maps/
- https://status.maptiler.com/
- https://github.com/maptiler/maptiler-sdk-js
- https://github.com/maptiler/maptiler-sdk-kotlin
- https://github.com/maptiler/maptiler-sdk-swift

## 未確認のこと

- `jp-gsi-standard` を使えるプラン: 発表記事、JP GSI スキーマページ、料金ページのいずれにもプラン別の可否が書かれておらず、地図カタログはクライアント側で読み込まれるため本文から確かめられなかった。Free で表示できるかはアカウントを作って試す必要がある。
- MapTiler Planet v4 のデータソースの内訳: 発表記事に記載がなく、スキーマページは v3 の説明のみだった。
- 日本の住所・番地のジオコーディング精度: 公開ドキュメントに日本の住所データの出どころや網羅性の記載が見つからなかった。
- 各タイルセットの更新頻度: ドキュメントはビューアで最終更新日を見る形式で、頻度の記載がない。
- MapTiler Planet スキーマと OpenMapTiles スキーマの互換の程度: スキーマページが OpenMapTiles との関係を明記していない。
- 資金源: 会社紹介ページに出資・資金調達の記載がない。
- Flex の年額料金: 料金ページに年額表示がない。
- On-Prem (MapTiler Server / Data) の価格: 要問い合わせで公開されていない。
