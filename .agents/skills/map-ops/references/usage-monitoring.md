# 地図 API の利用量と予算の監視

対象: 提供元ごとの利用量の見え方、予算アラート、上限 (クォータ) の設定、急増したときの調べ方

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

## 概要

地図 API の請求は、キーの漏洩、無限に再描画する不具合、クローラー、急な集客で桁が変わる。提供元によって、無料枠や上限に達したときに「止まる」ものと「課金が続く」ものがあり、予算アラートは多くの提供元で通知だけで止めない。運用では、提供元ごとに「止まる上限」と「知らせる閾値」の両方を置き、止まったときの見え方 (地図が出ない、警告が出る) を [fallback](fallback.md) とつなげておく。

## 手段

提供元ごとの上限と超過時の振る舞い。単価と無料枠の数字は map-compare-infra の provider の reference を見る。

| 提供元 | 利用量の見える場所 | 知らせる仕組み | 止める仕組み (ハードキャップ) | 無料枠や上限を超えたとき | 出典 |
|---|---|---|---|---|---|
| Google Maps Platform | Cloud console の Metrics explorer (キーごと、API ごと)、Cloud Billing。請求ダッシュボードは最大 48 時間遅れる | Cloud Billing の予算とアラート。予算は利用も請求も止めない | API ごとの 1 日あたりのクォータを下げる。上限に達するとその API の要求が失敗し、太平洋時間の 0 時に戻る。Maps JavaScript API は OverQuotaMapError | 従量で課金が続く (クォータを下げていなければ) | [providers/google-maps](../../map-compare-infra/references/providers/google-maps.md)、manage-costs |
| Mapbox | アカウントの Statistics と請求書 (画面の名前は未確認) | Usage notifications。サービスごとに月の閾値を複数置け、メールだけで、サービスは止めない。無料枠を初めて超えた月にもメールが来る | 支出上限は無い (「Mapbox accounts do not support a spending cap」)。前払いのクレジットを入れておき、使い切ったらトークンを入れ替えて止めるよう勧めている | 従量で課金が続く。支払いに失敗し未払いが続くとアカウントが無効になり、全トークンとサービスが止まる | [providers/mapbox](../../map-compare-infra/references/providers/mapbox.md)、Invoices の文書 |
| MapTiler Cloud | アカウントの Analytics タブ | 通知の機能は料金ページに書かれていない (未確認) | Flex は支出上限 (spending limit) を設定できる | Free は翌月まで止まる。Flex は超過分を月末に請求 | [providers/maptiler](../../map-compare-infra/references/providers/maptiler.md)、料金ページ |
| Esri ArcGIS Location Platform | usage ページのサービスごとのグラフ。請求の集計は UTC 2 時以降に確定 | 予算アラート、閾値通知は billing の文書に書かれていない (未確認) | 従量課金 (pay-as-you-go) を有効にしない。支払い上限の機能は文書に無い | 従量課金が無効なら、無料枠の無いサービスと、ホストしたデータのサービスが使えなくなり、帯域やタイル生成の超過は次の請求期間の始めに戻る。有効なら超過分を請求 | [providers/esri-arcgis-location-platform](../../map-compare-infra/references/providers/esri-arcgis-location-platform.md)、billing の文書 |
| HERE | ポータルの Usage ダッシュボードと請求のページ。請求書は毎月 15 日ごろ | Usage alerts (サービスごとの閾値でメール。KB の検索結果に基づく、本文は未確認) | 公式の支出上限は見つからなかった (未確認)。料金ページは「No daily transaction limits」 | 従量で課金が続く (推測: 上限の記載が無いため) | [providers/here](../../map-compare-infra/references/providers/here.md) |
| Stadia Maps | ダッシュボード (画面の名前は未確認) | 通知の機能は FAQ に書かれていない (未確認) | 既定でハードリミット。超過分の課金は opt-in | クレジットを使い切ると次の請求期間まで 429 を返す。pay-as-you-go を有効にすると超過分を次の請求書で課金。Free は超過分を買えない | [providers/stadia-maps](../../map-compare-infra/references/providers/stadia-maps.md)、FAQ |
| Geolonia Maps | ダッシュボード (未確認) | 利用上限に近づいたときの事前通知の機能は無い (FAQ) | Free は月 20,000 回で、上限に達すると地図上にアップグレードを促す表示が出る | Pro は 50,001 回目から従量課金で、上限の記載は無い | [providers/geolonia-maps](../../map-compare-infra/references/providers/geolonia-maps.md) |
| Cloudflare Workers / D1 (自前配信) | ダッシュボードの Workers と D1 の分析 | Free は課金されないので予算の通知は要らない。Paid の通知は未確認 | Free は 1 日 100,000 リクエスト (UTC 0 時に戻る)。D1 Free は 1 日の読み書きの行数 | Workers Free は Error 1027。ルートの fail mode が open なら Worker を飛ばして素通し、closed なら 1027 のエラーページ。D1 Free は UTC 0 時までエラー | [edge-functions](../../map-compare-arch/references/edge/edge-functions.md)、Workers limits |
| OpenFreeMap | 利用者側には見えない | 無し | 上限は公表されていない | 遮断の基準は示されていない | [providers/openfreemap](../../map-compare-infra/references/providers/openfreemap.md) |

## 判断を左右すること

