# 航空機と船舶の位置 (ADS-B、AIS)

対象: 航空機の ADS-B と船舶の AIS を受信者の網で集め、API で配る出どころ (OpenSky Network、adsb.lol、ADS-B Exchange、aisstream.io、Global Fishing Watch) の利用条件と、公開の地図に出すときの注意

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 提供者 | OpenSky Network (スイスの非営利団体と説明される。公式の規約ページは読めず未確認)、adsb.lol (有志の OSS)、ADS-B Exchange (民間)、aisstream.io、Global Fishing Watch |
| 配布ページ | https://openskynetwork.github.io/opensky-api/ 、https://api.adsb.lol/docs 、https://www.adsbexchange.com/data-products/ 、https://aisstream.io/documentation 、https://globalfishingwatch.org/our-apis/documentation |
| 利用規約・ライセンス | 出どころごとに大きく違う (下の表)。adsb.lol は ODbL 1.0、Global Fishing Watch は CC BY-NC 4.0、OpenSky と ADS-B Exchange の無料の API は非商用、aisstream.io は規約の記載が見つからない |

## 概要

ADS-B (航空機) と AIS (船舶) は、機体や船が自分の位置と識別子を電波で周りに知らせる仕組みで、地上の受信者が受けた電波を集めると、生きた位置の地図が作れる。2026-11-11 の観察では、Flight Atlas と adsb.lol が航空機の位置をそのまま地図に出していた。出どころは受信者の網で、受信者のいない場所 (洋上、山間) は抜ける。データは数秒ごとに変わるので、主題データというより配信の設計 (map-compare-protocol、map-compare-arch) と組で決める。利用条件の差が大きく、非商用のものを商用の地図に使う誤りが起きやすい。

## 出どころごとの条件

| 出どころ | 種類 | ライセンス・商用 | API と制限 | 出典 |
|---|---|---|---|---|
| OpenSky Network | ADS-B | API の文書は「研究と非商用の目的」と書き、商用で生きた位置が要るなら連絡するよう案内する。出版物 (Web ページを含む) では 2014 年の OpenSky の論文を引くよう求める。規約本文 (opensky-network.org/about/terms-of-use) は 403 で読めず未確認 | OAuth2 の client credentials だけ (トークンは 30 分)。1 日のクレジットは匿名 400、登録 4,000、受信者を提供する人 8,000、ライセンス契約者は 1 時間に 14,400。`/states/all` は範囲の面積で 1〜4 クレジット。時間の分解能は匿名 10 秒、認証あり 5 秒。AWS などのクラウドからのアクセスを遮断することがあると書く | https://openskynetwork.github.io/opensky-api/ 、https://openskynetwork.github.io/opensky-api/rest.html |
| adsb.lol | ADS-B | API と公開データ全体が ODbL 1.0 (API の OpenAPI の info に明記。「OpenStreetMap と同じライセンス」とも書く)。過去のデータの GitHub (globe_history) も ODbL を掲げ、CC0 のファイルも並ぶが、どのファイルがどちらかは書かれていない | 今は無料で鍵なし。将来は受信データを送る人に鍵を出すと書く。本番で使うなら連絡するよう求める。制限は負荷で変わる。`/v2/point/{lat}/{lon}/{radius}` (250 海里まで)、`/v2/ladd`、`/v2/pia`、`/v2/mil` などがある | https://api.adsb.lol/api/openapi.json 、https://github.com/adsblol/globe_history_2025 、https://github.com/adsblol/api |
| ADS-B Exchange | ADS-B | 無料の Community API は「非商用」。個人向けは RapidAPI 経由で月 10 ドル、10,000 リクエスト。商用はデータ製品 (Live positions など) の年間契約で、料金はページに無い | 製品ページでは Live positions の更新を 5 秒、500ms、250ms から選ぶ | https://www.adsbexchange.com/community/developer-hub/ 、https://www.adsbexchange.com/data-products/ |
| aisstream.io | AIS | 無料。利用規約、商用、再配布、出典表示の記載はトップと文書のページに見当たらない (未確認) | GitHub でサインインして鍵を作る。IP ごとに接続 3 本、アカウントごとに購読 3 本、購読の更新は接続ごとに 1 秒 1 回。ブラウザからの直接接続は禁止で、自分のサーバーから中継する。SLA は無い。2026 年 9 月から非圧縮の接続に利用者ごとの帯域の上限をかけると書く | https://aisstream.io/ 、https://aisstream.io/documentation |
| Global Fishing Watch | AIS (と VMS) から作った船の活動のデータ | API は非商用だけで、CC BY-NC 4.0 に従う。Web や図には「Powered by Global Fishing Watch」とリンクを付ける | トークンが要る。1 日 50,000 リクエスト、1 か月 1,500,000 リクエスト (利用者ごと)。超えると 24 時間か 30 日止まる | https://globalfishingwatch.org/our-apis/documentation/docs/license-rate-limits |

## ライセンスと出典表示

