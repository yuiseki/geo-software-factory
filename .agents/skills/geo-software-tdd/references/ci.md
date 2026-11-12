# CI の組み立て

根拠は [sources](sources.md)。

## 段の分け方

速く落ちるものを先に、重いものを後に置く。

1. 整形、lint、型検査 (警告を誤りとして扱う。Rust の `-D warnings`、matplotlib の `filterwarnings=error`)
2. 単体の試験 (純粋な処理、データ、サーバー)
3. ビルド
4. ブラウザの試験 (地図の描画、操作、描画の比較)。ビルドした配布物に対しても一部を流す (Leaflet は Firefox の試験を縮めた配布物に流す)
5. 本番と同じ構成を立てて、煙の試験 (geolens は本番の構成を Docker で立て、Playwright で当てる)

毎晩に回すもの:

- ブラウザをまたぐ全部の E2E (geolens は毎晩だけ全部のブラウザで回す)
- 依存の最新版や開発版との組み合わせ。落ちたら issue を立てる (cartopy、matplotlib、GeoPandas、folium)
- ファジング (RustGIS)

## 1 つの合否

段がいくつあっても、合否は「CI が通った」という 1 つの段にまとめ、それだけをマージの条件にする。段を足しても、条件の設定を変えずに済む (mln-rs、maplibre-native-rs、MapLibre Native、forge3d)。

## GPU の無い CI で地図を描く

- ブラウザの WebGL: Chromium を SwiftShader で動かす (`--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist` など)。Linux では仮想の画面 (Xvfb) を使う構成がある (MapLibre、deck.gl)。deck.gl は WebGPU も SwiftShader の Vulkan で試す。
- ネイティブの描画: Mesa の lavapipe (Vulkan) と llvmpipe (OpenGL)、Windows の WARP。Mesa の版を固定し、API の検証の層を有効にして、誤りがあれば止める (mln-rs)。
- 本物の GPU でしか言えない試験は、ソフトウェアの GPU の段では、理由を書いて外す。黙って通さない (forge3d)。本物の GPU の段は、自前のランナーか、端末を借りる仕組みに置く (forge3d、MapLibre Native)。
- WebGL を要る試験を CI で動かせないなら、その試験を分けて印を付け、手元でだけ動かすと書く (CesiumJS)。黙って飛ばさない。

## 版の両端

- 最も古い対応の版の段を置く: 依存の最小の版 (matplotlib、cartopy、GeoPandas)、Rust の最小の版 (mln-rs、maplibre-native-rs、ezu)。
- 地図のライブラリの版の範囲をうたうなら、範囲の両端の版で試す (deck.gl は npm の別名で MapLibre の 4、5、6 を試す)。
- 任意の依存を 1 つずつ外した段を置き、無いときの振る舞いを確かめる (GeoPandas)。

## 関門

- 依存のライセンス: 許すライセンスの一覧を決め、CI で確かめる (`cargo deny` は mln-rs、RustGIS。依存のライセンスの一覧を作れなければ落とすのは open-geocode)。npm や Python なら、同じ役割の道具を使う (推測: 道具の名前と設定は案件ごとに選ぶ)。
- 配布物の大きさ: 基準の枝と比べ、上限を超えたら落とす (Leaflet)。
- 秘密の漏れ: 秘密の値がリポジトリに入っていないかを検査する (geolens は gitleaks)。
- 試験の飛ばし: 結合の試験が飛ばされたら落とす。手元では飛ばしてよい試験のデータも、CI では必須にする (GeoPandas)。
- 本数が減る方向にだけ動く上限: panic の箇所や TODO の数に上限を置き、減ったら上限も下げる (mln-rs)。

## 落ちたときに残すもの

- 描画の比較の実際、期待、差分の画像。HTML の報告があれば、それも CI の成果物に上げる。
- ブラウザの試験のコンソールと通信の記録。再試行したときは、記録を増やして残す (MapLibre は再試行のときにログを出す)。

## 公開との関係

- CI の合否を通らなかった版は、本番に出さない。geo-software-deploy の直前の確認で、出す版の CI が通っていることを確かめる。
- 公開のあとは、smoke と、毎晩の段の結果を、群れの見つける役割に渡す (geo-software-swarm)。
