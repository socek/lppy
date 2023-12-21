from pydbus import SessionBus

from lppy.driver.action_resolvers import ScreenKey


def get_spotify():
    bus = SessionBus()
    proxy = bus.get("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
    return proxy["org.mpris.MediaPlayer2.Player"]


class PlayPauseSK(ScreenKey):
    def get_paint_configuration(self):
        config = super().get_paint_configuration()
        if get_spotify().PlaybackStatus == "Playing":
            config["background"] = "green"
        return config

    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        get_spotify().PlayPause()


class PreviousSK(ScreenKey):
    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        get_spotify().Previous()


class NextSK(ScreenKey):
    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        get_spotify().Next()
