import pytest
from bidcheck.auth import hash_password,verify_password
from bidcheck.session import SessionStore
from bidcheck.tenant import User
from bidcheck.auth_middleware import authenticate_bearer,AuthenticationRequired

def test_password_round_trip():
    record=hash_password('correct-password')
    assert verify_password('correct-password',record)
    assert not verify_password('wrong-password',record)

def test_bearer_session_resolves_user():
    store=SessionStore(); token=store.create('u1','t1')
    user=authenticate_bearer('Bearer '+token,store)
    assert user==User('u1','', 't1')

def test_invalid_bearer_is_rejected():
    with pytest.raises(AuthenticationRequired): authenticate_bearer('Bearer invalid',SessionStore())
