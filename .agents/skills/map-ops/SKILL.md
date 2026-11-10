---
name: map-ops
description: 地図プロダクトを運用する。地図 API のキーの管理 (公開キー、Origin や referrer の制限、漏洩したときの対処、入れ替え)、利用量と予算の監視とアラート、地図データとタイルの更新の手順、提供元の障害時の切り替えを扱う。「API キーの制限をどうする」「地図 API の請求が急に増えた」「タイルの更新手順」「地図が出なくなったときの備え」と言われたら使う。
---

# map-ops

地図プロダクトを運用する。

> 骨組みの段階で、手順と reference はまだ書かれていない。このスキルを使うと決めたら、骨組みであることを答えに書き、reference の「[記入]」や空欄を事実として扱わない。判断は、書き上がったスキル (map-compare-arch、map-compare-infra、map-compare-library、map-compare-data、map-legal-check) と公式の文書で確かめられる範囲にとどめる。

後で書く。

| reference | 読むとき | 中身 |
|---|---|---|
| [api-key-management](references/api-key-management.md) | 地図 API のキーを発行・公開するとき | API キーの管理 |
| [usage-monitoring](references/usage-monitoring.md) | 利用量と費用を見張るとき | 利用量と予算の監視 |
| [data-update](references/data-update.md) | 地図データやタイルを更新するとき | データとタイルの更新 |
| [fallback](references/fallback.md) | 提供元の障害に備えるとき | 障害時の切り替え |

後で書く:

- 入力 (要件のうち、このスキルの判断を左右するもの)
- 進め方
- 出力の形
- 注意
