FROM nvcr.io/nvidia/pytorch:23.05-py3

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y git vim sudo gpustat libopenexr-dev python3-pybind11 libx11-6


COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir -p /workspace

COPY . /workspace

EXPOSE ${PORT}
EXPOSE 8080

WORKDIR /workspace

CMD python api.py