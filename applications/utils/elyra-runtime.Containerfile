FROM registry.access.redhat.com/ubi9/python-311:latest

RUN pip install kfp-tekton==1.5.6 elyra