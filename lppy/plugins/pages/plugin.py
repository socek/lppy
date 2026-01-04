from lppy.driver.plugin import LDPlugin
from lppy.plugins.pages.keys import ChosePageButton


class PagePlugin(LDPlugin):
    name = "page"

    def get_action_resolvers(self):
        return {
            "choose": ChosePageButton,
        }
