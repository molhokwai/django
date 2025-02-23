#!/usr/bin/env python3
_B='.sequences'
_A='sequences'
import os,json
from django_app.settings import MAIN_APP_PATHNAME
MAIN_APP_PATHNAME=MAIN_APP_PATHNAME
class Util:
	@staticmethod
	def get_sequence(source_path,from_name=None,from_path=None):
		C=from_name;D=source_path;A=from_path;B=None
		if C:B=os.path.join(D,_A,MAIN_APP_PATHNAME,f"{C}.sequence.json")
		if A:
			if A.endswith('.sequence.json'):B=os.path.join(MAIN_APP_PATHNAME,D,_A,A)
			elif A.endswith(_B):raise ValueError("Single sequence file name cannot must end with '.sequence.json' - Items ending with '.sequences' must be folders containing single sequence files...")
			else:raise ValueError("Single sequence file name must end with '.sequence.json'. Multiple sequences folder name for folder containing single sequence files must end with '.sequences'...")
		E={}
		with open(B)as F:E=json.loads(F.read())
		return E
	@staticmethod
	def get_sequences_from_name(source_path,name):
		B=name;C=source_path
		if B.endswith(_B):
			' @ToDo :: Implement for a list of sequences ';D=os.path.join(MAIN_APP_PATHNAME,C,_A,f"{B}");A=[]
			for E in os.listdir(D):F=os.path.join(D,E);A.append(Util.get_sequence(C,from_path=os.path.abspath(F)))
			return A
		else:G=Util.get_sequence(C,from_name=B);A=[G];return A