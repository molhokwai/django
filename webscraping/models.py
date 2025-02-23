_D='truthfinder.sequences/find-person-in-usa.sequence.json'
_C=False
_B=None
_A=True
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.cache import cache
from django.conf import settings
from webscraping.modules.threader.classes.TaskHandler import TaskHandler
from time import sleep
from typing import Union
from datetime import datetime,timedelta
import uuid,copy,json
from uuid import uuid1
from enum import Enum
DEBUG=settings.DEBUG
class Countries(models.TextChoices):'\n        Description\n            Usage\n                view:\n                    ```python\n                        self.countries = list(zip(Countries.values, Countries.names))\n                    ```\n                template:\n                    ```html\n                        <select id="country">\n                            <option>Select a country...</option>\n                            {% for country in countries %}\n                                <option value="{{ country.0 }}">{{ country.1 }}</option>\n                            {% endfor %}\n                        </select>\n                    ```\n    ';CAMEROUN='CM',_('Cameroon');CANADA='CA',_('Canada');FRANCE='FR',_('France');NIGERIA='NG',_('Nigeria');USA='US',_('USA');UK='UK',_('United Kingdom')
class USStates(models.TextChoices):'\n        Description\n            Usage\n                view:\n                    ```python\n                        self.states = list(zip(USStates.values, USStates.names))\n                    ```\n                template:\n                    ```html\n                        <select id="state">\n                            <option>Select a state...</option>\n                            {% for state in states %}\n                                <option value="{{ state.0 }}">{{ state.1 }}</option>\n                            {% endfor %}\n                        </select>\n                    ```\n    ';CALIFORNIA='CA',_('California');FLORIDA='FL',_('Florida');NEW_JERSEY='NJ',_('New Jersey');WASHINGTON='WA',_('Washington');WINSCONSIN='WI',_('Wisconsin')
class WebscrapeTasks(models.TextChoices):'\n        Description\n            Usage\n                view:\n                    ```python\n                        self.webscrape_tasks = list(zip(WebscrapeTasks.values, WebscrapeTasks.names))\n                    ```\n                template:\n                    ```html\n                        <select id="task_name" name="task_name">\n                            <option>Select a webscrape_task...</option>\n                            {% for webscrape_task in webscrape_tasks %}\n                                <option value="{{ webscrape_task.0 }}">{{ webscrape_task.1 }}</option>\n                            {% endfor %}\n                        </select>\n                    ```\n    ';TRUTHFINDER_USA_FIND_A_PERSON=_D,_('TRUTHFINDER - USA: Find a person');AFRSCIENCE_AUTEUR_SOUMETTRE_UN_ARTICLE='afriscience.sequences/auteur-soumettre-un-article.sequence.json',_('AFRISCIENCE - AUTEUR: Soumettre un article')
class WebsiteUrls(models.TextChoices):'\n        Description\n            Usage\n                view:\n                    ```python\n                        self.website_urls = list(\n                            zip(WebsiteUrls.values, WebsiteUrls.names))\n                    ```\n                template:\n                    ```html\n                        <select id="website_url" name="website_url">\n                            <option>Select a website...</option>\n                            {% for website_url in website_urls %}\n                                <option value="{{ website_url.0 }}">{{ website_url.1 }}</option>\n                            {% endfor %}\n                        </select>\n                    ```\n    ';TRUTHFINDER='truthfinder.com','https://www.truthfinder.com';AFRISCIENCE='afriscience.org','https://app.afriscience.org';LOCALHOST='localhost','http://localhost:8001'
class StatusTextChoices(models.TextChoices):RUNNING='RUNNING',_('Running');SUCCESS='SUCCESS',_('Success');FAILED='FAILED',_('Failed');QUEUED='QUEUED',_('Queued');STARTED='STARTED',_('Started')
class WebscrapeTaskNameChoices(models.TextChoices):WEBSCRAPE_STEPS='webscrape_steps_long_running_method','Webscrape detailed process steps long running method...'
class WebscrapeData(models.Model):
	'\n        Model to store web scraping data in a flexible JSON format.\n\n        Fields:\n            - title: A short title for the web scraping task.\n            - description: A detailed description of the task or its purpose.\n            - json_data: A JSON field to store flexible web scraping data.\n            - created_on: The date and time when the record was created.\n            - last_modified: The date and time when the record was last modified.\n\n        Purpose:\n            This model is designed to store web scraping results in a flexible JSON format,\n            allowing for easy storage and retrieval of structured or unstructured data.\n            It can be used to save data such as:\n                - Scraped website content\n                - Metadata about the scraping process\n                - Results of data extraction or transformation\n\n        With:\n            Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025\n    ';title=models.CharField(max_length=200,null=_A,blank=_A,default='Webscraping Task');description=models.TextField(null=_A,blank=_A,default='\n            For scraping data from specified sources and saving the results\n            in a structured JSON format. The data may include:\n                - Extracted text, images, or links\n                - Metadata about the scraping process\n                - Results of data transformation or analysis\n            The JSON format allows for flexible storage and easy retrieval of the scraped data.\n        ');json_data=models.JSONField(null=_A,blank=_A,default=dict,help_text='Flexible JSON field to store web scraping results.');created_on=models.DateTimeField(auto_now_add=_A);last_modified=models.DateTimeField(auto_now=_A)
	def __str__(A):'\n        String representation of the model instance.\n        ';return f"{A.title} (Created: {A.created_on})"
	def save(A,*B,**C):
		'\n        Override the save method to ensure JSON data is properly formatted.\n        '
		if isinstance(A.json_data,str):
			try:A.json_data=json.loads(A.json_data)
			except json.JSONDecodeError:A.json_data={}
		super().save(*B,**C)
	@staticmethod
	def periodic_save_aggregated_results(aggregated_results):
		'\n            Periodically saves aggregated results to the WebscrapeData model if the last modification\n            was more than 1 hour ago.\n\n            Args:\n                aggregated_results (dict): The aggregated results to save.\n\n            Steps:\n                1. Retrieve the first WebscrapeData instance from the database.\n                2. If no instance exists, create a new one.\n                3. Calculate the time difference between the current time and the last modification time.\n                4. If the time difference is greater than or equal to 1 hour, update the json_data field\n                   and save the instance.\n\n            With:\n                Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025        \n        ';B=aggregated_results;A=WebscrapeData.objects.first()
		if not A:A=WebscrapeData(title='Aggregated Results',description='Automatically saved aggregated results.',json_data=B);A.save()
		C=datetime.now();D=C-A.last_modified.replace(tzinfo=_B)
		if D.total_seconds()>=3600:A.json_data=B;A.save()
	@staticmethod
	def data_for_export_output_to_csv(data_id):A=WebscrapeData.objects.get(id=data_id);print('-------------------------------| webscrapeData.json_data',A.json_data);return A.json_data
