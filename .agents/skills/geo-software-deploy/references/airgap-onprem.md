# 閉域網 (LGWAN)・オンプレミス納品手順

自治体 (LGWAN 接続系・マイナンバー利用事務系) や大企業の閉域網、完全エアギャップ環境では、外部インターネットへの通信が一切通らないため、パブリッククラウド向けの自動デプロイ手順が使えない。夜のうちに「オフラインでも再現・検証できる持ち込みパッケージ」を組み立てる手順を定める。

## 1. 外部通信ゼロの事前チェック (Build 時)

閉域環境に持ち込む前に、インターネット遮断状態のコンテナ (`docker network create --internal` 等) でアプリを起動し、外部通信が発生しないことを確かめる。

| 対象 | 閉域環境で壊れやすい箇所 | 対策 |
|---|---|---|
| **地図スタイル・タイル** | `style.json` が外部のベースマップ・PMTiles・Terrain URL を参照 | すべて相対パスまたは自前ホストのエンドポイントへ書き換える |
| **フォント (Glyphs) と Sprite** | MapLibre 等の `glyphs` / `sprite` が外部 CDN (`demotiles` / `fonts.openmaptiles.org` 等) を向く | 必要な文字範囲の PBF グリフと Sprite JSON/PNG をリポジトリまたは配信物に同梱する |
| **フロントエンド資産** | `<script src="https://unpkg.com/...">` や Google Fonts | すべてバンドル (Vite 等) し、外部 `<link>` / `<script>` を 0 件にする |
| **ジオコーダ・時刻・外部 API** | 外部 API 呼び出しや CDN 経由の WASM 取得 | ローカル索引 (SQLite FTS5 / DuckDB / 自前 API) と同梱 WASM へ切り替える |

## 2. 成果物バンドルの作り方 (持ち込み用)

顧客の閉域環境へ持ち込む場合は、ネットワーク接続なしで展開できる単一アーカイブを作成する。

1. **コンテナイメージの書き出し**: ターゲットアーキテクチャ (`--platform linux/amd64` 等) を合わせてビルドし、`docker save <image>:<tag> | gzip > app-image.tar.gz` と SHA-256 チェックサムを作成する。
2. **言語依存のオフライン化 (非コンテナ納品の場合)**:
   - Python: `pip download -r requirements.txt -d wheelhouse/` で wheel 一式を同梱し、`pip install --no-index --find-links=wheelhouse -r requirements.txt` で導入できるようにする。
   - Node.js: `npm ci --offline` またはビルド済み静的ファイル (`dist/`) と単一実行ファイル群のみを納品する。
3. **地図データ・タイルの同梱**: PMTiles / MBTiles / PostGIS ダンプと更新用ツールを `data/` に同梱し、パスを設定ファイル (環境変数) で切り替えられるようにする。

## 3. オンプレ VM / K8s / Windows Server (IIS) への配備要点

- **Linux VM (systemd + Docker Compose / Nginx)**: ポート設計、TLS 証明書 (庁内 CA 発行の内部証明書や自己署名証明書を OS トラストストアへ追加する手順)、ログローテーションを同梱する。
- **Windows Server (IIS リバースプロキシ)**: 庁内標準が Windows Server の場合、ARR (Application Request Routing) によるリバースプロキシ設定と、`.pbf` / `.pmtiles` / `.wasm` / `.geojson` の MIME タイプ登録および `Range` リクエスト (HTTP 206) の透過設定を手順書に明記する。

## 4. 納品前検証

- `--internal` (外部通信遮断) ネットワーク上の Docker で起動し、ブラウザ開発者ツールの Network タブで **外部ドメインへのリクエストが 0 件**、かつ Console エラー (フォント欠落・CORS・404) が 0 件であることを確認する。
