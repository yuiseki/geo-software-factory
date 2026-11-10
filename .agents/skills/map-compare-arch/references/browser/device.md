# 端末の機能

対象: Geolocation、DeviceOrientation、Screen Wake Lock、WebXR、Web Share、Badging、Notifications と Push、Web NFC、カメラ (getUserMedia)

## メタ情報

| 項目 | 値 |
|---|---|
| 確かめた日 | 2026-11-10 (版の数字は MDN browser-compat-data 8.1.8 (2026-11-02 23:19 JST 生成) と web-features 3.45.0 で確かめた) |
| 仕様と標準化の段階 (W3C / WHATWG / WICG、草案か勧告か) | Geolocation は W3C Candidate Recommendation Draft (2026-11-05 版)。DeviceOrientation Event は W3C Candidate Recommendation Draft。Screen Wake Lock は W3C Working Draft (2026-11-10 版)。WebXR Device API は W3C Candidate Recommendation Draft。Web Share は W3C Recommendation (2023-05-19)。Badging は W3C Working Draft (2026-04-27 版)。Push API は W3C Working Draft (2026-11-09 版)。Notifications は WHATWG の Living Standard。Media Capture and Streams (getUserMedia) は W3C Candidate Recommendation Draft (2025-10-09 版)。Web NFC は W3C の Community Group (w3c-cg) の文書。`<geolocation>` 要素は WICG の PEPC の文書 |
| Baseline の状態 (Widely available / Newly available / 未達) | Geolocation、getUserMedia (media-capture)、Permissions API は Widely available。DeviceOrientation Event は Widely available (2026-03-18 から)。Push と、アプリとしての Notifications (notifications-apps) は Widely available (2025-09-27 から)。Screen Wake Lock は Newly available (2025-03-31 から)。WebXR、Web Share、Badging、Web NFC、`<geolocation>` 要素は未達 |

## ブラウザの対応

API ごとに、対応した版を書く。iOS では全ブラウザが WebKit を使うので、iOS Safari の欄が iOS 全体の対応になる。

| API | Chrome / Edge | Firefox | Safari (macOS) | Safari (iOS / iPadOS) | Android の WebView | 出典 |
|---|---|---|---|---|---|---|
| Geolocation (`getCurrentPosition`、`watchPosition`) | 5 / 12 | 3.5 | 5 | 3 以前から | 4.4 | MDN BCD `api.Geolocation` |
| `<geolocation>` 要素 | 144 | 未対応 | 未対応 | 未対応 | 未対応 | MDN BCD `html.elements.geolocation`、Chrome 144 の記事 |
| DeviceOrientationEvent | 7 / 12 (Chrome 50 から相対値。絶対値は `deviceorientationabsolute`) | 6 | 17 | 4.2 | 3 | MDN BCD `api.DeviceOrientationEvent` |
| `deviceorientationabsolute` イベント | 50 / 79 | 110 | 未対応 | 未対応 | 50 | MDN BCD `api.Window.deviceorientationabsolute_event` |
| `DeviceOrientationEvent.requestPermission()` | 152 | 未対応 | 未対応 | 14.5 | 152 | MDN BCD `api.DeviceOrientationEvent.requestPermission_static` |
| AbsoluteOrientationSensor (Generic Sensor) | 67 / 79 | 未対応 | 未対応 | 未対応 | 67 | MDN BCD `api.AbsoluteOrientationSensor` |
| Screen Wake Lock | 84 | 126 | 16.4 | 18.4 (16.4〜18.3 はホーム画面の Web アプリで動かない) | 84 | MDN BCD `api.WakeLock` |
| WebXR (`navigator.xr`) | 79 (Android の Chrome も 79) | 未対応 | 未対応 (visionOS の Safari 18.0 から immersive-vr に対応) | 未対応 | 未対応 | MDN BCD `api.XRSystem`、WebKit の Safari 18.0 記事 |
| WebXR の AR (immersive-ar) | 86 | 未対応 | 未対応 | 未対応 | 未対応 | web-features `webxr-ar` |
| WebXR Hit Test | 81 | 未対応 | 未対応 | 未対応 | 未対応 | web-features `webxr-hit-test` |
| WebXR Anchors | 85 | 未対応 | 未対応 | 未対応 | 未対応 | web-features `webxr-anchors` |
| Web Share (`navigator.share`) | 128 (89〜127 は Windows と ChromeOS だけ)、Android の Chrome は 61 / Edge 93 | 71 からフラグ付き (Android の Firefox は 79) | 12.1 | 12.2 | 未対応 | MDN BCD `api.Navigator.share` |
| Badging (`navigator.setAppBadge`) | 81 (Windows と macOS、ChromeOS は 91)。Android の Chrome は未対応 | 未対応 | 17 (macOS Sonoma 以上でインストールした Web アプリ) | 16.4 (ホーム画面に置いた Web アプリだけ) | 未対応 | MDN BCD `api.Navigator.setAppBadge` |
| Notifications | 20 / 14 (Android の Chrome は 42 から Service Worker 経由だけ) | 22 | 7 | 16.4 (ホーム画面に置いた Web アプリだけ。Service Worker 経由だけ) | 未対応 | MDN BCD `api.Notification` |
| Push API (`PushManager`) | 42 / 17 | 44 | 16 (macOS Ventura 以上) | 16.4 (ホーム画面に置いた Web アプリだけ) | 未対応 | MDN BCD `api.PushManager` |
| Declarative Web Push | 未確認 | 未確認 | 18.5 | 18.4 (ホーム画面に置いた Web アプリ) | 未確認 | WebKit の Safari 18.4、18.5 の記事 |
| Web NFC (`NDEFReader`) | Android の Chrome 89 だけ (デスクトップは未対応) | 未対応 | 未対応 | 未対応 | 89 | MDN BCD `api.NDEFReader` |
| getUserMedia | 53 / 12 | 36 | 11 | 11 | 53 | MDN BCD `api.MediaDevices.getUserMedia` |
| Permissions API (`permissions.query`) | 43 / 79 | 46 | 16 | 16 | 未対応 | MDN BCD `api.Permissions.query` |