class ThreadTask(models.Model):
	'\n        Parent class for all Thread Tasks models.\n        ----------------------------------------\n        @ToDo :: Implement actual inheritance, checking and adjusting\n                 for databases interpretation: sqlite, Postgres, MySQL... \n    ';task_title=models.CharField(max_length=200,null=_A,blank=_A);task_run_id=models.CharField(max_length=50,null=_A,blank=_A);task_progress=models.IntegerField(default=0);task_status=models.CharField(max_length=20,null=_A,blank=_A,choices=StatusTextChoices.choices);task_output=models.TextField(null=_A,blank=_A);task_thread_started_at=models.DateTimeField(null=_A,blank=_A);task_thread_stopped_at=models.DateTimeField(null=_A,blank=_A);task_attempts=models.IntegerField(default=0);created_on=models.DateTimeField(auto_now_add=_A);last_modified=models.DateTimeField(auto_now=_A)
	def __str__(A):return f"title: {A.task_title} - run_id: {A.task_run_id} - progress: {A.task_progress} - attempts: {A.task_attempts}"
	def save(C,*A,**B):super().save(*A,**B)
	def update_ended_task_status(A):
		"\n            Description\n            -----------\n            If the task is not running anymore and not at 100% with SUCCESS status, marked as failed...\n            -    Get webscrape's Taskhandler TaskProgess object\n            -    If existing:\n                 *    Do nothing, task still running, to be updated\n                 *    If not:\n                     +    Check if webscrape at 100% with SUCCESS status\n                         -    If not:\n                             *    Change task_status to FAILED\n\n            ----------------------------\n            **The Task Lifecycle**\n\n            1.  Task is requested from ui frontend, either as individual, or in batch\n            2.  Task is sent to be queued in corresponding uip backend (manage_*.py)\n            3.  Task is mark as queued in uip backend webscrape.py\n            3.  Task is dequeued by Taskhandler when its time comes\n            4.  Task runs, and:\n                - is marked as succesfull in long running view function when succeeds\n                - is marked as failed in long running view function if fails\n\n            5.  Task is picked and queued in uip backend (table.py) if:\n                - not succesful\n                - not queued\n                - and nr of max attempts not reached...\n            6.  Task if checked for timeout, hanging... in model. If:\n                - Task has no taskProgress \n                - Task is not marked as successful or task_progress not = 100 \n                Task is marked as failed\n        ";B=TaskHandler.get_taskProgress(A.task_run_id)
		if not B:
			if A.task_progress>=100 and A.task_status!=StatusTextChoices.SUCCESS.value:A.task_status=StatusTextChoices.SUCCESS.value;A.save()
			if A.task_progress<=100 and A.task_status!=StatusTextChoices.FAILED.value:A.task_status=StatusTextChoices.FAILED.value;A.save()
