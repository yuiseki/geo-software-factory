# YouTube の埋め込みプレーヤーと YouTube API Services の規約

対象: 地図の上やポップアップに YouTube の動画やライブ配信を埋め込む (IFrame Player API を含む)、YouTube Data API で配信中かどうかや視聴者数を取って地図に出す場合の、YouTube API Services Terms of Service、Developer Policies、Required Minimum Functionality (RMF)、Branding Guidelines の条項

> 小節の番号について: YouTube API Services Developer Policies の小節番号 (III.D.1、III.F.2 など) の多くは、原文の見出しに番号が書かれておらず、本文中の相互参照 (III.E.4.b など) から推して付けたものである (推測)。引くときは番号ではなく見出しと本文で原文を確かめる。

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 根拠 (法令名と条、規約の版) | 法令ではなく YouTube との契約。YouTube API Services Terms of Service (以下 ToS)、YouTube API Services - Developer Policies (以下 Policies)、Required Minimum Functionality (以下 RMF)、Branding Guidelines。各ページの表示は「Last updated 2026-11-06 UTC」(ページの更新日で、条項の改定日とは限らない)。改訂履歴 (Revision History) の最新の項目は 2026-06-01 (Policies の III.L の更新)。RMF の埋め込みプレーヤーの識別の節は 2025-07-07 に追加。ToS 2.1 は、ToS、Policies、YouTube Guidelines (Branding Guidelines を含む)、認証情報、Google Software Principles、YouTube 利用規約を合わせて「Agreement」とし、2.4 で食い違えば ToS が優先するとする。25.13 で英語版だけが法的拘束力を持つ |
| 所管・管理者 | YouTube (Google)。改定は https://developers.google.com/youtube/terms/revision-history に載る (ToS 2.3) |

## 何を求める決まりか

目的は、YouTube の作り手、視聴者、権利者、広告主の利益を守ることにある (Policies 冒頭)。埋め込みは許されているが、再生の始まり方、プレーヤーの見え方、YouTube の帰属を YouTube が決めたとおりに保つことと、API で取ったデータを古いまま持ち続けたり別の指標に作り替えたりしないことを求める。義務の種類は契約上の禁止と表示で、事前の承認が要るのは一部 (プレーヤーの UI の変更、広告の販売など) だけである。

