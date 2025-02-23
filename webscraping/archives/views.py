_L='views.webscrape_steps_long_running_method - i in range(sequenceObjects) > : %i '
_K='webscraping/modules/webscraper/'
_J='views.webscrape_steps_long_running_method - webscrape.task_variables > : %s '
_I='webscrape.task_variables'
_H='type(webscrape.task_variables)'
_G='outputs'
_F='input'
_E='datetime'
_D='--no-sandbox'
_C='--disable-gpu'
_B='--headless'
_A=None
from django.shortcuts import render
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from webscraping.models import Webscrape,TaskProgress,TaskHandler,Status
from webscraping.modules.webscraper.classes.SequenceManager import SequenceManager
from django_app.settings import logger,_print,PRINT_VERBOSITY
import os,datetime,time,copy
DEBUG=settings.DEBUG
IS_LIVE=settings.IS_LIVE
def index(request):A={};return render(request,'webscraping/index.html',{})
def webscrape(request):A={};return render(request,'webscraping/webscrape.html',{})
def webscrape_data(request):A={};return render(request,'webscraping/webscrape-data.html',{})
def webscrape_get_details_from_field_choices(webscrape):'        \n        __________________________________________________\n        Compute task name and task start url from user filled & chosen fields:\n        @Update: Not required, generic sequences dictionary for all field combination...\n        \n        Webscrape variables: (filled field)\n        ------------------- \n            - first and last names\n            - first and last names, state\n            - first and last names, state, city\n            - first and last names, state, city\n           \n        Webscrape site: (choice field)\n        --------------\n        @ToDo: Turn to choice field...\n            - truthfinder.com\n\n\n        --------------------------------------------\n        @ToDo: This must happen before webscrape class instantiation in \n            `webscrape_get_details_from_field_choices(...)` method...\n\n        @Correction: This method is not required in this process, the variable \n                      are obtained from user from interface, not from cli prompt \n        --------------------------------------------\n        ```python\n            for var_name in variables:\n                val = variables[var_name]\n                if type(val) == type(lambda x: x):\n                    variables[var_name] = val()\n        ```\n\n        __________________________________________________\n    '
def webscrape_sequence_long_running_method(webscrape,taskProgress):
	"\n        -----------\n        Description:\n            ! NOT PREFERRED METHOD\n\n            This method executes a full sequences' step, and so \n            does not provide task progress handling at step level.            \n            To eventually be used for Taskprogress handling only for tasks with \n            multiple sequences.\n\n            See:\n            -    tests.integration.test_longrunning_taskhandler\n            -    models: TaskHandler, TaskProgress\n    ";C=taskProgress;A=webscrape
	def J(key,value):
		if PRINT_VERBOSITY>=3:print(f"-------| webscrape_sequence_long_running_method > {key}",value)
	B=0;C.set_unset(Status.STARTED,B,progress_message=f'The webscrape "{A}" has been started');K=A.task_name;D=Options()
	if not DEBUG:D.add_argument(_B);D.add_argument(_C);D.add_argument(_D)
	G=webdriver.Firefox(options=D);L=settings.WEBSCRAPER_SOURCE_PATH;H=SequenceManager(G,K,os.path.abspath(L));I=len(H.sequences)
	for E in range(I):
		J('i in range(sequences_len)',E);F=H.execute_sequence(variables=A.task_variables,i=0);B=int(E/I*100)
		if B>=100:B=100
		C.set_unset(Status.RUNNING if B<100 else Status.SUCCESS,B,progress_message=f"Sequence {E} has been processed | Details: {A}",output=F);A.task_progress=B;A.task_status=C.status;A.task_outputs=C.outputs;A.save()
		if B>=100 or C.status==Status.SUCCESS:break
	G.close();F={_E:datetime.datetime.now(),_F:A,_G:outputs};B=100;C.set_unset(Status.SUCCESS,B,progress_message=f"{F}% have been processed");A.task_progress=B;processObj.task_status=C.status;A.save()
def webscrape_steps_long_running_method(webscrape,taskProgress):
	"\n        A long-running method to execute web scraping steps sequentially.\n\n        -----------\n        Description:\n            ! PREFERRED METHOD\n\n            This method executes sequences' steps one bye one, and so \n            it provide task progress handling at step level.\n            To be preferred for Taskprogress handling.\n\n            See:\n            -    tests.integration.test_longrunning_taskhandler\n            -    models: TaskHandler, TaskProgress\n\n        Args:\n            webscrape (Webscrape): The web scraping task model.\n            taskProgress (TaskProgress): The TaskProgress object to track progress.\n    ";C=taskProgress;A=webscrape
	def J(key,value):
		if PRINT_VERBOSITY>=3:print(f"-------| webscrape_steps_long_running_method > {key}",value)
	B=0;C.set_unset(Status.STARTED,B,progress_message=f'The webscrape "{A}" has been started');O=A.task_name;P=A.task_variables;J(_H,type(A.task_variables));J(_I,A.task_variables);logger.debug(_J%str(A.task_variables));F=Options()
	if IS_LIVE:F.add_argument(_B)
	if IS_LIVE:F.add_argument(_C)
	else:F.add_argument(_D)
	M=webdriver.Firefox(options=F);Q=_K;R=SequenceManager(M,O,os.path.abspath(Q));D=R.sequenceObjects;U=len(D);K=[];L=0
	for E in range(len(D)):G=D[E];H=G.get_steps();L+=len(H)
	I=0
	for E in range(len(D)):
		J('i in range(sequenceObjects)',E);logger.debug(_L%E);G=D[E];H=G.get_steps()
		for S in range(len(H)):
			N=H[S];K.append(G.execute_step(N,variables=P));B=int(I/L*100)
			if B>=100:B=100
			C.set_unset(Status.RUNNING if B<100 else Status.SUCCESS,B,progress_message=f"Sequence step {I} of {L} has been processed | for: {A}");A.task_progress=B;A.task_status=C.status;A.task_output=str(K[-1]);A.save();logger.debug(f"views.webscrape_steps_long_running_method - STEP > : {B}% - {C.status} - {str(N)}")
			if B>=100 or C.status==Status.SUCCESS:break
			I+=1
		I+=1
	M.close();T={_E:datetime.datetime.now(),_F:A,_G:K};B=100;C.set_unset(Status.SUCCESS,B,progress_message=f"{T}% have been processed");A.task_progress=B;processObj.task_status=C.status;A.save()
