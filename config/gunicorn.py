# Konfiguracja produkcyjna serwera (wzorzec: docs/ARCHITEKTURA.md 7.6).
# Start: gunicorn main:app -c config/gunicorn.py

bind = "0.0.0.0:3000"
workers = 3
worker_class = "uvicorn.workers.UvicornWorker"

timeout = 240
keepalive = 65

# recykling workerów chroni przed wyciekami pamięci; jitter rozsuwa restarty
max_requests = 1000
max_requests_jitter = 50

# tmpfs zamiast dysku dla heartbeat workerów
worker_tmp_dir = "/dev/shm"

# logi na stdout/stderr (zbiera je Docker)
accesslog = "-"
errorlog = "-"
loglevel = "info"

# za reverse proxy (Traefik)
forwarded_allow_ips = "*"
