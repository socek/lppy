from lppy.driver.action_resolvers import CircleKnob
from lppy.plugins.obs.models import ObsConnection


class InputVolume(CircleKnob):
    CHANGE_VALUE = 3

    @property
    def input_name(self):
        assert self.configuration
        return self.configuration["input_name"]


    def get_paint_configuration(self):
        conf = {
            "draw_circle": False,
            "percentage": "(off)",
            "first_circle": 0,
            "second_circle": 0,
            "background": "black",
            "backbox_color": "#4444",
        }
        if not ObsConnection.validate_connection():
            return conf
        volume = ObsConnection.get_input_volume(self.input_name)
        if not volume:
            return conf
        conf["percentage"] = f"{volume:.0f}%"
        if ObsConnection.get_input_mute(self.input_name):
            conf["backbox_color"] = "red"
            conf["additional_text"] = "MUTED"
            return conf


        return {
            "draw_circle": True,
            "percentage": f"{volume:.0f}%",
            "first_circle": volume if volume >= 100 else volume - 100,
            "second_circle": max([volume - 100, 0]),
            "background": "black",
        }

    async def rotate(self, right: bool):
        if not ObsConnection.validate_connection():
            return

        old_volume = ObsConnection.get_input_volume(self.input_name) or 0
        new_volume = old_volume + self.CHANGE_VALUE * (1 if right else -1)
        ObsConnection.set_input_volume(self.input_name, new_volume)

    async def press(self):
        if not ObsConnection.validate_connection():
            return
        ObsConnection.toggle_input_mute(self.input_name)
