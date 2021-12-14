FROM quay.io/bedrock/ubuntu:focal-20210827
ENV container=docker

# increment the number in this file to force a full container rebuild
COPY files/update.txt /dev/null

RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        gnupg2 \
        locales \
        openssl \
        python3.8 \
        python3.8-distutils \
        python3.9 \
        python3.9-distutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# podman build fails with 'apt-key adv ...' but this works for both
RUN curl -sL "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xF23C5A6CF475977595C89F51BA6932366A755776" | apt-key add

COPY files/deadsnakes.list /etc/apt/sources.list.d/deadsnakes.list

RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3.10 \
        python3.10-distutils \
    && apt-get clean

RUN ln -s python3.10 /usr/bin/python \
    && ln -sf python3.10 /usr/bin/python3 \
    && locale-gen en_US.UTF-8

# Install pip
COPY files/*.py /usr/share/container-setup/
RUN python3.10 /usr/share/container-setup/setup.py \
    && rm -rf /usr/share/container-setup

# Install codecov uploader
RUN curl --silent --show-error --output /usr/local/bin/codecov https://ansible-ci-files.s3.us-east-1.amazonaws.com/codecov/linux/codecov \
    && chmod +x /usr/local/bin/codecov

# Install tox
COPY requirements/requirements.txt /usr/share/container-setup/
RUN python3.10 -m pip install -r /usr/share/container-setup/requirements.txt \
    && rm -rf /usr/share/container-setup

VOLUME /sys/fs/cgroup /run/lock /run /tmp
CMD ["tail"]
