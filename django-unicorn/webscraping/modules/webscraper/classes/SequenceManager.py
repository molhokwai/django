#!/usr/bin/env python3
# -*- coding: utf8 -*-
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from classes.Step import Step
from classes.Util import Util

import os


class Sequence:
    driver = None
    sequence_steps = None

    def __init__(self, driver, sequence_steps):
        self.driver = driver
        self.sequence_steps = sequence_steps


    def execute(self, _input=None):
        outputs = []

        stepObj = Step(self.driver)
        for step_dicts in self.sequence_steps:
            for step_dict in step_dicts:
                outputs.append(stepObj.execute(
                        step_dict,
                        _input if not len(outputs) else outputs[-1]
                    )
                )

        return outputs


class SequenceManager:
    driver = None
    name = None
    source_path = None


    def __init__(self, driver, name, source_path):
        self.driver = driver
        self.name = name
        self.source_path = os.path.abspath(source_path)


    _sequences = None
    @property    
    def sequences(self):
        if not self._sequences:
            self._sequences = Util.get_sequences_from_name(
                    self.source_path,
                    self.name
                )

        return self._sequences


    def execute_sequences(self):
        sequences = self.sequences

        for sequence_steps in sequences:
            sequence = Sequence(self.driver, sequence_steps)
            sequence.execute()


