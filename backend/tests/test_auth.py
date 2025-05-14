from src.interface.auth import _encode_token, _decode_token

def test_token_encode_decode():
    token = _encode_token(123456789, "manager")
    decoded = _decode_token(token)
    assert decoded["sub"] == 123456789
    assert decoded["role"] == "manager"