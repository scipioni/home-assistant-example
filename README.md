# home-assistant-example
home-assistant real configuration

## zwave

* Controller - Aeotec ZW090 Z-Stick Gen5 EU (node1)
  - reset: press and hold pinhole with paperclip for 20 seconds (blu led for 2 seconds as success)
* Multisensor - Aeotec Multisensor 6 (node2) multi_soggiorno
  - reset: press and hold button for 20 seconds
  - secure inclusion: press button 2 times within 1 second
* Extender - Aeotec Range Extender (node3) repeater_garage
  - reset: press and hold button for 20 seconds
  - secure inclusion: press button 2 times within 1 second
* Power - Zipato Micromodule Energy Meter PH-PAB01.eu Philio Technology Corporation (node4) power_contatore
  - reset: press button 3 times within 2 seconds and within 1 second hold button for 5 seconds
  - secure_inclusion: press button 3 times within 2 seconds 
    - 8.1 W consumo casa
    - 8.3 W fotovoltaico
* Power - Greenwave PowerNode NS310-F 
  - reset: press power button for few seconds at booting time
  - secure_inclusion: press sync button for 2 seconds
    - node5 lavastoviglie
    - node6 frigorifero
    - node8 asciugatrice e lavatrice
* Multisensor - Fibaro FGSM-001
  - reset: press and hold for 5 seconds until yellow, then release and press until red color
  - secure_inclusion: quickle triple press button and after blu led press button
  - waking up: quickle triple press button
  - manual: http://manuals.fibaro.com/content/manuals/en/FGMS-001/FGMS-001-EN-T-v2.1.pdf
    - node9
    - node10

## camera

1080P POE Bullet IP CAMERA (SV-B01POE-1080P) http://www.sv3c.com/1080P-POE-Bullet-IP-CAMERA-SV-B01POE-1080P-.html


## camera motion trigger

```
![Alt text](http://g.gravizo.com/g?
  digraph G {
    aize ="5,5";
    camera -> ftp [label="on motion"]
    ftp -> uploadscript -> onmotion
    ftp [label="ftp server"]
    onmotion [label="on-motion.sh"]
    onmotion -> hass [label="REST API"]
    onmotion -> image [style="box"]
    image [shape=box,style=filled,color=".7 .3 1.0"]
    hass -> telegram
    image -> telegram -> user
    user [shape=box,style=filled,color=".4 .5 1.0"]
  }
)
```

/etc/default/pure-ftpd-common 
```
UPLOADSCRIPT=/home/hass/on-motion.sh
```

/etc/pure-ftpd/conf/Umask
```
113 002
```

/etc/pure-ftpd/conf/CallUploadScript
```
yes
```



## camera FTP clean

/etc/cron.daily/photo-clean
```
#!/bin/sh

ARCHIVE=/media/photo
DAYS=2

find ${ARCHIVE} -mtime +${DAYS} -exec rm {} \;

```

## camera FTP stop/start 

create file /etc/sudoers.d/hass
```
hass  ALL=(ALL:ALL) NOPASSWD: /bin/systemctl * pure-ftpd.service
```

define ftp_stop and ftp_start in shell_command.yaml

define automation/ftp-stop.yaml and automation/ftp-start.yaml


## telegram webhooks

```yaml
# Example configuration.yaml entry
telegram_bot:
  platform: webhooks
  api_key: !secret telegram_token
  trusted_networks:
    - 149.154.167.197/32
    - 149.154.167.198/31
    - 149.154.167.200/29
    - 149.154.167.208/28
    - 149.154.167.224/29
    - 149.154.167.232/31
  allowed_chat_ids:
    - 73496590
    - 84015820
```

Configuration variables:

- **api_key** (*Optional*): The API token of yout bot. Setting the optional
 parameter `api_key` (with api_url) make an automatic registration of webhook
in telgram bot.


```yaml
alias: 'telegram bot'
hide_entity: true
trigger:
  platform: event
  event_type: telegram_command
  event_data:
    command: '/ping'
action:
  - service: notify.telegram
    data:
      message: "pong"
  - service: tts.google_say 
    data:
      entity_id: media_player.gstreamer
      message: "this is a test pong reply"
```

```yaml
hide_entity: true
trigger:
  platform: event
  event_type: telegram_command
  event_data:
    command: '/siren'
action:
  - service: homeassistant.turn_on
    entity_id: switch.vision_zm1601eu5_battery_operated_siren_switch_9_0
  - service: notify.telegram
    data:
      message: "siren ON"
  - delay: 
      seconds: 10
  - service: homeassistant.turn_off
    entity_id: switch.vision_zm1601eu5_battery_operated_siren_switch_9_0
  - service: notify.telegram
    data:
      message: "siren OFF"
```

## youtube

Configure pulse in headless mode http://wiki.csgalileo.org/doku.php/tips:audio#pulse_headless

Create youtube-dl update job in /etc/cron.daily/update-youtube-dl (chmod +x)
```
#!/bin/sh

wget https://yt-dl.org/latest/youtube-dl -O /tmp/youtube-dl

if [ ! -z /tmp/youtube-dl ]; then
        mv /tmp/youtube-dl /usr/local/bin/youtube-dl
        chmod +x /usr/local/bin/youtube-dl
fi

```

Execute at least one time /etc/cron.daily/update-youtube-dl

Put youtube-play in /home/pi and create automation/telegram-youtube

Create shell_command.yaml (adjusting path inside) and import from configuration.yaml
