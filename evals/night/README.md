# evals/night: 一晩分を通しで流す

昼に決めたプロダクト概要とデータを渡し、実装者 (Codex) が人間なしで作り、別のコンテナの評価者が見せないシナリオで判定する。evals/ のほかの課題が 1 つの判断を測るのに対し、これは昼から夜への受け渡し、評価の依頼と症状の往復、最後のコミットの判定までを通して測る。

    python3 evals/night/run_night.py --condition skills|baseline [--minutes 45] [--subnet 10.213.57.0/24]

| 置き場所 | 中身 |
|---|---|
| `task/` | 実装者に渡すもの: プロダクト概要、データ (台東区の名所 12 件、平面直角座標系 第 IX 系)、夜の指示 |
| `scenarios/` | 評価者だけが持つ 5 本のシナリオと、評価者の側の確かめのスクリプト。`OBSERVED:` の行だけが実装者に届く |
| `reference/` | シナリオを確かめるための手本。`REF_BREAK=swap`、`osm`、`search` の 3 つの壊し方で、それぞれ別のシナリオが落ちる |
| `run_night.py` | 用意、隔離の確かめ、夜、最後の判定、要約 (`tmp/evals-night/<run>/summary.json`) |

- 隔離は geo-software-eval の [isolation](../../.agents/skills/geo-software-eval/references/isolation.md) の構成で、流す前に毎回確かめる。確かめが通らなければ、夜を始めない。
- Codex の認証は、`$EVAL_CODEX_HOME` (既定は `~/.codex-evals`) の `auth.json` だけを、その回のための空のホームに写し、終わったら消す。
- シナリオを直したら、手本が全部通り、壊した版がそれぞれ落ちることを確かめ直す。

    for v in none swap osm search; do PORT=18787 REF_BREAK=$v python3 evals/night/reference/serve.py & ...; done

- 結果は [results.md](../results.md) に書く。
- このリポジトリは公開なので、シナリオは Web で見つけられる。夜の実装者のログで、`evals/night` や公開の OSM のサーバーの名前が出ていないかを要約の `mentions` で見る (プロダクト概要の本文に出る分は除いて読む)。
