import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    def testPage(self):
        # self.browser.get('http://www.google.com')
        self.browser.get("http://ec2-18-188-178-199.us-east-2.compute.amazonaws.com:8080/home/")

    def testSignup(self):
        self.browser.get("http://ec2-18-188-178-199.us-east-2.compute.amazonaws.com:8080/signup/")
        elem = self.browser.find_element_by_name("username")
        elem.send_keys('test0422_2')
        elem = self.browser.find_element_by_name("password1")
        elem.send_keys('qazwsxedc')
        elem = self.browser.find_element_by_name("password2")
        elem.send_keys('qazwsxedc')
        elem = self.browser.find_element_by_name("signup")
        elem.click()


    def testLogin(self):
        self.browser.get("http://ec2-18-188-178-199.us-east-2.compute.amazonaws.com:8080/login/")
        elem = self.browser.find_element_by_name("username")
        elem.send_keys('test0422_1')
        elem = self.browser.find_element_by_name("password")
        elem.send_keys('qazwsxedc')
        elem = self.browser.find_element_by_name("login")
        elem.click()

if __name__ == "__main__":
    unittest.main(verbosity=2)
