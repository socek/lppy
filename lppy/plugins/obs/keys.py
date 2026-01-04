from lppy.driver.action_resolvers import ScreenKey
from lppy.plugins.obs.models import ObsConnection


class SetScene(ScreenKey):
    async def touch(self, x_axis: int, y_axis: int):
        await super().touch(x_axis, y_axis)
        assert self.configuration
        scene_name = self.configuration.get("scene", "")
        ObsConnection.set_scene(scene_name)


    def get_paint_configuration(self):
        conf = super().get_paint_configuration()
        assert self.configuration
        if not ObsConnection.validate_connection():
            conf["background"] = "grey"
            return conf
        if ObsConnection.get_scene() == self.configuration.get("scene", ""):
            conf["background"] = "green"

        return conf
