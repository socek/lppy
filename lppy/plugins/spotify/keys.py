from gi.repository import GLib
from pydbus import SessionBus

from lppy.driver.action_resolvers import ScreenKey


def get_spotify():
    bus = SessionBus()
    try:
        proxy = bus.get("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
        return proxy["org.mpris.MediaPlayer2.Player"]
    except GLib.GError:
        return None


class PlayPauseSK(ScreenKey):
    def get_paint_configuration(self):
        config = super().get_paint_configuration()
        spotify = get_spotify()
        if not spotify:
            config["background"] = "grey"
            return config

        if spotify.PlaybackStatus == "Playing":
            config["background"] = "green"
        return config

    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        spotify = get_spotify()
        spotify and spotify.PlayPause()


class PreviousSK(ScreenKey):
    def get_paint_configuration(self):
        config = super().get_paint_configuration()
        spotify = get_spotify()
        if not spotify:
            config["background"] = "grey"
        return config

    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        spotify = get_spotify()
        spotify and spotify.Previous()


class NextSK(ScreenKey):
    def get_paint_configuration(self):
        config = super().get_paint_configuration()
        spotify = get_spotify()
        if not spotify:
            config["background"] = "grey"
        return config

    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        spotify = get_spotify()
        spotify and spotify.Next()
