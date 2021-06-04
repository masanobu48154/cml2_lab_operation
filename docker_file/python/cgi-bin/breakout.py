#!user/bin/python

import textwrap
import time
import env
import apple
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# CSS selector element to be processed.
configuration_tab = textwrap.dedent('''\
    #app > section > header > div > div > div > div:nth-child(2) > ul > \
    li:nth-child(2)\
''')
username_box = textwrap.dedent('''\
    #config > div > div > div > div > form > div:nth-child(4) > div > div > \
    input\
''')
controller_address_box = textwrap.dedent('''\
    #config > div > div > div > div > form > div:nth-child(1) > div > \
    div > input\
''')
verify_tls_switch = textwrap.dedent('''\
    #config > div > div > div > div > form > div:nth-child(2) > div > \
    div > span\
''')
all_nodes_switch = textwrap.dedent('''\
    #config > div > div > div > div > form > div:nth-child(3) > div > \
    div > span\
''')
password_box = textwrap.dedent('''\
    #config > div > div > div > div > form > div:nth-child(5) > div > \
    div > input\
''')
listen_address_box = textwrap.dedent('''\
    #config > div > div > div > div > form > div:nth-child(8) > div > \
    div > input\
''')
save_button = textwrap.dedent('''\
    #config > div > div > div > div > form > \
    button.el-button.el-button--primary\
''')
labs_tab = textwrap.dedent('''\
    #app > section > header > div > div > div > div:nth-child(2) > \
    ul > li:nth-child(1)\
''')
refresh_button = textwrap.dedent('''\
    #labs > div > div > div > div > \
    div.el-row.is-align-middle.el-row--flex > div.el-col.el-col-8 > \
    button.el-button.el-tooltip.el-button--primary.is-circle\
''')
onoff_switch = textwrap.dedent('''\
    #labs > div > div > div > div > div:nth-child(2) > div > div > \
    div.el-table__body-wrapper.is-scrolling-none > table > tbody > \
    tr > td.el-table_2_column_8 > div > div\
''')


class BreakOut:
    """
    Class for operating Breakout UI with selenium grid.
    How to call:
        1. Create a object with the CML2 lab address,
           the Selenium grid hub address, and the Breakout UI address.
        2. Execute breakout function.
    """

    def __init__(self, host, break_host):
        """
        Parameters
        ----------
        host : str
            CML2 lab address or FQDN
        break_host : str
            Breakout UI address or FQDN
        """
        env_object = env.MyEnv()
        self.login_data = {
            "username": env_object.my_env["your_username"],
            "password": env_object.my_env["your_password"]
        }
        self.host = host
        self.selenium_hub = 'http://{0}:4444/wd/hub'.format(
            env_object.my_env["selenium_hub"])
        self.break_host = break_host

    def get_webdriver(self):
        """
        Call an object of selenium.

        returns
        -------
        object
            webdriver object
        """
        return webdriver.Remote(command_executor=self.selenium_hub,
                                desired_capabilities=DesiredCapabilities.CHROME)

    def click_selector(self, getwebdriver_object, selector):
        """
        Function to click on the specified css selector element.

        Parameters
        ----------
        getwebdriver_object : object
            Return object of get_webdriver method
        selector : str
            CSS selector element to be clicked
        """
        element = getwebdriver_object.find_element_by_css_selector(selector)
        element.click()
        time.sleep(2)

    def get_attribute(self, getwebdriver_object, selector):
        """
        Function that extracts attributes from the specified css
        selector element.

        Parameters
        ----------
        getwebdriver_object : object
            Return object of get_webdriver method
        selector : str
            CSS selector element to be extracted attributes

        returns
        -------
        str
            String extracted from text box
        """
        element = getwebdriver_object.find_element_by_css_selector(selector)
        val = element.get_attribute("value")
        time.sleep(2)
        return val

    def sendkey_selector(self, getwebdriver_object, key, selector):
        """
        Function that sends attributes to the specified css selector element.

        Parameters
        ----------
        getwebdriver_object : object
            Return object of get_webdriver method
        key : str
            Text sent to CSS selector element
        selector : str
            CSS selector element to which the attribute is sent.
        """
        element = getwebdriver_object.find_element_by_css_selector(selector)
        element.clear()
        time.sleep(2)
        element.send_keys(key)
        time.sleep(2)

    def breakout(self):
        """
        Function that operate Breakout UI.
        1. If the attribute in the username text box is not the correct login
           user for CML2, change the settings on the configuration page.
        2. Refresh lab on the labs page and turn on the status toggle switch.
        """
        object = apple.Cml2(self.host)
        if object.check_converged() == "True":
            with self.get_webdriver() as driver:
                driver.get('http://{0}:8080'.format(self.break_host))
                self.click_selector(driver, configuration_tab)
                if self.get_attribute(
                        driver, username_box) != self.login_data["username"]:
                    self.sendkey_selector(
                        driver, 'https://{0}'.format(
                            self.host), controller_address_box)
                    self.click_selector(
                        driver, verify_tls_switch)
                    self.click_selector(
                        driver, all_nodes_switch)
                    self.sendkey_selector(
                        driver, '{0}'.format(
                            self.login_data["username"]), username_box)
                    self.sendkey_selector(
                        driver, '{0}'.format(
                            self.login_data["password"]), password_box)
                    self.sendkey_selector(
                        driver, self.break_host, listen_address_box)
                    self.click_selector(
                        driver, save_button)
                self.click_selector(driver, labs_tab)
                self.click_selector(driver, refresh_button)
                self.click_selector(driver, onoff_switch)
            return "Success"
        else:
            return "Fail"


if __name__ == '__main__':
    host = input("Target CML Address : ")
    break_host = input("Breakout server address : ")
    ob = BreakOut(host, break_host)
    print(ob.breakout())
