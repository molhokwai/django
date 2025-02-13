#!/usr/bin/env python3
# -*- coding: utf8 -*-
from django_app.settings import _print
from webscraping.modules.webscraper.classes.Step import Step
from webscraping.modules.webscraper.classes.Util import Util

import os
from typing import Union

class Sequence:
    driver = None
    sequence_steps = None
    source_path = None

    def __init__(self, driver, sequence_steps, source_path):
        self.driver = driver
        self.sequence_steps = sequence_steps
        self.source_path = os.path.abspath(source_path)


    # -------------------
    # FULL SEQUENCE EXECUTION
    # -------------------
    def execute(self, _input=None, variables={}):
        _outputs = []

        step_config = None
        for step_dicts in self.sequence_steps:
            for step_dict in step_dicts:
                for key in step_dict.keys():
                    if key == "config":
                        _print('----------| Sequence > %s' % key, VERBOSITY=3)
                        step_config = step_dict["config"]


        stepObj = Step(self.driver, config_dict=step_config)
        stepObj.variables = variables
        stepObj.source_path = self.source_path
        for step_dicts in self.sequence_steps:
            for step_dict in step_dicts:
                _outputs.append(stepObj.execute(
                        step_dict,
                        _input if not len(outputs) else outputs[-1]
                    )
                )

        return _outputs



    # -------------------
    # SEQUENCE STEP BY STEP EXECUTION
    # -------------------

    _step_config: Union[ dict, None] = None
    @property
    def step_config(self):
        if self._step_config is None:
            for step_dicts in self.sequence_steps:
                for step_dict in step_dicts:
                    for key in step_dict.keys():
                        if key == "config":
                            _print('----------| Sequence > %s' % key, VERBOSITY=3)
                            self._step_config = step_dict["config"]
        return self._step_config


    stepObj: Union[ Step, None] = None
    def get_stepObj(self, variables={}):
        if self.stepObj is None:
            self.stepObj = Step(self.driver, config_dict=self.step_config)
            self.stepObj.variables = variables
            self.stepObj.source_path = self.source_path
        return self.stepObj


    def get_steps(self):
        """
            Description
                step is the equivalent of step_dict...
        """
        steps = []
        for step_dicts in self.sequence_steps:
            for step_dict in step_dicts:
                steps.append(step_dict)
        return steps


    execute_step_outputs: list = []
    def execute_step(self, step: dict, _input=None, variables={}):
        """
            Description
                step is the equivalent of step_dict...
        """
        step_dict = step

        stepObj = self.get_stepObj(variables=variables)

        _outputs = self.execute_step_outputs
        output = stepObj.execute(
            step_dict,
            _input if not len(_outputs) else _outputs[-1]
        )

        self.execute_step_outputs.append(output)
        return output



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
            if self.name.endswith(".sequence.json"):
                sequence = Util.get_sequence(
                    self.source_path,
                    from_path=self.name
                )
                self._sequences = [sequence]

            else:
                self._sequences = Util.get_sequences_from_name(
                    self.source_path,
                    self.name
                )

        return self._sequences


    # -------------------
    # FULL SEQUENCE(S) EXECUTION
    # -------------------

    def execute_sequence(self, variables={}, i=0):
        sequence_steps = self.sequences[i]
        sequence = Sequence(self.driver, sequence_steps)
        return sequence.execute(variables=variables)


    def execute_sequences(self, variables={}):
        outputs = []

        sequences = self.sequences
        for sequence_steps in sequences:
            sequence = Sequence(self.driver, sequence_steps, self.source_path)
            outputs.append(sequence.execute(variables=variables))

        return outputs


    # -------------------
    # FOR SEQUENCE STEP BY STEP EXECUTION
    # -------------------

    _sequenceObjects: Union[ list[Sequence], None ] = None
    @property
    def sequenceObjects(self):
        if self._sequenceObjects is None:
            self._sequenceObjects = []

            sequences = self.sequences
            for sequence_steps in sequences:
                self._sequenceObjects.append(
                    Sequence(self.driver, sequence_steps, self.source_path))

        return self._sequenceObjects
