#!/usr/bin/env python3
# -*- coding: utf8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options

import pandas as pd
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

import os

from classes.SequenceManager import SequenceManager



def selenium_docs_example():
    options = Options()
    options.headless = False

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



def example_local():
    options = Options()
    options.headless = False

    driver = webdriver.Firefox(
        options=options
    )

    driver.get("http://localhost:8001/")
    assert "Webscraping" in driver.page_source

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



def sequenced(name, variables={}):
    options = Options()
    options.headless = False

    driver = webdriver.Firefox(
        options=options
    )

    sequenceManager = SequenceManager(driver, name, os.path.abspath("."))
    sequenceManager.execute_sequences(variables=variables)

    driver.close()

def execute_input(filepath, n=10):
    print(
        """
        --------- COMPLETED ------------
        Executing "%s"...
        
        --------------------------------
        """ % filepath
    )

    l = []
    input_filepath = os.path.join("input", filepath)
    filetext = ""
    with open(input_filepath) as f:
        filetext = f.read()
        l = filetext.split("\n")

    i = 0
    for line in l:
        def update_list_file(input_filepath, filetext, 
                                        line, addtoken=""):
            # Update list file
            # ----------------
            filetext = filetext.replace(line, f"{line} {addtoken}")
            with open(input_filepath, "w") as f:
                f.write(filetext)
            return filetext


        def _exec(filepath, line, variables):
            print(
                """
                --------- EXECUTING ------------
                sequenced(name, %s)...                
                --------------------------------
                """ % str(variables)
            )
            sequence_file = name = filepath.replace("txt", "json")
            sequenced(name, variables=variables)
            
            # Update list file
            # ----------------
            filetext = update_list_file(input_filepath, filetext, 
                                        line, addtoken="✓")

            print(
                """
                --------- COMPLETED ------------
                sequenced(name, %s).                
                --------------------------------
                """ % str(variables)
            )

        variables = {
            "firstName": line.split(" ")[0],
            "lastName": line.split(" ")[1],
        }

        if line.find("✓") < 0 and line.find("✗") < 0:
            if i < n:
                try:
                    _exec(filepath, line, variables)
                    i += 1
                except Exception as err:
                    print('--------------| Error: ', err)
                except AssertionError as err:
                    # Update list file
                    # ----------------
                    filetext = update_list_file(input_filepath, filetext, 
                                                line, addtoken="✗")
                    i += 1
                    print('--------------| Error: ', err)
            else:
                break
        else:
            print(
                """
                ---------- SKIPPING ------------
                sequenced(name, %s) : Done ✓                
                --------------------------------
                """ % str(variables)
            )

    print(
        """

        --------- COMPLETED ------------

        %i inputs executed...
        
        --------------------------------
        """ % i
    )

if __name__ == "__main__":

    i = input(
        """
        --------------------------
        0.        selenium_docs_example()
        1.        example_local()
        2.        sequenced("selenium-docs-example")
        3.        sequenced("example-local")
        4.        truthfinder.sequences
        5.        execute_input(
                    "truthfinder.sequences/find-person-in-usa-by-firstname-and-lastname.sequence.txt",
                    n=3
                  )
        6.        sequenced(
                    "truthfinder.sequences/find-person-in-usa-by-firstname-and-lastname.sequence.json",
                    variables={
                        "firstName": input("Enter firstName: "),
                        "lastName": input("Enter lastName: "),
                  })

        --------------------------
        Enter any other to exit...

        ___________
        Enter value: """
    )

    if i:
        i = int(i)
        f = [
            selenium_docs_example,
            example_local,
            (sequenced, "selenium-docs-example"),
            (sequenced, "example-local"),
            (sequenced, "truthfinder.sequences"),
            (execute_input, 
                (
                    ("truthfinder.sequences/find-person-in-usa-by-firstname-and-lastname.sequence.txt",),
                    { "n": 3 }
                )
            ),
            (sequenced,
                (
                    ("truthfinder.sequences/find-person-in-usa-by-firstname-and-lastname.sequence.json",),
                    { 
                        "variables":
                        { 
                            "firstName": input(
                                "        - Enter firstName: "),
                            "lastName": input(
                                "        - Enter lastName: ")
                        }
                    }
                )
            ),
        ][i]

        if type(f) == type((1,1)):
            _func = f[0]
            _arg = f[1]

            if type(_arg) == type((1,1)):
                _func(*_arg[0], **_arg[1])
            else:
                _func(_arg)
        else:
            _func = f
            _func()

