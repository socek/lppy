class LDPlugin:

    def setUp(self, app, configuration):
        self.app = app
        self.configuration = configuration.get(self.name, {})

    def get_action_resolvers(self):
        return {}
