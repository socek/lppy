from datetime import datetime
from datetime import timedelta

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
    async def press(self):
        ic("press", self.name)

    async def unpress(self):
        ic("unpress", self.name)


class GraphicActionResolver(ActionResolver):
    can_be_painted = True

    def get_paint_configuration(self):
        return {
            "background": "black",
        }

    def paint_image(self, image: Image) -> Image:
        assert self.configuration
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("/usr/share/fonts/TTF/Consolas-Regular.ttf", 12)

        x, y, display_width, display_height = self._get_display_box()
        _, _, text_width, text_height = draw.textbbox(
            (0, 0), self.configuration["name"], font=font
        )

        draw.text(
            ((display_width - text_width) / 2, (display_height - text_height) / 2),
            self.configuration["name"],
            font=font,
            fill="white",
        )

    def _get_display_box(self):
        assert self.page
        display = self.page.device.subdisplays.get(self.name)
        if display:
            x, y, width, height = display["x"], display["y"], display["width"], display["height"]
        else:
            x, y = 0, 0
            width, height = self.page.device.width, self.page.device.height
        return x, y, width, height

    def draw_image(self):
        conf = self.get_paint_configuration()
        x, y, width, height = self._get_display_box()

        image = Image.new(DISPLAY_IMAGE_MODE, (width, height), color=conf["background"])
        self.paint_image(image)
        return image, (x, y, x + width, y + height)


class Knob(GraphicActionResolver):
    async def press(self):
        ic("press", self.name)

    async def unpress(self):
        ic("unpress", self.name)

    async def rotate(self, right: bool):
        ic("rotate", self.name, right)


class ScreenKey(GraphicActionResolver):
    HOVER_TIMOUT = 0.1

    def __init__(self):
        super().__init__()
        self.last_touch = None
        self.last_touch_end = None

    def get_paint_configuration(self):
        first_touch = self.last_touch and self.last_touch_end is None
        touching = (
            self.last_touch and self.last_touch_end and self.last_touch > self.last_touch_end
        )
        cooldown = self.last_touch_end and self.last_touch_end > datetime.utcnow() - timedelta(
            seconds=self.HOVER_TIMOUT
        )
        if first_touch or touching or cooldown:
            return {
                "background": "blue",
            }
        return {
            "background": "black",
        }

    async def touch(self, x_axis: int, y_axis: int):
        self.last_touch = datetime.utcnow()

    async def touch_end(self, x_axis: int, y_axis: int):
        self.last_touch_end = datetime.utcnow()
