from lppy.driver.plugin import LDPlugin
from lppy.plugins.pulseaudio.knobs import VolumeCK


class PulseAudioPlugin(LDPlugin):
    name = "pulseaudio"

    def get_action_resolvers(self):
        return {
            "volume": VolumeCK,
        }
