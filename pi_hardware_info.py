"""
Get Raspberry Pi hardware info
"""

import os
import re
from dataclasses import dataclass, field
from enum import Enum
from logging import getLogger

__version__ = "0.6.0"

__author__ = "Rex Zhang"
__author_email__ = "rex.zhang@gmail.com"
__licence__ = "MIT"

__description__ = "Get Raspberry Pi hardware info"
__project_url__ = "https://github.com/rexzhang/pi-hardware-info"


logger = getLogger(__file__)

_CPU_INFO_FILE = "/proc/cpuinfo"
_NET_PATH = "/sys/class/net"
_MEMORY = [256, 512, 1024, 2048, 4096, 8192, 16384]


class Manufacturer(Enum):
    UNKNOWN = -100

    QISDA = -10

    SONY_UK = 0
    EGOMAN = 1
    EMBEST = 2
    SONY_JAPAN = 3
    EMBEST2 = 4
    STADIUM = 5


class Processor(Enum):
    UNKNOWN = -100

    BCM2835 = 0
    BCM2836 = 1
    BCM2837 = 2
    BCM2711 = 3
    BCM2712 = 4


class ModelType(Enum):
    UNKNOWN = -100

    RPI_A = 0
    RPI_B = 1
    RPI_A_PLUS = 2
    RPI_B_PLUS = 3
    RPI_2B = 4
    RPI_ALPHA = 5
    RPI_CM1 = 6
    # 0x7 pass
    RPI_3B = 8
    RPI_ZERO = 9
    RPI_CM3 = 0xA
    # 0xb pass
    RPI_ZERO_W = 0xC
    RPI_3B_PLUS = 0xD
    RPI_3A_PLUS = 0xE
    # 0x0f: Internal use only
    RPI_CM3_PLUS = 0x10
    RPI_4B = 0x11
    RPI_Zero2W = 0x12
    RPI_400 = 0x13
    RPI_CM4 = 0x14
    RPI_CM4S = 0x15
    # 0x16: Internal use only
    RPI_5 = 0x17
    RPI_CM5 = 0x18
    RPI_CM5_LITE = 0x19


_old_style = {
    0x0000: (ModelType.UNKNOWN, "0.0", 0, Manufacturer.UNKNOWN),
    0x0002: (ModelType.RPI_B, "1.0", 256, Manufacturer.EGOMAN),
    0x0003: (ModelType.RPI_B, "1.0", 256, Manufacturer.EGOMAN),
    0x0004: (ModelType.RPI_B, "2.0", 256, Manufacturer.SONY_UK),
    0x0005: (ModelType.RPI_B, "2.0", 256, Manufacturer.QISDA),
    0x0006: (ModelType.RPI_B, "2.0", 256, Manufacturer.EGOMAN),
    0x0007: (ModelType.RPI_A, "2.0", 256, Manufacturer.EGOMAN),
    0x0008: (ModelType.RPI_A, "2.0", 256, Manufacturer.SONY_UK),
    0x0009: (ModelType.RPI_A, "2.0", 256, Manufacturer.QISDA),
    0x000D: (ModelType.RPI_B, "2.0", 512, Manufacturer.EGOMAN),
    0x000E: (ModelType.RPI_B, "2.0", 512, Manufacturer.SONY_UK),
    0x000F: (ModelType.RPI_B, "2.0", 512, Manufacturer.EGOMAN),
    0x0010: (ModelType.RPI_B_PLUS, "1.2", 512, Manufacturer.SONY_UK),
    0x0011: (ModelType.RPI_CM1, "1.0", 512, Manufacturer.SONY_UK),
    0x0012: (ModelType.RPI_A_PLUS, "1.1", 256, Manufacturer.SONY_UK),
    0x0013: (ModelType.RPI_B_PLUS, "1.2", 512, Manufacturer.EMBEST),
    0x0014: (ModelType.RPI_CM1, "1.0", 512, Manufacturer.EMBEST),
    0x0015: (ModelType.RPI_A_PLUS, "1.1", 512, Manufacturer.EMBEST),
}


@dataclass
class PiHardwareInfo:
    revision_code: str = "0x0"

    model_type: ModelType = ModelType.UNKNOWN
    model_name: str = "UNKNOWN"
    processor: Processor = Processor.UNKNOWN
    memory: int = 0
    network_interface: dict = field(init=False)

    revision: str = "0.0"
    serial_number: str = "UNKNOWN"
    manufacturer: Manufacturer = Manufacturer.UNKNOWN

    overvoltage: bool = False
    otp_program: bool = False
    otp_read: bool = False

    def _get_info_from_revision_code(self, revision_code: str):
        code = int(revision_code, 16)

        new_flag = (code & 0x800000) >> 23
        if new_flag:
            self.model_type = ModelType((code & 0xFF0) >> 4)
            self.processor = Processor((code & 0xF000) >> 12)
            self.memory = _MEMORY[(code & 0x700000) >> 20]
            self.revision = f"1.{code & 0xF}"

            self.overvoltage = bool((code & 0x80000000) >> 31)
            self.overvoltage = bool((code & 0x40000000) >> 30)
            self.overvoltage = bool((code & 0x20000000) >> 29)

            self.manufacturer = Manufacturer((code & 0xF0000) >> 16)

        else:
            self.model_type = _old_style[code][0]
            self.revision = _old_style[code][1]
            self.memory = _old_style[code][2]

            self.manufacturer = _old_style[code][3]

    @staticmethod
    def _get_data_from_line(line: str) -> str:
        index = line.find(":")
        if index == -1:
            return ""

        return line[index + 1 :].lstrip(" ").strip(" \n")

    def __post_init__(self):
        try:
            with open(_CPU_INFO_FILE) as f:
                for line in f:
                    if "Revision" in line:
                        self._get_info_from_revision_code(
                            re.sub(r"Revision\t: ([a-z0-9]+)\n", r"\1", line)
                        )

                    elif line.startswith("Serial"):
                        data = self._get_data_from_line(line)
                        if data:
                            self.serial_number = data

                    elif line.startswith("Model"):
                        data = self._get_data_from_line(line)
                        if data:
                            self.model_name = data

        except FileNotFoundError:
            logger.warning(
                f"Load Raspberry Pi hardware info from {_CPU_INFO_FILE} failed!"
            )

        # ---
        network_interface = dict()
        try:
            for interface in os.listdir(_NET_PATH):
                mac_file = os.path.join(_NET_PATH, interface, "address")
                if os.path.exists(mac_file):
                    with open(mac_file) as f:
                        mac = f.read().strip().upper()
                        if mac != "00:00:00:00:00:00":
                            network_interface[interface] = mac

        except FileNotFoundError:
            logger.warning(f"Can not load network interface info from {_NET_PATH}")

        self.network_interface = network_interface


def get_info():
    # backwards compatible
    return PiHardwareInfo()


if __name__ == "__main__":
    import pprint
    from dataclasses import asdict

    print(
        f"PiHardwareInfo(\n {pprint.pformat(asdict(PiHardwareInfo()), sort_dicts=False)}\n)"
    )
