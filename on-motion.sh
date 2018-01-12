#!/bin/bash

# called by pure-ftpd ####################

# with slash at the end
CHROOT=/media/photo/
SECRETS=/home/hass/.homeassistant/secrets.yaml

##########################################

# passed by ftpd
FILENAME="$1"
EXTENSION="${FILENAME##*.}"

set -x

if [ "$EXTENSION" != "jpg" ]; then
	echo "$EXTENSION skipped"
	exit 0
fi

# name of the first folder level inside CHROOT
INPUT=$(cut -d'/' -f1 <<<"${FILENAME/$CHROOT/}")

# lowercase
INPUT=${INPUT,,}

# create link to FILENAME named INPUT
[ -f $FILENAME ] && ln -sf $FILENAME ${CHROOT}${INPUT}.jpg

# notify hass
PASS=$(egrep "^http_password" ${SECRETS} | awk '{ print $2 }')
#curl -X POST -H "x-ha-access: $PASS" -H "Content-Type: application/json" -d '{"state": "on"}' \
#  http://localhost:8123/api/states/input_boolean.motion_${INPUT}

curl -X POST -H "x-ha-access: $PASS" -H "Content-Type: application/json" -d "{\"source\": \"$INPUT\"}" \
  http://localhost:8123/api/events/motion_detected_${INPUT}

exit 0
