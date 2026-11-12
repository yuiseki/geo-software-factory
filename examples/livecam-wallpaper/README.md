# 窓の向こう

公開ライブカメラをランダムに巡る、個人利用向けのプロトタイプです。四画面で表示し、それぞれの映像の右側に地球上の位置と周辺地図を縦に並べます。画面の大きさに合わせて地図欄の幅を変え、映像は 16:9 に収めます。小さな地球ではカメラの所在国を塗り、Natural Earth 1:10m admin-1 の地図ではカメラが属する行政区画を塗り、カメラの位置をピンで示します。区画が一致しない場合は「境界未特定」と表示します。日本のカメラを 70% の確率で選び、各画面を 3 分ごとに切り替えます。各画面の切り替えは 45 秒ずつずらし、下端のバーで次の切り替えまでの進み具合を示します。

## 起動

このディレクトリで次のコマンドを実行し、ブラウザで `http://localhost:8000` を開きます。

```sh
python3 -m http.server 8000
```

`public/livecams.json` の `cams` を読み込みます。カメラの一覧はリポジトリに含めていません。形式は [public/livecams.example.json](public/livecams.example.json) にあり、これを `public/livecams.json` に写して実際のカメラで埋めます。映像、地図と表示用ライブラリにはインターネット接続が必要です。映像は無音で自動再生を試みます。YouTube IFrame Player API が動画の削除や埋め込み制限などの再生エラーを通知した場合は、その画面だけ次の映像に切り替え、エラーになったカメラをそのブラウザで10分間候補から外します。連続エラー時は高速な切り替えを制限します。API が読み込めない場合やブラウザの自動再生制限など、検知・自動復旧できない場合もあります。BGM、定期的な生存チェック、カメラの自動追加は未実装です。

詳細地図は [Turf.js](https://turfjs.org/) でカメラを含むポリゴンの bbox を求め、その範囲に合わせて表示します。離れた島々を含む行政区画では、カメラがある島や本土の範囲に合わせます。境界の簡略化によりポリゴンを特定できない場合は、カメラを中心とした固定の縮尺で表示します。区画を特定できない場合はカメラの位置を中心に表示します。

地図は [OpenFreeMap](https://openfreemap.org/) と [MapLibre GL JS 6.14.0](https://maplibre.org/) を使い、地球の陸地と行政区画は [Natural Earth](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/) のデータを用います。`public/camera-admin1.json` は Natural Earth 5.1.1 とカメラ一覧を照合して生成したもので、[scripts/build-admin1.py](scripts/build-admin1.py) と `/usr/bin/python3` の GDAL バインディングで再生成できます。境界は縮尺に応じて簡略化されており、海上や島しょ部などで一致しない場合があります。公開前にカメラ一覧の出典と再配布条件、映像の利用条件を確認してください。

## Cloudflare Workers へのデプロイ

公開先は https://livecams.yuiseki.net です。Cloudflare の認証済み Wrangler と Node.js の `npx` を用意し、このディレクトリから実行します。配信用に必要なファイルだけを一時ディレクトリに集めてアップロードします。

```sh
systemd-run --user --scope -q -p MemoryMax=8G -p MemorySwapMax=0 -p CPUQuota=400% -- ./deploy.sh
```

`wrangler.jsonc` はステージング先にコピーして使用します。`public/livecams.json` を更新した場合は、デプロイ前に行政区画との照合結果も再生成してください。
