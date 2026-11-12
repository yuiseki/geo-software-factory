---
name: geo-software-migrate
description: 既存の地図プロダクトを、別の地図サービスやライブラリへ乗り換える計画を立てる。Google Maps Platform、Mapbox、Leaflet とラスタタイルからの移行で、今の地図が使っているものの棚卸し、API の対応、移行元の規約で持ち越せないデータ (キャッシュ、プレイス ID、ジオコーディングの結果、Studio のスタイル) と併用の可否、費用の変化、段階的な切り替えと戻し方、移行後の見た目と機能の比べ方を扱う。「Google Maps から乗り換えたい」「Mapbox の料金が高い」「Mapbox GL JS から MapLibre に移りたい」「Leaflet からベクトルタイルに移りたい」「地図 SDK を入れ替える計画を立てて」と言われたら使う。
---

# geo-software-migrate

既存の地図プロダクトを、別の地図サービスやライブラリへ乗り換える計画を立てる。乗り換え先の選定は geo-software-infra (地図データ) と geo-software-library (ライブラリ) で行い、検索とルート検索の置き場所は geo-software-arch で決める。ここでは、今の地図の棚卸し、移行元の規約による制約、切り替えの段階と戻し方、移行後の比べ方を扱う。

| reference | 読むとき | 中身 |
|---|---|---|
| [from-google-maps](references/from-google-maps.md) | Google Maps Platform から移るとき | Google Maps JavaScript API、Places、Geocoding、Directions から MapLibre GL JS、OpenLayers、Leaflet などへの API の対応と、併用とデータの持ち越しの規約 |
| [from-mapbox](references/from-mapbox.md) | Mapbox から移るとき | Mapbox GL JS v1 / v2 以降から MapLibre GL JS への置き換え (パッケージ、トークン、`mapbox://`、スタイル仕様の違い、プラグイン) と、Studio のスタイルとタイルの規約 |
| [from-leaflet-raster](references/from-leaflet-raster.md) | ラスタタイルと Leaflet から移るとき | Leaflet に残してベクトルの層を足すか、MapLibre GL JS や OpenLayers に移るかの目安と、プラグインの対応 |
| [migration-plan](references/migration-plan.md) | どの移行でも、計画を立てるとき | 棚卸しの項目、機能フラグや段階的な公開、比較、戻し方、移行元を止める手順 |

## 入力

計画の前に、次のことをそろえる。プロダクト概要があればそこから読み、無ければ依頼から読み取る。

- 移行元: 地図のライブラリと版 (例: Mapbox GL JS 1.13 か 3.x か、Leaflet 1.9.4 か)、地図データの供給元、検索とルート検索の API
- 移行の理由: 費用、規約やライセンス、機能の不足、保守 (ライブラリの更新が止まった)、オフラインや閉域網への対応
- 対象端末と配布形態: Web、ネイティブアプリ、React Native、Flutter。SaaS、ストア配布、受託納品
- 規模: 月の地図表示回数、検索とルート検索の回数、モバイルなら MAU
- 保存しているデータ: キャッシュ、オフラインのタイル、DB に保存している座標や ID と、その出どころ
- 移行元の契約: 年間契約か従量か、更新日、解約の通知期限
- 期限と体制: いつまでに移すか、戻せる期間をどれだけ取れるか

移行元と移行の理由が分からないまま計画に入らない。この 2 つで読む reference と比べる軸が決まるので、分からなければ先に聞く。聞くときは選択肢で答えられる形にし、1 回に聞く数を絞る。移行先が決まっていなければ、計画の途中で geo-software-infra と geo-software-library を使って決める。

## 進め方

1. 棚卸しする。[migration-plan](references/migration-plan.md) の「手順」の 1 の項目 (描画、データ、保存、計測、費用と契約、表示) ごとに、今の地図が使っているものを書き出す。コードの検索 (`google.maps.`、`mapboxgl`、`mapbox://`、`L.`)、スタイル JSON、アクセスログ、請求書から数を取る。数が取れないものは推測で埋めず、取り方を書く。
2. 移行元の reference を開く ([from-google-maps](references/from-google-maps.md)、[from-mapbox](references/from-mapbox.md)、[from-leaflet-raster](references/from-leaflet-raster.md))。複数に当たるなら全部読む (例: Leaflet で Mapbox のラスタタイルを使っている)。
3. 移行元の規約で、持ち越せないものと併用できないものに印を付ける。代表的なもの:
   - Google: Google 以外の地図との併用禁止。Geocoding、Places、Directions のコンテンツを他社の地図に出せない。Google 由来の座標は移行先で使えないと読める。契約終了の日までにコンテンツを削除する
   - Mapbox: Studio のスタイルは Mapbox 以外の地図に使えない。タイルの書き出しと保存は禁止。モバイルアプリでは Mobile SDK が唯一のアクセス手段
   - ラスタタイル: 提供者ごとのキャッシュと併用の条項
   各条項は reference と [api-terms](../geo-software-legal-check/references/api-terms.md) から写し、答える前に規約の原文で確かめ直す。条文から読んだものと推測を分けて書く。
