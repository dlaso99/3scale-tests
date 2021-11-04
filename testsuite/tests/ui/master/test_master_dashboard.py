"""
    rewrite of admin dashboard test to master
"""
from testsuite.ui.views.master.foundation import MasterDashboardView


# pylint: disable=unused-argument
def test_dashboard_is_loaded_correctly(master_login, navigator):
    """
    Test:
        - Navigates to Dashboard
        - Checks whether everything is on the dashboard that is supposed to be there

        if this fails, there is higher chance that there is something wrong in the core, rather than here.
    """
    dashboard = navigator.navigate(MasterDashboardView)

    assert dashboard.is_displayed
