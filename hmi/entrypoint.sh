#!/bin/sh

HMI_TYPE=$1
NUM_PLC=$2
PLC_PORT=$3

# Default to the filling HMI if no HMI_TYPE is specified
if [ "$HMI_TYPE" = "packer" ]; then
  cp /usr/share/nginx/html/packer.html /usr/share/nginx/html/index.html
elif [ "$HMI_TYPE" = "stacker" ]; then
  cp /usr/share/nginx/html/stacker.html /usr/share/nginx/html/index.html
else
  cp /usr/share/nginx/html/filler.html /usr/share/nginx/html/index.html
fi

# Figure out the hostname prefix of the PLCs
# Our hostname will be of the format XXXhmi
# And the PLCs will be XXXplc01, XXXplc02, etc.

myhostname=$(hostname)
prefix=${myhostname%hmi}
plc_hostname_prefix=${prefix}plc

# Write a script that 'pings' all the PLCs on the PLC port.
# The script will be run by cron every 15 minutes
cat > /etc/periodic/15min/traffic.sh <<EOT
#!/bin/sh
rm /var/log/traffic.log
for i in \`seq 1 $NUM_PLC\`; do
    plc_hostname=\$(printf "%s%02d" $plc_hostname_prefix \$i)
    nc -vz -w 5 \${plc_hostname} $PLC_PORT >> /var/log/traffic.log 2>&1
done
EOT

chmod +x /etc/periodic/15min/traffic.sh

# Start crond
crond -l 2

# Start Nginx
nginx -g 'daemon off;'
