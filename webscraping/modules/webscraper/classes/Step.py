#!/usr/bin/env python3
_L='[input]'
_K='By.CSS_SELECTOR'
_J='By.NAME'
_I='step_dicts'
_H='find'
_G='[variable]'
_F='variables'
_E='send_keys'
_D='asserts'
_C='returned'
_B='element'
_A=None
from django_app.settings import _print
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
if sys.version_info[0]<3:from StringIO import StringIO
else:from io import StringIO
from django.utils.text import slugify
import os,datetime,time
class Step:
	class Config:ui_timeout=0
	config:Config=_A;step_dicts=[];outputs=[];steps_common={_D:[]};step_dict_keys_excluded='config',_I,_F;variables={};source_path=_A
	def __init__(A,driver,config_dict=_A):
		B=config_dict;A.driver=driver;A.config=Step.Config()
		if B:
			for C in B:setattr(A.config,C,B[C])
	def execute(A,step_dict,_input=_A):
		'\n            List of step functions:\n                assert_in_input\n                assert_in_page_source\n                clear\n                find\n                get\n                get_attribute\n                print OK\n                print TEXT\n                send_keys\n                text_to_csv\n                wait\n        ';C=step_dict;A.step_dicts.append(C);A.outputs=[]
		for B in C.keys():
			if B in dir(A)and not B in A.step_dict_keys_excluded:_print('----------| %s %s '%(B,C[B]),VERBOSITY=3);A.outputs.append(getattr(A,B)(C,_input if not len(A.outputs)else A.outputs[-1]))
		return A.outputs
	@staticmethod
	def _by(by_string):A={'By.ID':By.ID,_J:By.NAME,_K:By.CSS_SELECTOR}.get(by_string,ValueError('by_string not yet implemented in webscraping.modules.webscraper.classes.Step.by'));return A
	@staticmethod
	def dom_get_by(by_string):A={'By.ID':"document.getElementById('%s')",_J:"document.getElementsByName('%s')[0]",_K:"document.querySelector('%s')"}.get(by_string);return A
	def _keys(C,keys_string):'\n            @ToDo :: Use reflection instead, with ValueError if Keys.(.*) ...\n                ValueError("keys_string not yet implemented in "\n                        "webscraping.modules.webscraper.classes.Step.keys")\n        ';A=keys_string;B={'Keys.RETURN':Keys.RETURN,'Keys.SPACE':Keys.SPACE}.get(A,A);return B
	def input_keys(A,keys_string,_key=_A):'\n            @ToDo :: Fix [user_input] ... ?\n            Usage:\n                [variable]\n                    { "send_keys": "[variable]", "key": "..." }\n                    ___________\n                    Description:\n                        The variable will be fetched from the\n                        variables dict attribute of the step by\n                        the key provided in the config line above\n        ';B={'[user_input]':lambda _key:input('Enter value: '),_G:lambda _key:A.variables[_key]}.get(keys_string)(_key);return B
	def assert_in_driver_title(B,step_dict,_input):A=_input;C=step_dict['assert_in_driver_title'];assert C in B.driver.title;B.steps_common[_D].append(f"assert {C} in self.driver.title");return A if type(A)==type({})else A[0]
	def assert_in_input(D,step_dict,_input,_not=False):
		E=step_dict;A=_input;B=_A;A=A if type(A)==type({})else A[0];C=A[_C]if _C in A else D.driver.page_source
		if _not:B=E['assert_not_in_input'];assert B not in C
		else:B=E['assert_in_input'];assert B in C
		F='not'if _not else'';D.steps_common[_D].append(f"assert {B} {F} in {C}");return{_C:C}
	def assert_in_page_source(B,step_dict,_input,_not=False):
		F='placeholder_variables';D=_input;C=step_dict;E={}
		if F in C:
			for G in C[F]:E[G]=B.variables[G]
		A=_A
		if _not:A=C['assert_not_in_page_source']%E;assert A not in B.driver.page_source,f'Error "{A}" in source...'
		else:A=C['assert_in_page_source']%E;assert A.lower()in B.driver.page_source.lower(),f'Error "{A.lower()}" not in source...'
		H='not'if _not else'';B.steps_common[_D].append(f"assert {A} {H} in self.driver.page_source");return D if type(D)==type({})else D[0]
	def assert_not_in_input(B,step_dict,_input):A=_input;A=A if type(A)==type({})else A[0];return B.assert_in_input(step_dict,A,_not=True)
	def assert_not_in_page_source(B,step_dict,_input):A=_input;A=A if type(A)==type({})else A[0];return B.assert_in_page_source(step_dict,A,_not=True)
	def clear(C,step_dict,_input):A=_input;time.sleep(C.config.ui_timeout);A=A if type(A)==type({})else A[0];B=A[_B];B.clear();return{_B:B}
	def click(B,step_dict,_input):
		G='scrollIntoView';D=step_dict;A=_input;time.sleep(B.config.ui_timeout);E=_A;A=A if type(A)==type({})else A[0]if len(A)else A
		if type(A)==type({})and _B in A:
			E=A[_B]
			if E:
				C=B.step_dicts[-2];H=C[_H]if _H in C else C['wait'];I=C['by'];F=Step.dom_get_by(I)%H
				if G in D and D[G]:B.driver.execute_script(f"{F}.style.zIndex = 1000; {F}.scrollIntoView();")
				if D['click']=='Left':B.driver.execute_script(f"{F}.click();")
		return{_B:E}
	def find(B,step_dict,_input):A=step_dict;C=B.driver.find_element(Step._by(A['by']),A[_H]);return{_B:C}
	def get(A,step_dict,_input):A.driver.get(step_dict['get'])
	def get_attribute(B,step_dict,_input):A=_input[0][_B].get_attribute(step_dict['get_attribute']);return{_C:A}
	def print_OK(B,step_dict,_input):A=_input;C='\n'.join(B.steps_common[_D]);print(f"\n            ------------ OK ----------------\n            {C}\n            --------------------------------\n        ");return A if type(A)==type({})else A[0]
	def print_TEXT(B,step_dict,_input):
		A=_input;A=A if type(A)==type({})else A[0]
		if step_dict['print_TEXT']=='input':print(f"\n                ------------ TEXT --------------\n                {A[_C][200:]}\n                --------------------------------\n            ")
		return A if type(A)==type({})else A[0]
	def repeat(C,step_dict,_input):
		B=step_dict;D=B['repeat'];E=B[_I];A=_input
		for G in range(D):
			for F in E:A=C.execute(F,A)
		return A
	def select(B,step_dict,_input):
		'\n            @ToDo\n\n            ],[\n                { "find": "state", "by": "By.NAME"  },\n                { "select": "ALL", "key": "state", "function": "select_state" },\n                { "select": "[variable]", "key": "state", "function": "select_state" }\n        ';E=step_dict;A=_input;time.sleep(B.config.ui_timeout);A=A if type(A)==type({})else A[0];C=E[_E];D=''
		if C==_L:D=B.input_keys(C)
		elif E[_E]==_G:F=E['key'];D=B.input_keys(C,_key=F)
		else:D=B._keys(C)
		A[_B].send_keys(D);return A if type(A)==type({})else A[0]
	def send_keys(C,step_dict,_input):
		E=step_dict;A=_input;time.sleep(C.config.ui_timeout);A=A if type(A)==type({})else A[0];D=E[_E];B=''
		if D==_L:B=C.input_keys(D)
		elif E[_E]==_G:F=E['key'];B=C.input_keys(D,_key=F)
		else:B=C._keys(D)
		if B:A[_B].send_keys(B)
		return A if type(A)==type({})else A[0]
	def set_var(B,step_dict,_input):A=_input;time.sleep(B.config.ui_timeout);A=A if type(A)==type({})else A[0];C=step_dict['set_var'];B.variables[C]=A[_C];return A if type(A)==type({})else A[0]
	def text_to_csv(D,step_dict,_input):
		F='text_to_csv';B=step_dict;A=_input;A=A if type(A)==type({})else A[0];C=_A
		if B[F]==_F:
			C=''
			for G in B[_F]:C+='\n'+D.variables[G]
		elif B[F]=='input':C=A[_C]
		H=datetime.datetime.now();I=os.path.join(D.source_path,B['folderpath'],slugify(f"{H}-{B["filename"]}"));E=''
		if True:
			E=f"{I}.txt"
			with open(E,'w')as J:J.write(C)
		D.outputs.append(E);return A if type(A)==type({})else A[0]
	def wait(E,step_dict,_input):
		C='optional';A=step_dict;D=_A
		try:D=WebDriverWait(E.driver,A['timeout']).until(EC.element_to_be_clickable((Step._by(A['by']),A['wait'])))
		except TimeoutException as B:
			if C in A and A[C]:print('----------| Optional field - TimeoutException: ',B)
			else:print('----------| Non optional field - TimeoutException: ',B);raise B
		return{_B:D}