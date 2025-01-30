from django.shortcuts import render

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from webscraping.models import Webscrape, TaskProgress, TaskHandler, Status

from webscraping.modules.webscraper.classes.SequenceManager import SequenceManager

from datetime import datetime
import time, os

def index(request):
    context = {}
    return render(request, "webscraping/index.html", {})


def webscrape(request):
    context = {}

    from django.core.cache import cache
    import time
    print('----------| cache.set(..., ..., 10s): ', cache.set("glouboudrouda", { "gloubou": "drouda" }, 10 ))
    time.sleep(2)
    print('----------| 2s → cache.get(...: ', cache.get("glouboudrouda" ))
    time.sleep(9)
    print('----------| 11s → cache.get(...: ', cache.get("glouboudrouda" ))
    return render(request, "webscraping/webscrape.html", {})



def webscrape_get_details_from_field_choices(webscrape: Webscrape):
    """        
        __________________________________________________
        Compute task name and task start url from user filled & chosen fields:
        @Update: Not required, generic sequences dictionary for all field combination...
        
        Webscrape variables: (filled field)
        ------------------- 
            - first and last names
            - first and last names, state
            - first and last names, state, city
            - first and last names, state, city
           
        Webscrape site: (choice field)
        --------------
        @ToDo: Turn to choice field...
            - truthfinder.com


        --------------------------------------------
        @ToDo: This must happen before webscrape class instantiation in 
            `webscrape_get_details_from_field_choices(...)` method...

        @Correction: This method is not required in this process, the variable 
                      are obtained from user from interface, not from cli prompt 
        --------------------------------------------
        ```python
            for var_name in variables:
                val = variables[var_name]
                if type(val) == type(lambda x: x):
                    variables[var_name] = val()
        ```

        __________________________________________________
    """            

    # __________________________________________________
    # Compute task name and task start url from user filled & chosen fields:
    pass



def webscrape_long_running_method( webscrape: Webscrape, taskProgress ):
    """
        -----------
        Description:
            See:
            -    tests.integration.test_longrunning_taskhandler
            -    models: TaskHandler, TaskProgress
    """

    progress_value = 0
    taskProgress.set( 
        Status.STARTED, progress_value,
        progress_message=f'The webscrape "{webscrape}" has been started' )

    # input values
    # ------------
    name = webscrape.task_name

    # driver instance
    # ---------------
    options = Options()
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(
        options=options
    )

    # Tasks & progress
    # ----------------
    source_path = "webscraping/modules/webscraper/"

    sequenceManager = SequenceManager(driver, name, os.path.abspath(source_path))

    outputs = []
    sequences_len = len(sequenceManager.sequences)
    for i in range(sequences_len):
        """
            Execution loop sample
            ---------------------
            for i in range( 20 ):
                time.sleep( 0.5 )
                taskProgress.set( Status.RUNNING, progress_message=f"{ 5 * i + 1 }% has been processed" )
        """
        outputs.append(sequenceManager.execute_sequence(variables=webscrape.task_variables, i=0))

        progress_value = int(( i / sequences_len) * 100)

        taskProgress.set( 
            Status.RUNNING, progress_value,
            progress_message=f'Sequence {i} has been processed | Details: {webscrape}' )

        webscrape.task_progress = progress_value
        webscrape.save()


    driver.close()

    """
        sample output:
            f"[{ datetime.now() }] input::{ _input }, outputs::{outputs}"
    """
    output = {
        "datetime": datetime.now(),
        "input": _input,
        "outputs": outputs
    }
    progress_value = 100
    taskProgress.set( Status.SUCCESS, progress_value, output=output )

    webscrape.task_progress = progress_value
    webscrape.task_outputs = "-------ktou##################outk-------".join(outputs)
    webscrape.save()

