_A=None
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver import ChromeOptions
from webscraping.modules.threader.classes.TaskHandler import TaskHandler
from webscraping.modules.threader.classes.TaskProgress import TaskProgress,Status
from webscraping.models import Webscrape,WebscrapeData
from webscraping.modules.webscraper.classes.SequenceManager import SequenceManager
from django_app.settings import logger,_print,PRINT_VERBOSITY
import os,datetime,time,copy,csv,json
BASE_DIR=settings.BASE_DIR
DEBUG=settings.DEBUG
IS_LIVE=settings.IS_LIVE
WEBSCRAPER_HEADLESS=settings.WEBSCRAPER_HEADLESS
def index(request):A={};return render(request,'webscraping/index.html',{})
def webscrape(request):A={};return render(request,'webscraping/webscrape.html',{})
def webscrape_data(request):A={};return render(request,'webscraping/webscrape-data.html',{})
def export_output_to_csv(request,task_run_id=_A,data_id=_A):
	'\n        Exports the output of a specific Webscrape task to a CSV file.\n\n        Args:\n            request (HttpRequest): The HTTP request object.\n            task_run_id (str): The unique ID of the task whose output is to be exported.\n            data_id (str): The unique ID of the data object whose output is to be exported.\n\n        Raises:\n            ValueError: If neither `task_run_id` nor `data_id` is provided.\n\n        Returns:\n            HttpResponse: A CSV file as an HTTP response for download.\n\n        Steps:\n            1. Create an HTTP response object with CSV content type.\n            2. Set the Content-Disposition header to trigger a file download.\n            3. Retrieve the Webscrape object using the provided task_run_id.\n            4. Parse the task_output field (assumed to be JSON) into a Python object.\n            5. Process the parsed output to extract relevant data.\n            6. Write the header row to the CSV file.\n            7. Write the data rows to the CSV file.\n            8. Return the HTTP response with the CSV file.\n\n        Example Usage:\n            - URL: /export-csv/<task_run_id>/\n            - Template: <a href="{% url \'export_csv\' task_run_id=task.id %}">Download CSV</a>\n\n        With:\n            Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025        \n    ';A=data_id;B=task_run_id
	try:
		if not B and not A:raise ValueError('webscraping.Webscrape.parse_output_text :: One of <task_run_id> or <data_id> must be provided...')
		C=[];D,E=_A,_A
		if B:D,E=B,'task';C=Webscrape.data_for_export_output_to_csv(B)
		elif A:D,E=A,'data';C=WebscrapeData.data_for_export_output_to_csv(A)
		F=HttpResponse(content_type='text/csv');F['Content-Disposition']=f'attachment; filename="{E}_{D}_output.csv"';G=C[0].keys();H=csv.writer(F);H.writerow(G)
		for I in C:H.writerow(list(map(lambda x:I[x],G)))
		return F
	except Exception as J:_print('----------------| webscraping.views.export_output_to_csv > Error: %s'%J,VERBOSITY=0);return redirect('error')
