==============
PiHardwareInfo
==============

.. image:: https://img.shields.io/pypi/v/PiHardwareInfo.svg
    :target: https://pypi.org/project/PiHardwareInfo/
.. image:: https://img.shields.io/pypi/pyversions/PiHardwareInfo.svg
    :target: https://pypi.org/project/PiHardwareInfo/
.. image:: https://img.shields.io/pypi/dm/PiHardwareInfo.svg
    :target: https://pypi.org/project/PiHardwareInfo/


Get Raspberry Pi hardware/version info from /proc/cpuinfo


Try
===

run

.. code-block:: console

    curl -s https://raw.githubusercontent.com/rexzhang/pi-hardware-info/master/pi_hardware_info.py | python3

result

.. code-block:: console

    <PiHardwareInfo:0x000005, RPI_B, UNKNOWN, 256, 2.0, False, False, False, QISDA, UNKNOWN>
    <PiHardwareInfo:0xa020d3, RPI_3B_PLUS, BCM2837, 1024, 1.3, False, False, False, SONY_UK, UNKNOWN>


Install
=======

.. code-block:: console

    pip install PiHardwareInfo


Usage
=====

.. code-block:: python

    from pi_hardware_info import ModelType, get_info

    info = get_info()
    if info.model_type == ModelType.MODEL_3B_PLUS:
        print('5G Wifi ready')

    elif info.model_type == ModelType.MODEL_3B:
        print('only 2.4G Wifi')


History
=======

0.4.0
-----
* Add, support Zero2W/400/CM4
* Add, Overvoltage/OTP Program/OTP Read support

0.3.3
-----
* Support raspberry pi 4B
* Rewrite some code

0.2.0
-----
* Add old style revision code support, support 1A/1B

0.1.0
-----
* First release


Alternative
===========

* https://github.com/tompreston/raspi-version
* https://pypi.org/project/pirev
* https://pypi.org/project/RPi.version


Ref
===

* https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#raspberry-pi-revision-codes
* https://www.raspberrypi-spy.co.uk/2012/09/checking-your-raspberry-pi-board-version/
* https://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
