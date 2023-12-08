from lppy.driver.configuration import Configuration
from lppy.driver.devices import LoupeDeckLive


class Application:
    def __init__(self):
        self.devices: list | None = None
        self.configuration: Configuration = Configuration()

    async def init(self):
        configuration = self.configuration.read(None)
        self.devices = []

        for conf in configuration.get("devices", []):
            lp = LoupeDeckLive(conf)
            self.devices.append(lp)

        for device in self.devices:
            if await device.connect():
                print(f"Device {device.configuration['url']} connected")

        return [device.read() for device in self.devices]

    def exit_application(self, *args, **kwargs):
        print("\rExiting...")
        for device in self.devices or []:
            device.state = False
