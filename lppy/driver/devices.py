from asyncio import StreamReader
from asyncio import StreamWriter
from asyncio import sleep
from asyncio import wait_for
from struct import pack
from struct import unpack

from PIL import Image
from serial_asyncio import open_serial_connection

from lppy.driver.action_resolvers import GraphicActionResolver
from lppy.driver.consts import DISPLAY_IMAGE_MODE
from lppy.driver.consts import Commands
from lppy.driver.page import Page

HANDSHAKE = b"""GET /index.html
HTTP/1.1
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Key: xaxiscelo

"""

HANDSHAKE_RESPONSE = b"""HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: EqLgCGt60oQVT7QwxrLOg5p16PA=\r
\r
"""


class LPDevice:
    timeout = 1
    retries = 2
    state = True
    display_mode = None

    def __init__(self):
        self.configuration = None
        self.conn_configuration = None
        self.reader: StreamReader = None
        self.writer: StreamWriter = None
        self.transaction_id = 0
        self.handlers = {
            Commands.BUTTON_PRESS: self.handle_button_press,
            Commands.KNOB_ROTATE: self.handle_knob_rotate,
            Commands.TOUCH: self.handle_touch,
            Commands.TOUCH_END: self.handle_touch_end,
            Commands.FRAMEBUFF: self._debug_print,
        }
        self.screen_buffers = {
            0: self._new_image(),
            1: self._new_image(),
        }
        self.current_buffer = 0
        self.pages = {}
        self.current_page = "1"

    def setUp(self, configuration: dict):
        self.configuration = configuration
        self.conn_configuration = {"baudrate": 256000, **self.configuration.get("connection", {})}
        for key, page_config in self.configuration["pages"].items():
            page = Page()
            page.setUp(self, page_config)
            self.pages[key] = page

    def _new_image(self):
        return Image.new(DISPLAY_IMAGE_MODE, (self.width, self.height), "black")

    async def repaint_buffer(self):
        self.current_buffer = (self.current_buffer + 1) % 2
        self.screen_buffers[self.current_buffer] = self._new_image()
        for resolver in self.pages[self.current_page].get_all_graphic_resolvers():
            image, box = resolver.draw_image()
            self.screen_buffers[self.current_buffer].paste(image, box)

        if (
            self.screen_buffers[self.current_buffer]
            == self.screen_buffers[(self.current_buffer + 1) % 2]
        ):
            return  # do not repaint the same image

        imageBuff = self.screen_buffers[self.current_buffer].convert(self.display_mode).tobytes()
        pixelCount = self.width * self.height * 2
        if len(imageBuff) != pixelCount:
            raise RuntimeError(f"Expected buffer length of {pixelCount}, got {len(imageBuff)}!")

        header = pack("!H", 0) + pack("!H", 0) + pack("!H", self.width) + pack("!H", self.height)
        await self.write_command(
            Commands.FRAMEBUFF, bytearray(self.display_id + header + imageBuff)
        )

    async def repaint_task(self):
        await self.repaint_buffer()
        while self.state:
            await sleep(0.1)
            await self.repaint_buffer()

    async def connect(self) -> bool:
        for _ in range(self.retries):  # trie for 2 times
            try:
                self.reader, self.writer = await wait_for(
                    open_serial_connection(
                        url=self.configuration["url"], **self.conn_configuration
                    ),
                    timeout=self.timeout,
                )
                self.writer.write(HANDSHAKE)
                await wait_for(self.writer.drain(), timeout=self.timeout)
                response = await wait_for(
                    self.reader.read(len(HANDSHAKE_RESPONSE)), timeout=self.timeout
                )
                return response == HANDSHAKE_RESPONSE
            except TimeoutError:
                print("Connection not responding, trying again...")
        return False

    async def write(
        self,
        buff,
    ):
        assert self.writer
        if len(buff) > 0xFF:
            prep = bytearray(0 for _ in range(14))
            prep[0] = 0x82
            prep[1] = 0xFF
            prep[6:10] = pack("!I", len(buff))

        else:
            prep = bytearray(0 for _ in range(6))
            prep[0] = 0x82
            prep[1] = 0x80 + len(buff)

        self.writer.write(prep)
        self.writer.write(buff)
        await wait_for(self.writer.drain(), timeout=self.timeout)

    def get_next_transaction_id(self):
        self.transaction_id += 1
        if self.transaction_id >= 256:
            self.transaction_id = 1
        return self.transaction_id

    async def write_command(self, command: Commands, payload: bytearray):
        transaction_id = self.get_next_transaction_id()
        buff = bytearray([0])
        buff.append(command.value)  # command
        buff.append(transaction_id)  # transaction id
        buff.extend(payload)
        buff[0] = min([0xFF, len(buff)])
        await self.write(buff)

    async def read(self):
        assert self.reader
        while self.state:
            try:
                result: bytearray = await wait_for(
                    self.reader.readexactly(3), timeout=self.timeout
                )
            except TimeoutError:
                continue
            assert result[0] == 130
            payloud_length = result[1] - 1
            payload = await wait_for(self.reader.read(payloud_length), timeout=self.timeout)
            self.handle_command(payload)

    def handle_command(self, payload):
        command = payload[0]
        self.handlers[Commands(command)](payload[1:])

    def get_subscreen_name(self, x_axis: int, y_axis: int) -> str | None:
        for name, display in self.subdisplays.items():
            after_x = x_axis >= display["x"]
            before_x_end = x_axis <= display["x"] + display["width"]
            after_y = y_axis >= display["y"]
            before_y_end = y_axis <= display["y"] + display["height"]
            if after_x and before_x_end and after_y and before_y_end:
                return name
        return None

    def handle_button_press(self, payload: bytearray):
        for byte in payload:
            ic(payload)

    def handle_knob_rotate(self, payload: bytearray):
        ic(payload)

    def handle_touch(self, payload: bytearray):
        x_axis = unpack("!H", payload[2:4])[0]
        y_axis = unpack("!H", payload[4:6])[0]
        subscreen_name = self.get_subscreen_name(x_axis, y_axis)
        ic(subscreen_name)

    def handle_touch_end(self, payload):
        ic(payload)

    def _debug_print(self, payload):
        ic(payload)


