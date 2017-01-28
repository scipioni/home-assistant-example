"""
Allows utilizing telegram bot.

"""

import asyncio
import logging
import os

import requests
import voluptuous as vol

from homeassistant.const import CONF_ACCESS_TOKEN, HTTP_BAD_REQUEST
from homeassistant.config import load_yaml_config_file
import homeassistant.helpers.config_validation as cv
from homeassistant.components.http import HomeAssistantView
from homeassistant.const import CONF_API_KEY

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['python-telegram-bot==5.3.0']

CONF_USER_ID = 'user_id'
CONF_API_URL = 'api_url'

DEPENDENCIES = ['http']
DOMAIN = 'telegram_bot'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_API_URL): cv.string,
        vol.Required(CONF_USER_ID): {cv.string: cv.positive_int},
    }),
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Setup the telegram_bot component."""
    import telegram

    config = config[DOMAIN]

    bot = telegram.Bot(config[CONF_API_KEY])
    current_status = bot.getWebhookInfo()
    _LOGGER.debug("telegram webhook status: %s", current_status)
    if current_status and current_status['url'] != config[CONF_API_URL]:
        if bot.setWebhook(config[CONF_API_URL]):
            _LOGGER.info("set new telegram webhook")
        else:
            _LOGGER.error("telegram webhook failed")

    hass.http.register_view(TelegrambotPushReceiver(config[CONF_USER_ID]))
    hass.states.set('{}.command'.format(DOMAIN), '')
    return True


class TelegrambotPushReceiver(HomeAssistantView):
    """Handle pushes from telegram."""

    requires_auth = False
    url = "/api/telegram_bot"
    name = "telegram_bot"

    def __init__(self, user_id):
        self.users = dict([(user_id, dev_id) for (dev_id, user_id) in user_id.items()])
        _LOGGER.debug("users allowed: %s", self.users)

    @asyncio.coroutine
    def post(self, request):
        """Accept the POST from telegram."""
        try:
            data = yield from request.json()
            data = data['message']
        except ValueError:
            return self.json_message('Invalid JSON', HTTP_BAD_REQUEST)

        try:
            assert data['from']['id'] in self.users
        except:
            _LOGGER.warn("User not allowed")
            return self.json_message('Invalid user', HTTP_BAD_REQUEST)

        _LOGGER.debug("Received telegram data: %s", data)
        try:
            assert data['text'][0] == '/'
        except:
            _LOGGER.warn('no command')
            return self.json({})

        request.app['hass'].states.async_set('{}.command'.format(DOMAIN), data['text'], force_update=True)
        request.app['hass'].states.async_set('{}.user_id'.format(DOMAIN), data['from']['id'], force_update=True)
        return self.json({})
