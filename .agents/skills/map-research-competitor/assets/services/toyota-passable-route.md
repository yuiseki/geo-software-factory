# トヨタ | 通れた道マップ

- URL: https://www.toyota.co.jp/jpn/auto/passable_route/map/
- 観測した日: 2026-11-12
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 通れた道、通行実績、通行実績マップ、災害、地震、豪雨、道路情報、通行止め、交通規制、チェーン規制、冠水、プローブ情報、コネクティッドカー、テレマティクス、給電、トヨタ、passable route map、disaster road map、probe data

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | トヨタのテレマティクスサービスを使う車から集めたプローブ情報で、直近 24 時間 (災害時は 3 時間も) に車が実際に通れた道路を地図に示し、交通規制や給電できる車と販売店も重ねる地図 |
| 提供する価値 | 災害の後に、どの道を車が実際に通れているかを、規制の情報と同じ画面で確かめられる |
| 想定する利用者 | 災害の後に車で移動する人、被災地へ向かう支援者 |
| 商用か非商用か | 非商用と見られる (広告、課金、寄付は見えなかった。災害後の安全運転の参考情報として無償で公開している。データは本業のコネクティッドサービスの車両から集めたもの) |
| 推定の売上 | なし (非商用と見られる) |
| 運営 | 企業 (トヨタ自動車株式会社。交通規制の情報はトヨタコネクティッドが提供と書かれている) |
| 推定の運用費 | 推測: 月数十万〜数百万円。Bing Maps Enterprise のライセンスとゼンリンの地図、航空写真 (パスコ) の使用料、プローブ情報を集計して WMS で配る GeoServer、Azure と CloudFront の配信。プローブを集める仕組みは本業のコネクティッドサービスと共用と見られ、この地図だけの費用は分けられない |

## 技術 (2026-11-12 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Bing Maps の Web Control (`www.bing.com/api/maps/mapcontrol` を読み込み、グローバルに `Microsoft` がある) |
| フレームワーク | jQuery 3.7.1、jQuery UI、slick。サーバー側はパスの形 (`Home/GetVicsReg`、`Content/`、`Scripts/`) から ASP.NET MVC と見られる (未確認) |
| 背景の地図とタイル | Bing Maps のタイル (`t.ssl.ak.dynamic.tiles.virtualearth.net`、日本語、陰影つき)。通れた道と交通規制は GeoServer の WMS の透過 PNG を重ねる |
| 投稿やデータの保存先 | 投稿は無い。通行実績と規制は GeoServer の WMS、規制、写真、給電の情報はサイトと同じドメインの JSONP の API (`Home/GetVicsReg`、`Home/GetPhoto`、`Home/GetPowerSup`) |
| 配信 | ページは Azure (応答ヘッダーに `x-azure-ref`)。WMS は CloudFront 経由 (`rttileserver.dmp.tconnect.jp`) |

読み込んだタイルとスタイルの URL (一部):

- `https://t.ssl.ak.dynamic.tiles.virtualearth.net/comp/ch/{quadkey}?mkt=ja-JP&it=G,LC,BX,RL&shading=hill&...`
- `https://rttileserver.dmp.tconnect.jp/geoserver/wms?layers=cite:PassableRoad24H&...&request=GetMap&width=256&height=256&transparent=true`
- `https://rttileserver.dmp.tconnect.jp/geoserver/wms?layers=cite:PassableVicsReguration&...`

メモ:

- 地図の描画は Bing Maps に任せ、自社のデータは GeoServer の WMS で 256 ピクセルの透過 PNG にして重ねる構成。ベクトルタイルは使っていない
- 平時は通れた道 (直近 24 時間) と交通規制だけを出す。Tプローブ交通情報 (渋滞と混雑) と 3 時間の通行実績への切り替えは、災害時の情報提供の期間だけ (ご利用ガイド)
- 地図情報の欄に、試験版のワイパー情報 (車のワイパーの速さの平均を 5 段階)、冠水推定情報 (車両走行情報から推定)、滑りやすい地点がある。車の動きを雨や路面の状態の観測に使っている
- 縮尺 25 km より広い表示では、最大 3 時間前までの実績になることがある (地図情報の欄)
- 推奨ブラウザに Internet Explorer 11 が残っており、画面の最下部の著作権の表示は「©1995-2019」のまま (2026-11-12)
- はてなブックマーク 230 件 (2026-11-12)
- 通信は Google Analytics、Google Tag Manager、トヨタのタグ (`onetag.tws.toyota.jp`) と `techlab-cdn.com`。広告の通信は見えなかった
- 利用規約がコードの解析を禁じているかは確かめていないので、通信と画面の文字だけを記録した

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 背景の地図 | © 2026 Zenrin、© 2026 Microsoft Corporation (Bing Maps。Microsoft Bing Maps Enterprise ライセンスを使用) | 地図の帰属表示、画面の最下部 |
| 通れた道 (直近 24 時間と 3 時間の通行実績) | トヨタのテレマティクスサービスを使う車両から集めたプローブ情報 | ご利用ガイド |
| Tプローブ交通情報 (渋滞、混雑) | トヨタ独自のリアルタイム交通情報 (災害時のみ表示) | ご利用ガイド、地図情報の欄 |
| 交通規制、チェーン規制 | JARTIC (日本道路交通情報センター) と VICS センターの情報を、トヨタコネクティッドが提供 | ご利用ガイド、地図情報の欄 |
| 支援販売店、給電車両 | 災害支援ができるトヨタの販売店と、給電の機能を持つ車両 (燃料の残量で色分け) | ご利用ガイド |
| ワイパー情報、冠水推定情報、滑りやすい地点 (いずれも参考情報、前の 2 つは試験版) | 車両走行情報から推定 | 地図情報の欄 |
| 航空写真 | 株式会社パスコ提供 (©PASCO CORPORATION / Kokusai Kogyo Co., Ltd.) | 航空写真の表示、地図情報の欄 |

プローブ情報の集め方 (台数、匿名化の方法) と、交通規制の情報の再配布の条件は書かれていなかった (2026-11-12)
