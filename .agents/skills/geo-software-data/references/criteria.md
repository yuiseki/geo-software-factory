# 比較の軸 (主題データの出どころ)

地図に載せる主題データ (施設、建物、境界、住所、統計、災害リスクなど、ベースマップ以外) の出どころを同じ軸で並べるための手順。比較を始める前に読む。各出どころの事実は `sources/` と [license-mixing](license-mixing.md) にあり、この文書には軸と判定の手順だけを書く。例として挙げる事実は、各 reference に 2026-11-10 時点 (気象庁、航空機と船舶、AI で集めたデータは 2026-11-11 時点) で書かれていたもの。

## 進め方

1. 要件 (プロダクト概要の「表示するデータ」) から、要るデータを地物の種類ごとに分ける (例: 施設、建物、行政界、住所、人口、浸水想定区域)。出どころは地物の種類ごとに選ぶ。
2. 地物の種類ごとに、足切りの条件で候補を外す。足切りは「点数を下げる」ではなく「候補から外す」。
3. 残った候補を、評価の軸で比べる。軸の重みは「要件から軸の重みを決める」の表で決める。
4. 選んだ出どころを並べ、混ぜたときの条件を [license-mixing](license-mixing.md) で確かめる。
5. 推奨を先に書き、続けて地物の種類ごとの出どころと、出典表示の文面をまとめて示す。確かめられなかった項目は「未確認」のまま残し、推測で埋めない。

## 足切りの条件

| 条件 | 何を確かめるか | 外れる例 (各 reference の記述) |
|---|---|---|
| 商用利用と再配布 | 使う版の利用条件が、商用か、タイルやデータとして再配布するかに合うか | 国土数値情報の避難施設、市区町村役場 (P34)、郵便局、警察署、消防署、道の駅、緊急輸送道路は最新版でも非商用で再配布できない。学校は 2013 年度版だけ非商用。市町村役場等及び公的集会施設 (P05) は CC BY 4.0 ([ksj](sources/ksj.md))。自治体のデータには独自規約やライセンス未指定のものがある ([municipal-open-data](sources/municipal-open-data.md)) |
| 商用利用の制限 (生きた位置) | 無料の API が非商用に限られていないか | OpenSky Network の API、ADS-B Exchange の Community API、Global Fishing Watch (CC BY-NC 4.0) は非商用。adsb.lol は ODbL ([live-tracking](sources/live-tracking.md)) |
| 継承の条件 (シェアアライク) | 自社のデータと混ぜた結果を、同じライセンスで公開できるか | OSM と、OSM を含む Overture のテーマ (buildings、transportation、divisions、base) は ODbL。同じ種類の地物で自社のデータと突き合わせると、自社のデータにも共有義務が及びうる ([openstreetmap](sources/openstreetmap.md)、[overture-maps](sources/overture-maps.md)、[license-mixing](license-mixing.md)) |
| 法令上の手続 | ライセンスとは別に、手続が要るか | 基盤地図情報は基本測量成果に当たり、使い方によって測量法の承認が要る ([fgd](sources/fgd.md)、geo-software-legal-check の survey-act)。気象庁の予報や観測を補間や区域の変更で加工して出すと、気象業務法の予報業務許可が要りうる ([jma](sources/jma.md)) |
| 対象地域 | 対象地域を収録しているか | 国内の公的データは日本だけ。全球なら OSM、Overture |
| 安全に関わる情報の鮮度 | 古いデータを見せると危険がないか | 国土数値情報の避難施設は 2012 年度版が最新で、自治体の最新の指定とずれうる。避難場所は自治体のデータや国土地理院の指定緊急避難場所データで確かめる ([ksj](sources/ksj.md)) |

## 評価の軸

### 1. 収録範囲と網羅性

- 対象地域と地物の種類を、どこまで漏れなく持っているか。網羅率が公表されていないことが多い (Overture の日本の places、buildings、transportation は公式の網羅率が無い、[overture-maps](sources/overture-maps.md))。
- 地域による偏り: OSM は貢献者の数で密度が変わる。自治体のデータは公開している自治体にしか無い ([municipal-open-data](sources/municipal-open-data.md))。
- 例: OSM の日本の住所タグは建物数の約 1% で、住所の元には向かない ([openstreetmap](sources/openstreetmap.md))。

### 2. 詳しさと位置の精度

- 縮尺と精度: 基盤地図情報は都市計画区域が 1/2,500 相当、それ以外が 1/25,000 相当 ([fgd](sources/fgd.md))。アドレス・ベース・レジストリの代表点は縮尺が 500 から 25,000 まで違う ([abr](sources/abr.md))。
- 属性の豊かさ: 基盤地図情報は名前や属性をほとんど持たない幾何データ。POI には営業時間や種別が要るか。
- 形: 点か、区域のポリゴンか。アドレス・ベース・レジストリは代表点が中心でポリゴンは入っていない例がある ([abr](sources/abr.md))。

### 3. 鮮度と更新頻度

- 時点: 国勢調査の境界は 5 年ごと ([estat](sources/estat.md))。国土数値情報は項目ごとに時点が大きく違う ([ksj](sources/ksj.md))。
- 更新頻度: OSM の差分は分単位、Overture は毎月 ([openstreetmap](sources/openstreetmap.md)、[overture-maps](sources/overture-maps.md))。
- 過去の版の保存: Overture の公開リリースは 60 日で消えるので、再現が要るなら自分で保存する ([overture-maps](sources/overture-maps.md))。

