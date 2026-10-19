# PiHardwareInfo

[![image](https://img.shields.io/pypi/v/PiHardwareInfo.svg)](https://pypi.org/project/PiHardwareInfo/)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/rexzhang/pi-hardware-info/master/pyproject.toml)
[![image](https://img.shields.io/pypi/dm/PiHardwareInfo.svg)](https://pypi.org/project/PiHardwareInfo/)

Get Raspberry Pi hardware info from `/proc/cpuinfo` and `/sys/class/net/*`

## Try

run

```console
curl -s https://raw.githubusercontent.com/rexzhang/pi-hardware-info/master/pi_hardware_info/__init__.py | python3
```

This one-liner depends on `pi_hardware_info/__init__.py` staying self-contained (no relative imports).

result

```console
PiHardwareInfo(
 {'revision_code': '0x0',
 'model_type': <ModelType.RPI_3B_PLUS: 13>,
 'model_name': 'Raspberry Pi 3 Model B Plus Rev 1.3',
 'processor': <Processor.BCM2837: 2>,
 'memory': 1024,
 'manufacturer': <Manufacturer.SONY_UK: 0>,
 'revision': '1.3',
 'serial_number': '00000000d855943b',
 'mac_address': {'eth0': 'B8:27:EB:55:94:3B', 'wlan0': 'B8:27:EB:00:C1:6E'},
 'overvoltage': False,
 'otp_program': False,
 'otp_read': False}
)
```

## Install

```console
pip install PiHardwareInfo
```

## Usage as library

```python
from pi_hardware_info import ModelType, PiHardwareInfo

info = PiHardwareInfo()
if info.model_type == ModelType.MODEL_3B_PLUS:
    print('5G Wifi ready')

elif info.model_type == ModelType.MODEL_3B:
    print('only 2.4G Wifi')
```

## Usage as tool

```shell
python -m pi_hardware_info
```

## Note

- For a memory size of "0/Other", the actual memory capacity can be determined from the rpi-sdram-size-gbit [firmware parameter](https://www.raspberrypi.com/documentation/computers/configuration.html#part4)

## History

### 0.8.0 - 20261019

- Convert single module to package layout, add `py.typed` marker (PEP 561)
- Downstream mypy users no longer need `follow_untyped_imports`
- Add full type hints; enable strict mypy checking for package and tests
- Keep `curl | python3`, `python -m pi_hardware_info`, and direct-file execution working

### 0.7.0 - 20260805

- Support RPI_500, RPI_CM0
- Support memory size code:7(Other), output 0
- Fix RPI_CM5_LITE
- Fix .otp_program/.otp_program
- Add more unittest
- Add file `pi-hardware-info.desktop` for run in RPi GUI

### 0.6.1 - 20250225

- Add, network interface MAC address info
- Refactor

### 0.5.0 - 20250224

- Add, Support to raspberry pi 5
- Codebase modernization Updates
  - Drop py3.5 py3.6 py3.7 py3.8
  - Add type hints
  - Add unit test
  - Add pyproject.toml
  - Add pre-commit

### 0.4.0 - 20220810

- Add, support Zero2W/400/CM4
- Add, Overvoltage/OTP Program/OTP Read support

### 0.3.3 - 20190709

- Support raspberry pi 4B
- Rewrite some code

### 0.2.0 - 20190302

- Add old style revision code support, support 1A/1B

### 0.1.0 - 20190301

- First release

## Alternative

- <https://github.com/tompreston/raspi-version>
- <https://pypi.org/project/pirev>
- <https://pypi.org/project/RPi.version>

## Ref

- <https://www.raspberrypi.com/documentation/computers/raspberry-pi.html>
- <https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#raspberry-pi-revision-codes>
