from gunicorn.app.base import BaseApplication
from app import app
from bot import bot

class StandaloneApplication(BaseApplication):
    def __init__(self, app, bot, options=None):
        self.options = options or {}
        self.application = app
        self.bot = bot
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':
    options = {
        'bind': '0.0.0.0:80',
        'workers': 1
    }
    StandaloneApplication(app, bot, options).run()
