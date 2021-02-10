FROM odoo:14.0@sha256:ddebf5d6687839331b56d9c64cf2831429c65cd41b373df452d6824f0ebacccb
USER root
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp
RUN python3 -m pip install -r /tmp/requirements.txt
USER odoo
