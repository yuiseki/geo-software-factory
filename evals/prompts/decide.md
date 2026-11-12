地図のプロダクトの技術の判断を頼みます。人間はいないので、質問せずに、自分で決めてください。

作業の場所は {{WORKDIR}} です。この中だけで作業し、外のものは読まないでください。Web の検索と公式の文書の閲覧はしてかまいません。

- 依頼: {{WORKDIR}}/task/README.md

{{#SKILLS}}
この場所には、地図のソフトウェアを作るためのスキルがあります。最初に {{WORKDIR}}/AGENTS.md を読み、{{WORKDIR}}/.agents/skills/ のうち関係しそうなスキルの SKILL.md と reference を開いてから判断してください。
{{/SKILLS}}

答えは {{WORKDIR}}/answer.json に、この形で書いてください。`constraints` には、依頼の候補の名前 (コロンの前の英字) だけを入れます。

```json
{"status": "ok", "constraints": ["...", "..."], "reason": "選んだ理由と、選ばなかった理由を短く"}
```

時間は {{MINUTES}} 分です。その時点で打ち切られ、answer.json だけが採点されます。
