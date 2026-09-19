#!/usr/bin/env bash
# One-shot setup for the Maestro dataset workbench at https://maestro.enrica.ai
#
#   bash ~/maestro_setup.sh
#
# 1. Adds maestro.enrica.ai -> localhost:8090 to the Cloudflare Tunnel ingress (asks for sudo).
# 2. Restarts the tunnel connector (sudo).
# 3. Installs and starts the user service that keeps the workbench running.
# 4. Tells you where the login link is.
#
# Safe to re-run: every step checks its own state first.

set -euo pipefail

EXP="$HOME/git/maestro/experiments/001_ace_audio_personalization"
UNIT_SRC="$EXP/deploy/maestro-web.service"
UNIT_DST="$HOME/.config/systemd/user/maestro-web.service"
ENV_FILE="$HOME/.config/maestro/web.env"
CF_CONFIG="/etc/cloudflared/config.yml"
HOST_NAME="maestro.enrica.ai"
PORT=8090

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

[ -f "$UNIT_SRC" ] || { echo "Missing $UNIT_SRC. Pull the maestro repo first."; exit 1; }
[ -x "$EXP/.venv/bin/maestro-ace" ] || { echo "Missing venv. Run: cd $EXP && uv sync --extra web --extra youtube"; exit 1; }

# ---------------------------------------------------------------- token
say "1/4 Access token"
mkdir -p "$(dirname "$ENV_FILE")"
if [ ! -s "$ENV_FILE" ]; then
  (umask 077; printf 'MAESTRO_WEB_TOKEN=%s\n' "$(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')" > "$ENV_FILE")
  echo "created $ENV_FILE"
else
  echo "keeping existing $ENV_FILE"
fi
chmod 600 "$ENV_FILE"

# ---------------------------------------------------------------- tunnel ingress
say "2/4 Cloudflare Tunnel ingress ($CF_CONFIG)"
if sudo grep -q "hostname: $HOST_NAME" "$CF_CONFIG"; then
  echo "$HOST_NAME already routed"
else
  sudo cp "$CF_CONFIG" "$CF_CONFIG.bak-$(date +%Y%m%d-%H%M%S)"
  sudo python3 - "$CF_CONFIG" "$HOST_NAME" "$PORT" <<'PY'
import sys
path, host, port = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(path).read()
marker = "  - service: http_status:404"
if marker not in text:
    sys.exit(f"Could not find the catch-all rule {marker!r} in {path}; edit it by hand.")
rule = f"  - hostname: {host}\n    service: http://localhost:{port}\n"
open(path, "w").write(text.replace(marker, rule + marker, 1))
print(f"added {host} -> http://localhost:{port}")
PY
  sudo cloudflared tunnel --config "$CF_CONFIG" ingress validate
  sudo systemctl restart cloudflared
  echo "cloudflared restarted"
fi

# DNS record (idempotent)
if dig +short "$HOST_NAME" CNAME | grep -q cfargotunnel; then
  echo "DNS CNAME for $HOST_NAME already present"
else
  cloudflared tunnel route dns blacksmith "$HOST_NAME" 2>&1 | grep -v outdated || true
fi

# ---------------------------------------------------------------- user service
say "3/4 Workbench service"
if pkill -f "maestro-ace web" 2>/dev/null; then echo "stopped ad-hoc workbench process"; fi
mkdir -p "$(dirname "$UNIT_DST")"
cp "$UNIT_SRC" "$UNIT_DST"
systemctl --user daemon-reload
systemctl --user enable --now maestro-web.service
sleep 2
if systemctl --user is-active --quiet maestro-web.service; then
  echo "maestro-web.service is running (user lingering is on, so it survives logout and reboot)"
else
  echo "service failed to start; last log lines:"
  journalctl --user -u maestro-web.service -n 20 --no-pager
  exit 1
fi

# ---------------------------------------------------------------- summary
say "4/4 Open the workbench"
echo "Your token is the value in $ENV_FILE (show it with: cat $ENV_FILE)."
echo "Open once per device, replacing TOKEN with that value:"
echo "  local:   http://127.0.0.1:$PORT/?token=TOKEN"
echo "  public:  https://$HOST_NAME/?token=TOKEN"
echo
echo "The browser keeps a cookie for 90 days. Caption the clips, then press 'Run prepare'"
echo "when the readiness banner turns green."
