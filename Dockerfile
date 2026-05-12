FROM ghcr.io/puppeteer/puppeteer:24.37.5

USER root
ENV PIP_BREAK_SYSTEM_PACKAGES=1 \
    DEBIAN_FRONTEND=noninteractive \
    PUPPETEER_CACHE_DIR=/home/node/.cache/puppeteer

RUN wget -qO- https://pascalroeleven.nl/deb-pascalroeleven.gpg | tee /etc/apt/keyrings/deb-pascalroeleven.gpg

COPY docker/pascalroeleven.sources /etc/apt/sources.list.d/pascalroeleven.sources

RUN apt update

RUN apt install -y \
    software-properties-common \
    npm \
    librsvg2-bin \
    curl \
    xz-utils \
    python3.13  \
    python3.13-venv  \
    python3.13-dev

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.13 1

WORKDIR /tmp

RUN curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py --verbose

RUN curl -L -o /tmp/pandoc.deb https://github.com/jgm/pandoc/releases/download/3.9.0.2/pandoc-3.9.0.2-1-amd64.deb
RUN apt-get install -y /tmp/pandoc.deb
RUN rm /tmp/pandoc.deb

RUN curl -L -o pandoc-crossref.tar.xz https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.23a/pandoc-crossref-Linux-X64.tar.xz
RUN tar -xf pandoc-crossref.tar.xz
RUN mv pandoc-crossref /usr/local/bin/
RUN chmod +x /usr/local/bin/pandoc-crossref
RUN rm pandoc-crossref.tar.xz

RUN npm install -g @mermaid-js/mermaid-cli
RUN npm install -g mermaid-filter --unsafe-perm=true

RUN mkdir -p /app

COPY filters/pandoc_acro-0.11.0-py3-none-any.whl /app/pandoc_acro-0.11.0-py3-none-any.whl
COPY filters/more_pandoc_filters-0.1.0-py3-none-any.whl /app/more_pandoc_filters-0.1.0-py3-none-any.whl
COPY dist/docx_tools-1.0.2-py3-none-any.whl /app/docx_tools-1.0.2-py3-none-any.whl

RUN pip install /app/docx_tools-1.0.2-py3-none-any.whl
RUN pip install /app/pandoc_acro-0.11.0-py3-none-any.whl
RUN pip install /app/more_pandoc_filters-0.1.0-py3-none-any.whl

RUN chmod 1777 /tmp
ENV PATH=$PATH:/usr/local/bin/

USER node
COPY .puppeteer.json /home/node/.puppeteer.json