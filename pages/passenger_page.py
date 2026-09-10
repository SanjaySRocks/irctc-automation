from .base_page import BasePage, IRCTCPage


class PassengerPage(BasePage):
    def fill_passengers(self, passengers, auto_upgradation=False, tatkal_book_only_if_confirm=False, payment_mode=1):
        for index, passenger in enumerate(passengers):
            if index > 0:
                self.page.get_by_text(
                    "+ Add Passenger",
                    exact=True,
                ).click()

            self.page.locator(
                'input[placeholder="Full Name as per Govt. ID"]'
            ).nth(index).fill(passenger["name"])

            self.page.locator(
                'input[formcontrolname="passengerAge"]'
            ).nth(index).fill(str(passenger["age"]))

            self.page.locator(
                'select[formcontrolname="passengerGender"]'
            ).nth(index).select_option(passenger["gender"])

            self.page.locator(
                'select[formcontrolname="passengerBerthChoice"]'
            ).nth(index).select_option(passenger["berth"])

            print(f"Passenger {index + 1} details entered")

        if auto_upgradation:
            auto_upgrade = self.page.locator(
                'label[for="autoUpgradation"]'
            )
            auto_upgrade.scroll_into_view_if_needed()
            auto_upgrade.click()
            print("Auto Upgradation selected")

        if tatkal_book_only_if_confirm:
            confirm_berths = self.page.locator('[for="confirmberths"]')
            
            if confirm_berths.is_visible(timeout=0):
                confirm_berths.scroll_into_view_if_needed()
                confirm_berths.click()
                print("Tatkal: Confirm Berths selected")
            else:
                print("Tatkal: Confirm Berths option not available")

        

        if payment_mode == 2:
            payment_option = self.page.locator(
                'p-radiobutton[id="2"] div[role="radio"]'
            )
            payment_option.scroll_into_view_if_needed()
            payment_option.click()
            print("Payment mode 2 selected - BHIM / UPI / USSD")
        else:
            print(
                "Payment mode 1 selected - "
                "debit/credit card / default"
            )

        self.page.wait_for_timeout(1000)

        continue_button = self.page.get_by_role(
            "button",
            name="Continue",
            exact=True,
        )
        continue_button.scroll_into_view_if_needed()

        continue_button.click()
        self.wait_for_page(IRCTCPage.REVIEW_BOOKING)
        print("Continue clicked")
