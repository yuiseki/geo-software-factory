# 地図 API のキーの管理

対象: ブラウザに置く公開キーの制限 (Origin、referrer、アプリの署名、API の種類)、提供元ごとにできる制限、漏洩したときの止め方、入れ替えの手順

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |

## 概要

ブラウザやアプリで地図を出すキーは、利用者の端末に必ず届くので秘密にできない。守る手段は、キーを隠すことではなく、使える場所 (Origin、referrer、アプリの識別子) と使える API を絞ること、上限と予算で被害の大きさを抑えること、漏れたら入れ替えられるようにしておくことである。どこまで絞れるかは提供元ごとに違い、referrer の検査は回避できる「最善努力」の対策と明記している提供元もある。

## 手段

| 手段 | 何が解決するか | 制約 | 対応するライブラリ・サービス (版) | 出典 |
|---|---|---|---|---|
| HTTP referrer / Origin の制限 | 他人のサイトに貼られたキーが使われるのを防ぐ | ブラウザが送るヘッダーに頼るので、サーバーやスクリプトからは偽装できる (推測)。`Referrer-Policy: no-referrer` や、referrer を消すブラウザ拡張で正規の利用者も弾かれる | Google (Websites 制限、ワイルドカードでサブドメイン可)、Mapbox (URL restrictions、1 トークン 100 件、ワイルドカードと IP 不可、GL JS 0.53.1 以降)、MapTiler (Allowed HTTP origins、`*.example.com` 可)、Esri (referrer URL、任意だが推奨)、HERE (Trusted domains、画面から 20 件、CLI で 1 アプリ 3,000 件、反映に最大 30 分)、Stadia (ドメイン認証。キー自体を置かない)、Geolonia (利用 URL の登録。スキーム、ホスト名、ポートのどれかが違えば別の値) | 下の出典 |
| アプリの識別子の制限 | モバイルアプリのキーを他のアプリで使わせない | 判定の仕組みは提供元ごとに違う | Google (Android はパッケージ名と SHA-1 署名証明書の指紋、iOS はバンドル ID)、MapTiler (User-Agent に含まれる部分文字列、大文字小文字を区別)。Mapbox は URL 制限がモバイル SDK で効かない。Esri、HERE、Stadia、Geolonia のモバイル向けの制限は未確認 | 下の出典 |
| IP アドレスの制限 | サーバー用のキーを他のサーバーで使わせない | 送信元の固定 IP が要る | Google (IP addresses) | Google のベストプラクティス |
| API の種類の制限 (スコープ) | 地図表示のキーで高い API (ジオコーディング、ルート、Places) を叩かせない | 地図表示に要る API を漏らすと地図が出なくなる | Google (API restrictions)、Mapbox (公開トークン `pk` は公開スコープだけ、`sk` はサーバー専用)、Esri (credential の privileges) | 下の出典 |
| 用途ごとにキーを分ける | 漏れたときに止める範囲を小さくし、どのアプリが急増したかを分けて見る | キーの数の上限 (MapTiler Free は 1 個、HERE は 1 アプリ 2 個) | 全提供元 | MapTiler、Mapbox、HERE の文書 |
| 入れ替え (rotation) | 漏れたキー、制限できないキーを止める | 古いキーを消すと、更新していない版のアプリの地図が止まる | Google (Rotate key で制限を引き継いだ新キーを作り、猶予期間は両方有効)、Mapbox (新しいトークンを作り、配備してから古いものを削除。削除は取り消せず、キャッシュに当たらない要求には即時に効く)、MapTiler (2〜3 か月ごとを目安、API keys Service API で自動化可)、Esri (1 credential に 2 個まで、キーは最長 1 年で失効、期限や権限を変えると全キーが無効になる)、HERE (1 アプリ 2 個で、2 個目を作って切り替え、古い方を削除)、Stadia (画面か Account Management API) | 下の出典 |
| 短命のトークン | 長く使えるキーを端末に置かない | トークンを発行するサーバーが要る | Mapbox (`tk` トークン、最長 1 時間)、Esri (OAuth のアクセストークン。詳しくは未確認)。認証の設計は map-compare-auth で扱う | Mapbox の Access tokens |

## 判断を左右すること

- 配布形態: Web だけなら Origin / referrer の制限で足りることが多い。ストア配布のアプリはキーがバイナリに入り、古い版が端末に残るので、入れ替えに数か月かかる前提で考える (推測)。
- 提供元がモバイルで識別子の制限を持つか: Google と MapTiler は持つ。Mapbox はモバイルで URL 制限が効かないので、スコープを絞った専用の公開トークンを分ける。
- 課金に上限があるか: 上限のない提供元 (Google の予算、Mapbox) では、キーの制限が漏洩時の唯一の歯止めになりやすい。上限は [usage-monitoring](usage-monitoring.md) で決める。
- 開発用と本番用: Mapbox は URL 制限をかけたトークンで localhost が弾かれるので、開発用に別のトークンを勧めている。Geolonia はデモキーで localhost やプレビュー環境に描画できる。

## 手順

