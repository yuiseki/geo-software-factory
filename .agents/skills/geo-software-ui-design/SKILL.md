---
name: geo-software-ui-design
description: 地図プロダクトの UI (画面構造、レイアウトの型、四隅のコントロール配置、詳細パネル・ボトムシートと地図 padding の連動、操作モード、レイヤー・凡例、ベースマップとのコントラスト、一般的な Web UI 原則) を設計する。UX を扱う geo-software-ux-design の後、または実装前に「地図の画面レイアウトを決めたい」「ポップアップとサイドバー/ボトムシートのどちらにすべきか」「コントロールや凡例が地図を隠す」「モバイルで地図 UI が崩れる」と言われたら使う。
---

# geo-software-ui-design

地図プロダクトの画面構造、オーバーレイ配置、部品の振る舞い、見た目の基準を設計する。UX (利用者の目的、情報設計、操作フロー、負荷感覚) を決める [geo-software-ux-design](../geo-software-ux-design/SKILL.md) と役割を分け、このスキルでは「画面上のどこに何をどう配置し、どの状態でどう見せるか」を具体化する。

一般的な Web UI の基準 (ビューポート、固定 `z-index` スケール、コンポーネント、タイポグラフィ、色、動き、アクセシビリティ) は [general-ui-principles](references/general-ui-principles.md) を基準にし、地図特有の配置・連動ルールは下の reference を読む。

| reference | 読むとき | 中身 |
|---|---|---|
| [map-layout-and-overlays](references/map-layout-and-overlays.md) | 画面全体の型と配置を決めるとき | 全画面・分割・埋め込み・常時表示の 4 つの型、四隅の衝突回避、モバイル (`100dvh` / セーフエリア / ジェスチャ競合) |
| [detail-panels-and-padding](references/detail-panels-and-padding.md) | 地物の詳細や一覧を出すとき | Popup / サイドパネル / スナップ式ボトムシートの使い分け、地図 `padding` 連動、一覧と地図の同期 UI |
| [controls-modes-and-layers](references/controls-modes-and-layers.md) | ツールバー・モード・レイヤーを置くとき | 閲覧/計測/作図モードの明示と終了導線、レイヤー・凡例の折りたたみ、ベースマップに負けないコントラスト |
| [general-ui-principles](references/general-ui-principles.md) | 部品・余白・文字・色・動きを整えるとき | `ibelick/ui-skills` を基にした Web UI の一般原則 (`h-dvh`、固定 `z-index`、`tabular-nums`、1 アクセントカラー、アクセシビリティ等) |
| [unslop-ai-app](references/unslop-ai-app.md) | AI らしさを抜いた画面・日本語組版・モバイル実機確認を行うとき | `minorun365/unslop-ai-app` を基にした情報の引き算、AI 定番の型の回避、日本語組版、コントラスト測定、モバイル実機相当の検証 |

## 入力

設計の前に、次の情報を確認する。プロダクト概要 (`product-brief.md`) や `geo-software-ux-design` の設計結果があればそこから読み、不足があれば選択肢で聞ける形で確認する。

- 画面での地図の役割: 全画面オーバーレイ型 / 一覧との分割型 / 埋め込みカード型 / 常時表示型
- 主な利用端末と画面幅: デスクトップ中心 / モバイル中心 / 両方
- 地物選択時に見せる情報量: 見出しと数行 (軽量) / 写真・属性・編集フォーム (詳細)
- 操作モードの有無: 閲覧のみ / 検索・絞り込みあり / 計測・作図・編集あり
- ベースマップの種類: ライト / ダーク / 航空写真 / ユーザーによる切替あり

## 進め方

1. **画面の型と領域配分を決める**: [map-layout-and-overlays](references/map-layout-and-overlays.md) に沿って 4 つの型から 1 つを選び、デスクトップとモバイルでの切り替え方 (分割表示からボトムシートへの変換など) を決める。
2. **四隅と必須表示の定位置を固定する**: 帰属表示 (Attribution)、スケールバー、検索欄、ズーム・コンパス・現在地ボタンの角を割り当て、ボトムシートやパネル展開時にも帰属表示が隠れないことを確かめる。高さは `100vh` ではなく `100dvh` を使い、セーフエリアを確保する。
3. **詳細表示の器と地図 `padding` 連動を決める**: [detail-panels-and-padding](references/detail-panels-and-padding.md) に沿って Popup / サイドパネル / スナップ式ボトムシートを選び、パネル展開時に選択地物が隠れないよう地図側の `padding` を連動させる仕様を明記する。一覧がある場合はホバー・選択・フィルタの同期方式を決める。
4. **操作モードとレイヤー UI を整理する**: [controls-modes-and-layers](references/controls-modes-and-layers.md) に沿って、既定の閲覧モードと編集・計測モードの見た目・終了導線 (`Escape`・キャンセルボタン) を決める。レイヤーや凡例は初期状態で折りたたみ、地図面積の圧迫を防ぐ。
5. **一般的な UI 原則とコントラストを当てる**: [general-ui-principles](references/general-ui-principles.md) と [unslop-ai-app](references/unslop-ai-app.md) に沿って `z-index` スケール、タッチ領域 (`44px` 以上)、数値の `tabular-nums`、1 行省略 (`truncate`)、アイコンボタンの `aria-label`、空状態の次アクション、情報の引き算、AI らしい定番の型の排除、日本語組版 (`palt`・行間)、ベースマップ (航空写真やダークマップ含む) の上で読める不透明面・枠線・影を決める。UI の文言は `stop-describing-ui` の原則に沿って説明文を省き短い動詞・名詞にする。
6. **壊れやすい条件を実寸で確認する**: [unslop-ai-app](references/unslop-ai-app.md) のコントラスト測定とモバイル確認手順も踏まえ、狭いスマホ幅 (セーフエリア・入力欄 `16px` 以上・横はみ出しなし)、ソフトキーボード展開時、長文の施設名・住所、航空写真やダークマップへ切り替えた状態、ボトムシートを最大展開した状態でも帰属表示・閉じる操作・選択地物が見失われないかを設計チェックリストに含める。

## 出力

設計の結果はプロダクト概要 (`product-brief.md`) または設計書の「画面と操作 (UI 設計)」に次の項目として残す。

- 選択した画面の型とレスポンシブ時の切り替え方 (PC / モバイル)
- 四隅のコントロール配置表と固定 `z-index` スケール
- 詳細表示の器と地図 `padding` の連動ルール
- 操作モードとレイヤー・凡例の開閉ルール
- ベースマップ別 (ライト / ダーク / 航空写真) の UI パネル配色とコントラスト方針
