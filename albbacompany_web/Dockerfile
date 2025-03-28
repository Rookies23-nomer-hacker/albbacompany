FROM python:3.7-slim-buster

RUN set -e -x ;\
    echo "deb http://deb.debian.org/debian buster main contrib non-free" >> /etc/apt/sources.list ;\
    echo "deb-src http://deb.debian.org/debian buster main contrib non-free" >> /etc/apt/sources.list ;\
    apt update ;\    apt install -y docker.io build-essential ;\
    apt-get -y build-dep libseccomp ;\
    apt-get source libseccomp

ADD stage1.c /app/stage1.c
ADD stage2.c /app/stage2.c
ADD run.sh  /app/run.sh

RUN set -e -x ;\
    chmod 777 /app/run.sh ;\
    ls -l /app

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

CMD ["python", "app.py"]
