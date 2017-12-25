#!/bin/bash

# called by pure-ftpd

# with slash at the end
CHROOT=/media/photo/

# passed by ftpd
FILENAME="$1"

# name of the first folder level inside CHROOT
INPUT=$(cut -d'/' -f1 <<<"${FILENAME/$CHROOT/}")

# lowercase
INPUT=${INPUT,,}

# create link to FILENAME named INPUT
[ -f $FILENAME ] && ln -sf $FILENAME ${CHROOT}${INPUT}.jpg

# notify hass
PASS=$(grep http_password ~/secrets.yaml | awk '{ print $2 }')
curl -X POST -H "x-ha-access: $PASS" -H "Content-Type: application/json" -d '{"state": "on"}' \
  http://localhost:8123/api/states/input_boolean.motion_${INPUT}

exit 0
