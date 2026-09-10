from patchright.sync_api import sync_playwright, TimeoutError
from datetime import datetime, timedelta
import re
import json
from utils import extract_station_name


# --------------------------------------------------
# LOAD CONFIG
# --------------------------------------------------

with open("config.json", "r") as file:
    config = json.load(file)

with open("credentials.json", "r") as file:
    credentials = json.load(file)

with open("passengers.json","r") as file:
    passengers = json.load(file)["passengers"]

from_station_name = config["from"]
to_station_name = config["to"]
quota = config["quota"].upper()
journey_date_string = config["date"]
train_number = config.get("train_number", "")
coach_type = config.get("coach_type", "")
auto_upgradation = config.get("auto_upgradation", False)
payment_mode = config.get("payment_mode", 1)

username = credentials.get("username", "")
password = credentials.get("password", "")

journey_to_text = None
journey_from_text = None
# --------------------------------------------------
# PARSE JOURNEY DATE
# --------------------------------------------------

target_date = datetime.strptime(
    journey_date_string,
    "%d/%m/%Y"
).date()


today = datetime.now().date()

tomorrow = today + timedelta(days=1)


# --------------------------------------------------
# VALIDATE QUOTA AND DATE
# --------------------------------------------------

if quota == "TATKAL":

    # Tatkal is only allowed for tomorrow
    if target_date != tomorrow:

        raise ValueError(
            "Date is out of Tatkal window"
        )


elif quota == "GENERAL":

    # General booking starts from tomorrow
    # Maximum 60 days from tomorrow
    last_allowed_date = today + timedelta(days=60)

    if (
        target_date < today
        or target_date > last_allowed_date
    ):

        raise ValueError(
            "Date is out of General booking window"
        )


else:

    raise ValueError(
        f"Invalid quota: {quota}. "
        "Only TATKAL and GENERAL are supported."
    )


print("Journey configuration validated")
print("From:", from_station_name)
print("To:", to_station_name)
print("Quota:", quota)
print(
    "Date:",
    target_date.strftime("%d/%m/%Y")
)

def wait_for_loader(page):

    loader = page.locator(
        "div.loading-bg"
    )

    try:

        # Give loader a chance to appear
        loader.wait_for(
            state="visible",
            timeout=2000
        )

        print("Loader appeared")

        # Wait until loading finishes
        loader.wait_for(
            state="hidden",
            timeout=30000
        )

        print("Loader disappeared")

    except TimeoutError:

        print(
            "Loader did not appear or loading completed quickly"
        )

# --------------------------------------------------
# CLICK WITH RETRY
# --------------------------------------------------

def click_with_retry(
    page,
    locator,
    expected_url=None,
    success_locator=None,
    max_retries=3,
    action_timeout=15000,
    retry_delay=2000
):

    last_error = None


    for attempt in range(1, max_retries + 1):

        try:

            print(
                f"\nClick attempt "
                f"{attempt}/{max_retries}"
            )


            # ------------------------------------------
            # CLICK
            # ------------------------------------------

            locator.wait_for(
                state="visible",
                timeout=action_timeout
            )

            locator.scroll_into_view_if_needed()

            locator.click()

            print("✓ Click executed")


            # ------------------------------------------
            # HANDLE LOADER
            # ------------------------------------------

            wait_for_loader(page)


            # ------------------------------------------
            # VERIFY URL
            # ------------------------------------------

            if expected_url:

                page.wait_for_url(
                    f"**{expected_url}**",
                    timeout=action_timeout
                )

                print(
                    f"✓ Expected URL reached: "
                    f"{expected_url}"
                )


            # ------------------------------------------
            # VERIFY SUCCESS ELEMENT
            # ------------------------------------------

            if success_locator:

                success_locator.wait_for(
                    state="visible",
                    timeout=action_timeout
                )

                print(
                    "✓ Expected element appeared"
                )


            print(
                f"✓ Action successful "
                f"on attempt {attempt}"
            )

            return


        except Exception as error:

            last_error = error

            print(
                f"❌ Attempt {attempt} failed"
            )

            print(
                f"Error: {error}"
            )

            print(
                f"Current URL: {page.url}"
            )


            if attempt < max_retries:

                print(
                    "🔄 Retrying click..."
                )

                page.wait_for_timeout(
                    retry_delay
                )

            else:

                print(
                    "❌ Maximum retries reached"
                )

                raise last_error
            
