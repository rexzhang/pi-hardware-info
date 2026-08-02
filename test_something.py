import pytest

from pi_hardware_info import ModelType, PiHardwareInfo


@pytest.fixture
def info():
    obj = PiHardwareInfo()
    yield obj
    del obj


def test_old_style_revision_codes(info):
    info._get_info_from_revision_code("0005")
    assert info.model_type == ModelType.RPI_B
    assert info.revision == "2.0"

    info._get_info_from_revision_code("0015")
    assert info.model_type == ModelType.RPI_A_PLUS
    assert info.revision == "1.1"


def test_new_style_revision_codes(info):
    info._get_info_from_revision_code("a020d3")
    assert info.model_type == ModelType.RPI_3B_PLUS
    assert info.revision == "1.3"
    assert info.memory == 1024


def test_overvoltage_otp_program_otp_read(info):
    info._get_info_from_revision_code("a020d3")
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False


def test_5b(info):
    info._get_info_from_revision_code("d04170")
    print(info)
    assert info.model_type == ModelType.RPI_5
    assert info.revision == "1.0"
    assert info.memory == 8192
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False


def test_cm5(info):
    info._get_info_from_revision_code("b04180")
    print(info)
    assert info.model_type == ModelType.RPI_CM5
    assert info.revision == "1.0"
    assert info.memory == 2048
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False


def test_500plus(info):
    info._get_info_from_revision_code("e04190")
    print(info)
    assert info.model_type == ModelType.RPI_500
    assert info.revision == "1.0"
    assert info.memory == 16384
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False


def test_cm5_lite(info):
    info._get_info_from_revision_code("b041a0")
    print(info)
    assert info.model_type == ModelType.RPI_CM5_LITE
    assert info.revision == "1.0"
    assert info.memory == 2048
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False
