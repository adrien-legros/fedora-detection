FROM registry.redhat.io/ubi9/ubi:latest
USER root
RUN dnf install -y wget && wget https://github.com/mikefarah/yq/releases/download/v4.40.3/yq_linux_amd64 -O /usr/bin/yq \ 
    && chmod +x /usr/bin/yq
USER 1001