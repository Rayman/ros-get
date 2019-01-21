FROM ros:kinetic-ros-core

RUN apt-get update && apt-get install -y \
    python-pip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /root/src
WORKDIR /root/src

# install ros-get
RUN git clone https://github.com/Rayman/ros-get.git
RUN pip install --user -e ros-get/
ENV PATH /root/.local/bin:$PATH

# put your rosdistro somewhere, i.e. also in src/
RUN git clone https://github.com/Rayman/rosdistro.git

# make a directory for the workspace
RUN mkdir -p /root/ros/test1
WORKDIR /root/ros/test1

# create a ros-get workspace
RUN ros-get ws-create file:///root/src/rosdistro/index.yaml /opt/ros/kinetic
RUN ln -sv /root/src/ros-get/setup.sh setup.sh

# source this workspace in a login shell
RUN echo "source $PWD/setup.sh" >> ~/.bashrc

# don't put any additional commands in this Dockerfile, it's only for interactive usages
