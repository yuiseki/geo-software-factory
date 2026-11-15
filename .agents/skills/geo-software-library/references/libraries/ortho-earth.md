# Ortho Earth

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-16 |
| 最新の安定版 (リリース日) | `@ortho-earth/globe` 2.4.1 (npm、2026-11-11)。`@ortho-earth/cesium` 0.3.1 (同)、`@ortho-earth/japan` 2.0.2 (2026-10-19)。2.0 で 1.x の互換用の別名と内部の import のパスを外している (README、MIGRATION.md の存在) (https://www.npmjs.com/package/@ortho-earth/globe) |
| リポジトリ | https://github.com/kenjiyoshidahome2026-bit/ortho-earth |
| ドキュメント | https://www.ortho-earth.com/ (デモ、MapLibre の例との互換の一覧 /maplibre/、CesiumJS の例との比較 /sandcastle/、移行の手引き /docs/from-maplibre と /docs/from-cesium)。エージェント向けに llms.txt と MCP サーバー (`@ortho-earth/mcp`) がある |
| ライセンス (LICENSE ファイルで確かめる) | エンジン、SDK、アプリは GPL-3.0-or-later (リポジトリ直下の LICENSE は GPL-3.0 の全文。npm の `@ortho-earth/globe`、`cesium`、`japan` の `license` も GPL-3.0-or-later)。データ形式の道具 (geopbf、geoedit、altpbf、glbconv など) は MIT。データのパッケージ (world-data) は CC BY-SA 4.0。作者は GPL の義務を負えない場合のために商用ライセンスを別に出している (連絡先は README) |
| 運営主体・ガバナンス | 個人 (kenjiyoshidahome2026-bit)。README は、設計と実装を作者が行い、Claude と Gemini の協力を得たと書く。コミットは作者 3,346 件、claude の名義 1,518 件、ほか dependabot と外部 2 名 (GitHub の contributors、2026-11-16)。商用ライセンスを出すため、貢献者は最初の PR で CLA に署名する (CLA.md、`.github/workflows/cla.yml`) |

## 概要

ブラウザで動く、メルカトルの平面を持たない 3D の地球儀の地図エンジン。README は「MapLibre と Cesium から、メルカトルを引いたもの」と説明する。地図の初期状態から街路の縮尺まで、1 つの球の上の連続した視点で描き、平面の世界地図が要るときは Equal Earth (等積の図法) を使う。

- MapLibre GL JS の API を話す層 (`@ortho-earth/globe/maplibre`): style.json、式、ソース (MVT、MLT、PMTiles、GeoJSON、ラスタ、標高ラスタなど)、層の操作、マーカー、ポップアップ、コントロール、型定義。MapLibre のコードがそのまま地球儀の上で動くことを狙う。ただし `projection` は何と書いても地球儀として読む
- CesiumJS の名前を話す層 (`@ortho-earth/cesium`): Viewer、Camera、エンティティ、データソース、3D Tiles、ピッキングなど。描画しないものは Cesium の自前のコード、描画は Ortho Earth の地球儀
- 日本向けの同梱版 (`@ortho-earth/japan`): 同じエンジンと、日本の地域のデータ (国土地理院のベクトルタイル、標高、PLATEAU の建物、POI、検索)
- データ層の API (`addData`、H3 やセルのビン詰め、等値線)、解析 (日照と影、可視域、視線、断面、標高のサンプリング)、プラグインの仕組み、React のラッパー (`@ortho-earth/react`)

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): WebGPU を優先し、使えない、起動に失敗する、絵が出ないとエンジンが見分けられるときは WebGL2 に自動で切り替わる。`?gl2=1` と `?gpu=1` で強制もできる
- 2D / 2.5D (傾き・回転) / 3D: 3D の地球儀と地形、3D Tiles。傾きと回転を持つ
- 地球儀表示: 常に地球儀。メルカトルの平面に切り替える方法は無い (意図した設計。README の「Not built, on purpose」の項)
- 対応する投影法: 正射と透視が連続した球。WGS84 の楕円体は任意。平面は Equal Earth のみ

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | WMS、WMTS、COG も読む (README) |
| ベクトルタイル (MVT / PMTiles / MLT) | 対応 | MVT と MLT と PMTiles を読む (README) |
| スタイル仕様 (MapLibre/Mapbox Style 等) | MapLibre Style | 互換は公式の採点で、MapLibre の公式の例 137 のうち 91 が同じ絵、43 が同じ答え、3 が動くだけ。ただし 2.4.0 での作者の採点で、第三者の検証ではない |
| GeoJSON | 対応 | GeoParquet、FlatGeobuf、Shapefile、GeoPackage、KML、GPX なども (README) |
| 3D Tiles / glTF | 対応 | b3dm、i3dm、pnts、cmpt、glb、I3S、COPC の点群 |
| 地形 (標高タイル) | 対応 | 標高ラスタ、quantized-mesh |
| WMS / WMTS | 対応 | README |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリ側の禁止は見当たらない。タイルの供給元の規約 (他のライブラリや描画器での利用、キャッシュ) は供給元ごとに確かめる (geo-software-infra)。メルカトルのタイルを、地球儀の上に貼って表示することになる
- API キー・アカウントの要否: ライブラリは不要 (README)

