import logging
import threading

import config
from flask import Flask, request, abort, Response, jsonify
from strategies.colors.FixedColor import FixedColor
from strategies.light.Breath import Breath
from strategies.light.SimpleColor import SimpleColor
from strategies.light.TimedWrapper import TimedWrapper
from strategies.light.TurnedOff import TurnedOff


from werkzeug.serving import make_server

from strategies.screen.DisplayScrollingMessage import DisplayScrollingMessage
from strategies.screen.QuickTime import QuickTime
from strategies.screen.RealClockTime import RealClockTime

DEFAULT_COLOR = [255, 172, 68]

_state_lock = threading.Lock()
_light_state = {
    'state': 'off',
    'mode': 'off',
    'color': {'r': DEFAULT_COLOR[0], 'g': DEFAULT_COLOR[1], 'b': DEFAULT_COLOR[2]},
}


def _update_light_state(**kwargs):
    with _state_lock:
        _light_state.update(kwargs)
    if config.on_light_state_change is not None:
        config.on_light_state_change(dict(_light_state))


def _get_light_state():
    with _state_lock:
        return dict(_light_state)


def _light_on(light, rgb=None):
    if rgb is None:
        rgb = DEFAULT_COLOR
    _update_light_state(state='on', mode='solid', color={'r': rgb[0], 'g': rgb[1], 'b': rgb[2]})
    config.scheduler.set_light_thread(SimpleColor(light, FixedColor(rgb)))


def _light_off(light):
    _update_light_state(state='off', mode='off')
    config.scheduler.set_light_thread(TurnedOff(light))


def get_color_from_query(args):
    r = int(args.get('r', None))
    g = int(args.get('g', None))
    b = int(args.get('b', None))
    return FixedColor([r, g, b])


class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('0.0.0.0', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        logging.info('Starting web server')
        self.server.serve_forever()

    def shutdown(self):
        logging.info('Stopping web server')
        self.server.shutdown()


def start_rest_server(light, disp):
    app = Flask(__name__)

    @app.route("/ping")
    def ping():
        return 'pong'

    @app.route("/light/<mode>", methods=['POST'])
    def switch_light_mode(mode):
        if(mode == 'on'):
            _light_on(light)
        if(mode == 'off'):
            _light_off(light)
        return 'OK'

    @app.route("/light/color", methods=['POST'])
    def display_light_color():
        try:
            r = int(request.args['r'])
            g = int(request.args['g'])
            b = int(request.args['b'])
        except (KeyError, ValueError):
            abort(Response('r, g and b query params are mandatory and must be valid numbers', 400))

        requested_time = int(request.args.get('time', -1))
        _update_light_state(state='on', mode='solid', color={'r': r, 'g': g, 'b': b})
        if requested_time > 0:
            wrapped_thread = TimedWrapper(SimpleColor(light, FixedColor([r, g, b])), requested_time)
            config.scheduler.temporary_set_light_thread(wrapped_thread)
        else:
            _light_on(light, [r, g, b])
        return 'OK'

    @app.route("/light/breath", methods=['POST'])
    def display_light_breath():
        _update_light_state(state='on', mode='breath')
        config.scheduler.set_light_thread(Breath(
            light,
            hue=0.08,
            sat=0.9,
            value_target=0.99,
            value_from=0.1,
            duration=[2.5, 2.5],
            pauses=[0.05, 0.8],
            frequency=40
        ))
        return 'OK'

    @app.route("/light/switch", methods=['GET', 'POST'])
    def switch_light():
        if request.method == 'GET':
            return jsonify(_get_light_state())

        body = request.get_json(silent=True) or {}
        state = body.get('state')
        if state == 'on':
            color = body.get('color')
            if isinstance(color, dict):
                try:
                    rgb = [int(color['r']), int(color['g']), int(color['b'])]
                except (KeyError, TypeError, ValueError):
                    abort(Response('color must provide r, g and b as numbers', 400))
                _light_on(light, rgb)
            else:
                _light_on(light)
        elif state == 'off':
            _light_off(light)
        else:
            abort(Response('body must be JSON with a "state" of "on" or "off"', 400))
        return 'OK'

    @app.route("/display/text/<text>", methods=['POST'])
    def display_custom_text(text):
        color = None
        duration = len(text) / 3 + 1
        try:
            color = get_color_from_query(request.args)
        finally:
            if(color):
                config.scheduler.temporary_switch_screen_thread(
                    DisplayScrollingMessage(
                        disp, text, duration, screen_color_strategy=color)
                )
            else:
                config.scheduler.temporary_switch_screen_thread(
                    DisplayScrollingMessage(
                        disp, text, duration)
                )
            return 'OK'

    @app.route("/display/date", methods=['POST'])
    def display_date():
        config.scheduler.set_screen_thread(RealClockTime(disp))
        return 'OK'

    @app.route("/display/date/quick", methods=['POST'])
    def display_quick_date():
        config.scheduler.set_screen_thread(QuickTime(disp))
        return 'OK'

    server = ServerThread(app)
    server.start()
    return server
    # server_thread = Process(target=app.run, kwargs=dict(host='0.0.0.0'))
    # server_thread.start()
    # return server_thread
