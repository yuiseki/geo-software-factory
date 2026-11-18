---
financial: commercial
organization: corp-ent
---

# Google Earth

- URL: https://earth.google.com/web/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Google Earth、グーグルアース、3D 地球儀、衛星写真、航空写真、フォトグラメトリ、WebAssembly、Flutter Web、Google

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 衛星写真、航空写真、3D 地形、建物フォトグラメトリを統合した 3D 地球儀をブラウザやアプリで閲覧・計測できるサービス |
| 提供する価値 | 過去の衛星画像、ストリートビュー、3D 都市モデルをプラグイン不要の地球儀上で滑らかに探索し、距離計測や都市・太陽光設計の初期検討に活用できる |
| 想定する利用者 | 地理や旅に興味のある一般の人、教育・研究機関、不動産・建築・再エネ分野の専門家 |
| 商用か非商用か | 商用 (Standard プランは無料。Professional 月額 75 ドル、Professional Advanced 月額 150 ドルなどの有料プランを提供) |
| 推定の売上 | 未公表 (Alphabet / Google の決算では Google Earth 単体の売上は分けて公表されていない) |
| 運営 | 企業 (Google LLC) |
| 推定の運用費 | 未確認 (世界中の高解像度衛星画像・航空写真のライセンスと撮影、3D フォトグラメトリ生成、Google のグローバル配信基盤の維持に巨額の費用がかかる) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | WebAssembly + WebGL / WebGL2 (HTML に `data-flutterenabled="1"` および `/geo/earth/app/flutter/web/` の読み込み記述を確認) |
| フレームワーク | Flutter Web (2026-11-16 観測時のバージョン表記は `20261105_1202_RC00`) |
| 背景の地図とタイル | Google の衛星画像、航空写真、3D フォトグラメトリメッシュ、標高データ (DEM)、Google Maps 基盤の道路・地名・境界ベクターデータ |
| 投稿やデータの保存先 | Google アカウント / Google ドライブ連携 (プロジェクトや KML/KMZ の保存・インポートに対応) |
| 配信 | Google 自社インフラ (`server: ESF`、`www.gstatic.com`) |

メモ:

- 2026-11-16 に `https://earth.google.com/web/` の HTML を確認したところ、`data-flutterenabled="1"` とマルチスレッド/シングルスレッド切り替え用のスクリプトを確認した。
- 商用・業務向けには有料の Professional / Professional Advanced プランや、衛星画像解析向けの Google Earth Engine が用意されている。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 衛星画像・航空写真 | Google および Landsat・Sentinel 等の公的機関・商業衛星パートナー | Google Earth 公式ヘルプ・データ帰属案内 |
| 3D 都市・地形データ | Google 自社のフォトグラメトリ解析および標高データ (DEM) | Google Earth 公式技術解説 |
| 道路・施設・境界データ | Google Maps プラットフォームの地理空間データベース | Google Earth 公式ドキュメント |
