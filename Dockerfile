FROM pandoc/latex:latest

RUN apk add bash
RUN apk add wget perl fontconfig-dev freetype-dev tar

ENV CHROME_BIN="/usr/bin/chromium-browser" \
    PUPPETEER_SKIP_CHROMIUM_DOWNLOAD="true"

ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache python3 py3-pip

RUN mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old

RUN apk add --update udev ttf-freefont chromium npm \
    && npm install -g mermaid-filter@1.4.7 --unsafe-perm=true

RUN mkdir -p /app

COPY filters/page_break_heading_1.lua /app/page_break_heading_1.lua
COPY inject-properties.py /app/inject-properties.py

COPY requirements.txt /app/requirements.txt

ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN pip install -r /app/requirements.txt

