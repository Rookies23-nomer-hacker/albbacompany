FROM python:3.7-slim-buster

WORKDIR /app

COPY app.py /app/                                                                                                    eyrings/debian-archive-keyring.gpg \
COPY requirements.txt /app/                                                                                          r/share/keyrings/debian-security-archive-keyring.gpg \

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies, including Docker
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gnupg2 wget docker.io \
    && wget -qO - https://ftp-master.debian.org/keys/archive-key-10.asc | gpg --batch --yes --dearmor -o /usr/share/keyrings/debian-archive-keyring.gpg \
    && wget -qO - https://ftp-master.debian.org/keys/archive-key-10-security.asc | gpg --batch --yes --dearmor -o /usr/share/keyrings/debian-security-archive-keyring.gpg \
    && apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Flask explicitly
RUN pip install flask

COPY stage1.c /root/stage1.c
COPY stage2.c /root/stage2.c
COPY run.sh /root/run.sh

RUN chmod 777 /root/run.sh

CMD ["python", "/app/app.py"]
