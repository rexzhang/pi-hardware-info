# PiHardwareInfo
Get Raspberry Pi hardware info from /proc/cpuinfo


# Try
```bash
curl -s https://raw.githubusercontent.com/rexzhang/pi-hardware-info/master/pi_hardware_info.py | python3
```
```text
<PiHardwareInfo:0xa020d3, MODEL_3B_PLUS, BCM2837, 1024, 1.3, Sony_UK, 00000000d855943b>
```

# Install
```bash
pip install PiHardwareInfo
```

# Usage
```python
from pi_hardware_info import ModelType, get_info

info = get_info()
if info.model_type == ModelType.MODEL_3B_PLUS:
    print('5G Wifi ready')
    
else:
    print('only 2.4G Wifi')
```

# Other choice
* https://github.com/tompreston/raspi-version (work)
* https://pypi.org/project/pirev
* https://pypi.org/project/RPi.version

# Ref
* https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md
* https://www.raspberrypi-spy.co.uk/2012/09/checking-your-raspberry-pi-board-version/
* https://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
