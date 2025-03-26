FROM nginx:1.16
WORKDIR /usr/share/nginx/html
COPY files /usr/share/nginx/html

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gnupg2 wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*