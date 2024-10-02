# Dockerfile to build the HMI simulator
# Available on dockerhub as colortokenslabs/hmi-simulator
#
# Specify the HMI type for the web interface using 
# -e HMI_TYPE = filler|stacker|packer
# Default is filler (if HMI_TYPE is unspecified)
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

# Run the entrypoint script
CMD ["/entrypoint.sh"]