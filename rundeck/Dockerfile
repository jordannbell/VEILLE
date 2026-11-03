ARG RUNDECK_VERSION
FROM rundeck/rundeck:${RUNDECK_VERSION}

USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv postgresql-client \
 && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/veille-venv \
 && /opt/veille-venv/bin/pip install --no-cache-dir httpx feedparser "psycopg[binary]"
USER rundeck
