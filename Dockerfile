FROM ghcr.io/puppeteer/puppeteer:24.15.0

USER root
ENV PIP_BREAK_SYSTEM_PACKAGES=1 \
    DEBIAN_FRONTEND=noninteractive \
    PUPPETEER_CACHE_DIR=/home/node/.cache/puppeteer

RUN apt install -y \
    npm \
    librsvg2-bin \
    curl \
    xz-utils \
    python3  \
    python3-pip

RUN curl -L -o /tmp/pandoc.deb https://github.com/jgm/pandoc/releases/download/3.8.2.1/pandoc-3.8.2.1-1-amd64.deb
RUN apt-get install -y /tmp/pandoc.deb
RUN rm /tmp/pandoc.deb

RUN curl -L -o pandoc-crossref.tar.xz https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.22a/pandoc-crossref-Linux-X64.tar.xz
RUN tar -xf pandoc-crossref.tar.xz
RUN mv pandoc-crossref /usr/local/bin/
RUN chmod +x /usr/local/bin/pandoc-crossref
RUN rm pandoc-crossref.tar.xz

RUN npm install -g @mermaid-js/mermaid-cli
RUN npm install -g mermaid-filter --unsafe-perm=true

RUN mkdir -p /app

COPY filters/page_break_heading_1.lua /app/page_break_heading_1.lua
COPY inject-properties.py /app/inject-properties.py
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN chmod 1777 /tmp
ENV PATH=$PATH:/usr/local/bin/

USER node
COPY .puppeteer.json /home/node/.puppeteer.json