def login_step(page):
    # --------------------------------------------------
    # OPEN HAMBURGER MENU
    # --------------------------------------------------

    hamburger_menu = page.locator(
        "div.h_menu_drop_button:visible a:has(i.fa-align-justify)"
    )

    hamburger_menu.click()

    print("Hamburger menu opened")

    #Login
    login_button = page.locator(
        "button.search_btn"
    ).filter(
        has_text=re.compile("^LOGIN / REGISTER$")
    )

    login_button.click(
        timeout=15000
    )

    print("Login button clicked")

    page.wait_for_timeout(1000)

    # Username
    username_input = page.locator(
        'input[formcontrolname="userid"]'
    )

    username_input.fill(
        username
    )

    print("Username entered")


    # Password
    password_input = page.locator(
        'input[formcontrolname="password"]'
    )

    password_input.fill(
        password
    )

    print("Password entered")


    # Click SIGN IN
    page.get_by_role(
        "button",
        name="SIGN IN",
        exact=True
    ).click()

    print("Sign in clicked")

def fill_journey_details(page):
    # --------------------------------------------------
    # FROM STATION
    # --------------------------------------------------

    from_station = page.locator('[aria-controls="pr_id_1_list"]')
    from_station.scroll_into_view_if_needed()

    from_station.fill(
        from_station_name
    )

    page.get_by_role(
        "option"
    ).filter(
        has_text=from_station_name
    ).first.click()

    # Get selected full station text
    journey_from_text = from_station.input_value().strip()
    print("From station selected:", journey_from_text)


    # --------------------------------------------------
    # TO STATION
    # --------------------------------------------------

    to_station = page.locator('[aria-controls="pr_id_2_list"]')
    to_station.scroll_into_view_if_needed()

    to_station.fill(
        to_station_name
    )
    
    page.get_by_role(
        "option"
    ).filter(
        has_text=to_station_name
    ).first.click()

    # Get selected full station text
    journey_to_text = to_station.input_value().strip()
    print("To station selected:", journey_to_text)


    # --------------------------------------------------
    # QUOTA
    # --------------------------------------------------

    if quota == "TATKAL":

        quota_dropdown = page.locator(
            "div.ui-dropdown"
        ).filter(
            has=page.locator(
                'input[aria-label="GENERAL"]'
            )
        )

        quota_dropdown.click()

        print("Quota dropdown opened")


        # Select TATKAL
        tatkal_option = page.locator(
            ".ui-dropdown-item"
        ).filter(
            has_text=re.compile("^TATKAL$")
        )

        tatkal_option.click()

        print("TATKAL selected")


    elif quota == "GENERAL":

        # GENERAL is default quota
        # No need to open quota dropdown
        print("GENERAL quota selected by default")


    # --------------------------------------------------
    # DATE
    # --------------------------------------------------

    # Open date picker
    date_input = page.locator(
        'input[autocomplete="off"].ui-inputtext'
    ).nth(2)

    date_input.click()


    # Date picker container
    date_picker = page.locator(
        "div.ui-datepicker"
    )


    while True:

        # Read current month
        current_month = date_picker.locator(
            "span.ui-datepicker-month"
        ).inner_text()


        # Read current year
        current_year = int(
            date_picker.locator(
                "span.ui-datepicker-year"
            ).inner_text()
        )


        # Convert displayed month/year to datetime
        current_date = datetime.strptime(
            f"01 {current_month} {current_year}",
            "%d %B %Y"
        )


        # Check if target month and year matches
        if (
            current_date.month == target_date.month
            and current_date.year == target_date.year
        ):
            break


        # Current date is AFTER target → click LEFT
        elif current_date.date() > target_date:

            date_picker.locator(
                "a.ui-datepicker-prev"
            ).click()


        # Current date is BEFORE target → click RIGHT
        else:

            date_picker.locator(
                "a.ui-datepicker-next"
            ).click()


    # Select exact day after month/year matches
    date_picker.locator(
        "td a.ui-state-default"
    ).filter(
        has_text=re.compile(
            f"^{target_date.day}$"
        )
    ).click()


    print(
        "Date selected:",
        target_date.strftime("%d/%m/%Y")
    )


    # --------------------------------------------------
    # SEARCH TRAINS
    # --------------------------------------------------

    search_button = page.get_by_role(
        "button",
        name="Search Trains"
    )
    search_button.scroll_into_view_if_needed()
    search_button.click()
    
    print("Search Trains clicked")

