from icecream import ic
from icecream import install

from lppy.globals import app

install()
ic.configureOutput(includeContext=True)


if __name__ == "__main__":
     app.main()