4. 移行先を決める。地図データは geo-software-infra、ライブラリは geo-software-library、検索とルート検索は geo-software-arch で選ぶ。移行元の規約が併用を禁じるなら、地図と検索を同じ段階で移す前提で選ぶ。移行先を決めたら、棚卸しの項目ごとに「そのまま」「置き換え」「やめる」を表にする。
5. 移行先の対応を確かめる。棚卸しの機能ごとに、移行先のライブラリとサービスで同じことができるかを、reference の対応表と geo-software-library の reference で確かめる。できないもの (例: Mapbox Standard の設定、ストリートビュー、Mapbox の投影法) は、代わりの表現か、やめるかを利用者に選んでもらう。
6. 費用を並べる。geo-software-infra の [criteria](../geo-software-infra/references/criteria.md) の「費用の見積もり方」で、今の規模と 1 年後の規模について新旧を同じ単位で並べる。移行の作業、両方に払う期間、Google 由来のデータの付け直しの費用も足す。単価は答える前に料金ページで確かめ直す。
7. 段階と戻し方を決める。[migration-plan](references/migration-plan.md) の「手段」から、移行元の規約が許す切り替えの単位 (画面ごと、利用者ごと、一斉) を選ぶ。各段階に進む条件と戻す条件、戻すときの操作を書く。移行元の API キーと契約は最後の段階まで止めない。
8. 同等であることの確かめ方を決める。代表的な場所とズームの見た目、検索の代表的な入力の結果、地図の読み込み時間、低性能の端末での動作、帰属表示を新旧で並べる項目にする。性能が結論を左右するなら、試作して測ることを勧める。
9. 帰属表示の変更と、公開の前の確認を計画に入れる ([attribution](../geo-software-legal-check/references/attribution.md)、geo-software-legal-check)。
10. 「出力」の形で答える。決めたことはプロダクト概要の「技術選定の結果」に書き足す。

## 出力

答えは次の順に並べる。

1. 推奨: 移行先 (地図データ、ライブラリ、検索、ルート検索) と、切り替えの単位を 2〜3 文で。移行しないほうがよい場合はそう書く。
2. 棚卸しの表: 行に今使っているもの、列に「数」「移行先」「そのまま / 置き換え / やめる」「根拠の reference」。
3. 規約の制約: 持ち越せないデータ、併用できない組み合わせ、移行元を止めるときに消すもの。条項の番号と、条文か推測かの区別をつける。
4. 費用の比較: 規模ごとの新旧の費用と計算式、移行の期間の重複の費用。
5. 段階の計画: 段階ごとの対象、進む条件、戻す条件と操作、期限。
6. 比べる項目: 見た目、検索、性能、帰属表示の比べ方。
7. 確かめた日と版: 規約、料金、ライブラリの版を確かめた日。確かめ直せなかった項目は reference の確認日。
8. 未確認のこと: 計画を左右するのに確かめられなかったこと。

## 注意

- 移行の計画を左右するのは、技術より移行元の規約であることが多い。併用の禁止とデータの持ち越しの禁止を、API の対応表より先に確かめる。
- ライブラリの版で API とライセンスが変わる (Mapbox GL JS は v1 系と v2 以降でライセンスが違い、MapLibre GL JS v6 は ESM のみで WebGL2 必須)。移行元と移行先の版を必ず書く。
- 移行先の見た目は、ライブラリでなく地図データとスタイルで決まる。「同じ見た目にする」は約束せず、何が変わるかを先に書く。
- 規約やライセンスの解釈は、条文から読んだものと推測を分けて書く。法的な判断を断定しない。
- 利害関係の開示: このスキル集の作者は、Geolonia Maps を提供する株式会社 Geolonia に関係している。Geolonia の製品やライブラリを特別扱いせず、候補に入れたときは開示を答えに添える。
