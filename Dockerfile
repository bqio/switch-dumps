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

ENV MAGNET_LINK='magnet:?xt=urn:btih:141201CD86C814A6968F4BA9A1F3F6B83C15D067&tr=http%3A%2F%2Fbt4.t-ru.org%2Fann%3Fmagnet&dn=%D0%9D%D0%B5%D0%BE%D1%84%D0%B8%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D0%B1%D0%B0%D0%B7%D0%B0%20%D1%80%D0%B0%D0%B7%D0%B4%D0%B0%D1%87%20RuTracker.ORG%20v.%2020260627'

CMD bash -c "\
    echo '=== Start torrent download ===' && \
    aria2c --bt-metadata-only=false \
           --bt-save-metadata=false \
           --summary-interval=10 \
           --seed-time=0 \
           \"$MAGNET_LINK\" && \
    echo '=== Download complete. Start dumper ===' && \
    xz -d -c *.xml.xz | python dump.py - 1605 /output/result.json \
"
