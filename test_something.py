from pi_hardware_info import ModelType, get_info_from_revision_code


def test_old_style_revision_codes():
    info = get_info_from_revision_code("0005")
    assert info.model_type == ModelType.RPI_B
    assert info.revision == "2.0"

    info = get_info_from_revision_code("0015")
    assert info.model_type == ModelType.RPI_A_PLUS
    assert info.revision == "1.1"


def test_new_style_revision_codes():
    info = get_info_from_revision_code("a020d3")
    assert info.model_type == ModelType.RPI_3B_PLUS
    assert info.revision == "1.3"
    assert info.memory == 1024


def test_overvoltage_otp_program_otp_read():
    info = get_info_from_revision_code("a020d3")
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False


def test_5b():
    info = get_info_from_revision_code("d04170")
    print(info)
    assert info.model_type == ModelType.RPI_5
    assert info.revision == "1.0"
    assert info.memory == 8192
    assert info.overvoltage is False
    assert info.otp_program is False
    assert info.otp_read is False