def webscrape_steps_long_running_method(webscrape,taskProgress):
	"\n        A long-running method to execute web scraping steps sequentially.\n\n        -----------\n        Description:\n            ! PREFERRED METHOD - see other in archives\n\n            This method executes sequences' steps one bye one, and so \n            it provide task progress handling at step level.\n            To be preferred for Taskprogress handling.\n\n            See:\n            -    tests.integration.test_longrunning_taskhandler\n            -    models: TaskHandler, TaskProgress\n\n        Args:\n            webscrape (Webscrape): The web scraping task model.\n            taskProgress (TaskProgress): The TaskProgress object to track progress.\n    ";N='|||||||||||||||||||||| ALL_STEPS_LEN - N';B=taskProgress;A=webscrape
	def H(key,value):
		if PRINT_VERBOSITY>=3:print(f"-------| webscrape_steps_long_running_method > {key}",value)
	C=0;B.set_unset(Status.STARTED,C,progress_message=f'The webscrape "{A}" has been started');R=A.task_name;S=A.task_variables;H('type(webscrape.task_variables)',type(A.task_variables));H('webscrape.task_variables',A.task_variables);logger.debug('views.webscrape_steps_long_running_method - webscrape.task_variables > : %s '%str(A.task_variables));I=_A;D=FirefoxOptions()
	if IS_LIVE:D=ChromeOptions()
	D.add_argument('--start-maximized');D.add_argument('--disable-infobars');D.add_argument('--disable-extensions');D.add_argument('--disable-application-cache');D.add_argument('--disable-dev-shm-usage');D.add_argument('--no-sandbox')
	if WEBSCRAPER_HEADLESS or IS_LIVE:D.add_argument('--headless')
	if IS_LIVE:D.add_argument('--disable-gpu')
	if IS_LIVE:I=webdriver.Chrome(options=D,service_log_path=os.path.join(str(BASE_DIR),'log/chromedriver.log'))
	else:I=webdriver.Firefox(options=D,service_log_path=os.path.join(str(BASE_DIR),'log/geckodriver.log'))
	T='webscraping/modules/webscraper/';U=SequenceManager(I,R,os.path.abspath(T));G=U.sequenceObjects;X=len(G);J=[];E=0
	for K in range(len(G)):L=G[K];M=L.get_steps();E+=len(M)
	E-=1
	try:
		C=0;F=0
		for K in range(len(G)):
			logger.debug('views.webscrape_steps_long_running_method - i in range(sequenceObjects) > : %i '%K);logger.debug(f"views.webscrape_steps_long_running_method - |||||||||||||||||||||| ALL_STEPS_LEN - N :: {E} - {F}");H(N,f"{E} - {F}");L=G[K];M=L.get_steps()
			for V in range(len(M)):
				O=M[V];J.append(L.execute_step(O,variables=S));C=int(F/E*100)
				if C>=100:C=100
				B.set_unset(Status.RUNNING if C<100 else Status.SUCCESS,C,progress_message=f"Sequence step {F} of {E} has been processed | for: {A}");F+=1;P=False
				if F>=E or(C>=100 or B.status==Status.SUCCESS):B.value=C=100;B.status=Status.SUCCESS;P=True
				A.task_progress=B.value;A.task_status=B.status.value;A.task_output=str(J[-1]);A.save();logger.debug(f"views.webscrape_steps_long_running_method - STEP > : {C}% - {B.status} - {str(O)}");logger.debug(f"views.webscrape_steps_long_running_method - |||||||||||||||||||||| ALL_STEPS_LEN - N :: {E} - {F}");H(N,f"{E} - {F}")
				if P:break
	except Exception as Q:logger.error(f"{datetime.datetime.now()} - views.webscrape_steps_long_running_method - |||||||||||||||||||||| ERROR :: {Q}");B.set_unset(Status.FAILED,C,progress_message=f"An error occured at Sequence step {F} of {E} for: {A} |||||||||||||||||||||| ERROR :: {Q}");A.task_progress=B.value;A.task_status=B.status.value;A.task_output=str(J[-1]);A.save()
	I.close()
	if B.status!=Status.FAILED:W={'datetime':datetime.datetime.now(),'input':A,'outputs':J};B.set_unset(B.status,B.value,progress_message=f"{W}% have been processed");A.task_progress=B.value;A.task_status=B.status.value;A.save()
def parse_raw_outputs():
	'\n        Parses raw output files from a specified directory and returns a list of parsed results.\n\n        Steps:\n            1. Define the output directory using Django settings.\n            2. List all `.txt` files in the output directory.\n            3. Iterate through each file, parse its content using `Webscrape.parse_output_text`,\n               and append the results to a list.\n            4. Handle any exceptions that occur during file parsing.\n            5. Return the aggregated list of parsed results.\n\n        Returns:\n            list: A list of dictionaries, where each dictionary represents a parsed record.\n\n        Example Usage:\n            ```python\n            parsed_results = parse_raw_outputs()\n            for result in parsed_results:\n                print(result)\n            ```\n\n        With:\n            Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025        \n    ';A=os.path.join(settings.BASE_DIR,settings.WEBSCRAPER_SOURCE_PATH,'output');C=list(filter(lambda x:x.endswith('.txt'),os.listdir(A)));B=[];D=0
	for E in C:
		try:F=os.path.join(A,E);G=Webscrape.parse_output_text(file_path=F);B+=G;D+=1
		except Exception as H:print('---------------| webscraping/views > parse_raw_outputs :: Error : ',H)
	return B