# Yahoo!不動産

- URL: https://realestate.yahoo.co.jp/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Yahoo!不動産、ヤフー不動産、不動産、賃貸、新築、中古、地図検索、Mapbox、LINEヤフー

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | LINE ヤフーが運営し、大手不動産ポータル各社の提携物件と地図検索・周辺環境情報をまとめて比較できる不動産情報サイト |
| 提供する価値 | 複数の提携不動産会社の物件情報を横断して地図上で比較でき、ベクタータイルによる滑らかな地図操作や Yahoo! JAPAN サービス群との連携が利用できる |
| 想定する利用者 | 賃貸・売買・新築物件を横断的に比較したい一般消費者、および物件情報を掲載・送客連携する不動産会社・ポータル事業者 |
| 商用か非商用か | 商用 (利用者は無料。不動産会社・提携先からの掲載課金・送客手数料・ディスプレイ広告で運営) |
| 推定の売上 | 未確認 (LINE ヤフー株式会社のメディア・コマース関連事業の一部であり、単体売上は非開示) |
| 運営 | 企業 (LINE ヤフー株式会社、東証プライム上場) |
| 推定の運用費 | 未確認 (提携物件データの統合基盤、Mapbox プラットフォーム利用料、自社オブジェクトストレージ「DragonStorage」等の配信基盤) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Mapbox (`https://realestate.yahoo.co.jp/rent/map/` が読み込む `client.*.js` 内に `mapbox` / `https://www.mapbox.com` の参照を確認) |
| フレームワーク | Next.js / React (トップページで `_next`、地図検索アプリ `client.vendor.*.js` 内で React を確認) |
| 背景の地図とタイル | Mapbox および OpenStreetMap (`client.*.js` 内に `https://www.mapbox.com`、`https://www.openstreetmap.org`、`https://map.yahoo.co.jp` への参照を確認。LINE ヤフーは旧 YOLP から Mapbox へ全面移行) |
| 投稿やデータの保存先 | LINE ヤフー自社基盤 (各提携不動産ポータル・不動産会社から連携される物件データ) |
| 配信 | Yahoo! JAPAN 自社配信基盤 (`realestate-map.east.edge.storage-yahoo.jp` にて `Server: DragonStorage` ヘッダーを確認) |

メモ:

- Yahoo! JAPAN 全体の地図基盤が自社 YOLP から Mapbox へ移行した流れに沿い、Yahoo!不動産の地図検索 (`https://realestate.yahoo.co.jp/rent/map/`) でも React と Mapbox を組み合わせたクライアントバンドルが使われている。
- 静的アセットは Yahoo! JAPAN のオブジェクトストレージ「DragonStorage」(`east.edge.storage-yahoo.jp`) から gzip 圧縮で配信されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 地図描画・タイル基盤 | Mapbox、OpenStreetMap contributors | `https://realestate.yahoo.co.jp/rent/map/` の JS バンドル (2026-11-16 観測) |
| フロントエンド・配信基盤 | Next.js / React、DragonStorage | `https://realestate.yahoo.co.jp/` および `storage-yahoo.jp` の HTTP 応答 (2026-11-16 観測) |
| YOLP から Mapbox への移行経緯 | LINE ヤフー / Mapbox Japan 公開事例 | Mapbox 公式事例および Yahoo! JAPAN 技術講演 |
