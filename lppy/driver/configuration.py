sample = {
    "devices": [
        {
            "url": "/dev/ttyACM0",
            "brightness": 10,
            "pages": {
                "1": {
                    "action_resolvers": {
                        # "knob1": {
                        #     "name": "Spotify",
                        #     "type": "pulseaudio:Sink",
                        #     "sinkName": "spotify",
                        # },
                        # "knob2": {
                        #     "name": "Home",
                        #     "type": "pulseaudio:Sink",
                        #     "sinkName": "spotify2",
                        # },
                        "key1": {
                            "name": "Previous",
                            "plugin": "spotify",
                            "type": "previous",
                        },
                        "key2": {
                            "name": "Play/Pause",
                            "plugin": "spotify",
                            "type": "play_pause",
                        },
                        "key3": {
                            "name": "Next",
                            "plugin": "spotify",
                            "type": "next",
                        }
                    }
                }
            }
        }
    ]
}


class Configuration:
    def __init__(self):
        self.configuration: list | None = None
        self.path = None

    def read(self, path: str) -> dict:
        self.configuration = sample
        self.path = path
        return self.configuration

    def write(self):
        pass
