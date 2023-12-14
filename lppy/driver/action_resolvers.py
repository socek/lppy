from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from lppy.driver.consts import DISPLAY_IMAGE_MODE


class ActionResolver:
    can_be_painted = False

    def __init__(self, device):
        self.device = device


class GraphicActionResolver(ActionResolver):
    can_be_painted = True

    def __init__(self, device, screen: str | None):
        self.device = device
        self.screen = screen

    def paint_image(self, image: Image) -> Image:
        Im = ImageDraw.Draw(image)
        mf = ImageFont.truetype("/usr/share/fonts/TTF/Consolas-Bold.ttf", 14)
        Im.text((10, 30), "Marilyn Monroe", fill="white", font=mf)
        Im.text((10, 50), "Marilyn Monroe", fill="yellow", font=mf)

    def draw_image(self):
        if self.screen:
            display = self.device.subdisplays[self.screen]
            x, y, width, height = display["x"], display["y"], display["width"], display["height"]
        else:
            x, y = 0, 0
            width, height = self.device.width, self.device.height
        image = Image.new(DISPLAY_IMAGE_MODE, (width, height))
        self.paint_image(image)
        return image, (x, y, x+width, y+height)


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