def parse_raw_outputs():
	G='CRIMINAL_RECORDS';H='VERIFIED';I='AGE';F='NAME';D='POSSIBLE_RELATIVES';E='LOCATION'
	def M(file):
		with open(file)as A:return A.readlines()
	J=os.path.join(settings.BASE_DIR,settings.WEBSCRAPER_SOURCE_PATH,'output');K={F:_A,I:_A,E:_A,D:_A,H:_A,G:_A};N=list(filter(lambda x:x.endswith('.txt'),os.listdir(J)));R='Based on your input we have selected the best result for you';L=[];O=0
	for P in N:
		try:
			B=M(os.path.join(J,P));B=list(map(lambda x:x.replace('\n','').replace('\t',''),B));B=list(filter(lambda x:x.find('We could uncover')<0,B));B=list(filter(lambda x:x.find('OPEN REPORT')<0,B));B=list(filter(lambda x:x.find('ⓘ')<0,B));B=B[8:];A=copy.copy(K)
			for C in B:
				if len(C)>=2:
					if C.find('Based on your input')>=0:L.append(A);A=copy.copy(K)
					elif C.find('Possible Criminal or Traffic')>=0:A[G]=True
					elif C.lower().find('verified')>=0:A[H]=True
					elif C.lower().find(',')>=0:
						if not A[E]:A[E]=[]
						A[E].append(C)
					elif len(C)==2:A[I]=C
					elif not A[F]:A[F]=C
					else:
						if not A[D]:A[D]=[]
						A[D].append(C)
			O+=1
		except Exception as Q:print('---------------| webscraping/views > parse_raw_outputs :: Error : ',Q)
	return L
def Xwebscrape_steps_long_running_method(webscrape):
	"\n        A long-running method to execute web scraping steps sequentially.\n\n        -----------\n        Description:\n            ! PREFERRED METHOD - see other in archives\n\n            This method executes sequences' steps one bye one, and so \n            it provide task progress handling at step level.\n            To be preferred for Taskprogress handling.\n\n            See:\n            -    tests.integration.test_longrunning_taskhandler\n            -    models: TaskHandler, TaskProgress\n\n        Args:\n            webscrape (Webscrape): The web scraping task model.\n    ";M='|||||||||||||||||||||| ALL_STEPS_LEN - N';A=webscrape
	def F(key,value):
		if PRINT_VERBOSITY>=0:print(f"-------| webscrape_steps_long_running_method > {key}",value)
	B=0;P=A.task_name;Q=A.task_variables;F(_H,type(A.task_variables));F(_I,A.task_variables);logger.debug(_J%str(A.task_variables));H=Options()
	if IS_LIVE:H.add_argument(_B)
	if IS_LIVE:H.add_argument(_C)
	else:H.add_argument(_D)
	N=webdriver.Firefox(options=H);R=_K;S=SequenceManager(N,P,os.path.abspath(R));G=S.sequenceObjects;V=len(G);L=[];C=0
	for I in range(len(G)):J=G[I];K=J.get_steps();C+=len(K)
	D=0;B=0;E=_A
	for I in range(len(G)):
		logger.debug(_L%I);logger.debug(f"views.webscrape_steps_long_running_method - |||||||||||||||||||||| ALL_STEPS_LEN - N :: {C} - {D}");F(M,f"{C} - {D}");J=G[I];K=J.get_steps()
		for T in range(len(K)):
			O=K[T];L.append(J.execute_step(O,variables=Q));B=int(D/C*100)
			if B>=100:B=100
			E=Status.RUNNING if B<100 else Status.SUCCESS;U=f"Sequence step {D} of {C} has been processed | for: {A}";F('progress_message',U);A.task_progress=B;A.task_status=E;A.task_output=str(L[-1]);A.save();logger.debug(f"views.webscrape_steps_long_running_method - STEP > : {B}% - {E} - {str(O)}");D+=1
			if D>=C:B=100;E=Status.SUCCESS.value
			logger.debug(f"views.webscrape_steps_long_running_method - |||||||||||||||||||||| ALL_STEPS_LEN - N :: {C} - {D}");F(M,f"{C} - {D}")
			if B>=100 or E==Status.SUCCESS.value:break
	N.close();W={_E:datetime.datetime.now(),_F:A,_G:L};A.task_progress=B;A.task_status=E;A.save()