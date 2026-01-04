from lppy.driver.plugin import LDPlugin
from lppy.plugins.runscript.keys import ExecSK


class RunScriptPlugin(LDPlugin):
    name = "runscript"

    def get_action_resolvers(self):
        return {
            "exec": ExecSK,
        }
