"""
Allows utilizing telegram webhooks.

See https://core.telegram.org/bots/webhooks for details
 about webhooks.

"""
import asyncio
import logging
from ipaddress import ip_network
import json

import voluptuous as vol

from homeassistant.const import (
    HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.http import HomeAssistantView
from homeassistant.const import CONF_API_KEY
from homeassistant.components.http.util import get_real_ip

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = []

EVENT_GRAFANA_COMMAND = 'grafana.alert'

ATTR_COMMAND = 'command'
DEPENDENCIES = ['http']
DOMAIN = 'grafana_webhooks'
CONF_HANDLER_URL = '/api/grafana_webhooks'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        #vol.Optional(CONF_API_KEY, default=''): cv.string,
        #vol.Optional(CONF_TRUSTED_NETWORKS, default=DEFAULT_TRUSTED_NETWORKS):
        #    vol.All(cv.ensure_list, [ip_network]),
        #vol.Required(CONF_USER_ID): {cv.string: cv.positive_int},
    }),
}, extra=vol.ALLOW_EXTRA)

"""
{
'ruleId': 1, 
'state': 'ok', 
'ruleUrl': 'http://localhost:3000/grafana/dashboard/db/energia?fullscreen&edit&tab=alert&panelId=1', 
'evalMatches': [], 'message': '{"message":"frigorifero"}', 
'title': '[OK] Consumi alert', 
'ruleName': 'Consumi alert'
}
"""


def setup(hass, config):
    """Setup the telegram_webhooks component.

    register webhook if API_KEY is specified
    register /api/telegram_webhooks as web service for telegram bot
    """
    config = config[DOMAIN]
    hass.http.register_view(GrafanaPushReceiver())
    return True


class GrafanaPushReceiver(HomeAssistantView):
    """Handle pushes from telegram."""

    requires_auth = True
    url = CONF_HANDLER_URL
    name = "grafana_webhooks"

    def __init__(self):
        """Initialize users allowed to send messages to bot."""
        pass

    @asyncio.coroutine
    def post(self, request):
        """Accept the POST from telegram."""
        try:
            data = yield from request.json()
        except (ValueError, IndexError):
            return self.json_message('Invalid JSON', HTTP_BAD_REQUEST)

        _LOGGER.debug("Received grafana data: %s", json.dumps(data))

        request.app['hass'].bus.async_fire(EVENT_GRAFANA_COMMAND, {
            'payload':json.dumps(data)
            })
        return self.json({})
