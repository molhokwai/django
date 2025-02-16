from django.shortcuts import render
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from webscraping.models import Webscrape, TaskProgress, TaskHandler, Status

from webscraping.modules.webscraper.classes.SequenceManager import SequenceManager

from django_app.settings import logger, _print, PRINT_VERBOSITY

import os, datetime, time, copy

DEBUG = settings.DEBUG
IS_LIVE = settings.IS_LIVE


def index(request):
    context = {}
    return render(request, "webscraping/index.html", {})


def webscrape(request):
    context = {}
    return render(request, "webscraping/webscrape.html", {})


def webscrape_data(request):
    context = {}
    return render(request, "webscraping/webscrape-data.html", {})



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


def webscrape_sequence_long_running_method( webscrape: Webscrape, taskProgress ):
    """
        -----------
        Description:
            ! NOT PREFERRED METHOD

            This method executes a full sequences' step, and so 
            does not provide task progress handling at step level.            
            To eventually be used for Taskprogress handling only for tasks with 
            multiple sequences.

            See:
            -    tests.integration.test_longrunning_taskhandler
            -    models: TaskHandler, TaskProgress
    """
    def _print(key, value):
        if PRINT_VERBOSITY >= 3:
            print(f'-------| webscrape_sequence_long_running_method > {key}', value)


    progress_value = 0
    taskProgress.set_unset( 
        Status.STARTED, progress_value,
        progress_message=f'The webscrape "{webscrape}" has been started' )

    # input values
    # ------------
    name = webscrape.task_name

    # driver instance
    # ---------------
    options = Options()
    if not DEBUG:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

    driver = webdriver.Firefox(
        options=options
    )

    # Tasks & progress
    # ----------------
    source_path = settings.WEBSCRAPER_SOURCE_PATH

    sequenceManager = SequenceManager(driver, name, os.path.abspath(source_path))

    sequences_len = len(sequenceManager.sequences)
    for i in range(sequences_len):
        _print("i in range(sequences_len)", i)

        output = sequenceManager.execute_sequence(variables=webscrape.task_variables, i=0)

        progress_value = int(( i / sequences_len) * 100)
        if progress_value >= 100:
            progress_value = 100

        taskProgress.set_unset( 
            Status.RUNNING if progress_value < 100 else Status.SUCCESS,
            progress_value,
            progress_message=f'Sequence {i} has been processed | Details: {webscrape}',
            output = output)

        webscrape.task_progress = progress_value
        webscrape.task_status = taskProgress.status
        webscrape.task_outputs = taskProgress.outputs
        webscrape.save()

        if progress_value >= 100 or taskProgress.status == Status.SUCCESS.value:
            break

    # driver instance
    # ---------------
    driver.close()

    output = {
        "datetime": datetime.datetime.now(),
        "input": webscrape,
        "outputs": outputs
    }
    
    progress_value = 100
    taskProgress.set_unset(
        Status.SUCCESS, progress_value,
        progress_message=f"{output}% have been processed" )

    webscrape.task_progress = progress_value
    processObj.task_status = taskProgress.status
    webscrape.save()



