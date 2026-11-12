地図のプロダクトを作る前の調べものを頼みます。依頼した本人は今いないので、質問せずに進めてください。本人は朝にあなたの報告を読んで、進め方を選びます。

作業の場所は {{WORKDIR}} です。この中だけで作業し、外のファイルは読まないでください。Web の検索と、見つけたサービスを開くことはしてかまいません。

- 依頼: {{WORKDIR}}/task/README.md

{{#SKILLS}}
この場所には、地図のソフトウェアを作るためのスキルがあります。最初に {{WORKDIR}}/AGENTS.md を読み、{{WORKDIR}}/.agents/skills/ のうち関係しそうなスキルの SKILL.md と reference を開いてから進めてください。
{{/SKILLS}}

答えは {{WORKDIR}}/answer.json に、この形で書いてください。

```json
{"status": "ok",
 "services": [{"name": "...", "url": "...", "opened": true, "notes": "何ができて、何が足りないか"}],
 "alternatives": ["地図ではない代わりの手段 (1 行ずつ)"],
 "channels": [{"channel": "探した経路の名前", "query": "使った検索語"}],
 "recommendation": "A | B | C | D",
 "reason": "推奨の理由"}
```

`recommendation` は、本人に勧める進め方です。A 既存のものを使う、B 既存のものに貢献する、C 違いを決めて作る、D 学びや試作のために作る、のどれか 1 文字にします。決めるのは本人なので、推奨として書いてください。

時間は {{MINUTES}} 分です。その時点で打ち切られ、answer.json だけが採点されます。
