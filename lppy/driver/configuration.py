sample = {
    "devices": [
        {
            "url": "/dev/ttyACM0",
            "pages": {
                "1": {
                    "action_resolvers": {
                        "knob1": {
                            "name": "Spotify",
                            "type": "pulseaudio:Sink",
                            "sinkName": "spotify",
                        },
                        "key1": {
                            "name": "Previous",
                            "type": "spotify:PreviousSong",
                        },
                        "key2": {
                            "name": "Play/Pause",
                            "type": "spotify:PlayPauseToggle",
                        },
                        "key3": {
                            "name": "Next",
                            "type": "spotify:NextSong",
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
