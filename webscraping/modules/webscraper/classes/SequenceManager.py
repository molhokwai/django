#!/usr/bin/env python3
_C='----------| Sequence > %s'
_B='config'
_A=None
from django_app.settings import _print
from webscraping.modules.webscraper.classes.Step import Step
from webscraping.modules.webscraper.classes.Util import Util
import os
from typing import Union
class Sequence:
	driver=_A;sequence_steps=_A;source_path=_A
	def __init__(A,driver,sequence_steps,source_path):A.driver=driver;A.sequence_steps=sequence_steps;A.source_path=os.path.abspath(source_path)
	def execute(A,_input=_A,variables={}):
		E=[];F=_A
		for C in A.sequence_steps:
			for B in C:
				for G in B.keys():
					if G==_B:_print(_C%G,VERBOSITY=3);F=B[_B]
		D=Step(A.driver,config_dict=F);D.variables=variables;D.source_path=A.source_path
		for C in A.sequence_steps:
			for B in C:E.append(D.execute(B,_input if not len(outputs)else outputs[-1]))
		return E
	_step_config:Union[dict,_A]=_A
	@property
	def step_config(self):
		A=self
		if A._step_config is _A:
			for D in A.sequence_steps:
				for B in D:
					for C in B.keys():
						if C==_B:_print(_C%C,VERBOSITY=3);A._step_config=B[_B]
		return A._step_config
	stepObj:Union[Step,_A]=_A
	def get_stepObj(A,variables={}):
		if A.stepObj is _A:A.stepObj=Step(A.driver,config_dict=A.step_config);A.stepObj.variables=variables;A.stepObj.source_path=A.source_path
		return A.stepObj
	def get_steps(B):
		'\n            Description\n                step is the equivalent of step_dict...\n        ';A=[]
		for C in B.sequence_steps:
			for D in C:A.append(D)
		return A
	execute_step_outputs:list=[]
	def execute_step(A,step,_input=_A,variables={}):'\n            Description\n                step is the equivalent of step_dict...\n        ';D=step;E=A.get_stepObj(variables=variables);B=A.execute_step_outputs;C=E.execute(D,_input if not len(B)else B[-1]);A.execute_step_outputs.append(C);return C
class SequenceManager:
	driver=_A;name=_A;source_path=_A
	def __init__(A,driver,name,source_path):A.driver=driver;A.name=name;A.source_path=os.path.abspath(source_path)
	_sequences=_A
	@property
	def sequences(self):
		A=self
		if not A._sequences:
			if A.name.endswith('.sequence.json'):B=Util.get_sequence(A.source_path,from_path=A.name);A._sequences=[B]
			else:A._sequences=Util.get_sequences_from_name(A.source_path,A.name)
		return A._sequences
	def execute_sequence(A,variables={},i=0):B=A.sequences[i];C=Sequence(A.driver,B);return C.execute(variables=variables)
	def execute_sequences(A,variables={}):
		B=[];C=A.sequences
		for D in C:E=Sequence(A.driver,D,A.source_path);B.append(E.execute(variables=variables))
		return B
	_sequenceObjects:Union[list[Sequence],_A]=_A
	@property
	def sequenceObjects(self):
		A=self
		if A._sequenceObjects is _A:
			A._sequenceObjects=[];B=A.sequences
			for C in B:A._sequenceObjects.append(Sequence(A.driver,C,A.source_path))
		return A._sequenceObjects