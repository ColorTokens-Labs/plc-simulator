#!/bin/sh

# Default to the filling HMI if no HMI_TYPE is specified
if [ "$HMI_TYPE" = "packer" ]; then
  cp /usr/share/nginx/html/packer.html /usr/share/nginx/html/index.html
elif [ "$HMI_TYPE" = "stacker" ]; then
  cp /usr/share/nginx/html/stacker.html /usr/share/nginx/html/index.html
else
  cp /usr/share/nginx/html/filler.html /usr/share/nginx/html/index.html
fi

# Start Nginx
nginx -g 'daemon off;'