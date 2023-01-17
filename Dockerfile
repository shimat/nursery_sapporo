FROM openjdk:21-slim-bullseye
COPY --from=python:3.11-bullseye / /

COPY requirements.txt /tmp/
RUN pip install -U pip \
  && pip install --no-cache-dir -r /tmp/requirements.txt

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
  && apt install -y --no-install-recommends \
    wget \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

#RUN wget https://kosodate.city.sapporo.jp/material/files/group/1/R5ukeireyotesu1124_sasikae_1125_syuryo.pdf
