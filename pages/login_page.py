import re
from .base_page import BasePage


class LoginPage(BasePage):
    def login(self, username: str, password: str):
        hamburger_menu = self.page.locator(
            "div.h_menu_drop_button:visible a:has(i.fa-align-justify)"
        )
        hamburger_menu.click()
        print("Hamburger menu opened")

        login_button = self.page.locator("button.search_btn").filter(
            has_text=re.compile("^LOGIN / REGISTER$")
        )
        login_button.click(timeout=15000)
        print("Login button clicked")

        self.page.wait_for_timeout(1000)

        username_input = self.page.locator(
            'input[formcontrolname="userid"]'
        )
        username_input.fill(username)
        print("Username entered")

        password_input = self.page.locator(
            'input[formcontrolname="password"]'
        )
        password_input.fill(password)
        print("Password entered")

        self.page.get_by_role(
            "button",
            name="SIGN IN",
            exact=True,
        ).click()
        print("Sign in clicked")
