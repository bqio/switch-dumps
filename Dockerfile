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

CMD bash -c "\
    MAGNET_LINK=\$(cat magnet.txt) && \
    echo '=== Start torrent download ===' && \
    aria2c --bt-metadata-only=false \
           --bt-save-metadata=false \
           --summary-interval=10 \
           --seed-time=0 \
           \"\$MAGNET_LINK\" && \
    echo '=== Download complete. Start dumper ===' && \
    xz -d -c *.xml.xz | python dump.py --screenshots - 1605 /output/result.json \
"