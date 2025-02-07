from subprocess import STDOUT
from subprocess import TimeoutExpired
from subprocess import check_output

from lppy.driver.action_resolvers import ScreenKey


def run(cmd):
    try:
        output = check_output(cmd, stderr=STDOUT, timeout=1)
    except TimeoutExpired:
        # TODO: make better logging
        print(f"[{cmd!r} timeouted]")
        return None
    except CalledProcessError:
        print(f"[{cmd!r} failed]")
        return None

    return output.decode().strip()


def command(command: str, player: str = None):
    def gen():
        yield "/usr/bin/playerctl"
        if player:
            yield "-p"
            yield player
        yield command

    return run(list(gen()))


class PlayPauseSK(ScreenKey):
    def get_paint_configuration(self):
        config = super().get_paint_configuration()
        player = self.configuration.get("player")
        status = command("status", player)

        if status == "Playing":
            config["background"] = "green"
        elif status in ["Stopped", "Paused"]:
            config["background"] = "black"
        else:
            config["background"] = "grey"
        return config

    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        player = self.configuration.get("player")
        command("play-pause", player)


class PreviousSK(ScreenKey):
    def get_paint_configuration(self):
        config = super().get_paint_configuration()

        player = self.configuration.get("player")
        status = command("status", player)

        if status in ["Playing", "Stopped", "Paused"]:
            config["background"] = "black"
        else:
            config["background"] = "grey"
        return config

    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        player = self.configuration.get("player")
        command("previous", player)


class NextSK(ScreenKey):
    def get_paint_configuration(self):
        config = super().get_paint_configuration()

        player = self.configuration.get("player")
        status = command("status", player)

        if status in ["Playing", "Stopped", "Paused"]:
            config["background"] = "black"
        else:
            config["background"] = "grey"
        return config

    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        player = self.configuration.get("player")
        command("next", player)