## 概要

Geolocation は端末の位置を緯度経度と誤差 (メートル) で返し、DeviceOrientation は端末の向きを角度で返す。Screen Wake Lock は画面が暗くなるのを止め、WebXR はカメラ映像や空間に 3D を重ねる。Web Share は OS の共有画面を開き、Badging、Notifications、Push は Web アプリとして通知とアイコンの数字を出す。Web NFC は NFC タグを読み書きし、getUserMedia はカメラとマイクの映像と音声を取る。

## 地図プロダクトでの使いどころ

保存、計算、表現のどれを、ブラウザ・アプリの層に置けるようにするか。

- 保存: 端末で取った位置の軌跡、写真、NFC タグの読み取り結果を端末の中に溜めておき、通信できるときに送る構成にできる (保存先は OPFS や IndexedDB で、本書の範囲外)。
- 計算: 現在地を中心にした範囲検索や、進行方向に合わせた地図の回転を端末の中で計算できる。Geolocation の `heading` は移動中だけ値を持つ (止まっていると null) ので、止まっているときの向きは DeviceOrientation から取る。
- 表現: 現在地の表示と追従 (MapLibre GL JS の GeolocateControl は `watchPosition` を使う)。ナビ中に画面を消さない (Screen Wake Lock)。カメラ映像に方角や施設を重ねる AR 表示 (WebXR の immersive-ar と Hit Test。Android の Chrome だけ)。地図の場所を共有する (Web Share)。災害情報などの通知 (Push)。

## 制約

- 容量と寿命: Wake Lock はページが見えなくなると自動で解除されるので、表示に戻ったときに取り直す (仕様の振る舞い。仕様の該当箇所の引用は未確認)。Geolocation の `watchPosition` は、仕様上、完全に有効で見えている文書にだけ位置を届ける。バックグラウンドでの位置記録は Web では仕様上できない。
- 権限とユーザーの操作が要るか: Geolocation、カメラ、通知は利用者の許可が要る。iOS の DeviceOrientation は `requestPermission()` をユーザーの操作 (タップなど) の中で呼ぶ必要があり、操作が無いと WebKit は NotAllowedError で断る。iOS の Push の許可要求もユーザーの直接の操作の中で行う必要がある。Badging は通知の許可が無いとバッジが出ない (WebKit の記事)。Web Share もユーザーの操作の中で呼ぶ (推測。仕様の該当箇所は未確認)。
- セキュアコンテキスト、クロスオリジン分離 (COOP/COEP) などの前提: Geolocation は安全でない文脈 (HTTP) では PERMISSION_DENIED で失敗する。iframe の中では Permissions Policy の `geolocation` の既定の許可が `'self'` なので、別オリジンの iframe には `allow="geolocation"` が要る。COOP/COEP はどれも要らない。
- iOS / Safari での制限: Push、Notifications、Badging は、ホーム画面に置き、manifest の `display` が standalone か fullscreen の Web アプリでだけ使える。Screen Wake Lock がホーム画面の Web アプリで動くのは iOS 18.4 から。WebXR は iOS では使えない (visionOS だけ)。Web NFC と `deviceorientationabsolute` も無く、方位は非標準の `webkitCompassHeading` から取る。
- WebView (アプリに埋め込んだブラウザ) での制限: Android の WebView は Web Share、Badging、Notifications、Push、WebXR、Permissions API に対応していない (MDN BCD)。iOS の WKWebView では Badging が使えない (WebKit の記事)。Android の WebView で Geolocation を使うには、アプリ側で `WebChromeClient.onGeolocationPermissionsShowPrompt` を実装する必要がある (Android の API リファレンス)。

