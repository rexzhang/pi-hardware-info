#!/usr/bin/env python
# coding=utf-8


"""
Get Raspberry Pi hardware info

https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md
"""

import re
from enum import IntEnum

__version__ = '0.2.0'
__author__ = 'Rex Zhang'
__author_email__ = 'rex.zhang@gmail.com'
__licence__ = 'MIT'

_memory = [
    256,
    512,
    1024
]


class Manufacturer(IntEnum):
    UNKNOWN = -100

    QISDA = -10

    SONY_UK = 0
    EGOMAN = 1
    EMBEST = 2
    SONY_JAPAN = 3
    EMBEST2 = 4
    STADIUM = 5


class Processor(IntEnum):
    UNKNOWN = -100

    BCM2835 = 0
    BCM2836 = 1
    BCM2837 = 2


class ModelType(IntEnum):
    UNKNOWN = -100

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


_old_style = {
    0x0002: (ModelType.MODEL_B, 1.0, 256, Manufacturer.EGOMAN),
    0x0003: (ModelType.MODEL_B, 1.0, 256, Manufacturer.EGOMAN),
    0x0004: (ModelType.MODEL_B, 2.0, 256, Manufacturer.SONY_UK),
    0x0005: (ModelType.MODEL_B, 2.0, 256, Manufacturer.QISDA),
    0x0006: (ModelType.MODEL_B, 2.0, 256, Manufacturer.EGOMAN),
    0x0007: (ModelType.MODEL_A, 2.0, 256, Manufacturer.EGOMAN),
    0x0008: (ModelType.MODEL_A, 2.0, 256, Manufacturer.SONY_UK),
    0x0009: (ModelType.MODEL_A, 2.0, 256, Manufacturer.QISDA),
    0x000d: (ModelType.MODEL_B, 2.0, 512, Manufacturer.EGOMAN),
    0x000e: (ModelType.MODEL_B, 2.0, 512, Manufacturer.SONY_UK),
    0x000f: (ModelType.MODEL_B, 2.0, 512, Manufacturer.EGOMAN),
    0x0010: (ModelType.MODEL_B_PLUS, 1.2, 512, Manufacturer.SONY_UK),
    0x0011: (ModelType.MODEL_CM1, 1.0, 512, Manufacturer.SONY_UK),
    0x0012: (ModelType.MODEL_A_PLUS, 1.1, 256, Manufacturer.SONY_UK),
    0x0013: (ModelType.MODEL_B_PLUS, 1.2, 512, Manufacturer.EMBEST),
    0x0014: (ModelType.MODEL_CM1, 1.0, 512, Manufacturer.EMBEST),
    0x0015: (ModelType.MODEL_A_PLUS, 1.1, 512, Manufacturer.EMBEST),
}


class PiHardwareInfo(object):
    revision_code = None

    model_type = ModelType.UNKNOWN
    processor = Processor.UNKNOWN
    memory = 0
    revision = None
    serial_number = None

    manufacturer = Manufacturer.UNKNOWN

    def __str__(self):
        return '<PiHardwareInfo:{:#08x}, {}, {}, {}, {}, {}, {}>'.format(
            self.revision_code, self.model_type.name, self.processor.name, self.memory,
            self.revision, self.manufacturer.name, self.serial_number
        )


def get_info_from_revision_code(code):
    info = PiHardwareInfo()
    info.revision_code = code

    new_flag = (code & 0x800000) >> 23
    if new_flag:
        info.model_type = ModelType((code & 0xFF0) >> 4)
        info.processor = Processor((code & 0xF000) >> 12)
        info.memory = _memory[(code & 0x700000) >> 20]
        info.revision = '1.{}'.format(code & 0xF)

        info.manufacturer = Manufacturer((code & 0xF0000) >> 16)

    else:
        info.model_type = _old_style[code][0]
        info.revision = _old_style[code][1]
        info.memory = _old_style[code][2]
        info.manufacturer = _old_style[code][3]

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
    # print(get_info_from_revision_code(int('0005', 16)))
    # print(get_info_from_revision_code(int('a020d3', 16)))
    print(get_info())
