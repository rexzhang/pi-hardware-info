# PiHardwareInfo

[![image](https://img.shields.io/pypi/v/PiHardwareInfo.svg)](https://pypi.org/project/PiHardwareInfo/)
[![image](https://img.shields.io/pypi/pyversions/PiHardwareInfo.svg)](https://pypi.org/project/PiHardwareInfo/)
[![image](https://img.shields.io/pypi/dm/PiHardwareInfo.svg)](https://pypi.org/project/PiHardwareInfo/)

Get Raspberry Pi hardware/version info from /proc/cpuinfo

## Try

run

```console
curl -s https://raw.githubusercontent.com/rexzhang/pi-hardware-info/master/pi_hardware_info.py | python3
```

result

```console
PiHardwareInfo(revision_code='d04170', model_type=<ModelType.RPI_5: 23>, processor=<Processor.BCM2712: 4>, memory=8192, revision='1.0', serial_number='ecc0679911343e07', model_name='Raspberry Pi 5 Model B Rev 1.0', overvoltage=False, otp_program=False, otp_read=False, manufacturer=<Manufacturer.SONY_UK: 0>)
```

## Install

```console
pip install PiHardwareInfo
```

## Usage as library

```python
from pi_hardware_info import ModelType, get_info

info = get_info()
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

### 0.5.0

- Add, Support to raspberry pi 5
- Codebase modernization Updates
  - Drop py3.5 py3.6 py3.7 py3.8
  - Add type hints
  - Add unit test
  - Add pyproject.toml
  - Add pre-commit

### 0.4.0

- Add, support Zero2W/400/CM4
- Add, Overvoltage/OTP Program/OTP Read support

### 0.3.3

- Support raspberry pi 4B
- Rewrite some code

### 0.2.0

- Add old style revision code support, support 1A/1B

### 0.1.0

- First release

## Alternative

- <https://github.com/tompreston/raspi-version>
- <https://pypi.org/project/pirev>
- <https://pypi.org/project/RPi.version>

## Ref

- <https://www.raspberrypi.com/documentation/computers/raspberry-pi.html>
- <https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#raspberry-pi-revision-codes>
