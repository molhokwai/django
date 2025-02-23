#!/usr/bin/env python3
# -*- coding: utf8 -*-
import os, json
from django_app.settings import MAIN_APP_PATHNAME

MAIN_APP_PATHNAME = MAIN_APP_PATHNAME

class Util:
    @staticmethod
    def get_sequence(source_path, from_name=None, from_path=None):
        filepath = None
        if from_name:

            filepath = os.path.join(
                source_path, "sequences",
                MAIN_APP_PATHNAME, f"{from_name}.sequence.json"
            )

        if from_path:
            if from_path.endswith(".sequence.json"):
                filepath = os.path.join(
                    MAIN_APP_PATHNAME, source_path, "sequences", from_path
                )

            elif from_path.endswith(".sequences"):
                raise ValueError("Single sequence file name cannot must end with '.sequence.json'"
                                 " - Items ending with '.sequences' must be folders containing" 
                                 " single sequence files...")
            else:
                raise ValueError("Single sequence file name must end with '.sequence.json'."
                                 " Multiple sequences folder name for folder containing"
                                 " single sequence files must end with '.sequences'...")
        sequence = {}
        with open(filepath) as f:
            sequence = json.loads(f.read())

        return sequence

    @staticmethod
    def get_sequences_from_name(source_path, name):
        if name.endswith(".sequences"):
            """ @ToDo :: Implement for a list of sequences """                
            folderpath = os.path.join(
                MAIN_APP_PATHNAME, source_path, "sequences",
                f"{name}"
            )
            sequences = []
            for f in os.listdir(folderpath):
                filepath = os.path.join(folderpath, f)
                sequences.append(
                    Util.get_sequence(source_path, 
                                from_path=os.path.abspath(filepath))
                )
            return sequences

        else:
            sequence = Util.get_sequence(source_path, 
                                                from_name=name)
            sequences = [sequence]
            return sequences
