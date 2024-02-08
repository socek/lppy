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
        self.name: str | None = None
        self.configuration = None

    def setUp(self, page, name, configuration):
        self.page = page
        self.name = name
        self.configuration = configuration


class Button(ActionResolver):
    def get_active_color(self):
        return [0, 102, 255]

    def get_inactive_color(self):
        return [255, 102, 0]

    def get_color(self):
        assert self.page
        assert self.page.device
        assert self.name
        page_number = self.name[6:]
        if page_number == self.page.device.current_page:
            return self.get_active_color()
        else:
            return self.get_inactive_color()

    def get_index(self):
        assert self.page
        assert self.page.device
        inv_map = {v: k for k, v in self.page.device.button_indexes.items()}
        return inv_map[self.name]

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
        ...

    async def unpress(self):
        ...

    async def rotate(self, right: bool):
        ...


class CircleKnob(Knob):
    def get_paint_configuration(self):
        return {
            "draw_circle": True,
            "percentage": 75,
            "first_circle": 75,
            "second_circle": 50,
            "background": "black",
        }

    def paint_image(self, image: Image) -> Image:
        assert self.configuration
        conf = self.get_paint_configuration()
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("/usr/share/fonts/TTF/Consolas-Regular.ttf", 12)
        x, y, width, height = self._get_display_box()
        margin = 10
        stroke_width = int(width / 2) - margin
        shape_size = int(min(width, height) * 0.8)

        shape = [(margin, margin), (shape_size, shape_size)]

        if conf.get("backbox_color"):
            backbox_shape = [(0, 0), (shape_size + margin, shape_size + margin)]
            draw.rectangle(backbox_shape, fill=conf.get("backbox_color"))

        if conf["draw_circle"]:
            start = 270
            draw.arc(shape, start=0, end=360, fill="blue", width=stroke_width)
            draw.arc(
                shape,
                start=start,
                end=start + (360 * conf["first_circle"] / 100),
                fill="green",
                width=stroke_width,
            )
            if conf.get("second_circle"):
                draw.arc(
                    shape,
                    start=start,
                    end=start + (360 * conf["second_circle"] / 100),
                    fill="red",
                    width=stroke_width,
                )
        texts = [
            self.configuration["name"],
            f"{conf['percentage']}",
        ]
        if isinstance(conf["percentage"], int):
            texts[1] += "%"

        if conf.get("additional_text"):
            texts.append(conf.get("additional_text"))

        text = "\n".join(texts)
        _, _, text_width, text_height = draw.textbbox((0, 0), text, font=font)

        draw.text(
            ((width - text_width) / 2, ((height - text_height) / 2) - 15),
            text,
            font=font,
            fill="white",
            align="center",
        )

    async def touch(self, x_axis: int, y_axis: int):
        pass

    async def touch_end(self, x_axis: int, y_axis: int):
        pass


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
