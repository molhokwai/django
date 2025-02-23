#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Element:
	element=None
	def wait(B,identifier,by=By.NAME,timeout=10):A=identifier;print('------| waiting for %s...'%A);B.element=WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((by,A)))
	def send_keys(A,keys):print('------| sending %s to element (keys: %s)...'%(keys,element.__dict__.keys()));A.element.send_keys(keys)
def step1():
	A=webdriver.Chrome();A.get('https://www.truthfinder.com/people-search/')
	try:B=Element().wait('firstName');B.send_keys('David')
	except Exception as C:print(f"Error locating or interacting with element: {C}")
	A.quit()
step1()