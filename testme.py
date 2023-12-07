from asyncio import ensure_future
from asyncio import get_event_loop
from signal import SIGINT
from signal import SIGTERM
from signal import signal

from icecream import ic
from icecream import install
from lppy.driver.devices import LoupeDeckLive

install()
ic.configureOutput(includeContext=True)

PATH = "/dev/ttyACM0"

lp = LoupeDeckLive()


async def main():
    await lp.connect(PATH)
    print("Connected")
    await lp.read()
    return True


def stopMe(*args, **kwargs):
    print("\rExiting...")
    lp.state = False


if __name__ == "__main__":
    loop = get_event_loop()
    for signalCode in [SIGINT, SIGTERM]:
        signal(signalCode, stopMe)
    main_task = ensure_future(main())
    loop.run_until_complete(main_task)
