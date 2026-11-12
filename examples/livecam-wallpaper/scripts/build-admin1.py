#!/usr/bin/python3
"""Match camera coordinates to Natural Earth 10m admin-1 polygons.

Usage: /usr/bin/python3 scripts/build-admin1.py /path/to/ne_10m_admin_1_states_provinces.zip
"""
import json
import sys
from pathlib import Path
from osgeo import ogr

ogr.UseExceptions()

base = Path(__file__).resolve().parent.parent
source = ogr.Open('/vsizip/' + str(Path(sys.argv[1]).resolve()))
if source is None:
    raise SystemExit('Could not open Natural Earth archive')
layer = source.GetLayer(0)
cameras = json.loads((base / 'public/livecams.json').read_text())['cams']
remaining = {c['id']: (c['lng'], c['lat']) for c in cameras if isinstance(c.get('lat'), (int,float)) and isinstance(c.get('lng'), (int,float))}
assignments = {}
regions = {}
for feature in layer:
    geometry = feature.GetGeometryRef()
    if geometry is None:
        continue
    west, east, south, north = geometry.GetEnvelope()
    for key, (lng, lat) in list(remaining.items()):
        if not west <= lng <= east or not south <= lat <= north:
            continue
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint_2D(lng,lat)
        if not geometry.Intersects(point):
            continue
        region_id = str(feature.GetFID())
        if region_id not in regions:
            simple = geometry.SimplifyPreserveTopology(0.005)
            regions[region_id] = {'type':'Feature', 'properties':{'name':feature.GetField('name')}, 'geometry':json.loads(simple.ExportToJson())}
        assignments[key] = region_id
        del remaining[key]
out = {'assignments':assignments, 'regions':regions}
(base / 'public/camera-admin1.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
print(f'Matched {len(assignments)} cameras; {len(remaining)} unmatched; {len(regions)} regions')
