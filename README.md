# PiHardwareInfo

[![image](https://img.shields.io/pypi/v/PiHardwareInfo.svg)](https://pypi.org/project/PiHardwareInfo/)
[![image](https://img.shields.io/pypi/pyversions/PiHardwareInfo.svg)](https://pypi.org/project/PiHardwareInfo/)
[![image](https://img.shields.io/pypi/dm/PiHardwareInfo.svg)](https://pypi.org/project/PiHardwareInfo/)

Get Raspberry Pi hardware info from `/proc/cpuinfo` and `/sys/class/net/*`

## Try

run

```console
curl -s https://raw.githubusercontent.com/rexzhang/pi-hardware-info/master/pi_hardware_info.py | python3
```

result

```console
PiHardwareInfo(
 {'revision_code': '0x0',
 'model_type': <ModelType.RPI_5: 23>,
 'model_name': 'Raspberry Pi 5 Model B Rev 1.0',
 'processor': <Processor.BCM2712: 4>,
 'memory': 8192,
 'network_interface': {'eth0': '2C:CF:67:00:00:00',
                       'wlan0': '2C:CF:67:00:00:00'},
 'revision': '1.0',
 'serial_number': 'ecc0679911340000',
 'manufacturer': <Manufacturer.SONY_UK: 0>,
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

## History

### 0.6.0

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
