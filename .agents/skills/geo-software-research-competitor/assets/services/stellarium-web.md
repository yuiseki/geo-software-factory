# Stellarium Web

- URL: https://stellarium-web.org
- ソース: https://github.com/Stellarium/stellarium-web-engine (AGPL-3.0 / 商用デュアルライセンス)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Stellarium Web、プラネタリウム、星図、天体観測、星座、WebGL、stellarium-web-engine、AGPL-3.0、Noctua Software

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ブラウザ上で肉眼・双眼鏡・望遠鏡で見えるリアルな星空や天体・人工衛星の位置をリアルタイムに再現するオンラインプラネタリウム |
| 提供する価値 | アプリをインストールせずとも、任意の観測地点・日時における 1 億個以上の恒星や深空天体、星座、惑星の動きを高精細な 3D 天球上で探索できる |
| 想定する利用者 | 天体観測・天文ファン、教育機関・学生、プラネタリウム・科学館、一般利用者 |
| 商用か非商用か | 商用 / OSS ハイブリッド (Web 版の基本機能は無料。運営元の Noctua Software はモバイル版有料プラン Stellarium Mobile Plus や商用エンジンライセンスを販売) |
| 推定の売上 | 非公開 (香港法人 Noctua Software Limited の売上は非公開だが、モバイルアプリの課金・買い切りおよびエンジン商用ライセンスで収益化) |
| 運営 | 企業 + コミュニティ (Stellarium Labs / Noctua Software Limited、香港。Stellarium オリジナル開発者の Fabien Chéreau 氏らが設立) |
| 推定の運用費 | 推測: 月数十万円規模 (静的フロントエンドの Cloudflare 配信および DigitalOcean Spaces 上の星表・HiPS 天体画像データ配信費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | `stellarium-web-engine` (WebGL / WebAssembly による独自天球・星図レンダリングエンジン) |
| フレームワーク | Vite バンドル (HTML で `assets/index-BKxynjLN.js` の読み込みを確認) |
| 背景の地図とタイル | HiPS (Hierarchical Progressive Surveys) 全天サーベイ画像・DSS・Gaia 星表データ |
| 投稿やデータの保存先 | DigitalOcean Spaces CDN (`stellarium.sfo2.cdn.digitaloceanspaces.com` からのアセット配信を確認) |
| 配信 | Cloudflare + DigitalOcean Spaces (`server: cloudflare` を応答ヘッダーで確認) |

メモ:

- ウェブ版のほか、共通エンジンを用いた公式の iOS / Android アプリ「Stellarium Mobile」および VR 版が提供されている。
- エンジン (`Stellarium/stellarium-web-engine`) は AGPL-3.0 と商用ライセンスのデュアルライセンスで公開されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 恒星・天体カタログ・全天画像 | Gaia 星表、DSS、SIMBAD、HiPS サーベイデータ等 | https://github.com/Stellarium/stellarium-web-engine |
