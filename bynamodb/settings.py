# -*-coding:utf8-*-

__all__ = 'conf'


class Settings(object):
    def __init__(self):
        self.config = dict()

    def __getitem__(self, key):
        return self.config[key]

    def get(self, key, default=None):
        return self.config.get(key, default)

    def load_settings_from(self, settings):
        self.config.update(settings)


conf = Settings()