def train_and_coach_selection(page):
    # Select train    
    train = page.locator(
        "app-train-avl-enq"
    ).filter(
        has_text=train_number
    )
    train.scroll_into_view_if_needed()
    
    # Train journey details
    train_start_raw = train.locator(
        "div.col-xs-5.hidden-xs"
    ).inner_text()

    train_to_raw = train.locator(
        "div.col-xs-7.hidden-xs span.pull-right"
    ).inner_text()

    train_start = extract_station_name(
        train_start_raw
    ).upper()

    train_to = extract_station_name(
        train_to_raw
    ).upper()
    
    # --------------------------------------------------
    # FIND COACH
    # --------------------------------------------------

    coach = train.locator(
        "div.pre-avl"
    ).filter(
        has_text=f"({coach_type})"
    )


    # --------------------------------------------------
    # AVAILABILITY CARDS
    # --------------------------------------------------

    availability_cards = train.locator(
        "td.link div.pre-avl"
    )

    first_availability = availability_cards.first


    # --------------------------------------------------
    # RETRY COACH CLICK UNTIL STATUS APPEARS
    # --------------------------------------------------

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
            f"Train {train_number} - "
            f"Coach {coach_type} clicked"
        )

        wait_for_loader(page)

        # Wait 1 second for availability to load
        page.wait_for_timeout(1000)

        try:

            # Check card exists
            if first_availability.count() == 0:

                print(
                    "Availability card not found yet"
                )

                continue

            # Check strong elements
            strong_elements = first_availability.locator(
                "strong"
            )

            strong_count = strong_elements.count()

            print(
                f"Strong elements found: "
                f"{strong_count}"
            )

            # Need at least:
            # 1. Date
            # 2. Availability status
            if strong_count < 2:

                print(
                    "Availability status not loaded yet"
                )

                continue

            availability_date = (
                strong_elements
                .nth(0)
                .inner_text()
                .strip()
            )

            availability_status = (
                strong_elements
                .nth(1)
                .inner_text()
                .strip()
            )

            # Make sure status actually has text
            if availability_status:

                print(
                    "Availability date:",
                    availability_date
                )

                print(
                    "Seat status:",
                    availability_status
                )

                print(
                    "✓ Availability loaded successfully"
                )

                break


        except Exception as error:

            print(
                f"Status not available yet: {error}"
            )


    # --------------------------------------------------
    # FAILED AFTER ALL RETRIES
    # --------------------------------------------------

    if not availability_status:

        raise Exception(
            f"Failed to load availability after "
            f"{max_retries} coach selection attempts"
        )

    page.wait_for_timeout(1000)
    # --------------------------------------------------
    # CLICK BOOK NOW ONLY IF AVAILABLE
    # --------------------------------------------------

    if "AVAILABLE" in availability_status:

        first_availability.click()

        book_now_button = train.get_by_role(
            "button",
            name="Book Now",
            exact=True
        )

        book_now_button.wait_for(
            state="visible",
            timeout=10000
        )

        book_now_button.click()

        print("Book Now clicked")
    else:
        print("Seat not available or waitlisted. Booking stopped.")

    
    # Check if Confirmation popup appears
    confirmation_title = page.locator(
        "span.ui-dialog-title"
    ).filter(
        has_text="Confirmation"
    )

    try:

        confirmation_title.wait_for(
            state="visible",
            timeout=2000
        )

        print("Confirmation popup detected")

        page.get_by_text(
            "Yes",
            exact=True
        ).click()

        print("Yes clicked")

    except TimeoutError:
        print("Confirmation popup did not appear")

