from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from webscraping.models import (
    Webscrape, WebscrapeData,
    TaskProgress, TaskHandler, Status
)

from webscraping.modules.webscraper.classes.SequenceManager import SequenceManager

from django_app.settings import logger, _print, PRINT_VERBOSITY

import os, datetime, time, copy, csv, json

DEBUG = settings.DEBUG
IS_LIVE = settings.IS_LIVE
WEBSCRAPER_HEADLESS = settings.WEBSCRAPER_HEADLESS


def index(request):
    context = {}
    return render(request, "webscraping/index.html", {})


def webscrape(request):
    context = {}
    return render(request, "webscraping/webscrape.html", {})


def webscrape_data(request):
    context = {}
    return render(request, "webscraping/webscrape-data.html", {})



def export_output_to_csv(
                request,
                task_id: str = None, 
                data_id: int = None) -> HttpResponse:
    """
        Exports the output of a specific Webscrape task to a CSV file.

        Args:
            request (HttpRequest): The HTTP request object.
            task_id (str): The unique ID of the task whose output is to be exported.
            data_id (str): The unique ID of the data object whose output is to be exported.

        Raises:
            ValueError: If neither `task_id` nor `data_id` is provided.

        Returns:
            HttpResponse: A CSV file as an HTTP response for download.

        Steps:
            1. Create an HTTP response object with CSV content type.
            2. Set the Content-Disposition header to trigger a file download.
            3. Retrieve the Webscrape object using the provided task_id.
            4. Parse the task_output field (assumed to be JSON) into a Python object.
            5. Process the parsed output to extract relevant data.
            6. Write the header row to the CSV file.
            7. Write the data rows to the CSV file.
            8. Return the HTTP response with the CSV file.

        Example Usage:
            - URL: /export-csv/<task_id>/
            - Template: <a href="{% url 'export_csv' task_id=task.id %}">Download CSV</a>

        With:
            Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025        
    """

    try:
        if not task_id and not data_id:
            raise ValueError(
                "webscraping.Webscrape.parse_output_text :: "
                "One of <task_id> or <data_id> must be provided..."
            )

        # Step 1: Get the JSON data output from the object
        # Get file placehoders data
        # ------------------------------------------------
        data = []
        
        file_id, file_prefix = None, None
        if task_id:
            file_id, file_prefix = task_id, 'task'
            data = Webscrape.data_for_export_output_to_csv(task_id)

        elif data_id:
            file_id, file_prefix = data_id, 'data'
            data = WebscrapeData.data_for_export_output_to_csv(data_id)


        # Step 1: Create an HTTP response object with CSV content type
        # Step 2: Set the Content-Disposition header to trigger a file download
        # ---------------------------------------------------------        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{file_prefix}_{file_id}_output.csv"'


        # Step 4: Write the header row to the CSV file
        # --------------------------------------------
        header = data[0].keys()  # Extract header from the first row of data
        writer = csv.writer(response)
        writer.writerow(header)

        # Step 5: Write the data rows to the CSV file
        # -------------------------------------------
        for row in data:
            writer.writerow(list(map(lambda x: row[x], header)))  # Write each row

        # Step 6: Return the HTTP response with the CSV file
        # --------------------------------------------------
        return response

    except Exception as err:
        _print(
            '----------------| webscraping.views.export_output_to_csv > Error: %s' % err,
            VERBOSITY = 0
        )
        return redirect('error')


def webscrape_steps_long_running_method( webscrape: Webscrape, taskProgress ):
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
    if WEBSCRAPER_HEADLESS or IS_LIVE:
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

    # adjust for config step
    # @ToDo: Mark config as setup step vs sequence steps ?
    all_steps_len -= 1

    n = 0
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

            taskProgress.set_unset( 
                Status.RUNNING if progress_value < 100 else Status.SUCCESS,
                progress_value,
                progress_message=f'Sequence step {n} of {all_steps_len} has been processed | for: {webscrape}'
            )

            n += 1

            _break = False
            if (n >= all_steps_len) or (progress_value >= 100 or taskProgress.status == Status.SUCCESS.value):
                taskProgress.value = progress_value = 100
                taskProgress.status = Status.SUCCESS.value
                _break = True

            webscrape.task_progress = taskProgress.value
            webscrape.task_status = taskProgress.status
            webscrape.task_output = str(outputs[-1])
            webscrape.save()


            logger.debug("views.webscrape_steps_long_running_method - STEP > : "
                        f"{progress_value}% - {taskProgress.status} - {str(step)}")
            logger.debug("views.webscrape_steps_long_running_method - "
                         f"|||||||||||||||||||||| ALL_STEPS_LEN - N :: {all_steps_len} - {n}")
            _print(
                "|||||||||||||||||||||| ALL_STEPS_LEN - N",
                f"{all_steps_len} - {n}"
            )

            if _break:
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
    
    statusE = {
        'STARTED': Status.STARTED,
        'RUNNING': Status.RUNNING,
        'SUCCESS': Status.SUCCESS,
        'FAILED': Status.FAILED,
    }[taskProgress.status]
    taskProgress.set_unset(
        statusE, taskProgress.value,
        progress_message=f"{output}% have been processed"
    )

    webscrape.task_progress = taskProgress.value
    webscrape.task_status = taskProgress.status
    webscrape.save()


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



def parse_raw_outputs():
    """
        Parses raw output files from a specified directory and returns a list of parsed results.

        Steps:
            1. Define the output directory using Django settings.
            2. List all `.txt` files in the output directory.
            3. Iterate through each file, parse its content using `Webscrape.parse_output_text`,
               and append the results to a list.
            4. Handle any exceptions that occur during file parsing.
            5. Return the aggregated list of parsed results.

        Returns:
            list: A list of dictionaries, where each dictionary represents a parsed record.

        Example Usage:
            ```python
            parsed_results = parse_raw_outputs()
            for result in parsed_results:
                print(result)
            ```

        With:
            Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025        
    """

    # Step 1: Define the output directory using Django settings
    # ---------------------------------------------------------
    output_dir = os.path.join(
        settings.BASE_DIR, settings.WEBSCRAPER_SOURCE_PATH, 'output'
    )

    # Step 2: List all `.txt` files in the output directory
    # ---------------------------------------------------------
    files = list(filter(lambda x: x.endswith('.txt'), os.listdir(output_dir)))

    # Step 3: Iterate through each file, parse its content, and append the results
    # ---------------------------------------------------------
    results = []
    i = 0
    for f in files:
        try:
            # Parse the file content using Webscrape.parse_output_text
            # ---------------------------------------------------------
            file_path = os.path.join(output_dir, f)
            parsed_data = Webscrape.parse_output_text(file_path=file_path)
            results += parsed_data  # Append parsed data to the results list

            i += 1
        except Exception as err:
            # Step 4: Handle any exceptions that occur during file parsing
            # ---------------------------------------------------------
            print(
                '---------------| webscraping/views > parse_raw_outputs :: Error : ', err)

    # Step 5: Return the aggregated list of parsed results
    # ----------------------------------------------------
    return results

