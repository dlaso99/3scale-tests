"""View representations of Tenants pages"""
from widgetastic.widget import TextInput, GenericLocatorWidget, Text

from testsuite.ui.navigation import step
from testsuite.ui.views.master.audience import BaseMasterAudienceView
from testsuite.ui.widgets import AudienceTable
from testsuite.ui.widgets.buttons import ThreescaleDeleteButton, \
    ThreescaleEditButton, ThreescaleSubmitButton, ThreescaleSearchButton


class TenantView(BaseMasterAudienceView):
    """View representation of Tenants Listing page"""
    # TODO search will be separated into the AudienceTable Widget later.
    path_pattern = '/buyers/accounts'
    new_account = Text("//a[@href='/p/admin/accounts/new']")
    table = AudienceTable("//*[@id='buyer_accounts']")
    search_button = ThreescaleSearchButton()
    search_bar = TextInput(id="search_query")

    def search(self, value: str):
        """Search in Tenant table by given value"""
        self.search_bar.fill(value)
        self.search_button.click()

    @step("TenantNewView")
    def new(self):
        """Create new Tenant"""
        self.new_account.click()

    @step("TenantDetailView")
    def detail(self, account):
        """Opens detail Account by ID"""
        self.table.row(_row__attr=('id', f'account_{account.entity_id}')).grouporg.click()

    def prerequisite(self):
        return BaseMasterAudienceView

    @property
    def is_displayed(self):
        return BaseMasterAudienceView.is_displayed.fget(self) and self.new_account.is_displayed and \
               self.table.is_displayed and self.path_pattern in self.browser.url


class TenantDetailView(BaseMasterAudienceView):
    """View representation of Tenant detail page"""
    path_pattern = '/buyers/accounts/{account_id}'
    edit_button = ThreescaleEditButton()
    applications_button = Text("//*[contains(@title,'applications')]")
    public_domain = Text('//*[@id="twoCol"]/div[1]/div/table/tbody/tr[2]/td/a')
    admin_domain = Text('//*[@id="twoCol"]/div[1]/div/table/tbody/tr[3]/td/a')
    suspend_button = Text('//*[@id="twoCol"]/div[1]/div/table/tbody/tr[6]/td/a')

    def __init__(self, parent, account):
        super().__init__(parent, account_id=account.entity_id)

    @step("TenantEditView")
    def edit(self):
        """Edit account"""
        self.edit_button.click()

    def suspend_or_resume(self):
        """suspend / resume button click function that also handles alert"""
        self.suspend_button.click(handle_alert=True)

    def open_public_domain(self):
        """a helper function to open public-domain"""
        self.public_domain.click()

    def open_admin_domain(self):
        """a helper function to open admin-portal"""
        self.admin_domain.click()

    def prerequisite(self):
        return TenantView

    @property
    def is_displayed(self):
        return BaseMasterAudienceView.is_displayed.fget(self) and self.path_pattern in self.browser.url and \
               self.applications_button.is_displayed and self.admin_domain.is_displayed and \
               self.public_domain.is_displayed


class TenantNewView(BaseMasterAudienceView):
    """View representation of New Tenant page"""
    path_pattern = '/p/admin/accounts/new'
    password_confirm = TextInput(id="account_user_password_confirmation")
    username = TextInput(id='account_user_username')
    email = TextInput(id='account_user_email')
    password = TextInput(id='account_user_password')
    organization = TextInput(id='account_org_name')
    create_button = ThreescaleSubmitButton()

    def create(self, username: str, email: str, password: str, organization: str):
        """Crate new account"""
        self.username.fill(username)
        self.email.fill(email)
        self.password.fill(password)
        self.organization.fill(organization)
        self.password_confirm.fill(password)
        self.create_button.click()

    def prerequisite(self):
        return TenantView

    @property
    def is_displayed(self):
        return BaseMasterAudienceView.is_displayed.fget(self) and self.password_confirm.is_displayed \
               and self.username.is_displayed and self.email.is_displayed \
               and self.organization.is_displayed and self.path_pattern in self.browser.url


class TenantEditView(BaseMasterAudienceView):
    """View representation of Edit Tenant page"""
    path_pattern = "/buyers/accounts/{account_id}/edit"
    org_name = TextInput(id="account_org_name")
    update_button = GenericLocatorWidget("//input[@value='Update Account']")
    delete_button = ThreescaleDeleteButton()

    def __init__(self, parent, account):
        super().__init__(parent, account_id=account.entity_id)

    def update(self, org_name: str):
        """Update account"""
        self.org_name.fill(org_name)
        self.update_button.click()

    def delete(self):
        """Delete account"""
        self.delete_button.click()

    def prerequisite(self):
        return TenantDetailView

    @property
    def is_displayed(self):
        return BaseMasterAudienceView.is_displayed.fget(self) and self.org_name.is_displayed \
               and self.org_name.is_displayed and self.update_button.is_displayed
