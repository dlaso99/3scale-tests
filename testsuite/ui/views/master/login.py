""" Representation of Login specific MASTER views"""
from widgetastic.widget import View, Text

from testsuite.ui.navigation import Navigable
from testsuite.ui.views.admin.login import LoginWidget


class MasterLoginView(View, Navigable):
    """
    Basic login view page object that can be found on path
    """
    path = '/p/login'
    ROOT = "/html//div[@id='pf-login-page-container']"
    header = Text("//main/header/h2")
    error_message = Text("//p[@class='pf-c-form__helper-text pf-m-error']")
    login_widget = View.nested(LoginWidget)
    password_reset_link = Text("//a[@href='/p/password/reset']")

    def do_login(self, name, password):
        """
        Method handle login to 3scale admin portal
        :param name: User username for login
        :param password: User password for login
        :return DashboardView page object
        """
        self.login_widget.do_login(name, password)

    @property
    def is_displayed(self):
        return self.password_reset_link.is_displayed and self.path in self.browser.url and \
               self.browser.title == '3scale Login' and 'Log in to your account' in self.header.text and \
               self.login_widget.is_displayed
