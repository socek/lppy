from lppy.driver.action_resolvers import Knob
from lppy.driver.action_resolvers import ScreenKey

translator = {
    "knob1": Knob,
    "knob2": Knob,
    "key1": ScreenKey,
    "key2": ScreenKey,
    "key3": ScreenKey,
}


class Page:
    def __init__(self):
        self.device = None
        self.configuration = None
        self.action_resolvers = {}

    def setUp(self, device, configuration):
        self.device = device
        self.configuration = configuration
        configs = configuration.get("action_resolvers", {})
        for key, action_resolver_configuration in configs.items():
            self.action_resolvers[key] = translator[key]()
            self.action_resolvers[key].setUp(self, key, action_resolver_configuration)

    def get_action_resolver(self, name: str):
        return self.action_resolvers.get(name)

    def get_all_graphic_resolvers(self):
        for value in self.action_resolvers.values():
            if value.can_be_painted:
                yield value

    async def handle_command(self, key, action, *payload):
        resolver = self.action_resolvers.get(key)
        if not resolver:
            return

        action_function = getattr(resolver, action)
        return await action_function(*payload)
