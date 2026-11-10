---
name: map-poc-measure
description: 地図プロダクトの技術選定で、推測ではなく試作して測る手順を組む。1 回の地図表示あたりのタイル数と転送量、表示回数の見積もり、データ (PMTiles、索引、グラフ) の大きさ、対象端末 (iOS、Android の WebView) での動作、描画の速さを測る。「タイルが何枚読まれるか測りたい」「月の表示回数を見積もりたい」「この端末で動くか確かめたい」「PoC を設計したい」と言われたら使う。
---

# map-poc-measure

技術選定で結論を左右する値を、試作して測る。

> 骨組みの段階で、手順と reference はまだ書かれていない。このスキルを使うと決めたら、骨組みであることを答えに書き、reference の「[記入]」や空欄を事実として扱わない。判断は、書き上がったスキル (map-compare-arch、map-compare-infra、map-compare-library、map-compare-data、map-legal-check) と公式の文書で確かめられる範囲にとどめる。

後で書く。

| reference | 読むとき | 中身 |
|---|---|---|
| [tiles-per-view](references/tiles-per-view.md) | 費用の見積もりに、1 回の表示あたりのリクエスト数が要るとき | 1 回の地図表示あたりのタイル数と転送量の測り方 |
| [map-load-estimation](references/map-load-estimation.md) | 表示回数を見積もるとき | 月間の地図表示回数の見積もり |
| [data-size](references/data-size.md) | データの大きさが置き場所を左右するとき | データの大きさの測り方 |
| [device-testing](references/device-testing.md) | 対象端末で動くか確かめるとき | 対象端末での確かめ方 |
| [render-performance](references/render-performance.md) | 描画の速さが要件に入るとき | 描画の速さの測り方 |

後で書く:

- 入力 (要件のうち、このスキルの判断を左右するもの)
- 進め方
- 出力の形
- 注意
