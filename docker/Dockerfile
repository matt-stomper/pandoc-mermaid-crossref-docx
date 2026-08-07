FROM ghcr.io/puppeteer/puppeteer:25.3.0

USER root
ENV PIP_BREAK_SYSTEM_PACKAGES=1 \
    DEBIAN_FRONTEND=noninteractive \
    PUPPETEER_CACHE_DIR=/home/node/.cache/puppeteer

RUN wget -qO- https://pascalroeleven.nl/deb-pascalroeleven.gpg | tee /etc/apt/keyrings/deb-pascalroeleven.gpg

COPY pascalroeleven.sources /etc/apt/sources.list.d/pascalroeleven.sources

RUN apt update && apt install -y \
    software-properties-common \
    npm \
    librsvg2-bin \
    curl \
    xz-utils \
    python3.13  \
    python3.13-venv \
    python3-pip

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.13 1

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN mkdir /venv
ENV UV_PROJECT_ENVIRONMENT=/venv
ENV PATH=${UV_PROJECT_ENVIRONMENT}/bin:/root/.local/bin/:/usr/local/bin/:/$PATH

RUN uv venv /venv

WORKDIR /tmp

RUN curl -L -o /tmp/pandoc.deb https://github.com/jgm/pandoc/releases/download/3.10.1/pandoc-3.10.1-1-amd64.deb
RUN apt-get install -y /tmp/pandoc.deb
RUN rm /tmp/pandoc.deb

RUN curl -L -o pandoc-crossref.tar.xz https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.24a/pandoc-crossref-Linux-X64.tar.xz
RUN tar -xf pandoc-crossref.tar.xz
RUN apt-get remove -y curl
RUN mv pandoc-crossref /usr/local/bin/
RUN chmod +x /usr/local/bin/pandoc-crossref
RUN rm pandoc-crossref.tar.xz

RUN npm install -g @mermaid-js/mermaid-cli@11.16.0
RUN npm install -g glob

RUN mkdir -p /app/filters/

COPY ../filters/pandoc_acro-0.11.0-py3-none-any.whl /app/pandoc_acro-0.11.0-py3-none-any.whl
COPY ../filters/more_pandoc_filters-0.2.0-py3-none-any.whl /app/more_pandoc_filters-0.2.0-py3-none-any.whl
COPY ../filters/docx_tools-1.0.3-py3-none-any.whl /app/docx_tools-1.0.3-py3-none-any.whl
COPY ../filters/diagram/diagram.lua /app/filters/diagram.lua
COPY ../filters/diagram/_extensions /app/filters/_extensions
COPY ../.puppeteer.json /app/filters/

RUN uv pip install pandoc-include
RUN uv pip install /app/docx_tools-1.0.3-py3-none-any.whl && rm /app/docx_tools-1.0.3-py3-none-any.whl
RUN uv pip install /app/pandoc_acro-0.11.0-py3-none-any.whl && rm /app/pandoc_acro-0.11.0-py3-none-any.whl
RUN uv pip install /app/more_pandoc_filters-0.2.0-py3-none-any.whl && rm /app/more_pandoc_filters-0.2.0-py3-none-any.whl

RUN chmod 1777 /tmp

USER node