class Webscrape(models.Model):
	'\n        Inherits from TaskThread\n        ----------------------------------------\n        @ToDo :: Implement actual inheritance, checking and adjusting\n                 for databases interpretation: sqlite, Postgres, MySQL... \n    ';website_url=models.CharField(max_length=200,choices=WebsiteUrls.choices,default='https://www.truthfinder.com/');title=models.CharField(max_length=200,null=_A,blank=_A);task_title=models.CharField(max_length=200,null=_A,blank=_A);task_run_id=models.CharField(max_length=50,null=_A,blank=_A);task_progress=models.IntegerField(default=0);task_status=models.CharField(max_length=20,null=_A,blank=_A,choices=StatusTextChoices.choices);task_output=models.TextField(null=_A,blank=_A);task_thread_started_at=models.DateTimeField(null=_A,blank=_A);task_thread_stopped_at=models.DateTimeField(null=_A,blank=_A);task_attempts=models.IntegerField(default=0);task_name=models.CharField(max_length=200,null=_C,blank=_C,choices=WebscrapeTasks.choices,default=_D);task_variables=models.JSONField(max_length=200,null=_A,blank=_A);task_todo=models.CharField(max_length=100,null=_A,blank=_A,choices=WebscrapeTaskNameChoices.choices,help_text='The task to be performed for this web scraping job.');firstName=models.CharField(max_length=200,null=_C,blank=_C);lastName=models.CharField(max_length=200,null=_C,blank=_C);middleName=models.CharField(max_length=200,null=_A,blank=_A);middleInitial=models.CharField(max_length=6,null=_A,blank=_A);age=models.IntegerField(null=_A,blank=_A);by_list=models.TextField(null=_A,blank=_A);city=models.CharField(null=_A,blank=_A,max_length=200);state=models.CharField(null=_A,blank=_A,max_length=2,choices=USStates.choices);country=models.CharField(null=_A,blank=_A,max_length=2,choices=Countries.choices,default='US');parent=models.ForeignKey('Webscrape',null=_A,blank=_A,on_delete=models.CASCADE,related_name='webscrape_children',editable=_C);created_on=models.DateTimeField(auto_now_add=_A);last_modified=models.DateTimeField(auto_now=_A)
	def __str__(A):return f"{A.website_url} - {A.title} - task: {A.task_name} - variables: {A.task_variables}"
	def save(C,*A,**B):super().save(*A,**B)
	def update_ended_task_status(A):
		"\n            Description\n                Parent method call\n                ------------------\n                If the task is not running anymore and not at 100% with SUCCESS status, marked as failed...\n                -    Get webscrape's Taskhandler TaskProgess object\n                -    If existing:\n                     *    Do nothing, task still running, to be updated\n                     *    If not:\n                         +    Check if webscrape at 100% with SUCCESS status\n                             -    If not:\n                                 *    Change task_status to FAILED\n\n                Self method steps\n                ------------------\n                Update the tasks by_list corresponding [firtName] [lastName] line items:\n                -   parent tasks: task has by_list, update items\n                -   child task: task has parent, get parent's by_list and update items\n                -   save: save only if changed\n\n    \n                ----------------------------\n                **The Task Lifecycle**\n\n                1.  Task is requested from ui frontend, either as individual, or in batch\n                2.  Task is sent to be queued in corresponding uip backend (manage_*.py)\n                3.  Task is mark as queued in uip backend webscrape.py\n                3.  Task is dequeued by Taskhandler when its time comes\n                4.  Task runs, and:\n                    - is marked as succesfull in long running view function when succeeds\n                    - is marked as failed in long running view function if fails\n\n                5.  Task is picked and queued in uip backend (table.py) if:\n                    - not succesful\n                    - not queued\n                    - and nr of max attempts not reached...\n                6.  Task if checked for timeout, hanging... in model. If:\n                    - Task has no taskProgress \n                    - Task is not marked as successful or task_progress not = 100 \n                    Task is marked as failed\n        ";F=TaskHandler.get_taskProgress(A.task_run_id)
		if not F:
			if A.task_progress>=100 and A.task_status!=StatusTextChoices.SUCCESS.value:A.task_status=StatusTextChoices.SUCCESS.value;A.save()
			if A.task_progress<=100 and A.task_status!=StatusTextChoices.FAILED.value:A.task_status=StatusTextChoices.FAILED.value;A.save()
		def G(lines,name):
			B=list(filter(lambda x:x.find(f"{A.firstName} {A.lastName}")>=0,lines))
			if len(B):return B[0]
		def D(by_list,name,token):A=by_list.splitlines();B=G(A,firstName,lastName);return B.find(token)>0
		def E(by_list,name,token):return by_list.replace(name,f"{name} {token}")
		C=f"{A.firstName} {A.lastName}";B=''
		if A.task_status==StatusTextChoices.SUCCESS.value:B='✓';A.task_queue=_B
		else:B='✗'
		if A.by_list and A.task_status in(StatusTextChoices.SUCCESS.value,StatusTextChoices.FAILED.value):
			if not D(A.by_list,C,B)>0:A.by_list=E(A.by_list,C,B);A.save()
		if A.parent:
			if not D(A.by_list,C,B)>0:A.parent.by_list=E(A.parent.by_list,C,B);A.save()
	@staticmethod
	def parse_output_text(text='',file_path='',start_line=8):
		'\n            Parses the output text or file content into a list of dictionaries.\n\n            Args:\n                text (str, optional): The text to parse. Defaults to \'\'.\n                file_path (str, optional): The path to the file containing the text to parse. Defaults to \'\'.\n                start_line (int, optional): The line number from which to start parsing. Defaults to 8.\n\n            Returns:\n                list: A list of dictionaries, where each dictionary represents a parsed record.\n\n            Raises:\n                ValueError: If neither `text` nor `file_path` is provided.\n\n            Steps:\n                1. Define a template for the result dictionary.\n                2. Read lines from the provided text or file.\n                3. Clean and filter the lines to remove unwanted content.\n                4. Parse the cleaned lines into dictionaries using the result template.\n                5. Return the list of parsed dictionaries.\n\n            Example Usage:\n                ```python\n                text = "Name: John Doe\nAge: 30\nLocation: New York"\n                parsed_data = Webscrape.parse_output_text(text=text)\n                print(parsed_data)\n                ```\n\n            With:\n                Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025        \n        ';H='CRIMINAL_RECORDS';I='VERIFIED';J='AGE';K=file_path;F='NAME';G=text;D='POSSIBLE_RELATIVES';E='LOCATION';L={F:_B,J:_B,E:_B,D:_B,I:_B,H:_B}
		def N(file):
			'Reads lines from a file.'
			with open(file)as A:return A.readlines()
		A=[]
		if not G and not K:raise ValueError('webscraping.Webscrape.parse_output_text :: One of <text> or <file_path> must be provided...')
		elif G:A=G.splitlines()
		else:A=N(K)
		A=list(map(lambda x:x.replace('\n','').replace('\t',''),A));A=list(filter(lambda x:x.find('We could uncover')<0,A));A=list(filter(lambda x:x.find('OPEN REPORT')<0,A));A=list(filter(lambda x:x.find('ⓘ')<0,A));A=A[start_line:];M=[];B=copy.copy(L)
		for C in A:
			if len(C)>=2:
				if C.find('Based on your input')>=0:M.append(B);B=copy.copy(L)
				elif C.find('Possible Criminal or Traffic')>=0:B[H]=_A
				elif C.lower().find('verified')>=0:B[I]=_A
				elif C.lower().find(',')>=0:
					if not B[E]:B[E]=[]
					B[E].append(C)
				elif len(C)==2:B[J]=C
				elif not B[F]:B[F]=C
				else:
					if not B[D]:B[D]=[]
					B[D].append(C)
		return M
	@staticmethod
	def data_for_export_output_to_csv(task_run_id):B=Webscrape.objects.get(task_run_id=task_run_id);A=B.task_output;A=A.replace("'",'"').replace('\\xa0','');C=json.loads(A);A=C[0]['returned'];D=Webscrape.parse_output_text(A,start_line=0);return D