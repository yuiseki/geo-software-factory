# Wheelmap

- URL: https://wheelmap.org
- ソース: https://github.com/sozialhelden/wheelmap-frontend (MIT / モバイル版は Apache-2.0 / バックエンドは GPL-3.0)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Wheelmap、バリアフリー地図、車椅子、アクセシビリティ、Sozialhelden、OpenStreetMap、信号機色分け、クラウドソーシング

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 店舗や公共施設、駅などの車椅子でのアクセシビリティ（バリアフリー状況）を信号機の 3 色で直感的に検索・投稿できる世界的な地図サービス |
| 提供する価値 | 車椅子利用者が外出前に施設の段差やトイレの対応状況を簡単に確認でき、誰でもログイン不要で現地のアクセシビリティ評価を投稿・更新できる |
| 想定する利用者 | 車椅子利用者、ベビーカー利用者、介助者、高齢者、アクセシビリティ情報を整備するボランティアや自治体 |
| 商用か非商用か | 非商用 (ドイツの非営利団体 Sozialhelden e.V. が運営する無料プロジェクト。助成金、財団支援、寄付、企業パートナーシップで運営) |
| 推定の売上 | 推測: 年数千万円〜1 億円規模の活動予算 (非営利団体のため商用売上はなく、助成金・寄付・企業連携による運営資金) |
| 運営 | 非営利団体 (SOZIALHELDEN e.V.、ドイツ・ベルリン) |
| 推定の運用費 | 推測: 月数十万〜数百万円規模。React/Next.js のウェブ基盤と iOS/Android アプリ、アクセシビリティ API (accessibility.cloud) を維持している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | OpenStreetMap ベースの独自インタラクティブ地図 (2026-11-16 の自動プローブは Cloudflare により HTTP 403 で遮断。GitHub リポジトリおよび公開資料から確認) |
| フレームワーク | React / Next.js + Radix UI (`sozialhelden/wheelmap-frontend` の公開リポジトリで確認。HTML は Cloudflare チャレンジにより未取得) |
| 背景の地図とタイル | OpenStreetMap ベースの地図タイル |
| 投稿やデータの保存先 | OpenStreetMap データベース + Sozialhelden 独自のアクセシビリティ DB (`accessibility.cloud`) |
| 配信 | Cloudflare (`server: cloudflare` を応答ヘッダーで確認。2026-11-16 の自動プローブでは `403` "Just a moment..." ボット対策画面を返却) |

メモ:

- ウェブ版のほか iOS / Android アプリが提供されている。
- 2026-11-16 の一次 HTTP 観測では `https://wheelmap.org` が Cloudflare のボット対策によりステータス `403` を返した。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 施設・場所データ | OpenStreetMap contributors (ODbL) | Wikipedia・公式サイト |
| バリアフリー評価・写真 | Wheelmap ユーザー投稿および提携アクセシビリティデータ (CC BY / CC BY-SA) | Wikipedia・GitHub |
