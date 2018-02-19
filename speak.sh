#!/bin/bash

MESSAGE="$*"

SECRETS=/home/hass/.homeassistant/secrets.yaml
set -x

# this is device name given to google home device in android app settings
PLAYER_ID="main_google"

# notify hass
PASS=$(egrep "^http_password" ${SECRETS} | awk '{ print $2 }')

curl -X POST -H "x-ha-access: $PASS" -H "Content-Type: application/json" \
	-d "{\"entity_id\": \"media_player.${PLAYER_ID}\", \"message\": \"${MESSAGE}\"}" \
  	http://localhost:8123/api/services/tts/google_say

exit 0
