from lppy.driver.plugin import LDPlugin
from lppy.plugins.obs.keys import SetScene
from lppy.plugins.obs.knobs import InputVolume


class ObsPlugin(LDPlugin):
    name = "obs"

    @property
    def conf(self) -> dict:
        return self.configuration.get("plugins", {}).get("obs", {})

    def get_action_resolvers(self):
        return {
            "set_scene": SetScene,
            "input_volume": InputVolume,
        }
