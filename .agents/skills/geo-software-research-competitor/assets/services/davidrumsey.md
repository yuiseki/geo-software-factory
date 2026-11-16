# David Rumsey Map Collection

- URL: https://www.davidrumsey.com/ (ビューア: https://www.davidrumsey.com/luna/servlet)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: David Rumsey、古地図、歴史地図、デジタルアーカイブ、LUNA、IIIF、Stanford、Cartography Associates

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 16 世紀から 21 世紀の希少な地図・地図帳・地球儀 15 万点以上を高解像度で無償公開する世界最大級の私設歴史地図デジタルアーカイブ |
| 提供する価値 | 貴重な歴史地図の精細なズーム閲覧だけでなく、地図上の場所検索 (MapRank Search) や現代地図・3D 地球儀への重ね合わせ (Georeferencer)、IIIF 経由での再利用ができる |
| 想定する利用者 | 歴史学・地理学の研究者、教育者、地図デザイナー、古地図ファン |
| 商用か非商用か | 非商用 (公益・教育目的で全点無料公開。物理コレクションはスタンフォード大学へ寄贈され、オンライン版も課金壁なしで公開されている) |
| 推定の売上 | なし (公益・フィランソロピーに基づく無償公開プロジェクト) |
| 運営 | 企業・大学連携 (Cartography Associates がデジタル出版を管理し、物理資料はスタンフォード大学図書館 David Rumsey Map Center が収蔵。技術基盤は Luna Imaging 社が提供) |
| 推定の運用費 | 未確認 (高解像度画像 15 万点以上のストレージ、LUNA ソフトウェアおよび IIIF 画像サーバーの運用費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | LUNA Viewer (Luna Imaging 社)、Georeferencer (現代地図・3D 地球儀重畳)、IIIF Image API 対応 |
| フレームワーク | 未確認 (トップページ HTML では `importmap`、カスタムアセット、`globe` CSS 等を確認) |
| 背景の地図とタイル | 自社サーバーで配信する高解像度地図タイル・IIIF マニフェスト、および Georeferencer 用の現代地図ベースマップ |
| 投稿やデータの保存先 | LUNA デジタルアセット管理システム (Cartography Associates 管理) |
| 配信 | Apache/2.4.41 (Ubuntu) |

メモ:

- 1999 年からオンライン公開を開始した歴史地図デジタル化の先駆的事例。
- IIIF (International Image Interoperability Framework) に準拠しており、外部の IIIF ビューアや研究ツールから直接画像を呼び出せる。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 所蔵地図・地球儀コレクション | David Rumsey 氏収集資料 (スタンフォード大学図書館 David Rumsey Map Center 収蔵) | 公式サイトのコレクション解説および Wikipedia |
| プラットフォーム・IIIF 対応 | Luna Imaging (LUNA) および IIIF コンソーシアム事例紹介 | davidrumsey.com および iiif.io 公開情報 |
