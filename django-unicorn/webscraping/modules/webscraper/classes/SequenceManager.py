#!/usr/bin/env python3
# -*- coding: utf8 -*-
from classes.Step import Step
from classes.Util import Util

import os


class Sequence:
    driver = None
    sequence_steps = None

    def __init__(self, driver, sequence_steps):
        self.driver = driver
        self.sequence_steps = sequence_steps


    def execute(self, _input=None, variables={}):
        outputs = []

        step_config = None
        for step_dicts in self.sequence_steps:
            for step_dict in step_dicts:
                for key in step_dict.keys():
                    if key == "config":
                        print('----------| Sequence > ', key)
                        step_config = step_dict["config"]


        stepObj = Step(self.driver, config_dict=step_config)
        stepObj.variables = variables
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


    def execute_sequence(self, variables={}, i=0):
        sequence_steps = self.sequences[i]
        sequence = Sequence(self.driver, sequence_steps)
        return sequence.execute(variables=variables)


    def execute_sequences(self, variables={}):
        outputs = []

        sequences = self.sequences
        for sequence_steps in sequences:
            sequence = Sequence(self.driver, sequence_steps)
            outputs.append(sequence.execute(variables=variables))

        return outputs