def webscrape_steps_long_running_method( webscrape: Webscrape, taskProgress ):
    """
        A long-running method to execute web scraping steps sequentially.

        -----------
        Description:
            ! PREFERRED METHOD

            This method executes sequences' steps one bye one, and so 
            it provide task progress handling at step level.
            To be preferred for Taskprogress handling.

            See:
            -    tests.integration.test_longrunning_taskhandler
            -    models: TaskHandler, TaskProgress

        Args:
            webscrape (Webscrape): The web scraping task model.
            taskProgress (TaskProgress): The TaskProgress object to track progress.
    """
    def _print(key, value):
        if PRINT_VERBOSITY >= 3:
            print(f'-------| webscrape_steps_long_running_method > {key}', value)


    progress_value = 0
    taskProgress.set_unset( 
        Status.STARTED, progress_value,
        progress_message=f'The webscrape "{webscrape}" has been started' )

    # ------------
    # input values
    # ------------
    name = webscrape.task_name
    variables = webscrape.task_variables
    _print('type(webscrape.task_variables)', type(webscrape.task_variables))
    _print('webscrape.task_variables', webscrape.task_variables)
    logger.debug(
        "views.webscrape_steps_long_running_method - webscrape.task_variables > : %s " \
                                                        % str(webscrape.task_variables))

    # ---------------
    # driver instance create
    # ---------------
    options = Options()
    if IS_LIVE:
        # ----------------------------------------
        # Do not show browser (= headless) live...
        # remove True for showing browser locally
        options.add_argument("--headless")

    if IS_LIVE:
        # -------------------------
        # Disable GPU usage live...
        options.add_argument("--disable-gpu")
    else:
        # -------------------------
        # Disable sandboxing for chrome  locally 
        # (sandboxing = separated browser instance)...
        options.add_argument("--no-sandbox")


    driver = webdriver.Firefox(
        options=options
    )


    # ----------------
    # Task execution & progress
    # ----------------
    source_path = "webscraping/modules/webscraper/"

    sequenceManager = SequenceManager(driver, name, os.path.abspath(source_path))

    sequenceObjects = sequenceManager.sequenceObjects

    sequenceObjects_len = len(sequenceObjects)
    outputs = []
    all_steps_len = 0
    for i in range(len(sequenceObjects)):
        sequenceObj = sequenceObjects[i]
        steps = sequenceObj.get_steps()
        all_steps_len += len(steps)

    n = 0
    for i in range(len(sequenceObjects)):
        _print("i in range(sequenceObjects)", i)
        logger.debug(
            "views.webscrape_steps_long_running_method - i in range(sequenceObjects) > : %i " % i)

        sequenceObj = sequenceObjects[i]

        steps = sequenceObj.get_steps()
        for j in range(len(steps)):

            step = steps[j]
            outputs.append(sequenceObj.execute_step(step, variables=variables))

            progress_value = int(( n / all_steps_len) * 100)
            if progress_value >= 100:
                progress_value = 100

            taskProgress.set_unset( 
                Status.RUNNING if progress_value < 100 else Status.SUCCESS,
                progress_value,
                progress_message=f'Sequence step {n} of {all_steps_len} has been processed | for: {webscrape}'
            )

            webscrape.task_progress = progress_value
            webscrape.task_status = taskProgress.status
            webscrape.task_output = str(outputs[-1])
            webscrape.save()

            logger.debug("views.webscrape_steps_long_running_method - STEP > : "
                        f"{progress_value}% - {taskProgress.status} - {str(step)}")

            if progress_value >= 100 or taskProgress.status == Status.SUCCESS.value:
                break

            n += 1
        n += 1


    # ---------------
    # driver instance
    # ---------------
    driver.close()



    # ---------------
    # Task closure
    # ---------------
    output = {
        "datetime": datetime.datetime.now(),
        "input": webscrape,
        "outputs": outputs
    }
    
    progress_value = 100
    taskProgress.set_unset(
        Status.SUCCESS, progress_value,
        progress_message=f"{output}% have been processed"
    )

    webscrape.task_progress = progress_value
    processObj.task_status = taskProgress.status
    webscrape.save()




def parse_raw_outputs():
    def read_file(file):
        with open(file) as f:
            return f.readlines()

    output_dir = os.path.join(
        settings.BASE_DIR, settings.WEBSCRAPER_SOURCE_PATH, 'output'
    )

    result_template = {
        "NAME": None,
        "AGE": None,
        "LOCATION": None,
        "POSSIBLE_RELATIVES": None,
        "VERIFIED": None,
        "CRIMINAL_RECORDS": None,
    }

    files = list(filter(lambda x: x.endswith('.txt'), os.listdir(output_dir)))

    separator = "Based on your input we have selected the best result for you"
    results = []

    i = 0
    for f in files:
        try:
            items = read_file(os.path.join(output_dir, f))
            items = list(map( lambda x: x.replace('\n', '').replace('\t', ''), items))
            items = list(filter( lambda x: x.find('We could uncover') < 0, items))
            items = list(filter( lambda x: x.find('OPEN REPORT') < 0, items))
            items = list(filter( lambda x: x.find('ⓘ') < 0, items))
            items = items[8:]

            # if i < 15:
            #     print('----------------------------------------------| ', items)


            line_dict = copy.copy(result_template)
            for line in items:

                if len(line) >= 2:
                    if line.find("Based on your input") >= 0:
                        results.append(line_dict)
                        line_dict = copy.copy(result_template)

                    elif line.find("Possible Criminal or Traffic") >= 0:
                        line_dict["CRIMINAL_RECORDS"] = True

                    elif line.lower().find("verified") >= 0:
                        line_dict["VERIFIED"] = True

                    elif line.lower().find(",") >= 0:
                        if not line_dict["LOCATION"]:
                            line_dict["LOCATION"] = []
                        line_dict["LOCATION"].append(line)

                    elif len(line) == 2:
                        line_dict["AGE"] = line

                    else:
                        if not line_dict["NAME"]:
                            line_dict["NAME"] = line
                        else:
                            if not line_dict["POSSIBLE_RELATIVES"]:
                                line_dict["POSSIBLE_RELATIVES"] = []
                            line_dict["POSSIBLE_RELATIVES"].append(line)


            i += 1
        except Exception as err:
            print(
                '---------------| webscraping/views > parse_raw_outputs :: Error : ', err)
    return results