## ライセンスと費用

- ライセンス: GPL-3.0-or-later (強いコピーレフト)。AGPL ではない。作者の README の読みは、「web ページに組み込むのは配布に当たり、そのページ自身の JavaScript も GPL で公開する必要がある」。ブラウザに送るライブラリなので、この読みは自然である (推測)。法的な判断は、必ず条文と専門家で確かめる
  - 組み込み (Web ページ、アプリ): 利用者に届く JavaScript 全体を、GPL-3.0 以降で公開できる必要がある
  - 改変: 改変した版は GPL で公開する
  - 配布: 受け取る側にソースと GPL の許諾を渡す
  - SaaS: GPL は配布の義務で、ネットワーク越しの提供だけでは働かないが、このライブラリはブラウザに送られて動くので、SaaS の画面が使う場合は配布に当たりうる (推測)
- 商用ライセンス: GPL の義務を負えない場合のために、作者が別に出している (価格と条件は未確認、README に連絡先)
- MIT の部分: データ形式の道具 (geopbf など) は MIT で、GPL の条件は付かない。エンジンの依存に入っている (下の「エコシステム」)
- 利用料 (無料 / 従量 / 有料の機能): GPL の義務を果たせば無料
- 版によるライセンスの変化: 未確認。1.x など過去の版のライセンスは確かめていない。選ぶ版の LICENSE と npm の `license` を確かめる

## 性能と規模

- 公式の測定の数字は、確かめていない (README は GPU の描画の特徴を述べるが、件数と端末つきの測定は読んでいない)。性能が結論を左右するなら、要件の件数で試作して測る
- 実機での確認の範囲 (README): macOS、Windows、iOS、iPadOS、Android 端末 1 台 (Mali-G615)。Android の機種によっては WebGPU で黒い下地の地図になることがあり、エンジンは検出できない (README の注意)

## エコシステム

- 主なプラグイン・拡張: `definePlugin` で拡張し `map.use` で入れる仕組み (データの種類、タイル形式、光、雲、後処理など)。deck.gl の `MapboxOverlay`、three.js のモジュールを同じカメラで載せられる (README)
- React / Vue などのラッパー: React (`@ortho-earth/react`)
- TypeScript の型: 同梱 (README の `maplibre.d.ts`)
- ネイティブ版・兄弟プロジェクト: ネイティブのモバイル SDK は作らないと明記。データ形式の変換の道具 (`geopbf` など、MIT) がある
- 日本語の情報 (公式翻訳、国内コミュニティ): README と文書は英語が中心。UI は 26 言語、一部の文書 (SECURITY.ja.md、MIGRATION.md) は日本語。日本向けの同梱版がある
- 依存: README は「実行時の依存ゼロ」とうたうが、npm の `@ortho-earth/globe` 2.4.1 の `dependencies` には 14 個ある (@loaders.gl の 5 つ、earcut、fzstd、geopbf、geoedit、native-bucket、同じ作者の core、ephem、h3、tile-formats)。README の「ゼロ」がどの範囲を指すか (束ねたあとのビルドなど) は確かめていない
- AI エージェントとの相性: llms.txt、llms-full.txt、facts.json、レシピの start.md、MCP サーバー、`map.supports()` と `map.capabilities()` (実装済みか、プラグインか、仕様だけ受けるかを返す) を用意している (README)

## 開発の活発さ

