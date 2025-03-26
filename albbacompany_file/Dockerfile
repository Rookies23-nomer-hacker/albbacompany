FROM nginx:latest
WORKDIR /usr/share/nginx/html
COPY files /usr/share/nginx/html

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gnupg2 wget \
    && wget -qO - https://ftp-master.debian.org/keys/archive-key-10.asc | gpg --batch --yes --dearmor -o /usr/share/keyrings/debian-archive-keyring.gpg \
    && wget -qO - https://ftp-master.debian.org/keys/archive-key-10-security.asc | gpg --batch --yes --dearmor -o /usr/share/keyrings/debian-security-archive-keyring.gpg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*