def fill_passenger_details(page):
    
    for index, passenger in enumerate(passengers):

        # Add passenger fields for 2nd passenger onwards
        if index > 0:

            page.get_by_text(
                "+ Add Passenger",
                exact=True
            ).click()


        # Name
        page.locator(
            'input[placeholder="Full Name as per Govt. ID"]'
        ).nth(index).fill(
            passenger["name"]
        )


        # Age
        page.locator(
            'input[formcontrolname="passengerAge"]'
        ).nth(index).fill(
            str(passenger["age"])
        )


        # Gender
        page.locator(
            'select[formcontrolname="passengerGender"]'
        ).nth(index).select_option(
            passenger["gender"]
        )


        # Berth
        page.locator(
            'select[formcontrolname="passengerBerthChoice"]'
        ).nth(index).select_option(
            passenger["berth"]
        )


        print(
            f"Passenger {index + 1} details entered"
        )

    # --------------------------------------------------
    # AUTO UPGRADATION
    # --------------------------------------------------

    if auto_upgradation:
        auto_upgrade = page.locator(
            'label[for="autoUpgradation"]'
        )

        auto_upgrade.scroll_into_view_if_needed()

        auto_upgrade.click()

        print("Auto Upgradation selected")


    # --------------------------------------------------
    # PAYMENT MODE
    # --------------------------------------------------

    if payment_mode == 2:

        payment_option = page.locator(
            'p-radiobutton[id="2"] div[role="radio"]'
        )

        payment_option.scroll_into_view_if_needed()

        payment_option.click()

        print("Payment mode 2 selected - BHIM / UPI / USSD")

    else:
        print("Payment mode 1 selected - debit/credit card / default")

    page.wait_for_timeout(1000)

    # --------------------------------------------------
    # CONTINUE
    # --------------------------------------------------

    continue_button = page.get_by_role(
        "button",
        name="Continue",
        exact=True
    )

    continue_button.scroll_into_view_if_needed()

    #continue_button.click()
    click_with_retry(page, continue_button, expected_url="/nget/booking/reviewBooking")

    print("Continue clicked")

def review_booking_details(page):
    status_candidates = page.locator(
        "span.AVAILABLE, span.WL, span.RAC"
    )

    status_candidates.first.wait_for(
        state="attached",
        timeout=15000
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
        availability_status.get_attribute("class")
        or ""
    )

    print("Final seat status:", status_text)
    print("Status class:", status_class)

    if "AVAILABLE" in status_class.split():

        print("Seat is AVAILABLE. Proceeding...")

        final_continue = page.get_by_role(
            "button",
            name="Continue",
            exact=True
        )

        final_continue.scroll_into_view_if_needed()

        #final_continue.click()
        click_with_retry(page, final_continue, expected_url="/nget/payment/bkgPaymentOptions")

        print("Final Continue clicked")

    else:

        print(
            f"Booking stopped. Seat status: {status_text}"
        )

def print_payment_method_list(page):
    payment_methods = page.locator(
        "div.bank-type"
    )

    visible_payment_methods = []

    for i in range(payment_methods.count()):

        payment_method = payment_methods.nth(i)

        if payment_method.is_visible():

            payment_text = payment_method.inner_text().strip()

            visible_payment_methods.append(
                payment_method
            )

            print(
                f"{len(visible_payment_methods)}: {payment_text}"
            )

