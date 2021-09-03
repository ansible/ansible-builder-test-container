FROM quay.io/bedrock/ubuntu:focal-20210827
ENV container=docker

RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        git \
        python3-pip \
        python3.8 \
        python3.9 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl --silent --show-error --output /usr/local/bin/codecov https://ansible-ci-files.s3.us-east-1.amazonaws.com/codecov/linux/codecov \
    && chmod +x /usr/local/bin/codecov

COPY requirements/*.txt /tmp/
RUN python3.9 -m pip install tox -c /tmp/constraints.txt \
    && rm -f /tmp/*.txt

VOLUME /sys/fs/cgroup /run/lock /run /tmp
CMD ["tail"]
