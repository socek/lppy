from asyncio import timeout

from serial_asyncio import open_serial_connection

HANDSHAKE = b"""GET /index.html
HTTP/1.1
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Key: xaxiscelo

"""

HANDSHAKE_RESPONSE = b"""HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accep"""


class LPConnection:
    configuration = {
        "baudrate": 256000,
    }
    timeout = 1

    def __init__(self):
        self.reader = None
        self.writer = None
        self.path = None

    async def start(self, path: str) -> bool:
        for _ in range(2):  # trie for 2 times
            try:
                async with timeout(self.timeout):
                    self.reader, self.writer = await open_serial_connection(
                        url=path, **self.configuration
                    )
                    self.writer.write(HANDSHAKE)
                    await self.writer.drain()
                    response = await self.reader.read(len(HANDSHAKE))
                    return response == HANDSHAKE_RESPONSE
            except TimeoutError:
                print("Connection not responding, trying again...")
        return False

        # while True:
        #     line = ser.read(130)
        #     if line == b"":
        #         print("Reconnecting...")
        #         ser = Serial(PATH, baudrate=256000, timeout=1)
        #         ser.write(HANDSHAKE)
        #         line = ser.read(130)
        #     if (
        #         line
        #         == b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: ALtlZo9FMEUEQleXJmq++ukUQ1s=\r\n\r\n"
        #     ):
        #         break
