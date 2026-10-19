from collections.abc import Iterator
from unittest.mock import patch

import pytest

from pi_hardware_info import Manufacturer, ModelType, PiHardwareInfo, Processor


@pytest.fixture
def info() -> Iterator[PiHardwareInfo]:
    obj = PiHardwareInfo()
    yield obj
    del obj


def test_cpuinfo_permission_error(caplog: pytest.LogCaptureFixture) -> None:
    """PiHardwareInfo should survive PermissionError reading /proc/cpuinfo and keep defaults."""
    with patch("builtins.open", side_effect=PermissionError):
        obj = PiHardwareInfo()

    assert obj.model_type == ModelType.UNKNOWN
    assert obj.serial_number == "UNKNOWN"
    assert obj.model_name == "UNKNOWN"
    assert "Load Raspberry Pi hardware info from" in caplog.text


def test_net_path_permission_error(caplog: pytest.LogCaptureFixture) -> None:
    """PiHardwareInfo should survive PermissionError on /sys/class/net and keep mac_address empty."""
    with patch("pi_hardware_info.os.listdir", side_effect=PermissionError):
        obj = PiHardwareInfo()

    assert obj.mac_address == {}
    assert "Can not load network interface info from" in caplog.text


def test_old_style_revision_code_0005(info: PiHardwareInfo) -> None:
    info._get_info_from_revision_code("0005")
    assert info.model_type == ModelType.RPI_B
    assert info.revision == "2.0"


def test_old_style_revision_code_0015(info: PiHardwareInfo) -> None:
    info._get_info_from_revision_code("0015")
    assert info.model_type == ModelType.RPI_A_PLUS
    assert info.revision == "1.1"


def test_old_style_leaves_new_fields_at_defaults(info: PiHardwareInfo) -> None:
    """Old-style revision codes don't carry processor/otp bits; fields stay at defaults."""
    info._get_info_from_revision_code("0010")
    assert info.processor == Processor.UNKNOWN
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False


def test_unknown_old_style_revision_code(
    info: PiHardwareInfo, caplog: pytest.LogCaptureFixture
) -> None:
    """Unknown old-style revision codes should not raise KeyError; fields stay at defaults."""
    info._get_info_from_revision_code("0001")

    assert info.model_type == ModelType.UNKNOWN
    assert info.revision == "0.0"
    assert info.memory == 0
    assert info.manufacturer == Manufacturer.UNKNOWN

    assert "Unknown revision code: 0001" in caplog.text


def test_new_style_revision_codes(info: PiHardwareInfo) -> None:
    info._get_info_from_revision_code("a020d3")
    assert info.model_type == ModelType.RPI_3B_PLUS
    assert info.revision == "1.3"
    assert info.memory == 1024


def test_new_style_revision_code_uppercase(info: PiHardwareInfo) -> None:
    """Revision code extraction from /proc/cpuinfo should support uppercase hex (A-F)."""
    info._get_info_from_revision_code("A020D3")
    assert info.model_type == ModelType.RPI_3B_PLUS
    assert info.revision == "1.3"
    assert info.memory == 1024


def test_overvoltage_otp_program_otp_read(info: PiHardwareInfo) -> None:
    info._get_info_from_revision_code("a020d3")
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False


def test_5b(info: PiHardwareInfo) -> None:
    info._get_info_from_revision_code("d04170")
    print(info)
    assert info.model_type == ModelType.RPI_5
    assert info.revision == "1.0"
    assert info.memory == 8192
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False


def test_cm5(info: PiHardwareInfo) -> None:
    info._get_info_from_revision_code("b04180")
    print(info)
    assert info.model_type == ModelType.RPI_CM5
    assert info.revision == "1.0"
    assert info.memory == 2048
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False


def test_500plus(info: PiHardwareInfo) -> None:
    info._get_info_from_revision_code("e04190")
    print(info)
    assert info.model_type == ModelType.RPI_500
    assert info.revision == "1.0"
    assert info.memory == 16384
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False


def test_cm5_lite(info: PiHardwareInfo) -> None:
    info._get_info_from_revision_code("b041a0")
    print(info)
    assert info.model_type == ModelType.RPI_CM5_LITE
    assert info.revision == "1.0"
    assert info.memory == 2048
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False
