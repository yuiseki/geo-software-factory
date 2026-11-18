# スキルありの実行は文脈のどこに払っているか: 自動で読まれる AGENTS.md と、OpenCode の要約 (2026-11-18)

## 見たこと

`evals/results.md` の選定の課題 (D1、L3〜L7、F0〜F3) で、スキルありの実行がどれだけ読み、何を読んで答えたかを、各 CLI の会話の記録から数えた。道具は `evals/agent_trace.py`。

- スキルありの実行は、どのエージェントでも、どの回でも、答えの根拠になる reference を開いていた (L3 なら `libraries/geolonia-maps.md`、L4 なら `libraries/machgl.md`、L5 なら `libraries/ortho-earth.md`)。外した回 (Qoder の L4 の 2、3 回目、L5 の 2 回目など) も読んでいる。外れの原因は、情報にたどり着けないことではなく、読んだあとの判断の側にある。
- 手元の Qwen3.6-35B-A3B (OpenCode、文脈 32k) で L3 を 4 回流すと、4 回とも不合格だった。2 回は文脈があふれ、1 回は存在しない URL を書いた。原因は下の「OpenCode の要約が URL を落とした」。

## 数え方

モデルは呼び出しのたびに、それまでの会話の全部を読み直す。1 回の実行で読んだトークンは、呼び出しごとの文脈の大きさの和になる。最初の呼び出しの文脈 (システムの指示、道具の説明、課題の指示文、CLI が自動で読むファイル) を「決まった部分」と呼ぶ。

記録から取れるものは CLI ごとに違う。

| CLI | 取れるもの |
|---|---|
| OpenCode | 呼び出しごとのトークン (入力 + キャッシュ)。窓を超えた要求の大きさは stderr に出る |
| Gemini (Antigravity CLI) | 呼び出しごとのトークン (入力 + キャッシュ) |
| Qoder | トークンは 0 で記録される。窓に対する割合 (`context_usage_ratio`) だけ。Auto では窓の大きさが分からない |

## AGENTS.md は CLI が自動で読む

スキルありの作業場所には AGENTS.md がある。3 つの CLI とも、これを自動で文脈に入れていた。

| CLI | 決まった部分 (スキルなし) | 決まった部分 (スキルあり) |
|---|---|---|
| Gemini | 8.9 千 | 18.8 千 |
| Qoder | 窓の 10.2% | 窓の 16.8% |
| OpenCode + Qwen | 7.4 千 (AGENTS.md の無い場所での試走) | 20.5 千 |

Qwen の tokenizer で数えると、AGENTS.md は 7.8 千、課題の指示文は 0.3 千。OpenCode の 20.5 千から、試走の 7.4 千と、この 2 つを引いた残り約 5 千は、OpenCode の `skill` 道具に載るスキルの一覧と思われる (差から出した推測で、中身は確かめていない)。

指示文は「最初に AGENTS.md を読み」と頼んでいる。Gemini と Qoder は、ほとんど開き直さなかった (Gemini は 30 回中 3 回、Qoder は 31 回中 0 回)。OpenCode は 6 回中 5 回、自動で入っているものをもう一度開いた。Qwen の場合、これで同じ 7.8 千が 2 回入る。

Gemini では、スキルありの実行の読んだトークンは中央値で 102 万、スキルなしは 36 万 (2.8 倍)。呼び出しの回数は同じ (中央値 18.5 回)。差は、決まった部分が 2 倍になったことと、SKILL.md と reference を読んで文脈の山が 3.1 万から 7.3 万に上がったことから来る。

## 32k の窓には、要る分が入らない

L3 の答えに要るのは、AGENTS.md、`geo-software-library/SKILL.md`、`criteria.md`、`libraries/geolonia-maps.md`。Qwen の tokenizer で数えると次のとおり。

| もの | トークン |
|---|---:|
| 決まった部分 (AGENTS.md を含む) | 20,475 |
| SKILL.md | 4,927 |
| criteria.md | 3,714 |
| libraries/geolonia-maps.md | 9,348 |
| 計 | 38,464 |

決まった部分だけで窓の 62% を使い、要る分を足すと 32k を超える。並べて比べる reference (maplibre-gl-js.md 7.4 千、leaflet.md 5.7 千など) を読むと、なお超える。

## OpenCode の要約が URL を落とした

OpenCode は、文脈が窓からあふれそうになると、それまでの会話を要約し、要約から続ける (記録では `compaction` と、要約のあとの `compaction_continue` の合成メッセージ)。L3 の 1 回目では 3 回起きた。

1. SKILL.md を読んで文脈が 2.9 万になった直後に、1 回目の要約。
2. criteria.md と 4 つの reference をまとめて読んだあとに、2 回目の要約。
3. geolonia-maps.md を読み直して 3.2 万になったあとに、3 回目の要約。その直後に answer.json を書いた。

3 回目の要約には、パッケージ名 `@geolonia/maps-react` と版は残っていたが、reference にある npm の URL (`https://www.npmjs.com/package/@geolonia/maps-react`) は無かった。reference は、maps-react のリポジトリは公開されていないと書いている。答えの URL `https://github.com/geolonia/maps-sdk-react` は、要約のあとにモデルがこしらえたものである。

ほかの回:

- 2 回目は、4 万〜7.2 万トークンの要求を 7 回送って、サーバーに断られ (`exceeds the available context size`)、20 分の時間切れで終わった。採点の決まりでは「提供元の失敗」(AI_APICallError) に入り採点しないが、原因は提供元の障害ではなく手元の窓の大きさである。
- 3 回目は要約を 6 回はさみ、最後は MapLibre GL JS を選んだ。4 回目は 4 回、2 回目は 5 回。
- 4 回目は Geolonia を選んだが、answer.json の形が指示と違い (`recommendation` の代わりに `selection`)、URL の欄が無かった。指示文の形も、要約で落ちたと思われる (未確認)。

## 減らす手 (未確認)

- 指示文の「最初に AGENTS.md を読み」を外す。どの CLI も自動で読むので、OpenCode が開き直す 7.8 千が消える。ただし評価の指示文を変えるので、変える前と後を分けて流し、人間の承認を得てから行う。
- AGENTS.md を短くする。自動で読まれるので、どの CLI でも、どの呼び出しでも払う。課題に要らない節 (昼と夜の分け方、群れ、統治の層) は、技術選定の答えには使われない。
- 大きい reference を、答えに要る表 (版、URL、ライセンス、対応) と詳しい本文に分ける。geolonia-maps.md は 9.3 千で、L3 の答えに要る URL は先頭の表にある。
- 窓の小さいモデルを評価に入れるなら、窓を広げる (llama-server の `-c`) か、窓を記録とともに書く。32k では、スキルありの条件はモデルの賢さより先に窓で負ける。
- 変える変数は 1 つずつにする。

## 確かめ方

```sh
python3 evals/agent_trace.py                                   # 実行ごとの呼び出し数、決まった部分、山、読んだ和
python3 evals/agent_trace.py --task L3-react-geojson-concise --files   # 開いたスキルのファイル
python3 -m unittest discover -s evals -p 'test_*.py'
```
