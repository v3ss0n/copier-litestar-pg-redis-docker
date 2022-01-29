import os

import platform

if platform.system() == 'Linux':
    # Only runnable on linux
    cores = len(os.sched_getaffinity(0))
else:
    cores = os.cpu_count()

MULTIPLIER = 2  # gunicorn recommends 2-4x cores
MAX_WORKERS = os.getenv('MAX_WORKERS')
MIN_WORKERS = os.getenv('MIN_WORKERS', 2)
assert MIN_WORKERS > 0

# Set workers dynamically
if web_concurrency := os.getenv('GUNICORN_WORKER_COUNT'):
    web_concurrency = max(int(web_concurrency), MIN_WORKERS)
else:
    # If there's no value set, let's infer (multiplier * cores)
    # Gunicorn docs recommend ~2-4 * cores, while the Heroku docs seem to suggest 1-1.5x.
    web_concurrency = max(int(MULTIPLIER * cores), MIN_WORKERS)

if MAX_WORKERS:
    web_concurrency = min(web_concurrency, int(MAX_WORKERS))

# Gunicorn config variables
workers = web_concurrency
threads = os.getenv('GUNICORN_THREAD_COUNT', 2)
bind = os.getenv('BIND', None) or f'{os.getenv("HOST", "0.0.0.0")}:{os.getenv("PORT", "80")}'
loglevel = os.getenv('LOG_LEVEL', 'info')
errorlog = os.getenv('ERROR_LOG', '-')  # '-' makes gunicorn log to stderr
accesslog = os.getenv('ACCESS_LOG', None)
worker_tmp_dir = '/dev/shm'
preload_app = True
keepalive = 5
max_requests = 1000
max_request_jitter = 100
graceful_timeout = 25
timeout = 30
