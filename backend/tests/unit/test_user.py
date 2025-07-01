import pytest
from fastapi import HTTPException
from sqlmodel import Session
from app.database.models.user import User, UserCreate
from app.services.user_service import create_user
from app.core.security import get_password_hash, verify_password
from app.database.models.user import User


# Mock dependencies
@pytest.fixture
def mock_db():
    return Session()

@pytest.fixture
def mock_user_create():
    return UserCreate(username="testuser", email="test@example.com", password="Fakepass0o!")

# Test: Successful user creation
def test_create_user_success(mock_db, mock_user_create, mocker):
    # Mock database query to return no existing user
    mocker.patch.object(mock_db, 'query', return_value=mocker.Mock(**{
        'filter.return_value.first.return_value': None
    }))
    
    # Mock database operations
    mock_add = mocker.patch.object(mock_db, 'add')
    mock_commit = mocker.patch.object(mock_db, 'commit')
    mock_refresh = mocker.patch.object(mock_db, 'refresh')
    
    # Execute function
    result = create_user(mock_db, mock_user_create)
    
    # Assertions
    assert isinstance(result, User)
    assert result.username == mock_user_create.username
    assert result.email == mock_user_create.email
    assert verify_password(mock_user_create.password, result.hashed_password)
    # mock_hash.assert_called_once_with(mock_user_create.password)
    mock_add.assert_called_once()
    mock_commit.assert_called_once()
    mock_refresh.assert_called_once_with(result)

# Test: Username already exists
def test_create_user_username_exists(mock_db, mock_user_create, mocker):
    # Mock existing user with same username
    existing_user = User(username=mock_user_create.username, email="other@example.com", hashed_password="old_hash")
    mocker.patch.object(mock_db, 'query', return_value=mocker.Mock(**{
        'filter.return_value.first.return_value': existing_user
    }))
    
    # Execute and assert exception
    with pytest.raises(HTTPException) as exc_info:
        create_user(mock_db, mock_user_create)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Username or email already registered"

# Test: Email already exists
def test_create_user_email_exists(mock_db, mock_user_create, mocker):
    # Mock existing user with same email
    existing_user = User(username="otheruser", email=mock_user_create.email, hashed_password="old_hash")
    mocker.patch.object(mock_db, 'query', return_value=mocker.Mock(**{
        'filter.return_value.first.return_value': existing_user
    }))
    
    # Execute and assert exception
    with pytest.raises(HTTPException) as exc_info:
        create_user(mock_db, mock_user_create)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Username or email already registered"

# Test: Both username and email exist
def test_create_user_both_exist(mock_db, mock_user_create, mocker):
    # Mock existing user with same username and email
    existing_user = User(username=mock_user_create.username, email=mock_user_create.email, hashed_password="old_hash")
    mocker.patch.object(mock_db, 'query', return_value=mocker.Mock(**{
        'filter.return_value.first.return_value': existing_user
    }))
    
    # Execute and assert exception
    with pytest.raises(HTTPException) as exc_info:
        create_user(mock_db, mock_user_create)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Username or email already registered"


test_cases = [
    # Empty username
    ("", "Username cannot be empty"),
    # Invalid characters
    ("user@name", "Username can only contain letters and numbers"),
    ("user_name", "Username can only contain letters and numbers"),
    # Length < 5
    ("user", "Username must be between 5-20 characters"),
    # Length > 20
    ("a_very_long_username_that_exceeds_limit", "Username must be between 5-20 characters"),
    # Valid username
    ("ValidUser123", None),  # No error expected
]

@pytest.mark.parametrize("username, expected_error", test_cases)
def test_validate_username(username, expected_error):
    """
    Test the User.validate_username method with various inputs.
    """
    if expected_error:
        with pytest.raises(ValueError) as exc_info:
            User.validate_username(username) 
        assert str(exc_info.value) == expected_error
    else:
        result = User.validate_username(username)
        assert result == username