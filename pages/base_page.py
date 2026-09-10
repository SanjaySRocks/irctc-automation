from patchright.sync_api import TimeoutError


class BasePage:
    LOADER_SELECTOR = "div.loading-bg"

    def __init__(self, page):
        self.page = page

    def wait_for_loader(self):
        loader = self.page.locator(self.LOADER_SELECTOR)

        try:
            loader.wait_for(state="visible", timeout=2000)
            print("Loader appeared")
            loader.wait_for(state="hidden", timeout=30000)
            print("Loader disappeared")
        except TimeoutError:
            print("Loader did not appear or loading completed quickly")