- 直近 1 年のリリース数: npm に 23 版 (1.0.0 の 2026-09-23 から 2.4.1 の 2026-11-11 まで、約 7 週間)。GitHub のリリースは 8 件
- 最終コミット日: 2026-11-15 (push)。リポジトリの作成は 2026-04-14
- 近年の大きな破壊的変更: 1.x から 2.0 で、互換用の別名と内部の import のパスを外した (MIGRATION.md、日本語)。短い期間に大きく変わる

## 環境の違いと保守

- ブラウザ間の互換: WebGPU のあるデスクトップの Chrome と Edge、macOS、iOS、iPadOS の Safari、Android の Chrome を対象にし、WebGPU が無ければ WebGL2 に切り替わる。Firefox は README の制限の節に出てこない (未確認)。影、環境遮蔽、クリップ面、大気の散乱、後処理の効果は WebGPU だけで、WebGL2 では出ない (地図そのものは同じ)。対応の確認ページ (https://www.ortho-earth.com/check/) があり、送信はしないと書く
- OS 間の互換: 未確認
- 操作の網羅: 地図の操作 (カメラ、マーカー、ポップアップ、コントロール) は MapLibre の API の再現として持つ。MapLibre の公式の例の約 3 分の 1 (137 のうち 46) と、Cesium の例の約 13 % (304 のうち 40) は、同じ絵にならない (README の自己採点。どれが違うかは /maplibre/ と /sandcastle/ にある)
- エッジケースへの対応: 未確認。CI のワークフローは test、release、publish、pages、deploy、mirror、cla の 7 つ (`.github/workflows`)。中身と、ブラウザごとの試験の有無は読んでいない
- 継続的な保守: 個人と AI の協力による開発。issue は 57 件、PR は 1,100 件 (GitHub の検索、2026-11-16、閉じたものを含む)。公開から約 7 か月で、星は 12。作者が続けられなくなったときに、GPL のコードを誰が引き継ぐかは決まっていない (推測)。バス係数は 1

## 向いている場面

- 地球儀そのものが主役の地図 (全球のデータ、衛星の軌道、地震の分布、国や大陸の比較) を、サーバーなしでブラウザに出したい場合
- メルカトルの歪みを避けたい (面積の比較を伴う主題図)。平面の世界地図は Equal Earth でよい場合
- MapLibre のコードや Cesium のコードを、書き直さずに地球儀の 3D に載せ替えたい場合。AI エージェントに MapLibre の書き方で書かせ、そのまま動かしたい場合
- 日本の 3D の地図 (国土地理院のベクトルタイル、PLATEAU の建物、標高) を、1 つのバンドルで出したい場合 (`@ortho-earth/japan`)
- プロダクト自体を GPL-3.0 以降で公開できる (OSS として出す) 場合

## 向いていない場面

- プロダクトのコードを公開できない、または受託で納品して権利を相手に渡す場合 (GPL の義務を負えない。商用ライセンスが要る)
- 平面のメルカトルの地図、または Web メルカトルの前提のライブラリや標準に合わせる必要がある場合 (切り替えられない)
- ネイティブのモバイルアプリ (SDK が無い。WebView で包む形になる)
- 長期の保守を任せる製品で、個人 1 人の開発とバス係数 1 を許容できない場合。1.x から 2.0 のように、大きく変わる期間が続くことも考慮する
- WebGPU の効果 (影、大気) を前提に見せたいが、利用者の端末が WebGL2 に落ちる場合

## 出典

- https://github.com/kenjiyoshidahome2026-bit/ortho-earth (README の概要、制限、ライセンスの節、LICENSE の存在、.github/workflows のファイル名。ソースのコードは読んでいない。2026-11-16)
- npm (`@ortho-earth/globe`、`cesium`、`japan`、`geopbf` の版、license、dependencies、公開の日時。2026-11-16)
- GitHub の API (リポジトリのメタ情報、contributors、issue と PR の数、リリースの数。2026-11-16)

## 未確認のこと

- 商用ライセンスの価格と条件
- 1.x のライセンス
- 性能の数字 (件数と端末つき)
- Firefox と、OS 間の互換
- CI の中身と、ブラウザごとの試験の有無
- README の「依存ゼロ」と、npm の依存 14 個の食い違いの意味
- MapLibre と Cesium の互換の採点の再現 (作者の自己採点で、第三者は未確認)
