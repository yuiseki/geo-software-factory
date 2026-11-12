# iTunes Search API と Apple のバッジの決まり

対象: 地図の上の地点やアルバムに、iTunes Search API (itunes.apple.com/search、/lookup) で取った 30 秒の試聴 (previewUrl) やアルバムのアートワーク (artworkUrl100 など) を出す、再生する場合の、Search API の文書の「Legal」の条件、Apple Services Performance Partner Program、iTunes Store と Apple Music の Identity Guidelines (バッジ、リンク、クレジット行)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-11 |
| 根拠 (法令名と条、規約の版) | 法令ではなく Apple との条件。iTunes Search API の文書 (Apple Services Performance Partner Program のサイト、https://performance-partners.apple.com/search-api 、ページのフッターは Copyright © 2022、条件の版や改定日の記載なし) の「Legal」の節 (i) から (vi)。同じ条件は旧版の文書 (https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html 、Updated: 2017-09-19) にもある。iTunes Identity Guidelines (https://marketing.services.apple/itunes-identity-guidelines) と Apple Music Identity Guidelines (https://marketing.services.apple/apple-music-identity-guidelines)。どちらもフッターは © 2023 で、改定日の記載なし |
| 所管・管理者 | Apple Inc.。アフィリエイトは Apple Services Performance Partner Program (Partnerize のネットワークで運営) |

## 何を求める決まりか

目的は、試聴やアートワーク (Apple の言う「Promo Content」) を、ストアの商品を売るための宣伝に限って使わせることにある。Search API の文書の Overview は、試聴、ミュージックビデオ、アルバムアート、アプリのアイコンを「ストアの内容の宣伝のためだけに使い、娯楽の目的に使わない」こと、試聴などの素材は「ストアのバッジの近くに置く」ことを求める。義務の種類は契約上の条件 (満たせば使ってよい) と表示である。

- Legal の条件 (Search API の文書の「Legal」の節、原文の番号): Promo Content は、その内容自体を宣伝する目的に限り、次をすべて満たす場合に使える。(i) Promo Content の元になった内容を宣伝するページにだけ置く。(ii) Apple が承認した「Download on iTunes」又は「Download on App Store」のバッジの近くに置き、そのバッジは消費者がその内容を買える iTunes の中のページへ直接リンクする。(iii) 曲やミュージックビデオの試聴を含むなら、Promo Content が「provided courtesy of iTunes」であることを示す帰属を付ける。(iv) 曲やミュージックビデオの試聴を含むなら、ストリーミングだけで再生し、ダウンロード、保存、キャッシュ、映像との同期をしない。(v) 宣伝の目的から離れた独立の娯楽の価値のために使わない。(vi) 他の商品やサービスの宣伝に使わない。
- その他の Legal の記述: Apple は Promo Content を「as is」で提供し、非侵害を含む保証をしない。Promo Content について受けた請求は直ちに Apple に回し、Apple に求められたら直ちに取り除く。条件と Promo Content の利用にはカリフォルニア州法が適用される。
- 利用量: Search API はおおむね 1 分に 20 回まで (変わりうる)。それより多く使うなら Enterprise Partner Feed (EPF) を検討するよう書く。大きなサイトは search と lookup の要求にキャッシュの仕組みを置くべきだとする (Search API の文書「Notes」)。この「キャッシュ」は検索結果 (JSON) の要求についてで、試聴のキャッシュの禁止 ((iv)) とは別のことと読める (推測)。
- バッジ (iTunes Identity Guidelines 1.1 から 1.6): Apple が承認したバッジだけを使い、作らない、変えない。現在のバッジは「Buy on」「Pre-order on」「Get it on」iTunes Store で、「iTunes」は翻訳しない (1.2)。オンラインでバッジを使うなら、バッジを使う場所に iTunes Store へのリンクを置く (1.3)。バッジはレイアウトに 1 つ、画像や文の下か右に置き、他の画像より小さくし、主役にしない (1.4)。周りの余白はバッジの高さの 10 分の 1 以上、最小の大きさは印刷 8mm、デジタル 30px (1.5.1)。灰色の縁もバッジの一部で、省かない。
- Apple Music のバッジ (Apple Music Identity Guidelines 1.1 から 1.7、6): 曲やアルバムに Apple Music へリンクするなら「Listen on Apple Music」バッジ。バッジを使う場所には Apple Music へのリンクを置く (6 の冒頭)。最小の大きさは印刷 10mm、デジタル 30px、小さいバッジは 12px 以上 (1.5)。他の音楽サービスのバッジと並べるなら Apple Music を最初に置く (1.3)。
- クレジット行 (iTunes Identity Guidelines 7.1、Apple Music Identity Guidelines 9.2): 使った Apple の商標だけをクレジット行に挙げる。iTunes Store のバッジを使うなら iTunes Store をクレジットする。Apple Music の名前を使うなら「Apple and Apple Music are trademarks of Apple Inc., registered in the U.S. and other countries」。クレジット行は法的な表記を置く場所に 1 回だけ置く。
- 承認 (iTunes Identity Guidelines 6、Apple Music Identity Guidelines 8.1): 多くの宣伝物は承認が要らない。テレビや印刷、目立つ宣伝の形式、Apple 製品が写る写真や動画は事前の書面の承認が要る。

## 地図プロダクトで当たる場面

| 場面 | 当たるか | 根拠 | 出典 |
|---|---|---|---|
| 世界地図に千を超えるアルバムを置き、実行時に lookup で試聴の URL とアートワークを取って鳴らす | 当たる。試聴とアートワークは Promo Content で、(i) から (vi) をすべて満たす場合に限って使える。各アルバムの近くに、その商品の購入ページへ直接リンクするバッジを置き、試聴には「provided courtesy of iTunes」の帰属を付ける | Search API の文書「Legal」 | https://performance-partners.apple.com/search-api |
| 試聴を Web Audio に読み込み、加工 (フィルタ、空間化、重ね合わせ) して鳴らす | (iv) の「ストリーミングだけで再生し、ダウンロード、保存、キャッシュしない」と、(v) の「独立の娯楽の価値のために使わない」に照らして確かめる必要がある。Web Audio で音声を復号してメモリに持つことが「保存」や「キャッシュ」に当たるか、地図の体験そのものが「独立の娯楽の価値」に当たるかは書かれていない (推測)。加工を許す・禁じる明文は見つからなかった (未確認) | Search API の文書「Legal」(iv)、(v) | 同上 |
| 試聴の音声ファイルやアートワークを自社のサーバや CDN に複製して配る | 試聴は (iv) でダウンロード、保存、キャッシュが禁止。アートワークの保存を明示に禁じる文は Legal の節に無いが、宣伝の目的と (i) の条件は同じくかかる (推測) | Search API の文書「Legal」(iv) | 同上 |
| lookup の結果 (JSON) を地図の読み込みのたびに 1,800 件分取りに行く | 1 分に 20 回ほどの制限があり、大きなサイトにはキャッシュの仕組みを求めている。実行時にまとめて取ると制限を超えうる (推測) | Search API の文書「Notes」 | 同上 |
| アルバムの点のポップアップに Apple Music と他社の音楽サービスのバッジを並べる | Apple Music のバッジを最初に置き、ロックアップでなくバッジを使う | Apple Music Identity Guidelines 1.3、2.3 | https://marketing.services.apple/apple-music-identity-guidelines |
| 曲を試聴できる地図を、広告やスポンサーの宣伝にも使う | (vi) の「他の商品やサービスの宣伝に使わない」に照らして確かめる。ページ内の広告が「Promo Content を他の商品の宣伝に使う」に当たるかは書かれていない (推測) | Search API の文書「Legal」(vi) | https://performance-partners.apple.com/search-api |
| ブラウザから itunes.apple.com や試聴の配信元に直接取りに行く | 利用者の端末から Apple に情報が送られる。電気通信事業法の外部送信規律に当たりうる | 外部送信規律 | [external-transmission](external-transmission.md) |

## 当たらない場面

- 曲やミュージックビデオの試聴を含まない Promo Content (アートワークだけ) には、(iii) の帰属と (iv) のストリーミングだけの条件は書かれていない (条文の読み)。(i)、(ii)、(v)、(vi) はかかる。
- アフィリエイトのリンクを使うこと自体は条件ではない。Performance Partner Program は、ストアへのリンクから生じた売上に手数料を払う任意の仕組みで、別の申し込みが要る (Search API の文書 Overview、Performance Partner の FAQ)。
- 多くの宣伝物 (ウェブやアプリの通常の掲載) は、バッジの使用に Apple の承認を要しない (iTunes Identity Guidelines 6、Apple Music Identity Guidelines 8.1)。

## 求められる手続き・表示

- 手続き (申請先、期間、費用): Search API の利用に申請や API キーは無い (文書に登録の手順が無い。条件への同意の手続も書かれていない)。アフィリエイトの手数料を受けるなら Performance Partner Program に申し込む。テレビ、印刷、目立つ宣伝の形式は Apple の書面の承認 (少なくとも 7 営業日前に提出、返事が無いことは承認ではない) が要る (Apple Music Identity Guidelines 8.2)。
- 表示の内容: (1) 各アルバムの近くに、購入ページへ直接リンクするバッジ、(2) 試聴には「provided courtesy of iTunes」の帰属、(3) 使った商標のクレジット行を法的な表記の場所に 1 回。
- 表示の書き方 (公式の例): 帰属の文言は Legal の節が引用符で示す「provided courtesy of iTunes」。クレジット行の例は「Apple and Apple Music are trademarks of Apple Inc., registered in the U.S. and other countries」(Apple Music Identity Guidelines 9.2)、iTunes Store のバッジは「... and iTunes Store are trademarks of Apple Inc., registered in the U.S. and other countries」の形で、使った商標だけを挙げる (iTunes Identity Guidelines 7.1)。
- 公開の前に確かめること: (1) 地図が「元の内容を宣伝するページ」といえる作りか ((i)、(v))、(2) バッジが試聴やアートワークの近くにあり、購入ページへ直接リンクするか ((ii))、(3) 試聴に帰属が付いているか ((iii))、(4) 試聴をダウンロード、保存、キャッシュしていないか (Service Worker のキャッシュ、CDN、ビルド時の取り込みを含む) ((iv))、(5) lookup の呼び出しの回数とキャッシュの仕組み、(6) バッジの種類と大きさ (デジタル 30px 以上)、余白、置き場所、(7) 使った商標のクレジット行。

## 守らなかった場合

- Apple に求められたら Promo Content を直ちに取り除く義務がある (Search API の文書「Legal」)。
- バッジやロゴの使い方の違反に対する措置は、Identity Guidelines には書かれていない (本稿で確かめた範囲)。商標の使い方の一般の決まりは Guidelines for Using Apple Trademarks and Copyrights (https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html) にあるが、本稿では読んでいない。
- 利用量を超えたときの扱い (遮断されるか) は書かれていない (未確認)。

## 判断に迷う点

- 「Download on iTunes」のバッジ: Search API の Legal の節は (ii) で「Download on iTunes」又は「Download on App Store」のバッジを挙げるが、現在の iTunes Identity Guidelines のバッジは「Buy on」「Pre-order on」「Get it on」iTunes Store で、「Download on iTunes」は見当たらない。どのバッジで (ii) を満たせるかは公式に示されていない。現在の Guidelines の「Get it on iTunes Store」で代えるのが一つの読み方である (推測)。Apple Music へのリンク (Listen on Apple Music) で (ii) の「iTunes の中の購入ページ」を満たせるかも書かれていない (推測)。
- 音を中心にした地図の体験が、宣伝の目的から離れた「独立の娯楽の価値」((v)) に当たるか。条件は宣伝ページに置くことを前提にしており、試聴を作品の素材として鳴らす使い方は想定の外にあると読める (推測)。
- Search API の文書は Performance Partner Program のサイトにあり、プログラムに参加しない利用者にも Legal の条件がかかるかは明示されていない。文書の Overview は Search API の利用者一般に向けて書かれているので、かかると読むのが自然である (推測)。

## 出典

- https://performance-partners.apple.com/search-api : iTunes Search API の文書 (Overview、Notes の 1 分 20 回とキャッシュ、結果の previewUrl と artworkUrl100、Legal の (i) から (vi))。2026-11-11 確認
- https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html : 旧版の文書 (Updated: 2017-09-19)。Legal の条件は現行の文書と同じ趣旨。2026-11-11 確認
- https://marketing.services.apple/itunes-identity-guidelines : iTunes Store のバッジ、リンク、最小の大きさ、クレジット行、承認。2026-11-11 確認
- https://marketing.services.apple/apple-music-identity-guidelines : Apple Music のバッジ、リンク、最小の大きさ、クレジット行、承認。2026-11-11 確認
- https://performance-partners.apple.com/faq 、https://performance-partners.apple.com/linking : アフィリエイトの仕組み (Partnerize、別の申し込み)。2026-11-11 確認

## 未確認のこと

- Search API の文書が「Caching Architecture later in this document」と参照するキャッシュの節。現行のページには見当たらなかった。
- Performance Partner Program の参加契約の本文 (https://performance-partners.apple.com/terms は 2026-11-11 に 404)。
- Apple Media Services の利用規約 (エンドユーザー向け) と、試聴の配信元のサーバに直接アクセスすることの関係。
- 試聴を Web Audio で加工して鳴らすことを許す、又は禁じる明文。
- Guidelines for Using Apple Trademarks and Copyrights の本文。
- 2,000 件近い lookup を 1 回の要求でまとめられる件数の上限 (id をカンマで並べる例はあるが、上限は書かれていない)。
