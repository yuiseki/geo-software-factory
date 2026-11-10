# map-pdm-skills

地図サービスや地図プロダクトを開発・運用するための知見とノウハウを集めたエージェントスキル集。

> 骨組みの段階。各ファイルの「後で書く」を順に埋めていく。進み具合は [.agents/skills/TODO.md](.agents/skills/TODO.md)。

## スキル

| スキル | 使う場面 |
|---|---|
| [map-product-grilling](.agents/skills/map-product-grilling/SKILL.md) | 作りたい地図プロダクトの価値と機能が曖昧なとき、明確になるまで問い詰める |
| [map-compare-infra](.agents/skills/map-compare-infra/SKILL.md) | 地図タイルサービス (OSM, OpenFreeMap, Mapbox, Google Maps, Geolonia Maps, HERE, MapFan API など) と自前配信 (PMTiles など) を要件に照らして選ぶ |
| [map-compare-library](.agents/skills/map-compare-library/SKILL.md) | 地図ライブラリ (Leaflet, MapLibre GL JS, Mapbox GL JS, Google Maps JS API, CesiumJS など)、ネイティブアプリ向け SDK、複数 SDK の抽象化層 (MapConductor など) を要件に照らして選ぶ |

スキルの使い分けはエージェント向けに [AGENTS.md](AGENTS.md) に書く。

## 使い方

後で書く。

- Claude Code: `.claude/skills` は `.agents/skills` へのシンボリックリンク。リポジトリを開けばスキルが読まれる
- Codex / Gemini CLI / opencode など: 後で書く
- 他のリポジトリへの導入方法 (コピー、`npx skills add` 等): 後で書く

## ディレクトリ構成

```
AGENTS.md                 エージェント向け: どのスキルをいつ使うか
CLAUDE.md                 Claude Code 向け: AGENTS.md を読み込むだけ
.claude/skills -> ../.agents/skills
.agents/skills/
  AGENTS.md               スキルを書く人向けの決まり
  TODO.md                 執筆の進み具合
  map-product-grilling/
  map-compare-infra/
  map-compare-library/
```

## ライセンス

後で決める。
