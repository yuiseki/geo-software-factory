# CARTO basemaps

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | CartoDB Inc. (屋号 CARTO、307 Fifth Avenue, Floor 9, New York, NY 10016, USA) |
| 公式サイト | https://carto.com/basemaps |
| 料金ページ | https://carto.com/basemaps/apikey/ (料金表は同ページの #pricing) |
| 利用規約・利用ポリシー | Basemap Terms https://carto.com/legal/basemap-terms/ (2026-09-29 最終更新)、帰属表示 https://carto.com/attribution/ 、FAQ https://docs.carto.com/faqs/carto-basemaps |

## 概要

CARTO basemaps は、データ可視化の背景に使う控えめな配色のベースマップ (Voyager、Positron、Dark Matter) を、ラスタタイルとベクトルタイルで配信するサービスである (https://github.com/CartoDB/basemap-styles)。2026-09 に API キー必須化と商用の有料プランが導入され、ラスタは 2026-09-25 からキーなしでは配信されない (https://docs.carto.com/faqs/carto-basemaps)。ベクトル版は 2026-10-21 から Protomaps basemap のスキーマ (v2) で配信され、従来の OpenMapTiles スキーマ (v1) は非推奨で 2025-12 以降データ更新がない (https://github.com/CartoDB/basemap-styles)。地図以外の API (ジオコーディング、ルート検索など) はベースマップサービスには含まれない。

## 地図データ

- データの出どころ (自社調査 / OSM / 公的データ / 他社からのライセンス): OpenStreetMap ベース (https://docs.carto.com/faqs/carto-basemaps)。v2 の TileJSON は「Basemap layers derived from OpenStreetMap and Natural Earth」と記述している (https://tiles.basemaps.cartocdn.com/vector/carto.streets/v2/tiles.json を 2026-11-10 に取得)。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): OSM の日本のデータに依存する。v2 のタイルには buildings (高さ、番地の属性 `addr_housenumber` を含む)、pois、roads、places の各レイヤがあり、places / pois / roads / water / earth に `name:ja` 属性がある (同 TileJSON の vector_layers を 2026-11-10 に確認)。ただし配信スタイル (Voyager) のラベルは `name` と `name:en` を参照しており、日本語ラベル表示の挙動は未確認 (https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json を 2026-11-10 に取得)。
- 全球の対応: 全球 (TileJSON の bounds が全球、z0〜15) (同 TileJSON)。ラスタは z0〜20 (https://github.com/CartoDB/basemap-styles)。
- 更新頻度: ベクトルは少なくとも年 1 回、多くの年は 3 か月か 6 か月ごとだが保証はない。ラスタも同じデータで更新が続く (https://docs.carto.com/faqs/carto-basemaps)。2026-11-10 時点の配信リリースは `20261026-01` (style.json の URL から確認)。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | `https://{s}.basemaps.cartocdn.com/{style}/{z}/{x}/{y}{scale}.png`、@2x あり。light_all、dark_all、rastertiles/voyager とラベル有無の派生。API キー必須 (https://github.com/CartoDB/basemap-styles 、https://docs.carto.com/faqs/carto-basemaps) |
| ベクトルタイル (形式、スキーマ) | あり | MVT。v2 は Protomaps basemap スキーマ (TileJSON の version 4.15.2)、v1 は OpenMapTiles スキーマで非推奨・更新停止 (https://github.com/CartoDB/basemap-styles 、https://docs.protomaps.com/basemaps/layers)。2026-11-10 時点はキーなしでも配信されるが、将来キー必須になる可能性があると FAQ にある (https://docs.carto.com/faqs/carto-basemaps) |
| スタイルの編集・カスタマイズ | 自前で可 | 配信スタイルは voyager、positron、dark-matter と各 nolabels 版。カスタムスタイルは自分でホストし、グリフとスプライトも自前で用意し、ソースだけ v2 TileJSON を指す。配信スタイルのコピーは内部の URL (`/v/<release>/`) が変わるため壊れうる (https://github.com/CartoDB/basemap-styles)。スタイル編集の GUI はない |
| 衛星・航空写真 | なし | ベースマップの一覧にない (https://github.com/CartoDB/basemap-styles) |
| 地形・3D 建物 | 一部 | v2 の buildings に高さ属性があり、押し出し表示は自作スタイルで可能 (TileJSON で確認)。地形 (標高) タイルの提供はない |
| ジオコーディング / 逆ジオコーディング | なし (basemaps としては) | ベースマップの FAQ・README・規約に記載なし。CARTO 本体のプラットフォームの機能は本資料の対象外 |
| ルート検索 | なし (basemaps としては) | 同上。規約 14 条はリアルタイムのナビゲーション用途を制限している (https://carto.com/legal/basemap-terms/) |
| オフライン利用 | なし | 端末・ブラウザでのキャッシュは 30 日まで、サーバ側のキャッシュ・プロキシと一括ダウンロードは禁止 (規約 9.c、https://carto.com/legal/basemap-terms/) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): ベースマップ用の独自 Web SDK はなく、MapLibre GL JS や deck.gl にスタイル URL を渡す (https://github.com/CartoDB/basemap-styles)。README は CARTO Mobile SDK 向けスタイルに触れているが、github.com/CartoDB/mobile-sdk は 2026-11-10 に gh で取得すると 404 で、現行の提供状況は未確認。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): 使える。FAQ は Leaflet、OpenLayers、MapLibre GL JS、Mapbox GL JS、deck.gl を挙げる (https://docs.carto.com/faqs/carto-basemaps)。OpenLayers は ol-mapbox-style でベクトルスタイルを使える (https://github.com/CartoDB/basemap-styles)。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): 特定 SDK に限定する条項は見当たらない (https://carto.com/legal/basemap-terms/)。v1 から v2 への移行ではレイヤ名と属性が変わるため、OpenMapTiles 用の自作スタイルやラベル・フィルタの処理は書き直しになる (https://docs.carto.com/faqs/carto-basemaps 、https://docs.protomaps.com/basemaps/layers)。
- API キー・アカウントの要否: ラスタは必須。キーなしのリクエストには「API KEY REQUIRED · carto.com/basemaps/apikey」と入った画像が返る (https://docs.carto.com/faqs/carto-basemaps)。ベクトルは 2026-11-10 時点でキーなしでも取得できた (curl で v2 の MVT が HTTP 200)。キーはタイル URL に `?key=` で渡す (https://github.com/CartoDB/basemap-styles)。

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): タイルリクエスト数。暦月 (UTC) でアカウント内の全キー、ラスタとベクトルを合算する (https://carto.com/basemaps/apikey/)。
- 無料枠: 非商用 (個人、研究、教育、非営利) は月 500 万リクエストまで無料。商用は月 100 万リクエストまで無料 (https://carto.com/basemaps/apikey/、2026-11-10 確認)。CARTO プラットフォームの顧客と CARTO の助成対象は商用プラン不要 (https://docs.carto.com/faqs/carto-basemaps)。
- 従量単価 (主な API ごとに、通貨と確かめた日つき。問い合わせ制ならそう書き、金額を推測しない): 従量単価はなく定額プラン。Basemaps Commercial は月 500 USD か年 5,000 USD 前払いで月 1,000 万リクエストまで。Basemaps Commercial Plus は月 1,500 USD か年 15,000 USD で月 5,000 万リクエストまで。いずれも税別。月 5,000 万超は問い合わせ制 (https://carto.com/basemaps/apikey/ 、https://docs.carto.com/faqs/carto-basemaps、2026-11-10 確認)。上限超過時の扱い (停止か追加請求か) は公開ページに書かれていない。
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式と仮定を書く。単価が非公開なら「算出しない」): 仮定は商用利用、1 地図ロードあたり 20 タイル。月間リクエスト = ロード数 × 20。10 万ロードは 200 万リクエストで商用の無料枠 (100 万) を超え、Basemaps Commercial の月 500 USD (年払いなら 5,000 USD / 12 = 約 416.67 USD/月)。100 万ロードは 2,000 万リクエストで Basemaps Commercial Plus の月 1,500 USD (年払いなら 1,250 USD/月)。1,000 万ロードは 2 億リクエストで 5,000 万を超え、問い合わせ制のため算出しない。非商用なら 10 万ロード (200 万リクエスト) は無料枠 500 万の範囲内。1 ロードあたりのタイル数は画面サイズと操作量で変わる (仮定)。
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): Commercial と Commercial Plus はダッシュボードからカードで購入するセルフサーブ (月額か年額)。解約はいつでもできるが支払済み期間の終わりまで続く。月 5,000 万超や個別要件は要見積もり (https://carto.com/basemaps/apikey/)。2026-09-23 より前に登録したキーの商用利用は 2026-11-30 まで従来どおり使える (https://docs.carto.com/faqs/carto-basemaps)。

## 利用規約上の制約

- 商用利用: 可。規約上の商用利用は「広告を含め収益を生む」利用で、それ以外 (個人、教育、学術、研究、非営利) は非商用 (1.g 条)。2026-09-23 から商用で月 100 万リクエストを超える場合は有料プランが必要 (https://carto.com/legal/basemap-terms/ 、https://docs.carto.com/faqs/carto-basemaps)。
- アクセス量の上限・公正利用の条件: 非商用は月 500 万、商用は月 100 万リクエストの公正利用上限 (12 条、https://carto.com/legal/basemap-terms/)。有料プランは月 1,000 万 / 5,000 万 (https://carto.com/basemaps/apikey/)。
- キャッシュ・オフライン保存: 端末・ブラウザでの 30 日を超えるキャッシュ、利用終了後のキャッシュ保持、サーバ側のプロキシ・キャッシュ、一括ダウンロード、タイルやデータとしての再販・再配布はいずれも禁止 (9.c 条、https://carto.com/legal/basemap-terms/)。
- 帰属表示の要件: OpenStreetMap と CARTO の両方を、各地図の閲覧者に目立つ形で表示する (13 条、https://carto.com/legal/basemap-terms/)。例「© OpenStreetMap contributors © CARTO」 (https://github.com/CartoDB/basemap-styles)。
- 他社の地図との併用、データの持ち出しの制限: 他社地図との併用を禁じる条項は見当たらない。他のソフトウェアに組み込んだリアルタイムナビゲーション用途は制限される (14 条)。タイルの再配布は禁止 (9.c 条) (https://carto.com/legal/basemap-terms/)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): スタイル定義 (CartoDB/basemap-styles) はコードが BSD-3-Clause、見た目のデザインが CC BY 4.0 (https://github.com/CartoDB/basemap-styles の LICENSE.md)。CC BY 4.0 は継承 (SA) 条件がなく、改変・配布・SaaS 提供のいずれでもデザインの出典表示 (CARTO) が求められるだけ。v2 タイルが基づく Protomaps basemap はコードが BSD-3、スタイルデザインが CC0、タイルは OSM の Produced Work として ODbL の下にあり「© OpenStreetMap」の表示が必要。Protomaps のタイルやスタイルを改変して配布・API 提供する場合は製品名に Protomaps を使えない (https://github.com/protomaps/basemaps)。CARTO のタイルからデータを抽出して派生データベースを配布すると ODbL の継承条件が問題になるが、規約が一括ダウンロードと再配布を禁じているため、そもそもできない (https://carto.com/legal/basemap-terms/)。

## 安定性と運用

- SLA: Basemap Terms に SLA や稼働率の約束はなく、中断なく提供されることを保証しない旨の免責がある (19 条、https://carto.com/legal/basemap-terms/)。有料プランの SLA の有無は未確認。
- 運営の継続性 (運営主体、資金源): 運営は CartoDB Inc. (ニューヨーク州法準拠、22 条) (https://carto.com/legal/basemap-terms/)。資金源は未確認。2026-09 の有料化により、ベースマップ単体の収益源ができた (https://carto.com/basemaps/apikey/)。
- 障害情報の公開先: https://status.carto.com/ (CARTO 全体のステータスページ。ベースマップ単独の項目があるかは未確認)。

## 向いている場面

- データ可視化の背景として、主張の弱い配色 (Positron、Dark Matter、Voyager) を使いたい場合 (https://github.com/CartoDB/basemap-styles)。
- 非営利・研究・教育用途で、月 500 万リクエストまで無料で使いたい場合。
- deck.gl や MapLibre GL JS で、Protomaps スキーマのタイルを使い、スタイルを自分で書きたい場合 (スタイルデザインは CC BY 4.0、Protomaps のスタイルは CC0 で流用しやすい)。
- 月 1,000 万〜5,000 万リクエストの商用利用で、定額で予算を固定したい場合。

## 向いていない場面

- 衛星画像、ジオコーディング、ルート検索も同じ提供元で揃えたい場合 (ベースマップサービスにない)。
- オフライン利用やサーバ側キャッシュが必要な場合 (規約で禁止)。
- v1 (OpenMapTiles スキーマ) 用に作ったスタイルをそのまま使い続けたい場合 (v1 は更新停止、v2 はスキーマが異なる)。
- SLA が必要な場合 (規約に SLA がない)。
- 日本向けに、日本語ラベルや国内の詳しい表現が前提の汎用地図が欲しい場合 (背景用の控えめな表現で、配信スタイルは `name` / `name:en` を参照)。

## プライバシーとテレメトリ (2026-11-14 確認)

- **リクエストデータの扱い**: CARTO の Basemaps Terms and Conditions によると、CARTO は顧客の委託先 (Data Processor) としてタイルリクエストを処理し、レート制限・不正検知・配信運用のために IP アドレスの末尾オクテット (IPv4) / 末尾セグメント (IPv6) を切り詰めて記録する。
- **保持期間と処理場所**: 切り詰め後のリクエストログは米国で 30 日間保持される。独自 SDK による端末横断の行動追跡や位置テレメトリ収集の記載は未確認。

## 出典

- https://carto.com/basemaps
- https://carto.com/basemaps/apikey/
- https://carto.com/legal/basemap-terms/
- https://carto.com/attribution/
- https://docs.carto.com/faqs/carto-basemaps
- https://github.com/CartoDB/basemap-styles
- https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json
- https://tiles.basemaps.cartocdn.com/vector/carto.streets/v2/tiles.json
- https://docs.protomaps.com/basemaps/layers
- https://github.com/protomaps/basemaps
- https://status.carto.com/

## 未確認のこと

- 配信スタイルでの日本語ラベル表示: タイルには `name:ja` があるが、Voyager の style.json は `name` と `name:en` を参照しており、実際に日本でどの言語のラベルが出るかを描画して確かめていない。
- 有料プランの上限超過時の扱いと SLA: 料金ページ・FAQ・規約に記載がない。
- CARTO Mobile SDK の現行の提供状況: README は言及しているが、GitHub リポジトリが 404 だった。
- 資金源: ベースマップの公開ページに記載がなく、会社情報のページは調べていない。
- status.carto.com にベースマップ単独の監視項目があるか: ページが JavaScript 依存で、取得したテキストからは部品の一覧を読めなかった。
- basemap-styles の LICENSE.md 冒頭に「ホスト配信の利用は CARTO のエンタープライズ顧客と助成対象に限る」という記述が残っており、README・FAQ・規約 (無料枠あり) と食い違う。本文は 2026-09-29 更新の規約と FAQ を正とした。
