import logging
import re
import time
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


browser = webdriver.Firefox()

log = logging.getLogger(__name__)


def login(account_id, username, password):
    log.info('Logging in as %s for account %s...', username, account_id)
    browser.get('https://www.sircon.com/login.html')
    browser.find_element_by_id('accountId').send_keys(account_id)
    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('password').send_keys(password)
    browser.find_element_by_css_selector('input.submit').click()
    time.sleep(6)   # Selenium is moving too quickly?


def search_and_result_url(ssn, last_name):
    log.info('Searching for %s, %s-xx-xxx...', last_name, ssn[:3])
    browser.get('https://www.sircon.com/ComplianceExpress/Inquiries/PdbInq.jsp?entTypeCd=IL&srvcTypeCd=PDBQ')
    browser.find_element_by_css_selector('form[name=PdbInqForm] input[name=tin]').send_keys(ssn)
    elem = browser.find_element_by_css_selector('form[name=PdbInqForm] input[name=lname]')
    elem.send_keys(last_name)
    elem.send_keys(Keys.RETURN)

    elem = browser.find_element_by_css_selector('table a')
    href = elem.get_attribute('href')
    log.info('Found URL %s.', href)
    return href


def _get_license_info(basic_html, activity_html):
    basic_details = basic_html.find_elements_by_css_selector('td')[1::2]
    license_number = basic_details[0]
    issue_date = basic_details[1]
    expiration_date = basic_details[2]
    license_class = basic_details[3]
    residency = basic_details[4]
    active = basic_details[5]

    # TODO Process activity block

    # TODO Store/return this info


def _get_appointment_info(html):
    # TODO Process the appointment info
    pass


def get_person_info(ssn, last_name):
    url = search_and_result_url(ssn, last_name)
    browser.get(url)

    # Filter the info
    log.info('Retrieving license and appointment info...')
    browser.find_element_by_css_selector('input[name=licenses]').click()
    browser.find_element_by_css_selector('input[name=appointments]').click()
    browser.find_element_by_css_selector('input[name=groupByState]').click()
    browser.find_element_by_css_selector('input[type=submit]').click()

    # Get the person's info
    state_name_regex = re.compile("STATE: (\w+)")

    # Get the state elements
    state_data = browser.find_elements_by_css_selector('table[xmlns\\:fo] font.header')[1:-1]
    state_data = state_data[0::3]

    for datum in state_data:
        text = datum.text
        state_name = state_name_regex.search(text).groups()[0]
        log.info('Processing data for %s', state_name)

        details = datum.find_elements_by_css_selector('table.statusInqTable')
        _get_license_info(details[0], details[1])
        _get_appointment_info(details[2])


if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2], sys.argv[3])

    # TODO Read people from CSV
    get_person_info(sys.argv[4], sys.argv[5])

    # TODO Write parsed info to a different CSV
