#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
stage_dir=$(mktemp -d /tmp/livecam-wallpaper-deploy-XXXXXXXX)
mkdir -p "$stage_dir/assets/public"
install -m 644 index.html style.css app.js "$stage_dir/assets/"
install -m 644 public/livecams.json public/camera-admin1.json public/country-codes.json "$stage_dir/assets/public/"
install -m 644 wrangler.jsonc "$stage_dir/"
printf 'Deploy staging directory: %s\n' "$stage_dir"
npx --yes wrangler@4.160.0 deploy --config "$stage_dir/wrangler.jsonc"
