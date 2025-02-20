from django.test import SimpleTestCase, TestCase, TransactionTestCase
from django.db.utils import OperationalError

from webscraping.modules.threader.classes.TaskHandler import TaskHandler
from webscraping.modules.threader.classes.TaskProgress import TaskProgress, Status
from webscraping.models import Webscrape

import re, datetime, time
from typing import Union


class ProcessObject:
    """
        processObj = {
            "title": "A process object with: task_run_id, task_progress, task_outputs",
            "task_run_id": None,
            "task_progress": None,
            "task_outputs": None,
        }
    """
    task_run_id: Union[ str, None ] = None
    task_progress: Union[ int, None ] = None
    task_status: Union[ str, None ] = None
    task_outputs: Union[ list, None] = None
    description: str = "A process object with: task_run_id, task_progress, task_outputs"


class LongRunningTaskHandlerTestCases(TransactionTestCase):
    """
        -----------
        @T :: SimpleTestCase →to TestCase →to TransactionTestCase
        @T ::   try:
                    ...
                except django.db.utils.OperationalError as err:
                    ...

        @T ::   darklight.Blog.date_created: (fields.W161) Fixed default value provided.
                HINT: It seems you set a fixed date / time / datetime value as default for this field. This may not be what you want. If you want to have the current date as default, use `django.utils.timezone.now`

        @T ::   Status.STATUS instead of Status.SUCCESS

                :167    taskProgress.set_unset(
                            Status.STATUS, progress_value,
                            progress_message=f"{output}% has been processed" )



        -----------
        Src:
            "A simple approach for background task in Django"
            Handle long running task using Threading and Django Cache
            - https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django
    """

    def from_source(self):
        # def test_long_running_task(self):

        #     input = 'aaaaaa'
        #     print( f'{ input= }' )

        #     task_run_id = self.__start_task( input )
        #     print( f'{ task_run_id= }' )

        #     while True:

        #         time.sleep( 1 )
        #         result = self.__get_task_progress_response( task_run_id )

        #         if result_dict[ 'status' ] == "SUCCESS":
        #             self.print_output(result_dict)
        #             break

        #         self.print_progress_message(result_dict)

        # def print_output(self, result_dict):
        #     status = result_dict[ 'status' ]
        #     output = result_dict[ "output" ]
        #     print( f'{status=}, { output= }' )

        # def print_progress_message(self, result_dict):
        #     status = result_dict[ 'status' ]
        #     progress_message = result_dict[ 'progress_message' ]
        #     print( f'{ status= },{ progress_message= }' )

        # def __start_task( self, input ):
        #     res = self.client.get( f'/bgTaskExAPI/start_long_running_task/?input={ input }' )
        #     self.assertEqual( res.status_code, 200 )

        #     task_run_id = res.json()[ 'task_run_id' ]
        #     UUID_V1_PATTERN = re.compile( '[a-f0-9]{8}-[a-f0-9]{4}-1[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$', re.IGNORECASE)
        #     self.assertEqual( UUID_V1_PATTERN.match( task_run_id ) is not None, True )

        #     return task_run_id

        # def __get_task_progress_response( self, task_run_id : str ):
        #     res = self.client.get( f'/bgTaskExAPI/get_task_progress/?task_run_id={ task_run_id }' )
        #     self.assertEqual( res.status_code, 200 )

        #     return res.json()
        pass


    @staticmethod
    def _print(key, value):
        print( f'webscraping.tests.integration.test_long_running_task - { key } :: { value }' )


    def test_long_running_task(self):
        _print = LongRunningTaskHandlerTestCases._print

        processObj = ProcessObject()

        # Get/Generate task id with Task handler
        processObj.task_run_id = TaskHandler().start_task(
            self.long_running_method, [ processObj ] )

        UUID_V1_PATTERN = re.compile( '[a-f0-9]{8}-[a-f0-9]{4}-1[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$', re.IGNORECASE)
        self.assertEqual( UUID_V1_PATTERN.match( processObj.task_run_id ) is not None, True )

        _print( 'processObj.task_run_id', processObj.task_run_id )

        i = 0
        taskProgress = TaskHandler.get_taskProgress( processObj.task_run_id )
        while taskProgress.status != Status.SUCCESS.value:
            try:

                    time.sleep( 1 )
                    taskProgress = TaskHandler.get_taskProgress( processObj.task_run_id )

                    progress_value = taskProgress.value
                    self.assertTrue( taskProgress.value is not None )

                    _print( 'taskProgress.value', taskProgress.value )
                    _print( 'taskProgress.status', taskProgress.status )
                    if taskProgress.status == Status.SUCCESS:
                        _print( f'{taskProgress.status} > output', taskProgress.output )
                        break

                    _print( f'{taskProgress.status} > progress_message', taskProgress.progress_message )
                    i += 1
            except OperationalError as err:
                _print( 'Caught <django.db.utils.OperationalError>: ', err )


        self.assertTrue( taskProgress.outputs is not None )
        _print( 'test_long_running_task > taskProgress.outputs', taskProgress.outputs )
        _print( 'test_long_running_task > processObj.task_outputs', processObj.task_outputs )



    def long_running_method(self, processObj: ProcessObject, taskProgress ):
        _print = LongRunningTaskHandlerTestCases._print

        progress_value = 0
        taskProgress.set_unset( 
            Status.STARTED, progress_value,
            progress_message=f'The process with object "{processObj}" has been started' )


        sequence = range(2)
        sequences_len = len(sequence)
        for i in range(sequences_len):
            for j in range( 10 ):
                time.sleep( 1 )
                output = 5 * j + 1

                progress_value = int(( i / sequences_len) * 100)
                if progress_value >= 100:
                    progress_value = 100

                taskProgress.set_unset(
                    Status.RUNNING if progress_value < 100 else Status.SUCCESS,
                    progress_value,
                    progress_message=f"{output}% has been processed",
                    output = output)

                processObj.task_progress = progress_value
                processObj.task_status = taskProgress.status
                processObj.task_outputs = taskProgress.outputs

                if progress_value >= 100 or taskProgress.status == Status.SUCCESS.value:
                    break

        final_output = f"[{ datetime.datetime.now() }] input::{ processObj }, outputs::{taskProgress.outputs}"

        progress_value = 100
        taskProgress.set_unset(
            Status.SUCCESS, progress_value,
            progress_message=f"{final_output}% have been processed" )

        processObj.task_progress = progress_value
        processObj.task_status = taskProgress.status

        _print( 'long_running_method > taskProgress.status', taskProgress.status )
        _print( 'long_running_method > processObj.task_progress', processObj.task_progress )
        _print( 'long_running_method > processObj.task_outputs', processObj.task_outputs )

