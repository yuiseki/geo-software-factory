---
financial: non-commercial
organization: individual
first_seen: 2001-03-31
first_seen_by: wayback
---

# 東京観光公式サイト GO TOKYO

- URL: https://www.gotokyo.org/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: 東京、観光、スポット、イベント、モデルコース、エリアマップ、多言語、GO TOKYO、Tokyo tourism

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 東京都と東京観光財団が運営する、多言語対応の東京公式観光情報サイト |
| 提供する価値 | 都内各地の観光スポット、イベント、エリアガイド、路線図や観光マップ PDF を日本語と外国語でまとめて探せる |
| 想定する利用者 | 東京を訪れる国内外の観光客、修学旅行や団体の旅行者、観光事業者 |
| 商用か非商用か | 非商用 (公的機関の観光プロモーションサイト。広告枠の販売や有料会員は見当たらない) |
| 推定の売上 | 該当なし (東京都からの委託事業・公的予算による運営と見られる) |
| 運営 | 公益財団法人東京観光財団 (TCVB: Tokyo Convention & Visitors Bureau) |
| 推定の運用費 | 推測: 月数十万円から数百万円規模 (多言語自動翻訳システム、AWS 上の API や配信基盤、CMS 運用を含む公的サイト規模) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 外部の Web 地図ライブラリ (Google Maps JS API、Mapbox、Leaflet 等) の読み込みは観測されなかった。エリア案内は独自 SVG (`map_all.svg`) と WebP 背景画像 (`bg_all.webp` 等) を組み合わせた `$.GFUNC.regionMap` で描画し、個別スポットページからは Google マップ (`maps.google.com/?cid=...` および `www.google.com/maps/dir/?api=1`) へ外部リンクする構成。 |
| フレームワーク | jQuery、jQuery UI、Splide (スライダー) を利用。静的 HTML と専用 JS 群 (`/shared/site_gotokyo_rn/js/`、`/shared/system/js/`) で構築されている。 |
| 背景の地図とタイル | 外部の地図タイル通信は観測されなかった。エリアマップ用の独自画像 (WebP/SVG) および PDF マップを提供する。 |
| 投稿やデータの保存先 | サイト内検索や一部データ取得には AWS API Gateway (`*.execute-api.ap-northeast-1.amazonaws.com` が CSP の `connect-src` に記載) やサーバー側の検索スクリプトを利用。ユーザー投稿機能は見当たらない。 |
| 配信 | openresty (HTTP ヘッダー `Server: openresty`、`Cache-Status` ヘッダーあり)。多言語変換に `msta.j-server.com` を利用。 |

データの出どころ (2026-11-16):

- 観光スポット情報、エリア解説、PDF マップ: 東京観光公式サイト GO TOKYO (公益財団法人東京観光財団) の独自掲載情報。
- スポット詳細ページの地図リンク先: Google マップ (`maps.google.com` への外部リンク。サイト最下部の著作権表記は `Copyright © Tokyo Convention & Visitors Bureau. All rights reserved.`)。