### 4. 公的な裏付け

公共案件や行政との整合が要るなら、公的な出所 (国土数値情報、基盤地図情報、e-Stat、アドレス・ベース・レジストリ、自治体のデータ) を重く見る。ただし公的データにも、境界が行政上の町界と一致しない (e-Stat の境界、[estat](sources/estat.md))、境界が未確定の部分は暫定 (国土数値情報の行政区域、[ksj](sources/ksj.md)) などの限界がある。

### 5. 形式と取り込みの手間

- 配布形式: 基盤地図情報は GML だけで、登録とログインが要る ([fgd](sources/fgd.md))。e-Stat の境界は GeoJSON が無い ([estat](sources/estat.md))。Overture は GeoParquet ([overture-maps](sources/overture-maps.md))。
- 座標参照系: 版や行で混ざることがある。アドレス・ベース・レジストリの位置参照拡張は JGD2000 と JGD2011 が混在する例がある ([abr](sources/abr.md))。基盤地図情報は JGD2024 に変わり、改定前の標高と混ぜるとずれうる ([fgd](sources/fgd.md))。
- 集める手間: 自治体のデータは自治体ごとに列名や文字コードが違い、集める処理の保守が重くなる ([municipal-open-data](sources/municipal-open-data.md))。

### 6. ライセンスと出典表示の負担

- 出典表示の数: 出どころを増やすほど、地図の上に並べる出典が増える。CC BY 4.0、PDL1.0、政府標準利用規約 2.0 は互換で、出典と加工の表示を書けば混ぜやすい ([license-mixing](license-mixing.md))。
- 加工の表示: 国のデータを加工したら、加工したことと加工した主体を書き、国が作ったように見せない ([ksj](sources/ksj.md)、[estat](sources/estat.md)、[abr](sources/abr.md))。
- 公式見解の無い組み合わせ: ODbL のデータと CC BY や PDL のデータを 1 つのデータベースにする場合の扱いは、公的機関と OSMF のどちらの公式見解も見つかっていない ([license-mixing](license-mixing.md))。

### 7. 集め方と検証

- 人が確かめたデータか、AI や機械で集めたデータか。AI で集めた、確かめたデータは、根拠の URL、確かめた日、無作為の抜き取り検査の誤りの率があるものを重く見る。率が無ければ未確認として扱う ([ai-collected-data](ai-collected-data.md))。
- 公式の配布か、画面が内部で読んでいる非公開のエンドポイントか。気象庁のナウキャストのタイルや画面の JSON は仕様が公開されず、予告なく変わり、止まっても 200 を返すことがある ([jma](sources/jma.md))。

### 8. 識別子と結びつけやすさ

- 安定した ID: Overture の GERS ID はリリースをまたいで地物を対応づけられる (2025-06-25.0 より前の ID は使えない、[overture-maps](sources/overture-maps.md))。アドレス・ベース・レジストリの町字 ID、全国地方公共団体コード、e-Stat の KEY_CODE は、他のデータと結合する鍵になる。
- 自社のデータや統計と結合する予定があるなら、鍵の有無を重く見る。

## 要件から軸の重みを決める

| 要件 | 足切りに当てる条件 | 重くする軸 |
|---|---|---|
| 商用のプロダクト、データを再配布する | 商用利用と再配布、継承の条件 | ライセンスと出典表示の負担 |
| 自社のデータと同じ種類の地物を統合する | 継承の条件 | ライセンスと出典表示の負担、識別子 |
| 公共案件、行政の台帳との整合 | 法令上の手続 | 公的な裏付け、詳しさと位置の精度 |
| 防災、避難 | 安全に関わる情報の鮮度 | 鮮度と更新頻度、公的な裏付け |
| 全国で同じ質にそろえたい | 対象地域 | 収録範囲と網羅性、形式と取り込みの手間 |
| 特定の自治体の地図 | 商用利用と再配布 | 鮮度と更新頻度 (自治体のデータを優先) |
| 統計の主題図 (人口、事業所) | なし | 識別子 (KEY_CODE)、鮮度 |
| 住所の検索や正規化 | なし | 公的な裏付け、識別子 (町字 ID) |
| 全球、海外を含む | 対象地域 | 収録範囲と網羅性 |
| 生きた位置 (航空機、船舶) | 商用利用の制限 (生きた位置)、継承の条件 | ライセンスと出典表示の負担、鮮度と更新頻度 ([live-tracking](sources/live-tracking.md)) |
| AI で集めた、AI で確かめたデータを載せる | 継承の条件 (OSM を出発点にしたとき) | 集め方と検証 ([ai-collected-data](ai-collected-data.md)) |

## この文書で扱っていない出どころ

- 民間の POI データ (商用ライセンスのもの): reference で調べていない。国内の POI 検索 API は geo-software-infra の `search/` にある。
- 3D 都市モデル (PLATEAU) と衛星画像: geo-software-infra の `3d/` と `imagery/` にある。
- 登記所備付地図データ (地番の区域): アドレス・ベース・レジストリの地番系に重なる利用規約として名前だけ挙がっており、中身は調べていない ([abr](sources/abr.md))。