- 埋め込みプレーヤーも YouTube API Services に含まれる: Policies III.D.1 は認証情報の手順を持つサービスの例に「YouTube embedded player」を挙げ、III.D.2 は「IFrame Player API はユーザーの認可を要しない」とする。YouTube ヘルプの埋め込みのページも、埋め込みプレーヤーに ToS と Policies が適用されると書く (https://support.google.com/youtube/answer/171780 、2026-11-11 確認)。ToS 1 の「API Client」は YouTube API Services を使うウェブサイトやアプリを指す。このため、動画を埋め込むだけの地図サイトも API Client に当たると読める (条文の読み。推測を含む)。
- 利用規約とプライバシーポリシー (Policies III.A): API Client は YouTube 利用規約 (https://www.youtube.com/t/terms) へのリンクを表示し、自らの利用規約に「利用者は YouTube 利用規約に拘束される」と書く (III.A.1)。プライバシーポリシーは常に目立つ場所から読め、YouTube API Services を使っていること、Google プライバシーポリシー (http://www.google.com/policies/privacy) へのリンク、第三者に広告などの配信を許していればその旨、Cookie などで端末の情報を扱っていればその旨を書く (III.A.2)。ToS 7 も公開されたプライバシーポリシーを求める。
- 帰属とブランド (Policies III.F.2、ToS 10、11、Branding Guidelines): YouTube の内容 (検索結果、動画、チャンネル、サムネイル、プレーヤー) を出す画面では、YouTube が出どころであることを YouTube Brand Features で示す。複数の出どころが混ざる画面では、YouTube の分だけを個別に示し、全体に 1 つの帰属で済ませない。埋め込みプレーヤーの中の帰属を妨げたり隠したりしない (III.F.2)。著作権表示や作者の帰属、出どころの表示を消したり変えたりしない (ToS 11)。
- プレーヤーの大きさと自動再生 (RMF「Embedded YouTube Player size」「Autoplay and scripted playbacks」): 埋め込みプレーヤーの表示領域は 200px × 200px 以上。コントロールを出すなら、表示領域を最小より縮めずに全部見える大きさにする。16:9 なら 480 × 270px 以上を推奨。自動再生は、プレーヤーが見えていて半分を超えて見えるまで始めない。1 つの画面で同時に自動再生するプレーヤーは 1 つまで。再生を始めるサムネイルは幅 120px、高さ 70px 以上。
- プレーヤーを変えない (RMF「YouTube Player attributes」「Overlays and frames」「Mouseovers」、Policies III.I): API の文書に書かれていない変更をプレーヤーに加えない。プレーヤーとそのコントロールの前に、重ね表示、枠、その他の要素を置かず、隠さない。マウスオーバーやタッチでウィンドウを開くなどの操作を起こさない。プレーヤーの中のリンクを消したり隠したりしない、YouTube の広告を変えたり塞いだりしない、音声と映像を分けない、表示していない「バックグラウンドのプレーヤー」で再生しない、入れ子の iframe で出どころを隠さない (III.I)。プレーヤーの UI の変更は事前の書面の承認が要る (III.F.1)。
- 再生の公正 (Policies III.F.3): 埋め込みの視聴に料金を取らない、再生ボタン以外の操作 (チャンネル登録など) を視聴の条件にしない、視聴や高評価に報酬を出さない。
- プレーヤーの識別 (RMF「API Client Identity and Credentials」): 埋め込みプレーヤーを使う API Client は HTTP の Referer で自らを示す。Referrer-Policy で Referer を消さない (推奨は strict-origin-when-cross-origin)、window.open で noreferrer を使わない。アプリの WebView ではアプリ ID を Referer に入れる。要求の多い API Client には追加の認証情報が要ることがあり、守らないと埋め込みプレーヤーの機能が減ることがある。
- 動画そのものの保存 (Policies III.E.1): YouTube の事前の書面の承認なしに、動画の複製をダウンロード、取り込み、バックアップ、キャッシュ、保存しない。オフライン再生をさせない。ToS 16.3 は、YouTube API Services を通す以外の方法で動画を複製・配布する権利を与えないとする。
- API Data の保存と表示 (Policies III.E.4): 認可を要しないデータ (Non-Authorized Data。公開の動画やチャンネルの情報、視聴回数などの統計) は、必要な間だけ、30 日を超えない範囲で一時保存できる。30 日を過ぎたら消すか取り直す。認可なしに取った統計を 30 日を超えて保存してはならない (例: チャンネルの登録者数)。保存したデータは YouTube の現在の値と合うよう努め、画面には最新の値を出す。過去の値は時点を正しく示すなら出してよい。API Data を自前で計算した似た値に置き換えない、API Data から新しい指標を作らない。API Data でない値を並べるときは、YouTube のものでないことを目立つ形で示す。
- データの集約 (Policies III.E.2): 同じコンテンツオーナーのチャンネルに関するものを除き API Data を集約しない。API Data で YouTube の利用状況や収益などの洞察を得ない。
- スクレイピング (Policies III.E.6、III.I): YouTube のサイトをスクレイピングしない、スクレイピングした YouTube のデータを手に入れない。YouTube API Services 以外の技術で API Data を取らない。文書化されていない API を使わない (III.D)。
- 子ども向けの動画 (Policies III.E): 埋め込む動画ごとに Made For Kids かを調べ、該当する動画のプレーヤーでは追跡を切り、データの収集を COPPA や GDPR などに合わせる。サイト自体が子ども向けなら Google に申告する (III.J)。
- 埋め込みで送られる利用者の情報 (Policies III.E.4): ページを読み込んだ時点で、埋め込みプレーヤーを通じて基本的な利用者データが YouTube に送られ、再生時にさらに送られる。自動再生を有効にすると読み込み時に再生のデータも送られ、自動再生を切ると操作前に送る情報を減らせると書く。YouTube ヘルプは、埋め込みの URL を https://www.youtube-nocookie.com にするプライバシー強化モードで、その視聴を YouTube での表示や広告のパーソナライズに使わないとする (ウェブサイトの埋め込みに限る)。
- 利用量 (ToS 15、Policies III.D): YouTube は割当て (quota) を設け、超えたり回避したりしてはならない。YouTube Data API の既定の割当ては、search.list が 1 日 100 回、videos.insert が 1 日 100 回、その他のエンドポイントの合計が 1 日 10,000 ユニットで、変わりうる (Quota Calculator、Getting Started のページ、2026-11-11 確認)。videos.list は 1 回 1 ユニット。増やすには API Compliance Audit を通して申請する (Policies III.D)。プロジェクトが 90 日続けて使われないと割当てを減らされることがある。1 つの API Client に API Project は 1 つ (III.D.1.c)。
- 商用利用 (Policies III.G): 広告つきのサイトは許される (III.G.2)。ただし、YouTube の API Data がある画面で広告を売るのは、YouTube から得たもの以外の内容が同じ画面にあり、API Data を除いても広告の販売に見合う独立した価値がある場合に限る (III.G.1.d)。プレーヤーや動画の中に広告を載せて売るのは事前の書面の承認が要る (III.G.1.c)。
- YouTube の代わりを作らない (Policies III.I): YouTube のサービスの代わりや実質的に同じサービスを作らない。YouTube の閲覧体験を、大きな独自の価値を足さずに作り直さない。

## 地図プロダクトで当たる場面

| 場面 | 当たるか | 根拠 | 出典 |
|---|---|---|---|
| 世界地図に数千のライブ配信を点で置き、点を押すとポップアップで埋め込みプレーヤーを開く | 当たる。ポップアップのプレーヤーは 200 × 200px 以上、コントロールが全部見える大きさにする。ポップアップの閉じるボタンや地図の UI をプレーヤーの上に重ねない。点をサムネイルにして押すと再生が始まるなら、サムネイルは 120 × 70px 以上 | RMF の大きさ、自動再生、重ね表示の節 | https://developers.google.com/youtube/terms/required-minimum-functionality |
| 地図を動かして見えた範囲の配信を自動で再生する | 自動再生は 1 画面に同時に 1 つまで、プレーヤーの半分を超えて見えるまで始めない。複数のプレーヤーを並べて同時に流す形は当たる | RMF「Autoplay and scripted playbacks」 | 同上 |
| 配信が今ライブかを定期的に調べ、視聴者数を地図に出す | YouTube Data API で取るなら、取った値 (liveBroadcastContent、concurrentViewers など) は認可なしの API Data で、保存は 30 日以内、画面には最新の値を出す。視聴者数で点の大きさや順位を決めるのは表示の工夫で済むか、「新しい指標」に当たるかは条文から決められない (推測。下の「判断に迷う点」)。YouTube のページを読み取って配信中かを判定する方法はスクレイピングの禁止に当たる | Policies III.E.4、III.E.6、III.I | https://developers.google.com/youtube/terms/developer-policies |
| 配信の一覧 (動画 ID、タイトル、チャンネル名) を自社のデータベースや静的な JSON に持つ | タイトルやチャンネル名は API Data で、API で取ったなら 30 日以内に取り直すか消す。動画 ID の扱いを別に定めた条項は見当たらない (未確認) | Policies III.E.4 | 同上 |
| 全配信の視聴者数の合計や国別の合計を出す | 「API Data を集約しない」(III.E.2) に当たりうる。集約の範囲は条文から決められない (推測) | Policies III.E.2 | 同上 |
| 地図の横に AdSense などの広告を出す | 広告つきのサイトは許される。ただし API Data のある画面での広告の販売は、YouTube 以外の内容に独立した価値がある場合に限る。地図とその上の独自のデータが独立した価値に当たるかは書かれていない (推測) | Policies III.G.1.d、III.G.2 | 同上 |
| サイトの名前やロゴに YouTube や YT を入れる | 当たる。アプリ全体の名前に YouTube やその略語、変形を使えない。「works with YouTube」のような書き方は可 | Branding Guidelines「Requirements」 | https://developers.google.com/youtube/terms/branding-guidelines |
| 配信の音声だけを地図の背景音として流す、プレーヤーを画面外に置いて鳴らす | 当たる。音声と映像を分けること、表示していないプレーヤーでの再生は禁止 | Policies III.I | https://developers.google.com/youtube/terms/developer-policies |
| 埋め込みを含むページで、利用者の情報が YouTube (Google) に送られる | 電気通信事業法の外部送信規律に当たりうる。規約の側では、プライバシーポリシーに Cookie などの扱いと Google プライバシーポリシーへのリンクを書く | Policies III.A.2、III.E.4 | [external-transmission](external-transmission.md) |

## 当たらない場面

- 埋め込みプレーヤーだけを使う場合は、ユーザーの認可 (OAuth) は要らない (Policies III.D.2)。認可したデータ (Authorized Data) の削除や取り消しの規定 (III.D.2、III.E.3) は、ユーザーのアカウントに触れない地図では当たらないと読める (推測)。
- アップロードの画面の警告文 (ToS 9.1) は、利用者に動画をアップロードさせない地図では当たらない。
- 広告つきのウェブサイトやアプリを作ること、自社のブランドを置くこと (Branding Guidelines に従い、再生や YouTube のブランドを妨げない範囲) は許される (Policies III.G.2)。
- YouTube のロゴを使うのに特別な承認は要らない (Branding Guidelines 冒頭)。

## 求められる手続き・表示

- 手続き (申請先、期間、費用): 埋め込みだけなら申請は無い。YouTube Data API を使うなら Google Cloud のコンソールで API Project と認証情報を作る (Policies III.D.1)。既定の割当てを超えるなら API Compliance Audit と割当ての拡張の申請をする (III.D)。プレーヤーの UI の変更、プレーヤーや動画の中の広告の販売、動画の保存は事前の書面の承認が要る (III.F.1、III.G.1、III.E.1)。
- 表示の内容: YouTube 利用規約へのリンク、自社の利用規約での YouTube 利用規約への言及 (III.A.1)。プライバシーポリシー (III.A.2 の項目)。YouTube の内容の出どころを示す YouTube Brand Features (III.F.2)。
- 表示の書き方 (公式の例): Branding Guidelines は 3 種類を示す。アプリが YouTube の内容なしでは役に立たないなら「developed with YouTube」ロゴ (例として、動画の場所を地図に出して道案内するアプリを挙げる)、YouTube を外しても役に立つなら YouTube ロゴ、複数の出どころが混ざり個々の要素に帰属を付けるが場所が無いなら YouTube アイコン。ロゴは YouTube の内容のある場所の近くに置き、押すと YouTube の内容か YouTube の部分へ飛ぶようにする。ロゴを画面でいちばん目立つ要素にしない。色や形を変えない。最小の大きさは YouTube のブランドサイトの要件に従う (数値は本稿では未確認)。
- 公開の前に確かめること: (1) プレーヤーの大きさがどの端末幅でも 200 × 200px 以上か (地図のポップアップはスマートフォンで縮みやすい)、(2) 自動再生が同時に 1 つまでか、(3) プレーヤーの上に地図の UI や閉じるボタンが重なっていないか、(4) Referrer-Policy や noreferrer で Referer を消していないか、(5) API で取った値を 30 日を超えて持っていないか、取り直しの仕組みがあるか、(6) 配信中かの判定に YouTube のページを読み取っていないか、(7) 埋め込む動画の Made For Kids を調べているか、(8) 利用規約とプライバシーポリシーの記載、(9) 埋め込みを許可していない動画や年齢制限の動画は再生できない (YouTube ヘルプ) ので、そのときの表示を決めたか。

## 守らなかった場合

- YouTube は、API Client を予告なく監視・検査できる (ToS 6、Policies III.H)。ToS や Policies に反したり YouTube のコミュニティに悪い影響を与えたりすると、利用を制限・禁止しうる (ToS 冒頭)。YouTube は API の利用をいつでも停止・終了できる (ToS 24.2)。停止、終了、提供終了の通知を受けたら、直ちに利用をやめ、API Data を含む YouTube API Services を自社のサーバも含めて消す (ToS 24.3)。
- Referer による識別を守らないと、埋め込みプレーヤーの機能が減ることがある (RMF)。
- ブランドの使い方が Branding Guidelines に反すると、変更や使用の中止を求められうる (Branding Guidelines)。
- 準拠法はカリフォルニア州法 (ToS 25.11)。損害賠償と免責の条項 (ToS 19 から 21) は本稿では詳しく読んでいない。

## 判断に迷う点

- 地図の点の大きさや色を視聴者数で変える、配信を視聴者数の順に並べることが、「API Data から新しい指標を作る」(Policies III.E.4) に当たるか。表示の値そのものを変えずに並べるだけなら当たらないとも読めるが、公式の例は高評価の割合や独自のスコアを禁止の例に挙げるだけで、並べ替えや図示には触れていない (推測)。
- 「API Data を集約しない」(Policies III.E.2) の範囲。同じ条の例はコンテンツオーナーごとの分析データの集約で、多数のチャンネルの公開情報を 1 つの地図に並べることがこれに当たるかは書かれていない。合計値や国別の集計を出すと当たりうる (推測)。
- YouTube を外すと何も残らない地図 (配信を地図に並べるだけのサイト) が、YouTube の閲覧体験の作り直し (Policies III.I) に当たるか。地図という独自の価値が「significant independent value」に当たるかは YouTube の判断による (推測)。Branding Guidelines は動画の場所を地図に出すアプリを「developed with YouTube」の例に挙げており、この種のアプリ自体は想定されている。
- 動画 ID やチャンネル ID だけを長く保存すること。30 日の制限は API Data 一般にかかるが、ID を別に扱う条項は見つからなかった。ID は API を通さずに人手で集めたものでも、それで API を呼べば取ったデータは API Data になる (推測)。
- 埋め込みだけのサイトに III.A (利用規約へのリンク、プライバシーポリシー) が当たるか。API Client の定義と YouTube ヘルプの記述からは当たると読めるが、埋め込みだけの例を挙げた公式の記述は見つからなかった (推測)。

## 出典

- https://developers.google.com/youtube/terms/api-services-terms-of-service : ToS (1 定義、2 Agreement、7 プライバシー、9 通知、10 ブランドと帰属、11 権利表示、15 利用量、16.3、24 終了、25.11 準拠法、25.13 翻訳)。2026-11-11 確認
- https://developers.google.com/youtube/terms/developer-policies : Policies (III.A、III.D、III.E、III.F、III.G、III.H、III.I、III.J、III.L)。2026-11-11 確認
- https://developers.google.com/youtube/terms/required-minimum-functionality : RMF (識別、大きさ、自動再生、プレーヤーの属性、重ね表示、マウスオーバー)。2026-11-11 確認
- https://developers.google.com/youtube/terms/branding-guidelines : ロゴの 3 種類、地図アプリの例、置き場所とリンク、アプリ名の禁止。2026-11-11 確認
- https://developers.google.com/youtube/terms/revision-history : 改訂履歴 (最新 2026-06-01、RMF の識別の節は 2025-07-07)。2026-11-11 確認
- https://developers.google.com/youtube/player_parameters : 埋め込みのパラメータ。modestbranding は 2023-08-15 に廃止され効かない、rel=0 でも関連動画は消せない。2026-11-11 確認
- https://developers.google.com/youtube/iframe_api_reference : IFrame Player API、onAutoplayBlocked。2026-11-11 確認
- https://support.google.com/youtube/answer/171780 : 埋め込み、プライバシー強化モード (youtube-nocookie.com)、子ども向けサイトの申告、年齢制限の動画。2026-11-11 確認
- https://developers.google.com/youtube/v3/getting-started 、https://developers.google.com/youtube/v3/determine_quota_cost : 既定の割当てとメソッドごとのユニット。2026-11-11 確認
- https://developers.google.com/youtube/v3/docs/videos : liveBroadcastContent、liveStreamingDetails.concurrentViewers (配信者が視聴者数を隠していれば返らない、配信終了で追跡をやめる)。2026-11-11 確認

## 未確認のこと

- YouTube ロゴと YouTube アイコンの最小の大きさ (Branding Guidelines が参照する YouTube のブランドサイトの数値)。
- videos.list の id に 1 回で渡せる ID の上限。2,750 件の配信を何回の呼び出しで調べられるかは、この上限と割当てで決まる。
- YouTube 利用規約 (https://www.youtube.com/t/terms) のうち、埋め込みと視聴者側の利用に関わる条項。本稿は読んでいない。
- 日本の利用者に適用される ToS の地域版 (改訂履歴は Americas、APAC、EMEA、Russia の版を挙げる) と、本稿で読んだ版の差分。
- Policies III.L の「Additional policies on derived metrics and data storage」の中身 (監査を通った分析用途の開発者に限る)。
- oEmbed (https://www.youtube.com/oembed) でタイトルやサムネイルを取ることが「YouTube API Services」に当たるか。
