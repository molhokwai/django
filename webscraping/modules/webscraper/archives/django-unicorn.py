#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Element:
	driver=None;element=None
	def __init__(A,driver):A.driver=driver
	def find(A,identifier,by=By.ID,timeout=10):B=identifier;print('------| findind "%s"...'%B);A.element=A.driver.find_element(b,B)
	def wait(A,identifier,by=By.ID,timeout=10):B=identifier;print('------| waiting for "%s"...'%B);A.element=WebDriverWait(A.driver,timeout).until(EC.element_to_be_clickable((by,B)))
	def send_keys(A,keys):print('------| sending "%s" to element (keys: %s)...'%(keys,element.__dict__.keys()));A.element.send_keys(keys)
def step1():
	B={'website_url':'https://www.truthfinder.com/','title':'','first_name':'David','last_name':'Jonathan','middle_name':'Henry','middle_initials':'H.','age':55,'city':'New York','state':'NJ','country':'US'};A=webdriver.Chrome();A.get('http://localhost:8001/webscraping/')
	try:
		for C in B:D=Element(A);D.find(C);D.send_keys(B[C])
	except Exception as E:print(f"Error locating or interacting with element: {E}")
	A.quit()
step1()