# OldMapsOnline

- URL: https://www.oldmapsonline.org/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: OldMapsOnline、古地図、歴史地図、アーカイブ、MapTiler、Klokan、IIIF、ジオリファレンス、タイムライン

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中の図書館やアーカイブ機関が所蔵するデジタル古地図を、現代の地図や年代スライダーから横断検索して閲覧できるポータルサイト |
| 提供する価値 | 各地の機関に分散した数十万点の歴史地図を、場所 (バウンディングボックス) と年代で直感的に絞り込み、現代地図と重ね合わせて比較できる |
| 想定する利用者 | 歴史研究者、地理・郷土史愛好家、教育関係者、アーカイブ機関 |
| 商用か非商用か | 商用 (基本閲覧は無料のフリーミアムモデル。広告非表示・JPG 書き出し等の Friend プランが年額換算約 1.99 ドル/月、WMTS/IIIF/GeoTIFF 出力・プライベート地図アップロード等の Member プランが約 9.97 ドル/月) |
| 推定の売上 | 未確認 (OldMapsOnline 単体の売上は非公開。運営母体の Klokan Technologies / MapTiler 全体の推定年商は約 720 万ドル規模とされる) |
| 運営 | 企業 (Klokan Technologies GmbH / MapTiler、スイス) |
| 推定の運用費 | 未確認 (MapTiler の地図配信基盤および Georeferencer 処理・Cloudflare CDN の運用費) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapTiler SDK JS (WebGL ベース、タイムラインや 3D 地形・オーバーレイ表示に対応) |
| フレームワーク | 未確認 (`curl` でのアクセスは Cloudflare により HTTP 403 を返却) |
| 背景の地図とタイル | MapTiler のベースマップ、および世界中の連携図書館・David Rumsey Map Collection 等が提供する古地図タイル・IIIF 画像 |
| 投稿やデータの保存先 | Klokan Technologies / MapTiler クラウド (ジオリファレンス情報、お気に入り、有料会員のアップロード地図等) |
| 配信 | Cloudflare (`server: cloudflare`) |

メモ:

- 元々は英国の大学等との共同研究プロジェクトとして始まり、現在は MapTiler を展開する Klokan Technologies が基盤技術と運営を担っている。
- ジオリファレンス (古地図に緯度経度を付与する作業) をクラウドソーシングや専用ツールで行う仕組みと連携している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 歴史地図・古地図データ | 大英図書館、David Rumsey Map Collection、スイス連邦工科大学図書館など世界中の連携機関 | OldMapsOnline 公式サイトおよび Klokan Technologies 解説ページ |
| 料金・運営企業情報 | OldMapsOnline 料金ページおよび MapTiler 公式ブログ | 公開ウェブページ |
