from lppy.driver.plugin import LDPlugin
from lppy.plugins.spotify.keys import NextSK
from lppy.plugins.spotify.keys import PlayPauseSK
from lppy.plugins.spotify.keys import PreviousSK


class SpotifyPlugin(LDPlugin):
    name = "spotify"

    def get_action_resolvers(self):
        return {
            "play_pause": PlayPauseSK,
            "next": NextSK,
            "previous": PreviousSK,
        }
