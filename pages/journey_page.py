import re
from datetime import datetime
from .base_page import BasePage, IRCTCPage


class JourneyPage(BasePage):
    def fill_and_search(self, journey):
        from_station = self.page.locator(
            '[aria-controls="pr_id_1_list"]'
        )
        from_station.scroll_into_view_if_needed()
        from_station.fill(journey.from_station)
        from_station.press("Enter")

        journey_from_text = from_station.input_value().strip()
        print("From station selected:", journey_from_text)

        to_station = self.page.locator(
            '[aria-controls="pr_id_2_list"]'
        )
        to_station.scroll_into_view_if_needed()
        to_station.fill(journey.to_station)
        to_station.press("Enter")

        journey_to_text = to_station.input_value().strip()
        print("To station selected:", journey_to_text)

        if journey.quota == "TATKAL":
            quota_dropdown = self.page.locator("div.ui-dropdown").filter(
                has=self.page.locator('input[aria-label="GENERAL"]')
            )
            quota_dropdown.click()

            tatkal_option = self.page.locator(
                ".ui-dropdown-item"
            ).filter(
                has_text=re.compile("^TATKAL$")
            )
            tatkal_option.click()
            print("TATKAL selected")
        elif journey.quota == "GENERAL":
            print("GENERAL quota selected by default")

        target_date = datetime.strptime(
            journey.date,
            "%d/%m/%Y",
        ).date()

        date_input = self.page.locator(
            'input[autocomplete="off"].ui-inputtext'
        ).nth(2)
        date_input.click()

        date_picker = self.page.locator("div.ui-datepicker")

        while True:
            current_month = date_picker.locator(
                "span.ui-datepicker-month"
            ).inner_text()

            current_year = int(
                date_picker.locator(
                    "span.ui-datepicker-year"
                ).inner_text()
            )

            current_date = datetime.strptime(
                f"01 {current_month} {current_year}",
                "%d %B %Y",
            )

            if (
                current_date.month == target_date.month
                and current_date.year == target_date.year
            ):
                break

            if current_date.date() > target_date:
                date_picker.locator(
                    "a.ui-datepicker-prev"
                ).click()
            else:
                date_picker.locator(
                    "a.ui-datepicker-next"
                ).click()

        date_picker.locator(
            "td a.ui-state-default"
        ).filter(
            has_text=re.compile(f"^{target_date.day}$")
        ).click()

        print("Date selected:", target_date.strftime("%d/%m/%Y"))

        search_button = self.page.get_by_role(
            "button",
            name="Search Trains",
        )
        search_button.scroll_into_view_if_needed()
        search_button.click()
        self.wait_for_page(IRCTCPage.TRAIN_LIST)
        print("Search Trains clicked")
