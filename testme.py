from asyncio import TaskGroup
from asyncio import ensure_future
from asyncio import get_event_loop
from asyncio import sleep
from signal import SIGINT
from signal import SIGTERM
from signal import signal

from icecream import ic
from icecream import install

from lppy.daemon.app import Application
from lppy.driver.configuration import Configuration
from lppy.driver.devices import LoupeDeckLive

install()
ic.configureOutput(includeContext=True)


async def main():
    app = Application()
    for signalCode in [SIGINT, SIGTERM]:
        signal(signalCode, app.exit_application)

    await app.init()

    async with TaskGroup() as tg:
        while app.state:
            async for task in app.start_devices_tasks():
                tg.create_task(task)
            await sleep(1)



if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(ensure_future(main()))
