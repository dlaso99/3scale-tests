"""View representations of Accounts pages"""
from widgetastic.widget import TextInput, GenericLocatorWidget

from testsuite.ui.navigation import step
from testsuite.ui.views.admin.foundation import AudienceNavView
from testsuite.ui.widgets import Link, ThreescaleDropdown, AudienceTable, ThreescaleCreateButton, \
    ThreescaleUpdateButton, ThreescaleDeleteButton, ThreescaleEditButton, ThreescaleCheckBox


class AccountsView(AudienceNavView):
    """View representation of Accounts Listing page"""
    endpoint_path = '/buyers/accounts'
    new_account = Link("//a[@href='/buyers/accounts/new']")
    table = AudienceTable("//*[@id='buyer_accounts']")

    @step("NewAccountView")
    def new(self):
        """Create new Account"""
        self.new_account.click()

    @step("AccountsDetailView")
    def detail(self, account_id):
        """Opens detail Account by ID"""
        self.table.row(_row__attr=('id', 'account_' + str(account_id))).grouporg.click()

    # pylint: disable=invalid-overridden-method
    def prerequisite(self):
        return AudienceNavView

    def is_displayed(self):
        return AudienceNavView.is_displayed and self.new_account.is_displayed and self.table.is_displayed and \
               self.endpoint_path in self.browser.url


class AccountsDetailView(AudienceNavView):
    """View representation of Account detail page"""
    endpoint_path = '/buyers/accounts/{account_id}'
    edit_button = ThreescaleEditButton()
    plan_dropdown = ThreescaleDropdown("//*[@id='account_contract_plan_id']")
    change_plan_button = GenericLocatorWidget("//*[@value='Change']")
    applications_button = Link("//*[contains(@title,'applications')]")

    @step("AccountEditView")
    def edit(self):
        """Edit account"""
        self.edit_button.click()

    @step("AccountApplicationsView")
    def applications(self):
        """Open account's applications"""
        self.applications_button.click()

    # pylint: disable=invalid-overridden-method
    def prerequisite(self):
        return AccountsView

    def is_displayed(self):
        return AudienceNavView.is_displayed and self.endpoint_path in self.browser.url

    def change_plan(self, value):
        """Change account plan"""
        self.plan_dropdown.select_by_value(value)
        self.change_plan_button.click(handle_alert=True)


class NewAccountView(AudienceNavView):
    """View representation of New Account page"""
    endpoint_path = '/buyers/accounts/new'
    username = TextInput(id='account_user_username')
    email = TextInput(id='account_user_email')
    password = TextInput(id='account_user_password')
    organization = TextInput(id='account_org_name')
    create_button = ThreescaleCreateButton()

    # pylint: disable=invalid-overridden-method
    def prerequisite(self):
        return AccountsView

    def is_displayed(self):
        return AudienceNavView.is_displayed and self.username.is_displayed and self.email.is_displayed \
               and self.organization.is_displayed and self.endpoint_path in self.browser.url

    def create(self, username: str, email: str, password: str, organization: str):
        """Crate new account"""
        self.username.fill(username)
        self.email.fill(email)
        self.password.fill(password)
        self.organization.fill(organization)
        self.create_button.click()


class AccountEditView(AudienceNavView):
    """View representation of Edit Account page"""
    endpoint_path = "/buyers/accounts/{account_id}/edit"
    org_name = TextInput(id="account_org_name")
    update_button = ThreescaleUpdateButton()
    delete_button = ThreescaleDeleteButton()

    # pylint: disable=invalid-overridden-method
    def prerequisite(self):
        return AccountsDetailView

    def is_displayed(self):
        return AudienceNavView.is_displayed and self.org_name.is_displayed

    def update(self, org_name: str):
        """Update account"""
        self.org_name.fill(org_name)
        self.update_button.click()

    def delete(self):
        """Delete account"""
        self.delete_button.click()


class AccountApplicationsView(AudienceNavView):
    """View representation of Account's Applications page"""
    endpoint_path = "/buyers/accounts/{account_id}/applications"
    create_button = Link("//*[contains(@href,'/applications/new')]")

    @step("NewApplicationView")
    def new(self):
        """Crate new application"""
        self.create_button.click()

    # pylint: disable=invalid-overridden-method
    def prerequisite(self):
        return AccountsDetailView

    def is_displayed(self):
        return AudienceNavView.is_displayed and self.create_button.is_displayed and \
               self.endpoint_path in self.browser.url


class UsageRulesView(AudienceNavView):
    """View representation of Account's Usage Rules page"""
    endpoint_path = "/site/usage_rules/edit"
    account_plans_checkbox = ThreescaleCheckBox(locator="//input[@id='settings_account_plans_ui_visible']")
    update_button = ThreescaleUpdateButton()

    # pylint: disable=invalid-overridden-method
    def prerequisite(self):
        return AudienceNavView

    def is_displayed(self):
        return AudienceNavView.is_displayed and self.account_plans_checkbox.is_displayed and \
               self.endpoint_path in self.browser.url

    def account_plans(self):
        """Allow account plans"""
        self.account_plans_checkbox.check()
        self.update_button.click()
