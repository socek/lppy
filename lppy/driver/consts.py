from enum import Enum

DISPLAY_IMAGE_MODE = "RGB"


class Commands(Enum):
    BUTTON_PRESS = 0x00
    KNOB_ROTATE = 0x01
    SET_COLOR = 0x02
    SERIAL = 0x03
    RESET = 0x06
    VERSION = 0x07
    SET_BRIGHTNESS = 0x09
    FRAMEBUFF = 0x10
    SET_VIBRATION = 0x1B
    MCU = 0x0D
    DRAW = 0x0F
    TOUCH = 0x4D
    TOUCH_CT = 0x52
    TOUCH_END = 0x6D
    TOUCH_END_CT = 0x72
