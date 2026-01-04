from lppy.driver.plugin import LDPlugin
from lppy.plugins.playerctl.keys import NextSK
from lppy.plugins.playerctl.keys import PlayPauseSK
from lppy.plugins.playerctl.keys import PreviousSK


class PlayerCtlPlugin(LDPlugin):
    name = "playerctl"

    def get_action_resolvers(self):
        return {
            "play_pause": PlayPauseSK,
            "next": NextSK,
            "previous": PreviousSK,
        }
