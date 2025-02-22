#!/usr/bin/env python3
# -*- coding: utf8 -*-
from django_app.settings import _print
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

# import pandas
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

from django.utils.text import slugify

import os, datetime, time

class Step:
    class Config:
        ui_timeout = 0
    config: Config = None

    step_dicts = []
    outputs = []
    steps_common = {
        "asserts": []
    }
    step_dict_keys_excluded = ("config", "step_dicts", "variables")

    variables = {}

    source_path = None

    def __init__(self, driver, config_dict=None):
        self.driver = driver

        self.config = Step.Config()
        if config_dict:
            for key in config_dict:
                setattr(self.config, key, config_dict[key])

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
        self.step_dicts.append(step_dict)
        self.outputs = []

        for key in step_dict.keys():
            if key in dir(self) and not key in self.step_dict_keys_excluded:
                _print('----------| %s %s ' % (key, step_dict[key]), VERBOSITY=3)
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
            "By.CSS_SELECTOR": By.CSS_SELECTOR,
        }.get(by_string, ValueError("by_string not yet implemented in "
                                    "webscraping.modules.webscraper.classes.Step.by"))
        return r

    @staticmethod
    def dom_get_by(by_string):
        # @ToDo :: Use reflection instead...
        r = {
            "By.ID": "document.getElementById('%s')",
            "By.NAME": "document.getElementsByName('%s')[0]",
            "By.CSS_SELECTOR": "document.querySelector('%s')",
        }.get(by_string)
        return r


    def _keys(self, keys_string):
        """
            @ToDo :: Use reflection instead, with ValueError if Keys.(.*) ...
                ValueError("keys_string not yet implemented in "
                        "webscraping.modules.webscraper.classes.Step.keys")
        """
        r = {
            "Keys.RETURN": Keys.RETURN,
            "Keys.SPACE": Keys.SPACE,
        }.get(keys_string, keys_string)
        return r

    def input_keys(self, keys_string, _key=None):
        """
            @ToDo :: Fix [user_input] ... ?
            Usage:
                [variable]
                    { "send_keys": "[variable]", "key": "..." }
                    ___________
                    Description:
                        The variable will be fetched from the
                        variables dict attribute of the step by
                        the key provided in the config line above
        """
        r = {
            "[user_input]": lambda _key: input("Enter value: "),
            "[variable]": lambda _key: self.variables[_key],
        }.get(keys_string)(_key)
        return r




    def assert_in_driver_title(self, step_dict, _input):
        _assert_in_driver_title = step_dict["assert_in_driver_title"]

        assert _assert_in_driver_title in self.driver.title
        self.steps_common["asserts"].append(
            f"assert {_assert_in_driver_title} in self.driver.title"
        )

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

        _not_string = "not" if _not else ""
        self.steps_common["asserts"].append(
            f"assert {_assert} {_not_string} in {_returned}"
        )
        return { "returned": _returned }


    def assert_in_page_source(self, step_dict, _input, _not=False):
        _placeholder_variables = {}
        if "placeholder_variables" in step_dict:
            for var_name in step_dict["placeholder_variables"]:
                _placeholder_variables[var_name] = self.variables[var_name]

        _assert = None
        if _not:
            _assert = step_dict["assert_not_in_page_source"] \
                                            % _placeholder_variables
            assert _assert not in self.driver.page_source, f'Error "{_assert}" in source...'
        else:
            _assert = step_dict["assert_in_page_source"] \
                                            % _placeholder_variables
            assert _assert.lower() in self.driver.page_source.lower(), f'Error "{_assert.lower()}" not in source...'

        _not_string = "not" if _not else ""
        self.steps_common["asserts"].append(
            f"assert {_assert} {_not_string} in self.driver.page_source"
        )

        return _input if type(_input) == type({}) else _input[0]


    def assert_not_in_input(self, step_dict, _input):
        _input = _input if type(_input) == type({}) else _input[0]
        return self.assert_in_input(step_dict, _input, _not=True)


    def assert_not_in_page_source(self, step_dict, _input):
        _input = _input if type(_input) == type({}) else _input[0]
        return self.assert_in_page_source(step_dict, _input, _not=True)


    def clear(self, step_dict, _input):
        time.sleep(self.config.ui_timeout)

        _input = _input if type(_input) == type({}) else _input[0]
        element = _input["element"]
        element.clear()
        return { "element": element }


    def click(self, step_dict, _input):
        time.sleep(self.config.ui_timeout)

        element = None

        _input = _input if type(_input) == type({}) else _input[0] if len(_input) else _input
        if type(_input) == type({}) and "element" in _input:
            element = _input["element"]

            if element:
                element_step_dict = self.step_dicts[-2]
                element_find = element_step_dict["find"] if "find" in element_step_dict else element_step_dict["wait"]
                element_by = element_step_dict["by"]
                element_dom_get_by = Step.dom_get_by(element_by) % element_find

                if "scrollIntoView" in step_dict and step_dict["scrollIntoView"]:
                    # scrollIntoView()
                    self.driver.execute_script(f"{element_dom_get_by}.style.zIndex = 1000; {element_dom_get_by}.scrollIntoView();")

                # click()
                if step_dict["click"] == "Left":
                    # element.click()
                    self.driver.execute_script(f"{element_dom_get_by}.click();")


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


    def repeat(self, step_dict, _input):
        repeat = step_dict["repeat"]
        step_dicts = step_dict["step_dicts"]

        _io = _input
        for i in range(repeat):
            for _step_dict in step_dicts:
                _io = self.execute(_step_dict, _io)

        return _io


    def select(self, step_dict, _input):
        """
            @ToDo

            ],[
                { "find": "state", "by": "By.NAME"  },
                { "select": "ALL", "key": "state", "function": "select_state" },
                { "select": "[variable]", "key": "state", "function": "select_state" }
        """
        time.sleep(self.config.ui_timeout)

        _input = _input if type(_input) == type({}) else _input[0]

        _send_keys = step_dict["send_keys"]
        _keys_value = ""
        if _send_keys == "[input]":
            _keys_value = self.input_keys(_send_keys)

        elif step_dict["send_keys"] == "[variable]":
            _key = step_dict["key"]
            _keys_value = self.input_keys(_send_keys, _key=_key)

        else:
            _keys_value = self._keys(_send_keys)

        _input["element"].send_keys(_keys_value)

        return _input if type(_input) == type({}) else _input[0]


    def send_keys(self, step_dict, _input):
        time.sleep(self.config.ui_timeout)

        _input = _input if type(_input) == type({}) else _input[0]

        _send_keys = step_dict["send_keys"]
        _keys_value = ""
        if _send_keys == "[input]":
            _keys_value = self.input_keys(_send_keys)

        elif step_dict["send_keys"] == "[variable]":
            _key = step_dict["key"]
            _keys_value = self.input_keys(_send_keys, _key=_key)

        else:
            _keys_value = self._keys(_send_keys)

        if _keys_value:
            _input["element"].send_keys(_keys_value)

        return _input if type(_input) == type({}) else _input[0]


    def set_var(self, step_dict, _input):
        time.sleep(self.config.ui_timeout)

        _input = _input if type(_input) == type({}) else _input[0]

        var_name = step_dict["set_var"]
        self.variables[var_name] = _input["returned"]


        return _input if type(_input) == type({}) else _input[0]


    def text_to_csv(self, step_dict, _input):
        _input = _input if type(_input) == type({}) else _input[0]

        text = None
        if step_dict["text_to_csv"] == "variables":
            text = ""
            for var_name in step_dict["variables"]:
                text += "\n" + self.variables[var_name]

        elif step_dict["text_to_csv"] == "input":
            text = _input["returned"]


        _now = datetime.datetime.now()
        output_pathname = os.path.join(
            self.source_path, step_dict["folderpath"],
            slugify(f'{_now}-{step_dict["filename"]}')
        )
        output_fullpath = ""

        # -----------------
        # data = StringIO(f"""
        #     {text}
        # """)
        #
        # try:
        #     output_fullpath = f"{output_pathname}.csv"
        #     df = pandas.read_table(data)
        #     df.to_csv(output_fullpath)
        #
        # except pandas.errors.ParserError as err:
        #
        #     output_fullpath = f"{output_pathname}.txt"
        #     with open(output_fullpath, "w") as f:
        #         f.write(text)
        #
        #     print('----------| pandas.errors.ParserError: ', err)
        #
        # -----------------
        # @ToDo :: Fix pandas install on pythonanywhere to restore code (see all "Fix pandas" todos)
        #          ref: https://stackoverflow.com/questions/30761152/how-to-solve-import-error-for-pandas
        # -----------------
        if True:
            output_fullpath = f"{output_pathname}.txt"
            with open(output_fullpath, "w") as f:
                f.write(text)

        self.outputs.append(output_fullpath)

        return _input if type(_input) == type({}) else _input[0]


    def wait(self, step_dict, _input):
        element = None

        try:
            element = WebDriverWait(
                    self.driver, step_dict["timeout"]).until(
                EC.element_to_be_clickable(
                        (Step._by(step_dict["by"]), step_dict["wait"]))
            )
        except TimeoutException as err:
            if "optional" in step_dict and step_dict["optional"]:
                print('----------| Optional field - TimeoutException: ', err)
            else:
                print('----------| Non optional field - TimeoutException: ', err)
                raise err

        return { "element": element }

