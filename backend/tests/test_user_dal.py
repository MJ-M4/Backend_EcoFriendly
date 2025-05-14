import pytest
from src.models.user import User
from src.dal import user_dal

def test_create_and_get_user():
    u = User(
        user_id=999999999,
        role_id=2,
        first_name="Test",
        last_name="User",
        password_hash="testpass123"
    )
    user_dal.create(u)
    u2 = user_dal.get_by_id(999999999)
    assert u2.full_name() == "Test User"
    assert u2.check_password("testpass123")

def test_update_user():
    user_dal.update(999999999, first_name="Updated")
    u = user_dal.get_by_id(999999999)
    assert u.first_name == "Updated"

def test_delete_user():
    user_dal.delete(999999999)
    with pytest.raises(Exception):
        user_dal.get_by_id(999999999)