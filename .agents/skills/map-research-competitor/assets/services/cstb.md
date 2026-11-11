# CSTB Japan and NW Pacific 2026

- URL: https://gis.ikgm.net/cstb/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 海底地形、水深、測深、バシメトリ、bathymetry、海洋

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 日本と北西太平洋の、船の測深を集めて 1 枚にした海底地形の陰影図と、そのセルごとの出どころを示す地図 |
| 提供する価値 | 約 90 m の解像度の海底地形を、どの航海のデータ由来かまで確かめながら見られる |
| 想定する利用者 | 海洋や地球科学の研究者、海底地形の図を作る人 |
| 商用か非商用か | 非商用 (広告、寄付、有料プランは見えなかった) |
| 推定の売上 | なし (非商用) |
| 運営 | 個人と見られる (ikgm.net のサブドメイン。運営者の表示は見つからなかった) |
| 推定の運用費 | 推測: 月 0〜数百円。自前のタイルを Cloudflare から配る静的配信。編纂の計算は手元 |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet 1.9.4 |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | 自前のタイル (サイトと同じドメイン) |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Cloudflare |

読み込んだタイルとスタイルの URL (一部):

- `https://tiles.ikgm.net/cstb-japan-nwp-2026/r4/ao_topousm.pmtiles`
- `https://tiles.ikgm.net/cstb-japan-nwp-2026/r4/hillshade.pmtiles`
- `https://tiles.ikgm.net/cstb-japan-nwp-2026/r4/source.pmtiles`
- `https://tiles.ikgm.net/cstb-japan-nwp-2026/r4/specular_topousm.pmtiles`
- `https://tiles.ikgm.net/gebco-2026-composite/r1/basemap.pmtiles`

メモ:

- 陰影などを自前の PMTiles に分けて置き、Leaflet で重ねている

データの出どころ (地図の帰属表示と画面の最下部 500 字、2026-11-12):

- 地図の帰属表示: 「Basemap: IGR Map (Ikegami 2026), from GEBCO 2026, CSTB Japan and NW Pacific 2026 v27 (JAMSTEC DARWIN, NOAA NCEI DCDB, MGDS, PANGAEA, PIBHMC, KHOA, JODC)」
- 画面の最下部ほか: 「出典の表示を条件に自由に利用できます」「本データセットと、依拠した航海や格子を引用してください」「編纂物であるため、元データには提供機関ごとに異なる条件が及びます」