## 地図の実装例

この API を使っている OSS やライブラリ (地図ライブラリ、PMTiles、DuckDB-Wasm など)。

- MapLibre GL JS の GeolocateControl: `navigator.geolocation.watchPosition` と `getCurrentPosition` を使う。既定値は `enableHighAccuracy: false`、`maximumAge: 0`、`timeout: 6000`。使えるかの判定に `navigator.permissions.query({name: 'geolocation'})` を使い、iOS 16 で query が拒否される場合は `navigator.geolocation` の有無で判定する (src/ui/control/geolocate_control.ts、src/util/geolocation_support.ts)。DeviceOrientation は使っていない。

## 落とし穴

- Geolocation の `accuracy` は仕様では 68% の信頼水準 (1 標準偏差) のメートルである。MDN の記述 (95%) と食い違うので、誤差の円の意味は仕様に合わせて説明する。
- `heading` は止まっているときと取れないときに null になる (以前の仕様は NaN だった)。古い実装の扱いの違いに備える。
- `enableHighAccuracy` はヒントにすぎず、実装は無視してよく、応答が遅くなり電力を使う。`timeout` の既定値は事実上無限で、文書が見えるようになるのと許可を待つ時間は数えない。
- Chrome の DeviceOrientationEvent は 50 から地磁気に対する絶対値ではなく相対値を返す。方位が要るなら Chrome 系では `deviceorientationabsolute`、iOS では `webkitCompassHeading` と、ブラウザごとに取り方が分かれる。
- `requestPermission()` は iOS (MDN BCD では 14.5 から) に加えて Chrome 152 にも入った。`typeof DeviceOrientationEvent.requestPermission === "function"` で iOS かどうかを判定するコードは、Chrome 152 以降で許可の画面を出すようになる (推測)。
- iOS 16.4〜18.3 では Screen Wake Lock の API があるのに、ホーム画面の Web アプリでは動かない (WebKit bug 254545)。機能の有無の判定だけでは足りない。
- iOS の Push は Safari のタブでは使えず、ホーム画面への追加を利用者に頼む導線が要る。
- MapLibre GL JS の判定コードにあるとおり、iOS 16 では `permissions.query({name: 'geolocation'})` が例外を投げる。Permissions API の結果だけで Geolocation の可否を決めない。

## まだ使えないもの、これから使えるもの

提案中、Origin Trial 中、一部のブラウザだけのもの。

- `<geolocation>` 要素: ユーザーの操作で位置の許可と取得を行う HTML 要素。Chrome 144 (紹介記事は 2026-01-13 付) から使える。Firefox と Safari は未対応。chromestatus は Firefox の立場を Positive、Safari を No signal と記録している。
- 位置の精度を選ぶ `accuracyMode` (`"precise"` か `"approximate"`): chromestatus では Proposed で、出荷予定は Android 153、デスクトップ 165。Safari の立場は Support、Firefox は Negative と記録されている。
- WebXR Layers と Plane Detection: chromestatus では Chrome 147 の予定として Proposed。
- カメラとマイクの許可を出す `<camera>`、`<microphone>` 要素: chromestatus では Chrome 153 の予定として Proposed。
- Declarative Web Push (Service Worker 無しで Push の通知を出す): iOS と iPadOS 18.4 (ホーム画面の Web アプリ) と macOS の Safari 18.5 で使える。他のブラウザの対応は未確認。
- visionOS の Safari の WebXR: Safari 18.0 で immersive-vr に対応し、26.2 で WebGPU、27.0 で WebXR Layers のテクスチャ配列の投影レイヤーに対応した。immersive-ar の対応は確認できなかった。

## 出典

