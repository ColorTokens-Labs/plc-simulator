# Dockerfile to build the EtherNet/IP simulator
# Available on dockerhub as colortokenslabs/enip-plc-simulator
#
# Use these prefixes when creating the container:
# 
#     Rockwell:  00:00:BC
#
# (C) 2024, ColorTokens Inc.
# Venky Raju

FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3
COPY server.py /server.py
ENTRYPOINT ["python3", "/server.py"]

