#!/usr/bin/env python3
# -*- coding: utf8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Element:
    element = None

    def wait(self, identifier, by=By.NAME, timeout=10):
        # Wait for the element to be clickable (adjust timeout as needed)
        print('------| waiting for %s...' % identifier)
        self.element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, identifier)) 
        ) 

    def send_keys(self, keys):
        # Interact with the element (e.g., send keys)
        print('------| sending %s to element (keys: %s)...' \
                                    % (keys, element.__dict__.keys()))
        self.element.send_keys(keys)

def step1():

    # Initialize WebDriver (e.g., Chrome)
    driver = webdriver.Chrome()

    # Navigate to TruthFinder website (replace with the actual URL)
    driver.get("https://www.truthfinder.com/people-search/") 

    try:
        # Example: Find elements by name and interact, send keys
        firstNameEl = Element().wait("firstName")
        firstNameEl.send_keys("David") 

    except Exception as e:
        print(f"Error locating or interacting with element: {e}")

    # Close the browser
    driver.quit()

step1()