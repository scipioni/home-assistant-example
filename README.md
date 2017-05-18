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

## telegram webhooks

```yaml
# Example configuration.yaml entry
telegram_webhooks:
  api_key: ABCDEFGHJKLMNOPQRSTUVXYZ
  api_url: https://<PUBLIC_HOST>/api/telegram_webhooks
  user_id:
    user1: USER_ID
    user2: USER_ID
```

Configuration variables:

- **user_id** array (Required): List of users allowed to send messages to
 webhooks (formt name: USER_ID).
- **api_key** (*Optional*): The API token of yout bot. Setting the optional
 parameter `api_key` (with api_url) make an automatic registration of webhook
in telgram bot.
- **api_url** (*Optional*): The API token of your bot
 (see api_key for automatic update of webhooks url)


```yaml

alias: 'telegram bot ping pong to check presence of bot'
hide_entity: true
trigger:
  platform: state
  entity_id: telegram_webhooks.command
  to: '/ping'
action:
  - service: notify.telegram
    data:
      message: 'pong'
```

```yaml
alias: 'telegram bot start command'
hide_entity: true
trigger:
  platform: state
  entity_id: telegram_webhooks.command
  to: '/start'
action:
  - service: notify.telegram
    data:
      message: 'commands'
      data:
        keyboard:
          - '/ping, /alarm'
          - '/siren'
```

## youtube

Configure pulse in headless mode http://wiki.csgalileo.org/doku.php/tips:audio#pulse_headless

Create youtube-dl update job in /etc/cron.daily/update-youtube-dl (chmod +x)
```
#!/bin/sh

wget https://yt-dl.org/latest/youtube-dl -O /usr/local/bin/youtube-dl

```

Execute at least one time /etc/cron.daily/update-youtube-dl

Put youtube-play in /home/pi and create automation/telegram-youtube

Create shell_command.yaml (adjusting path inside) and import from configuration.yaml