class LoupeDeckLive(LPDevice):
    display_id = b"\x00M"
    display_mode = "BGR;16"
    width = 480
    height = 270
    subdisplays = {
        "left": {
            "x": 5,
            "y": 0,
            "width": 52,
            "height": 265,
        },
        "right": {
            "x": 425,
            "y": 0,
            "width": 52,
            "height": 265,
        },
        "key1": {
            "x": 64,
            "y": 0,
            "width": 84,
            "height": 84,
        },
        "key2": {
            "x": 155,
            "y": 0,
            "width": 84,
            "height": 84,
        },
        "key3": {
            "x": 245,
            "y": 0,
            "width": 84,
            "height": 84,
        },
        "key4": {
            "x": 325,
            "y": 0,
            "width": 84,
            "height": 84,
        },
        "key5": {
            "x": 64,
            "y": 90,
            "width": 84,
            "height": 84,
        },
        "key6": {
            "x": 155,
            "y": 90,
            "width": 84,
            "height": 84,
        },
        "key7": {
            "x": 245,
            "y": 90,
            "width": 84,
            "height": 84,
        },
        "key8": {
            "x": 325,
            "y": 90,
            "width": 84,
            "height": 84,
        },
        "key9": {
            "x": 64,
            "y": 180,
            "width": 84,
            "height": 84,
        },
        "key10": {
            "x": 155,
            "y": 180,
            "width": 84,
            "height": 84,
        },
        "key11": {
            "x": 245,
            "y": 180,
            "width": 84,
            "height": 84,
        },
        "key12": {
            "x": 325,
            "y": 180,
            "width": 84,
            "height": 84,
        },
        "knob1": {
            "x": 0,
            "y": 0,
            "width": 64,
            "height": 90,
        },
    }
