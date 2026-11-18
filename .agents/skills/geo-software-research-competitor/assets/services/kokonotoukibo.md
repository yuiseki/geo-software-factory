---
financial: commercial
organization: individual
---

# ここの登記簿

- URL: https://kokonotoukibo.jp/
- 観測した日: 2026-11-19
- 概要と収支を確かめた日: 2026-11-19
- 探すときの語: 登記簿、登記情報、公図、地積測量図、地番、法務局地図、不動産登記、登記の見守り、容積の余り

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 地図上で筆を選んで地番を確認し、法務局の登記情報 PDF・公図・地積測量図の取り寄せと Excel 自動集計、変更の見守りまで行えるサービス |
| 提供する価値 | 法務局の登記所備付地図と自治体の地番参考図を精度別に色分けして重ねた地図から複数筆をまとめて選び、24 時間注文できる (見つからなければ 0 円)。取得した登記 PDF は無料で Excel 一覧表に自動集計され、PLATEAU 由来の「容積の余り」表示や定期的な「登記の見守り」も使える |
| 想定する利用者 | 不動産業者 (売買・賃貸・管理・調査)、司法書士、土地家屋調査士、金融機関、不動産を調べる個人、月 100 筆以上を取得する法人 |
| 商用か非商用か | 商用 (無料会員制・従量課金。振込チャージ払いは登記情報提供サービスと同額: 全部事項 330 円、再利用 308 円、所有者事項 140 円、公図・地積測量図 360 円、見守り 430 円/240 円。カード払いは 343 円〜。広告なし、2026-11-19 観測) |
| 推定の売上 | 未確認 (利用件数・会員数は非公開。振込チャージ単価は登記情報提供サービス実費と同額水準のため、単体手数料の利幅は薄いかほぼ実費であり、再利用・見守り・法人利用等の付加価値を含めた収益設計と見られる) |
| 運営 | 個人事業 (ここの登記簿、代表者: 居初 一志、愛知県清須市、特定商取引法・プライバシーポリシー 2026-11-19) |
| 推定の運用費 | 推測: 月数千〜数万円。自前の nginx サーバーから PMTiles 静的ファイルと `/api/*` を配信し、Stripe 決済と登記情報提供サービスへの取次ぎを運用 |

## 技術 (2026-11-19 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS (`/out/vendor/maplibre-gl.js`、PMTiles `/out/vendor/pmtiles.js` 併用) |
| フレームワーク | 見つからなかった (静的 HTML + 素の JavaScript モジュール `/out/tsujou_an.js` 等) |
| 背景の地図とタイル | 地理院タイル (`cyberjapandata.gsi.go.jp/xyz/seamlessphoto`, `std`)、自前の PMTiles (地名・カバレッジ・市区町村別の筆ポリゴン・PLATEAU 由来の容積オーバーレイ) |
| 投稿やデータの保存先 | 自前の API (`/api/me`, `/api/config`, `/api/cities`, `/api/fude`, `/api/check`, `/api/saiyou`, `/api/mimamori`) |
| 配信 | nginx (HTTP `206 Partial Content` で PMTiles を直接配信、外部 CDN ヘッダなし) |

読み込んだタイルと API の URL (一部):

- `https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg`
- `https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png`
- `https://kokonotoukibo.jp/out/placed/chimei.pmtiles`
- `https://kokonotoukibo.jp/out/placed/_coverage.pmtiles`
- `https://kokonotoukibo.jp/out/%E5%90%8D%E5%8F%A4%E5%B1%8B%E5%B8%82_placed.pmtiles`
- `https://kokonotoukibo.jp/out/youseki/%E5%90%8D%E5%8F%A4%E5%B1%8B_%E5%AE%B9%E7%A9%8D5.pmtiles`
- `https://kokonotoukibo.jp/api/fude?c=23100&i=197624057012412`

メモ:

- 未登録でも地図・航空写真と筆の閲覧は無料 (法務局地図以外の地番表示は IP ごとに 1 日 100 筆、無料会員で 300 筆、1 件以上購入で 1,000 筆まで)。
- 取得できるのは法的証明力のない「登記情報 (PDF)」であり、登記事項証明書ではない旨が明記されている。
- 2026-12-01 から「登記情報の再利用」(308 円) や審査済み国内事業者向けの「名前の検索」の提供開始が案内されている。
