FROM registry.access.redhat.com/ubi9/python-39

USER 0

WORKDIR /opt/app-root/src

COPY requirements.txt requirements.txt
COPY app.py app.py
COPY templates templates

RUN dnf update -y && \
dnf config-manager --enable codeready-builder-for-rhel-9-$(arch)-rpms  && \
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm -y && \
dnf install opencv opencv-devel -y && \
pip install --no-cache-dir -r requirements.txt && \
pip install torch torchvision  --index-url https://download.pytorch.org/whl/cpu


USER 1001

CMD ["python /opt/app-root/src/app.py"]