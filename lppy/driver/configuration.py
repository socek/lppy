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
                            "plugin": "runscript",
                            "type": "exec",
                            "cmd": "/home/socek/tmp/run1.sh",
                        },
                        "key2": {
                            "name": "Play/Pause",
                            "plugin": "runscript",
                            "type": "exec",
                            "cmd": "/home/socek/tmp/run2.sh",
                        },
                        "key3": {
                            "name": "Next",
                            "plugin": "runscript",
                            "type": "exec",
                            "cmd": "/home/socek/tmp/run3.sh",
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
