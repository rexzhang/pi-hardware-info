#!/usr/bin/env python
# coding=utf-8


"""
Get Raspberry Pi hardware info

https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md
https://www.raspberrypi.org/documentation/hardware/raspberrypi/README.md
"""

import re
from enum import IntEnum

__version__ = '0.3.2'

__author__ = 'Rex Zhang'
__author_email__ = 'rex.zhang@gmail.com'
__licence__ = 'MIT'

__description__ = 'Get Raspberry Pi hardware info'
__project_url__ = 'https://github.com/rexzhang/pi-hardware-info'

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

    RPI_A = 0
    RPI_B = 1
    RPI_A_PLUS = 2
    RPI_B_PLUS = 3
    RPI_2B = 4
    RPI_ALPHA = 5
    RPI_CM1 = 6
    # RPI_UNKNOWN = 7
    RPI_3B = 8
    RPI_ZERO = 9
    RPI_CM3 = 0xa
    # RPI_UNKNOWN = 0xb
    RPI_ZERO_W = 0xc
    RPI_3B_PLUS = 0xd
    RPI_3A_PLUS = 0xe
    # RPI_UNKNOWN = 0xf
    RPI_CM3_PLUS = 0x10


_old_style = {
    0x0002: (ModelType.RPI_B, 1.0, 256, Manufacturer.EGOMAN),
    0x0003: (ModelType.RPI_B, 1.0, 256, Manufacturer.EGOMAN),
    0x0004: (ModelType.RPI_B, 2.0, 256, Manufacturer.SONY_UK),
    0x0005: (ModelType.RPI_B, 2.0, 256, Manufacturer.QISDA),
    0x0006: (ModelType.RPI_B, 2.0, 256, Manufacturer.EGOMAN),
    0x0007: (ModelType.RPI_A, 2.0, 256, Manufacturer.EGOMAN),
    0x0008: (ModelType.RPI_A, 2.0, 256, Manufacturer.SONY_UK),
    0x0009: (ModelType.RPI_A, 2.0, 256, Manufacturer.QISDA),
    0x000d: (ModelType.RPI_B, 2.0, 512, Manufacturer.EGOMAN),
    0x000e: (ModelType.RPI_B, 2.0, 512, Manufacturer.SONY_UK),
    0x000f: (ModelType.RPI_B, 2.0, 512, Manufacturer.EGOMAN),
    0x0010: (ModelType.RPI_B_PLUS, 1.2, 512, Manufacturer.SONY_UK),
    0x0011: (ModelType.RPI_CM1, 1.0, 512, Manufacturer.SONY_UK),
    0x0012: (ModelType.RPI_A_PLUS, 1.1, 256, Manufacturer.SONY_UK),
    0x0013: (ModelType.RPI_B_PLUS, 1.2, 512, Manufacturer.EMBEST),
    0x0014: (ModelType.RPI_CM1, 1.0, 512, Manufacturer.EMBEST),
    0x0015: (ModelType.RPI_A_PLUS, 1.1, 512, Manufacturer.EMBEST),
}


class PiHardwareInfo(object):
    revision_code = 0

    model_type = ModelType.UNKNOWN
    processor = Processor.UNKNOWN
    memory = 0
    revision = '0.0'
    serial_number = 'UNKNOWN'

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

    try:
        with open('/proc/cpuinfo') as f:
            for line in f:
                if "Revision" in line:
                    info = get_info_from_revision_code(
                        int(re.sub(r'Revision\t: ([a-z0-9]+)\n', r'\1', line), 16)
                    )

                if line[0:6] == 'Serial':
                    info.serial_number = line[10:26]

    except FileNotFoundError:
        info = PiHardwareInfo()

    return info


if __name__ == '__main__':
    # print(get_info_from_revision_code(int('0005', 16)))
    # print(get_info_from_revision_code(int('a020d3', 16)))
    print(get_info())
