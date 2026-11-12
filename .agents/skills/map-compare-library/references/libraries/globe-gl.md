# globe.gl

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |
| 最新の安定版 (リリース日) | 2.46.2 (npm 公開 2026-08-22、JST)。GitHub Releases は使っておらず、版はタグと npm で出している ([npm](https://www.npmjs.com/package/globe.gl)、[タグ](https://github.com/vasturiano/globe.gl/tags)) |
| リポジトリ | https://github.com/vasturiano/globe.gl |
| ドキュメント | https://github.com/vasturiano/globe.gl#api-reference (README の API リファレンス)、例は https://vasturiano.github.io/globe.gl/ |
| ライセンス (LICENSE ファイルで確かめる) | MIT (Copyright (c) 2019 Vasco Asturiano) ([LICENSE](https://github.com/vasturiano/globe.gl/blob/master/LICENSE)) |
| 運営主体・ガバナンス | 個人 (Vasco Asturiano) のリポジトリ。財団や企業の運営ではない |

## 概要

three.js (WebGL) の上に作られた、3D の地球儀にデータ可視化レイヤーを重ねる Web コンポーネントである。three-globe プラグインを使いやすく包んだもので、点、弧、ポリゴン、経路、ヒートマップ、六角形集計、ラベル、HTML 要素、任意の three.js オブジェクトなどのレイヤーを持つ ([README](https://github.com/vasturiano/globe.gl))。道路や注記まで描く詳しい地図を見せる道具ではなく、全球規模のデータ (航路、人口、地震など) を見せる演出向けである (README の例の構成から判断)。

## 描画方式

- レンダリング (DOM / Canvas 2D / WebGL / WebGPU): WebGL (three.js の `WebGLRenderer`)。`rendererConfig` は `WebGLRenderer` のコンストラクタに渡される。HTML 要素レイヤーは DOM で重ねる ([README](https://github.com/vasturiano/globe.gl))。WebGPU への言及は README にない
- 2D / 2.5D (傾き・回転) / 3D: 3D のみ (球体をカメラで回して見る)。平面地図の表示はない ([README](https://github.com/vasturiano/globe.gl))
- 地球儀表示: 対応 (表示の前提そのもの)
- 対応する投影法: 球面への投影のみ。地球を包む画像 (`globeImageUrl`) と起伏の画像 (`bumpImageUrl`) は正距円筒図法 (equirectangular) の画像を求める ([README](https://github.com/vasturiano/globe.gl))

## 対応するデータ

| データ | 対応 | 備考 |
|---|---|---|
| ラスタタイル (XYZ) | 対応 | `globeTileEngineUrl(x, y, l)` に slippy map タイルの URL を返す関数を渡すと、タイルで地球儀表面を覆う ([README](https://github.com/vasturiano/globe.gl)、[Tiled Map Engine の例](https://vasturiano.github.io/globe.gl/example/tile-engine/)) |
| ベクトルタイル (MVT / PMTiles / MLT) | 非対応 | README に記述がない |
| スタイル仕様 (MapLibre/Mapbox Style 等) | 非対応 | README に記述がない。見た目は three.js のマテリアルとアクセサ関数で指定する |
| GeoJSON | 一部対応 | ポリゴンレイヤーと六角形化ポリゴンレイヤーが、各データの GeoJSON ジオメトリ (`type` と `coordinates`) を読む ([README](https://github.com/vasturiano/globe.gl))。FeatureCollection を丸ごと読み込む関数はなく、利用者が配列にして渡す。点や線は緯度経度のアクセサで渡す |
| 3D Tiles / glTF | 3D Tiles は非対応、glTF は three.js 経由で可 | 3D Objects レイヤーと Custom レイヤーは任意の three.js `Object3D` を受け取るので、three.js のローダーで読んだ glTF を置ける (推測。README は glTF を名指ししていない) |
| 地形 (標高タイル) | 非対応 | 起伏は `bumpImageUrl` のバンプマップ (見た目の陰影) で表すだけで、標高タイルからの形状生成はない ([README](https://github.com/vasturiano/globe.gl)) |
| WMS / WMTS | 未確認 | README に記述がない。XYZ 形式の URL で引けるなら `globeTileEngineUrl` で使える (推測) |

## 組み合わせの制約

- 使えない、または規約上使ってはならないタイルサービス: ライブラリ側の制約はない。`globeTileEngineUrl` で使うタイルは各配信元の規約に従う。Google の地図タイルは Google 以外の地図と併用できない (Google Maps Platform 利用規約 3.2.3(e)、[利用規約](https://cloud.google.com/maps-platform/terms))
- API キー・アカウントの要否: 不要 (ライブラリ自体)。使うタイル配信元が要求する場合はその配信元の条件に従う

## ライセンスと費用

- ライセンス: MIT ([LICENSE](https://github.com/vasturiano/globe.gl/blob/master/LICENSE))
- 利用料 (無料 / 従量 / 有料の機能): 無料
- 版によるライセンスの変化: なし

## 性能と規模

- バンドルサイズ (min+gzip、版と出典つき): 2.46.2 で 559,272 バイト ([bundlephobia globe.gl@2.46.2](https://bundlephobia.com/package/globe.gl@2.46.2))。three.js が peer 依存ではなく通常の依存 (`three: >=0.179 <1`) なので、この数値は three.js を含む ([npm](https://www.npmjs.com/package/globe.gl))
- 扱える地物の数の目安 (公式の記述か、測った条件つき): 公式の数値はない。点と六角形集計には、全メッシュを 1 つの three.js オブジェクトに統合して描画を速くする `pointsMerge` / `hexBinMerge` があるが、統合するとクリックやホバーが効かなくなる。曲面の分割解像度 (`*CurvatureResolution`) を細かくすると負荷が上がる ([README](https://github.com/vasturiano/globe.gl))
- 低性能端末・モバイルブラウザでの注意: 公式の記述はない。静止画で足りる場面では `pauseAnimation()` で描画ループを止めて負荷を下げられる ([README](https://github.com/vasturiano/globe.gl))

## エコシステム

- 主なプラグイン・拡張: 中核の three-globe (three.js のプラグイン、MIT) ([three-globe](https://github.com/vasturiano/three-globe))。AR 版の globe-ar、A-Frame 用の aframe-globe-component (1.19.1) が同じ作者から出ている ([README](https://github.com/vasturiano/globe.gl)、[npm aframe-globe-component](https://www.npmjs.com/package/aframe-globe-component))
- React / Vue などのラッパー: React 向けに同じ作者の react-globe.gl (2.38.0) ([react-globe.gl](https://github.com/vasturiano/react-globe.gl))。Vue の公式ラッパーは未確認
- TypeScript の型: 同梱 (`dist/globe.gl.d.ts`) ([package.json](https://github.com/vasturiano/globe.gl/blob/master/package.json))
- ネイティブ版・兄弟プロジェクト: ネイティブ版はない。兄弟は three-globe、react-globe.gl、globe-ar、aframe-globe-component
- 日本語の情報 (公式翻訳、国内コミュニティ): 公式の日本語訳はない (ドキュメントは英語の README のみ)。国内コミュニティは未確認

## 開発の活発さ

- 直近 1 年のリリース数: 6 (2025-11-10〜2026-11-10 に npm へ公開された版。2.45.1〜2.46.2。`npm view globe.gl time` で数えた)
- 最終コミット日: 2026-08-22 (master ブランチ、JST)。中核の three-globe は 2026-10-14 に push がある ([three-globe](https://github.com/vasturiano/three-globe))
- 近年の大きな破壊的変更: メジャー版は 2019-09 の 2.0.0 から 2.x のまま ([npm](https://www.npmjs.com/package/globe.gl))。CHANGELOG と GitHub Releases がないため、マイナー版での破壊的変更の有無は未確認

## 環境の違いと保守

- ブラウザ間の互換: 対応ブラウザを示した公式文書は未確認。リポジトリに `.github/workflows` がなく (GitHub API で 404、2026-11-12)、package.json にテストのスクリプトもない (https://github.com/vasturiano/globe.gl/blob/master/package.json)。CI での自動テストは行っていない。
- OS 間の互換: 対応 OS と端末、GPU の違い、メモリ上限への対応を述べた文書は未確認。描画は three.js (`>=0.179 <1`) に任せる (https://github.com/vasturiano/globe.gl/blob/master/package.json)。タイトルに mobile を含む issue は 11 件、iOS は 1 件である (GitHub の issue 検索、`repo:vasturiano/globe.gl` に各条件を付けて、2026-11-12)。
- 操作の網羅: カメラは three.js の OrbitControls (`controlType: 'orbit'`) で動かし、減衰による慣性 (`enableDamping`) を有効にし、平行移動を切り、地表の少し上から半径の 100 倍までに距離を制限する (https://github.com/vasturiano/globe.gl/blob/master/src/globe.js)。`controls()` で OrbitControls を取り出して設定を変えられる (同)。ピンチとキーボードの扱いは OrbitControls の既定に従う (推測)。`enablePointerInteraction` でマウスの追跡 (ホバーとクリックとツールチップ) を切り替え、`pauseAnimation` で描画と操作を止める (https://github.com/vasturiano/globe.gl/blob/master/README.md)。ページのスクロールと両立させる設定は未確認。
- エッジケースへの対応: 球の曲面を何度刻みで分割するかを `globeCurvatureResolution` で決める (https://github.com/vasturiano/globe.gl/blob/master/README.md)。日付変更線、精度、WebGL のコンテキスト喪失、読み込み失敗の扱いを述べた文書は未確認。
- 継続的な保守: CSP についての公式文書と変更履歴のファイルは未確認。three.js の版の上限 (`<1`) を package.json で管理している (https://github.com/vasturiano/globe.gl/blob/master/package.json)。ブラウザ別のラベルはなく、タイトルに Safari を含む issue は 1 件、Firefox は 0 件である (同 issue 検索)。

## 向いている場面

- 全球規模のデータ (航路、通信ケーブル、人口、地震、衛星など) を地球儀上で見せる展示・ランディングページ・ダッシュボードの演出
- 弧、リング、粒子などのアニメーションで流れや動きを見せたい場合
- three.js の知識を活かして独自の 3D 表現を足したい場合

## 向いていない場面

- 道路、建物、注記などを読む詳しい地図。ベクトルタイルとスタイル仕様に対応しない
- 都市・街区レベルまでズームして使う地図アプリ
- 平面地図や地球儀以外の投影法が要る場合
- 長期の保守体制 (複数の保守者、財団、企業) を重視する場合 (個人が保守する)

## 出典

- https://github.com/vasturiano/globe.gl
- https://github.com/vasturiano/globe.gl/blob/master/LICENSE
- https://github.com/vasturiano/globe.gl/blob/master/package.json
- https://github.com/vasturiano/globe.gl/tags
- https://vasturiano.github.io/globe.gl/
- https://vasturiano.github.io/globe.gl/example/tile-engine/
- https://github.com/vasturiano/three-globe
- https://github.com/vasturiano/react-globe.gl
- https://www.npmjs.com/package/globe.gl
- https://www.npmjs.com/package/aframe-globe-component
- https://bundlephobia.com/package/globe.gl@2.46.2
- https://cloud.google.com/maps-platform/terms

## 未確認のこと

- WMS / WMTS: README に記述がない
- glTF の読み込み: README は任意の three.js オブジェクトを置けるとだけ書き、glTF を名指ししていない。上の記述は推測
- 扱える地物の数とモバイルでの性能: 公式の記述がない
- マイナー版での破壊的変更: CHANGELOG と GitHub Releases がなく、コミット履歴を全て読むことはしていない
- Vue 向けラッパー、国内コミュニティ: 公式の案内が見つからなかった
