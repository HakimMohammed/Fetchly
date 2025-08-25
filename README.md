# Fetchly

Fast, modern media downloader.

-   Backend: FastAPI + yt-dlp + ffmpeg
-   Frontend: Next.js + React + Tailwind

## What it does

Paste a URL, pick “video” or “audio”, optionally set start/end times, and Fetchly downloads it. The server auto-chooses sensible formats/quality (e.g., video up to 1080p; audio mp3/m4a/etc based on ffmpeg support).

## Prerequisites

-   Python 3.11+ (server)
-   ffmpeg installed and on PATH
-   Node.js 18+ and pnpm (client)

## Setup

1. Server

```bash
cd server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Client

```bash
cd client
pnpm install
cp .env.example .env.local   # then set NEXT_PUBLIC_API_BASE_URL (e.g., http://localhost:8000)
pnpm dev
```

Open http://localhost:3000 and paste a URL.

## Docker

Build and run with Docker Compose (includes API, Next.js, and Nginx proxy):

```bash
docker compose up --build -d
```

-   App: http://localhost
-   API: http://localhost/api (proxy to FastAPI)

For local development without Nginx, run services individually:

```bash
# API
docker build -t fetchly-api ./server
docker run --rm -p 8000:8000 fetchly-api

# Web (ensure NEXT_PUBLIC_API_BASE_URL is set accordingly)
docker build -t fetchly-web ./client
docker run --rm -e NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 -p 3000:3000 fetchly-web
```

## Deploying to a server

1. Provision a Linux VM (Ubuntu/Debian recommended) with Docker and Docker Compose.
2. Clone the repo to the server: `git clone https://github.com/HakimMohammed/fetchly.git && cd fetchly`.
3. Update client env (`client/.env` or pass at runtime) so the web app calls the API via Nginx:
    - `NEXT_PUBLIC_API_BASE_URL=/api`
4. Start the stack:
    ```bash
    docker compose up --build -d
    ```
5. Add your domain and TLS:
    - Point DNS A record to the server IP.
    - Replace `nginx/nginx.conf` with a server block for your domain and set up TLS (e.g., use nginx-proxy + acme-companion, or Certbot in a sidecar).

Minimal example for domain (replace `example.com`):

```nginx
server {
  listen 80;
  server_name example.com;
  location /api/ { proxy_pass http://api:8000/; }
  location /      { proxy_pass http://web:3000; }
}
```

Then handle HTTPS via reverse proxy stack or Certbot.

See HOSTING.md for a detailed, step‑by‑step hosting guide.

## API quick reference

-   GET /health – server health
-   GET /capabilities – ffmpeg-supported containers and encoders
-   GET /info?url=... – returns media info (title, duration, thumbnail)
-   POST /download – body: { url, media_type: "video"|"audio", start_time?, end_time? }
    -   Response: { filename, download_url }
-   GET /download-file/{filename} – fetch the binary file

Notes

-   extension and quality are optional; the server picks defaults if omitted
-   time format is HH:MM:SS; omit to download full media

## Development

-   Server tests: run `pytest` (coming soon) or `python test_download.py`
-   Type-check client: `pnpm -C client type-check`

## License

MIT
