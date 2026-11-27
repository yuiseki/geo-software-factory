---
financial: commercial
organization: corp-smb
first_seen: 2004-04-12
first_seen_by: wayback
---

# Citymapper

- URL: https://citymapper.com/ (Web アプリ: https://citymapper.com/webapp)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Citymapper、シティマッパー、乗換案内、公共交通、マルチモーダル、徒歩ナビ、自転車ナビ、都市交通、MaaS、transit app

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界の主要都市を対象に、電車・バス・徒歩・自転車・シェアモビリティ・配車を統合して最適ルートを案内する都市型乗換案内アプリ |
| 提供する価値 | 鉄道やバスのリアルタイム運行状況、駅の出口や乗車車両位置まで考慮した高精度な都市内ドアツードアの経路案内と遅延通知 |
| 想定する利用者 | ロンドン・東京・ニューヨークなど大都市圏の通勤者・通学者・旅行者、および交通ソリューションを導入する自治体・法人 (Via 経由) |
| 商用か非商用か | 商用 (基本無料。有料会員プラン「Citymapper CLUB」、配車・シェアモビリティ送客手数料、B2B エンタープライズ契約、都市内広告) |
| 推定の売上 | 未確認 (2023 年 3 月に Via が買収。買収額や単体売上は非公開だが、買収当時は調達額に比べ低い価格と報じられた) |
| 運営 | 企業 (Via Transportation 傘下、2011 年に英ロンドンで設立) |
| 推定の運用費 | 未確認 (数百都市の GTFS / GTFS-RT データ収集・クレンジング基盤、独自のルーティングエンジン、地図・リアルタイム配信基盤の運用) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`https://citymapper.com/webapp` の HTML 内に `maps.googleapis.com/maps/api/js` の読み込みを確認。モバイルアプリではカスタム地図 UI を採用) |
| フレームワーク | 未確認 (Web アプリでは独自バンドル `/static/components/bundle-*.js` を確認) |
| 背景の地図とタイル | Google Maps (Web アプリ)、および OpenStreetMap (公式情報にて、歩行者・自転車・道路データの基盤として OSM を活用し独自データを重ねていることを公表) |
| 投稿やデータの保存先 | Citymapper / Via 自社基盤 (各都市交通局の GTFS / GTFS-RT フィードおよび自社「Data Factory」で整備した駅構内・出口データ) |
| 配信 | Cloudflare (`server: cloudflare`, `cf-ray` ヘッダーを確認) |

メモ:

- 2023 年 3 月にニューヨークの TransitTech 企業 Via に買収され、Via の自治体向け交通基盤と統合された (セルフサーブの旧開発者 API は終了し Via 経由の法人契約へ集約)。
- 独自の「Data Factory」により、鉄道の車両ごとの乗換推奨位置や駅の出入口など、一般的な GTFS に含まれない細かな都市交通データを整備している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 道路・歩行者・自転車ネットワーク基盤 | OpenStreetMap contributors | Citymapper 公式ブログおよび OpenStreetMap Wiki |
| Web アプリ地図 API・配信基盤 | Google Maps JavaScript API、Cloudflare | `https://citymapper.com/webapp` の HTTP 応答ヘッダーおよび HTML (2026-11-16 観測) |
| 運行ダイヤ・リアルタイム運行情報 | 各都市の公共交通事業者・自治体 (GTFS / GTFS-RT 等) | Citymapper 公式サイト |
