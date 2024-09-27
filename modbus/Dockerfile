# Dockerfile to build the modbus simulator
# Available on dockerhub as colortokenslabs/modbus-plc-simulator
#
# Use these prefixes when creating the container:
# 
#     Rockwell:  00:00:BC
#     Schneider: 00:00:54
#
# (C) 2024, ColorTokens Inc.
# Venky Raju

FROM python:3.9.20-slim-bullseye

RUN pip3 install --no-cache-dir pymodbus \
    && mkdir -p /app/config

COPY server.py /app/server.py
COPY config/* /app/config

# Default is a Rockwell Micrologix PLC.
ENTRYPOINT ["python3", "/app/server.py"]
CMD ["rockwell-ml"]