def Xwebscrape_steps_long_running_method( webscrape: Webscrape ):
    """
        A long-running method to execute web scraping steps sequentially.

        -----------
        Description:
            ! PREFERRED METHOD - see other in archives

            This method executes sequences' steps one bye one, and so 
            it provide task progress handling at step level.
            To be preferred for Taskprogress handling.

            See:
            -    tests.integration.test_longrunning_taskhandler
            -    models: TaskHandler, TaskProgress

        Args:
            webscrape (Webscrape): The web scraping task model.
    """
    def _print(key, value):
        if PRINT_VERBOSITY >= 0:
            print(f'-------| webscrape_steps_long_running_method > {key}', value)


    progress_value = 0

    # ------------
    # input values
    # ------------
    name = webscrape.task_name
    variables = webscrape.task_variables
    _print('type(webscrape.task_variables)', type(webscrape.task_variables))
    _print('webscrape.task_variables', webscrape.task_variables)
    logger.debug(
        "views.webscrape_steps_long_running_method - webscrape.task_variables > : %s " \
                                                        % str(webscrape.task_variables))

    # ---------------
    # driver instance create
    # ---------------
    options = Options()
    if IS_LIVE:
        # ----------------------------------------
        # Do not show browser (= headless) live...
        # remove True for showing browser locally
        options.add_argument("--headless")

    if IS_LIVE:
        # -------------------------
        # Disable GPU usage live...
        options.add_argument("--disable-gpu")
    else:
        # -------------------------
        # Disable sandboxing for chrome  locally 
        # (sandboxing = separated browser instance)...
        options.add_argument("--no-sandbox")


    driver = webdriver.Firefox(
        options=options
    )


    # ----------------
    # Task execution & progress
    # ----------------
    source_path = "webscraping/modules/webscraper/"

    sequenceManager = SequenceManager(driver, name, os.path.abspath(source_path))

    sequenceObjects = sequenceManager.sequenceObjects

    sequenceObjects_len = len(sequenceObjects)
    outputs = []
    all_steps_len = 0
    for i in range(len(sequenceObjects)):
        sequenceObj = sequenceObjects[i]
        steps = sequenceObj.get_steps()
        all_steps_len += len(steps)

    n = 0
    progress_value = 0
    progress_status = None
    for i in range(len(sequenceObjects)):
        logger.debug(
            "views.webscrape_steps_long_running_method - i in range(sequenceObjects) > : %i " % i)
        logger.debug("views.webscrape_steps_long_running_method - "
                     f"|||||||||||||||||||||| ALL_STEPS_LEN - N :: {all_steps_len} - {n}")
        _print(
            "|||||||||||||||||||||| ALL_STEPS_LEN - N",
            f"{all_steps_len} - {n}"
        )

        sequenceObj = sequenceObjects[i]

        steps = sequenceObj.get_steps()
        for j in range(len(steps)):

            step = steps[j]
            outputs.append(sequenceObj.execute_step(step, variables=variables))

            progress_value = int(( n / all_steps_len) * 100)
            if progress_value >= 100:
                progress_value = 100

            progress_status = Status.RUNNING if progress_value < 100 else Status.SUCCESS
            progress_message=f'Sequence step {n} of {all_steps_len} has been processed | for: {webscrape}'
            _print('progress_message', progress_message)

            webscrape.task_progress = progress_value
            webscrape.task_status = progress_status
            webscrape.task_output = str(outputs[-1])
            webscrape.save()

            logger.debug("views.webscrape_steps_long_running_method - STEP > : "
                        f"{progress_value}% - {progress_status} - {str(step)}")

            n += 1

            if n >= all_steps_len:
               progress_value = 100
               progress_status = Status.SUCCESS.value

            logger.debug("views.webscrape_steps_long_running_method - "
                         f"|||||||||||||||||||||| ALL_STEPS_LEN - N :: {all_steps_len} - {n}")
            _print(
                "|||||||||||||||||||||| ALL_STEPS_LEN - N",
                f"{all_steps_len} - {n}"
            )

            if progress_value >= 100 or progress_status == Status.SUCCESS.value:
                break


    # ---------------
    # driver instance
    # ---------------
    driver.close()



    # ---------------
    # Task closure
    # ---------------
    output = {
        "datetime": datetime.datetime.now(),
        "input": webscrape,
        "outputs": outputs
    }
    

    webscrape.task_progress = progress_value
    webscrape.task_status = progress_status
    webscrape.save()

