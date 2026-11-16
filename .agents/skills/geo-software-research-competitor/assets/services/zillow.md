# Zillow

- URL: https://www.zillow.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Zillow、ジロウ、不動産、米国不動産、Zestimate、地図検索、Mapbox、学区、物件価格マップ

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 米国・カナダの住宅売買・賃貸物件と独自の推定査定価格「Zestimate」を、インタラクティブな地図上で検索・比較できる北米最大級の不動産プラットフォーム |
| 提供する価値 | 地図の移動・ズームに連動した数百万件の物件ピンや価格表示、学区・犯罪・災害・近隣境界レイヤの重ね合わせ、AI 査定額 Zestimate による相場把握 |
| 想定する利用者 | 米国・カナダで住宅の購入・売却・賃貸を検討する消費者、不動産エージェント、貸主、住宅ローン利用者 |
| 商用か非商用か | 商用 (一般利用者は無料。不動産エージェント向け送客・広告「Premier Agent」、賃貸掲載料、住宅ローン仲介等で収益化) |
| 推定の売上 | 約 25 億 8,300 万米ドル (Zillow Group 2025 年通期売上高。2024 年は 22 億米ドル) |
| 運営 | 企業 (Zillow Group, Inc.、米 NASDAQ 上場) |
| 推定の運用費 | 未確認 (MLS 等の不動産データベース統合、機械学習による査定基盤、大規模地図配信・CDN、3D ツアー処理基盤の運用) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (`curl -sL` で `https://www.zillow.com/` にアクセスしたところ CloudFront のボット防御により HTTP 403 が返却されたため直接観測不可。公開技術情報では WebGL ベースの Mapbox 等の採用が報告されている) |
| フレームワーク | 未確認 (HTTP 403 のため直接観測不可) |
| 背景の地図とタイル | 未確認 (公開資料・技術解説では Mapbox ベクタータイル、およびモバイルの過去事例では Google Maps API と独自ラスタータイルオーバーレイの併用が言及されている) |
| 投稿やデータの保存先 | Zillow Group 自社基盤 (全米の MLS 連携データ、公的登記データ、独自査定 Zestimate データ) |
| 配信 | Amazon CloudFront (`server: CloudFront`, `x-cache: LambdaGeneratedResponse from cloudfront` ヘッダーを確認。HTTP 403) |

メモ:

- 2026-11-16 時点の `curl -sL` による確認では CloudFront (`Lambda@Edge` とみられる `LambdaGeneratedResponse from cloudfront`) により `HTTP/2 403` が返却され、HTML/JS の直接取得はできなかった。
- Zillow Engineering ブログでは、過去には Android 版で Google Maps の `TileOverlays` を用いた境界描画を行っていたことや、近年は 3D Gaussian Splatting (3DGS) による物件外観の 3D 表現「SkyTour」等に取り組んでいることが公開されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 配信・WAF 応答 | Amazon CloudFront | `https://www.zillow.com/` の HTTP 応答ヘッダー (2026-11-16 観測) |
| 地図・3D 描画の技術解説 | Zillow Engineering ブログおよび公開技術資料 | Zillow Group 公式テックブログ |
| 年間売上高 | Zillow Group 2025 年通期決算 | Zillow Group IR 資料 |