1. 発行するキーを用途ごとに分ける: 本番 Web、ステージング、開発、Android、iOS、サーバー。1 つのキーを複数の用途で共有しない。
2. 各キーに、アプリケーションの制限を 1 種類 (referrer、IP、Android、iOS のどれか) と、使う API だけの制限をかける。Google はこの組み合わせを最善の方法としている。
3. referrer / Origin はスキームとポートまで含めて登録する (Google は全体の文字列、Geolonia は `http` と `https` を別に扱う)。本番、`www` あり / なし、ステージングのホストを漏らさない。
4. キーの所在 (どのリポジトリ、どの環境変数、どのアプリの版) を台帳にして、入れ替えのときに探さなくて済むようにする。サーバー用のキー (Mapbox の `sk` など) をリポジトリにコミットしない。
5. 漏れた、または不審な利用を見つけたら: (a) 利用量を見てどのキーかを特定する (Google は Metrics explorer で `credential_id` と `platform_type`)。(b) 制限で止められるなら先に制限を締める。(c) 止められなければ新しいキーを作って制限をかけ、アプリを配備し、利用が移ったことを確かめてから古いキーを消す。(d) 急ぐときは、更新していない版が止まるのを受け入れて古いキーを先に消す。
6. 入れ替えを定期の作業にする (MapTiler は 2〜3 か月ごとを目安とする)。Esri のキーは最長 1 年で失効するので、期限の前に入れ替えの予定を入れる。

## 落とし穴

- referrer の制限はブラウザのヘッダーに頼る。Mapbox は自社の制限を「best-effort mitigation」と書いている。上限と予算の監視と組み合わせる。
- `Referrer-Policy: no-referrer` や `same-origin` のページでは、Mapbox と Stadia の制限で正規の要求が 401 / 403 になる。
- Mapbox の URL 制限をかけたトークンは課金対象のサービスにしか使えない。既定のトークンには URL 制限もシークレットのスコープも付けられない。
- MapTiler で origin に `?` を入れると Origin ヘッダーの無い要求を通してしまう。
- MapTiler の User-Agent の制限は部分文字列の一致なので、ありふれた文字列にすると他のアプリも通る。
- Esri の credential は、期限や権限を変えるとそこから作った全キーが無効になる。運用中に設定を触ると地図が止まる。
- HERE の Trusted domains は反映に最大 30 分かかり、OAuth トークンには効かない。ドメインを 1 つも登録せずに有効にしても制限にならない。
- 消せないキーがある: MapTiler は、自分で入れ替えられないソフトウェアに入ったキーは自社のサポートに相談するよう書いている。アプリにキーを焼き込む前に、遠隔で差し替える手段 (設定の配信) を用意する (推測)。
- Google のキーの入れ替えの猶予期間の長さは公式ページに書かれていない。

## ライセンス上の注意

コピーレフト (GPL、LGPL、AGPL)、OSI 非承認、データの継承条件 (ODbL など) があるものは、組み込み、改変、配布、SaaS 提供のそれぞれで何が求められるかを書く。

- なし。キーの管理はライセンスではなく各提供元の規約の問題である。キーを他社に貸す、複数アカウントで無料枠に収めるなどは規約で禁じられることがある (Mapbox Product Terms 1.3。[providers/mapbox](../../map-compare-infra/references/providers/mapbox.md))。

## 出典

- https://developers.google.com/maps/api-security-best-practices (Google の制限の種類、API の制限、Rotate key と猶予期間、Metrics explorer での調べ方。2026-11-11)
- https://developers.google.com/maps/documentation/javascript/error-messages (RefererNotAllowedMapError、InvalidKeyMapError、OverQuotaMapError、BillingNotEnabledMapError。2026-11-11)
- https://docs.mapbox.com/accounts/guides/tokens/ (pk / sk / tk、URL 制限の件数と条件、モバイルで効かないこと、入れ替えと削除。2026-11-11)
- https://docs.maptiler.com/cloud/api/authentication-key/ (Allowed HTTP origins、User-Agent の制限、入れ替えの目安、漏洩時の手順。2026-11-11)
- https://developers.arcgis.com/documentation/security-and-authentication/api-key-authentication/ (最長 1 年、1 credential 2 個、referrer、期限や権限の変更で無効化。2026-11-11)
- https://docs.here.com/identity-and-access-management/docs/plat-using-apikeys (1 アプリ 2 個、Trusted domains 20 件、反映 30 分。2026-11-11)
- https://docs.stadiamaps.com/authentication/ (ドメイン認証、キーはブラウザ外用、入れ替え。2026-11-11)
- https://docs.geolonia.com/tutorials/embed/publish/ (利用 URL の登録とスキーム、ホスト名、ポートの扱い。2026-11-11)

## 未確認のこと

- Esri、HERE、Stadia、Geolonia Maps のキーを、モバイルアプリの識別子 (バンドル ID、パッケージ名) で制限できるか。
- Stadia の API キーに、ドメインや IP の制限をかけられるか (認証の文書に記載がない)。
- Geolonia Maps のキーの再発行や削除の手順、利用 URL のワイルドカードの可否 (公開文書に記載がない)。
- Google のキーの入れ替えの猶予期間の長さ。
- HERE の Trusted domains の上限が画面 20 件、CLI 3,000 件であることは KB とブログの検索結果に基づき、3,000 件の一次資料は開けなかった (KB のページが取得時に 404)。
