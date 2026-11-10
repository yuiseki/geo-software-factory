# 韓国 (NAVER Maps / Kakao Maps / VWorld)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |

## 概要

韓国では、国が作った基本測量成果と公共測量成果 (地図や測量用写真) を国土交通部長官の許可なく国外へ持ち出すことが法律で禁じられている ([공간정보관리법 제16조・제21조](https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B3%B5%EA%B0%84%EC%A0%95%EB%B3%B4%EC%9D%98%EA%B5%AC%EC%B6%95%EB%B0%8F%EA%B4%80%EB%A6%AC%EB%93%B1%EC%97%90%EA%B4%80%ED%95%9C%EB%B2%95%EB%A5%A0))。そのため国外のデータセンターで地図を処理する Google などは、精細な国の地図データを使えず、韓国国内では経路案内などの機能が制限されてきた ([Wikipedia](https://en.wikipedia.org/wiki/Restrictions_on_geographic_data_in_South_Korea))。国内のサーバーで処理する NAVER と Kakao が国内の Web 地図の主な選択肢になっている。2026-02-27 に Google への 1:5,000 地図の国外持ち出しが条件付きで許可されたが、2026-11-10 時点で実際の持ち出しは確認されていない。

## 法規制

- 地図データの作成・提供・国外持ち出しに関わる法令と所管 (条文や公的文書の出典つき):
  - 「공간정보의 구축 및 관리 등에 관한 법률」(공간정보관리법、2026-07-01 施行版、所管は国土交通部 공간정보제도과) ([国家法令情報センター](https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B3%B5%EA%B0%84%EC%A0%95%EB%B3%B4%EC%9D%98%EA%B5%AC%EC%B6%95%EB%B0%8F%EA%B4%80%EB%A6%AC%EB%93%B1%EC%97%90%EA%B4%80%ED%95%9C%EB%B2%95%EB%A5%A0))。
  - 第16条 第1項: 何人も国土交通部長官の許可なく基本測量成果のうち地図等または測量用写真を国外へ持ち出してはならない (外国政府との交換など大統領令で定める場合を除く)。第2項: 第14条第3項の各号 (国家安保や国の重大な利益を害するおそれがある場合など) に当たる基本測量成果は国外に持ち出してはならない。ただし国土交通部長官が科学技術情報通信部、外交部、統一部、国防部、行政安全部、産業通商部、国家情報院などの長と協議体を構成して持ち出しを決めた場合は除く。第3項で協議体に 1 人以上の民間専門家を含めることを求める。
  - 第21条: 公共測量成果にも同じ趣旨の国外持ち出し禁止を定め、国家安保に関わる場合は第16条第2項の協議体の決定を要件とする。
  - 第15条: 基本測量成果を使った地図等を刊行・販売・配布する者は国土交通部長官の審査を受ける (第4項)。国家安保を害するおそれがあり大統領令で定める事項は地図等に表示できない (第2項)。
  - 罰則: 第16条または第21条に違反して測量成果を国外へ持ち出した者は 2 年以下の懲役または 2,000 万ウォン以下の罰金 (第108条第3号)。第15条第4項の審査を受けずに地図等を刊行・販売・配布した者は 1 年以下の懲役または 1,000 万ウォン以下の罰金 (第109条第2号)。法人にも罰金刑を科す両罰規定がある (第110条)。
  - 以上の条文は 2026-11-10 に国家法令情報センターの本文で確認した。「Web 地図サービスのタイル配信が『国外持ち出し』に当たるか」といった個別の解釈は条文からは決まらず、ここでは断定しない。
- 外国企業・外国人がサービスを提供・利用するときの制約:
  - 法律上の制約は国籍ではなく「国外への持ち出し」にかかる。国外のサーバーで韓国の精細な地図データを処理するには、第16条の許可が要る。
  - 2026-02-27 の Google への条件付き許可 (国土交通部の측량성과 국외반출 협의체。9 つの政府機関と民間専門家で構成) の内容は次のとおり ([정책브리핑 korea.kr](https://www.korea.kr/news/policyNewsView.do?newsId=148960112)、[UPI](https://www.upi.com/Top_News/World-News/2026/02/27/korea-Google-map-data-South-Korea-approval-high-precision/4641772177574/))。
    - 範囲: ナビゲーションと経路探索に必要な最小限のデータ。等高線など安保上敏感なデータは除く。
    - 条件: 衛星・航空画像の保安処理、過去の画像とストリートビューでの軍事・保安施設のぼかし、座標表示の制限、国内の提携企業が国内サーバーで原データを加工し政府の検討を経たものだけを持ち出すこと、政府の要請時の速やかな修正、緊急停止の仕組みを含む保安事故対応体制、国内常駐の責任者の配置。
    - 事後管理: 政府が条件の履行を確かめてから持ち出しを認め、履行しない場合や重大な違反があれば中止・取り消しできる。
  - 外国企業が NAVER や Kakao の API を契約して使う場合の制約は「主なサービス」の表に書いた。
- 国境・領土表示の規制と罰則:
  - 国家安保を害するおそれがある事項 (大統領令で定める) は地図等に表示できない (공간정보관리법 第15条第2項)。軍事・保安施設は画像上でぼかす運用がされており、Google への許可条件にも含まれる ([정책브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=148960112))。
  - 国境や地名の表記 (島や海の名称など) を定める規定と罰則は、今回確かめられなかった (未確認)。

## 座標系

- 使われる座標系と WGS84 との違い:
  - 공간정보관리법 第6条は、位置を「세계측지계」(世界測地系) による経緯度と平均海面からの高さで表すと定め、地図作成などのために直角座標などを使うことも認める ([国家法令情報センター](https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B3%B5%EA%B0%84%EC%A0%95%EB%B3%B4%EC%9D%98%EA%B5%AC%EC%B6%95%EB%B0%8F%EA%B4%80%EB%A6%AC%EB%93%B1%EC%97%90%EA%B4%80%ED%95%9C%EB%B2%95%EB%A5%A0))。中国の GCJ-02 のように、公開地図の座標を意図的にずらす制度は確認できなかった。世界測地系の楕円体などの細目は大統領令で定めるとされ、その本文は確かめていない (未確認)。
  - 国内では投影座標 (TM 系) や旧来の Bessel 楕円体の座標も使われる。Kakao のローカル API の座標系変換は WGS84、WCONGNAMUL、CONGNAMUL、WTM、TM、KTM、UTM、BESSEL、WKTM、WUTM を扱い、既定は WGS84 ([Kakao Developers ローカル API](https://developers.kakao.com/docs/ko/local/dev-guide))。
- 座標変換の扱い (公開されたアルゴリズムの有無、法的な制約):
  - 国内の座標系間の変換は Kakao などの API で公開されており、変換そのものを禁じる規定は見当たらなかった。ただし Google への許可条件には「座標表示の制限」が含まれており、精細なデータを国外へ出す事業者に座標の表示を制限する運用がありうる ([정책브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=148960112))。
- 技術選定への影響 (GPS 座標や他の地図との重ね合わせ):
  - GPS (WGS84) の座標は、WGS84 の経緯度を受け付ける地図 API にそのまま載せられる。韓国の公共データを使う場合は TM 系や Bessel 系の座標で配布されていることがあるので、取り込むときに WGS84 へ変換する。
  - NAVER Maps の座標系の扱いは公式文書で確かめていない (未確認)。

## 主なサービス

| サービス | 運営 | 提供形式 (Web / ネイティブ / タイル API) | 外国企業・国外からの利用条件 | 商用利用と料金の概略 | 出典 |
|---|---|---|---|---|---|
| NAVER Maps (NAVER Cloud Platform の Maps) | NAVER Cloud | Web Dynamic Map (JS)、Mobile Dynamic Map SDK (Android/iOS)、REST API (Static Map、Directions 5/15、Geocoding、Reverse Geocoding)。2025 年にカスタムスタイル対応の新しい Maps 商品が出た | NAVER Cloud Platform のリージョンは韓国、米国、シンガポール、日本、ドイツで、提供内容は同じとされる。韓国外の利用者は加入手続や一部サービスに制限があり、加入はサポートへの問い合わせとされる (検索結果の抜粋による)。外国法人が Maps を契約できるかは未確認 | 代表アカウント 1 つに限り月間無料枠: Dynamic Map 6,000,000 件、Static Map 3,000,000 件、Geocoding 3,000,000 件、Reverse Geocoding 3,000,000 件、Directions 5 が 60,000 件、Directions 15 が 3,000 件。超過分の単価はページ上で動的に表示され取得できなかった (未確認)。税別。2026-11-10 確認 | [NAVER Cloud Maps 商品ページ](https://www.ncloud.com/product/applicationService/maps)、[Maps 概要](https://guide.ncloud-docs.com/docs/maps-overview)、[新 Maps 告知](https://www.ncloud.com/support/notice/all/1965)、[会員種別ガイド](https://guide.ncloud-docs.com/docs/en/userguide-userguideaccount) |
| Kakao Maps API | Kakao | Web (JavaScript) SDK、Android/iOS SDK、REST API (住所・座標変換、キーワード・カテゴリ検索、公共交通・徒歩・自転車経路、静的地図) | Kakao Developers のアカウントで利用。無料枠は開発者アカウントで最初に有効化したアプリだけ。2 つ目以降のアプリはビズウォレットを連携して有料設定が必要 (2026-07-21 から)。国外の法人・個人がビズウォレットを使えるかは未確認 | 日次無料枠: 地図 Web SDK 300,000 件、Android/iOS SDK 300,000 件、ローカル REST API 各 100,000 件、経路と静的地図 各 1,000 件。月間合計 3,000,000 件。追加分の単価: 地図 SDK 0.1 ウォン/件、住所・座標変換 0.5 ウォン/件、検索と静的地図 2 ウォン/件、経路 10 ウォン/件。2026-11-10 確認 | [Kakao Developers クォータ](https://developers.kakao.com/docs/ko/getting-started/quota)、[2026-06-16 の告知](https://devtalk.kakao.com/t/api-notice-on-new-kakao-map-api-features-and-free-quota-policy/150222)、[Kakao Maps API](https://apis.map.kakao.com/) |
| VWorld (공간정보 오픈플랫폼) | 国土交通部 (国土交通部の空間情報オープンプラットフォーム) | WebGL 2D/3D 地図 API、WMTS (`https://api.vworld.kr/req/wmts/1.0.0/{APIキー}/WMTSCapabilities.xml` の形式)、ジオコーダーなどの Open API | 会員登録のうえ API キーを申請し、キーは登録したサービス URL で動く (第三者の記事による)。国外からの登録と接続の可否は未確認 (この調査環境からは接続できなかった) | 無料で使えるとする第三者の記事があるが、公式の利用規約と商用条件は取得できなかった (未確認)。一部 API に日次の呼び出し上限があり、超過は申請と承認が必要とされる (検索結果の抜粋による) | [VWorld 開発者センター](https://www.vworld.kr/dev/v4dv_dhapiguide_s001.do)、[Esri Korea の VWorld 利用資料](https://preview.esrikr.com/content/dam/distributor-share/esrikr-com/home/kr-techsupport-file/enterprise-attached-file/arcgis-vworld-25.pdf) |

## 国外のサービスを使う場合

- Google Maps, Mapbox, OSM などをこの地域で使ったときの制約と表示の質:
  - Google Maps: Google Maps Platform の Prohibited Territories に韓国は含まれていない (北朝鮮は含まれる) ([Prohibited Territories](https://cloud.google.com/maps-platform/terms/maps-prohibited-territories))。ただし Google は韓国の地図を公開されている 1:25,000 の地図データと航空・衛星画像で作っており ([UPI](https://www.upi.com/Top_News/World-News/2026/02/27/korea-Google-map-data-South-Korea-approval-high-precision/4641772177574/))、韓国では車と徒歩の経路案内などが制限されてきた ([Wikipedia](https://en.wikipedia.org/wiki/Restrictions_on_geographic_data_in_South_Korea))。
  - 2026-02-27 以降の状況 (日付つき):
    - 2026-02-27: 1:5,000 地図の国外持ち出しを条件付き許可 ([정책브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=148960112))。
    - 2026-09: Google が青瓦台、国防部、在韓米軍基地、DMZ などの衛星画像のぼかしを始めた ([電子新聞 2026-10-28](https://www.etnews.com/20261028000277))。
    - 2026-10-20 時点: 条件全体の履行結果は政府に提出されていないと報じられた ([디지털데일리 2026-10-26](https://www.ddaily.co.kr/page/view/2026102610060597667))。
    - 2026-10-23: 国会の国政監査で、古里原発の施設がぼかされていないと指摘された。国土交通部長官は条件の履行を検証してから実データを持ち出すと答えた (同上の 2 記事)。
    - 2026-10-28 報道: 政府と専門家の実務 TF が Google Korea を訪れ、持ち出し前の技術事項を点検した。業界は早ければ年内、遅くとも 2027 年初めに Google が国の 1:5,000 地図で国内サービスを更新すると見ている ([電子新聞](https://www.etnews.com/20261028000277))。これは業界の見通しで、Google の発表ではない。
    - 2026-11-10 時点で、実際の持ち出しや経路案内の提供開始を伝える公式発表は見つからなかった。
  - Mapbox: 韓国向けの特別な制約や提供形態は公式文書で確かめていない (未確認)。
  - OSM: OSM のデータは WGS84 で、韓国の Web 地図と座標は大きくずれない。韓国の政府地図をなぞって OSM に入れることの適否は OSM コミュニティで議論があるが ([OSM コミュニティ](https://community.openstreetmap.org/t/osm/5177))、結論は確かめていない (未確認)。国内事業者と比べた道路・POI の詳しさの定量比較も確かめていない (未確認)。

## 技術選定への影響

- この地域を対象に含むプロダクトで、ライブラリとタイルの選び方がどう変わるか:
  - 韓国国内の利用者向けに経路案内や詳しい POI が要るなら、NAVER Maps か Kakao Maps が第一候補になる。どちらも自社の JS SDK とネイティブ SDK で描画する形で、MapLibre などで汎用のベクトルタイルとして読む提供形態は確認できなかった (未確認)。
  - 背景地図だけでよく、国の公式データを使いたいなら VWorld の WMTS が候補になる。WMTS なので MapLibre、OpenLayers、Leaflet などで表示できる。国外からの利用可否と規約は先に確かめる。
  - 世界向けプロダクトで Google Maps を使う場合、韓国だけ経路機能が欠ける前提で設計し、韓国では NAVER か Kakao に出し分けるかを決める。抽象化層を挟んでおくと、Google の韓国対応が進んだときに切り替えやすい。
  - 無料枠はどちらも「代表アカウント 1 つ」「最初に有効化したアプリ 1 つ」に限られる。複数のアプリや環境 (開発・本番) を持つなら、2 つ目以降は最初から有料になる前提で見積もる (2026-11-10 確認)。
- 情勢で変わりうる点 (日付つきで書き、見直す前提にする):
  - Google への条件付き許可 (2026-02-27) の履行検証と実際の持ち出しは 2026-11-10 時点で未完了と報じられている。持ち出しが始まれば Google Maps の韓国での経路案内などが変わりうる。2027 年初めごろに見直す。
  - Kakao の無料枠の運用は 2026-07-21 に変わった。それ以前から使っているアプリは追って案内があるまで従来の無料枠を維持するとされ、今後変わりうる。
  - NAVER は 2025-07-01 に旧 AI NAVER API の地図 API の無料枠を終了し、新しい Maps 商品へ移行した ([新 Maps 告知](https://www.ncloud.com/support/notice/all/1965))。料金体系は再び変わりうる。
  - 공간정보관리법 は 2026-03-05 改正、2026-07-01 施行の版を確認した。第16条第2項の協議体の構成機関は 2025-10-01 に改正されている。

## 出典

- https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B3%B5%EA%B0%84%EC%A0%95%EB%B3%B4%EC%9D%98%EA%B5%AC%EC%B6%95%EB%B0%8F%EA%B4%80%EB%A6%AC%EB%93%B1%EC%97%90%EA%B4%80%ED%95%9C%EB%B2%95%EB%A5%A0 (공간정보관리법、国家法令情報センター)
- https://www.korea.kr/news/policyNewsView.do?newsId=148960112 (정책브리핑 2026-02-27)
- https://www.upi.com/Top_News/World-News/2026/02/27/korea-Google-map-data-South-Korea-approval-high-precision/4641772177574/
- https://en.wikipedia.org/wiki/Restrictions_on_geographic_data_in_South_Korea
- https://www.etnews.com/20261028000277 (電子新聞 2026-10-28)
- https://www.ddaily.co.kr/page/view/2026102610060597667 (디지털데일리 2026-10-26)
- https://cloud.google.com/maps-platform/terms/maps-prohibited-territories
- https://www.ncloud.com/product/applicationService/maps
- https://guide.ncloud-docs.com/docs/maps-overview
- https://guide.ncloud-docs.com/docs/maps-spec
- https://www.ncloud.com/support/notice/all/1965
- https://guide.ncloud-docs.com/docs/en/userguide-userguideaccount
- https://developers.kakao.com/docs/ko/getting-started/quota
- https://devtalk.kakao.com/t/api-notice-on-new-kakao-map-api-features-and-free-quota-policy/150222
- https://developers.kakao.com/docs/ko/local/dev-guide
- https://apis.map.kakao.com/
- https://www.vworld.kr/dev/v4dv_dhapiguide_s001.do
- https://preview.esrikr.com/content/dam/distributor-share/esrikr-com/home/kr-techsupport-file/enterprise-attached-file/arcgis-vworld-25.pdf
- https://community.openstreetmap.org/t/osm/5177

## 未確認のこと

- 国土交通部・国土地理情報院の 2026-02-27 の報道資料の原文: 取得できず、政府の政策ポータル (korea.kr) の記事と報道で確認した。
- Google への 1:5,000 地図の実際の持ち出し開始と、韓国での経路案内の提供開始: 2026-11-10 時点で公式発表を見つけられなかった。
- 国境・地名の表記を定める規定と罰則: 該当する規定を特定できなかった。
- 世界測地系の楕円体などを定める大統領令の本文と、NAVER Maps の座標系の扱い: 本文を確認していない。
- NAVER Maps の超過単価: 料金表の金額がページ上で動的に描画され、取得できなかった。
- 外国法人が NAVER Cloud Platform の Maps を契約できるか、Kakao のビズウォレットを国外の法人・個人が使えるか: 公式の説明を見つけられなかった。NAVER の会員種別ガイドは本文を取得できず、検索結果の抜粋で確認した。
- VWorld の利用規約、商用条件、日次上限の数値、国外からの登録と接続: VWorld のサイトにこの調査環境から接続できなかった。国外からの接続制限によるものかは判別できていない。
- NAVER / Kakao のタイルを他社の描画ライブラリで直接読む提供形態の有無: 規約本文を確認していない。
- Mapbox の韓国での制約、OSM で韓国の政府地図をなぞることの適否、国外サービスと国内事業者の詳しさの定量比較: 公式の資料や信頼できる比較を見つけられなかった。
