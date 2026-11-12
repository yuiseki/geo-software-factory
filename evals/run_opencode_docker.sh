#!/usr/bin/env bash
# Run OpenCode inside Docker on a workdir made by bench.py.
#
# CPU, memory and process limits are enforced by Docker (cgroups) and are part of the eval condition: baseline
# and skills runs use the same image, limits and model; only the workdir differs. Nothing of the everyday
# OpenCode is brought in (no config, auth or state from $HOME). The state lives in the container and goes with it.
#
# Usage: evals/run_opencode_docker.sh [--prompt FILE] [--dry-run] WORKDIR [opencode args...]
#
# Environment (defaults are the eval conditions):
#   EVAL_IMAGE=geo-software-factory-evals-opencode  EVAL_CPUSET=0-7  EVAL_CPUS=8  EVAL_MEMORY=16g  EVAL_PIDS=512
#   EVAL_MODEL=opencode/deepseek-v4.1-flash-free  EVAL_MINUTES=30 (cut off inside the container, exit code 124)
set -euo pipefail

IMAGE=${EVAL_IMAGE:-geo-software-factory-evals-opencode}
CPUSET=${EVAL_CPUSET:-0-7}
CPUS=${EVAL_CPUS:-8}
MEMORY=${EVAL_MEMORY:-16g}
PIDS=${EVAL_PIDS:-512}
MODEL=${EVAL_MODEL:-opencode/deepseek-v4.1-flash-free}
MINUTES=${EVAL_MINUTES:-30}
CONFIG='{"$schema":"https://opencode.ai/config.json","share":"disabled","autoupdate":false}'

dry=0 prompt=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run) dry=1; shift ;;
    --prompt) prompt=${2:?--prompt needs a file}; shift 2 ;;
    --) shift; break ;;
    -*) echo "unknown option $1" >&2; exit 2 ;;
    *) break ;;
  esac
done
[[ $# -ge 1 ]] || { echo "usage: $0 [--prompt FILE] [--dry-run] WORKDIR [opencode args...]" >&2; exit 2; }
workdir=$(realpath "$1"); shift
[[ -d "$workdir" ]] || { echo "$workdir is not a directory" >&2; exit 2; }
if [[ -e "$workdir/evals" || -e "$workdir/.git" ]]; then
  echo "$workdir contains evals/ or .git; prepare it with evals/bench.py" >&2; exit 2
fi

docker_args=(
  run --rm --init
  --cpuset-cpus="$CPUSET" --cpus="$CPUS"
  --memory="$MEMORY" --memory-swap="$MEMORY"
  --pids-limit="$PIDS"
  --cap-drop=ALL --security-opt=no-new-privileges
  -e OPENCODE_CONFIG_CONTENT="$CONFIG"
  -v "$workdir":/work -w /work
)
if [[ -n "$prompt" ]]; then
  cmd=(docker "${docker_args[@]}" -i "$IMAGE" timeout "${MINUTES}m"
       opencode run --format json --auto --pure --print-logs --dir /work --model "$MODEL" "$@")
  prompt_in=$(realpath "$prompt")
else
  cmd=(docker "${docker_args[@]}" -it "$IMAGE" opencode /work --model "$MODEL" "$@")
fi
if [[ $dry -eq 1 ]]; then printf '%q ' "${cmd[@]}"; echo; exit 0; fi
if [[ -n "${prompt_in:-}" ]]; then exec "${cmd[@]}" < "$prompt_in"; fi
exec "${cmd[@]}"
