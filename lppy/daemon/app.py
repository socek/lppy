from importlib import import_module
from os.path import dirname
from pkgutil import iter_modules

from lppy import plugins
from lppy.driver.configuration import Configuration
from lppy.driver.consts import DEFAULT_CONFIGURATION_PATH
from lppy.driver.devices import LoupeDeckLive
from lppy.driver.plugin import LDPlugin
from lppy.driver.tasks import communicate
from lppy.driver.tasks import repaint_task


def get_all_tasks(devices):
    for device in devices:
        yield repaint_task(device)
        yield communicate(device)


class Application:
    def __init__(self):
        self.devices: list | None = None
        self.configuration: Configuration = Configuration()
        self.plugins = {}

    async def init(self):
        configuration = self.configuration.read(DEFAULT_CONFIGURATION_PATH)
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

        return list(get_all_tasks(self.devices))

    def exit_application(self, *args, **kwargs):
        print("\rExiting...")
        for device in self.devices or []:
            device.state = False


def get_plugins():
    pkgpath = dirname(plugins.__file__)
    names = [name for _, name, _ in iter_modules([pkgpath])]
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
