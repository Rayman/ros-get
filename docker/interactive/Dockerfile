FROM ros:kinetic-ros-core

RUN apt-get update && apt-get install -y \
    python-pip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /root/src
WORKDIR /root/src

# install ros-get
COPY . .
RUN ls -hl
RUN pip install -e .
