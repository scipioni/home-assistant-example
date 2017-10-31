# home-assistant-example
home-assistant real configuration


## camera motion trigger

![Alt text](http://g.gravizo.com/g?
  digraph G {
    aize ="5,5";
    camera -> ftp [label="on motion"]
    ftp -> incron -> onmotion
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

## camera FTP clean

/etc/cron.daily/photo-clean
```
#!/bin/sh

ARCHIVE=/media/photo
DAYS=2

find ${ARCHIVE} -mtime +${DAYS} -exec rm {} \;

```

## camera FTP stop/start 

create file /etc/sudoers.d/pi
```
pi  ALL=(ALL:ALL) NOPASSWD: /bin/systemctl * pure-ftpd.service
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