- https://github.com/mdn/browser-compat-data (npm @mdn/browser-compat-data 8.1.8 の data.json を取得し、表の各 API の版と注記を確かめた)
- https://github.com/web-platform-dx/web-features (npm web-features 3.45.0 の data.json を取得し、Baseline の状態と日付、WebXR の各機能の版を確かめた)
- https://www.w3.org/TR/geolocation/ (W3C の段階、accuracy が 68% の信頼水準であること、heading が null になる条件、enableHighAccuracy と timeout の意味、安全でない文脈での失敗、見えている文書だけへの更新、Permissions Policy の既定値)
- https://www.w3.org/TR/orientation-event/ 、https://www.w3.org/TR/screen-wake-lock/ 、https://www.w3.org/TR/webxr/ 、https://www.w3.org/TR/web-share/ 、https://www.w3.org/TR/badging/ 、https://www.w3.org/TR/push-api/ 、https://www.w3.org/TR/mediacapture-streams/ (各仕様の W3C の段階)
- https://developer.chrome.com/blog/new-in-chrome-144 と https://developer.chrome.com/blog/geolocation-html-element (Chrome 144 の `<geolocation>` 要素)
- https://chromestatus.com/feature/5125006551416832 (`<geolocation>` 要素と他ブラウザの立場)
- https://chromestatus.com/feature/5143609755828224 (Approximate geolocation の予定と他ブラウザの立場)
- https://chromestatus.com/feature/5915984063889408 (DeviceOrientation の許可要求 API)
- https://chromestatus.com/feature/5177993049800704 、https://chromestatus.com/feature/6634466544058368 (WebXR Plane Detection、WebXR Layers)
- https://chromestatus.com/feature/5153829504024576 (`<camera>`、`<microphone>` 要素)
- https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/ (iOS 16.4 の Web Push の条件)
- https://webkit.org/blog/14112/badging-for-home-screen-web-apps/ (Badging が通知の許可を要し、ホーム画面の Web アプリだけで、WKWebView では使えないこと)
- https://webkit.org/blog/16574/webkit-features-in-safari-18-4/ と https://webkit.org/blog/16535/meet-declarative-web-push/ (Declarative Web Push)
- https://webkit.org/blog/16923/webkit-features-in-safari-18-5/ (macOS の Declarative Web Push)
- https://webkit.org/blog/15865/webkit-features-in-safari-18-0/ (visionOS の WebXR)
- https://webkit.org/blog/17640/webkit-features-for-safari-26-2/ と https://webkit.org/blog/18325/webkit-features-for-safari-27-0/ (visionOS の WebXR の WebGPU 対応と Layers)
- https://webkit.org/b/254545 (iOS のホーム画面の Web アプリで Wake Lock が動かなかった問題。MDN BCD の注記から)
- https://webkit.googlesource.com/WebKit/+/master/Source/WebCore/dom/DeviceOrientationEvent.idl (`webkitCompassHeading` の定義)
- https://webkit.googlesource.com/WebKit/+/1a79bee400eb09e4e61992ad877612506d12b02d/LayoutTests/fast/device-orientation/device-orientation-request-permission-user-gesture-expected.txt (ユーザーの操作が無い許可要求が断られること)
- https://developer.android.com/reference/android/webkit/WebChromeClient (WebView で Geolocation の許可を扱う `onGeolocationPermissionsShowPrompt`)
- https://github.com/maplibre/maplibre-gl-js/blob/main/src/ui/control/geolocate_control.ts と https://github.com/maplibre/maplibre-gl-js/blob/main/src/util/geolocation_support.ts (GeolocateControl の既定値と判定方法)

## 未確認のこと

- iOS の `DeviceOrientationEvent.requestPermission()` が入った版。MDN BCD は 14.5 とするが、iOS 13 から使えたとする解説が多く、WebKit の一次資料で確かめていない。
- Screen Wake Lock がページを隠したときに自動で解除される挙動の、仕様の該当箇所。
- Web Share が一時的なユーザーの操作 (transient activation) を要することの、仕様の該当箇所。
- iOS で利用者が「正確な位置情報」を切ったときに、Web の Geolocation の `accuracy` がどう変わるか。
- Chrome と Firefox の Declarative Web Push の対応状況。
- visionOS の Safari の WebXR で immersive-ar が使えるか。
- WebXR を使った AR の地図表示の OSS 実例 (地図ライブラリとの組み合わせ)。
- Android の WebView で Screen Wake Lock と getUserMedia を使うときにアプリ側で要る設定。
