from .base_page import BasePage


class ReviewPage(BasePage):
    def review_and_continue(self):
        status_candidates = self.page.locator(
            "span.AVAILABLE, span.WL, span.RAC"
        )

        status_candidates.first.wait_for(
            state="attached",
            timeout=15000,
        )

        availability_status = None

        for i in range(status_candidates.count()):
            candidate = status_candidates.nth(i)

            if candidate.is_visible():
                availability_status = candidate
                break

        if availability_status is None:
            raise Exception(
                "Could not find visible seat availability status"
            )

        status_text = availability_status.inner_text().strip()
        status_class = (
            availability_status.get_attribute("class") or ""
        )

        print("Final seat status:", status_text)
        print("Status class:", status_class)

        if "AVAILABLE" in status_class.split():
            print("Seat is AVAILABLE. Proceeding...")

            final_continue = self.page.get_by_role(
                "button",
                name="Continue",
                exact=True,
            )
            final_continue.scroll_into_view_if_needed()

            final_continue.click()
            self.page.wait_for_url(
                "**/nget/payment/bkgPaymentOptions**",
                timeout=15000,
            )
            print("Final Continue clicked")
            return True

        print(f"Booking stopped. Seat status: {status_text}")
        return False
