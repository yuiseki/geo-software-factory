# LIFULL HOME'S

- URL: https://www.homes.co.jp/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: LIFULL HOME'S、ライフルホームズ、HOME'S、不動産、賃貸、売買、地図検索、ハザードマップ、物件マップ

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の賃貸・購入物件を地図や通勤時間・ハザードマップなどの条件と組み合わせて比較できる総合不動産・住宅情報サイト |
| 提供する価値 | 地図上で家賃相場や物件分布を俯瞰しながら検索でき、浸水・土砂災害などのハザード情報や周辺環境を同じ画面上で確認できる |
| 想定する利用者 | 賃貸・購入・投資用不動産を探す一般消費者、および集客・反響獲得を行う全国の不動産会社 |
| 商用か非商用か | 商用 (利用者は無料。不動産会社からの掲載課金、反響課金、広告収入で運営) |
| 推定の売上 | 約 255 億 3,000 万円 (親会社 LIFULL の 2025 年 9 月期「HOME'S関連事業」セグメント売上収益。連結売上収益は 281 億 2,700 万円) |
| 運営 | 企業 (株式会社 LIFULL、東証上場) |
| 推定の運用費 | 未確認 (全国数百万件規模の物件検索・画像配信、Google Maps API 利用料、CloudFront 配信基盤の運用) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`https://www.homes.co.jp/chintai/tokyo/map/` の HTML 内に `maps.googleapis.com/maps/api/js?language=ja&v=3.32&channel=v5_map` の読み込みを確認) |
| フレームワーク | 未確認 (地図検索ページでは独自バンドル `/search/assets/js/dist/route/pc/mapmain@*.js` 等を確認) |
| 背景の地図とタイル | Google Maps、および国土地理院タイル等 (`gsi.go.jp` への参照を地図検索ページ HTML 内で確認) |
| 投稿やデータの保存先 | LIFULL 自社基盤 (全国の提携不動産会社から入稿・連携される物件情報、独自に整備した街情報・相場データ) |
| 配信 | Amazon CloudFront (`via: ... cloudfront.net (CloudFront)`, `x-amz-cf-pop: NRT12-P2` ヘッダーを確認) |

メモ:

- 賃貸地図検索ページ (`https://www.homes.co.jp/chintai/tokyo/map/`) では Google Maps JavaScript API (`v=3.32`) を明示的に読み込んでいる。
- HTML 内に `gsi.go.jp` の記述があり、ハザードマップや地理院タイルとの連携・参照が行われている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 背景地図・ジオコーディング・検索 UI | Google Maps JavaScript API | `https://www.homes.co.jp/chintai/tokyo/map/` の HTML (2026-11-16 観測) |
| 防災・基盤地図情報 | 国土地理院 (`gsi.go.jp`) | `https://www.homes.co.jp/chintai/tokyo/map/` の HTML (2026-11-16 観測) |
| 売上・セグメント業績 | 株式会社 LIFULL 2025 年 9 月期決算短信 | LIFULL IR 資料 |
