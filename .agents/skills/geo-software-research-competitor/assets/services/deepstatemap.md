---
financial: non-commercial
organization: individual
---

# DeepStateMap

- URL: https://deepstatemap.live/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: DeepStateMap、Deep State、ウクライナ戦況マップ、OSINT、前線マップ、Leaflet、PixiJS、紛争地図

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ウクライナ戦争の前線推移・占領地域・軍事ユニット配置を OSINT に基づき高頻度で更新・可視化する戦況マップ |
| 提供する価値 | ジオロケーション検証済みの公開情報と公式発表をもとに、日次の前線変化や紛争の地理的状況をタイムラインと距離・射程計測ツール付きで確認できる |
| 想定する利用者 | ウクライナの市民・避難民、軍事・OSINT 分析家、報道機関、研究者 |
| 商用か非商用か | 非商用 (ウクライナの NGO Deep State UA が無料で公開。一般からの寄付・クラウドファンディングや Brave1 等の支援で運営) |
| 推定の売上 | 推測: 非営利の寄付・支援金モデルのため商業売上はなし (約 100 名のスタッフ・ボランティアを維持する規模の寄付・助成を受けている) |
| 運営 | 非営利団体 (Deep State UA、ウクライナの NGO。2020 年に Roman Pohorilyi 氏と Ruslan Mykula 氏が設立) |
| 推定の運用費 | 推測: 月数万米ドル規模 (100 名規模の分析・運用チームの人件費と、大量のアクセスをさばく Cloudflare・地図タイル配信コスト) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet 1.9.3 + PixiJS 6.4.2 (`leaflet.min.js`、`pixi.min.js`、`L.PixiOverlay.min.js`、`fabric.min.js`、`leaflet.pattern.js` を HTML 内で確認) |
| フレームワーク | 独自バンドル + Workbox PWA (`bundle-be1a1f.min.js` および `workbox-window@6.6.1` を確認) |
| 背景の地図とタイル | MapTiler 等の背景タイルおよび自前の戦況ポリゴン・シンボルレイヤー |
| 投稿やデータの保存先 | 自前サーバー (OSINT チームが検証した前線・部隊データを配信) |
| 配信 | Cloudflare (`server: cloudflare`、`cf-ray` ヘッダーを確認) |

メモ:

- ウェブ版のほか iOS / Android アプリも提供しており、低通信環境向けのオフラインキャッシュ機能を備える。
- Leaflet 上に大量のポリゴンや部隊アイコンを高速描画するため、`L.PixiOverlay` (WebGL) を併用している点が技術的な特徴。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 前線・部隊配置データ | Deep State UA チームによる OSINT (ジオロケーション検証済み SNS・衛星画像・公式発表) | 公式サイトおよび Wikipedia 等の公開情報 |
| 背景地図 | MapTiler 等 | 公式サイト内の表記 |
