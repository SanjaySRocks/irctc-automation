from .base_page import BasePage
from utils.station_utils import extract_station_name


class TrainPage(BasePage):
    def select_train_and_book(self, booking):
        train = self.page.locator("app-train-avl-enq").filter(
            has_text=booking.train_number
        )
        train.scroll_into_view_if_needed()

        train_start_raw = train.locator(
            "div.col-xs-5.hidden-xs"
        ).inner_text()
        train_to_raw = train.locator(
            "div.col-xs-7.hidden-xs span.pull-right"
        ).inner_text()

        train_start = extract_station_name(train_start_raw).upper()
        train_to = extract_station_name(train_to_raw).upper()

        print("Train route:", train_start, "->", train_to)

        coach = train.locator("div.pre-avl").filter(
            has_text=f"({booking.coach_type})"
        )

        availability_cards = train.locator("td.link div.pre-avl")
        first_availability = availability_cards.first

        max_retries = 30
        availability_status = None

        for attempt in range(1, max_retries + 1):
            print(
                f"Coach selection attempt "
                f"{attempt}/{max_retries}"
            )

            coach.scroll_into_view_if_needed()
            coach.click()

            print(
                f"Train {booking.train_number} - "
                f"Coach {booking.coach_type} clicked"
            )

            self.wait_for_loader()
            self.page.wait_for_timeout(1000)

            try:
                if first_availability.count() == 0:
                    print("Availability card not found yet")
                    continue

                strong_elements = first_availability.locator("strong")
                strong_count = strong_elements.count()

                print(f"Strong elements found: {strong_count}")

                if strong_count < 2:
                    print("Availability status not loaded yet")
                    continue

                availability_date = (
                    strong_elements.nth(0).inner_text().strip()
                )
                availability_status = (
                    strong_elements.nth(1).inner_text().strip()
                )

                if availability_status:
                    print("Availability date:", availability_date)
                    print("Seat status:", availability_status)
                    print("✓ Availability loaded successfully")
                    break

            except Exception as error:
                print(f"Status not available yet: {error}")

        if not availability_status:
            raise Exception(
                f"Failed to load availability after "
                f"{max_retries} coach selection attempts"
            )

        self.page.wait_for_timeout(1000)

        if "AVAILABLE" in availability_status:
            first_availability.click()

            book_now_button = train.get_by_role(
                "button",
                name="Book Now",
                exact=True,
            )
            book_now_button.wait_for(
                state="visible",
                timeout=10000,
            )
            book_now_button.click()
            print("Book Now clicked")
        else:
            print("Seat not available or waitlisted. Booking stopped.")
            return False

        confirmation_title = self.page.locator(
            "span.ui-dialog-title"
        ).filter(
            has_text="Confirmation"
        )

        try:
            confirmation_title.wait_for(
                state="visible",
                timeout=2000,
            )
            print("Confirmation popup detected")

            self.page.get_by_text(
                "Yes",
                exact=True,
            ).click()
            print("Yes clicked")
        except Exception:
            print("Confirmation popup did not appear")

        return True
