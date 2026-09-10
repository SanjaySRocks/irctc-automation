from patchright.sync_api import sync_playwright

from utils.config_loader import load_config
from utils.validators import validate_journey

from pages.base_page import IRCTC_URL
from pages.journey_page import JourneyPage
from pages.login_page import LoginPage
from pages.train_page import TrainPage
from pages.passenger_page import PassengerPage
from pages.review_page import ReviewPage
from pages.payment_page import PaymentPage


def run():
    config = load_config("config")
    target_date = validate_journey(config.journey)

    print("Journey configuration validated")
    print("From:", config.journey.from_station)
    print("To:", config.journey.to_station)
    print("Quota:", config.journey.quota)
    print("Date:", target_date.strftime("%d/%m/%Y"))

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--start-maximized"],
        )

        page = browser.new_page(no_viewport=True)

        alert_dialog = page.locator(".ui-dialog").filter(
            has=page.locator(
                ".ui-dialog-title",
                has_text="Alert",
            )
        )

        def handle_alert():
            print("IRCTC Alert popup detected")
            alert_dialog.locator("button").filter(
                has_text="English"
            ).click()
            print("English button clicked")

        page.add_locator_handler(alert_dialog, handle_alert)

        page.goto(
            IRCTC_URL,
            wait_until="domcontentloaded",
        )
        print("IRCTC Train Search opened")

        try:
            JourneyPage(page).fill_and_search(config.journey)
            page.wait_for_timeout(1000)
            LoginPage(page).login(
                config.credentials.username,
                config.credentials.password,
            )
            page.wait_for_timeout(1000)

            booked = TrainPage(page).select_train_and_book(
                config.booking
            )
            if not booked:
                return

            page.wait_for_timeout(1000)
            PassengerPage(page).fill_passengers(
                config.passengers,
                auto_upgradation=config.booking.auto_upgradation,
                tatkal_confirm_birth_only=config.booking.tatkal_confirm_birth_only,
                payment_mode=config.payment.mode,
            )
            page.wait_for_timeout(1000)
            reviewed = ReviewPage(page).review_and_continue()
            if not reviewed:
                return

            page.wait_for_timeout(1000)
            PaymentPage(page).pay(config.payment)

        except Exception as error:
            print("\n❌ BOOKING FLOW FAILED")
            print("Error:", error)
            print("Current URL:", page.url)
            raise

        finally:
            page.wait_for_load_state("domcontentloaded")
            input("\nPress Enter to close browser...")
            browser.close()


if __name__ == "__main__":
    run()
