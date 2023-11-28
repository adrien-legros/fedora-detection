FROM registry.fedoraproject.org/fedora-minimal:38

ARG TARGETARCH

USER 0

# Update base image for latest security updates
# (ubi images are not released that often)

RUN microdnf install -y --setopt=install_weak_deps=0 \
    python3 python3-opencv python3-pip

RUN pip3 install -U "micropipenv[toml]"

WORKDIR /opt/app-root/src

# Copy files
COPY pipfiles/$TARGETARCH/Pipfile.lock app.py ./
ADD templates/ ./templates/

# Install packages and cleanup
# (all commands are chained to minimize layer size)
RUN echo "Installing softwares and packages" && \
    # Install Python packages \
    micropipenv install && \
    rm -f ./Pipfile.lock

CMD python3 -m flask run --host 0.0.0.0