import * as maplibregl from 'https://unpkg.com/maplibre-gl@6.14.0/dist/maplibre-gl.mjs';

'use strict';

const SWITCH_MS = 3 * 60 * 1000;
const JAPAN_WEIGHT = 0.7;
const FAILED_CAMERA_COOLDOWN_MS = 10 * 60 * 1000;
const MAX_CONSECUTIVE_ERRORS = 5;
const VIDEO_ERROR_CODES = new Set([2, 5, 100, 101, 150]);
const failedCameras = new Map();
const stage = document.querySelector('#stage');
let cameras = [];
let countries = null;
let countryCodes = {};
let admin1 = null;
let slots = [];

const youtubeReady = new Promise(resolve => {
  if (window.YT && window.YT.Player) return resolve(window.YT);
  let settled = false;
  const finish = api => {
    if (settled) return;
    settled = true;
    resolve(api);
  };
  window.onYouTubeIframeAPIReady = () => finish(window.YT);
  const script = document.createElement('script');
  script.src = 'https://www.youtube.com/iframe_api';
  script.onerror = () => finish(null);
  document.head.append(script);
  setTimeout(() => finish(null), 15000);
});

function eligible(camera) {
  return camera && /^[\w-]{11}$/.test(camera.id) && Number.isFinite(camera.lat) && Math.abs(camera.lat) <= 90 && Number.isFinite(camera.lng) && Math.abs(camera.lng) <= 180;
}
function chooseCamera(excluded) {
  const now = Date.now();
  for (const [id, until] of failedCameras) if (until <= now) failedCameras.delete(id);
  const available = cameras.filter(camera => !excluded.has(camera.id) && !failedCameras.has(camera.id));
  const pool = available.length ? available : cameras;
  const japan = pool.filter(camera => camera.country === 'JP');
  const abroad = pool.filter(camera => camera.country !== 'JP');
  const chosenPool = japan.length && abroad.length ? (Math.random() < JAPAN_WEIGHT ? japan : abroad) : pool;
  return chosenPool[Math.floor(Math.random() * chosenPool.length)];
}
function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}
function renderGlobe(container, camera) {
  if (!window.d3 || !countries) return;
  const size = 160;
  const projection = d3.geoOrthographic().scale(72).translate([80,80]).rotate([-camera.lng, -camera.lat]);
  const path = d3.geoPath(projection);
  const svg = d3.select(container).append('svg').attr('viewBox', `0 0 ${size} ${size}`).attr('role','img').attr('aria-label','地球上の位置');
  svg.append('circle').attr('cx',80).attr('cy',80).attr('r',72).attr('fill','#d8e1df');
  svg.append('path').datum(d3.geoGraticule10()).attr('d',path).attr('fill','none').attr('stroke','#b2c3bf').attr('stroke-width',0.6);
  svg.append('path').datum(countries).attr('d',path).attr('fill','#7e9992').attr('stroke','#d8e1df').attr('stroke-width',0.35);
  const country = countries.features.find(feature => Number(feature.id) === Number(countryCodes[camera.country]) && countryCodes[camera.country]);
  if (country) svg.append('path').datum(country).attr('d',path).attr('fill','#d7654d').attr('stroke','#fff').attr('stroke-width',1);
  svg.append('circle').attr('cx',80).attr('cy',80).attr('r',72).attr('fill','none').attr('stroke','#a2b3ae').attr('stroke-width',1);
}
function cameraRegionPart(region, camera) {
  if (region.geometry.type !== 'MultiPolygon') return region;
  const position = [camera.lng, camera.lat];
  for (const coordinates of region.geometry.coordinates) {
    const part = turf.polygon(coordinates);
    if (turf.booleanPointInPolygon(position, part)) return part;
  }
  // Simplification can put coastal cameras just outside the polygon.
  // A fixed camera-centred view is more useful than fitting distant islands.
  return null;
}
function dispose(slot) {
  if (slot.timer) clearTimeout(slot.timer);
  if (slot.retryTimer) clearTimeout(slot.retryTimer);
  if (slot.player) slot.player.destroy();
  if (slot.map) slot.map.remove();
  slot.node.remove();
}
function updateSlot(slot, nextSwitchMs = SWITCH_MS) {
  if (slot.timer) clearTimeout(slot.timer);
  if (slot.retryTimer) clearTimeout(slot.retryTimer);
  slot.retryTimer = null;
  if (slot.player) { slot.player.destroy(); slot.player = null; }
  if (slot.map) { slot.map.remove(); slot.map = null; }
  const excluded = new Set(slots.filter(other => other !== slot && other.camera).map(other => other.camera.id));
  if (slot.camera) excluded.add(slot.camera.id);
  const camera = chooseCamera(excluded);
  slot.camera = camera;
  slot.node.replaceChildren();
  const content = element('div','tile-content');
  const video = element('div','video');
  const iframe = document.createElement('iframe');
  iframe.src = `https://www.youtube.com/embed/${encodeURIComponent(camera.id)}?autoplay=1&mute=1&playsinline=1&rel=0&enablejsapi=1&origin=${encodeURIComponent(window.location.origin)}`;
  iframe.title = `${camera.spot || camera.city || 'ライブカメラ'}のライブ映像`;
  iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
  iframe.allowFullscreen = true;
  iframe.referrerPolicy = 'strict-origin-when-cross-origin';
  video.append(iframe);
  const location = element('aside','location');
  const head = element('div','location-head');
  const globe = element('div','globe');
  renderGlobe(globe,camera);
  const place = element('div','place');
  const region = admin1 && admin1.regions[admin1.assignments[camera.id]];
  place.append(element('h2','',region ? (region.properties.name || camera.city || '場所') : `${camera.city || camera.country || '場所'}（境界未特定）`));
  head.append(place);
  const mapNode = element('div','map');
  mapNode.setAttribute('aria-label','カメラ周辺の地図');
  location.append(mapNode,globe,head);
  content.append(video,location);
  const progress = element('div','switch-progress');
  progress.setAttribute('aria-hidden','true');
  progress.style.setProperty('--switch-duration', `${nextSwitchMs}ms`);
  slot.node.append(content,progress);
  youtubeReady.then(api => {
    if (!api || slot.camera !== camera || !slot.node.isConnected) return;
    slot.player = new api.Player(iframe, {
      events: {
        onReady: event => { event.target.mute(); },
        onStateChange: event => { if (slot.camera === camera && event.data === 1) slot.failures = 0; },
        onError: event => {
          if (slot.camera !== camera || slot.retryTimer || !VIDEO_ERROR_CODES.has(event.data)) return;
          failedCameras.set(camera.id, Date.now() + FAILED_CAMERA_COOLDOWN_MS);
          slot.failures++;
          if (slot.failures <= MAX_CONSECUTIVE_ERRORS) {
            slot.retryTimer = setTimeout(() => updateSlot(slot), 2000);
          }
        }
      }
    });
  });
  if (maplibregl) {
    slot.map = new maplibregl.Map({container:mapNode,style:'https://tiles.openfreemap.org/styles/positron',center:[camera.lng,camera.lat],zoom:4.5,interactive:false,attributionControl:false});
    slot.map.addControl(new maplibregl.AttributionControl({compact:true}));
    new maplibregl.Marker({color:'#b94330'}).setLngLat([camera.lng, camera.lat]).addTo(slot.map);
    // MapLibre 6 initially expands even compact controls when attribution arrives.
    const map = slot.map;
    const collapseInitialAttribution = () => {
      const control = map.getContainer().querySelector('.maplibregl-ctrl-attrib.maplibregl-compact');
      if (!control) return;
      control.classList.remove('maplibregl-compact-show');
      control.removeAttribute('open');
      map.off('sourcedata', collapseInitialAttribution);
      map.off('styledata', collapseInitialAttribution);
    };
    map.on('sourcedata', collapseInitialAttribution);
    map.on('styledata', collapseInitialAttribution);
    if (region) slot.map.on('load', () => {
      if (!slot.map) return;
      slot.map.addSource('region', {type:'geojson', data:region});
      slot.map.addLayer({id:'region-fill',type:'fill',source:'region',paint:{'fill-color':'#dd644c','fill-opacity':0.38}});
      slot.map.addLayer({id:'region-outline',type:'line',source:'region',paint:{'line-color':'#b94330','line-width':2}});
      if (window.turf) {
        const part = cameraRegionPart(region, camera);
        if (part) {
          const [west, south, east, north] = turf.bbox(part);
          slot.map.fitBounds([[west, south], [east, north]], {padding:12, maxZoom:8, duration:0});
        } else {
          slot.map.jumpTo({center:[camera.lng, camera.lat], zoom:7});
        }
      }
    });
  } else {
    mapNode.textContent = '地図を読み込めませんでした';
  }
  slot.timer = setTimeout(() => { slot.failures = 0; updateSlot(slot); }, nextSwitchMs);
}
function setMode(count) {
  slots.forEach(dispose);
  slots = [];
  stage.replaceChildren();
  stage.classList.toggle('multi',count > 1);
  for (let i=0; i<count; i++) {
    const slot = {node:element('article','tile'),camera:null,map:null,timer:null,retryTimer:null,player:null,failures:0};
    slots.push(slot);
    stage.append(slot.node);
    updateSlot(slot, SWITCH_MS * (i + 1) / count);
  }
}
(async () => {
  try {
    const [response, world, regions, codes] = await Promise.all([
      fetch('public/livecams.json'),
      fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json').then(r => r.ok ? r.json() : null).catch(() => null),
      fetch('public/camera-admin1.json').then(r => r.ok ? r.json() : null).catch(() => null),
      fetch('public/country-codes.json').then(r => r.ok ? r.json() : {}).catch(() => ({}))
    ]);
    if (!response.ok) throw new Error('camera list unavailable');
    const data = await response.json();
    cameras = (Array.isArray(data) ? data : data.cams || []).filter(eligible);
    if (!cameras.length) throw new Error('no valid cameras');
    admin1 = regions;
    countryCodes = codes;
    if (world && window.topojson) countries = topojson.feature(world,world.objects.countries);
    setMode(4);
  } catch (error) {
    stage.replaceChildren(element('p','message','ライブカメラの一覧を読み込めませんでした。ローカルサーバーから開いてください。'));
    console.error(error);
  }
})();
