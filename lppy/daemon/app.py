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


class Application:
    def __init__(self):
        self.configuration: Configuration = Configuration()
        self.plugins = {}
        self.devices = {}
        self.state = False

    async def init(self):
        self.plugins = {}
        self.devices = {}
        self._configuration = self.configuration.read(DEFAULT_CONFIGURATION_PATH)

        for plugin_class in get_plugins():
            plugin = plugin_class()
            plugin.setUp(self, self._configuration)
            self.plugins[plugin.name] = plugin

        self.state = True

    def configure_new_devices(self):
        for conf in self._configuration.get("devices", []):
            lp = LoupeDeckLive()
            lp.setUp(self, conf)
            if lp.name in self.devices and self.devices[lp.name].state:
                continue
            self.devices[lp.name] = lp
            yield lp

    def exit_application(self, *args, **kwargs):
        print("\rExiting...")
        for device in self.devices.values() or []:
            device.state = False
        self.state = False

    def get_all_tasks(self, devices):
        for device in devices:
            yield repaint_task(device)
            yield communicate(device)

    def remove_device(self, lp: LoupeDeckLive):
        if lp.name in self.devices:
            del self.devices[lp.name]

    async def start_devices_tasks(self):
        for device in self.configure_new_devices():
            if await device.connect():
                print(f"Device {device.configuration['url']} connected")
                await device.send_configuration()
                yield repaint_task(device)
                yield communicate(device)


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
