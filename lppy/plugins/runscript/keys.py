from asyncio import create_subprocess_shell
from asyncio import create_task
from asyncio import sleep
from asyncio import subprocess

from lppy.driver.action_resolvers import ScreenKey


async def run(cmd):
    proc = await create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        # TODO: make better logging
        print(f"[{cmd!r} exited with {proc.returncode}]")
        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")


class ExecSK(ScreenKey):
    def __init__(self):
        super().__init__()
        self._task = None

    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        if self._task and not self._task.done():
            return
        self._task = create_task(run(self.configuration["cmd"]))
