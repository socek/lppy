import os.path
import pkgutil
from importlib import import_module

from lppy import plugins
from lppy.driver.configuration import Configuration
from lppy.driver.devices import LoupeDeckLive
from lppy.driver.plugin import LDPlugin


class Application:
    def __init__(self):
        self.devices: list | None = None
        self.configuration: Configuration = Configuration()
        self.plugins = {}

    async def init(self):
        configuration = self.configuration.read(None)
        self.devices = []

        for plugin_class in get_plugins():
            plugin = plugin_class()
            plugin.setUp(self, configuration)
            self.plugins[plugin.name] = plugin

        for conf in configuration.get("devices", []):
            lp = LoupeDeckLive()
            lp.setUp(self, conf)
            self.devices.append(lp)

        for device in self.devices:
            if await device.connect():
                print(f"Device {device.configuration['url']} connected")
                await device.send_configuration()

        return [device.read() for device in self.devices] + [
            device.repaint_task() for device in self.devices
        ]

    def exit_application(self, *args, **kwargs):
        print("\rExiting...")
        for device in self.devices or []:
            device.state = False


def get_plugins():
    pkgpath = os.path.dirname(plugins.__file__)
    names = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
    for name in names:
        try:
            module = import_module(f"lppy.plugins.{name}.plugin")
        except ModuleNotFoundError:
            continue

        for objname in dir(module):
            obj = getattr(module, objname)
            try:
                if issubclass(obj, LDPlugin) and not obj is LDPlugin:
                    yield obj
            except TypeError:
                continue
