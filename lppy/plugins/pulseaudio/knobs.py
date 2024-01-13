from pulsectl import Pulse

from lppy.driver.action_resolvers import CircleKnob

pulse = Pulse("ldpy")


def get_sink_input_by_name(name):
    for sink in pulse.sink_input_list():
        if sink.name == name:
            yield sink


def get_sink_by_name(name):
    for sink in pulse.sink_list():
        if sink.name == name:
            yield sink


def get_sink_by_application_name(name):
    for sink in pulse.sink_input_list():
        if sink.proplist.get("application.name") == name:
            yield sink


def get_source_by_name(name):
    for sink in pulse.source_list():
        if sink.name == name:
            yield sink


def get_stream_restore_by_name(name):
    for sink in pulse.stream_restore_list():
        if sink.name == name:
            yield sink


sink_type_translator = {
    "sink-input": get_sink_input_by_name,
    "sink": get_sink_by_name,
    "source": get_source_by_name,
    "stream-restore": get_stream_restore_by_name,
    "application": get_sink_by_application_name,
}


class VolumeCK(CircleKnob):
    def get_sink_objects(self):
        assert self.configuration
        fun = sink_type_translator[self.configuration["sink_type"]]
        return fun(self.configuration["sink_name"])

    def get_paint_configuration(self):
        for sink in self.get_sink_objects():
            value = int(sink.volume.value_flat * 100)

            conf = {
                "draw_circle": True,
                "percentage": value,
                "first_circle": value if value >= 100 else value - 100,
                "second_circle": max([value - 100, 0]),
                "background": "black",
            }
            if sink.mute:
                conf["backbox_color"] = "red"
                conf["additional_text"] = "MUTED"
            return conf

        return {
            "draw_circle": False,
            "percentage": "(off)",
            "first_circle": 0,
            "second_circle": 0,
            "background": "black",
            "backbox_color": "#4444",
        }

    async def rotate(self, right: bool):
        for sink in self.get_sink_objects():
            volume = sink.volume
            if right:
                volume.value_flat += 0.05
            else:
                volume.value_flat -= 0.05
                if volume.value_flat < 0:
                    volume.value_flat = 0
            pulse.volume_set(sink, volume)

    async def press(self):
        for sink in self.get_sink_objects():
            pulse.mute(sink, not sink.mute)
