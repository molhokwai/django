#!/usr/bin/env python3
_E='variables'
_D='truthfinder.sequences/find-person-in-usa.sequence.json'
_C='lastName'
_B='firstName'
_A=False
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import sys
if sys.version_info[0]<3:from StringIO import StringIO
else:from io import StringIO
import os
from django_app.settings import _print
from modules.webscraper.classes.SequenceManager import SequenceManager
def selenium_docs_example():C=Options();C.headless=_A;A=webdriver.Firefox(options=C);A.get('http://www.python.org');assert'Python'in A.title;B=A.find_element(By.NAME,'q');B.clear();B.send_keys('pycon');B.send_keys(Keys.RETURN);assert'No results found.'not in A.page_source;_print('\n        ------------ OK ----------------\n        assert "Python" in driver.title\n        assert "No results found." not in driver.page_source\n        --------------------------------\n    ',VERBOSITY=0);A.close()
def example_local():C=Options();C.headless=_A;B=webdriver.Firefox(options=C);B.get('http://localhost:8001/');assert'Webscraping'in B.page_source;A=B.find_element(By.ID,'webscraping');A.send_keys(Keys.RETURN);A=WebDriverWait(B,10).until(EC.element_to_be_clickable((By.ID,'first_name')));A.clear();A.send_keys('David');A=B.find_element(By.ID,'last_name');A.clear();A.send_keys('Jonathan');A=B.find_element(By.ID,'unique_title');A.send_keys(Keys.RETURN);A=B.find_element(By.ID,'title');D=A.get_attribute('value');assert'David Jonathan'in D;assert'GMT'in D;_print('\n        ------------ OK ----------------\n        assert "David Jonathan" in title\n        assert "GMT" in title\n        --------------------------------\n    ',VERBOSITY=0);A=B.find_element(By.ID,'webscrapes-table');E=A.get_attribute('innerText');_print(f"\n        ------------ TEXT --------------\n        {E}\n        --------------------------------\n    ",VERBOSITY=0);F=StringIO(f"\n        {E}\n    ");"\n        read from file\n        --------------\n        df = pandas.read_fwf('log.txt')\n    ";G=pandas.read_table(F);G.to_csv('data.csv');B.close()
def sequenced(name,variables={}):
	A=variables;B=Options();B.headless=_A
	for C in A:
		D=A[C]
		if type(D)==type(lambda x:x):A[C]=D()
	E=webdriver.Firefox(options=B);F=SequenceManager(E,name,os.path.abspath('.'));F.execute_sequences(variables=A);E.close()
def execute_input(filepath,n=10):
	D=filepath;_print('\n        --------- COMPLETED ------------\n        Executing "%s"...\n\n        --------------------------------\n        '%D,VERBOSITY=0);G=[];E=os.path.join('input',D);B=''
	with open(E)as J:B=J.read();G=B.split('\n')
	C=0
	for A in G:
		def H(input_filepath,filetext,line,addtoken=''):
			A=filetext;A=A.replace(line,f"{line} {addtoken}")
			with open(input_filepath,'w')as B:B.write(A)
			return A
		def K(filepath,line,variables):A=variables;_print('\n                --------- EXECUTING ------------\n                sequenced(name, %s)...\n                --------------------------------\n                '%str(A),VERBOSITY=0);D=B=filepath.replace('txt','json');sequenced(B,variables=A);C=H(E,C,line,addtoken='✓');_print('\n                --------- COMPLETED ------------\n                sequenced(name, %s).\n                --------------------------------\n                '%str(A),VERBOSITY=0)
		I={_B:A.split(' ')[0],_C:A.split(' ')[1]}
		if A.find('✓')<0 and A.find('✗')<0:
			if C<n:
				try:K(D,A,I);C+=1
				except AssertionError as F:B=H(E,B,A,addtoken='✗');C+=1;_print('--------------| Assertion rrror: ',F.args[0],VERBOSITY=0)
				except Exception as F:print('--------------| Error: ',F)
			else:break
		else:_print('\n                ---------- SKIPPING ------------\n                sequenced(name, %s) : Done ✓\n                --------------------------------\n                '%str(I),VERBOSITY=0)
	_print('\n\n        --------- COMPLETED ------------\n\n        %i inputs executed...\n\n        --------------------------------\n        '%C,VERBOSITY=0)
if __name__=='__main__':
	i=input('\n        --------------------------\n        0.        selenium_docs_example()\n        1.        example_local()\n        2.        sequenced("selenium-docs-example")\n        3.        sequenced("example-local")\n        4.        truthfinder.sequences\n        5.        execute_input(\n                    "truthfinder.sequences/find-person-in-usa-by-firstname-and-lastname.sequence.txt",\n                    n=3\n                  )\n        6.        sequenced(\n                    "truthfinder.sequences/find-person-in-usa-by-firstname-and-lastname.sequence.json",\n                    variables={\n                        "firstName": input("Enter firstName: "),\n                        "lastName": input("Enter lastName: "),\n                  })\n        7.        sequenced(\n                    "truthfinder.sequences/find-person-in-usa-by-firstname-and-lastname.sequence.json",\n                    variables={\n                        "firstName": "William",\n                        "lastName": "Smith",\n                  })\n\n        --------------------------\n        Enter any other to exit...\n\n        ___________\n        Enter value: ')
	if i:
		i=int(i);f=[selenium_docs_example,example_local,(sequenced,'selenium-docs-example'),(sequenced,'example-local'),(sequenced,'truthfinder.sequences'),(execute_input,(('truthfinder.sequences/find-person-in-usa.sequence.txt',),{'n':3})),(sequenced,((_D,),{_E:{_B:lambda:input('        - Enter firstName: '),_C:lambda:input('        - Enter lastName: ')}})),(sequenced,((_D,),{_E:{_B:'William',_C:'Smith'}}))][i]
		if type(f)==type((1,1)):
			_func=f[0];_arg=f[1]
			if type(_arg)==type((1,1)):_func(*_arg[0],**_arg[1])
			else:_func(_arg)
		else:_func=f;_func()