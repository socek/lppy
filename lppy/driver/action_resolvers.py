from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from lppy.driver.consts import DISPLAY_IMAGE_MODE


class ActionResolver:
    can_be_painted = False

    def __init__(self):
        self.page = None
        self.name = None
        self.configuration = None

    def setUp(self, page, name, configuration):
        self.page = page
        self.name = name
        self.configuration = configuration


class Button(ActionResolver):
    def press(self, payload):
        pass


class GraphicActionResolver(ActionResolver):
    can_be_painted = True

    def paint_image(self, image: Image) -> Image:
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("/usr/share/fonts/TTF/Consolas-Regular.ttf", 12)

        x, y, display_width, display_height = self._get_display_box()
        _, _, text_width, text_height = draw.textbbox((0, 0), self.configuration["name"], font=font)

        draw.text(((display_width-text_width)/2, (display_height-text_height)/2), self.configuration["name"], font=font, fill="white")

    def _get_display_box(self):
        display = self.page.device.subdisplays.get(self.name)
        if display:
            x, y, width, height = display["x"], display["y"], display["width"], display["height"]
        else:
            x, y = 0, 0
            width, height = self.page.device.width, self.page.device.height
        return x, y, width, height

    def draw_image(self):
        x, y, width, height = self._get_display_box()

        image = Image.new(DISPLAY_IMAGE_MODE, (width, height))
        self.paint_image(image)
        return image, (x, y, x + width, y + height)


class Knob(GraphicActionResolver):
    def press(self, payload):
        pass

    def rotate(self, payload):
        pass


class ScreenKey(GraphicActionResolver):
    def touch(self, payload):
        pass

    def touch_end(self, payload):
        pass
