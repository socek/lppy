from asyncio import TaskGroup
from asyncio import ensure_future
from asyncio import get_event_loop
from asyncio import sleep
from importlib import import_module
from os.path import dirname
from pkgutil import iter_modules
from signal import SIGINT
from signal import SIGTERM
from signal import SIGUSR1
from signal import signal

from lppy import plugins
from lppy.driver.configuration import Configuration
from lppy.driver.consts import DEFAULT_CONFIGURATION_PATH
from lppy.driver.consts import State
from lppy.driver.devices import LoupeDeckLive
from lppy.driver.plugin import LDPlugin
from lppy.driver.tasks import communicate
from lppy.driver.tasks import repaint_task


class Application:
    def __init__(self):
        self.configuration: Configuration = Configuration()
        self.plugins = {}
        self.devices = {}
        self.state = State.BEFORE_START

    def configure_new_devices(self):
        for conf in self._configuration.get("devices", []):
            lp = LoupeDeckLive()
            lp_config = self._configuration.get("configs", {}).get(conf.get("config"), {})
            lp.setUp(self, lp_config, conf["url"])
            if lp.name in self.devices and self.devices[lp.name].state:
                continue
            if not lp.connection_exists():
                continue
            self.devices[lp.name] = lp
            yield lp

    def get_all_tasks(self, devices):
        for device in devices:
            yield repaint_task(device)
            yield communicate(device)

    def remove_device(self, lp: LoupeDeckLive):
        if lp.name in self.devices:
            del self.devices[lp.name]

    async def start_devices_tasks(self):
        device_found = False
        for device in self.configure_new_devices():
            if await device.connect():
                print(f"Device {device.url} connected")
                device_found = True
                await device.send_configuration()
                yield repaint_task(device)
                yield communicate(device)
        if not device_found:
            print("No device found!")

    def refresh(self):
        print("Initializing...")
        self.plugins = {}
        self.devices = {}
        self._configuration = self.configuration.read(DEFAULT_CONFIGURATION_PATH)

        for plugin_class in get_plugins():
            plugin = plugin_class()
            plugin.setUp(self, self._configuration)
            self.plugins[plugin.name] = plugin

        self.state = State.RUNNING

    def init(self):
        for signalCode in [SIGINT, SIGTERM]:
            signal(signalCode, self.exit_application)
        signal(SIGUSR1, self.restart)

    def exit_application(self, *args, **kwargs):
        print("\rExiting...")
        self.state = State.EXITING
        for device in self.devices.values() or []:
            device.state = False

    def restart(self, *args, **kwargs):
        for device in self.devices.values() or []:
            device.state = False
        self.state = State.RESTART

    async def run_all_tasks(self):
        async with TaskGroup() as tg:
            while self.state == State.RUNNING:
                async for task in self.start_devices_tasks():
                    tg.create_task(task)
                await sleep(1)

    def main(self):
        self.init()
        while self.state in (State.BEFORE_START, State.RUNNING, State.RESTART):
            self.refresh()
            get_event_loop().run_until_complete(ensure_future(self.run_all_tasks()))


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
