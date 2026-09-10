from .base_page import BasePage


class PaymentPage(BasePage):
    PAYMENT_OPTIONS = {
        1: "IRCTC iPay (Credit Card/Debit Card/UPI)",
        2: "Multiple Payment Service",
        3: "BHIM/ UPI/ USSD",
    }

    def print_payment_method_list(self):
        payment_methods = self.page.locator("div.bank-type")

        visible_payment_methods = []

        for i in range(payment_methods.count()):
            payment_method = payment_methods.nth(i)

            if payment_method.is_visible():
                payment_text = payment_method.inner_text().strip()
                visible_payment_methods.append(payment_method)
                print(
                    f"{len(visible_payment_methods)}: "
                    f"{payment_text}"
                )

    def print_payment_vendors_list(self):
        payment_vendors = self.page.locator(
            "div.border-all.link.no-pad"
        )

        vendor_count = payment_vendors.count()
        print(
            f"\nPayment gateway vendors found: "
            f"{vendor_count}"
        )

        visible_vendors = []

        for i in range(vendor_count):
            vendor_card = payment_vendors.nth(i)

            if vendor_card.is_visible():
                vendor_name = vendor_card.locator(
                    "div.bank-text > span.col-pad"
                ).evaluate(
                    "(element) => element.childNodes[0].textContent.trim()"
                )

                if vendor_name:
                    visible_vendors.append(vendor_card)
                    print(
                        f"{len(visible_vendors)}: "
                        f"{vendor_name}"
                    )

    def pay(self, payment):
        self.page.wait_for_timeout(2000)

        if payment.mode == 2:
            payment_text = self.PAYMENT_OPTIONS.get(3)

            if not payment_text:
                raise ValueError(
                    f"Invalid payment mode: {payment.mode}"
                )

            payment_option = self.page.locator(
                "div.bank-type"
            ).filter(
                has_text=payment_text
            )

            payment_option.wait_for(
                state="visible",
                timeout=15000,
            )
            payment_option.scroll_into_view_if_needed()
            payment_option.click()

            print(
                f"Payment option selected: {payment_text}"
            )

            self.page.wait_for_timeout(1500)

            selected_vendor_name = payment.vendor

            payment_vendors = self.page.locator(
                "div.border-all.link.no-pad"
            )

            selected_vendor = None

            for i in range(payment_vendors.count()):
                vendor_card = payment_vendors.nth(i)

                if vendor_card.is_visible():
                    vendor_name = vendor_card.locator(
                        "div.bank-text > span.col-pad"
                    ).evaluate(
                        "(element) => element.childNodes[0].textContent.trim()"
                    )

                    if vendor_name:
                        print(f"Found vendor: {vendor_name}")

                        if (
                            vendor_name.strip().upper()
                            == selected_vendor_name.strip().upper()
                        ):
                            selected_vendor = vendor_card
                            print(
                                f"✓ Matching vendor found: "
                                f"{vendor_name}"
                            )
                            break

            if selected_vendor is None:
                raise Exception(
                    f"Payment vendor not available: "
                    f"{selected_vendor_name}"
                )

            selected_vendor.scroll_into_view_if_needed()
            selected_vendor.click()

            print(
                f"✓ Payment vendor selected: "
                f"{selected_vendor_name}"
            )

        self.page.wait_for_timeout(2500)

        pay_and_book = self.page.get_by_role(
            "button",
            name="Pay & Book",
            exact=True,
        )
        pay_and_book.wait_for(
            state="visible",
            timeout=15000,
        )
        pay_and_book.scroll_into_view_if_needed()

        print("\nClicking Pay & Book...")
        print("Current URL before click:")
        print(self.page.url)

        pay_and_book.click()
        print("✓ Pay & Book clicked")

        print("\nWaiting for payment redirect...")
        self.page.wait_for_timeout(10000)
