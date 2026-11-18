---
financial: commercial
organization: corp-ent
---

# DoorDash

- URL: https://apps.apple.com/us/app/doordash-food-grocery-more/id719972451
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: フードデリバリー、出前、宅配、ラストワンマイル、DoorDash

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 飲食店や食料品店、小売店の商品を注文し、配達員 (Dasher) によるリアルタイム配送を受けられる北米最大級のデリバリーアプリ |
| 提供する価値 | 配送先周辺の店舗を探し、注文後は配達員の現在位置と到着予定時刻を地図上でリアルタイムに確認できる |
| 想定する利用者 | 食事や日用品の即時配達を求める一般消費者 (米国・カナダ・豪州等) |
| 商用か非商用か | 商用 (配達手数料、サービス料、店舗手数料、DashPass サブスクリプション) |
| 推定の売上 | 公開 (上場企業 DoorDash, Inc. の年間売上は百億ドル規模) |
| 運営 | 企業 (DoorDash, Inc.) |
| 推定の運用費 | 推測: 年間数十億ドル規模 (配達員報酬、地図・ナビゲーション基盤、クラウド、カスタマーサポート) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 種類 | iOS と Android のアプリ |
| 描画 | 未確認 (アプリの中は開いていない) |
| 背景の地図とタイル | Google Maps Platform (On-demand Rides and Deliveries ソリューション、Navigation SDK 等) を採用 (Google Maps Platform 公式顧客事例) |
| 投稿やデータの保存先 | サーバー (配達先住所、店舗在庫、配達員の GPS 位置、注文・決済情報) |
| 配信 | App Store、Google Play |

ストアの表示 (2026-11-16):

- App Store: 販売元 DoorDash, Inc.、Free (無料)、米国ストア評価 23,647,526 件 (平均 4.77)、初出 2013-10-10、最新版 8.44.1 (2026-11-11)、分類 Food & Drink
- Google Play: `com.dd.doordash`、5,000万+ ダウンロード (50M+)、開発元 DoorDash、アプリ内購入 なし

メモ:

- Google Maps Platform 公式顧客事例にて、ラストワンマイル配送の課題解決のために Google Maps Platform の On-demand Rides and Deliveries と Navigation SDK を導入し、建物の輪郭・番地・信号機などの詳細情報を用いた正確なドロップオフを実現していると紹介されている
- アプリの中の描画のライブラリや通信先は端末で開いていないため未確認。確かめるには端末でオープンソースのライセンス一覧と通信を見る
