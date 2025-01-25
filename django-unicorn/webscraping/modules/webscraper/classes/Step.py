#!/usr/bin/env python3
# -*- coding: utf8 -*-
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import pandas as pd
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO


class Step:
    steps_common = {
        "asserts": []
    }

    def __init__(self, driver):
        self.driver = driver


    def execute(self, step_dict, _input=None):
        """
            List of step functions:
                assert_in_input
                assert_in_page_source
                clear
                find
                get
                get_attribute
                print OK
                print TEXT
                send_keys
                text_to_csv
                wait
        """
        outputs = []

        for key in step_dict.keys():
            if key in dir(self):
                print('----------|', key)
                outputs.append(
                    getattr(self, key)(
                        step_dict,
                        _input if not len(outputs) else outputs[-1]
                    )
                )

        return outputs


    @staticmethod
    def _by(by_string):
        # @ToDo :: Use reflection instead...
        r = {
            "By.ID": By.ID,
            "By.NAME": By.NAME,
        }.get(by_string, ValueError("by_string not yet implemented in "
                                    "webscraping.modules.webscraper.classes.Step.by"))
        return r

    @staticmethod
    def _keys(keys_string):
        """
            # @ToDo :: Use reflection instead...

            ValueError("keys_string not yet implemented in "
                    "webscraping.modules.webscraper.classes.Step.keys")
        """
        r = {
            "Keys.RETURN": Keys.RETURN,
        }.get(keys_string, keys_string)
        return r


    def assert_in_input(self, step_dict, _input):
        _assert_in_input = step_dict["assert_in_input"]
        _returned = _input[0]["returned"]

        assert _assert_in_input in _returned
        self.steps_common["asserts"].append(
            f"assert {_assert_in_input} in {_returned}"
        )
        return { "returned": _returned }


    def assert_in_page_source(self, step_dict, _input):
        _assert_in_page_source = step_dict["assert_in_page_source"]

        assert _assert_in_page_source in self.driver.page_source
        self.steps_common["asserts"].append(
            f"assert {_assert_in_page_source} in self.driver.page_source"
        )


    def clear(self, step_dict, _input):
        element = _input[0]["element"]
        element.clear()
        return { "element": element }


    def find(self, step_dict, _input):
        element = self.driver.find_element(
            Step._by(step_dict["by"]), 
            step_dict["find"]
        )
        return { "element": element }


    def get(self, step_dict, _input):
        self.driver.get(step_dict["get"])


    def get_attribute(self, step_dict, _input):
        out = _input[0]["element"].get_attribute(step_dict["get_attribute"])
        return { "returned": out }


    def print_OK(self, step_dict, _input):
        _asserts = "\n".join(self.steps_common["asserts"])
        print(f"""
            ------------ OK ----------------
            {_asserts}
            --------------------------------
        """)
        return _input[0] if type(_input[0]) == type({}) else _input

    def print_TEXT(self, step_dict, _input):
        if step_dict["print_TEXT"] == "input":
            print(f"""
                ------------ TEXT --------------
                {_input[0]["returned"]}
                --------------------------------
            """)
        return _input[0] if type(_input[0]) == type({}) else _input


    def send_keys(self, step_dict, _input):
        _input[0]["element"].send_keys(Step._keys(step_dict["send_keys"]))


    def text_to_csv(self, step_dict, _input):
        if step_dict["text_to_csv"] == "input":
            data = StringIO(f"""
                {_input[0]["returned"]}
            """)

            df = pd.read_table(data)
            df.to_csv(step_dict["filepath"])


    def wait(self, step_dict, _input):
        element = WebDriverWait(
                self.driver, step_dict["timeout"]).until(
            EC.element_to_be_clickable(
                    (Step._by(step_dict["by"]), step_dict["wait"])) 
        )
        return { "element": element }

