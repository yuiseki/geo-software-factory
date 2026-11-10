# 地理院タイル (国土地理院)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | 国土交通省 国土地理院 |
| 公式サイト | https://maps.gsi.go.jp/development/ichiran.html (地理院タイル一覧)、https://maps.gsi.go.jp/development/siyou.html (仕様) |
| 料金ページ | なし (無料で提供。料金ページは存在しない) |
| 利用規約・利用ポリシー | 国土地理院コンテンツ利用規約 https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html 、地理院地図の利用規約 https://maps.gsi.go.jp/help/termsofuse.html 、測量法に基づく承認申請 https://www.gsi.go.jp/LAW/2930-index.html |

## 概要

国土地理院が XYZ 方式で配信するラスタタイル群で、標準地図、淡色地図、全国最新写真 (シームレス)、年代別の空中写真、色別標高図や陰影起伏図、標高タイル (DEM) などを含む (https://maps.gsi.go.jp/development/ichiran.html)。URL は `https://cyberjapandata.gsi.go.jp/xyz/{t}/{z}/{x}/{y}.{ext}` の形で、タイルは 256x256 ピクセル、ウェブメルカトル投影である (https://maps.gsi.go.jp/development/siyou.html)。API キーや登録は無く、出典を明示すれば外部のウェブサイトやアプリからリアルタイムに読み込める (https://www.gsi.go.jp/LAW/2930-qa.html Q1-12)。ベクトルタイルは「最適化ベクトルタイル」として試験公開中である (https://github.com/gsi-cyberjapan/optimal_bvmap)。

## 地図データ

- データの出どころ (自社調査 / OSM / 公的データ / 他社からのライセンス): 公的データ。標準地図・淡色地図は国の基本図である電子国土基本図が元で、ズーム 5〜8 は 500 万分 1 の小縮尺地図が元である (https://maps.gsi.go.jp/development/ichiran.html)。全球の低ズームでは海底地形に GEBCO、海岸線に VMAP0 を使い、それらの出所も明示する必要がある (同)。一部のタイルは他機関の作成物で、その機関の条件が加わる (同、「その他」の区分)。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): 標準地図はズーム 18 まであり、電子国土基本図の建物 (家屋の形状)、道路、鉄道、地名・施設名の注記を含む (https://maps.gsi.go.jp/development/ichiran.html)。住所・番地の表示や商業 POI (店舗など) は収録対象ではない (推測。電子国土基本図の性格から。一覧ページに POI の記載が無い)。道路属性はラスタ画像なので取り出せない。最適化ベクトルタイルでは地物種別コードや注記分類コードを属性として持つ (https://github.com/gsi-cyberjapan/optimal_bvmap)。
- 全球の対応: 標準地図・淡色地図はズーム 2〜8 で全球を表示できる (国内と周辺は 5〜18) (https://maps.gsi.go.jp/development/ichiran.html)。標高タイルには地球地図全球版標高第 2 版によるズーム 0〜8 の全球版がある (同)。詳細な地図は国内のみ。
- 更新頻度: 決まった頻度の公表は無い。電子国土基本図は「面的更新」と「迅速更新」(道路の開通などに合わせた更新) で随時更新されている (https://www.gsi.go.jp/kibanjoho/kibanjoho40082.html 、https://www.gsi.go.jp/kyusyu/kyusyu41011.html)。最適化ベクトルタイルの PMTiles 版は「2026年7月1日時点」のデータで、従来の XYZ 版は 2023 年 10 月 1 日時点で更新を止めている (https://github.com/gsi-cyberjapan/optimal_bvmap)。DEM のテキスト形式タイルは 2024 年 10 月から更新を停止している (https://maps.gsi.go.jp/development/ichiran.html)。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | 標準地図 `std` (PNG)、淡色地図 `pale` (PNG)、英語版 `english`、白地図、色別標高図 `relief` (z5〜15)、陰影起伏図 `hillshademap`、傾斜量図、赤色立体地図など (https://maps.gsi.go.jp/development/ichiran.html) |
| ベクトルタイル (形式、スキーマ) | 試験公開 | 「最適化ベクトルタイル」。Mapbox Vector Tile 仕様の pbf を XYZ (`optimal_bvmap-v1/{z}/{x}/{y}.pbf`) と単一 PMTiles (`optimal_bvmap-v1.pmtiles`) で配信。ズーム 4〜16 (17 はオーバーズーム)。ズームはラスタより 1 小さい数値で対応する。スキーマは国土地理院独自 (地物種別コード等の仕様書あり)。URL や属性は変わる可能性があると明記 (https://github.com/gsi-cyberjapan/optimal_bvmap) |
| スタイルの編集・カスタマイズ | ベクトルのみ可 | 最適化ベクトルタイルのリポジトリにスタイル JSON、スプライト、グリフがあり、MapLibre GL JS で表示するデモがある (https://github.com/gsi-cyberjapan/optimal_bvmap)。ラスタは配色を変えられない |
| 衛星・航空写真 | あり | 全国最新写真 (シームレス) `seamlessphoto` z14〜18、電子国土基本図 (オルソ画像) `ort`、年代別: 1936〜1942 年頃 `ort_riku10` (東京 23 区・大阪市周辺のみ、z13〜18)、1945〜1950 年 `ort_USA10`、1961〜1969 年 `ort_old10`、1974〜1978 年 `gazo1`、1979〜1983 年 `gazo2`、1984〜1986 年 `gazo3`、1987〜1990 年 `gazo4` (いずれも z10〜17)、年度別 `nendophoto{年}`。低ズームの世界衛星モザイク `modis` (z2〜8) もある (https://maps.gsi.go.jp/development/ichiran.html) |
| 地形・3D 建物 | 地形のみ | 標高タイル: DEM1A (z1〜17)、DEM5A/5B/5C (z1〜15)、DEM10B (z1〜14) の PNG 形式とテキスト形式、全球版 `demgm` (z0〜8)、湖水深タイル (https://maps.gsi.go.jp/development/ichiran.html)。PNG 標高タイルは独自の符号化で、MapLibre の raster-dem が標準で読む Terrain-RGB / Terrarium 形式ではない (推測。変換が要る)。3D 建物のタイルは一覧に無い |
| ジオコーディング / 逆ジオコーディング | 公式の公開 API は無い | 地理院地図が内部で使う地名検索などのサーバ機能は「主に地理院地図からの利用を想定」しており、長期提供や仕様の維持は保証しないと国土地理院の担当者が回答している。住所検索は東京大学 CSIS のシンプルジオコーディングを使っているとも回答している (https://github.com/gsi-cyberjapan/gsimaps/issues/29) |
| ルート検索 | なし | 一覧に無い (https://maps.gsi.go.jp/development/ichiran.html) |
| オフライン利用 | 条件付き | タイルをダウンロードして使うこと自体を禁じる規定は見当たらないが、標準地図・淡色地図など基本測量成果に当たるタイルは、複製・加工の内容によって測量法 29 条・30 条の申請が要る場合がある (https://www.gsi.go.jp/LAW/2930-index.html 、https://www.gsi.go.jp/LAW/2930-qa.html)。最適化ベクトルタイルは PMTiles 1 ファイルで配信されている (https://github.com/gsi-cyberjapan/optimal_bvmap) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): 無い。地理院地図自体のソースは BSD-2-Clause で公開されている (https://github.com/gsi-cyberjapan/gsimaps)。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 使える。ラスタは標準的な XYZ なので、XYZ タイルを読める Leaflet、OpenLayers、MapLibre GL JS などで表示できる (https://maps.gsi.go.jp/development/siyou.html)。最適化ベクトルタイルは MapLibre GL JS と pmtiles パッケージで表示するデモが公式リポジトリにある (https://github.com/gsi-cyberjapan/optimal_bvmap)。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): 規約上、特定の SDK に限る定めは見当たらない (https://maps.gsi.go.jp/help/termsofuse.html)。
- API キー・アカウントの要否: 不要。URL を直接参照する (https://maps.gsi.go.jp/development/siyou.html)。

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): なし (無料)。
- 無料枠: 全量無料。ただし、サーバの正常な運用を妨げるおそれのある負荷をかける通信は予告なく遮断される場合がある (https://maps.gsi.go.jp/help/termsofuse.html)。
- 従量単価 (主な API ごとに、通貨と確かめた日つき。問い合わせ制ならそう書き、金額を推測しない): なし (2026-11-10 時点で無料)。
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式と仮定を書く。単価が非公開なら「算出しない」): 利用料は 0 円。ただし数値上の上限は公表されておらず、大量アクセスは遮断の対象になりうるので、1,000 万ロード級では自前でタイルを配信する (申請要否を確かめたうえで) か、キャッシュ層を挟む構成を検討する必要がある (推測)。
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): 契約なし。登録も不要。

## 利用規約上の制約

- 商用利用: 国土地理院コンテンツ利用規約は特段の記載が無い限り公共データ利用規約 第 1.0 版 (PDL1.0) を適用する (https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html)。PDL1.0 は商用利用を妨げない。リアルタイムに読み込むウェブサイトやアプリは営利・非営利を問わず出典の明示のみで申請不要 (https://www.gsi.go.jp/LAW/2930-qa.html Q1-12)。
- アクセス量の上限・公正利用の条件: 数値の上限は公表されていない。サーバの正常な運用を妨げる、またはそのおそれがある負荷の通信は予告なく遮断される場合がある (https://maps.gsi.go.jp/help/termsofuse.html)。
- キャッシュ・オフライン保存: キャッシュについての明文の規定は見当たらない (https://maps.gsi.go.jp/help/termsofuse.html)。タイルを複製して使う場合、基本測量成果に当たるタイル (標準地図、淡色地図など。一覧の備考に「基本測量成果」と書かれたもの) は、複製なら測量法 29 条、加工して別の地図を作るなら 30 条の承認申請が要る場合がある。基本測量成果でないタイル (写真など) はコンテンツ利用規約に従い出典明示で使える (https://www.gsi.go.jp/LAW/2930-index.html)。Q&A では、ウェブ提供される地理院タイルなどの基本測量成果は「刊行地図をそのまま複製して配布してはならない」原則の対象外とされている (https://www.gsi.go.jp/LAW/2930-qa.html Q1-17)。個別の判断は「地図の利用手続ナビ」(https://service.gsi.go.jp/onestop/navi/index/) で行う。
- 帰属表示の要件: 「国土地理院」または「地理院タイル」などと記載し、地理院タイル一覧ページへリンクする (https://www.gsi.go.jp/LAW/2930-qa.html Q1-12)。加工した場合はその旨を別に記載し、国土地理院が作成したように見せてはならない (https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html)。低ズームの全球図は GEBCO と VMAP0 の出所も記載する。タイルによっては備考欄に個別の出典表記がある (https://maps.gsi.go.jp/development/ichiran.html)。最適化ベクトルタイルは「国土地理院最適化ベクトルタイル」などと出典を明示する (https://github.com/gsi-cyberjapan/optimal_bvmap)。「地理院地図」「地理院タイル」は国土地理院の登録商標である (https://maps.gsi.go.jp/development/ichiran.html)。
- 他社の地図との併用、データの持ち出しの制限: 他の地図との重ね合わせを禁じる規定は見当たらない (https://maps.gsi.go.jp/help/termsofuse.html)。持ち出し (複製・加工) は上記の測量法の手続に従う。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): データに継承条件 (share-alike) は無い。PDL1.0 は出典表示型で CC BY 4.0 と互換とされる (PLATEAU のサイトポリシーでの説明 https://www.mlit.go.jp/plateau/site-policy/ 。国土地理院のページ自体は互換性に触れていない)。ただし測量法という別の法律による手続が上乗せされる点が CC BY と異なる。組み込み (リアルタイム参照) は出典明示のみ、改変 (加工して別の地図を作る) は基本測量成果なら 30 条申請の対象になりうる、配布 (タイルを同梱して再配布) は 29 条の対象になりうる、SaaS 提供 (自社サーバから地理院タイルを再配信) も複製に当たるため基本測量成果なら申請の要否を確かめる (推測。Q&A に SaaS の明示例は無い)。地理院地図のソースコードは BSD-2-Clause でコピーレフトではない (https://github.com/gsi-cyberjapan/gsimaps)。

## 安定性と運用

- SLA: なし。利用によって生じた一切の損害について国土地理院は責任を負わず、内容は予告なく変更・追加・削除される場合がある (https://maps.gsi.go.jp/help/termsofuse.html)。最適化ベクトルタイルは試験公開で、公開期間は「公開終了まで」とされ、基本測量成果としての提供を検討するための位置付けである (https://github.com/gsi-cyberjapan/optimal_bvmap)。
- 運営の継続性 (運営主体、資金源): 国の行政機関 (国土交通省 国土地理院) が国費で運営する。ラスタの標準地図は 2013 年から提供されている (https://maps.gsi.go.jp/development/ichiran.html)。
- 障害情報の公開先: 専用のステータスページは見当たらない。国土地理院ウェブサイトのお知らせで、メンテナンスや緊急メンテナンスを告知している (例: https://www.gsi.go.jp/johosystem/johosystem45041.html)。

## 向いている場面

- 国内の公共・行政・防災・教育向けの地図で、無料かつ国の基本図を背景にしたいとき。
- 年代別の空中写真や標高データ (陰影起伏図、赤色立体地図、DEM) を重ねて土地の変化や地形を見せたいとき。
- 試作や小中規模のサービスで、API キーや契約なしにすぐ表示したいとき。

## 向いていない場面

- SLA が要る業務システムや、大量アクセスが見込まれる商用サービス (遮断の可能性があり、保証が無い)。
- 店舗 POI、住所・番地、ルート検索、ジオコーディングが要る用途 (公式の公開 API が無い)。
- ベクトルタイルを長期に固定のスキーマで使いたい場合 (試験公開で URL や属性が変わりうる)。
- 海外の詳しい地図が要る用途。

## 出典

- https://maps.gsi.go.jp/development/ichiran.html
- https://maps.gsi.go.jp/development/siyou.html
- https://maps.gsi.go.jp/help/termsofuse.html
- https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html
- https://www.gsi.go.jp/LAW/2930-index.html
- https://www.gsi.go.jp/LAW/2930-qa.html
- https://service.gsi.go.jp/onestop/navi/index/
- https://www.gsi.go.jp/kibanjoho/kibanjoho40082.html
- https://www.gsi.go.jp/kyusyu/kyusyu41011.html
- https://www.gsi.go.jp/johosystem/johosystem45041.html
- https://github.com/gsi-cyberjapan/optimal_bvmap
- https://github.com/gsi-cyberjapan/gsimaps
- https://github.com/gsi-cyberjapan/gsimaps/issues/29
- https://www.mlit.go.jp/plateau/site-policy/

## 未確認のこと

- 電子国土基本図の更新が地理院タイルに反映される頻度: 面的更新・迅速更新を随時行うとの説明はあるが、タイルへの反映周期を示す公式の記述が見つからなかった。
- アクセス量の具体的な上限値: 規約は「負荷をかける通信は遮断する場合がある」とだけ書き、数値を公表していない。
- タイルを一括ダウンロードしてオフライン同梱する場合や、自社サーバから再配信する場合に申請が要るかの確定的な判断: Q&A は書籍やウェブへの挿入、リアルタイム参照の例を示すが、アプリ同梱や再配信の明示例が見つからなかった。利用手続ナビで個別に確かめる必要がある。
- 最適化ベクトルタイルの建物に高さ属性があるか (3D 建物表示に使えるか): 属性一覧の PDF を読んでいない。
- 年代別空中写真 (gazo1〜4、ort_old10、ort_USA10) の提供範囲: 一覧ページに範囲の記載が無かった。
