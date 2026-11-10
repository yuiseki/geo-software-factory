# 利用者の近くに置くサーバー

対象: 自治体の庁舎、工場、店舗、車両、災害時の現地などに置く小さなサーバーやクラスタ (k3s、単体の小型機)。閉域網やオフラインでの運用

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 |

## 候補ごとの制約

自前のハードで動かすので、CDN のエッジ関数のような 1 リクエストあたりの CPU 時間の上限やコードサイズの上限はない。上限を決めるのは機械のメモリ、ディスク、電源である。表の「CPU 時間の上限」「配れるコード・Wasm の大きさ」は、この節では「計算資源」「配れるもの」と読み替える。

| 候補 | CPU 時間の上限 (計算資源) | メモリの上限 | 配れるコード・Wasm の大きさ (配れるもの) | 置けるデータ (オブジェクトストレージ、KV、DB) | Range リクエスト | 料金の単位 | 出典 |
|---|---|---|---|---|---|---|---|
| Raspberry Pi 5 | BCM2712、Arm Cortex-A76 4 コア 2.4 GHz。リクエストごとの上限はない | LPDDR4X で 1、2、4、8、16 GB の 5 種 | 任意 (arm64 の Linux バイナリとコンテナ) | microSD (SDR104) か、M.2 HAT 経由の PCIe 2.0 x1 の NVMe SSD | 自分で動かすサーバー次第。go-pmtiles や Martin はローカルの PMTiles を読む | 本体の買い切り。16 GB 版は 2026-11-02 に 80 ドル値上げされ 385 ドル (メモリの値上がりによる。https://www.raspberrypi.com/news/price-rises-for-some-16gb-raspberry-pi-products/)。製品ページは 2026-11-10 時点で 305 ドルのままで、他の版の価格はページになかった。電源は 5V 5A の USB-C PD | [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) |
| k3s (単体の小型機やクラスタ) | サーバー 2 コア、エージェント 1 コアが最小 | サーバー 2 GB、エージェント 512 MB が最小 (k3s 本体と同梱部品の分で、載せる仕事の分は別) | コンテナイメージ。x86_64、armhf、arm64 | ノードのディスク。SSD を推奨。Raspberry Pi では外付け SSD を推奨し、SD カードと eMMC は etcd の書き込みに耐えないと書かれている | ワークロード次第 | OSS (料金なし) | [k3s requirements](https://docs.k3s.io/installation/requirements)、[air-gap](https://docs.k3s.io/installation/airgap) |
| k0s | コントローラー 1 vCPU、ワーカー 1 vCPU (目安) | コントローラー 1 GB、ワーカー 0.5 GB、両方兼ねて 1 GB (目安) | コンテナイメージ。x86_64、aarch64、armv7l、riscv64 (riscv64 はビルド済みバイナリなし) | 両方兼ねる場合 k0s 自体が約 2.0 GB を要し、ワーカーは 15% 以上の空きが必要 | ワークロード次第 | OSS | [k0s system requirements](https://docs.k0sproject.io/stable/system-requirements/)、[airgap install](https://docs.k0sproject.io/stable/airgap-install/) |
| MicroK8s | 公式ページに CPU の最小値はない | 最小 540 MB、推奨 4 GB | snap で入れる (`--channel=1.35`) | 推奨 20 GB 以上のディスク | ワークロード次第 | OSS | [MicroK8s getting started](https://canonical.com/microk8s/docs/getting-started) |
| ミニ PC (x86_64) | 機種による | 機種による | 任意 | 機種による (NVMe が一般的 (推測)) | ワークロード次第 | 本体の買い切り | 公式の比較資料は確かめていない (未確認) |

地図の部品ごとの必要資源 (公式の記載):

| 部品 | ライセンス | 必要資源 | 出典 |
|---|---|---|---|
| go-pmtiles (`pmtiles serve`、`extract`) | BSD-3-Clause | 依存のない単一バイナリ。v1.31.2 で Linux arm64 と x86_64 のビルドがある。`serve` のディレクトリキャッシュは既定 64 MB | [CLI](https://docs.protomaps.com/pmtiles/cli)、[go-pmtiles](https://github.com/protomaps/go-pmtiles) |
| Martin (タイルサーバー) | Apache-2.0 か MIT の選択 | Rust 製。v1.16.1 で aarch64 Linux (gnu、musl) のビルドがある。PostGIS、PMTiles、MBTiles、GeoJSON を配る | [martin](https://github.com/maplibre/martin) |
| OSRM (ルート検索) | BSD-2-Clause | 2021 年 11 月の全球 (pbf 61 GiB、車) で実行時に約 123 GiB の RAM。大きさは入力データにほぼ比例する | [Disk and Memory Requirements](https://github.com/Project-OSRM/osrm-backend/wiki/Disk-and-Memory-Requirements) |
| Valhalla (ルート検索) | MIT | タイル状の階層グラフで、メモリの少ない機器でのオフラインのルート検索を狙った設計と公式に書かれている。iOS と Android でも使われている | [Valhalla docs](https://valhalla.github.io/valhalla/)、[valhalla](https://github.com/valhalla/valhalla) |
| Nominatim 5.3.3 (ジオコーディング) | GPL-3.0 | 最小 2 GB の RAM。全球では 128 GB 以上と 1 TB 以上のディスク、NVMe を推奨 | [Nominatim installation](https://nominatim.org/release-docs/latest/admin/Installation/) |
| Photon (検索) | Apache-2.0 | 全球で約 95 GB のディスク (2026 年時点、年 10% 増)、64 GB の RAM を推奨。SSD を強く推奨 | [photon](https://github.com/komoot/photon) |

## 地図プロダクトでの使いどころ

- 保存: 背景地図は地域で切り出した PMTiles 1 本をローカルの SSD に置く。`pmtiles extract` は bbox か GeoJSON の範囲とズームの上限で切り出せ、元のアーカイブはリモートでもよい。日本全体の OSM 抽出 (Geofabrik の japan-latest.osm.pbf) は 2.4 GB、地方単位では四国 87 MB から関東 499 MB である。Raspberry Pi では SD カードでなく NVMe を使う (k3s の公式も SD と eMMC は書き込みに耐えないと書いている)。
- 計算: (リクエスト時のタイル計算、検索、ルート検索が動くか)
  - タイル配信: PMTiles や MBTiles を返すだけなら go-pmtiles や Martin が arm64 で動くので、Raspberry Pi 5 でも成り立つ (推測)。PostGIS から動的に MVT を作る場合は、DB を同じ機械に載せる分のメモリが要る。
  - ルート検索: OSRM は全球で RAM 123 GiB、入力に比例するという公式の記載から、日本 (2.4 GB) なら数 GiB 程度と見積もれる (推測。61 GiB に対する比で概算しただけで、実測していない)。Valhalla はタイル状のグラフを前提に省メモリとオフラインを狙っているので、小型機ではこちらが候補になる (推測)。
  - 検索: Nominatim は最小 2 GB だが全球の数字しか公式にない。Photon は全球で RAM 64 GB を推奨しており、国単位の数字は公式にない。日本だけの検索を 8 GB や 16 GB の Raspberry Pi 5 で動かせるかは未確認である。
  - オフライン運用: k3s は画像の tar を `/var/lib/rancher/k3s/agent/images/` に置く方式、プライベートレジストリ、組み込みのレジストリミラーの 3 通りでインターネットなしに入れられる。k0s は OCI のイメージバンドルを `/var/lib/k0s/images` に置くと取り込む。MicroK8s にもオフラインの導入手順がある。
- 表現: サーバーは描画しない。庁舎の端末や車載タブレットのブラウザ、アプリの MapLibre に、閉域網の中からスタイル、タイル、フォント、スプライトを配る。外部の CDN やフォント配信に依存したスタイルはオフラインでは崩れるので、スタイルが参照する URL をすべて内側に向ける必要がある (推測)。

## 地図の実装例

- 閉域網の中で `pmtiles serve` を動かし、前段に Caddy などのリバースプロキシを置く。公式は本番では CDN かリバースプロキシの後ろで動かすことを勧めている。Docker イメージ `protomaps/go-pmtiles` もある。
- データの差し替え: 新しい版の PMTiles を別名で置いてから切り替える。Photon は「古い DB の上に展開すると壊れる」と明記しており、更新時は DB 2 つ分の容量が要る。週次の全球と一部の国のダンプは GraphHopper が配っている。
- k3s のオフラインでの更新: 新しい画像 tar と k3s バイナリを差し替えてインストールスクリプトを同じ環境変数で再実行する手動手順と、`rancher/k3s-upgrade` などをプライベートレジストリに入れて system-upgrade-controller で自動化する手順が公式にある。

## 落とし穴

- Raspberry Pi OS は既定で cgroups が有効でなく、k3s を入れる前に起動コマンドラインを書き換える必要がある。Ubuntu 21.10 から 23.10 の Raspberry Pi 版は VXLAN のカーネルモジュールを別に入れる必要がある (24.04 以降は不要)。
- k3s は firewalld や ufw を無効にすることを勧めている。残すなら 6443 番とポッド、サービスの CIDR を通す規則を足す。自治体の閉域網の端末では、ここが情報システム部門との調整点になる (推測)。
- k3s のオフライン導入では、デフォルトルートのないノードにダミーのルートを足す必要がある (主 IP の判定と kube-proxy のため)。
- k3s の画像 tar を手で置く方式では、k3s は起動時にすべての画像があることを保証しないので、消えた画像は手で取り込み直す。
- `pmtiles extract` の元のアーカイブはクラスタ化されている必要がある (tippecanoe、planetiler、pmtiles CLI の出力はクラスタ化済み)。
- Nominatim (GPL-3.0) を閉域網で使うだけなら配布にあたらないが、改変したものを機器ごと顧客に納品すると配布になり、ソースの提供義務が生じる (GPL の一般的な解釈。法的助言ではない)。GPL-3.0 はネットワーク越しの利用 (SaaS) ではソース提供義務を生じない。AGPL ならネットワーク越しでも生じる。
- OSM のデータ (ODbL) を使う場合、帰属表示と ODbL であることの明示が要り、データを改変・加工したデータベースを配るなら同じライセンスで配る必要がある。タイルや画像のような生成物 (produced works) の表示の仕方は OSM の帰属ガイドラインに従う。
- Raspberry Pi 5 は 5V 5A の電源が要り、足りない電源では不具合が出ると公式が警告している。車載や災害現場の電源ではここが制約になる (推測)。

## 出典

- https://www.raspberrypi.com/products/raspberry-pi-5/ (CPU、RAM の種類、PCIe 2.0 x1、microSD と M.2 HAT、5V 5A 電源、16 GB 版の価格)
- https://docs.k3s.io/installation/requirements (k3s の最小構成、SSD 推奨、Raspberry Pi の注意、対応アーキテクチャ、OS ごとの注意)
- https://docs.k3s.io/installation/airgap (k3s のオフライン導入 3 方式と更新手順)
- https://docs.k0sproject.io/stable/system-requirements/ (k0s の最小構成と対応アーキテクチャ)
- https://docs.k0sproject.io/stable/airgap-install/ (k0s のイメージバンドルの置き場所と取り込み)
- https://canonical.com/microk8s/docs/getting-started (MicroK8s の最小と推奨の構成、snap での導入、オフライン導入の案内)
- https://docs.protomaps.com/pmtiles/cli (pmtiles の serve、extract、cluster、Docker イメージ、リバースプロキシの推奨)
- https://github.com/protomaps/go-pmtiles (BSD-3-Clause。v1.31.2 のリリース資産を GitHub API で確認)
- https://github.com/maplibre/martin (対応ソースとライセンス。v1.16.1 の aarch64 資産を GitHub API で確認)
- https://github.com/Project-OSRM/osrm-backend/wiki/Disk-and-Memory-Requirements (OSRM の前処理と実行時のメモリ、入力への比例)
- https://valhalla.github.io/valhalla/ (タイル状グラフ、省メモリとオフラインのルート検索、MIT)
- https://nominatim.org/release-docs/latest/admin/Installation/ (Nominatim 5.3.3 のハードウェア要件)
- https://github.com/komoot/photon (Photon の必要資源、Apache-2.0、ダンプの更新方法)
- https://download.geofabrik.de/asia/japan.html (日本と地方ごとの pbf の大きさ)
- https://www.openstreetmap.org/copyright (ODbL の帰属表示と継承の要件)
- GitHub API の license フィールドで OSRM (BSD-2-Clause)、Nominatim (GPL-3.0)、Photon (Apache-2.0) を確認

## 未確認のこと

- 日本だけのデータで OSRM、Valhalla、Photon、Nominatim を Raspberry Pi 5 (8 GB、16 GB) で動かした時のメモリ、前処理時間、応答時間の実測。
- ミニ PC の具体的な機種ごとの性能と価格。
- MicroK8s の対応アーキテクチャ一覧 (公式の入門ページには載っていない)。
- 車載や災害現場での耐環境性 (温度、振動、停電時の書き込み保護) に関する公式の資料。
- Martin の Docker イメージが arm64 に対応しているか (リリース資産のバイナリは確認したが、コンテナイメージは見ていない)。
- k0s のオフライン環境での更新手順 (公式ページに更新の節がない)。
