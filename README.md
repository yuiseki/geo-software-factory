# geo-app-factory

地図サービスや地図プロダクトを開発・運用するための知見とノウハウを集めたエージェントスキル集。

> 骨組みの段階。各ファイルの「後で書く」を順に埋めていく。進み具合は [.agents/skills/TODO.md](.agents/skills/TODO.md)。

## スキル

| スキル | 使う場面 |
|---|---|
| [map-product-grilling](.agents/skills/map-product-grilling/SKILL.md) | 作りたい地図プロダクトの価値と機能が曖昧なとき、明確になるまで問い詰める |
| [map-compare-arch](.agents/skills/map-compare-arch/SKILL.md) | 保存・計算・表現を、クラウド、エッジ、ブラウザ/アプリのどこに置くかを機能ごとに決める (自前配信、ブラウザの API の活用を含む) |
| [map-compare-infra](.agents/skills/map-compare-infra/SKILL.md) | 地図タイルサービス (OSM, OpenFreeMap, Mapbox, Google Maps, Geolonia Maps, HERE, MapFan API など) を要件に照らして選ぶ |
| [map-compare-library](.agents/skills/map-compare-library/SKILL.md) | 地図ライブラリ (Leaflet, MapLibre GL JS, Mapbox GL JS, Google Maps JS API, CesiumJS など)、ネイティブアプリ向け SDK、複数 SDK の抽象化層 (MapConductor など) を要件に照らして選ぶ |
| [map-compare-data](.agents/skills/map-compare-data/SKILL.md) | 地図に載せる主題データ (OSM、Overture、国土数値情報、統計など) の出どころを選ぶ |
| [map-compare-auth](.agents/skills/map-compare-auth/SKILL.md) | 認証と認可の仕組み、タイルやデータへのアクセス制御を選ぶ |
| [map-compare-protocol](.agents/skills/map-compare-protocol/SKILL.md) | リアルタイムの配信と、地理空間の API の標準 (OGC API、WMS、NGSI-LD など) を選ぶ |
| [map-ux-design](.agents/skills/map-ux-design/SKILL.md) | 地図の UI と UX (大量の地物、検索、現在地、モバイル、アクセシビリティ) を設計する |
| [map-poc-measure](.agents/skills/map-poc-measure/SKILL.md) | タイル数、表示回数、データの大きさ、端末での動作を試作して測る |
| [map-legal-check](.agents/skills/map-legal-check/SKILL.md) | 公開の前に、帰属表示、ODbL、測量法、位置情報と個人情報、地図 API の規約を確かめる |
| [map-ops](.agents/skills/map-ops/SKILL.md) | API キー、利用量と予算、データの更新、障害時の切り替えを運用する |
| [map-migrate](.agents/skills/map-migrate/SKILL.md) | Google Maps、Mapbox、Leaflet などからの乗り換えを計画する |

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
  map-compare-arch/
  map-compare-infra/
  map-compare-library/
  map-compare-data/
  map-legal-check/
  map-ux-design/
  map-poc-measure/
  map-ops/
  map-compare-auth/
  map-compare-protocol/
  map-migrate/
```

## ライセンス

後で決める。
