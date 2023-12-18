from lppy.driver.action_resolvers import GraphicActionResolver


class Page:
    def __init__(self):
        self.device = None
        self.configuration = None
        self.action_resolvers = {}

    def setUp(self, device, configuration):
        self.device = device
        self.configuration = configuration
        for key, action_resolver_configuration in configuration.get("action_resolvers", {}).items():
            self.action_resolvers[key] = GraphicActionResolver()
            self.action_resolvers[key].setUp(self, key, action_resolver_configuration)

    def get_action_resolver(self, name: str):
        return self.action_resolvers.get(name)

    def get_all_graphic_resolvers(self):
        for value in self.action_resolvers.values():
            if value.can_be_painted:
                yield value
