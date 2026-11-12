# evals: スキルの効きを測る

このディレクトリは、人間が、このリポジトリのスキルがコーディングエージェントを良くしているかを測るためのもの。同じエージェントに、スキルを渡したとき (skills) と渡さないとき (baseline) で、同じ課題を解かせて比べる。エージェントに渡す作業場所には入れない (`.gitattributes` の `export-ignore` と、`bench.py` の検査の両方で除く)。

作り方は、作者の GeoAI-master-skills と Geo-Ref-skills の evals に倣った。違うのは、このリポジトリの関心が「地理の分析」でも「ジオリファレンス」でもなく、「地図のソフトウェアを作り、技術を判断すること」である点。

## 何を見るか

- ギャップ: スキルなしで落ちて、スキルありで通ったこと。スキルの効き。
- 教科書: スキルなしでも通ること。モデルが既に知っている。人間向けの教科書として残し、削除の理由にしない。印を付けるだけ。
- 手間: 正解に届いても、かかった時間が違えば効きである。実行ごとに秒数を残す。
- 誤りの種類: 不合格の理由 (緯度経度の取り違え、投影座標のまま、帰属表示の欠け、選んだ制約の過不足) を、機械の判定の符号で残す。

## 課題

`bench.json` に置く。どれも、エージェントに流す前に書き、正解は作業場所に入らない。

| 課題 | 種類 | 何を試すか | 採点 |
|---|---|---|---|
| B1-taito-plane-ix | 作る | 平面直角座標系 (第 IX 系、X が北、Y が東) の CSV を、Web 地図の GeoJSON とページにする | geo-software-eval の geocheck、正解の点との 1 m 以内の一致、出典の属性、帰属表示 |
| N1-plane-unknown | 作る (陰性対照) | 座標系も場所も分からない CSV。決められないと宣言できるか | 失敗の宣言なら正しい拒否、地図を作ったら誤った受け入れ |
| D1-mobile-tiles | 判断 | モバイルで MapLibre Native、Mapbox のタイル、Google の衛星写真、オフラインという計画の、規約上の制約を候補から選ぶ | 正解の集合との一致 (適合率と再現率) |

課題の結果を見てスキルを直したら、その課題の `contaminated` に日付を入れ、以後その課題では効きを測らない。同じ種類の新しい課題を作る (場所、座標系、製品の組み合わせを変える)。直すのに使った課題で効果を測ると、効きを大きく見誤る。

## 採点の結果

| 結果 | 意味 |
|---|---|
| accurate | 機械の判定をすべて通った |
| inaccurate | 答えはあるが、判定のどれかに落ちた (理由の符号を添える) |
| declared_failure | 失敗を宣言した |
| correct_reject、false_accept | 陰性対照で、失敗を宣言した、地図を作った |
| invalid_answer | 読めない答え |
| no_answer、timeout | 答えが無い。時間切れのときは timeout (終了コード 124)。時間切れはエージェントの振る舞いとして数える |
| provider_error | 実行の道具が 0 と 124 以外で終わり、答えが無い。モデルの提供側の失敗なので採点に数えず、別の `--rep` で流し直す |

`public_osm` の欄は、ログに公開の OSM サーバーの URL が出たかを示す。指示文が名前を挙げて禁じているので、名前だけでは数えない。

## 流し方

リポジトリの根から。スキルありの作業場所は、コミット済みの版 (`--rev`、既定 HEAD) の `git archive` から作る。作業は `tmp/evals-bench/` (git に入らない) に書く。

```sh
docker build -f evals/Dockerfile.opencode -t geo-software-factory-evals-opencode evals
uv run --no-project --with pyproj python3 evals/bench.py make
EVAL_CPUSET=0-7  python3 evals/bench.py run --agent opencode --cond skills   --task B1-taito-plane-ix --minutes 20
EVAL_CPUSET=8-15 python3 evals/bench.py run --agent opencode --cond baseline --task B1-taito-plane-ix --minutes 20
python3 evals/bench.py score > tmp/evals-bench/results.tsv
```

Codex は `--agent codex` で流す (`run_codex_docker.sh`。認証は `~/.codex-evals` で、普段の `~/.codex` とは分ける)。

## 条件

- CPU 8、メモリ 16 GB (swap に逃げない)、プロセス 512、非 root、`--cap-drop=ALL`。上限は Docker で強制し、スキルあり、なしで同じにする。
- 作業場所だけを `/work` に載せる。元のリポジトリ、`evals/`、ホームは渡さない。
- 違ってよいのは、作業場所の中身 (リポジトリの有無) と、指示文の「スキルを読め」の段落だけ。
- ネットワークは開いている (CDN、自前のタイル、モデルの API)。公開の OSM のサーバーは指示文で禁じ、ログで確かめる。
- モデル、CLI の版、イメージは結果と一緒に記録する。

## 読むときの注意

- 1 回ずつの差は、偶然とスキルの効果を分けられない。同じ課題を繰り返す (`--rep`)。
- 無料のモデルは混むと止まる。提供側の失敗は数えず、流し直す。
- 機械の判定は、正しさの一部しか見ない。画面の見た目や操作は geo-software-eval のシナリオで別に見る。ここでの合格は、地図に載せるデータが正しく、出典と帰属表示があることまで。
- 結果は [results.md](results.md) に、版、モデル、日付と一緒に残す。
