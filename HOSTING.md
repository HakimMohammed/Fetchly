# Hosting Guide

This guide walks you through deploying Fetchly on a fresh Linux VM using Docker, Docker Compose, and Nginx. You’ll end with:

-   API (FastAPI + yt‑dlp + ffmpeg)
-   Web app (Next.js)
-   Nginx reverse proxy: `/` -> web, `/api/` -> API
-   Optional HTTPS via Let’s Encrypt

Tested on Ubuntu 22.04/24.04; adapt for other distros as needed.

---

## 1) Prepare the VM

-   Provision a VM (2 vCPU, 2–4 GB RAM recommended if handling large media). Ensure outbound internet and inbound ports 80/443 allowed.
-   Set your hostname and update packages.

```bash
sudo hostnamectl set-hostname fetchly
sudo apt-get update && sudo apt-get upgrade -y
```

Optional: set timezone.

```bash
sudo timedatectl set-timezone UTC
```

---

## 2) Install Docker + Compose

```bash
# Remove old versions (safe if none installed)
sudo apt-get remove -y docker docker-engine docker.io containerd runc || true

# Prereqs
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Docker GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install engine + compose plugin
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Allow your user to run docker without sudo (log out/in afterwards)
sudo usermod -aG docker $USER
```

Verify:

```bash
docker --version
docker compose version
```

---

## 3) Clone the repository

```bash
cd ~
git clone https://github.com/HakimMohammed/fetchly.git
cd fetchly
```

---

## 4) Configure environment

The web app needs to know where the API lives. Behind the bundled Nginx proxy, use a relative base URL so it works with your domain.

Set this before building the client:

```bash
# In the repo root
printf "NEXT_PUBLIC_API_BASE_URL=/api\nNEXT_PUBLIC_APP_NAME=Fetchly\nNEXT_PUBLIC_APP_VERSION=0.1.0\n" > client/.env
```

Note: Next.js embeds public env vars at build time. Ensure `client/.env` exists with `NEXT_PUBLIC_API_BASE_URL=/api` before you run `docker compose up --build`.

---

## 5) Start the stack (HTTP)

```bash
docker compose up --build -d
```

Services:

-   App: http://SERVER_IP/
-   API: http://SERVER_IP/api/

Check logs:

```bash
docker compose ps
docker compose logs -f nginx
```

Stop / restart:

```bash
docker compose down
# or
docker compose restart
```

---

## 6) Point your domain

Create an A record for your domain (e.g., `example.com`) pointing to the server IP.

If you only need HTTP (not recommended), you’re done: visit http://example.com.

---

## 7) Enable HTTPS (Let’s Encrypt)

There are multiple ways. Two common approaches:

### Option A: Use Certbot on the host

1. Install Certbot and Nginx plugin on the host:

```bash
sudo apt-get install -y certbot python3-certbot-nginx
```

2. Replace the containerized Nginx with host Nginx, or proxy from host Nginx to the Docker Nginx. The simplest is to terminate TLS at host Nginx and proxy to the `web` and `api` containers.

Create `/etc/nginx/sites-available/fetchly.conf`:

```nginx
server {
  listen 80;
  server_name example.com;

  location /api/ {
    proxy_pass http://127.0.0.1:8080/; # map to API published port
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 300;
  }

  location / {
    proxy_pass http://127.0.0.1:3000;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/fetchly.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

Open compose ports for host Nginx to reach:

-   Publish API on 8080 by changing `docker-compose.yml` api service port mapping to `8080:8000`.
-   Keep web on `3000:3000`.
-   Optionally remove the `nginx` service from compose when using host Nginx.

3. Request certificates:

```bash
sudo certbot --nginx -d example.com --redirect
```

This adds HTTPS and auto-renewal.

### Option B: Use containerized nginx-proxy + acme-companion

If you prefer everything in containers, add:

-   `jwilder/nginx-proxy` (or `nginxproxy/nginx-proxy`) and
-   `nginxproxy/acme-companion`

Then set `VIRTUAL_HOST=example.com` and `LETSENCRYPT_HOST=example.com` on the web service, `VIRTUAL_PATH=/` and on the api service `VIRTUAL_PATH=/api/`. This method is more advanced; open an issue if you want me to wire this into your compose.

---

## 8) Firewall (UFW)

If UFW is enabled, allow HTTP/HTTPS:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status
```

---

## 9) Updates & maintenance

-   Pull updates and rebuild:

```bash
cd ~/fetchly
git pull
# Ensure client/.env is correct (NEXT_PUBLIC_API_BASE_URL=/api)
docker compose up --build -d
```

-   View service logs:

```bash
docker compose logs -f api
# or web / nginx
```

-   Check API health:

```bash
curl -fsS http://localhost:8000/health
# behind proxy
curl -fsS http://localhost/api/health
```

-   Disk usage and cleanup:

```bash
docker system df
docker system prune -f
```

---

## 10) Advanced: persistence & tuning

-   Downloads are created inside the API container (`/app/downloads`) and are auto-cleaned by the service. If you want to persist or inspect them, map a volume:

```yaml
# docker-compose.yml (api service)
volumes:
    - ./server/downloads:/app/downloads
```

-   Increase Nginx timeouts for very large downloads or slow networks. The bundled `nginx/nginx.conf` sets a `proxy_read_timeout` of 300s for `/api/`.

-   Scale vertically (larger VM) or horizontally (replicas + an external load balancer). For replicas you’ll need shared storage or an object store for outputs if you keep files longer.

---

## 11) Troubleshooting

-   Web shows network errors:

    -   Confirm `NEXT_PUBLIC_API_BASE_URL` baked correctly. The HTML should contain `/api` in embedded scripts. If not, rebuild after setting `client/.env`.
    -   Check CORS is open on the API (it is by default in `server/main.py`).

-   502/404 from Nginx:

    -   Ensure containers are up: `docker compose ps`.
    -   Check `nginx` logs: `docker compose logs -f nginx`.

-   API errors referencing `yt-dlp` or `ffmpeg`:

    -   They are installed in the API image; if missing in logs, rebuild the image.

-   Certbot challenges fail:
    -   Ensure port 80 is open publicly and DNS points correctly.

---

## 12) Quick reference

-   Start: `docker compose up -d`
-   Build: `docker compose up --build -d`
-   Stop: `docker compose down`
-   Logs: `docker compose logs -f`
-   Restart one: `docker compose restart api` (or `web` / `nginx`)

---

If you prefer a different proxy (Caddy/Traefik) or want a ready-to-use TLS compose, say the word and I’ll wire it up.
