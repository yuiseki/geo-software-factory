# Open Infrastructure Map

- URL: https://openinframap.org/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: インフラ、送電線、発電所、電力、通信、パイプライン、OSM

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | OpenStreetMap にある世界の電力、通信、石油、ガスのインフラを描き出した地図 |
| 提供する価値 | ふつうの OSM の地図では見えない送電線や発電所を、世界規模で見て、統計や書き出しも使える |
| 想定する利用者 | 電力やインフラの技術者と研究者、OSM のマッパー |
| 商用か非商用か | 非商用 (地図は無料。GIS 形式の商用の書き出しは Infrageomatics が売っており、その会社がこの地図の作業を支えている) |
| 推定の売上 | 地図そのものの売上は無い。Infrageomatics の書き出しの売上は未確認 |
| 運営 | 個人 (作者は Russ。背景の地図は Protomaps、検索は OpenCage の支援) |
| 推定の運用費 | 推測: 月数万円。全球の OSM からインフラを取り出して自前のタイルを作り、Cloudflare の後ろから配る |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | 自前のタイル (サイトと同じドメイン) |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Cloudflare |

読み込んだタイルとスタイルの URL (一部):

- `https://openinframap.org/map/power/{z}/{x}/{y}.pbf`
- `https://openinframap.org/{z}/{x}/{y}/0.mvt`
- `https://openinframap.org/{z}/{x}/{y}/1.mvt`
- `https://openinframap.org/{z}/{x}/{y}/2.mvt`
