# Dockerfile to build the HMI simulator
# Available on dockerhub as colortokenslabs/hmi-simulator
#
# When you start the container specify the following arguments:
#   HMI type - filler|packer|stacker
#   number of PLCs
#   port number on PLC (502 for modbus, 102 for S7)
#
# (C) 2024, ColorTokens Inc.
# Venky Raju

FROM alpine:latest

RUN apk add --no-cache nginx

COPY default.conf /etc/nginx/http.d/default.conf

# Copy HTML files for all three variants
RUN mkdir -p /usr/share/nginx/html
COPY html/packer.html /usr/share/nginx/html/packer.html
COPY html/stacker.html /usr/share/nginx/html/stacker.html
COPY html/filler.html /usr/share/nginx/html/filler.html

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script.
ENTRYPOINT ["/entrypoint.sh"]
CMD ["filler", "5", "502"]