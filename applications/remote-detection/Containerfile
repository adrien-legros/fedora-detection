FROM registry.fedoraproject.org/fedora-minimal:38

ARG TARGETARCH

USER 0

# Update base image for latest security updates
# (ubi images are not released that often)

RUN microdnf install -y --setopt=install_weak_deps=0 \
    python3 python3-opencv python3-pip python3-devel gcc

RUN pip3 install -U "micropipenv[toml]"

WORKDIR /opt/app-root/src

# Copy files
COPY requirements.txt app.py ./
ADD templates/ ./templates/
ADD yolov5 yolov5

RUN pip install -r requirements.txt && pip install -r yolov5/requirements.txt

ADD model model

CMD python3 -m flask run --host 0.0.0.0
