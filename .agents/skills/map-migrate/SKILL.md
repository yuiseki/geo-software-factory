---
name: map-migrate
description: 既存の地図プロダクトを、別の地図サービスやライブラリへ乗り換える計画を立てる。Google Maps Platform、Mapbox、Leaflet とラスタタイルからの移行で、API の対応、移行元のデータ (キャッシュ、プレイス ID、ジオコーディングの結果) の扱い、移行中の併用の可否、費用の変化、段階的な切り替えの手順を扱う。「Google Maps から乗り換えたい」「Mapbox の料金が高い」「Leaflet からベクトルタイルに移りたい」と言われたら使う。
---

# map-migrate

既存の地図プロダクトを、別の地図サービスやライブラリへ乗り換える計画を立てる。乗り換え先の選定は map-compare-infra と map-compare-library で行い、ここでは移行の計画を扱う。

> 骨組みの段階で、手順と reference はまだ書かれていない。このスキルを使うと決めたら、骨組みであることを答えに書き、reference の「[記入]」や空欄を事実として扱わない。判断は、書き上がったスキル (map-compare-arch、map-compare-infra、map-compare-library、map-compare-data、map-legal-check) と公式の文書で確かめられる範囲にとどめる。

後で書く。

| reference | 読むとき | 中身 |
|---|---|---|
| [from-google-maps](references/from-google-maps.md) | Google Maps Platform から移るとき | Google Maps Platform からの移行 |
| [from-mapbox](references/from-mapbox.md) | Mapbox から移るとき | Mapbox からの移行 |
| [from-leaflet-raster](references/from-leaflet-raster.md) | ラスタタイルと Leaflet から移るとき | Leaflet とラスタタイルからの移行 |
| [migration-plan](references/migration-plan.md) | どの移行でも、計画を立てるとき | 段階的な切り替えの手順 |

後で書く:

- 入力 (要件のうち、このスキルの判断を左右するもの)
- 進め方
- 出力の形
- 注意
