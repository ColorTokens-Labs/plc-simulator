# Dockerfile to build the S7 PLC simulator
# Available on dockerhub as colortokenslabs/s7-plc-simulator
#
# Use these prefixes when creating the container:
# 
#    Siemens AG:  00:1B:1B
#
# (C) 2024, ColorTokens Inc.
# Venky Raju

FROM python:3.9.20-slim-bullseye

RUN pip3 install python-snap7

COPY server.py /app/server.py

ENTRYPOINT ["python3", "/app/server.py"]