import logging
import config
from flask import Flask, request, abort, Response
from multiprocessing import Process
from strategies.colors.FixedColor import FixedColor
from strategies.light.Breath import Breath
from strategies.light.SimpleColor import SimpleColor
from strategies.light.TurnedOff import TurnedOff


from werkzeug.serving import make_server
import threading

from strategies.screen.DisplayScrollingMessage import DisplayScrollingMessage
from strategies.screen.QuickTime import QuickTime
from strategies.screen.RealClockTime import RealClockTime


def get_color_from_query(args):
    r = int(request.args.get('r', None))
    g = int(request.args.get('g', None))
    b = int(request.args.get('b', None))
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
            config.scheduler.set_light_thread(
                SimpleColor(light, FixedColor([255, 172, 68])))
        if(mode == 'off'):
            config.scheduler.set_light_thread(TurnedOff(light))
        return 'OK'

    @app.route("/light/color", methods=['POST'])
    def display_light_color():
        color_strategy = None
        try:
            color_strategy = get_color_from_query(request.args)
        except:
            abort(Response('r, g and b query params are mandatory and must be valid numbers given : r:' +
                  str(r)+', g:'+str(g)+', b:'+str(b), 400))
        config.scheduler.set_light_thread(
            SimpleColor(
                light,
                color_strategy
            )
        )
        return 'OK'

    @app.route("/light/breath", methods=['POST'])
    def display_light_breath():
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

    @app.route("/display/text/<text>", methods=['POST'])
    def display_custom_text(text):
        color = None
        try:
            color = get_color_from_query(request.args)
        finally:
            if(color):
                config.scheduler.temporary_switch_screen_thread(
                    DisplayScrollingMessage(
                        disp, text, 2, screen_color_strategy=color)
                )
            else:
                config.scheduler.temporary_switch_screen_thread(
                    DisplayScrollingMessage(
                        disp, text, 2)
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
