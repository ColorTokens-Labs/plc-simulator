FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install pymodbus --break-system-packages

COPY server.py /app/server.py
RUN mkdir -p /app/config
COPY config/* /app/config

ENTRYPOINT ["python3", "/app/server.py"]
CMD ["rockwell-ml"]
