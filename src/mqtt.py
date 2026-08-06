import json
import logging
import os
import threading

import config
from strategies.colors.FixedColor import FixedColor
from strategies.light.SimpleColor import SimpleColor
from strategies.light.TurnedOff import TurnedOff

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

CONFIG_FILE = '/etc/aurora/mqtt.conf'

DEFAULT_BASE_TOPIC = 'aurora/light'
DEFAULT_DISCOVERY_PREFIX = 'homeassistant'

_state_lock = threading.Lock()
_mirror = {
    'state': 'OFF',
    'color': {'r': 255, 'g': 172, 'b': 68},
    'brightness': 255,
}

_client = None
_light = None
_command_topic = None
_state_topic = None
_availability_topic = None
_discovery_topic = None


def _load_settings():
    settings = {}
    try:
        with open(CONFIG_FILE, 'r') as fptr:
            for line in fptr:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    settings[key.strip()] = value.strip()
    except IOError:
        logging.info("MQTT : no config file at %s, falling back to environment", CONFIG_FILE)
    return settings


def _setting(settings, name, default=None):
    for key in (name, 'MQTT_' + name):
        if key in settings:
            return settings[key]
    return os.environ.get('MQTT_' + name, default)


def _publish_state():
    if _client is None:
        return
    with _state_lock:
        payload = json.dumps(_mirror)
    _client.publish(_state_topic, payload, qos=0, retain=True)


def _discovery_payload():
    return {
        'name': 'Aurora',
        'unique_id': 'aurora_led_light',
        'schema': 'json',
        'command_topic': _command_topic,
        'state_topic': _state_topic,
        'availability_topic': _availability_topic,
        'payload_available': 'online',
        'payload_not_available': 'offline',
        'brightness': True,
        'color_mode': True,
        'supported_color_modes': ['rgb'],
        'qos': 0,
        'retain': True,
    }


def _apply_command(payload):
    with _state_lock:
        state = _mirror['state']
        color = dict(_mirror['color'])
        brightness = _mirror['brightness']

    if 'state' in payload:
        state = 'ON' if payload['state'] in ('ON', 'on', True, 1) else 'OFF'

    if isinstance(payload.get('color'), dict):
        color = {
            'r': int(payload['color']['r']),
            'g': int(payload['color']['g']),
            'b': int(payload['color']['b']),
        }

    if 'brightness' in payload:
        try:
            brightness = max(0, min(255, int(payload['brightness'])))
        except (TypeError, ValueError):
            brightness = 255

    with _state_lock:
        _mirror['state'] = state
        _mirror['color'] = color
        _mirror['brightness'] = brightness

    if state == 'ON':
        thread = SimpleColor(_light, FixedColor(
            [color['r'], color['g'], color['b']],
            luminosity=brightness / 255.0,
        ))
    else:
        thread = TurnedOff(_light)
    config.scheduler.set_light_thread(thread)

    _publish_state()


def _on_connect(client, userdata, flags, rc):
    logging.info('MQTT : connected to broker (rc=%s)', rc)
    client.subscribe(_command_topic)
    client.publish(_availability_topic, 'online', retain=True)
    _publish_state()


def _on_disconnect(client, userdata, rc):
    logging.warning('MQTT : disconnected from broker (rc=%s)', rc)
    try:
        client.publish(_availability_topic, 'offline', retain=True)
    except Exception as err:
        logging.warning('MQTT : could not publish offline state : %s', err)


def _on_message(client, userdata, msg):
    logging.info('MQTT : command on %s : %s', msg.topic, msg.payload)
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
    except ValueError:
        logging.warning('MQTT : ignoring invalid JSON command : %s', msg.payload)
        return
    if not isinstance(payload, dict):
        logging.warning('MQTT : ignoring non-object command : %s', msg.payload)
        return
    try:
        _apply_command(payload)
    except Exception as err:
        logging.error('MQTT : failed to apply command : %s', err)


def _on_external_state_change(state):
    with _state_lock:
        _mirror['state'] = 'ON' if state.get('state') == 'on' else 'OFF'
        if isinstance(state.get('color'), dict):
            _mirror['color'] = dict(state['color'])
        if _mirror['state'] == 'ON':
            _mirror['brightness'] = 255
    _publish_state()


def _on_local_toggle():
    with _state_lock:
        _mirror['state'] = 'OFF' if _mirror['state'] == 'ON' else 'ON'
        if _mirror['state'] == 'ON':
            _mirror['brightness'] = 255
    _publish_state()


def start_mqtt(light):
    if mqtt is None:
        logging.error('MQTT : paho-mqtt is not installed, MQTT disabled')
        return None

    global _light, _client, _command_topic, _state_topic, _availability_topic, _discovery_topic

    settings = _load_settings()
    host = _setting(settings, 'HOST', None)
    if not host:
        logging.warning('MQTT : no host configured (create %s), MQTT disabled', CONFIG_FILE)
        return None

    _light = light
    base_topic = _setting(settings, 'BASE_TOPIC', DEFAULT_BASE_TOPIC).strip('/')
    prefix = _setting(settings, 'DISCOVERY_PREFIX', DEFAULT_DISCOVERY_PREFIX).strip('/')
    _command_topic = base_topic + '/set'
    _state_topic = base_topic + '/state'
    _availability_topic = base_topic + '/availability'
    _discovery_topic = prefix + '/light/aurora/config'

    try:
        port = int(_setting(settings, 'PORT', 1883))
    except ValueError:
        port = 1883

    client = mqtt.Client(client_id='aurora')
    user = _setting(settings, 'USER', None)
    password = _setting(settings, 'PASS', None)
    if user:
        client.username_pw_set(user, password)

    client.on_connect = _on_connect
    client.on_disconnect = _on_disconnect
    client.on_message = _on_message
    client.reconnect_delay_set(min_delay=5, max_delay=60)

    try:
        client.connect(host, port, keepalive=60)
    except Exception as err:
        logging.error('MQTT : failed to connect to %s:%s : %s', host, port, err)
        return None

    client.loop_start()
    _client = client
    client.publish(_discovery_topic, json.dumps(_discovery_payload()), retain=True)

    config.on_light_state_change = _on_external_state_change
    config.mqtt_toggle_sync = _on_local_toggle

    logging.info('MQTT : started (host=%s:%s, base_topic=%s)', host, port, base_topic)
    return client
