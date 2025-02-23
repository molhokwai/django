#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import pandas as pd,sys
if sys.version_info[0]<3:from StringIO import StringIO
else:from io import StringIO
import os
from classes.SequenceManager import SequenceManager
def selenium_docs_example():C=Options();C.headless=False;A=webdriver.Firefox(options=C);A.get('http://www.python.org');assert'Python'in A.title;B=A.find_element(By.NAME,'q');B.clear();B.send_keys('pycon');B.send_keys(Keys.RETURN);assert'No results found.'not in A.page_source;print('\n        ------------ OK ----------------\n        assert "Python" in driver.title\n        assert "No results found." not in driver.page_source\n        --------------------------------\n    ');A.close()
def example_local():driver.get('http://localhost:8001/');assert'Webscraping'in driver.page_source;A=driver.find_element(By.ID,'webscraping');A.send_keys(Keys.RETURN);A=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,'first_name')));A.clear();A.send_keys('David');A=driver.find_element(By.ID,'last_name');A.clear();A.send_keys('Jonathan');A=driver.find_element(By.ID,'unique_title');A.send_keys(Keys.RETURN);A=driver.find_element(By.ID,'title');B=A.get_attribute('value');assert'David Jonathan'in B;assert'GMT'in B;print('\n        ------------ OK ----------------\n        assert "David Jonathan" in title\n        assert "GMT" in title\n        --------------------------------\n    ');A=driver.find_element(By.ID,'webscrapes-table');C=A.get_attribute('innerText');print(f"\n        ------------ TEXT --------------\n        {C} \n        --------------------------------\n    ");D=StringIO(f"\n        {C} \n    ");E=pd.read_table(D);E.to_csv('data.csv');driver.close()
def sequenced(name):A=SequenceManager(driver,name,os.path.abspath('.'));A.execute_sequences();driver.close()
if __name__=='__main__':
	i=input('\n        --------------------------\n        0.        selenium_docs_example()\n        1.        example_local()\n        2.        sequenced("selenium-docs-example")\n        3.        sequenced("example-local")\n        4.        truthfinder.sequences\n        --------------------------\n        Enter any other to exit...\n\n        ___________\n        Enter value: ')
	if i:
		i=int(i);f=[selenium_docs_example,example_local,(sequenced,'selenium-docs-example'),(sequenced,'example-local'),(sequenced,'truthfinder.sequences')][i]
		if type(f)==type((1,1)):_func=f[0];_arg=f[1];_func(_arg)
		else:_func=f;_func()