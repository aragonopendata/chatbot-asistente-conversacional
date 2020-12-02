'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

NODE_URL = "http://hamilton:3001"
# NODE_URL = "http://193.144.225.134:2999/"


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job_Firefox(self):
        capabilities = webdriver.DesiredCapabilities().FIREFOX
        capabilities["marionette"] = False
        driver = webdriver.Firefox(capabilities=capabilities)
        driver.implicitly_wait(30)
        driver.get(NODE_URL)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='Análisis y Estadísticas'])[1]/preceding::i[2]"
        ).click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='Análisis y estadísticas'])[1]/preceding::div[4]"
        ).click()
        # driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Análisis y estadísticas'])[1]/following::i[1]").click()
        driver.stop_client()
        driver.close()
        # driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='default'])[1]/following::span[1]").click()

    def test_app_dynamics_job_IExplorer(self):
        driver = webdriver.Ie("c:\\JENKINS\\IEDriverServer.exe")
        driver.get(NODE_URL)
        # driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Análisis y estadísticas'])[1]/preceding::i[2]").click()
        # driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Análisis y estadísticas'])[1]/preceding::div[4]").click()
        # driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Análisis y estadísticas'])[1]/following::i[1]").click()
        # driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='default'])[1]/following::span[1]").click()
        driver.stop_client()
        driver.close()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
