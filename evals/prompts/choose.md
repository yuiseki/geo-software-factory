地図のプロダクトの技術の選定を頼みます。依頼した本人は今いないので、質問せずに決めてください。

作業の場所は {{WORKDIR}} です。この中だけで作業し、外のファイルは読まないでください。Web の検索と、公式の文書やリポジトリの閲覧はしてかまいません。

- 依頼: {{WORKDIR}}/task/README.md

{{#SKILLS}}
この場所には、地図のソフトウェアを作るためのスキルがあります。最初に {{WORKDIR}}/AGENTS.md を読み、{{WORKDIR}}/.agents/skills/ のうち関係しそうなスキルの SKILL.md と reference を開いてから決めてください。
{{/SKILLS}}

答えは {{WORKDIR}}/answer.json に、この形で書いてください。

```json
{"status": "ok",
 "recommendation": "勧めるライブラリや SDK の名前",
 "recommendation_url": "そのリポジトリか公式のページの URL",
 "alternatives": [{"name": "...", "url": "...", "why_not": "..."}],
 "caveats": ["勧めるうえでの注意 (成熟度、ライセンス、対応環境など)"],
 "reason": "選んだ理由"}
```

時間は {{MINUTES}} 分です。その時点で打ち切られ、answer.json だけが採点されます。
