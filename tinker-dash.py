import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

DASHBOARD_LIST = 'the-dashboard-list.txt'
TAB_ROTATION_PERIOD = 5  # 5 second tab rotation


def pull_list(list_file):
    with open(list_file) as f:
        content = f.readlines()
    # Remove whitespace characters from the end of each line
    content = [x.strip() for x in content]

    return content


def open_dashboard(url_list, driver):
    max_tabs = len(url_list) - 1
    tab_ordinal = 1

    for dashboard_url in url_list:
        # 10 second limit on loading URLs
        try:
            driver.set_page_load_timeout(10)
            driver.get(dashboard_url)
            if tab_ordinal <= max_tabs:
                browser_tab = 'tab' + str(tab_ordinal + 1)
                tab_open_command = "window.open('about:blank', '" + browser_tab + "');"
                driver.execute_script(tab_open_command)
                driver.switch_to.window(browser_tab)
                tab_ordinal += 1
        except TimeoutException:
            pass


def rotate_dashboard(url_list, driver):
    max_tabs = len(url_list) - 1
    tab_ordinal = 1

    while tab_ordinal <= max_tabs:
        browser_tab = 'tab' + str(tab_ordinal + 1)
        driver.switch_to.window(browser_tab)
        time.sleep(TAB_ROTATION_PERIOD)
        tab_ordinal += 1


def main():
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

    dashboard_list = pull_list(DASHBOARD_LIST)
    # The first browser tab is not in the tab rotation sequence (it is just a placeholder)
    dashboard_list.insert(0, 'https://python.org')
    open_dashboard(dashboard_list, browser)

    running = True
    while running:
        new_dashboard_list = pull_list(DASHBOARD_LIST)
        new_dashboard_list.insert(0, 'https://python.org')
        # Detect new content in the dashboard list
        if new_dashboard_list != dashboard_list:
            dashboard_list = new_dashboard_list
            browser.stop_client()
            browser.quit()
            browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
            open_dashboard(dashboard_list, browser)

        rotate_dashboard(dashboard_list, browser)


main()