- 無料枠を超えたら止めたいか、課金してでも出し続けたいか: 止めたいなら、上限で止まる提供元 (Stadia の既定、MapTiler Free、Geolonia Free、Workers Free) を選ぶか、Google のクォータ、MapTiler の支出上限を設定する。出し続けたいなら、通知の閾値を月の想定の 50%、80%、100% に置き、超過の単価を予算に入れる。
- 止まったときの見え方: Google はクォータ超過で地図が出なくなり、Geolonia Free は地図上に表示が出る、Stadia は 429 でタイルが欠ける。利用者にどう見せるかを [fallback](fallback.md) で決める。
- 請求の締めと集計の遅れ: Google の請求ダッシュボードは最大 48 時間、Esri は UTC 2 時まで確定しない。急増の検知には、請求ではなく利用量の指標 (Metrics explorer、usage のグラフ) を見る。
- 課金単位: 同じ利用でも、SDK を通すか直接タイルを取るかで地図ロード、MAU、タイル数と単位が変わる (リポジトリ直下の AGENTS.md の「段階どうしが制約し合うとき」)。閾値は課金単位で置く。

## 手順

1. 提供元ごとに、課金単位、無料枠、超過時の振る舞いを上の表と provider の reference で確かめ、公式の料金ページで確かめ直す。
2. 想定の月間利用量 (map-compare-infra の費用表の前提) から、月の閾値 (例: 50%、80%、100%、150%) を課金単位で決める。
3. 知らせる仕組みを置く: Google は Cloud Billing の予算、Mapbox は Usage notifications、HERE は Usage alerts。通知先はメールだけにせず、チームのチャンネルに転送する。
4. 止める仕組みを置く: Google は API ごとの 1 日のクォータを、普段の利用の数倍に下げる。MapTiler Flex は支出上限、Stadia は pay-as-you-go を有効にするかを決める。Mapbox は上限が無いので、前払いのクレジットと、閾値を超えたらトークンを止める手順を用意する。
5. 急増を見つけたら: (a) どのキー、どの API、どの platform からかを分ける (Google は `credential_id` と `platform_type`)。(b) 新しい版の配備と時刻が重なるなら、再描画やスタイルの再読み込みを繰り返す不具合を疑う。(c) 知らない Origin や IP からなら漏洩として [api-key-management](api-key-management.md) の手順で止める。(d) 正規の集客なら上限を上げるか、自前配信への移行を map-compare-arch で検討する。
6. 月に一度、請求書と利用量を突き合わせ、閾値と前提の表示回数を見直す。

## 落とし穴

- Google の予算は通知だけで、利用も請求も止めない。Google は「Setting a budget does not automatically cap」と明記している。
- クォータを上げると、上限が緩むだけで支出は減らない。低すぎるクォータは正規の利用者の地図も止める。
- Mapbox の Usage notifications は「never pause your service」で、通知は止めない。
- Esri は従量課金を有効にした後の支払い上限が文書に無い。
- Workers Free の上限超過は、ルートの fail mode が open だと Worker を素通しする。Worker で鍵の照合やアクセス制御をしているなら closed にする。
- 開発環境やテストの自動実行 (E2E テスト、スクリーンショットの生成) も本番のキーで数えられる。開発用のキーを分け、無料枠の中で数える (推測)。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- なし。複数アカウントで無料枠に収める行為は Mapbox の規約が禁じている ([providers/mapbox](../../map-compare-infra/references/providers/mapbox.md))。他の提供元でも規約を確かめる。

## 出典

- https://developers.google.com/maps/billing-and-pricing/manage-costs (予算は止めない、1 日のクォータでハードキャップ、太平洋時間 0 時に戻る、請求ダッシュボードは最大 48 時間遅れ。2026-11-11)
- https://developers.google.com/maps/api-security-best-practices (Metrics explorer の `credential_id` と `platform_type`。2026-11-11)
- https://developers.google.com/maps/documentation/javascript/error-messages (OverQuotaMapError。2026-11-11)
- https://docs.mapbox.com/accounts/guides/invoices/ (支出上限なし、Usage notifications、無料枠超過のメール、未払いでの無効化。2026-11-11)
- https://www.maptiler.com/cloud/pricing/ (Free は翌月まで停止、Flex の spending limit、Analytics タブ。2026-11-11)
- https://location.arcgis.com/help/billing/ (従量課金の有無による振る舞い、集計の確定時刻。2026-11-11)
- https://docs.here.com/identity-and-access-management/docs/plat-using-apikeys と HERE KB の検索結果 (Usage alerts、請求書の時期。KB の本文は取得時に 404 で、検索結果の抜粋に基づく。2026-11-11)
- https://stadiamaps.com/faqs/ と https://stadiamaps.com/pricing/ (既定のハードリミット、429、opt-in の超過課金。2026-11-11)
- https://developers.cloudflare.com/workers/platform/limits/ (1 日 100,000 リクエスト、Error 1027、fail open / closed。2026-11-11)

## 未確認のこと

- MapTiler、Esri、Stadia、Geolonia Maps に、利用量の閾値で知らせる機能があるか。
- HERE の Usage alerts の詳細と、支出上限の有無 (KB の本文を開けなかった)。
- Mapbox の利用量の画面の正式な名前。
- Stadia の 429 が、pay-as-you-go を有効にしていない有料プランでも同じか (FAQ の文脈は無料枠と試用期間)。
- Cloudflare Workers Paid の利用量の通知 (Billing の通知の機能)。
