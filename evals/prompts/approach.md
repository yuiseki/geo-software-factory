地図のプロダクトの作り方の判断を頼みます。依頼した本人は今いないので、質問せずに決めてください。

作業の場所は {{WORKDIR}} です。この中だけで作業し、外のファイルは読まないでください。Web の検索と、公式の文書やリポジトリの閲覧はしてかまいません。

- 依頼: {{WORKDIR}}/task/README.md

{{#SKILLS}}
この場所には、地図のソフトウェアを作るためのスキルがあります。最初に {{WORKDIR}}/AGENTS.md を読み、{{WORKDIR}}/.agents/skills/ のうち関係しそうなスキルの SKILL.md と reference を開いてから決めてください。
{{/SKILLS}}

答えは {{WORKDIR}}/answer.json に、この形で書いてください。`approach` は、汎用の地図ライブラリを使うなら `library`、依頼専用の描画器を自分で書くなら `full-scratch` のどちらかです。

```json
{"status": "ok",
 "approach": "library | full-scratch",
 "recommendation": "使うライブラリの名前か、書く描画器の概要",
 "recommendation_url": "ライブラリならその URL (full-scratch なら空でよい)",
 "caveats": ["その判断で気をつけること"],
 "reason": "選んだ理由と、選ばなかった方の理由"}
```

時間は {{MINUTES}} 分です。その時点で打ち切られ、answer.json だけが採点されます。
