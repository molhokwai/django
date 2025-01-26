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
    outputs = []
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
        self.outputs = []

        for key in step_dict.keys():
            if key in dir(self):
                print('----------|', key)
                self.outputs.append(
                    getattr(self, key)(
                        step_dict,
                        _input if not len(self.outputs) else self.outputs[-1]
                    )
                )

        return self.outputs


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
            @ToDo :: Use reflection instead, with ValueError if Keys.(.*) ...
                ValueError("keys_string not yet implemented in "
                        "webscraping.modules.webscraper.classes.Step.keys")
        """
        r = {
            "Keys.RETURN": Keys.RETURN,
        }.get(keys_string, keys_string)
        return r


    def assert_in_driver_title(self, step_dict, _input):
        _assert_in_driver_title = step_dict["assert_in_driver_title"]

        assert _assert_in_driver_title in self.driver.title
        self.steps_common["asserts"].append(
            f"assert {_assert_in_driver_title} in self.driver.title"
        )
        # new
        return _input if type(_input) == type({}) else _input[0]


    def assert_in_input(self, step_dict, _input, _not=False):
        _assert = None
        _input = _input if type(_input) == type({}) else _input[0]
        _returned = _input["returned"] if "returned" in _input \
                                            else self.driver.page_source

        if _not:
            _assert = step_dict["assert_not_in_input"]
            assert _assert not in _returned
        else:
            _assert = step_dict["assert_in_input"]
            assert _assert in _returned

        self.steps_common["asserts"].append(
            f"assert {_assert} in {_returned}"
        )
        return { "returned": _returned }


    def assert_in_page_source(self, step_dict, _input):
        _assert_in_page_source = step_dict["assert_in_page_source"]

        assert _assert_in_page_source in self.driver.page_source
        self.steps_common["asserts"].append(
            f"assert {_assert_in_page_source} in self.driver.page_source"
        )
        # new
        return _input if type(_input) == type({}) else _input[0]


    def assert_not_in_input(self, step_dict, _input):
        # new
        _input = _input if type(_input) == type({}) else _input[0]
        return self.assert_in_input(step_dict, _input, _not=True)


    def clear(self, step_dict, _input):
        _input = _input if type(_input) == type({}) else _input[0]
        element = _input["element"]
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
        return _input if type(_input) == type({}) else _input[0]


    def print_TEXT(self, step_dict, _input):
        _input = _input if type(_input) == type({}) else _input[0]
        if step_dict["print_TEXT"] == "input":
            print(f"""
                ------------ TEXT --------------
                {_input["returned"][200:]}
                --------------------------------
            """)
        return _input if type(_input) == type({}) else _input[0]


    def send_keys(self, step_dict, _input):
        _input = _input if type(_input) == type({}) else _input[0]
        _input["element"].send_keys(Step._keys(step_dict["send_keys"]))
        # new
        return _input if type(_input) == type({}) else _input[0]


    def text_to_csv(self, step_dict, _input):
        if step_dict["text_to_csv"] == "input":
            data = StringIO(f"""
                {_input[0]["returned"]}
            """)

            df = pd.read_table(data)
            df.to_csv(step_dict["filepath"])
        # new
        return _input if type(_input) == type({}) else _input[0]


    def wait(self, step_dict, _input):
        element = WebDriverWait(
                self.driver, step_dict["timeout"]).until(
            EC.element_to_be_clickable(
                    (Step._by(step_dict["by"]), step_dict["wait"])) 
        )
        return { "element": element }