- adsb.lol の ODbL: 位置を取り込んで自分のデータベースに貯め、公に使うなら、OSM と同じく派生データベースの共有義務がかかりうる。地図の画像だけを出すなら Produced Work として通知だけでよい。どちらかは [license-mixing](../license-mixing.md) の手順で決める。同じ地図で OSM のベースマップと重ねるのは、地物の種類が違う (航空機と道路) ので水平レイヤーとして分けられる (推測)。
- 非商用の出どころ (OpenSky の無料 API、ADS-B Exchange の Community API、Global Fishing Watch) は、広告や有料の機能がある地図、企業の社内用途に使わない。ADS-B Exchange は、売らない社内用途でも企業のプロジェクトなら商用のライセンスが要ると、ヘルプで答えている (検索結果の要約で見ただけで、本文は読んでいない)。
- 出典表示: OpenSky は論文の引用、Global Fishing Watch は「Powered by Global Fishing Watch」。adsb.lol は ODbL の表示 (出どころと ODbL へのリンク) を地図の隅に出す (推奨。adsb.lol の文例は見つからなかった)。

## プライバシーと、出してよいもの

- LADD と PIA (米国): LADD は、機体の所有者が FAA に頼んで、FAA のデータ系統から第三者の追跡サービスに渡る情報を絞る仕組み、PIA は所有者と結びつかない一時的な ICAO アドレスを使う仕組みと説明されている。LADD は FAA を通るデータにしか効かず、受信者が電波を直接受ける網には効かない、とも説明される。どれも NBAA などの業界団体の説明で、FAA のページ (https://www.faa.gov/pilots/ladd) は 403 で読めず未確認。
- 網ごとの扱い: adsb.lol の API には LADD の機体、PIA の機体、軍用機を一覧で返す口がある (`/v2/ladd`、`/v2/pia`、`/v2/mil`)。つまり受けた機体を隠さず出している。ADS-B Exchange は FAA のデータを使わないのでフィルターが無いと以前から説明されてきたが、今の公式ページでは確認できなかった (未確認)。
- 地図に出すときの推奨 (推測を含む): 公開の地図では、LADD や PIA の機体、個人の小型機を、識別子 (登録記号、ICAO アドレス) や所有者の情報と結びつけて出さない。機体の軌跡を日をまたいで貯めて個人の行動が分かる形で出さない。船も、漁船や個人のボートは同じ扱いにする。人の居場所が分かる情報は map-legal-check の位置情報の項で確かめる。
- 日本の電波法 第 59 条: 「何人も法律に別段の定めがある場合を除くほか、特定の相手方に対して行われる無線通信 ... を傍受してその存在若しくは内容を漏らし、又はこれを窃用してはならない。」ADS-B と AIS は周りの不特定の相手に送る放送型なので「特定の相手方に対して行われる無線通信」には当たらないと読むのが一般的だが、総務省の公式の説明は見つけていない (推測、未確認)。自分で受信者を立てて配るときは確かめる。

## 地図プロダクトでの使いどころ

- 空港や港の周りの生きた交通を見せる地図。範囲を絞って API のクレジットや帯域を節約する。
- 研究や報道で、ある日の航跡を見せる地図。非商用の条件と引用の求めを守る。

## 向いていない場面

- 商用のサービスで、無料の API をそのまま使うこと。商用の契約 (OpenSky、ADS-B Exchange) か、ODbL を受け入れて adsb.lol を使う。
- 受信者のいない海域や山間を網羅する用途。衛星 AIS などの商用データが要る (本調査では調べていない)。
- ブラウザから直接つなぐ作り (aisstream.io は禁止)。サーバーで受けて、間引いて配る。

## 出典

- https://openskynetwork.github.io/opensky-api/ : 研究と非商用、商用の連絡先、論文の引用、クラウドからのアクセスの遮断。
- https://openskynetwork.github.io/opensky-api/rest.html : クレジット、時間の分解能、OAuth2。
- https://api.adsb.lol/api/openapi.json : ODbL、利用の条件、エンドポイントの一覧 (OpenAPI の info と paths)。
- https://github.com/adsblol/globe_history_2025 : 過去のデータの ODbL と CC0 の表示。
- https://github.com/adsblol/api : 将来の鍵、負荷で変わる制限。
- https://www.adsbexchange.com/community/developer-hub/ : Community API の非商用、個人向けの料金。
- https://www.adsbexchange.com/data-products/ : 商用のデータ製品と更新間隔。
- https://aisstream.io/ と https://aisstream.io/documentation : 無料、鍵、接続の上限、ブラウザからの接続の禁止、SLA なし。
- https://globalfishingwatch.org/our-apis/documentation/docs/license-rate-limits : CC BY-NC 4.0、出典の文面、リクエストの上限。
- https://nbaa.org/aircraft-operations/security/privacy/limiting-aircraft-data-displayed-ladd/ : LADD と PIA の業界団体の説明 (検索結果の要約で見ただけ)。
- https://laws.e-gov.go.jp/law/325AC0000000131 : 電波法 第 59 条 (条文は e-Gov の法令 API で取得)。

## 未確認のこと

- OpenSky Network の規約本文 (非商用の範囲、営利企業の利用に書面の許可が要るか)。第三者の写しでは「営利企業の利用は書面の許可が要る」と書かれているが、公式ページを読めていない。
- aisstream.io の利用規約、商用利用と再配布の可否、出典表示。
- adsb.lol の出典表示の文例と、globe_history のファイルごとの ODbL と CC0 の区別。
- ADS-B Exchange の今のフィルターの方針と、商用ライセンスの料金。
- FAA の LADD と PIA の公式の説明。
- 日本で ADS-B と AIS を受信して公開することについての総務省の公式の説明。
- MarineTraffic、VesselFinder、Flightradar24、FlightAware などの商用の出どころ (本調査では調べていない)。
