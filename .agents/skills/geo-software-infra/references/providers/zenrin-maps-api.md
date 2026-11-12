# ZENRIN Maps API

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 運営主体 | 株式会社ゼンリン (データと API の提供元、利用条件の契約相手)。販売・トライアルの窓口は株式会社ゼンリンデータコム (https://www.zenrin-datacom.net/solution/zenrin-maps-api 、https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html) |
| 公式サイト | https://www.zenrin-datacom.net/solution/zenrin-maps-api 、開発者サイト https://developers.zmaps-api.com/ |
| 料金ページ | 専用の料金表は無い。初期費用と月額の下限は製品ページと FAQ に記載 (https://www.zenrin-datacom.net/solution/zenrin-maps-api 、https://www.zenrin-datacom.net/solution/zenrin-maps-api/faq) 。課金の計上方法は https://developers.zmaps-api.com/service.html |
| 利用規約・利用ポリシー | ZENRIN Maps API 利用条件 https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html 、地図使用規約 (ZENRIN Maps API 版) https://developers.zmaps-api.com/document/Terms_of_Use_for_Map.html |

## 概要

ゼンリンの国内地図 (住宅地図を含む) を Web アプリや業務システムに組み込むための API 群で、地図表示の JavaScript API、サーバ側で使う Web API (検索、ルート、住所クレンジングなど)、スマートフォン向けの位置測位・ジオフェンスライブラリーから成る (https://developers.zmaps-api.com/service.html)。2020 年 12 月 15 日に提供を始めた (https://www.sbbit.jp/article/refers/49303)。旧来の「いつもNAVI API」と SDK、住宅地図サービス ZNETTOWN API/CGI の機能は ZENRIN Maps API に統合され、現在は ZENRIN Maps API が案内されている (https://www.zenrin-datacom.net/solution/api)。法人向けの見積もり契約で、2 か月の無料トライアルがある (https://www.zenrin-datacom.net/solution/zenrin-maps-api/trial)。

## 地図データ

- データの出どころ (自社調査 / OSM / 公的データ / 他社からのライセンス): 自社調査。POI は株式会社ゼンリンのデータに基づき、一部オプションは協力会社のデータ (https://developers.zmaps-api.com/qa.html)。ゼンリンの住宅地図は専門スタッフの現地調査で全国 1,741 市区町村を網羅し、都市部は毎年、それ以外も 2〜6 年に 1 回を目安に更新するとしている (https://www.zenrin.co.jp/product/category/residentialmap/index.html)。
- 国内の詳しさ (建物の形状、住所・番地、POI、道路の属性、注記): 住宅地図デザインは建物 1 軒ごとの家形と表札名 (居住者名) を描画でき、表札名なしの版もある (https://developers.zmaps-api.com/v20/reference/javascriptAPI/maptype.html 、https://developers.zmaps-api.com/v20/reference/javascriptAPI/info_js.html)。Web API に住所検索、地番検索、地番と住所の変換、建物・テナント検索、施設 (POI) 検索、交差点検索、建物の到着地点・入口検索、道路リンク検索 (プレミアムで標高・中央分離帯) がある (https://developers.zmaps-api.com/v20/reference/webAPI/)。
- 全球の対応: 国内のみ。FAQ はサービスを「国内地図の提供」と説明している (https://developers.zmaps-api.com/qa.html)。英語、簡体字・繁体字中国語、韓国語の多言語検索と英語版地図デザインはある (https://developers.zmaps-api.com/v20/reference/webAPI/ 、https://developers.zmaps-api.com/v20/reference/javascriptAPI/maptype.html)。
- 更新頻度: 地図の調査時期は地区によって異なり、調査地区一覧で確かめる (https://developers.zmaps-api.com/qa.html 、https://gis.zenrin.co.jp/product/gis/znettown/manual/area_list.pdf)。API 側の地図データ更新周期は未確認。

## 提供形式と機能

| 機能 | 有無 | 備考 |
|---|---|---|
| ラスタタイル | あり | Web API「画像出力 (WMTS)」が OGC WMTS 互換のタイル画像を返す (GetCapabilities / GetTile)。中心点とサイズを指定する静的地図画像 API もある (https://developers.zmaps-api.com/v20/reference/webAPI/)。JavaScript API にも「ラスター配信用」の地図デザインがある (https://developers.zmaps-api.com/v20/reference/javascriptAPI/maptype.html) |
| ベクトルタイル (形式、スキーマ) | JavaScript API 内部のみ | JavaScript API の「スタンダード」「住宅地図」「過去地図」はベクター描画 (https://developers.zmaps-api.com/v20/reference/javascriptAPI/maptype.html)。ベクトルタイルを直接取得する Web API は一覧に無い (https://developers.zmaps-api.com/v20/reference/webAPI/) |
| スタイルの編集・カスタマイズ | 既定デザインの選択のみ | スタンダード、モノクロ、英語版、住宅地図 (表札名あり/なし)、過去地図 (2020 年まで / 2021 年から)、ブランドアイコンなしのラスターなど ID で選ぶ。ズームは 3〜22 (過去地図の 2020 年までは 17〜22) (https://developers.zmaps-api.com/v20/reference/javascriptAPI/maptype.html)。自由なスタイル編集の機能は見当たらない |
| 衛星・航空写真 | 未確認 | API 一覧と地図デザインの一覧に航空写真の項目が見当たらない (https://developers.zmaps-api.com/v20/reference/webAPI/) |
| 地形・3D 建物 | 一部 | 標高・水深検索 (5m、10m、500m メッシュ) がある。住宅地図デザインはズーム 16 以上で等高線を表示する (https://developers.zmaps-api.com/v20/reference/webAPI/ 、https://developers.zmaps-api.com/v20/reference/javascriptAPI/maptype.html)。地図は回転と傾きを操作できる (https://developers.zmaps-api.com/v20/reference/javascriptAPI/info_js.html)。3D 建物の表示は未確認 |
| ジオコーディング / 逆ジオコーディング | あり | 住所検索 (フリーワード、リスト、緯度経度からの逆引き)、多言語住所検索、郵便番号検索、住所クレンジング、住所マッチング (https://developers.zmaps-api.com/v20/reference/webAPI/) |
| ルート検索 | あり | 歩行者ルート、自動車ルート (地点間、最適巡回)、ルート候補とガイダンス、マルチモーダル、VICS 交通情報、マップマッチング (https://developers.zmaps-api.com/v20/reference/webAPI/)。一部は有料オプション (https://developers.zmaps-api.com/qa.html) |
| オフライン利用 | なし | 利用にはインターネット接続が要る (https://developers.zmaps-api.com/qa.html)。端末に保存できるのは ZID と、利用条件で定める「保存可能データ」に限られる (https://developers.zmaps-api.com/service.html) |

## 対応ライブラリ

- 公式 SDK (Web / Android / iOS): Web は JavaScript API (地図表示、図形、マーカー、GL レイヤーなど)。iOS / Android は位置測位ライブラリーとジオフェンスライブラリーで、ネイティブの地図表示 SDK は一覧に無い (https://www.zenrin-datacom.net/solution/zenrin-maps-api 、https://developers.zmaps-api.com/v20/reference/javascriptAPI/)。
- 公式以外のライブラリから使えるか (MapLibre GL JS, Leaflet, OpenLayers など): WMTS 互換のタイル画像があるので、WMTS や XYZ のラスタを読めるライブラリで技術的には表示できると考えられる (推測。公式のサンプルや可否の明記は見つからなかった)。ベクター描画の地図は JavaScript API でのみ使える。
- 組み合わせの制約 (特定の SDK でしか表示してはならない等): 利用条件に、特定のライブラリに限る定めは見当たらない。一方で、地図データの複製、抽出、加工、送信、第三者への使用許諾は禁じられている (https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html)。
- API キー・アカウントの要否: 要る。契約とお試し ID の発行が前提で、認証は OAuth 2.0 (クライアント ID とシークレット)、IP 認証、リファラ認証に対応する (https://developers.zmaps-api.com/qa.html 、https://developers.zmaps-api.com/v20/reference/webAPI/)。

## 料金

- 課金単位 (地図ロード、タイルリクエスト、MAU など): PV 数による従量課金と、住宅地図など一部機能のライセンス課金。Web API は原則 1 リクエスト 1 PV、WMTS 系は 1 リクエスト 0.1 PV、住所クレンジングは処理した住所 1 件ごと、ZID 検索は ZID 1 件ごと。JavaScript 地図はローダーの読み込みごとに 1 PV で、スクロールや縮尺変更は計上しない (https://developers.zmaps-api.com/service.html)。検証環境への接続は課金対象外 (https://developers.zmaps-api.com/qa.html)。
- 無料枠: 恒常的な無料枠は見当たらない。お試し ID による 2 か月の無料トライアルがある。申込は会社や所属組織のメールアドレスが要り (フリーメール不可)、海外でのデータ受信による利用はできず、競合他社からの申込は控えるよう求めている。ID は申込から 3 営業日以内にメールで届く (https://www.zenrin-datacom.net/solution/zenrin-maps-api/trial)。導入フローには「約 1〜2 ヶ月間」との記載もある (https://www.zenrin-datacom.net/solution/zenrin-maps-api)。
- 従量単価 (主な API ごとに、通貨と確かめた日つき。問い合わせ制ならそう書き、金額を推測しない): 初期費用 36 万円 (税別)、月額 6 万円 (税別) から (日本円、2026-11-10 確認) (https://www.zenrin-datacom.net/solution/zenrin-maps-api/faq)。PV あたりの単価は公開されておらず問い合わせ制。住宅地図は利用エリアと条件により個別見積もり (https://www.zenrin-datacom.net/solution/zenrin-maps-api)。
- 月 10 万 / 100 万 / 1,000 万 地図ロードの概算 (計算式と仮定を書く。単価が非公開なら「算出しない」): 算出しない (PV 単価が非公開)。初年度の下限は 36 万円 + 6 万円 x 12 か月 = 108 万円 (税別) だが、月額 6 万円にどれだけの PV が含まれるかは未確認。
- 契約形態 (セルフサーブ / 要見積もり / 年間契約): 要見積もり。利用条件に同意したうえで、営業担当から案内される申込書で申し込む (https://developers.zmaps-api.com/service.html)。有効期間は申込書の記載どおりで、自動更新を選ぶと満了 3 か月前までに意思表示が無ければ 1 年間継続する (https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html 第 5 条)。プランはスタンダード契約とプレミアム契約 (住宅地図、過去住所、土地コンテンツなど) (https://developers.zmaps-api.com/service.html)。

## 利用規約上の制約

- 商用利用: 可能 (法人向けの有償契約が前提)。ユーザーは契約者の役員・従業員、または契約者や再許諾先の顧客である第三者と定義されている (https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html 第 2 条)。
- アクセス量の上限・公正利用の条件: チャネルごと・API 機能ごとに 1 秒あたりのリクエスト数の上限があり、値は営業担当に問い合わせる。超過分は HTTP 429、資源の状況によっては制限内でも 503 を返す。上限の引き上げは追加契約 (https://developers.zmaps-api.com/v20/reference/appendix/req_limit.html)。
- キャッシュ・オフライン保存: 端末への保存は ZID と、住所クレンジングや ZID 検索などの応答 (「保存可能データ」) に限られる (https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html 第 7 条、https://developers.zmaps-api.com/service.html)。地図使用規約は、地図データ等の複製 (印刷を含む)、転記、抽出、加工、改変、翻案、送信を禁じる。印刷は公開サイトや不特定多数向けアプリでない場合に限りブラウザ印刷で A3 以下まで (https://developers.zmaps-api.com/document/Terms_of_Use_for_Map.html)。
- 帰属表示の要件: 利用条件と地図使用規約に、利用者へ著作権表示を義務付ける条文は見当たらない。一方、ユーザーへ「地図使用規約」を掲載して同意を得ることが義務とされる (https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html 第 8 条)。
- 他社の地図との併用、データの持ち出しの制限: 他の地図の精度向上や新たな地図の作成への利用、AI モデルや機械学習への利用、生成 AI の成果物作成への利用、リバースエンジニアリングは禁止 (https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html 第 8 条)。他社の地図を同じ画面に重ねることを直接禁じる条文は見当たらない。日本国外で利用する場合は個人情報保護法の趣旨に沿った体制整備が要り、国外向けのサイトやアプリに住宅地図の居住者氏名を配信する API を組み込むことは禁止 (同 第 8 条、第 13 条)。
- ライセンス上の注意 (GPL / LGPL / AGPL などのコピーレフト、OSI 非承認、UNLICENSED、データの ODbL / CC BY-SA などの継承条件があれば、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。無ければ「なし」): データはプロプライエタリで、継承条件付きのオープンライセンスではない。組み込みは契約の範囲内、改変 (加工・翻案) と配布 (複製・送信・第三者への許諾) は禁止、SaaS 提供は契約者の顧客を「ユーザー」とする再許諾の枠組みで、利用条件と申込書の範囲に限られる (https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html)。開発者サイトの OSS ライセンス一覧には AGPL-3.0 の PM2 が載っている (https://developers.zmaps-api.com/oss.html)。PM2 はサーバ側のプロセス管理ツールで、利用者が配布物に組み込むものではないため、利用者側に AGPL の義務は生じないと考えられる (推測)。

## 安定性と運用

- SLA: 公開文書に SLA の記載は見当たらない。ゼンリンは天災、保守、障害などでサービスを中断でき、事前通知は可能な限り努めるとされる。完全性・正確性・目的適合性は保証しない (https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html 第 16 条、第 17 条)。リクエスト上限内でもリソースや応答時間は保証しない (https://developers.zmaps-api.com/v20/reference/appendix/req_limit.html)。
- 運営の継続性 (運営主体、資金源): 住宅地図事業の株式会社ゼンリン (上場企業、証券コード 9474) が提供し、販売は子会社のゼンリンデータコムが担う (https://www.zenrin.co.jp/ir/pdf/corporate_profile.pdf 、https://www.zenrin-datacom.net/solution/api)。前身のいつもNAVI API から統合された経緯がある (https://www.zenrin-datacom.net/solution/api)。
- 障害情報の公開先: 開発者サイトの「お知らせ」と「API 更新履歴」(https://developers.zmaps-api.com/news.html 、https://developers.zmaps-api.com/changelog.html)。専用のステータスページは見当たらない。

## 向いている場面

- 建物 1 軒単位の住宅地図、地番、表札名が業務に要る用途 (不動産、保険、インフラ点検、自治体の業務システムなど)。
- 住所クレンジングや住所と地番の変換、建物ターゲティングなど、住所データの整備と地図表示を同じ契約で済ませたいとき。
- 大型車ルートや最適巡回など、国内の配送・移動業務のルート計算。

## 向いていない場面

- 個人開発や小規模サービス (初期費用 36 万円と月額 6 万円からの契約が前提で、恒常的な無料枠が無い)。
- 海外の地図が要る用途、海外からのアクセスが中心のサービス。
- オフライン利用、地図データの保存・加工・機械学習への利用、自前のタイル配信が必要な用途 (規約で禁止)。
- MapLibre などでスタイルを自由に作り込みたい用途 (ベクトルタイルの直接取得とスタイル編集の手段が見当たらない)。

## 出典

- https://www.zenrin-datacom.net/solution/zenrin-maps-api
- https://www.zenrin-datacom.net/solution/zenrin-maps-api/faq
- https://www.zenrin-datacom.net/solution/zenrin-maps-api/trial
- https://www.zenrin-datacom.net/solution/api
- https://developers.zmaps-api.com/
- https://developers.zmaps-api.com/service.html
- https://developers.zmaps-api.com/qa.html
- https://developers.zmaps-api.com/oss.html
- https://developers.zmaps-api.com/news.html
- https://developers.zmaps-api.com/changelog.html
- https://developers.zmaps-api.com/document/Terms_of_Use_for_ZMapsAPI.html
- https://developers.zmaps-api.com/document/Terms_of_Use_for_Map.html
- https://developers.zmaps-api.com/v20/reference/javascriptAPI/
- https://developers.zmaps-api.com/v20/reference/javascriptAPI/info_js.html
- https://developers.zmaps-api.com/v20/reference/javascriptAPI/maptype.html
- https://developers.zmaps-api.com/v20/reference/webAPI/
- https://developers.zmaps-api.com/v20/reference/appendix/req_limit.html
- https://gis.zenrin.co.jp/product/gis/znettown/manual/area_list.pdf
- https://www.zenrin.co.jp/product/category/residentialmap/index.html
- https://www.zenrin.co.jp/ir/pdf/corporate_profile.pdf
- https://www.sbbit.jp/article/refers/49303 (提供開始のプレスリリース転載。補助)

## 未確認のこと

- PV あたりの従量単価と、月額 6 万円に含まれる PV 数: 公式ページに金額の記載が無く、問い合わせ制のため。
- 衛星・航空写真と 3D 建物の提供有無: API 一覧と地図デザイン一覧に項目が見当たらないが、提供しないとの明記も見つからなかった。
- WMTS タイルを MapLibre GL JS や Leaflet など他のライブラリで表示することが規約上認められるか: 利用条件に明示的な定めが見つからなかった。
- 地図表示に著作権表示 (例: ZENRIN のクレジット) を出す義務の有無: 利用条件と地図使用規約に義務の条文が見つからなかった。地図描画に自動で表示される可能性はあるが、確かめていない。
- API の地図データの更新周期: 調査時期が地区ごとに異なるとの説明のみで、API への反映周期は書かれていない。
- 個人の申込可否: トライアルページは法人を主な対象とし、フリーメール不可とするが、個人を明示的に排除する文言は見つからなかった。
- 提供開始日 (2020-12-15) は第三者サイトへのプレスリリース転載で確かめた。ゼンリン公式のニュースリリース本文は読んでいない。
