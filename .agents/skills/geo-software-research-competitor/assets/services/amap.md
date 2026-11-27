---
financial: commercial
organization: corp-ent
first_seen: 1996-12-20
first_seen_by: wayback
---

# 高徳地図 (Amap / AutoNavi)

- URL: https://www.amap.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: 高徳地図、高德地图、Amap、AutoNavi、Alibaba、アリババ、中国地図、配車、ナビ

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | Alibaba 傘下の AutoNavi が運営する、中国国内のナビゲーション、配車アグリゲーション、生活サービス予約を統合した地図スーパーアプリ |
| 提供する価値 | 高度な 3D ナビや屋内地図、リアルタイム渋滞回避に加え、複数の配車サービスの一括呼び出し、ホテル・チケット予約、店舗評価を 1 つの地図上で完結できる |
| 想定する利用者 | 中国国内のドライバー・通勤者・旅行者、ローカル店舗を探したい一般の人、地図 API を使う法人・開発者 |
| 商用か非商用か | 商用 (一般利用は無料。アプリ内の配車仲介手数料、ホテル・チケット予約、ローカル店舗広告、法人向け地図 API で収益化) |
| 推定の売上 | 未公表 (Alibaba Group の Local Services Group セグメントに含まれ、Amap 単体の売上は分けて公表されていない) |
| 運営 | 企業 (AutoNavi Software / 高徳軟件、Alibaba Group Holding 傘下) |
| 推定の運用費 | 未確認 (数億人規模の DAU・約 10 億人規模の MAU を支える Alibaba Cloud 上のサーバーレス基盤と、膨大な地図・POI データの維持費がかかる) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | WebGL および独自レンダリングパイプライン (3D ナビ・屋内地図・都市デジタルツイン表示。HTML では `amapConfig.js` と `mapTracker.js` の読み込みを確認) |
| フレームワーク | 未確認 (HTML 内では Alibaba 系のボット対策スクリプト `AWSC/awsc.js`、`baxiaCommon.js` 等を確認) |
| 背景の地図とタイル | AutoNavi 自社測量および走行プローブデータ、Alibaba 経済圏 (Cainiao・Alipay) 連携データ、中国国外向けは HERE Technologies 等の提携データ |
| 投稿やデータの保存先 | 高徳 / Alibaba アカウント (口コミ、店舗評価、移動履歴等の保存) |
| 配信 | Tengine + Alibaba Cloud (`server: Tengine` ヘッダーおよび `g.alicdn.com` からのアセット配信を確認。バックエンドでは Function Compute を活用) |

メモ:

- 2026-11-16 に `https://www.amap.com/` を確認したところ、`__amap_cookie_probe` への 302 リダイレクトを経て `200 OK` となり、`server: Tengine` と `g.alicdn.com` のスクリプトを確認した。
- 中国国内にとどまらず、HERE Technologies 等との提携により海外旅行者向けの「World Map」機能も提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 中国国内道路・POI・交通データ | AutoNavi (高徳) 自社測量データ、利用者の走行クラウドソースデータ、Cainiao / Alipay 連携データ | Alibaba 公式ニュースリリース (Alizila)・Alibaba Cloud 技術記事 |
| 中国国外の地図データ | HERE Technologies 等の外部地図パートナー | HERE Technologies・Alibaba 提携発表 |
