#!/usr/bin/env python
# coding=utf-8


"""Get Raspberry Pi hardware info"""

import re
from enum import IntEnum

__version__ = '0.1.0'
__author__ = 'Rex Zhang'
__author_email__ = 'rex.zhang@gmail.com'
__licence__ = 'MIT'

_memory = [
    256,
    512,
    1024
]


class Manufacturer(IntEnum):
    Sony_UK = 0
    Egoman = 1
    Embest = 2
    Sony_Japan = 3
    Embest2 = 4
    Stadium = 5


class Processor(IntEnum):
    BCM2835 = 0
    BCM2836 = 1
    BCM2837 = 2


class ModelType(IntEnum):
    MODEL_A = 0
    MODEL_B = 1
    MODEL_A_PLUS = 2
    MODEL_B_PLUS = 3
    MODEL_2B = 4
    MODEL_ALPHA = 5
    MODEL_CM1 = 6
    # MODEL_UNKNOWN = 7
    MODEL_3B = 8
    MODEL_ZERO = 9
    MODEL_CM3 = 0xa
    # MODEL_UNKNOWN = 0xb
    MODEL_ZERO_W = 0xc
    MODEL_3B_PLUS = 0xd
    MODEL_3A_PLUS = 0xe
    # MODEL_UNKNOWN = 0xf
    MODEL_CM3_PLUS = 0x10


class PiHardwareInfo(object):
    revision_code = None

    model_type = None
    processor = None
    memory = 0
    revision = None
    serial_number = None

    manufacturer = None

    def __str__(self):
        return '<PiHardwareInfo:0x{:x}, {}, {}, {}, {}, {}, {}>'.format(
            self.revision_code, self.model_type.name, self.processor.name, self.memory,
            self.revision, self.manufacturer.name, self.serial_number
        )


def get_info_from_revision_code(code):
    info = PiHardwareInfo()
    info.revision_code = code
    info.model_type = ModelType((code & 0xFF0) >> 4)
    info.processor = Processor((code & 0xF000) >> 12)
    info.memory = _memory[(code & 0x700000) >> 20]
    info.revision = '1.{}'.format(code & 0xF)

    info.manufacturer = Manufacturer((code & 0xF0000) >> 16)
    return info


def get_info():
    info = None
    for line in open("/proc/cpuinfo"):
        if "Revision" in line:
            info = get_info_from_revision_code(
                int(re.sub(r'Revision\t: ([a-z0-9]+)\n', r'\1', line), 16)
            )

        if line[0:6] == 'Serial':
            info.serial_number = line[10:26]

    return info


if __name__ == '__main__':
    print(get_info())