def print_payment_vendors_list(page):
    payment_vendors = page.locator(
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

            # Get vendor name
            vendor_name = vendor_card.locator(
                "div.bank-text > span.col-pad"
            ).evaluate(
                "(element) => element.childNodes[0].textContent.trim()"
            )

            if vendor_name:

                visible_vendors.append(
                    vendor_card
                )

                print(
                    f"{len(visible_vendors)}: "
                    f"{vendor_name}"
                )


def payment_step(page):
    
    page.wait_for_timeout(2000)

    if payment_mode == 2:

        # Print all available methods
        payment_options = {
            1: "IRCTC iPay (Credit Card/Debit Card/UPI)",
            2: "Multiple Payment Service",
            3: "BHIM/ UPI/ USSD"
        }

        payment_text = payment_options.get(3)

        if not payment_text:
            raise ValueError(
                f"Invalid payment mode: {payment_mode}"
            )

        payment_option = page.locator(
            "div.bank-type"
        ).filter(
            has_text=payment_text
        )

        payment_option.wait_for(
            state="visible",
            timeout=15000
        )

        payment_option.scroll_into_view_if_needed()

        payment_option.click()

        print(
            f"Payment option selected: {payment_text}"
        )

        page.wait_for_timeout(1500)

        # PAYMENT VENDOR SELECTION
        payment_vendor_options = {
            1: "Amazon Pay",
            2: "Paytm UPI"
        }

        selected_vendor_name = payment_vendor_options.get(2)

        payment_vendors = page.locator(
            "div.border-all.link.no-pad"
        )
        vendor_count = payment_vendors.count()

        selected_vendor = None

        for i in range(vendor_count):

            vendor_card = payment_vendors.nth(i)

            if vendor_card.is_visible():

                vendor_name = vendor_card.locator(
                    "div.bank-text > span.col-pad"
                ).evaluate(
                    "(element) => element.childNodes[0].textContent.trim()"
                )

                if vendor_name:

                    print(
                        f"Found vendor: {vendor_name}"
                    )


                    # Exact case-insensitive comparison
                    if (
                        vendor_name.strip().upper()
                        ==
                        selected_vendor_name.strip().upper()
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



    page.wait_for_timeout(2500)


    

    # ----------------------------------------
    # CLICK PAY & BOOK
    # ----------------------------------------

    pay_and_book = page.get_by_role(
        "button",
        name="Pay & Book",
        exact=True
    )

    pay_and_book.wait_for(
        state="visible",
        timeout=15000
    )

    pay_and_book.scroll_into_view_if_needed()

    print("\nClicking Pay & Book...")
    print("Current URL before click:")
    print(page.url)

    pay_and_book.click()

    print("✓ Pay & Book clicked")


    # ----------------------------------------
    # WAIT AND MONITOR REDIRECT
    # ----------------------------------------

    print("\nWaiting for payment redirect...")

    page.wait_for_timeout(10000)

    

# --------------------------------------------------
# PLAYWRIGHT
# --------------------------------------------------

with sync_playwright() as p:

    browser = p.chromium.launch(
        channel="chrome",
        headless=False,
        args=["--start-maximized"]
    )

    page = browser.new_page(
        no_viewport=True
    )

    # Language Popup 
    alert_dialog = page.locator(
        ".ui-dialog"
    ).filter(
        has=page.locator(
            ".ui-dialog-title",
            has_text="Alert"
        )
    )


    def handle_alert():

        print("IRCTC Alert popup detected")

        alert_dialog.locator(
            "button"
        ).filter(
            has_text=re.compile("^English$")
        ).click()

        print("English button clicked")


    page.add_locator_handler(
        alert_dialog,
        handle_alert
    )

    # Open IRCTC Train Search
    page.goto(
        "https://www.irctc.co.in/nget/train-search",
        wait_until="domcontentloaded"
    )

    print("IRCTC Train Search opened")

    try:
        fill_journey_details(page)

        page.wait_for_timeout(1000)

        login_step(page)

        page.wait_for_timeout(1000)

        train_and_coach_selection(page)

        page.wait_for_timeout(1000)

        fill_passenger_details(page)

        page.wait_for_timeout(1000)

        review_booking_details(page)

        payment_step(page)

    except Exception as error:
        print("\n❌ BOOKING FLOW FAILED")
        print("Error:", error)
        print("Current URL:", page.url)

    # Wait for results
    page.wait_for_load_state(
        "domcontentloaded"
    )
    

    input("\nPress Enter to close browser...")

    browser.close()