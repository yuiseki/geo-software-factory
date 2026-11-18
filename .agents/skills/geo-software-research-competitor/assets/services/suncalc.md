---
financial: non-commercial
organization: individual
---

# SunCalc

- URL: https://www.suncalc.org
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: SunCalc、太陽軌道、日の出、日の入り、影の長さ、太陽高度、太陽方位角、OpenLayers、OSINT、写真撮影

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 地図上の任意の地点と日時における太陽の軌道、日の出・日の入り時刻、太陽高度・方位角、物体の影の長さをシミュレーションできるウェブ地図ツール |
| 提供する価値 | 指定した場所・時間に太陽がどの方向から差し込み、建物や人物の影がどの方向にどれだけ伸びるかを地図上で直感的に検証できる |
| 想定する利用者 | 写真家・映像制作者、建築設計者、太陽光発電の設置検討者、OSINT (画像・動画の撮影時刻や場所の検証) 調査者 |
| 商用か非商用か | 非商用 (ドイツの個人開発者 Torsten Hoffmann が無料で提供し、PayPal による任意の寄付を受け付けている。広告表示あり) |
| 推定の売上 | 推測: 少額の寄付と広告収入のみ (正確な金額は非公開) |
| 運営 | 個人 (Torsten Hoffmann、ドイツ。なお類似の `suncalc.net` や JS ライブラリ `suncalc` を開発した Vladimir Agafonkin 氏とは別プロジェクト) |
| 推定の運用費 | 推測: 月数千円〜数万円規模 (軽量な静的ファイルと Plesk/nginx サーバーによる小規模運用) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | OpenLayers 6.15.1 (`scripts/ol-6.15.1.min.js`、`ol-layerswitcher.min.js`、`ol-sonnenverlauf-overlay.min.js` 等を確認) |
| フレームワーク | jQuery + jQuery UI (`jquery-1.9.1.min.js`、`jquery-ui-1.12.0.min.js`) |
| 背景の地図とタイル | OpenStreetMap 等 (OpenLayers レイヤースイッチャー経由で複数背景地図を切り替え) |
| 投稿やデータの保存先 | なし (URL パラメータに緯度経度・日時・物体高さを保持し、クライアント側で天文計算を実行) |
| 配信 | nginx + Plesk (`server: nginx`, `x-powered-by: PleskLin` を応答ヘッダーで確認) |

メモ:

- ウェブ版のほか、Torsten Hoffmann 氏による公式の Android アプリ「SunCalc org」が Google Play で提供されている (iOS 公式アプリはなし)。
- 調査リストの所有者欄に「Vladimir Agafonkin」と記載があったが、実際の `suncalc.org` の運営者はドイツの Torsten Hoffmann 氏であることを HTML の著作権表記と検索で確認した (Vladimir Agafonkin 氏は `suncalc.net` および OSS ライブラリ `suncalc` の作者)。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 太陽位置・軌道計算 | クライアント側天文計算ロジック | https://www.suncalc.org/ |
| 背景地図 | OpenStreetMap 等 | OpenLayers レイヤースイッチャー |
