"""
    Testing ground for testing master on tenant creation / edit / deletion ...
"""
from testsuite.ui.views.admin.login import LoginView
from testsuite.ui.views.common.foundation import NotFoundView
from testsuite.utils import blame
from testsuite.ui.views.master.audience.tenant import TenantDetailView, TenantEditView
from testsuite.ui.views.devel import LandingView


def test_create_tenant(custom_ui_tenant, request, navigator, browser):
    """
    Test:
        - Creates tenant via UI
        - Checks whether it exists
    """
    username = blame(request, "name")
    email_begin = blame(request, "email")     # [email_begin]@email.com     <- generates only [] part.
    org_name = blame(request, "org-name")
    tenant = custom_ui_tenant(username, email_begin, "description", org_name)

    assert tenant.entity_name == org_name

    detail_view = navigator.navigate(TenantDetailView, account=tenant)

    assert detail_view.public_domain.text == tenant.entity['domain']
    assert detail_view.admin_domain.text == tenant.entity['admin_domain']

    with browser.new_tab(detail_view.open_public_domain):
        view = LandingView(browser)
        view.wait_page_ready()
        assert view.is_displayed

    with browser.new_tab(detail_view.open_admin_domain):
        view = LoginView(browser)
        assert view.is_displayed


# pylint: disable=unused-argument
def test_edit_tenant(master_login, navigator, custom_tenant, master_threescale):
    """
    Test:
        - Create tenant via API
        - Edit tenant via UI
        - check whether it was edited
    """
    account = custom_tenant()
    edit = navigator.navigate(TenantEditView, account=account)

    edit.update(org_name="updated_name")
    account = master_threescale.accounts.read(account.entity_id)

    assert account is not None
    assert account.entity_name == "updated_name"


# pylint: disable=unused-argument
def test_delete_tenant(master_login, navigator, threescale, custom_tenant, browser):
    """
    Test:
        - Create tenant via API without auto-clean
        - Delete tenant via UI
        - Assert that deleted tenant is deleted
    """

    account = custom_tenant(autoclean=False)
    # account.wait_tenant_ready()

    edit = navigator.navigate(TenantEditView, account=account)
    edit.delete()

    detail_view = navigator.navigate(TenantDetailView, account=account)

    account_deleted = threescale.accounts.read_by_name(account.entity_name)
    assert account_deleted is None

    with browser.new_tab(detail_view.open_public_domain):
        view = NotFoundView(browser)
        assert view.is_displayed

    with browser.new_tab(detail_view.open_admin_domain):
        view = NotFoundView(browser)
        assert view.is_displayed

    # resume tenant from deletion
    detail_view.suspend_or_resume()

    with browser.new_tab(detail_view.open_public_domain):
        view = LandingView(browser)
        view.wait_page_ready()
        assert view.is_displayed

    with browser.new_tab(detail_view.open_admin_domain):
        view = LoginView(browser)
        assert view.is_displayed

    edit = navigator.navigate(TenantEditView, account=account)
    edit.delete()

    account_deleted = threescale.accounts.read_by_name(account.entity_name)
    assert account_deleted is None
