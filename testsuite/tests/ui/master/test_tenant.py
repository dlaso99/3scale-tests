"""
    Testing ground for testing master on tenant creation / edit / deletion ...
"""
from testsuite.ui.views.admin.login import LoginView
from testsuite.ui.views.common.foundation import NotFoundView
from testsuite.utils import blame
from testsuite.ui.views.master.audience.tenant import TenantDetailView, TenantEditView
from testsuite.ui.views.devel import LandingView


# pylint: disable=invalid-name
def check_is_displayed_in_new_tab(browser, new_tab_opener, View, wait=False):
    """
        Opens the website in the new tab and checks if it is displayed.
        If "wait" is set to true, it will also trigger a function THAT IS PRESENT ONLY IN SPECIFIC CLASSES in order to
        wait for the website to be loaded by refreshing it. (Example -> LandingView)
    """
    with browser.new_tab(new_tab_opener):
        view = View(browser)
        if wait:
            view.wait_page_ready()
        assert view.is_displayed


def test_create_tenant(custom_ui_tenant, request, navigator, browser, master_threescale):
    """
    Test:
        - Creates tenant via UI
        - Checks whether it exists
    """
    username = blame(request, "name")
    email_begin = blame(request, "email")     # [email_begin]@email.com     <- generates only [] part.
    org_name = blame(request, "org-name")
    tenant = custom_ui_tenant(username, email_begin, "description", org_name)
    account_id = tenant.entity['signup']['account']['id']
    account = master_threescale.accounts.read(account_id)

    assert account.entity_name == org_name

    detail_view = navigator.navigate(TenantDetailView, account=account)

    assert detail_view.public_domain.text == account.entity['domain']
    assert detail_view.admin_domain.text == account.entity['admin_domain']

    check_is_displayed_in_new_tab(browser, detail_view.open_public_domain, LandingView, wait=True)
    check_is_displayed_in_new_tab(browser, detail_view.open_admin_domain, LoginView)


# pylint: disable=unused-argument
def test_edit_tenant(master_login, navigator, custom_tenant, master_threescale):
    """
    Test:
        - Create tenant via API
        - Edit tenant via UI
        - check whether it was edited
    """
    tenant = custom_tenant()
    account_id = tenant.entity['signup']['account']['id']
    account = master_threescale.accounts.read(account_id)

    edit = navigator.navigate(TenantEditView, account=account)

    edit.update(org_name="updated_name")
    account = master_threescale.accounts.read(account_id)

    assert account.entity_name == "updated_name"


# pylint: disable=unused-argument
def test_delete_tenant(master_login, navigator, master_threescale, custom_tenant, browser):
    """
    Test:
        - Create tenant via API without auto-clean
        - Delete tenant via UI
        - Assert that deleted tenant is deleted
    """

    tenant = custom_tenant(autoclean=False)
    tenant.wait_tenant_ready()
    account_id = tenant.entity['signup']['account']['id']
    account = master_threescale.accounts.read(account_id)

    edit = navigator.navigate(TenantEditView, account=account)
    edit.delete()

    detail_view = navigator.navigate(TenantDetailView, account=tenant)

    account_deleted = master_threescale.accounts.read_by_name(account.entity_name)
    assert account_deleted.entity['state'] == 'scheduled_for_deletion'

    check_is_displayed_in_new_tab(browser, detail_view.open_public_domain, NotFoundView)
    check_is_displayed_in_new_tab(browser, detail_view.open_admin_domain, NotFoundView)

    # resume tenant from deletion
    detail_view.suspend_or_resume()

    account_deleted = master_threescale.accounts.read_by_name(account.entity_name)
    assert account_deleted.entity['state'] != 'scheduled_for_deletion'

    check_is_displayed_in_new_tab(browser, detail_view.open_public_domain, LandingView)
    check_is_displayed_in_new_tab(browser, detail_view.open_admin_domain, LoginView)

    edit = navigator.navigate(TenantEditView, account=tenant)
    edit.delete()

    account_deleted = master_threescale.accounts.read_by_name(account.entity_name)
    assert account_deleted.entity['state'] == 'scheduled_for_deletion'
