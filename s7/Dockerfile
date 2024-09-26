FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install python-snap7 --break-system-packages

COPY server.py /app/server.py

ENTRYPOINT ["python3", "/app/server.py"]