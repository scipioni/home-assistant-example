#!/bin/sh

# called by incron
# /media/usb0/photo/C1_00626E611E80/snap/ IN_CLOSE_WRITE /home/hass/on-motion.sh $@$#

IMAGE=$1
[ -f $IMAGE ] && ln -sf $IMAGE /media/usb0/latest.jpg

PASS=$(grep http_password ~/secrets.yaml | awk '{ print $2 }')

curl -X POST -H "x-ha-access: $PASS" -H "Content-Type: application/json" -d '{"state": "on"}' \
  http://localhost:8123/api/states/input_boolean.motion_detected
