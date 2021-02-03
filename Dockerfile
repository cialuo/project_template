FROM odoo:14.0
USER root
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp
RUN python3 -m pip install -r /tmp/requirements.txt
USER odoo
