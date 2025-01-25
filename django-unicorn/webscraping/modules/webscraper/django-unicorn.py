#!/usr/bin/env python3
# -*- coding: utf8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Element:
    driver = None
    element = None

    def __init__(self, driver):
        self.driver = driver

    def find(self, identifier, by=By.ID, timeout=10):
        # Wait for the element to be clickable (adjust timeout as needed)
        print('------| findind "%s"...' % identifier)        
        self.element = self.driver.find_element(b, identifier)

    def wait(self, identifier, by=By.ID, timeout=10):
        # Wait for the element to be clickable (adjust timeout as needed)
        print('------| waiting for "%s"...' % identifier)
        self.element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, identifier)) 
        ) 

    def send_keys(self, keys):
        # Interact with the element (e.g., send keys)
        print('------| sending "%s" to element (keys: %s)...' \
                                    % (keys, element.__dict__.keys()))
        self.element.send_keys(keys)

def step1():

    fields_keys = {
        'website_url': 'https://www.truthfinder.com/',
        'title': '',
        'first_name': 'David',
        'last_name': 'Jonathan',
        'middle_name': 'Henry',
        'middle_initials': 'H.',
        'age': 55,
        'city': 'New York',
        'state': 'NJ',
        'country': 'US'
    }

    # Initialize WebDriver (e.g., Chrome)
    driver = webdriver.Chrome()

    # Navigate to TruthFinder website (replace with the actual URL)
    driver.get("http://localhost:8001/webscraping/") 

    try:
        # Example: Find elements by name and interact, send keys
        for _id in fields_keys:
            firstNameEl = Element(driver)
            # firstNameEl.wait(_id)
            firstNameEl.find(_id)
            firstNameEl.send_keys(fields_keys[_id])

    except Exception as e:
        print(f"Error locating or interacting with element: {e}")

    # Close the browser
    driver.quit()

step1()