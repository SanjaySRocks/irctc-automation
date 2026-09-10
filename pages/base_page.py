from enum import Enum

from patchright.sync_api import TimeoutError


IRCTC_URL = "https://www.irctc.co.in"


class IRCTCPage(Enum):
    JOURNEY_DETAILS = "/nget/train-search"
    TRAIN_LIST = "/nget/booking/train-list"
    PASSENGER_DETAILS = "/nget/booking/psgninput"
    REVIEW_BOOKING = "/nget/booking/reviewBooking"
    PAYMENT_OPTIONS = "/nget/payment/bkgPaymentOptions"


class BasePage:
    LOADER_SELECTOR = "div.loading-bg"
    PAGE_NAVIGATION_TIMEOUT = 60000

    def __init__(self, page):
        self.page = page

    def wait_for_loader(self):
        loader = self.page.locator(self.LOADER_SELECTOR)

        try:
            loader.wait_for(state="visible", timeout=2000)
            print("Loader appeared")

            loader.wait_for(
                state="hidden",
                timeout=30000,
            )

            print("Loader disappeared")

        except TimeoutError:
            print("Loader did not appear or loading completed quickly")

    def wait_for_page(
        self,
        expected_page: IRCTCPage,
        timeout: int = PAGE_NAVIGATION_TIMEOUT,
    ):
        self.page.wait_for_url(
            f"**{expected_page.value}**",
            timeout=timeout,
        )

        print(f"Page loaded: {expected_page.name}")
