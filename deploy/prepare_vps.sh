#!/usr/bin/env bash
set -euo pipefail
release_id=$1
archive=/tmp/ali33-release.tar.gz
env_source=/tmp/ali33-demo.env
app_root=/opt/ali33-research
app_release="$app_root/releases/$release_id"

if ! id ali33-demo >/dev/null 2>&1; then
    sudo useradd --system --home-dir "$app_root" --shell /usr/sbin/nologin ali33-demo
fi
sudo install -d -o ali33-demo -g ali33-demo -m 755 "$app_root" "$app_root/releases" "$app_release"
sudo install -d -o ali33-demo -g ali33-demo -m 700 "$app_root/shared" "$app_root/shared/transcripts" "$app_root/shared/arxiv_papers"
sudo tar -xzf "$archive" --no-same-owner -C "$app_release"
sudo chown -R ali33-demo:ali33-demo "$app_release"
sudo install -o ali33-demo -g ali33-demo -m 600 "$env_source" "$app_root/shared/.env"
sudo ln -sfn "$app_root/shared/.env" "$app_release/starter_v0/.env"
sudo ln -sfn "$app_root/shared/transcripts" "$app_release/starter_v0/transcripts"
sudo ln -sfn "$app_root/shared/arxiv_papers" "$app_release/starter_v0/arxiv_papers"
if [ ! -x "$app_root/.venv/bin/pip" ]; then
    sudo -u ali33-demo python3 -m venv "$app_root/.venv"
fi
sudo -u ali33-demo "$app_root/.venv/bin/pip" install --disable-pip-version-check -r "$app_release/starter_v0/requirements.lock.txt"
cd "$app_release/starter_v0"
sudo -u ali33-demo "$app_root/.venv/bin/python" -m pytest -q
sudo ln -sfn "$app_release" "$app_root/current"
sudo install -m 644 "$app_release/deploy/ali33-research.service" /etc/systemd/system/ali33-research.service
sudo systemctl daemon-reload
sudo systemctl enable --now ali33-research.service
sudo systemctl restart ali33-research.service
for attempt in $(seq 1 20); do
    if curl -fsS --max-time 3 http://127.0.0.1:8503/_stcore/health; then break; fi
    sleep 1
done
curl -fsS --max-time 5 http://127.0.0.1:8503/_stcore/health
sudo install -d -m 755 /var/www/ali33-acme
sudo install -m 644 "$app_release/deploy/ali33-http.conf" /etc/nginx/sites-available/ali33-research
sudo ln -sfn /etc/nginx/sites-available/ali33-research /etc/nginx/sites-enabled/ali33-research
if ! sudo nginx -t; then
    sudo unlink /etc/nginx/sites-enabled/ali33-research
    exit 1
fi
sudo systemctl reload nginx
rm -f -- "$env_source" "$archive"
printf '\nALI33 private backend ready; HTTP challenge site installed.\n'
