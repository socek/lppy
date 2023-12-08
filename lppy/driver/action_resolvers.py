class ActionResolver:
    def __init__(self, device):
        self.device = device


class GraphicActionResolver(ActionResolver):
    def create_image(self):
        pass


class Knob(GraphicActionResolver):
    def press(self, payload):
        pass

    def rotate(self, payload):
        pass


class Key(GraphicActionResolver):
    def touch(self, payload):
        pass

    def touch_end(self, payload):
        pass


class Button:
    def press(self, payload):
        pass
