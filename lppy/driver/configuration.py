from os.path import expanduser

from tomli_w import dump as toml_write
from tomllib import load as toml_read


class Configuration:
    def __init__(self):
        self.configuration: dict | None = None
        self.path: str | None = None

    def read(self, path: str) -> dict:
        self.path = expanduser(path)
        with open(self.path, "rb") as conffile:
            self.configuration = toml_read(conffile)
        return self.configuration

    def write(self):
        assert self.path
        with open(self.path, "wb") as conffile:
            toml_write(self.configuration, conffile)
