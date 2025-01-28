from datetime import datetime
import time
from .taskHandler import Status

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from classes.SequenceManager import SequenceManager


def webscrape_long_running_method( _input : dict, task_progress ):

    task_progress.set( 
        Status.STARTED, 
        progress_message=f'The webscrape "{_input[title]}" has been started' )

    # input values
    # ------------
    name = _input["name"]

    variables = _input["variables"]
    for var_name in variables:
        val = variables[var_name]
        if type(val) == type(lambda x: x):
            variables[var_name] = val()


    # driver instance
    # ---------------
    options = Options()
    options.headless = False
    driver = webdriver.Firefox(
        options=options
    )

    # Tasks & progress
    # ----------------
    source_path = "modules/webscraper/"

    sequenceManager = SequenceManager(driver, name, os.path.abspath(source_path))

    outputs = []
    for i in range(len(sequenceManager.sequences)):
        """
            Execution loop sample
            ---------------------
            for i in range( 20 ):
                time.sleep( 0.5 )
                task_progress.set( Status.RUNNING, progress_message=f"{ 5 * i + 1 }% has been processed" )
        """
        outputs.append(sequenceManager.execute_sequence(variables=variables, i))
        task_progress.set( 
            Status.RUNNING,
            progress_message=f'Sequence {i} has been processed | Details: {_input}' )


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
    task_progress.set( Status.SUCCESS, output=output )


