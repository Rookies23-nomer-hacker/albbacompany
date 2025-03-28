FROM python:3.7-slim-buster as python-base

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gnupg2 wget \
    && wget -qO - https://ftp-master.debian.org/keys/archive-key-10.asc | gpg --batch --yes --dearmor -o /usr/share/keyrings/debian-archive-keyring.gpg \
    && wget -qO - https://ftp-master.debian.org/keys/archive-key-10-security.asc | gpg --batch --yes --dearmor -o /usr/share/keyrings/debian-security-archive-keyring.gpg \
    && apt-get update \
    && pip install flask \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM ubuntu:18.04

WORKDIR /root

RUN set -e -x ;\
    sed -i 's,# deb-src,deb-src,' /etc/apt/sources.list ;\
    apt -y update ;\
    apt-get -y install build-essential ;\
    apt-get -y build-dep libseccomp ;\
    apt-get source libseccomp

COPY --from=python-base /app /app

COPY stage1.c /root/stage1.c
COPY stage2.c /root/stage2.c
COPY run.sh  /root/run.sh

RUN chmod 777 /root/run.sh

CMD ["python", "/app/app.py"]