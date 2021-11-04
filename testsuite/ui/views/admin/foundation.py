"""
Module contains Base View used for all Admin Views. This View is further extended by: Dashboard, Audience,
Product, Backend, and AccountSettings Views. All of them creates basic page structure for respective
Admin portal pages.
:TODO Add locators/menus for basic pages
"""

from widgetastic.widget import GenericLocatorWidget, View, Text
from widgetastic_patternfly4 import Button

from testsuite.ui.navigation import step, Navigable
from testsuite.ui.widgets import ContextMenu


class BaseAdminView(View, Navigable):
    """
    Basic representation of logged in admin portal page.
    All admin portal page should inherits from this class.
    """
    path_pattern = ''
    explorer_menu = Text("//div[@id='api_selector']//a[@title='Context Selector']/span")
    threescale_menu_logo = GenericLocatorWidget('//*[@id="user_widget"]/a/div')
    support_link = Text("//a[@href='//access.redhat.com/products/red-hat-3scale#support']")
    user_session = GenericLocatorWidget("//a[@href='#session-menu']")
    user_logout_link = Text("//a[@href='/p/logout']")
    threescale_version = Text("//*[contains(@class,'powered-by-3scale')]/span")

    context_menu = ContextMenu()

    def __init__(self, parent, logger=None, **kwargs):
        super().__init__(parent, logger=logger, **kwargs)
        self.path = self.path_pattern.format_map(kwargs)

    def logout(self):
        """Method which logouts current user from admin portal"""
        self.user_session.click()
        self.user_logout_link.click()

    @step("BaseAudienceView")
    def audience(self):
        """Selects Audience item from ContextSelector"""
        self.context_menu.item_select("Audience")

    @step("ProductsView")
    def products(self):
        """Selects Products item from ContextSelector"""
        self.context_menu.item_select("Products")

    @step("BackendsView")
    def backends(self):
        """Selects Backends item from ContextSelector"""
        self.context_menu.item_select("Backends")

    @step("BaseSettingsView")
    def settings(self):
        """Select Account Settings from ContextSelector"""
        self.context_menu.item_select("Account Settings")

    @step("DashboardView")
    def dashboard(self):
        """Select Dashboard from ContextSelector"""
        self.context_menu.item_select("Dashboard")

    @property
    def is_displayed(self):
        return self.threescale_menu_logo.is_displayed and self.support_link.is_displayed \
               and self.explorer_menu.is_displayed


class DashboardView(BaseAdminView):
    """Dashboard view page object that can be found on path"""
    path_pattern = '/p/admin/dashboard'
    account_link = Text('//a[@href="/buyers/accounts"]')
    application_link = Text('//a[@href="/p/admin/applications"]')
    billing_link = Text('//a[@href="/finance"]')
    develop_portal_link = Text('//a[@href="/p/admin/cms"]')
    message_link = Text('//a[@href="/p/admin/messages"]')
    explore_all_products = Text('//a[@href="/apiconfig/services"]')
    explore_all_backends = Text('//a[@href="/p/admin/backend_apis"]')

    @View.nested
    # pylint: disable=invalid-name
    class backends(View):
        """Backends page object"""
        backend_title = Text(locator='//*[@id="backends-widget"]/article/div[1]/div[1]/h1')
        create_backend_button = Button(locator='//a[@href="/p/admin/backend_apis/new"]')

        @property
        def is_displayed(self):
            return self.backend_title.is_displayed and self.create_backend_button.is_displayed

    @View.nested
    # pylint: disable=invalid-name
    class products(View):
        """Products page object"""
        products_title = Text(locator='//*[@id="products-widget"]/article/div[1]/div[1]/h1')
        create_product_button = Button(locator="//a[@href='/apiconfig/services/new']")

        @property
        def is_displayed(self):
            return self.products_title.is_displayed and self.create_product_button.is_displayed

    def prerequisite(self):
        return BaseAdminView

    @property
    def is_displayed(self):
        return self.path in self.browser.url and self.message_link.is_displayed \
               and self.products.is_displayed and self.backends.is_displayed \
               and self.account_link.is_displayed and self.application_link.is_displayed \
               and self.billing_link.is_displayed and self.develop_portal_link.is_displayed


class AccessDeniedView(View):
    """Base Access Denied page object"""
    logo = GenericLocatorWidget(locator="//h1[@id='logo']/span[@class='logo-3scale--svg']")
    title = Text(locator='//*[@id="content"]/h1[2]')
    text_message = Text(locator='//*[@id="content"]/p')

    @property
    def is_displayed(self):
        return self.title.text == "Access Denied" and \
               self.text_message.text == "Sorry, you do not have permission to access this page." and \
               self.logo.is_displayed
