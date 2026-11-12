地図の作業を頼みます。人間はいないので、質問せずに、自分で決めて最後まで進めてください。

作業の場所は {{WORKDIR}} です。この中だけで作業し、外のものは読まないでください。

- 依頼: {{WORKDIR}}/task/README.md
- データ: {{WORKDIR}}/task/data.csv

背景地図のタイルは、https://tile.yuiseki.net/styles/osm-liberty/{z}/{x}/{y}.png (ラスタ、256 px) と、MapLibre GL JS 用のスタイル https://tile.yuiseki.net/styles/osm-liberty/style.json を使えます。OpenStreetMap の公開サーバー (tile.openstreetmap.org、nominatim.openstreetmap.org、overpass-api.de) は呼ばないでください。

{{#SKILLS}}
この場所には、地図のソフトウェアを作るためのスキルがあります。最初に {{WORKDIR}}/AGENTS.md を読み、{{WORKDIR}}/.agents/skills/ のうち関係しそうなスキルの SKILL.md を開いてから手順を決め、それに従ってください。
{{/SKILLS}}

作るもの:

- {{WORKDIR}}/out/places.geojson: 地点の GeoJSON (RFC 7946)。各地物の properties に、名前 (`name`) と出典 (`source`) を入れる。
- {{WORKDIR}}/out/index.html: 地点を背景地図の上に表示するページ。ライブラリは CDN から読んでよい。
- {{WORKDIR}}/answer.json: 終わったら `{"status": "ok"}` と書く。データから地点の位置を確かに決められないときは、作らずに `{"status": "failed", "reason": "..."}` と書く。誤った地図は、失敗の宣言より悪い。

時間は {{MINUTES}} 分です。その時点で打ち切られ、out/ と answer.json だけが採点されます。CPU のスレッドは 8 までにしてください。
