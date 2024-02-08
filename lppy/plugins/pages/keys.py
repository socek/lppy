from lppy.driver.action_resolvers import Button
from lppy.driver.consts import Commands


class ChosePageButton(Button):
    async def press(self):
        assert self.page
        assert self.page.device
        assert self.configuration
        device = self.page.device
        page = self.configuration.get("page", "1")
        self.page.device.current_page = page
        await self.page.device.refresh_button_color()

    async def unpress(self):
        assert self.page
        assert self.page.device
        await self.page.device.refresh_button_color()
