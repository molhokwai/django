#!/usr/bin/env python3
# -*- coding: utf8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = False

import pandas as pd
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

def example1():
    driver = webdriver.Firefox(
        options=options        
    )
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element(By.NAME, "q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source

    print("""
        ------------ OK ----------------
        assert "Python" in driver.title
        assert "No results found." not in driver.page_source
        --------------------------------
    """)

    driver.close()


def example1_local():
    driver = webdriver.Firefox(
        options=options        
    )

    driver.get("http://localhost:8001/")
    assert  "Webscraping" in driver.page_source

    # Find button/link element and press Enter to navigate
    # ------------------------------------------
    elem = driver.find_element(By.ID, "webscraping")
    elem.send_keys(Keys.RETURN)


    # Navigation to another page
    # Page load, wait for element to be clickable
    # ------------------------------------------
    elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "first_name")) 
    ) 
    elem.clear()
    elem.send_keys("David")


    # Page loaded, Find and fill elements
    # ------------------------------------------
    elem = driver.find_element(By.ID, "last_name")
    elem.clear()
    elem.send_keys("Jonathan")

    elem = driver.find_element(By.ID, "last_name")
    elem.clear()
    elem.send_keys("Jonathan")

    # Find button/link element, press Enter
    # ------------------------------------------
    elem = driver.find_element(By.ID, "unique_title")
    elem.send_keys(Keys.RETURN)

    elem = driver.find_element(By.ID, "title")
    title = elem.get_attribute("value")

    assert "David Jonathan" in title
    assert "GMT" in title

    print("""
        ------------ OK ----------------
        assert "David Jonathan" in title
        assert "GMT" in title
        --------------------------------
    """)


    elem = driver.find_element(By.ID, "webscrapes-table")
    text = elem.get_attribute("innerText")

    print(f"""
        ------------ TEXT --------------
        {text} 
        --------------------------------
    """)
    data = StringIO(f"""
        {text} 
    """)
    # df = pd.read_fwf('log.txt')
    df = pd.read_table(data)
    df.to_csv('data.csv')


    driver.close()


if __name__ == "__main__":

    i = input(
        """
        --------------------------
        0.        example1()
        1.        example1_local()
        --------------------------
        Enter any other to exit...
        """
    )

    if i:
        i = int(i)
        f = [example1, example1_local]
        f[i]()


