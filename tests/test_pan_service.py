from services.pan_service import validate_pan, normalize_pan


def test_validate_pan_success():
    assert validate_pan('ABCDE1234F') is True


def test_validate_pan_failure():
    assert validate_pan('ABC123') is False


def test_normalize_pan():
    assert normalize_pan(' abcd-e1234f ') == 'ABCDE1234F'
