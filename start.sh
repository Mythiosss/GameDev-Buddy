#!/bin/sh
set -eu

export OLLAMA_HOST="${OLLAMA_HOST:-http://127.0.0.1:11434}"
export OLLAMA_MODEL="${OLLAMA_MODEL:-gemma3:4b}"
export PORT="${PORT:-8000}"

run_ollama() {
  env -u OLLAMA_HOST ollama "$@"
}

run_ollama serve &
ollama_pid=$!
uvicorn_pid=""

stop() {
  if [ -n "$uvicorn_pid" ]; then
    kill "$uvicorn_pid" 2>/dev/null || true
  fi
  kill "$ollama_pid" 2>/dev/null || true
}

trap stop INT TERM EXIT

until run_ollama list >/dev/null 2>&1; do
  if ! kill -0 "$ollama_pid" 2>/dev/null; then
    exit 1
  fi
  sleep 1
done

run_ollama pull "$OLLAMA_MODEL"

uvicorn backend.main:app --host 0.0.0.0 --port "$PORT" &
uvicorn_pid=$!
wait "$uvicorn_pid"
