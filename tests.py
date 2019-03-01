#!/usr/bin/env python
# coding=utf-8


import unittest

from .pi_hardware_info import (
    ModelType,
    Processor,
    get_info_from_revision_code,
)


class TestStringMethods(unittest.TestCase):

    def test_new_style(self):
        info = get_info_from_revision_code(int('a020d3', 16))
        self.assertEqual(info.model_type, ModelType.MODEL_3B_PLUS)
        self.assertEqual(info.processor, Processor.BCM2837)


if __name__ == '__main__':
    unittest.main()
