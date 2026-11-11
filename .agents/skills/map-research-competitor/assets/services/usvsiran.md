# Trump Deadline Countdown | CENTCOM Theater Operations Map | US vs Iran Force Tracker

- URL: https://bamqam.com/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 米軍、イラン、中東、軍事、戦力、OSINT

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 中東での米軍とイランの戦力 (基地、艦船、航空機、攻撃目標) と、期限までの残り時間を示すダッシュボードの地図 |
| 提供する価値 | 米国とイランの衝突の状況を、航空機と船の位置の生の情報と合わせて 1 画面で追える |
| 想定する利用者 | 中東の軍事情勢を追う人、OSINT の愛好家 |
| 商用か非商用か | 非商用と見られる (広告、寄付、有料プランは見えなかった。規約は商用の利用と再配布を禁じている。ログインと登録がある) |
| 推定の売上 | なし (非商用と見られる) |
| 運営 | 個人 (画面に「Dashboard by: Nehemia Gershuni-Aylho」) |
| 推定の運用費 | 推測: 月数千〜数万円。Cloudflare の配信、Supabase、航空機 (ADS-B) と船 (AIS) と衛星の生の情報の取得 |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet |
| フレームワーク | Next.js |
| 背景の地図とタイル | CARTO basemaps |
| 投稿やデータの保存先 | Supabase |
| 配信 | Cloudflare |

読み込んだタイルとスタイルの URL (一部):

- `https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png`
- `https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png`
- `https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png`
