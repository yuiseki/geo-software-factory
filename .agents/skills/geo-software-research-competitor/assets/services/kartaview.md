# KartaView

- URL: https://kartaview.org/
- ソース: https://github.com/kartaview/openstreetcam.org (ウェブフロントエンド、TypeScript)、https://github.com/kartaview/ (Android、iOS、upload-scripts、josm-plugin 等を公開)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: KartaView、OpenStreetCam、ストリートビュー、道路写真、街路画像、OSM、Grab、GrabMaps、車載カメラ

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | スマートフォンや車載カメラで撮影した道路の写真と走行データをクラウドソーシングで集め、OpenStreetMap の編集や道路情報の抽出に使えるようにする街路画像プラットフォーム |
| 提供する価値 | 誰でも無料で街路画像を閲覧・アップロードでき、CC-BY-SA ライセンスの下で OSM マッパーが道路標識や車線、施設を地図化する際の現地確認資料として利用できる |
| 想定する利用者 | OpenStreetMap のマッパー、道路データを整備したい自治体や開発者、GrabMaps のドライバーパートナーおよび調査チーム |
| 商用か非商用か | 非商用と見られる (利用は無料、投稿画像は CC-BY-SA で公開。ただし運営母体の Grab は収集データや技術基盤を自社の商用サービス GrabMaps や AWS 経由の地図提供に活用している) |
| 推定の売上 | 未確認 (Grab の地図事業 GrabMaps の一部として運用されており、KartaView 単体の売上は公表されていない) |
| 運営 | 企業 (Grab Holdings Limited。旧名 OpenStreetCam、2019 年 12 月に Telenav から Grab が買収) |
| 推定の運用費 | 未確認 (世界中の大量の街路画像・360 度写真の保存と、画像認識による標識検出や顔・ナンバープレートのぼかし処理の計算基盤を維持しているが、費用は公表されていない) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet および Mapbox 系ライブラリ (`main.*.js` 内で `leaflet` と `mapbox` の参照を確認) |
| フレームワーク | Angular (`kartaview.org` の `runtime.*.js` / `polyfills.*.js` / `main.*.js` 構成と GitHub `kartaview/openstreetcam.org` の TypeScript 実装を確認) |
| 背景の地図とタイル | OpenStreetMap ベースの地図タイル (`main.*.js` 内で `openstreetmap` を確認) |
| 投稿やデータの保存先 | Grab 管理の非公開サーバーバックエンド (Grab のインフラ基盤。AWS との戦略提携で GrabMaps を展開している) |
| 配信 | `cdn.kartaview.org` (HTML の `dns-prefetch` で確認。応答ヘッダーは `Strict-Transport-Security` のみで配信事業者はヘッダーからは未確認) |

メモ:

- 旧称は OpenStreetCam。JOSM プラグインや iD エディタとの連携機能を持つ。
- 専用ハードウェア (KartaCam) やドライバーパートナー網を通じた東南アジアでのデータ収集にも使われている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 街路画像および撮影トラック | KartaView contributors (CC-BY-SA) | KartaView 公式案内・OpenStreetMap Wiki |
| 背景地図 | OpenStreetMap contributors | `main.*.js` 内の `openstreetmap` 参照 |
