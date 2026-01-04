from asyncio import sleep
from asyncio import wait_for
from struct import pack

from serial.serialutil import SerialException

from lppy.driver.consts import Commands
from lppy.driver.devices import LPDevice


async def repaint_task(device: LPDevice):
    await device.repaint_buffer()
    while device.state:
        await sleep(0.1)
        try:
            await device.repaint_buffer()
        except SerialException:
            device.state = False
            break


async def communicate(device: LPDevice):
    assert device.reader
    while device.state:
        try:
            result: bytearray = await wait_for(
                device.reader.readexactly(3), timeout=device.timeout
            )
        except TimeoutError:
            continue
        except SerialException:
            device.state = False
            break
        assert result[0] == 130
        payloud_length = result[1] - 1
        payload = await wait_for(device.reader.read(payloud_length), timeout=device.timeout)
        await device.handle_command(payload)
    try:
        await device.paint_image(device._new_image())
        brightness = pack("B", 0)
        await device.write_command(Commands.SET_BRIGHTNESS, bytearray(brightness))
        await sleep(0.1)
    except SerialException:
        pass
