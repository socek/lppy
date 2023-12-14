from asyncio import TaskGroup
from asyncio import ensure_future
from asyncio import get_event_loop
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

devices = []


async def main():
    app = Application()
    for signalCode in [SIGINT, SIGTERM]:
        signal(signalCode, app.exit_application)

    async with TaskGroup() as tg:
        for task in await app.init():
            tg.create_task(task)


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(ensure_future(main()))
