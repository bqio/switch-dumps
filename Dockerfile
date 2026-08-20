FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    aria2 \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /output

COPY . .

ENV MAGNET_LINK='magnet:?xt=urn:btih:6B5CC220E4D438709FAB834DFDAF64014E35E8B2&tr=http%3A%2F%2Fbt4.t-ru.org%2Fann%3Fmagnet'

CMD bash -c "\
    echo '=== Start torrent download ===' && \
    aria2c --bt-metadata-only=false \
           --bt-save-metadata=false \
           --summary-interval=10 \
           --seed-time=0 \
           \"$MAGNET_LINK\" && \
    echo '=== Download complete. Start dumper ===' && \
    xz -d -c *.xml.xz | python dump.py --screenshots - 1605 /output/result.json \
"
