from icecream import ic
from icecream import install

from lppy.daemon.app import Application

install()
ic.configureOutput(includeContext=True)


if __name__ == "__main__":
    app = Application()
    app.main()
