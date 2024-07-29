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
            plugin = self.device.application.plugins[action_resolver_configuration["plugin"]]
            action_resolver = plugin.get_action_resolvers()[action_resolver_configuration["type"]]
            self.action_resolvers[key] = action_resolver()
            self.action_resolvers[key].setUp(self, key, action_resolver_configuration)

    def get_action_resolver(self, name: str):
        return self.action_resolvers.get(name)

    def get_all_graphic_resolvers(self):
        for value in self.action_resolvers.values():
            if value.can_be_painted:
                yield value

    async def handle_command(self, key, action, *payload):
        for ar_key, value in self.action_resolvers.items():
            if ar_key == key:
                continue
            await value.reset()

        resolver = self.action_resolvers.get(key)
        if not resolver:
            return

        action_function = getattr(resolver, action)
        return await action_function(*payload)
